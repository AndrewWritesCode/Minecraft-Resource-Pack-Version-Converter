import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLineEdit, QCheckBox, QProgressBar, \
    QRadioButton, QLabel, QComboBox
from PyQt5.uic import loadUi
from minecraft_version_translator import MinecraftVersionTranslator
from json2pack import json2pack
from fileMapper import FileMapper
from fileMapper import Unzip
import json

try:
    json_templates_dir = os.path.join(os.getcwd(), 'JSON_templates')
except:
    os.mkdir(os.path.join(os.getcwd(), 'JSON_templates'))
    json_templates_dir = os.path.join(os.getcwd(), 'JSON_templates')

try:
    version_dir = os.path.join(os.getcwd(), 'env', 'pack_format.json')
    with open(version_dir, encoding="utf-8") as json_file:
        verDict = json.load(json_file)
except:
    print('Could not load pack_format.json')

appInput = {
    "csv_path": str(os.path.abspath(os.getcwd() + '/CSVconfigs/manualChanges.csv')),
    # step 1 input
    "step1_zipped": "True",
    "step1_path": "",
    # step 2 input
    "optionUsed": "",
    "step2Option1path": "",
    "step2Option2_packPath": "",
    "step2Option2_jsonPath": "",
    # step 3 input
    "step3_path": "UNDEFINED"
}


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("mainWindow.ui", self)

        # Widgets
        # Step 1
        self.step1CheckBox = self.findChild(QCheckBox, "step1CheckBox1")
        self.step1LineEdit = self.findChild(QLineEdit, "step1LineEdit1")
        self.step1Button = self.findChild(QPushButton, "step1Button1")
        # Step 2
        # Option 1
        self.option1RadioButton = self.findChild(QRadioButton, "option1RadioButton")
        self.option1LineEdit = self.findChild(QLineEdit, "step2Option1LineEdit1")
        self.option1Button = self.findChild(QPushButton, "step2Option1Button1")
        # Option 2
        self.option2RadioButton = self.findChild(QRadioButton, "option2RadioButton")
        self.option2LineEdit1 = self.findChild(QLineEdit, "step2Option2LineEdit1")
        self.option2Button1 = self.findChild(QPushButton, "step2Option2Button1")
        self.option2LineEdit2 = self.findChild(QLineEdit, "step2Option2LineEdit2")
        self.option2Button2 = self.findChild(QPushButton, "step2Option2Button2")
        self.option2zipCheckBox = self.findChild(QCheckBox, "step2Option2CheckBox")
        # Step 3
        self.step3LineEdit = self.findChild(QLineEdit, "step3LineEdit1")
        self.step3Button1 = self.findChild(QPushButton, "step3Button1")
        self.versionSelect = self.findChild(QComboBox, "comboBox")
        self.step3Button2 = self.findChild(QPushButton, "step3Button2")
        self.progressBar = self.findChild(QProgressBar, "ProgressBar")
        self.progressLabel = self.findChild(QLabel, "step3ProgressLabel_2")
        self.step3Button3 = self.findChild(QPushButton, "step3Button3")

        # Widget Functionality
        self.step1Button.clicked.connect(self.Step1PathHandler)
        self.option1Button.clicked.connect(self.Step2Option1PathHandler)
        self.option2Button1.clicked.connect(self.Step2Option2PathHandlerPart1)
        self.option2Button2.clicked.connect(self.Step2Option2PathHandlerPart2)
        self.step3Button1.clicked.connect(self.Step3PathHandler)
        self.step3Button2.clicked.connect(self.Generate)
        self.step3Button3.clicked.connect(self.GoToOutputPack)
        self.versionSelect.setCurrentIndex(5)
        self.step3Button3.setText("Awaiting Generation")
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)

        # Window Settings
        self.setFixedWidth(600)
        self.setFixedHeight(920)
        self.show()

    def Step1PathHandler(self):
        if self.step1CheckBox.isChecked():
            f = QFileDialog.getOpenFileName(self, 'Open Resource Pack .zip', '', 'Zip Files (*.zip)')
            self.step1LineEdit.setText(f[0])
            appInput["step1_path"] = f[0]
        else:
            p = QFileDialog.getExistingDirectory(self, 'Open Resource Pack root directory')
            self.step1LineEdit.setText(p)
            appInput["step1_path"] = p

    def Step2Option1PathHandler(self):
        if self.option1RadioButton.isChecked():
            f = QFileDialog.getOpenFileName(self, 'Open .json template file', json_templates_dir, 'JSON Files (*.json)')
            self.option1LineEdit.setText(f[0])
            appInput["optionUsed"] = '1'
            appInput["step2Option1path"] = f[0]

    def Step2Option2PathHandlerPart1(self):
        if self.option2RadioButton.isChecked():
            appInput["optionUsed"] = '2'
            if self.option2zipCheckBox.isChecked():
                f = QFileDialog.getOpenFileName(self, 'Open Resource Pack .zip', '', 'Zip Files (*.zip)')
                self.option2LineEdit1.setText(f[0])
                appInput["step2Option2_packPath"] = f[0]
            else:
                p = QFileDialog.getExistingDirectory(self, 'Open Resource Pack root directory')
                self.option2LineEdit1.setText(p)
                appInput["step2Option2_packPath"] = p

    def Step2Option2PathHandlerPart2(self):
        if self.option2RadioButton.isChecked():
            f = QFileDialog.getSaveFileName(self, 'Save .json template file', json_templates_dir, 'JSON Files (*.json)')
            self.option2LineEdit2.setText(f[0])
            appInput["step2Option2_jsonPath"] = f[0]

    def Step3PathHandler(self):
        p = QFileDialog.getExistingDirectory(self, 'Save ResourcePack')
        self.step3LineEdit.setText(p)
        appInput["step3_path"] = p

    def Generate(self):
        # step 1
        self.progressLabel.setText("Progress: Starting!")
        if self.step1CheckBox.isChecked():
            try:
                dir = os.path.join(os.path.dirname(appInput["step1_path"]),
                                   os.path.splitext(os.path.basename(appInput["step1_path"]))[0])
                os.chdir(dir)
            except:
                dir = os.path.join(os.path.dirname(appInput["step1_path"]),
                                   os.path.splitext(os.path.basename(appInput["step1_path"]))[0])
                os.mkdir(dir)

            Unzip(appInput["step1_path"], dir)
            appInput["step1_path"] = dir
            step1dict = FileMapper(fxnRootDir=appInput["step1_path"])
        else:
            step1dict = FileMapper(fxnRootDir=appInput["step1_path"])
        self.progressLabel.setText("Progress: Step 1 Complete!")
        self.progressBar.setValue(33)
        # step 2
        # option 1
        if appInput["optionUsed"] == '1':
            with open(appInput["step2Option1path"], encoding="utf-8") as json_file:
                step2dict = json.load(json_file)
        # option 2
        else:
            if self.option2zipCheckBox.isChecked():
                try:
                    dir = os.path.join(os.path.dirname(appInput["step2Option2_packPath"]),
                                       os.path.splitext(os.path.basename(appInput["step2Option2_packPath"]))[0])
                    os.chdir(dir)
                except:
                    dir = os.path.join(os.path.dirname(appInput["step2Option2_packPath"]),
                                       os.path.splitext(os.path.basename(appInput["step2Option2_packPath"]))[0])
                    os.mkdir(dir)

                Unzip(appInput["step2Option2_packPath"], dir)
                appInput["step2Option2_packPath"] = dir
                step2dict = FileMapper(fxnRootDir=appInput["step2Option2_packPath"])
            else:
                step2dict = FileMapper(fxnRootDir=appInput["step2Option2_packPath"], fxnJsonPath=appInput["step2Option2_jsonPath"])

        self.progressLabel.setText("Progress: Step 2 Complete!")
        self.progressBar.setValue(66)
        #step 3
        convDict, noMatchDict = MinecraftVersionTranslator(step1dict, step2dict, appInput["step1_path"], 'mcrpc-conversion', csv_path=appInput["csv_path"])
        json2pack(convDict, appInput["step3_path"], mode='ui')
        try:
            mcmeta_path = os.path.join(appInput["step3_path"], 'pack.mcmeta')
            with open(mcmeta_path) as mcmeta_file:
                mcmeta_dict = json.load(mcmeta_file)
            mcmeta_dict["pack"]["pack_format"] = verDict[self.versionSelect.currentText()]["pack_format"]
            mcmeta_object = json.dumps(mcmeta_dict, indent=2)
            m = open(mcmeta_path, "w")
            m.write(mcmeta_object)
            m.close()
        except:
            print("UNABLE TO ACCESS PACK MCMETA")

        json_object = json.dumps(noMatchDict, indent=4)
        f = open(os.path.join(appInput["step3_path"], 'noMatch.json'), "w")
        f.write(json_object)
        f.close()

        self.progressBar.setValue(100)
        self.progressLabel.setText("Progress: Step 3 Complete! DONE!")
        self.step3Button3.setText("Go to " + os.path.basename(appInput["step3_path"]))


    def GoToOutputPack(self):
        if appInput["step3_path"] != "UNDEFINED":
            os.startfile(appInput["step3_path"])


app = QApplication(sys.argv)
mainWindow = MainWindow()
sys.exit(app.exec_())
