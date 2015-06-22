class Config():

    dict = {}
    with open("config") as configFile:
            for line in configFile:
                key = line.split("=")[0]
                value = line.split("=")[1]
                dict[key] = value.rstrip()

    @staticmethod
    def getUsername():
        return Config.dict["user"]
    
    @staticmethod
    def getPassword():
        return Config.dict["passwd"]
    
    @staticmethod
    def getHost():
        return Config.dict["host"]
    
    @staticmethod
    def getSocket():
        return Config.dict["socket"]
    
    @staticmethod
    def getAllDbParams():
        dictToReturn = {}
        dictToReturn['host'] = Config.getHost()
        dictToReturn['user'] = Config.getUsername()
        dictToReturn['passwd'] = Config.getPassword()
        try:
            dictToReturn['socket'] = Config.getSocket()
        except KeyError:
            pass
        return dictToReturn
    
    @staticmethod
    def getDetectionsTestPath():
        return Config.dict['detections_test_path']
    
    @staticmethod
    def getTracesTestPath():
        return Config.dict['traces_test_path']