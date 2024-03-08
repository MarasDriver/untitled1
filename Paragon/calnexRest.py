"""
calnexRest.py, version 2.3.0

This file provides a Python interface to Paragon-Neo and Attero.

Changes -----------------------------------------------------------------------
Version 2.0, 19 Feb 2020:
    Added a number of help functions for downloading reports

Version 2.1, 19 Oct 2021:
    All code now PEP8 Compliant
    Improvement to CAT & PFV report handling
    Wait for various app generation and measurement starts
    Clear MSE and ToD pending commands upon Neo initialise
    Improved command docstrings

    ---- Utility Functions ----
    PFV status monitoring
    Check if specific CAT measurement or app is running
    Instrument option license fitted check

Version 2.1.1 05 Jan 2022
    Neo initialise command clears pending configuration

Version 2.1.2 07 Feb 2022
    Improved CAT & PFV Live Mode detection

    ---- Utility Functions ----
    Added PFV report download

Version 2.1.3 26 Apr 2022
    Minor bug fixes

Version 2.1.4 24 Oct 2022
    Displays HTTP request error contents

Version 2.2 28 Nov 2022
    Moved CAT waits to separate pre-command check
    ---- Utility Functions ----
    Fixed file/folder download bug in Windows systems
    Added command to download a folder from instrument
    Added command to download session folders of the files currently
        loaded in CAT
    Added command to download files currently loaded in CAT
    Added command to get instrument folder elements

Version 2.3.0 27 Mar 2022
    Added check for no return in response.content
    Added backwards compatability for P100G CAT 'enable' command for
    addressing measurements
    ---- Utility Functions ----
    Added masks query and check commands
    Added statistics query command
    Added HTTP/HTTPS/SSL keywords and comms check to calnexInit process
"""

###############################################################################
#   Copyright (c) Calnex Solutions Ltd 2008 - 2023                            #
#                                                                             #
#   The contents of this file should not be copied or distributed             #
#   without permission being granted by Calnex Solutions Ltd.                 #
#                                                                             #
#   All rights reserved.                                                      #
#                                                                             #
###############################################################################

import os
import time
import json
import requests
import hashlib

_VERSION = "2.3.0"
_LAST_ERR = ""
_INSTRUMENT = ""
_HW_TYPE = ""
_AUTH_TOKEN = ""
_CAT_TIMEOUT = 20
_PFV_TIMEOUT = 20
_HTTP_TYPE = ''
_SSL_VERIFY = ''


def _raise_runtime_error(label):
    """
    Uses last error to raise a runtime error
    """
    raise RuntimeError(label)


def _check_for_error(label):
    """
    Uses last error to raise an exception.
    """
    global _LAST_ERR

    if len(_LAST_ERR) > 0:
        raise Exception("%s : %s" % (label, _LAST_ERR))


def _args_to_json(arg):
    """
    Convert from list to JSON and inject authentication token.
    """
    global _AUTH_TOKEN

    i = iter(arg)
    dictionary = dict(zip(i, i))
    dictionary["AuthToken"] = _AUTH_TOKEN
    return json.dumps(dictionary)


def _pre_cmd_behaviour(caller, url):
    """
    Executes commands before a specific user command based on calling
    function, hardware type and url, e.g. to ensure instrument is in
    a specific state before executing the command.

    Returns a modified URL if required, if not required, returns original
    url.
    """

    # Waits for CAT.  Reports are handled in their own function.
    # Trailing slash means the generic measurement command does
    # not match, and therefore runs without wait.
    wait_for_cat_urls = ['cat/chart/',
                         'cat/general/range',
                         'cat/measurement/',
                         ]

    for entry in wait_for_cat_urls:
        if entry in url:
            calnexWaitForCat()

    # Translates between Neo "isenabled" and P100G "enable" (CAT-5899)
    # P100G: cat/measurement/DelayReq/D/PDV/-/enable
    # NEO:   cat/measurement/DelayReq/D/PDV/-/isenabled
    # The tests for match below mean that the replacement is unique to the
    # correct command as of CATv30.
    if _HW_TYPE == 'Paragon-100G':

        match_all = 'cat/measurement'
        match_any = ['/-/isenabled', '/Rx/isenabled', '/Tx/isenabled']
        not_match_any = ['cat/measurement/trace/', '/threshold/enable']

        if caller in ('calnexGet', 'calnexSet'):
            if match_all in url:
                if any(substring in url for substring in match_any):
                    if not any(substring in url for substring
                               in not_match_any):

                        url = url.replace('isenabled', 'enable')

    return(url)


def _post_cmd_behaviour(caller, url):
    """
    Executes commands after a specific function call based on calling
    function, hardware type and url, e.g. to ensure instrument is in
    a specific state before returning.
    """

    if caller == 'calnexInit':

        if _HW_TYPE == 'Paragon-Neo':
            # Clear any pending commands from previous session:
            calnexSet('app/mse/clearpending')
            calnexSet('app/generation/tod/clearpending')

    if caller == 'calnexSet':

        if url == 'app/measurement/onepps/timeerror/start':
            # Wait for 1PPS measurement to start before returning, allows
            # immediately subsequent commands to address it. Does not
            # check status.
            calnexWaitForCatMeas('1ppsTEAbsolute')

        if url == 'app/conformance/generation/start':
            # Wait for generation to start before returning, allows
            # immediately subsequent commands to address it. Does not
            # check status.
            calnexWaitForAppRunState('ConformanceTest',
                                     'GenerationLocking', 10)

        if url == 'app/conformance/measurement/start':
            # Check if 1PPS measurement is selected, if so wait for it to start
            if calnexGet('app/conformance/measurement')[
                         'OnePps']['Value'] is True:
                calnexWaitForCatMeas('1ppsTEAbsolute')


def _set_comms(ip, http_type, ssl_verify):
    """Tries and sets HTTP or HTTPS communications with the instrument based
      on arguments passed from the calling script.

      For backwards compatability, if the user does not specify an argument for
      https_type or ssl_verify, a connection will be tried for both https
      and http. If either are specified, a https connection is assumed to be
      mandated and http will not be tried.
      """

    global _HTTP_TYPE, _SSL_VERIFY

    def try_comms(ip, typ, ver):

        url_prefix = typ + "://" + ip + "/api/"
        url_suffix = 'instrument/software/buildversion'
        url = url_prefix + url_suffix

        response = requests.get(
            "{0}?format=json".format(url),
            data='',
            headers={'Content-Type': 'application/json'},
            verify=ver
            )
        response.raise_for_status()
        ret = response.json()

    if http_type not in ('http', 'https', None):
        print(http_type, "is not a valid HTTP type, "
              "use \"http\" or \"https\".")
        quit()

    # Set to strictest settings by default
    http_allowed = False
    https_allowed = False
    unverified_ssl_allowed = False

    if http_type in ('https', None):
        https_allowed = True

    if http_type in ('http', None):
        http_allowed = True

    if ssl_verify is False:
        # If the user did not specify a value for ssl_verify, assume
        # verification is required.
        unverified_ssl_allowed = True

    # Make the command strings for help message
    caller_http_cmd = ''
    caller_ssl_cmd = ''
    if http_type is not None:
        caller_http_cmd = ', http_type=' + '\"' + http_type + '\"'
    if ssl_verify is not None:
        caller_ssl_cmd = ', ssl_verify=' + caller_ssl_cmd

    if unverified_ssl_allowed:
        # Switch off Python warning as this is generated for all
        # subsequent unsecure calls
        print("INFO: SSL certificate validation disabled by user. Disabling \""
              "requests.packages.urllib3.exceptions.InsecureRequestWarning\"")
        requests.packages.urllib3.disable_warnings(
            requests.packages.urllib3.exceptions.InsecureRequestWarning)

    if https_allowed:
        # print("INFO: Trying HTTPS connection...")
        try:
            # If the user has explicitly set verification off, raise an SSL
            # error so that it is dealt with as part of that error path.
            if ssl_verify is False:
                raise requests.exceptions.SSLError

            try_comms(ip, 'https', ssl_verify)
            print("INFO: Connected to Neo \"" + ip + "\" using HTTPS/SSL")
            _HTTP_TYPE = 'https'
            _SSL_VERIFY = ssl_verify
            return

        except requests.exceptions.SSLError as exc:
            # If there is a problem with the SSL certificate verification,
            #  or the user has set verfication off'
            if unverified_ssl_allowed:
                try:
                    print("WARNING: The SSL certificate loaded on Neo", ip,
                          "is not validated as SSL verification was turned "
                          "OFF by user calnexInit command, adding certificate "
                          "verification is strongly advised.")

                    # print('INFO: Trying HTTPS with SSL verfication '
                    #        'disabled...')
                    try_comms(ip, 'https', False)
                    print("INFO: Connected to Neo \"" + ip + "\" using HTTPS "
                          "with unverified SSL certificate")
                    _HTTP_TYPE = 'https'
                    _SSL_VERIFY = False
                    return

                except Exception as exc:
                    # This is a catch-all for problems subsequent to switching
                    #  off certificate verification.
                    print('ERROR:', exc)
                    print("WARNING: Cannot connect to Neo using HTTPS/SSL "
                          "with the currently configured settings for "
                          "calnexInit")

            elif not unverified_ssl_allowed:
                if http_type == 'https' or ssl_verify not in (False, None):
                    # If the user has explicitly requested HTTPS or
                    # certificate verification then print errors and quit.
                    # If not, drop out and try HTTP.
                    print('ERROR:', exc)
                    print("ERROR: SSL Certficate error. To use HTTPS/SSL, load"
                          " a valid SSL certificate onto Neo and configure "
                          "Python and the calnexInit command appropriately. "
                          "Alternatively (not recommended) certificate "
                          "verification can be switched off using the "
                          "following calnexInit command:")
                    print("     calnexInit(\"" + ip + "\"" + caller_http_cmd +
                          ", ssl_verify=False)")
                    quit()

        except Exception as exc:
            if http_type == 'https' or ssl_verify not in (False, None):
                # If the user has explicitly requested HTTPS or
                # certificate verification then print a warning and quit.
                # If not, drop out and try HTTP.
                print('ERROR:', exc)
                print("ERROR: Cannot connect to Neo \"" + ip + "\" using "
                      " HTTPS/SSL. Check network, Python, and Neo "
                      "configuration.")
                quit()

    if http_allowed:
        # print("INFO: Trying HTTP connection...")
        try:
            try_comms(ip, 'http', 'N/A')
            print("INFO: Connected to Neo \"" + ip + "\" using HTTP")
            _HTTP_TYPE = 'http'
            _SSL_VERIFY = 'N/A'

        except requests.exceptions.ConnectionError as exc:
            print('ERROR:', exc)
            print("ERROR: Cannot connect to Neo at", ip,
                  "using HTTP. Check network, Python, and Neo configuration.")
            quit()

    elif not http_allowed:
        print("ERROR: Cannot connect to Neo at", ip,
              "using HTTPS. Check network, Python, and Neo configuration.")
        quit()


def calnexInit(ip_addr, **kwargs):
    """
    Initialises the connection to the instrument.

    Arguments:
        IP Address (str): The IP address of the instrument
    """
    global _INSTRUMENT
    global _HW_TYPE
    global _LAST_ERR
    global _AUTH_TOKEN

    _LAST_ERR = ""

    if ip_addr == "":

        _LAST_ERR = "Must specify an IP Address for the instrument"

    else:
        ip_address = ip_addr

        # Setup communications (http/https/ssl)
        http_type = kwargs.get('http_type', None)
        ssl_verify = kwargs.get('ssl_verify', None)
        _set_comms(ip_addr, http_type, ssl_verify)

        _INSTRUMENT = _HTTP_TYPE + "://" + ip_address + "/api/"
        try:
            _HW_TYPE = calnexGetVal("instrument/information", "HwType")
            sn = calnexGetVal("instrument/information", "SerialNumber")
            features = calnexGetVal("instrument/options/features", "Features")

            # Authentication
            password = kwargs.get('password', None)
            if ("Authentication" in features):
                if password is None:
                    _LAST_ERR = "Instrument authentication is enabled, " \
                                    "but no password has been supplied"
                else:
                    if (len(password) != 32):
                        password = hashlib.md5(
                            password.encode('utf-8')).hexdigest()
                    _AUTH_TOKEN = calnexGet("authentication/login",
                                            "Password", password)["AuthToken"]
            else:
                if(password is not None):
                    print("WARNING: Authentication option not fitted, "
                          "supplied password not required!")

        except requests.exceptions.RequestException as exc:
            if exc.response is not None:
                response_content = '\n' + str(exc.response.content)
            else:
                response_content = ''

            _LAST_ERR = str(exc) + response_content

        print("%s %s" % (_HW_TYPE, sn))

    _check_for_error("calnexInit")

    # Specific initliasiation based on hardware type
    _post_cmd_behaviour('calnexInit', None)


def calnexGet(url, *arg):
    """
    Reads the specified setting from the connected instrument.

    Returns:
        Value from instrument.
    """
    global _INSTRUMENT
    global _LAST_ERR

    _LAST_ERR = ""
    if _INSTRUMENT == "":
        _LAST_ERR = "IP address not configured \
                    - call calnexInit before any other calls"
        ret = ""
    else:
        try:
            mod_url = _pre_cmd_behaviour('calnexGet', url)
            url = mod_url
            response = requests.get(
                "{0}{1}?format=json".format(_INSTRUMENT, url),
                data=_args_to_json(arg),
                headers={'Content-Type': 'application/json'},
                verify=_SSL_VERIFY)
            response.raise_for_status()
            ret = response.json()

        except requests.exceptions.RequestException as exc:
            if exc.response is not None:
                response_content = '\n' + str(exc.response.content)
            else:
                response_content = ''

            _LAST_ERR = str(exc) + response_content

    _check_for_error("calnexGet %s" % (url))

    return ret


def calnexGetVal(url, arg):
    """
    Read a setting from the connected instrument and return a specified value.

    Returns:
        Specified value from instrument.
    """
    global _INSTRUMENT
    global _LAST_ERR
    res = calnexGet(url, arg)
    ret = res
    if arg not in res:
        _LAST_ERR = "\"" + arg + "\" does not exist in response: " + str(res)
    else:
        ret = res[arg]

    _check_for_error("calnexGetVal %s %s" % (url, arg))
    return ret


def calnexSet(url, *arg):
    """
    Write to a setting in the connected instrument.

    Returns:
        Nothing.
    """
    global _INSTRUMENT
    global _LAST_ERR

    _LAST_ERR = ""
    if _INSTRUMENT == "":
        _LAST_ERR = "IP address not configured, " \
                        "call calnexInit before any other calls"
    else:
        try:
            mod_url = _pre_cmd_behaviour('calnexSet', url)
            url = mod_url
            requests.put(
                "{0}{1}?format=json".format(_INSTRUMENT, url),
                _args_to_json(arg),
                headers={'Content-Type': 'application/json'},
                verify=_SSL_VERIFY
                ).raise_for_status()

        except requests.exceptions.RequestException as exc:
            if exc.response is not None:
                response_content = '\n' + str(exc.response.content)
            else:
                response_content = ''

            _LAST_ERR = str(exc) + response_content

    _check_for_error("calnexSet %s" % (url))

    _post_cmd_behaviour('calnexSet', url)


def calnexCreate(url, *arg):
    """
    Creates an object on the connected instrument, e.g. PDF report.

    Currently there is no way to check if PFV has a capture loaded prior to
    attemping to generate report, no capture loaded results in
    "400 Client Error: ArgumentException".

    Returns:
        Nothing.

    Raises:
        Runtime error if CAT measurements query results in no data
        as suspicion is no measurements are loaded.
        Runtime error if CAT report is requested while measurement is running
        Runtime error if PFV option is not fitted.
        Runtime error if wait for appplication processing or
        loading times out.
    """
    global _INSTRUMENT
    global _LAST_ERR

    _LAST_ERR = ""

    def _create_cat_report(arg):
        """
        Creates CAT Report, includes wait for 60s for report functions to
        complete.

        Returns:
            Nothing.

        Raises:
            Runtime error if CAT measurements query results in no data
            as suspicion is no measurements are loaded.
            Runtime error if CAT measurement is running.
            Runtime error if wait for processing or loading times out.
        """

        global _LAST_ERR

        try:
            calnexGet('cat/measurement')

        except ValueError:
            _raise_runtime_error(
                "CAT measurement query returned no data, "
                "this usually means no measurements are loaded.")

        # Wait 5 seconds for live/starvation mode to exit,
        # if not exited assume measurement has not been stopped.
        cat_ready = False
        retry = 0
        retries = 10

        while cat_ready is False:
            if retry < retries:
                cat_status = calnexGet('cat/general/status')
                cat_live_mode = cat_status['IsInLiveMode']
                cat_starv_mode = cat_status['IsInStarvationMode']

                if True not in (cat_live_mode, cat_starv_mode):
                    cat_ready = True

                else:
                    retry = retry + 1
                    time.sleep(0.5)

            else:
                _raise_runtime_error(
                    "Unable to generate report while measurement is running. "
                    "Stop all measurements before generating report.")

        if calnexIsCatDone():
            calnexSet("cat/report/prepare")

        else:
            _raise_runtime_error(
                "Unable to prepare report. "
                "Wait for CAT to become ready timed out.")

        if calnexIsCatDone():
            try:
                requests.post(
                    "{0}{1}".format(_INSTRUMENT, 'cat/report'),
                    _args_to_json(arg),
                    headers={'Content-Type': 'application/json'},
                    verify=_SSL_VERIFY
                    ).raise_for_status()

            except requests.exceptions.RequestException as exc:
                if exc.response is not None:
                    response_content = '\n' + str(exc.response.content)
                else:
                    response_content = ''

                _LAST_ERR = str(exc) + response_content

        else:
            _raise_runtime_error(
                "Unable to generate report. "
                "Wait for CAT to become ready timed out.")

        _check_for_error("calnexCreate %s" % (url))

    def _create_pfv_report(arg):
        """
        Creates PFV Report, includes waits 60s for report functions to
        complete.

        Currently there is no way to test if PFV has a capture loaded prior to
        attemping to generate report, no capture loaded results in
        "400 Client Error: ArgumentException".

        Returns:
            Nothing.

        Raises:
            Runtime error if PFV option is not fitted.
            Runtime error if wait for processing or loading times out.
        """

        global _LAST_ERR

        if calnexOptionFitted('NEO-PFV') is not True:
            _raise_runtime_error(
                "PFV option not fitted. ")

        pfv_ready = False
        retry = 0
        retries = 10

        while pfv_ready is False:
            if retry < retries:
                pfv_status = calnexGet('pfv/general/status')
                pfv_live_mode = pfv_status['IsInLiveMode']
                pfv_starv_mode = pfv_status['IsInStarvationMode']

                if True not in (pfv_live_mode, pfv_starv_mode):
                    pfv_ready = True

                else:
                    retry = retry + 1
                    time.sleep(0.5)

            else:
                _raise_runtime_error(
                    "Unable to generate report while measurement is running. "
                    "Stop all measurements before generating report.")

        if calnexIsPfvDone():
            calnexSet("pfv/report/prepare")

        else:
            _raise_runtime_error(
                "Unable to prepare report. Wait for PFV to "
                "become ready timed out.")

        if calnexIsPfvDone():
            try:
                requests.post(
                    "{0}{1}".format(_INSTRUMENT, 'pfv/report'),
                    _args_to_json(arg),
                    headers={'Content-Type': 'application/json'},
                    verify=_SSL_VERIFY
                    ).raise_for_status()

            except requests.exceptions.RequestException as exc:
                if exc.response is not None:
                    response_content = '\n' + str(exc.response.content)
                else:
                    response_content = ''

                _LAST_ERR = str(exc) + response_content

        else:
            _raise_runtime_error(
                "Unable to generate report. Wait for PFV to "
                "become ready timed out.")

        _check_for_error("calnexCreate %s" % (url))

    if _INSTRUMENT == "":
        _LAST_ERR = "IP address not configured \
                    - call calnexInit before any other calls"

    else:
        if url == 'cat/report':
            _create_cat_report(arg)
            return

        if url == 'pfv/report':
            _create_pfv_report(arg)
            return

        try:
            requests.post(
                "{0}{1}".format(_INSTRUMENT, url),
                _args_to_json(arg),
                headers={'Content-Type': 'application/json'},
                verify=_SSL_VERIFY
                ).raise_for_status()

        except requests.exceptions.RequestException as exc:
            if exc.response is not None:
                response_content = '\n' + str(exc.response.content)
            else:
                response_content = ''

            _LAST_ERR = str(exc) + response_content

    _check_for_error("calnexCreate %s" % (url))


def calnexDel(url):
    """ TBD """
    global _INSTRUMENT
    global _AUTH_TOKEN
    global _LAST_ERR

    _LAST_ERR = ""
    if _INSTRUMENT == "":
        _LAST_ERR = "IP address not configured, " \
                        "call calnexInit before any other calls"
    else:
        try:
            requests.delete(
                "{0}{1}".format(_INSTRUMENT, url),
                data=json.dumps({'AuthToken': _AUTH_TOKEN}),
                headers={'Content-Type': 'application/json'},
                verify=_SSL_VERIFY
                ).raise_for_status()

        except requests.exceptions.RequestException as exc:
            if exc.response is not None:
                response_content = '\n' + str(exc.response.content)
            else:
                response_content = ''

            _LAST_ERR = str(exc) + response_content

    _check_for_error("calnexDel %s" % (url))


# --------------------------- Utility functions ---------------------------
# These functions provide expanded capability. Functionality  may change in
# future versions.


def calnexOptionFitted(option_id: str) -> bool:
    """Checks whether a licensable option is fitted
    Arguments:
        Option ID   (str)
            The Option ID of the licensable option e.g. 'NEO-PFV'
    Results:
        Fitted Status   (bool)
            Returns TRUE if the option is fitted.
            Returns FALSE if the option is not fitted.
    Raises:
        Exception if the requested Option ID is not found
    """

    global _LAST_ERR

    try:
        option_state = (next(item for item in
                        calnexGet('instrument/options/state')
                        if item['OptId'] == option_id)['OptState'])

    except StopIteration:
        _LAST_ERR = 'Requested instrument Option ID \"' + option_id + \
                    '\" is invalid'

        _check_for_error("calnexOptionFitted")

    if option_state == 'Fitted':
        return True

    else:
        return False


def calnexWaitForAppRunState(app_ref: str, target_runstate: str,
                             wait_time: int):
    """
    Waits for an application to be in a specific state before returning.
    Does not check for valididy of app or run state strings, if either
    is invalid will raise error.

    Arguments:
        Measurement Name    (str)
        Wait time [s]       (int)
    Returns:
        None
    Raises:
        Runtime error if specified app runstate is not reached before wait
        time expires.
    """

    global _LAST_ERR
    runstate_reached = False
    retry = 0
    retries = wait_time

    while runstate_reached is False:
        try:
            if retry < retries:
                app_runstate = (next(item for item in
                                calnexGet("app/all")
                                if item['AppRef'] == app_ref)['RunState'])
                if app_runstate == target_runstate:
                    runstate_reached = True
                else:
                    retry = retry + 1
                    time.sleep(1)

            else:
                _raise_runtime_error(
                    app_ref + ': Application did not enter desired ' +
                              'runstate: ' + target_runstate
                                )

        except StopIteration:
            _LAST_ERR = 'Requested application \"' + app_ref + \
                        '\" is invalid'

        _check_for_error("calnexWaitForAppRunState")


def calnexWaitForCatMeas(meas_name: str):
    """
    Waits 10 seconds for a specific measurement in CAT to start before
    returning. Does not check for valididy of measurement name,
    i.e. if a measurement name is invalid will raise error.

    Arguments:
        Measurement Name    (str)
    Returns:
        None
    Raises:
        Runtime error if measurement is not started.
    """

    time.sleep(10)
    cat_meas = calnexGet("cat/measurement")

    if not any(measurement['MeasurementName'] == meas_name for
               measurement in cat_meas):
        meas_started = False
        retry = 0
        retries = 20

        while meas_started is False:
            if retry < retries:
                cat_meas = calnexGet("cat/measurement")
                if any(measurement['MeasurementName'] == meas_name for
                        measurement in cat_meas):
                    meas_started = True
                else:
                    retry = retry + 1
                    time.sleep(0.5)

            else:
                _raise_runtime_error(
                    meas_name + ' not started after wait time expired.'
                )


def calnexIsPfvDone():
    """ Wait for the PFV to finish opening files and processing data
    Arguments:
        None
    Results:
          Returns TRUE when the PFV no longer indicates that it is
          processing or opening a file.
          The polling period is 1 second with a meximum of 60 re-tries.
          If the re-try count is exceeded, FALSE is returned.
      """
    global _PFV_TIMEOUT

    pfv_status = calnexGet("pfv/general/status")
    pfv_currently_processing = pfv_status["IsApiCurrentlyProcessing"]
    pfv_opening = pfv_status["IsOpeningInProgress"]
    retry = 0

    while pfv_currently_processing or pfv_opening:
        time.sleep(1)
        pfv_status = calnexGet("pfv/general/status")
        pfv_currently_processing = pfv_status["IsApiCurrentlyProcessing"]
        pfv_opening = pfv_status["IsOpeningInProgress"]

        retry = retry + 1
        if retry > _PFV_TIMEOUT:
            return False

    return True


def calnexWaitForCat():
    """
    Waits for CAT to finish opening files and processing data before
    Returning. Raises runtime error if wait times out.

    Arguments:
        None
    Returns:
        None
    Raises:
        Runtime error if CAT does not is not reached before wait
        time expires.
    """

    if calnexIsCatDone():
        return

    else:
        _raise_runtime_error(
            "Wait for CAT to become ready timed out.")


def calnexIsCatDone():
    """ Wait for the CAT to finish opening files and processing data
    Arguments:
        None
    Returns:
        Returns TRUE when the CAT no longer indicates that it is
        processing or opening a file.
        The polling period is 1 second with a maximum of 60 re-tries.
        If the re-try count is exceeded, FALSE is returned.
    Raises:
        Nothing.
    """
    global _CAT_TIMEOUT

    cat_status = calnexGet("cat/general/status")
    cat_currently_processing = cat_status["IsApiCurrentlyProcessing"]
    cat_opening = cat_status["IsOpeningInProgress"]
    retry = 0

    while cat_currently_processing or cat_opening:
        time.sleep(1)
        cat_status = calnexGet("cat/general/status")
        cat_currently_processing = cat_status["IsApiCurrentlyProcessing"]
        cat_opening = cat_status["IsOpeningInProgress"]
        retry = retry + 1
        if retry > _CAT_TIMEOUT:
            return False

    return True


def calnexDownloadFile(folder_type: str, src_folder: str,
                       filename: str, dest_folder: str):
    """
    Download a file from the instrument
    Arguments:
        folder_type	str
            "SessionsFolder" or "ReportFolder"
        src_folder	str
            The name of the folder on the instrument. For sessions files
            this is the name of the session folder e.g. Session_<date>
        filename	str
            The name of the file - for capture files, this is the name of
            the file in the Session folder
        dest_folder	str
            The name of the folder on the local machine where the
            remote file will be saved
    Results:
        Raises an error if the file cannot be found on the instrument.
        Raises an error if the destination folder does nt exist.
        If the local file or folder can't be accessed then Python will raise a
        file access error.
    """
    global _LAST_ERR
    global _INSTRUMENT
    global _AUTH_TOKEN

    if os.path.exists(dest_folder) is False:
        _raise_runtime_error(
            'Destination folder \'' + dest_folder + '\' does not exist.'
            )

    # The Neo URL uses forward slashes only
    src_folder = src_folder.replace("\\", "/")

    # If there is no "/" at the end of the folder name, add one
    if not src_folder.endswith('/'):
        src_folder = src_folder + '/'

    remote_file = src_folder + filename

    url = \
        "cat/filecommander/download/" + folder_type + \
        "?AsAttachment=true&FileId=" + remote_file
    local_file = os.path.join(dest_folder, filename)
    local_fid = open(local_file, "wb")

    try:
        response = requests.get("{0}{1}".format(_INSTRUMENT, url),
                                data=json.dumps({'AuthToken': _AUTH_TOKEN}))
        response.raise_for_status()
        local_fid.write(response.content)

    except requests.exceptions.RequestException as exc:
        if exc.response is not None:
            response_content = '\n' + str(exc.response.content)
        else:
            response_content = ''

        _LAST_ERR = str(exc) + response_content

    local_fid.close()

    _check_for_error(
        "calnexDownloadFile: Unable to download " + filename +
        " from " + src_folder)


def calnexDownloadFolder(folder_type: str, src_folder: str,
                         dest_folder: str = "./", new_folder_name: str = None):
    """
    Downloads a folder from the instrument.  Creates the local folder with the
    same name as on the instrument, unless a new folder name is specified.
    Arguments:
        folder_type	str
            "SessionsFolder" or "ReportFolder"
        src_folder:	str
            The name of the folder on the instrument. For sessions files
            this is the name of the session folder e.g. Session_<date>
        dest_folder	str (optional)
            The name of the folder on the local machine where the
            remote file will be saved. If none is specified defaults to the
            current folder.
        new_folder_name str (optional)
            The new name for the copied folder.
    Results:
        Raises an error if the folder cannot be found on the instrument
        If the local folder can't be accessed then Python will raise an
        error.
    """

    target_files = calnexGetFolderElements(folder_type,
                                           child_element=src_folder)

    if os.path.exists(dest_folder) is False:
        _raise_runtime_error(
            'Destination folder \'' + dest_folder + '\' does not exist.'
            )

    if new_folder_name is not None:
        folder_name = new_folder_name
    else:
        folder_name = src_folder

    local_folder = os.path.join(dest_folder, folder_name)
    if os.path.exists(local_folder) is False:
        os.mkdir(local_folder)

    for target_file in target_files['ChildrenElements']:
        calnexDownloadFile(folder_type, src_folder, target_file,
                           local_folder)


def calnexGetFolderElements(folder_type, child_element=None):
    """Returns a dictionary containing information about the elements in the
    specified instrument folder, e.g. "SessionsFolder".  The child elements
    (files and/or folders) are a list in the 'ChildrenElements' key.

    Arguments:
        folder_type str
            The folder type on the instrument, e.g. "SessionsFolder"
        child_element str (Optional)
            The child element to be addressed, e.g. sub-folder or file.
            Defaults to none.
    Results:
        HTTP Error if target element does not exist.
    Returns:
        Dictionary containing information about the specified folder
        elements.
    """

    global _INSTRUMENT
    global _LAST_ERR

    url = "cat/filecommander/" + folder_type + '?format=json'

    if child_element is not None:
        url += "&FileId=" + child_element

    try:
        response = requests.get(
            "{0}{1}".format(_INSTRUMENT, url),
            data=json.dumps({'AuthToken': _AUTH_TOKEN}))
        response.raise_for_status()
        ret = response.json()

    except requests.exceptions.RequestException as exc:
        if exc.response is not None:
            response_content = '\n' + str(exc.response.content)
        else:
            response_content = ''

        _LAST_ERR = str(exc) + response_content

    _check_for_error("calnexGetFolderElements %s" % (url))

    return(ret)


def calnexDownloadCatFiles(dest_folder: str = './', sub_folder: str = None):
    """
    Downloads all capture files currently loaded into CAT to a local folder.
    Defaults to the current folder unless a sub-folder is specified.

    Arguments:
        dest_folder	str
            The name of the folder on the local machine where the
            remote files will be saved
        sub_folder  str (Optional)
            The sub-folder where the files are to be copied to.  If this does
            not exist it will be created.
    Results:
        If the local destination folder does not exist then the wrapper will
        raise a runtime error.
        If there are duplicate filenames in the download set, the wrapper will
        raise a runtime error, this is to prevent loss of data.
        If the local file or folder can't be accessed then Python will raise a
        file access error.
    Returns:
        List of dictionaries of the session files and folders
    """

    calnexWaitForCat()
    measurements = calnexGet('cat/measurement')

    loaded_files = []

    for entry in measurements:
        for k, v in entry.items():
            if k == 'Filename':
                v = v.replace('/home/calnex/Calnex100G/Sessions', '')
                loaded_files.append({})
                loaded_files[-1]['Folder'] = '.' + v.rsplit('/', 1)[0] + '/'
                loaded_files[-1]['FileName'] = v.rsplit('/', 1)[1]

    loaded_files = sorted(loaded_files, key=lambda d: d['Folder'])

    # Remove duplicates in the measurement list
    target_files = [i for n, i in enumerate(loaded_files)
                    if i not in loaded_files[n + 1:]]

    # Check for duplicate filenames - as all are going into the same folder
    # duplicates will result in overwritten files
    filenames = set()
    for item in target_files:
        filenames.add(item['FileName'])

    if len(filenames) < len(target_files):
        _raise_runtime_error(
            'Duplicate filenames exist in download set.  Use the '
            '\"calnexDownloadCATSessions()\" command instead to download '
            'to separate folders'
        )

    for entry in target_files:
        src_folder = entry['Folder']
        filename = entry['FileName']

        if os.path.exists(dest_folder) is False:
            _raise_runtime_error(
                'Destination folder \'' + dest_folder + '\' does not exist.'
                )

        if sub_folder is not None:
            local_folder = os.path.join(dest_folder, sub_folder)
        else:
            local_folder = dest_folder

        if os.path.exists(local_folder) is False:
            os.mkdir(local_folder)

        calnexDownloadFile('SessionsFolder', src_folder, filename,
                           local_folder)

    return(target_files)


def calnexDownloadCatSessions(files: str = 'All',
                              dest_folder: str = './',
                              new_subfolder: str = None):
    """
    Downloads the session folders of the captures currently loaded into CAT
    to a local folder.  If a new folder name is specified and it does not
    exist, it will be created.
    Subfolders are created with the same session folder name as on the
    instrument.

    Arguments:
        files str
            "All":
                (Default) Downloads all files in all the session folders
                where a file from that session folder is currently loaded into
                CAT.  This is primarily to get all PortEvents100.CDF.
            "LoadedOnly":
                Downloads only the files that are currently loaded into
                CAT.  The files will still be int there deparate
        dest_folder	str
            The name of the folder on the local machine where the
            remote folders will be copied to.
    Raises:
        If the local destination folder does not exist then the wrapper will
        raise a runtime error.
        If the local file or folder can't be accessed then Python will raise a
        file access error.
    Returns:
        List of dictionaries of the session files and folders
    """

    file_selectors = ['All', 'LoadedOnly']
    if files not in file_selectors:
        _raise_runtime_error(
            'Download file selection type: \'' + files + '\' is not valid.'
            ' Allowable types: ' + str(file_selectors)
            )

    calnexWaitForCat()
    measurements = calnexGet('cat/measurement')

    # For All, get the folders of open measurements in CAT then put all
    # elements from those folders into the download list.
    # For loadedOnly, get the specific path of all files in the measurement
    # list in CAT, remove duplicates to make the download list

    target_files = []

    if files == 'All':
        current_session_folders = set()
        for entry in measurements:
            for k, v in entry.items():
                if k == "Filename":
                    v = v.replace('/home/calnex/Calnex100G/Sessions', '')
                    current_session_folders.add('.' + v.rsplit('/', 1)[0]
                                                + '/')

        for folder in current_session_folders:
            elements = calnexGetFolderElements('SessionsFolder',
                                               child_element=folder)
            for element in elements['ChildrenElements']:
                child_element = calnexGetFolderElements('SessionsFolder',
                                                        folder + element)
                if not child_element['IsDirectory']:
                    target_files.append({})
                    target_files[-1]['Folder'] = folder
                    target_files[-1]['FileName'] = element

    if files == 'LoadedOnly':
        loaded_files = []
        for entry in measurements:
            for k, v in entry.items():
                if k == 'Filename':
                    v = v.replace('/home/calnex/Calnex100G/Sessions', '')
                    loaded_files.append({})
                    loaded_files[-1]['Folder'] = '.' + \
                                                 v.rsplit('/', 1)[0] + '/'
                    loaded_files[-1]['FileName'] = v.rsplit('/', 1)[1]

        # Remove duplicates in the measurement list
        target_files = [i for n, i in enumerate(loaded_files)
                        if i not in loaded_files[n + 1:]]

    target_files = sorted(target_files, key=lambda d: d['Folder'])

    if os.path.exists(dest_folder) is False:
        _raise_runtime_error(
            'Destination folder \'' + dest_folder + '\' does not exist.'
            )

    if new_subfolder is not None:
        new_folder_path = os.path.join(dest_folder, new_subfolder)
        if os.path.exists(new_folder_path):
            _raise_runtime_error(
                'Specified new subfolder \'' + new_folder_path + '\' '
                'already exists. Unable to create new subfolder.'
                )
        os.mkdir(new_folder_path)
        dest_folder = new_folder_path

    for entry in target_files:
        src_folder = entry['Folder']
        filename = entry['FileName']

        local_folder = os.path.join(dest_folder, src_folder)
        if os.path.exists(local_folder) is False:
            os.mkdir(local_folder)

        calnexDownloadFile('SessionsFolder', src_folder, filename,
                           local_folder)

    return(target_files)


def calnexCatGenerateReport(report_name: str,
                            dest_folder="./", with_charts=True):
    """
    Generate a report in the CAT and then download it to the local PC
    The measurement must have been stopped before a report can be generated

    Parameters:
        reportName: (str)
            The name of the report to be generated
        destFolder: (str), optional
            The name of the folder on the local PC where the report will
            be saved. The path to the folder will be created if required.
            If destFolder is not specified then the report will be
            saved in the current working directory (i.e. where
            the script is executing)
        withCharts: bool, optional
            If True (the default), then charts will be included in the report.
    Returns:
        None
    Raises:
       None
    """
    calnexCreate("cat/report", "RenderCharts", with_charts,
                 "ReportFilename", report_name)

    # Report is now generated. Download it.
    calnexDownloadFile(
        "ReportFolder", "./", report_name, dest_folder)


def calnexPfvGenerateReport(report_name: str,
                            dest_folder="./", with_charts=True):
    """
    Generate a report in the PFV and then download it to the local PC
    The measurement must have been stopped before a report can be generated

    Parameters:
        reportName: (str)
            The name of the report to be generated
        destFolder: (str), optional
            The name of the folder on the local PC where the report will
            be saved. The path to the folder will be created if required.
            If destFolder is not specified then the report will be
            saved in the current working directory (i.e. where
            the script is executing)
        withCharts: bool, optional
            If True (the default), then charts will be included in the report.
    Returns:
        None
    Raises:
       None
    """

    calnexCreate("pfv/report", "RenderCharts", with_charts,
                 "ReportFilename", report_name)

    calnexDownloadFile("PfvReportFolder", "./", report_name, dest_folder)


def calnexCatGetAllMasksStatus(to_screen: bool = False):
    """
    Queries all currently enabled measurements that have masks or thesholds set
    and returns their details, mask status, and the calnexRest.py command to
    get the individual mask value directly from a user script.

    For ease of use, the status of both "masks" and "thresholds" are both held
    as "MaskStatus" in the returned object.

    Note: The commands to SET masks and thresholds can be easily determined by
          using the "Script Recorder" function of the instrument.

    Returns:
        A list of dictionaries, each dictionary holds:
            MeasurementName: The API name of the measurement (e.g. "2Way")
            MetricType: The API name of the metric (e.g. "TIMEERROR")
            MaskName: The mask or theshold name
            MaskState: Pass, Fail, Insufficient Data
            WrapperGetCmd:   The command to be used in a user script that will
                             return the pass/fail status of that mask
    Raises:
        None
    """

    masks_status = []
    no_mask_values = ['No Mask', 'NoMask']

    measurements = calnexGet('cat/measurement')
    for measurement in measurements:
        if measurement['Enabled'] is True:
            for metric_type in measurement['Metrics']:
                if metric_type['IsEnabled'] is True:
                    url_suffix = measurement['MeasurementName'] + '/' + \
                                 measurement['PortName'] + '/' + \
                                 metric_type['MetricType'] + '/' + \
                                 metric_type['ExtId']

                    get_metric_url = 'cat/measurement/' + url_suffix
                    metric = calnexGet(get_metric_url)

                    if metric['MaskName'] not in no_mask_values:
                        masks_status.append({})
                        masks_status[-1]['MeasurementName'] = \
                            measurement['MeasurementName']
                        masks_status[-1]['MetricType'] = \
                            metric_type['MetricType']
                        masks_status[-1]['MaskName'] = \
                            metric['MaskName']
                        masks_status[-1]['MaskState'] = \
                            metric['MaskState']

                        calnex_getval_cmd = 'calnexGetVal(' + \
                                            '\'' + get_metric_url + \
                                            '\'' + ', ' + '\'MaskState' + '\')'
                        masks_status[-1]['WrapperGetCmd'] = calnex_getval_cmd

                    # Currently in place to catch "Supplementary Metrics"
                    # Pk-Pk ( as of CAT v29)
                    if 'Thresholds' in metric:
                        for threshold in metric['Thresholds']:
                            if threshold['MaskState'] not in no_mask_values:
                                masks_status.append({})
                                masks_status[-1]['MeasurementName'] = \
                                    measurement['MeasurementName']
                                masks_status[-1]['MetricType'] = \
                                    metric_type['MetricType']
                                masks_status[-1]['ThresholdName'] = \
                                    threshold['ThresholdName']
                                masks_status[-1]['MaskState'] = \
                                    threshold['MaskState']

                                # Pk-Pk can be retrieved from the
                                # Statistics call
                                if threshold['ThresholdName'] == 'Pk-Pk Limit':
                                    get_mask_status_suffix = '/statistics/PkPk'

                                    calnex_getval_cmd = 'calnexGetVal(' + \
                                        '\'' + get_metric_url + \
                                        get_mask_status_suffix + \
                                        '\'' + ', ' + '\'PassFailResult' + \
                                        '\')'

                                    masks_status[-1]['WrapperGetCmd'] = \
                                        calnex_getval_cmd

    if to_screen is True:
        for entry in masks_status:

            if 'MaskName' in entry:
                name = 'MaskName'
            else:
                name = 'ThresholdName'

            print('\n' + 'COMMAND    : ' + entry['WrapperGetCmd'])
            print('METRIC     : ' + entry['MeasurementName'] +
                  ' ' + entry['MetricType'])
            print('MASK       :' + ' ' + entry[name])
            print('MASK STATE : ' + entry['MaskState'])

    return masks_status


def calnexDoAllMeasurementsPass(pass_insuf_data: bool = False):
    """
    Checks mask status of currently enabled measurements that have a mask or
    threshold set and returns TRUE if all masks are passed, and FALSE if any
    mask is not passed.

    Parameters:
        pass_insuf_data: (Boolean) sets whether a metric that does not
                          have enough data to be calculated is treated as a
                          pass (set to True) or a fail (set to False).

    Returns:
        TRUE if all masks pass the criteria
        FALSE if the masks do not pass the criteria
    """

    mask_pass_values = ['Pass']
    if pass_insuf_data is True:
        mask_pass_values.append('InsufficientData')

    masks_status = calnexCatGetAllMasksStatus()

    for entry in masks_status:
        if entry['MaskState'] not in mask_pass_values:
            return False

    return True


def calnexGetMeasurementStats(to_screen: bool = False,
                              timing_only: bool = True):
    """
    A utility function to assist with addressing measurement statistics.
    Queries all currently enabled measurements that currently have statistics
    associated with them, and returns selected details and the calnexRest.py
    command to get the individual statistic value directly from a user script.

    Parameters:
        to_screen: (Boolean) if set to True, prints the contents of the
        statistics to the screen.  Useful for quickly identifying the
        script commands.

        timing_only: (Boolean) if set to True, statistics NOT
        directly related to timing errors (e.g. message rates, packet counts,
        clock types) will not be returned.

    Returns:
        A list of dictionaries, each dictionary holds:
            MeasurementName: The API name of the measurement (e.g. "2Way")
            MetricType:      The API name of the metric (e.g. "TIMEERROR")
            StatisticsName:  The full name of the statistic, with its unit
            StatisticsValue: The current value of the statistic
            WrapperGetCmd:   The command to be used in a user script that will
                             return the value of that statistic
    Raises:
        None
    """

    statistics = []
    timing_stats = ['cTe', 'PkPk', 'Mean', 'Min', 'Max', 'Range', 'StdDev']

    measurements = calnexGet('cat/measurement')
    for measurement in measurements:
        if measurement['Enabled'] is True:
            for metric_type in measurement['Metrics']:
                if metric_type['IsEnabled'] is True:
                    url_suffix = measurement['MeasurementName'] + '/' + \
                                 measurement['PortName'] + '/' + \
                                 metric_type['MetricType'] + '/' + \
                                 metric_type['ExtId']

                    try:
                        get_stats_url = 'cat/measurement/' + \
                            url_suffix + '/statistics/'
                        stats = calnexGet(get_stats_url)

                    # assume an exception here if the metric does not
                    # have any statistics
                    except Exception as exc:
                        continue

                    for stat in stats['StatisticsFields']:
                        stat_id = stat['StatisticsId']
                        stat_name = stat['StatisticsName']
                        stat_url = get_stats_url + '/' + stat_id
                        stat_value_key = 'StatisticsValue'

                        stat_value = calnexGetVal(stat_url, stat_value_key)
                        calnex_getval_cmd = 'calnexGetVal(' + '\'' + \
                                            stat_url + '\'' + ', ' + \
                                            '\'StatisticsValue' + '\')'

                        statistics.append({})
                        statistics[-1]['MeasurementName'] = \
                            measurement['MeasurementName']
                        statistics[-1]['MetricType'] = \
                            metric_type['MetricType']
                        statistics[-1]['StatisticsId'] = stat_id
                        statistics[-1]['StatisticsName'] = stat_name
                        statistics[-1]['StatisticsValue'] = stat_value
                        statistics[-1]['WrapperGetCmd'] = calnex_getval_cmd

    if timing_only is True:
        # remove non timing related statistics
        for i in range(len(statistics) - 1, -1, -1):
            element = statistics[i]
            if element['StatisticsId'] not in timing_stats:
                del statistics[i]

    if to_screen is True:
        for entry in statistics:
            print('\n' + 'COMMAND   : ' + entry['WrapperGetCmd'])
            print('STATISTIC : ' + entry['MeasurementName'] +
                  ' ' + entry['MetricType'] + ' ' + entry['StatisticsName'])
            print('VALUE     : ' + entry['StatisticsValue'])

    return statistics


#
# Old syntax - kept for backwards compatibility
#


def p100get(url, *arg):
    """ Compatibility alias for matching calnexXXX """
    return calnexGet(url, *arg)


def p100set(url, *arg):
    """ Compatibility alias for matching calnexXXX """
    calnexSet(url, *arg)


def p100create(url, *arg):
    """ Compatibility alias for matching calnexXXX """
    calnexCreate(url, *arg)


def p100del(url):
    """ Compatibility alias for matching calnexXXX """
    calnexDel(url)


def a100get(url, *arg):
    """ Compatibility alias for matching calnexXXX """
    return calnexGet(url, *arg)


def a100set(url, *arg):
    """ Compatibility alias for matching calnexXXX """
    calnexSet(url, *arg)


def a100create(url, *arg):
    """ Compatibility alias for matching calnexXXX """
    calnexCreate(url, *arg)


def a100del(url):
    """ Compatibility alias for matching calnexXXX """
    calnexDel(url)


# Simple example and used for testing
if __name__ == "__main__":

    # The instrument IP address
    IP_ADDR = "192.168.1.1"

    # The interface to test
    INTERFACE = "qsfp28"

    from datetime import datetime

    def is_link_up(port):
        """ Is the link up on the specified port """
        eth_link = "UNDEFINED"
        link_state = "UNDEFINED"

        leds = calnexGet("results/statusleds")
        if port == 0:
            eth_link = 'ethLink_0'
        else:
            eth_link = 'ethLink_1'

        for led in leds:
            # print (led)
            if led['Name'] == eth_link:
                link_state = led['State']
        if link_state == 'Link':
            return True
        else:
            return False

    def is_good_pkts(port):
        """ Are packets being received on the specified port """
        eth_pkts = "UNDEFINED"
        pkts_state = "UNDEFINED"

        leds = calnexGet("results/statusleds")
        if port == 0:
            eth_pkts = 'ethPkt_0'
        else:
            eth_pkts = 'ethPkt_1'

        for led in leds:
            # print (led)
            if led['Name'] == eth_pkts:
                pkts_state = led['State']
        if pkts_state == 'GoodPackets':
            return True
        else:
            return False

    def is_ref_locked():
        """ Is the frequency reference locked """
        leds = calnexGet("results/statusleds")

        for led in leds:
            # print (led)
            if led['Name'] == 'refInClk':
                state = led['State']
        if state == 'Signal':
            return True
        else:
            return False

    def noise_generation_test(duration_s):
        """ Measure SyncE wander """
        print("--- Noise Generation ----------------------------\
                ----------------------------")
        # Start SyncE Wander measurement
        calnexSet("app/measurement/synce/wander/Port1/start")

        time.sleep(duration_s)

        # Stop SyncE Wander measurement
        calnexSet("app/measurement/synce/wander/Port1/stop")

        # Enable MTIE and TDEV in the CAT
        # calnexSet("cat/measurement/SyncE/A/MTIE/-/enable", "Value", True)
        # calnexSet("cat/measurement/SyncE/A/TDEV/-/enable", "Value", True)
        calnexSet("cat/measurement/SyncE/A/MTIE/-/isenabled", "Value", True)
        calnexSet("cat/measurement/SyncE/A/TDEV/-/isenabled", "Value", True)

        # Select the G.8262 mask and calculate
        calnexSet("cat/measurement/SyncE/A/MTIE/-/mask",
                  "MaskName", 'G.8262 Wander Generation EEC Op1')
        calnexSet("cat/general/calculate/start")
        calnexWaitForCat()

        # Get the pass/fail result from the CAT
        pf_mtie = calnexGetVal("cat/measurement/SyncE/A/MTIE/-", 'MaskState')
        pf_tdev = calnexGetVal("cat/measurement/SyncE/A/TDEV/-", 'MaskState')

        print("MTIE mask: {}   TDEV mask: {}". format(pf_mtie, pf_tdev))

    # Connect to the instrument
    calnexInit(IP_ADDR)
    # Print the instrument model
    MODEL = calnexGetVal("/instrument/information", "HwType")
    print(MODEL)

    # Select PTP and leave some time for the preset change
    calnexSet("instrument/preset", "Name", 'SyncE Wander')
    time.sleep(5)
    # Configure the reference - external 10MHz on BNC
    calnexSet("physical/references/in/clock/bnc/select")
    calnexSet("physical/references/in/clock/bnc", "Signal", '10M')
    # Configure the ethernet ports
    calnexSet("physical/port/ethernet/Port1/" + INTERFACE + "/select")

    # Check that the reference is locked
    ref_lock = is_ref_locked()
    if not ref_lock:
        print("Reference is not locked. Aborting...")
        exit(1)
    else:
        print("Reference is locked")

    # Check that the links are up and that we are seeing packets
    port1_link = is_link_up(1)
    port2_link = is_link_up(2)
    if not port1_link or not port2_link:
        print("Links are not up. Aborting...")
        exit(1)
    else:
        print("Links are up")

    port1_pkts = is_good_pkts(1)
    port2_pkts = is_good_pkts(2)
    if not port1_pkts or not port2_pkts:
        print("No packets being received. Aborting...")
        exit(1)
    else:
        print("Packets are being received")

    noise_generation_test(30)       # Should run for ~3000s

    # Generate the report and save it into the same folder as the script
    dt = datetime.today()
    dt_str = dt.strftime("%Y-%m-%dT%H-%M-%S")
    fname = "NoiseGen_" + dt_str + ".pdf"
    calnexCatGenerateReport(fname)
