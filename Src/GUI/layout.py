from PyQt6.QtWidgets import *
from .customWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QIntValidator

from ..Page.bdoMainWeb import runCodeRedeem
from ..Tools.tools import ConfigConstants, CONFIG_PATH
from .myScheduler import MyScheduler

import logging

import os
import yaml

class ConfigLayout(QVBoxLayout):

    def __init__(self, fn):
        super().__init__()
        self.regionWgt = LabelComboBox(ConfigConstants.region, ["NAEU", "ASIA"])
        self.loginMethodWgt = LabelComboBox(ConfigConstants.loginMethod, ["Steam", "PearlAbyss"])
        self.ffprofileWgt = LabelTextBox(ConfigConstants.ffProfilePath)
        self.ffprofileTipWgt = QLabel("Info: profile path can be found by typing 'about:profiles' into Firefox")
        self.usernameWgt = LabelTextBox(ConfigConstants.username)
        self.passwordWgt = LabelTextBox(ConfigConstants.password)

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
        config = yaml.safe_load(open(CONFIG_PATH))
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
        with open(CONFIG_PATH, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
            # logger.info(f"Saving config information:\n {data}")


class LogLayOut (QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.textBoxWgt = QPlainTextEdit()
        self.textBoxWgt.setReadOnly(True)
        self.textBoxWgt.setMinimumSize(200, 400)
        self.textBoxWgt.setMaximumSize(500,600)
        self.buttonWgt = QPushButton("Clear")
        self.buttonWgt.clicked.connect(self.clearText)

        self.addWidget(self.textBoxWgt, 0, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.buttonWgt, 0, Qt.AlignmentFlag.AlignCenter)

    def clearText(self):
        self.textBoxWgt.clear()

    def getPlainTextWgt(self):
        return self.textBoxWgt

class TimerLayOut(QVBoxLayout):

    nextDate: QDateTime = QDateTime.currentDateTime()
    schedule: MyScheduler = None

    def __init__(self):
        super().__init__()
        self.schedule = MyScheduler()
        # starting datatime
        self.startDateWgt = QDateTimeEdit()
        self.startDateWgt.setDateTime(QDateTime.currentDateTime())

        self.daysWgt = LabelTextBox("Days")
        self.daysWgt.lineWgt.setValidator(QIntValidator())

        self.hoursWgt = LabelTextBox("Hour")
        self.hoursWgt.lineWgt.setValidator(QIntValidator())

        #save time config button
        self.saveTimeConfigWgt = QPushButton("Save")
        self.saveTimeConfigWgt.pressed.connect(self.setTimer)

        # Date and time of execution widget
        self.timeWgt = QLabel("Executing on: Month, Day, time")

        # add widget into layout
        self.addWidget(QLabel("Job Scheduler:"), 0)
        self.addWidget(QLabel("Set Start Date"), 0)
        self.addWidget(self.startDateWgt, 0)
        self.addWidget(QLabel("Frequency of job schedule"), 0, Qt.AlignmentFlag.AlignCenter)
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
        logging.info("Creating Job...")
        self.schedule.once(self.nextDate.toPyDateTime(), self.schedule.cyclicJob, args=(runCodeRedeem, day, hours))
        logging.info(f"Job created:  {self.schedule}")

    
