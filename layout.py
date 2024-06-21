from PyQt6.QtWidgets import *
import customWidgets as CW
from PyQt6.QtCore import *
from PyQt6.QtGui import QIntValidator
from bdoMainWeb import runCodeRedeem

import Tools
import logger

import os
import yaml

class ConfigLayout(QVBoxLayout):
    configPath = os.path.dirname(os.path.abspath(__file__)) + "/config.yml"

    def __init__(self, fn):
        super().__init__()
        self.regionWgt = CW.LabelComboBox(Tools.ConfigConstants.region, ["NAEU", "ASIA"])
        self.loginMethodWgt = CW.LabelComboBox(Tools.ConfigConstants.loginMethod, ["Steam", "PearlAbyss"])
        self.ffprofileWgt = CW.LabelTextBox(Tools.ConfigConstants.ffProfilePath)
        self.ffprofileTipWgt = QLabel("Info: profile path can be found by typing 'about:profiles' into Firefox")
        self.usernameWgt = CW.LabelTextBox(Tools.ConfigConstants.username)
        self.passwordWgt = CW.LabelTextBox(Tools.ConfigConstants.password)

        # Button layout
        buttonLayOut = QHBoxLayout()
        saveWgt = QPushButton("Save")
        runWgt = QPushButton("run")
        saveWgt.clicked.connect(self.saveData)
        runWgt.clicked.connect(fn)
        buttonLayOut.addWidget(saveWgt)
        buttonLayOut.addWidget(runWgt)

        self.addWidget(self.regionWgt)
        self.addWidget(self.loginMethodWgt)
        self.addWidget(self.ffprofileWgt)
        self.addWidget(self.ffprofileTipWgt)
        self.addWidget(self.usernameWgt)
        self.addWidget(self.passwordWgt)
        self.addLayout(buttonLayOut)
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
        self.regionWgt.setText(config[Tools.ConfigConstants.region])
        self.loginMethodWgt.setText(config[Tools.ConfigConstants.loginMethod])
        self.ffprofileWgt.setText(config[Tools.ConfigConstants.ffProfilePath])
        self.usernameWgt.setText(config[Tools.ConfigConstants.username])
        self.passwordWgt.setText(config[Tools.ConfigConstants.password])
        

    def saveData(self):
        data = {
            Tools.ConfigConstants.region: self.regionWgt.getText(),
            Tools.ConfigConstants.loginMethod: self.loginMethodWgt.getText(),
            Tools.ConfigConstants.ffProfilePath: self.ffprofileWgt.getText(),
            Tools.ConfigConstants.username: self.usernameWgt.getText(),
            Tools.ConfigConstants.password: self.passwordWgt.getText()
        }  
        with open(self.configPath, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
            # logger.info(f"Saving config information:\n {data}")

    def runCodeRedeem(self):
        import bdoMainWeb
        print("Run code redeem")
        bdoMainWeb.runCodeRedeem()


class LogLayOut (QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.textBoxWgt = QPlainTextEdit()
        self.textBoxWgt.setReadOnly(True)
        self.buttonWgt = QPushButton("Clear")
        self.buttonWgt.clicked.connect(self.clearText)

        self.addWidget(self.textBoxWgt, 0, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.buttonWgt, 0, Qt.AlignmentFlag.AlignCenter)

    def clearText(self):
        self.textBoxWgt.clear()

    def getPlainTextWgt(self):
        return self.textBoxWgt


from myScheduler import MyScheduler
class timerLayOut(QVBoxLayout):

    nextDate: QDateTime = QDateTime.currentDateTime()
    schedule: MyScheduler = None

    def __init__(self):
        super().__init__()
        self.schedule = MyScheduler()
        # starting datatime
        self.startDateWgt = QDateTimeEdit()
        self.startDateWgt.setDateTime(QDateTime.currentDateTime())

        self.daysWgt = CW.LabelTextBox("Days")
        self.daysWgt.lineWgt.setValidator(QIntValidator())

        self.hoursWgt = CW.LabelTextBox("Hour")
        self.hoursWgt.lineWgt.setValidator(QIntValidator())

        #save time config button
        self.saveTimeConfigWgt = QPushButton("Save")
        self.saveTimeConfigWgt.pressed.connect(self.setTimer)

        # Date and time of execution widget
        self.timeWgt = QLabel("Executing on: Month, Day, time")

        # add widget into layout
        self.addWidget(QLabel("Start Date"), 0)
        self.addWidget(self.startDateWgt, 0)
        self.addWidget(QLabel("Please insert the period of exeuction below"), 0, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.daysWgt, 0, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.hoursWgt, 0, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.saveTimeConfigWgt, 0, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.timeWgt, 0, Qt.AlignmentFlag.AlignCenter)

    def setTimer(self):
        
        startDate = self.startDateWgt.dateTime()
        
        day = 0
        hours = 0
        if self.daysWgt.getText() != "":
            day = int(self.daysWgt.getText())
        if self.hoursWgt.getText() != "":
            hours = int(self.hoursWgt.getText())
        
        self.nextDate = startDate
        self.nextDate = self.nextDate.addDays(day)
        self.nextDate = self.nextDate.addSecs(60 * 60 * hours)
        self.timeWgt.setText(f"Date of Next Execution: {self.nextDate.toString()}")
        
        # first clear out any upstanding jobs
        self.schedule.delete_jobs()
        # schedule the task 
        logger.logging.info("Creating Job...")
        self.schedule.cyclicJob(runCodeRedeem, day, hours)
        logger.logging.info(f"Job created:  {self.schedule}")

    
