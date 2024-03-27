import asyncio
import multiprocessing
import os
import shutil
import threading
import tkinter as tk
import tkinter.filedialog
from tkinter import ttk

import psutil
from PIL import Image, ImageTk

from src.Main.UpdateTxtFileFromLog import UpdateTxtFileFromLog
from src.Common.Constants import constants
from src.Logging.Logger import Logger
from src.Main.LoginAccount import LoginAccount
from src.Main.StartChromedriver import StartChromedriver
from src.Main.StartScraper import StartScraper
from src.Utility.BrowserUtility import BrowserUtility
from src.Utility.ConfigUtility import ConfigUtility
from src.Utility.DownloadUtility import DownloadUtility
from src.Utility.FileUtility import FileUtility


class HomeScreen:
    def __init__(self):
        self.config = None
        self.logger = None
        self.process = None
        self.configJson = None
        self.processes = []
        self.checkboxes = []

        self.app = tk.Tk()
        imagePath = os.path.join(constants.commonFolderPath, "icon.gif")
        pilImage = Image.open(imagePath)
        self.app.iconphoto(True, ImageTk.PhotoImage(pilImage))
        self.app.geometry("400x400")
        self.app.title("Educative Scraper")

        self.configFilePath = tk.StringVar()
        self.userDataDirVar = tk.StringVar()
        self.headlessVar = tk.BooleanVar(value=False)
        self.ucdriverVar = tk.BooleanVar(value=False)
        self.autoResumeScraper = tk.BooleanVar(value=False)
        self.autoFixTextFile = tk.BooleanVar(value=False)
        self.courseUrlsFilePathVar = tk.StringVar()
        self.saveDirectoryVar = tk.StringVar()
        self.isProxyVar = tk.BooleanVar(value=True)
        self.proxyVar = tk.StringVar()
        self.loggingLevelVar = tk.StringVar()
        self.loggingLevels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "NOTSET"]
        self.logLevelDesc = {
            "DEBUG": "Detailed info for debugging.",
            "INFO": "Confirmation of expected functionality.",
            "WARNING": "Indication of unexpected events.",
            "ERROR": "Software can't perform a function.",
            "CRITICAL": "Program can't continue running.",
            "NOTSET": "Lowest level, turns off logging."
        }
        self.scrapingMethodVar = tk.StringVar()
        self.scrapingMethods = ["SingleFile-HTML", "Full-Page-Screenshot"]
        self.scraperTypeVar = tk.StringVar()
        self.scraperTypes = ["Course-Topic-Scraper", "All-Course-Urls-Text-File-Generator"]
        self.fileTypeVar = tk.StringVar()
        self.fileTypes = ["html2pdf", "html", "png2pdf", "png"]

        self.fileUtil = FileUtility()
        self.downloadUtil = DownloadUtility()
        self.progressVar = tk.DoubleVar()
        self.configUtil = ConfigUtility()
        self.loadDefaultConfig()
        self.logLevelDescVar = tk.StringVar(value=self.configJson['logger'])
        self.logDescriptionLabel = None
        self.checkButtonStateVar = tk.StringVar()
        self.updateTextFromLog = UpdateTxtFileFromLog()
        self.clickedByUser = False


    def onConfigChange(self, *args):
        self.createConfigJson()
        self.logger = Logger(self.configJson, "HomeScreen").logger
        self.logLevelDescVar.set(self.configJson['logger'])
        self.logDescriptionLabel.config(text=self.logLevelDesc[self.logLevelDescVar.get()])


    def updateComboboxStates(self, *args):
        if self.scraperTypeVar.get() == "All-Course-Urls-Text-File-Generator":
            self.scrapingMethodCombobox.config(state="disabled")
            self.fileTypeCombobox.config(state="disabled")
        elif self.scraperTypeVar.get() == "Course-Topic-Scraper":
            self.scrapingMethodCombobox.config(state="enabled")
            self.fileTypeCombobox.config(state="enabled")
            if self.scrapingMethodVar.get() == "SingleFile-HTML":
                if self.fileTypeVar.get() == "png" or self.fileTypeVar.get() == "png2pdf":
                    self.fileTypeVar.set("html")
                self.fileTypeCombobox['values'] = self.fileTypes[:2]
            else:
                self.fileTypeCombobox['values'] = self.fileTypes[1:]
    

    def trackUserClick(self, event):
        self.clickedByUser = True


    def autoStartScraperOnConditions(self):
        if self.startScraperButton['state'] == 'normal' and \
            not self.updateTextFromLog.getBlockScraper() and \
            self.configJson['autoresume']:

            if self.updateTextFromLog.updateTextFileFromLogMain():
                self.startScraperButton.invoke()
                self.clickedByUser = False


    def createHomeScreen(self, version):
        self.logger = Logger(self.configJson, "HomeScreen").logger
        self.loggingLevelVar.trace("w", self.onConfigChange)
        self.saveDirectoryVar.trace("w", self.onConfigChange)
        self.logLevelDescVar.trace("w", self.onConfigChange)
        self.scrapingMethodVar.trace("w", self.updateComboboxStates)
        self.scraperTypeVar.trace("w", self.updateComboboxStates)
        self.logger.info("Creating Home Screen...")

        configFilePathFrame = tk.Frame(self.app)
        configFilePathLabel = tk.Label(configFilePathFrame, text="Config File Path:")
        configFileTextBox = tk.Entry(configFilePathFrame, textvariable=self.configFilePath, width=70)
        browseConfigFileButton = tk.Button(configFilePathFrame, text="...", command=self.browseConfigFile)
        configFilePathLabel.grid(row=0, column=0, sticky="w", padx=2, pady=2)
        configFileTextBox.grid(row=0, column=1, sticky="w", padx=2, pady=2)
        browseConfigFileButton.grid(row=0, column=2, padx=2)
        configFilePathFrame.pack(pady=3, padx=10, anchor="w")

        optionsContainerFrame = tk.Frame(self.app)
        scraperOptionFrame = tk.Frame(optionsContainerFrame)
        scraperTypeLabel = tk.Label(scraperOptionFrame, text="Scraper Type:")
        scraperTypeLabel.grid(row=0, column=0, sticky="w", padx=2, pady=0)
        self.scraperTypeCombobox = ttk.Combobox(scraperOptionFrame, textvariable=self.scraperTypeVar,
                                           values=self.scraperTypes, state="readonly", width=30)
        self.scraperTypeCombobox.grid(row=0, column=1, sticky="w", padx=0, pady=5)
        scrapingMethodLabel = tk.Label(scraperOptionFrame, text="Scraping Method:")
        scrapingMethodLabel.grid(row=1, column=0, sticky="w", padx=2, pady=0)
        self.scrapingMethodCombobox = ttk.Combobox(scraperOptionFrame, textvariable=self.scrapingMethodVar,
                                           values=self.scrapingMethods, state="readonly", width=30)
        self.scrapingMethodCombobox.grid(row=1, column=1, sticky="w", padx=0, pady=5)
        fileTypeLabel = tk.Label(scraperOptionFrame, text="File Type:")
        fileTypeLabel.grid(row=2, column=0, sticky="w", padx=2, pady=0)
        self.fileTypeCombobox = ttk.Combobox(scraperOptionFrame, textvariable=self.fileTypeVar,
                                           values=self.fileTypes, state="readonly", width=30)
        self.fileTypeCombobox.grid(row=2, column=1, sticky="w", padx=0, pady=5)
        loggerLevelLabel = tk.Label(scraperOptionFrame, text="Logger Level:")
        loggerLevelLabel.grid(row=3, column=0, sticky="w", padx=2, pady=0)
        loggingLevelCombobox = ttk.Combobox(scraperOptionFrame, textvariable=self.loggingLevelVar,
                                            values=self.loggingLevels, state="readonly", width=30)
        loggingLevelCombobox.grid(row=3, column=1, sticky="w", padx=0, pady=5)
        self.logDescriptionLabel = tk.Label(scraperOptionFrame, text=self.logLevelDesc[self.logLevelDescVar.get()])
        self.logDescriptionLabel.grid(row=3, column=2, sticky="w", padx=2, pady=2)
        ToolDescriptionLabel0 = tk.Label(scraperOptionFrame, text="About: Educative Scraper")
        ToolDescriptionLabel1 = tk.Label(scraperOptionFrame, text=version)
        ToolDescriptionLabel2 = tk.Label(scraperOptionFrame, text="Developed by Anilabha Datta")
        ToolDescriptionLabel0.grid(row=0, column=2, sticky="w", padx=2, pady=2)
        ToolDescriptionLabel1.grid(row=1, column=2, sticky="w", padx=2, pady=2)
        ToolDescriptionLabel2.grid(row=2, column=2, sticky="w", padx=2, pady=2)

        checkboxesFrame = tk.Frame(optionsContainerFrame)
        optionCheckboxes = [
            ("Headless", self.headlessVar),
            ("Proxy", self.isProxyVar)
        ]
        for i, (optionText, optionVar) in enumerate(optionCheckboxes):
            checkbox = tk.Checkbutton(checkboxesFrame, text=optionText, variable=optionVar, wraplength=400, anchor="w")
            checkbox.grid(row=int(i), column=0, sticky="w", padx=0, pady=2)
            self.checkboxes.append(checkbox)
        proxyEntry = tk.Entry(checkboxesFrame, textvariable=self.proxyVar, width=33)
        proxyEntry.grid(row=len(optionCheckboxes)-1, column=1, sticky="w", padx=(30, 2), pady=2)
        proxyLabel = tk.Label(checkboxesFrame, text="Format: Host:Port")
        proxyLabel.grid(row=len(optionCheckboxes)-1, column=2, sticky="w", padx=2, pady=0)
        ucdriverCheckbox = tk.Checkbutton(checkboxesFrame, text="SeleniumBase(uc mode)", variable=self.ucdriverVar, wraplength=400, anchor="w")
        ucdriverCheckbox.grid(row=len(optionCheckboxes)-2, column=1, sticky="w", padx=(25,0), pady=2)
        self.autoResumeScraperCheckbox = tk.Checkbutton(checkboxesFrame, text="Auto Resume Scraper", variable=self.autoResumeScraper, wraplength=400, anchor="w")
        self.autoResumeScraperCheckbox.grid(row=len(optionCheckboxes)-2, column=2, sticky="w", padx=(0,0), pady=2)
        self.autoFixTextFileCheckbox = tk.Checkbutton(checkboxesFrame, text="Auto Fix Url File", variable=self.autoFixTextFile, wraplength=400, anchor="w")
        self.autoFixTextFileCheckbox.grid(row=len(optionCheckboxes)-2, column=3, sticky="w", padx=(15,0), pady=2)

        scraperOptionFrame.grid(row=0, column=0, padx=0, pady=3, sticky="nw")
        checkboxesFrame.grid(row=1, column=0, padx=0, pady=3, sticky="nw")
        optionsContainerFrame.pack(pady=3, padx=10, anchor="w")

        entriesFrame = tk.Frame(self.app)
        userDataDirLabel = tk.Label(entriesFrame, text="User Data Directory:")
        userDataDirEntry = tk.Entry(entriesFrame, textvariable=self.userDataDirVar, width=65)
        courseUrlsFilePathLabel = tk.Label(entriesFrame, text="Course URLs File Path:")
        courseUrlsFilePathEntry = tk.Entry(entriesFrame, textvariable=self.courseUrlsFilePathVar, width=65)
        courseUrlsFilePathButton = tk.Button(entriesFrame, text="...", command=self.browseCourseUrlsFile)
        saveDirectoryLabel = tk.Label(entriesFrame, text="Save Directory:")
        saveDirectoryEntry = tk.Entry(entriesFrame, textvariable=self.saveDirectoryVar, width=65)
        saveDirectoryButton = tk.Button(entriesFrame, text="...", command=self.browseSaveDirectory)
        logPathLabel = tk.Label(entriesFrame,
                                text="Logs are saved in Save Directory Path with name 'EducativeScraper.log")
        userDataDirLabel.grid(row=0, column=0, sticky="w", padx=2, pady=2)
        userDataDirEntry.grid(row=0, column=1, sticky="w", padx=2, pady=2)
        courseUrlsFilePathLabel.grid(row=1, column=0, sticky="w", padx=2, pady=2)
        courseUrlsFilePathEntry.grid(row=1, column=1, sticky="w", padx=2, pady=2)
        courseUrlsFilePathButton.grid(row=1, column=2, padx=2)
        saveDirectoryLabel.grid(row=2, column=0, sticky="w", padx=2, pady=2)
        saveDirectoryEntry.grid(row=2, column=1, sticky="w", padx=2, pady=2)
        saveDirectoryButton.grid(row=2, column=2, padx=2)
        logPathLabel.grid(row=3, column=1, sticky="w", padx=2, pady=2)
        entriesFrame.pack(pady=3, padx=10, anchor="w")

        buttonConfigFrame = tk.Frame(self.app)
        loadDefaultConfigButton = tk.Button(buttonConfigFrame, text="Default Config",
                                            command=self.loadDefaultConfig)
        updateConfigButton = tk.Button(buttonConfigFrame, text="Update Config", command=self.updateConfig)
        exportConfigButton = tk.Button(buttonConfigFrame, text="Export Config", command=self.exportConfig)
        deleteUserDataButton = tk.Button(buttonConfigFrame, text="Delete User Data", command=self.deleteUserData)
        loadDefaultConfigButton.grid(row=0, column=0, sticky="w", padx=2, pady=2)
        updateConfigButton.grid(row=0, column=1, sticky="w", padx=2, pady=2)
        exportConfigButton.grid(row=0, column=2, sticky="w", padx=2, pady=2)
        deleteUserDataButton.grid(row=0, column=3, sticky="w", padx=2, pady=2)
        buttonConfigFrame.pack(pady=3, padx=100, anchor="center")

        buttonScraperFrame = tk.Frame(self.app)
        self.downloadChromeDriverButton = tk.Button(buttonScraperFrame, text="Download Chrome Driver", width=19,
                                                    command=self.downloadChromeDriver)
        self.downloadChromeBinaryButton = tk.Button(buttonScraperFrame, text="Download Chrome Binary", width=20,
                                                    command=self.downloadChromeBinary)
        self.startChromeDriverButton = tk.Button(buttonScraperFrame, text="Start Chrome Driver",
                                                 command=self.startChromeDriver, width=19, state="disabled")
        self.loginAccountButton = tk.Button(buttonScraperFrame, text="Login Account", command=self.loginAccount,
                                            width=20)
        self.startScraperButton = tk.Button(buttonScraperFrame, text="Start Scraper", command=self.startScraper,
                                            width=19)
        self.checkButtonStateVar.set(self.startScraperButton['state'])
        self.checkButtonStateVar.trace("w", lambda *args: self.autoStartScraperOnConditions())
        self.startScraperButton.bind("<Button-1>", self.trackUserClick)
        self.terminateProcessButton = tk.Button(buttonScraperFrame, text="Stop Scraper/Close Browser",
                                                command=self.terminateProcess,
                                                width=20, state="disabled")
        self.downloadChromeDriverButton.grid(row=0, column=0, sticky="w", padx=2, pady=3)
        self.downloadChromeBinaryButton.grid(row=0, column=1, sticky="w", padx=2, pady=3)
        self.startChromeDriverButton.grid(row=1, column=0, sticky="w", padx=2, pady=3)
        self.loginAccountButton.grid(row=1, column=1, sticky="w", padx=2, pady=3)
        self.startScraperButton.grid(row=2, column=0, sticky="w", padx=2, pady=3)
        self.terminateProcessButton.grid(row=2, column=1, sticky="w", padx=2, pady=3)
        buttonScraperFrame.pack(pady=4, padx=100, anchor="center")

        progressBarFrame = tk.Frame(self.app)
        downloadProgressLabel = tk.Label(progressBarFrame, text="Download Progress:")
        progressBar = ttk.Progressbar(progressBarFrame, length=380, mode="determinate", variable=self.progressVar)
        downloadProgressLabel.grid(row=0, column=0, sticky="w", padx=2, pady=2)
        progressBar.grid(row=0, column=1, sticky="w", padx=2, pady=2)
        progressBarFrame.pack(pady=3)

        self.updateComboboxStates()
        self.fixGeometry()
        self.app.update_idletasks()
        self.logger.debug("createHomeScreen completed")
        self.app.protocol("WM_DELETE_WINDOW", self.onClosingWindow)
        self.app.mainloop()


    def onClosingWindow(self):
        self.terminateProcess()
        self.app.destroy()


    def fixGeometry(self):
        self.logger.debug("fixGeometry called")
        self.app.update_idletasks()
        width = self.app.winfo_reqwidth()
        height = self.app.winfo_reqheight()

        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.app.geometry(f"{width}x{height}+{x}+{y}")
        self.app.resizable(False, False)
        self.logger.debug("fixGeometry completed")


    def browseCourseUrlsFile(self):
        self.logger.debug("browseCourseUrlsFile called")
        courseUrlsFilePath = tk.filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt")])
        if courseUrlsFilePath:
            self.courseUrlsFilePathVar.set(courseUrlsFilePath)
        self.logger.debug(f"""browseCourseUrlsFile completed 
                              courseUrlsFilePath: {courseUrlsFilePath}
                            """)


    def browseSaveDirectory(self):
        self.logger.debug("browseSaveDirectory called")
        saveDirectoryPath = tk.filedialog.askdirectory()
        if saveDirectoryPath:
            self.saveDirectoryVar.set(saveDirectoryPath)
        self.logger.debug(f"""browseSaveDirectory completed
                              saveDirectoryPath: {saveDirectoryPath}
                            """)


    def browseConfigFile(self):
        self.logger.debug("browseConfigFile called")
        configFilePath = tk.filedialog.askopenfilename(
            filetypes=[("INI Files", "*.ini")])
        if configFilePath:
            self.configFilePath.set(configFilePath)
            self.config = self.configUtil.loadConfig(configFilePath)['ScraperConfig']
            self.mapConfigValues()
            self.createConfigJson()
            self.logger.debug(f"""browseConfigFile completed
                                  configFilePath: {configFilePath}
                                """)


    def mapConfigValues(self):
        self.userDataDirVar.set(self.config['userDataDir'])
        self.headlessVar.set(self.config['headless'])
        self.courseUrlsFilePathVar.set(self.config['courseUrlsFilePath'])
        self.saveDirectoryVar.set(self.config['saveDirectory'])
        self.loggingLevelVar.set(self.config['logger'])
        self.isProxyVar.set(self.config['isProxy'])
        self.proxyVar.set(self.config['proxy'])
        self.fileTypeVar.set(self.config["fileType"])
        self.scraperTypeVar.set(self.config["scraperType"])
        self.scrapingMethodVar.set(self.config["scrapingMethod"])
        self.ucdriverVar.set(self.config["ucdriver"])
        self.autoResumeScraper.set(self.config["autoresume"])
        self.autoFixTextFile.set(self.config["autofixtextfile"])


    def createConfigJson(self):
        self.configJson = {
            'userDataDir': self.userDataDirVar.get(),
            'headless': self.headlessVar.get(),
            'courseUrlsFilePath': self.courseUrlsFilePathVar.get(),
            'saveDirectory': self.saveDirectoryVar.get(),
            'logger': self.loggingLevelVar.get(),
            'isProxy': self.isProxyVar.get(),
            'proxy': self.proxyVar.get(),
            'scraperType': self.scraperTypeVar.get(),
            "scrapingMethod": self.scrapingMethodVar.get(),
            'fileType': self.fileTypeVar.get(),
            'ucdriver': self.ucdriverVar.get(),
            'binaryversion': self.config["binaryversion"],
            'autoresume': self.autoResumeScraper.get(),
            'autofixtextfile': self.autoFixTextFile.get()
        }


    def startScraper(self):
        self.logger.debug("startScraper called")
        self.createConfigJson()
        if self.clickedByUser:
            self.updateTextFromLog.setBlockScraper(False)
            self.updateTextFromLog.resetLastTopicUrlsList()
            if self.configJson['autofixtextfile'] and not self.updateTextFromLog.updateTextFileFromLogMain():
                self.logger.info("No URL found in log file. Starting Scraper from first url...")
        startScraper = StartScraper()
        self.process = multiprocessing.Process(target=startScraper.start, args=(self.configJson,))
        self.process.start()
        self.processes.append(self.process)
        self.updateButtonState()
        self.logger.debug("startScraper completed")


    def loginAccount(self):
        self.logger.debug("loginAccount called")
        self.createConfigJson()
        self.updateTextFromLog.setBlockScraper(True)
        loginAccount = LoginAccount()
        self.process = multiprocessing.Process(target=loginAccount.start, args=(self.configJson,))
        self.process.start()
        self.processes.append(self.process)
        self.updateButtonState()
        self.logger.debug("loginAccount completed")


    def terminateProcess(self):
        self.logger.debug("terminateProcess called")
        self.logger.info("Terminating Process...")
        self.updateTextFromLog.setBlockScraper(True)
        browserUtil = BrowserUtility(self.configJson)
        for process in self.processes:
            try:
                process.terminate()
                process.join()
            except psutil.NoSuchProcess:
                pass
        asyncio.get_event_loop().run_until_complete(browserUtil.shutdownChromeViaWebsocket())
        self.processes = []
        self.updateButtonState()
        self.logger.debug("terminateProcess completed")


    def updateButtonState(self):
        if self.process and self.process.is_alive():
            self.EnableDisableButtons("disabled")
            self.terminateProcessButton.config(state="normal")
        else:
            self.EnableDisableButtons("normal")
            self.terminateProcessButton.config(state="disabled")
        self.checkButtonStateVar.set(self.startScraperButton['state'])
        self.app.after(1000, self.updateButtonState)


    def EnableDisableButtons(self, state):
        self.downloadChromeDriverButton.config(state=state)
        self.downloadChromeBinaryButton.config(state=state)
        # self.startChromeDriverButton.config(state=state)
        self.startScraperButton.config(state=state)
        self.loginAccountButton.config(state=state)


    def startChromeDriver(self):
        self.logger.info(f"""  Starting Chrome Driver...
                                Path:  {constants.chromeDriverPath}
                          """)
        self.updateTextFromLog.setBlockScraper(True)
        StartChromedriver().loadChromeDriver()
        self.logger.debug("startChromeDriver completed")


    def loadDefaultConfig(self):
        self.configFilePath.set(constants.defaultConfigPath)
        self.config = self.configUtil.loadConfig()['ScraperConfig']
        self.mapConfigValues()
        self.createConfigJson()


    def deleteUserData(self):
        self.logger.debug("deleteUserData called")
        userDataDirPath = os.path.join(constants.OS_ROOT, self.userDataDirVar.get())
        if self.fileUtil.checkIfDirectoryExists(userDataDirPath):
            shutil.rmtree(userDataDirPath)
            self.logger.info(f"Deleted User Data Directory: {userDataDirPath}")


    def updateConfig(self):
        self.logger.debug("updateConfig called")
        self.createConfigJson()
        self.configUtil.updateConfig(self.configJson, 'ScraperConfig', self.configFilePath.get())
        self.logger.info(f"Updated Config with filePath: {self.configFilePath.get()}")


    def exportConfig(self):
        self.logger.debug("exportConfig called")
        self.createConfigJson()
        filePath = tk.filedialog.asksaveasfilename(defaultextension='.ini', filetypes=[('INI Files', '*.ini')],
                                                   title='Save Config File')
        if filePath:
            self.configUtil.updateConfig(self.configJson, 'ScraperConfig', filePath)
            self.logger.info(f"Exported Config with filePath: {filePath}")


    def downloadChromeDriver(self):
        self.updateTextFromLog.setBlockScraper(True)
        self.EnableDisableButtons("disabled")
        downloadThread = threading.Thread(target=lambda: self.downloadUtil.downloadChromeDriver(self.app,
                                                                                                self.progressVar,
                                                                                                self.configJson))
        downloadThread.start()
        self.app.after(100, self.checkDownloadThread, downloadThread)


    def downloadChromeBinary(self):
        self.updateTextFromLog.setBlockScraper(True)
        self.EnableDisableButtons("disabled")
        downloadThread = threading.Thread(target=lambda: self.downloadUtil.downloadChromeBinary(self.app,
                                                                                                self.progressVar,
                                                                                                self.configJson))
        downloadThread.start()
        self.app.after(100, self.checkDownloadThread, downloadThread)


    def checkDownloadThread(self, thread):
        if thread.is_alive():
            self.app.after(100, self.checkDownloadThread, thread)
        else:
            self.EnableDisableButtons("normal")
