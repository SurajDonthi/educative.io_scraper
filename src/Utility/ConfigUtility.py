import configparser
import os.path
import shutil

from src.Common.Constants import constants
from src.Utility.FileUtility import FileUtility


class ConfigUtility:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.fileUtil = FileUtility()
        self.loadConfig()


    def loadConfig(self, path=constants.defaultConfigPath):
        self.checkAndResetConfig(path)
        self.config = configparser.ConfigParser()
        self.config.read(path)
        if not os.path.exists(self.config['ScraperConfig']["saveDirectory"]):
            self.checkAndResetConfig(path, forceReset=True)
            self.config.read(path)
        return self.config


    def checkAndResetConfig(self, path, forceReset=False):
        if path is not constants.commonConfigPath:
            if not self.checkKeys(path, "ScraperConfig"):
                print("ConfigUtility: Config file is corrupted. Replacing with default common config...")
                shutil.copy(constants.commonConfigPath, path)
            if forceReset:
                shutil.copy(constants.commonConfigPath, path)


    def updateConfig(self, configJson, sectionName, path=constants.defaultConfigPath):
        for key, value in configJson.items():
            self.config[sectionName][key] = str(value)
        with open(path, 'w') as configfile:
            self.config.write(configfile)


    def checkKeys(self, path, sectionName):
        self.config = configparser.ConfigParser()
        self.config.read(path)
        configKeys = set(self.config.options(sectionName))
        defaultConfigParse = configparser.ConfigParser()
        defaultConfigParse.read(constants.commonConfigPath)
        defaultConfigKeys = set(defaultConfigParse.options(sectionName))

        binaryversionKeyExists = 'binaryversion' in configKeys and 'binaryversion' in defaultConfigKeys
        binaryversionValuesMatch = (
                self.config.get(sectionName, 'binaryversion') == defaultConfigParse.get(sectionName, 'binaryversion')
        ) if binaryversionKeyExists else True

        return configKeys == defaultConfigKeys and binaryversionValuesMatch
