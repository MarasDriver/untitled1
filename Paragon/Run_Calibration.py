running=1
repeat=0

def get_mean_value():
    cala_strona2 = open("Measurements 2WayTime.txt", "r")
    whole_file2 = cala_strona2.readlines()
    mean = float(whole_file2[4][4:-3])
    print("Actual Mean Value:", mean)
    return mean

while running!=0:
    while running==1:
        import Paragon_Calibr_Config
        path_for_measurement = Paragon_Calibr_Config.par.create_path()
        run_measure= Paragon_Calibr_Config.paragon_config.config_calibration("WTF")
        running=2
        while running==2:
            import Setup_Conifguration_file
            print("Running ==", running," " + Setup_Conifguration_file.run.device, Setup_Conifguration_file.run.host,
                  Setup_Conifguration_file.run.port)
            running=3
            while running == 3:
                import readPDF
                print("Running ==", running," Reading Measurements")
                pdf= readPDF.klasa_readPDF.czytaj(Paragon_Calibr_Config.ścieżkaPDF)
                pdf= readPDF.klasa_readPDF.zgarnij_linijki("3")
                running=4
                while running==4:
                    import Telnet_OSACalibrationXML
                    print("Running ==",running," GetPhyDelays")
                    val = Telnet_OSACalibrationXML.phy_Delays()
                    val.getPhyDelays()
                    running=5
                    while running==5:
                        print("Running ==", running, " Evaluating new Rx and Tx")
                        import Matematyka
                        licz = Matematyka.klasa_Matematyka()
                        old_mean=get_mean_value()
                        if old_mean> Setup_Conifguration_file.run.mean_value_threshold or old_mean<-Setup_Conifguration_file.run.mean_value_threshold:
                            print("Running ==", running, "Starting 2way mean value improvement")
                            running = 6
                        else:
                            running = 0
                            print("Running ==", running, "2Way mean value Pre calibrated under ",
                                  Setup_Conifguration_file.run.mean_value_threshold, "ns")
                        while running==6:
                            print("Running ==", running, "Setting new values in devTools-dc/SetPhyDelays")
                            val= Telnet_OSACalibrationXML.phy_Delays()
                            val.setDelays()
                            running=7
                            while running==7:
                                print("Running ==", running,"Verification of new Rx and Tx values, and deciding if another loop is required")
                                path_for_measurement = Paragon_Calibr_Config.par.create_path()
                                run_measure = Paragon_Calibr_Config.paragon_config.config_calibration("WTF")
                                pdf = readPDF.klasa_readPDF.czytaj(Paragon_Calibr_Config.ścieżkaPDF)
                                pdf = readPDF.klasa_readPDF.zgarnij_linijki("6")
                                policz= Matematyka.klasa_Matematyka()
                                new_mean=get_mean_value()
                                if new_mean> Setup_Conifguration_file.run.mean_value_threshold or new_mean<-Setup_Conifguration_file.run.mean_value_threshold:
                                    running = 8
                                    print("Running ==", running, "One more loop for 2way mean value improvement")
                                    repeat=1
                                else:
                                    running = 0
                                    print("Running ==", running, "2Way mean value Pre calibrated under ",
                                          Setup_Conifguration_file.run.mean_value_threshold, "ns")
                                    repeat=0

                            else:
                                running = 0
                        else:
                            running = 0

                    else:
                        running = 0

                else:
                    running = 0
            else:
                running = 0
        else:
            running = 0

        if repeat == 1:
            print("Running ==", running, "Repeating one more loop for 2way mean value improvement")
            running = 1
    else:
        running = 0
        print("Running ==",running, "Not Running")

print("Calibration Finished Succesfully")
