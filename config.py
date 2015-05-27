class Config():

    dict = {}
    with open("config") as configFile:
        #TODO: empty lines check
            for line in configFile:
                key = line.split("=")[0]
                value = line.split("=")[1]
                dict[key] = value.rstrip()

    @staticmethod
    def getUsername():
        return Config.dict["username"]
    
    @staticmethod
    def getPassword():
        return Config.dict["password"]
    
    @staticmethod
    def getHost():
        return Config.dict["host"]
    
    @staticmethod
    def getDatabase():
        return Config.dict["database"]
    
    @staticmethod
    def getSocket():
        return Config.dict["socket"]
    
    @staticmethod
    def getAllParams():
        return Config.dict