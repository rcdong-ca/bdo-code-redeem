from PyQt6.QtWidgets import *
import customWidgets as CW
from PyQt6.QtCore import *
from PageTools import *

import os
import yaml

class ConfigLayout(QVBoxLayout):
    configPath = os.path.dirname(os.path.abspath(__file__)) + "/config.yml"

    def __init__(self):
        super().__init__()
        self.regionWgt = CW.LabelComboBox(ConfigConstants.region, ["NAEU", "ASIA"])
        self.loginMethodWgt = CW.LabelComboBox(ConfigConstants.loginMethod, ["Steam", "PearlAbyss"])
        self.ffprofileWgt = CW.LabelTextBox(ConfigConstants.ffProfilePath)
        self.ffprofileTipWgt = QLabel("Info: profile path can be found by typing 'about:profiles' into Firefox")
        self.usernameWgt = CW.LabelTextBox(ConfigConstants.username)
        self.passwordWgt = CW.LabelTextBox(ConfigConstants.password)
        self.saveWgt = CW.SaveButton(self.saveData)
        self.addWidget(self.regionWgt)
        self.addWidget(self.loginMethodWgt)
        self.addWidget(self.ffprofileWgt)
        self.addWidget(self.ffprofileTipWgt)
        self.addWidget(self.usernameWgt)
        self.addWidget(self.passwordWgt)
        self.addWidget(self.saveWgt, 0, Qt.AlignmentFlag.AlignCenter)
        self.setSpacing(0)
        self.setContentsMargins(0,0,0,0)
        self.loadData()

    def getData(self):
        data = {
            self.regionWgt.getLabel(): self.regionWgt.getText(),
            self.loginMethodWgt.getLabel(): self.loginMethodWgt.getText(),
            self.ffprofileWgt.getLabel(): self.ffprofileWgt.getText(),
            self.usernameWgt.getLabel(): self.usernameWgt.getText(),
            self.passwordWgt.getLabel(): self.passwordWgt.getText()
        }
        return data

    def loadData(self):
        config = yaml.safe_load(open(self.configPath))
        self.regionWgt.setText(config[ConfigConstants.region])
        self.loginMethodWgt.setText(config[ConfigConstants.loginMethod])
        self.ffprofileWgt.setText(config[ConfigConstants.ffProfilePath])
        self.usernameWgt.setText(config[ConfigConstants.username])
        self.passwordWgt.setText(config[ConfigConstants.password])
        

    def saveData(self):
        data = {
            ConfigConstants.region: self.regionWgt.getText(),
            ConfigConstants.loginMethod: self.loginMethodWgt.getText(),
            ConfigConstants.ffProfilePath: self.ffprofileWgt.getText(),
            ConfigConstants.username: self.usernameWgt.getText(),
            ConfigConstants.password: self.passwordWgt.getText()
        }  
        with open(self.configPath, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
            logger.info(f"Saving config information:\n {data}")
