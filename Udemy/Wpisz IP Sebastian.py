def is_ipv4(value):
    ip = value.split(".")
    if isinstance(value, str):
        if len(ip) == 4:
            success = 1
            for i in ip:
                try:
                    int(i)
                except Exception as error:
                    print("{0} value is not a int. error: {1}".format(
                          i, error))
                    success = 0
                    break
                if int(i) < 0 or int(i) > 254:
                    print("value should be in range from 0-254")
                    success = 0

            if success:break
                return value
            else:
                print("bad addres type")
        else:
            print("ip.v4 should look: 10.10.10.10")
    else:
        print("Bad type", type(value), type(str()))
    return None


print(is_ipv4("1.1.1.1"))
print(is_ipv4("1.-1.1.1"))
print(is_ipv4("1.1.257.1"))
print(is_ipv4("1.1.1.a"))
