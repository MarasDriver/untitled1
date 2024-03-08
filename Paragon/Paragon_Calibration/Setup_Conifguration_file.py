chosen=[]
mean_values_dict={"1000": 20,"100":20,"10G":3}
number_of_iterations={"1000": 4,"100":40,"10G":20}

class Setup_Config():
    def device_set(self):
        devices = ["54CR", "54x2"]
        # device = input("Which device do we calibrate? 54CR or 54x2?")
        device="54x2"
        while device not in devices:
            try:
                device = input("Please try again? 54CR or 54x2? ")
            except ValueError:
                print("It's not 54CR or 54x2!!!")
        chosen.append(device)
        self.device = "54x2"
        self.host = "10.12.152.14"
        self.port = 6037
        self.acc_port = 2
        self.mediatype = "copper"  # Use fiber or copper or coppersfp or coppersfp_synce
        self.paragon_speed = "100BASET"  # Use 1GBE or 10GBE or 100BASET
        self.paragon_mediaType = "ELECTRICAL"  # Use OPTICAL or ELECTRICAL
        self.speed_Phy="100" #<10/100/1000/10G>
        self.OSA_tested_speed="100-full" #copper: 10-full/100-full/auto/auto-10-full/auto-100-full/auto-1000-full/auto-1000-full-master/auto-1000-full-slave  # fiber:100-full/1000-full/10g-full/auto-1000-full
        self.OSA_other_speed = "auto-1000-full" #copper: 10-full/100-full/auto/auto-10-full/auto-100-full/auto-1000-full/auto-1000-full-master/auto-1000-full-slave  ###### fiber:100-full/1000-full/10g-full/auto-1000-full
        self.mean_value_threshold=mean_values_dict[run.speed_Phy]
        self.iterations=number_of_iterations[run.speed_Phy]
        return chosen,self.host,self.port,self.acc_port,self.mediatype,self.paragon_mediaType,self.paragon_speed,self.device,self.OSA_tested_speed,self.OSA_other_speed


run=Setup_Config()
run.device_set()
device=chosen[0]
