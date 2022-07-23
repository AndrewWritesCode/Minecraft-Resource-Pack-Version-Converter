import sys
import os
from PyQt5.QtWidgets import  QApplication, QMainWindow, QFileDialog, QPushButton, QLineEdit, QCheckBox, QProgressBar, QRadioButton
from PyQt5.uic import loadUi

json_templates_dir = os.path.join(os.getcwd(), 'JSON_templates')

appInput = {
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
        self.step3Button2 = self.findChild(QPushButton, "step3Button2")

        self.progressBar = self.findChild(QProgressBar, "ProgressBar")

        self.step3Button3 = self.findChild(QPushButton, "step3Button3")

        # Widget Functionality
        self.step1Button.clicked.connect(self.Step1PathHandler)
        self.option1Button.clicked.connect(self.Step2Option1PathHandler)
        self.option2Button1.clicked.connect(self.Step2Option2PathHandlerPart1)
        self.option2Button2.clicked.connect(self.Step2Option2PathHandlerPart2)
        self.step3Button1.clicked.connect(self.Step3PathHandler)
        self.step3Button2.clicked.connect(self.Generate)
        self.step3Button3.clicked.connect(self.GoToOutputPack)



        self.setFixedWidth(600)
        self.setFixedHeight(850)

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
                self.option1LineEdit.setText(f[0])
                appInput["step2Option2_packPath"] = f[0]
            else:
                p = QFileDialog.getExistingDirectory(self, 'Open Resource Pack root directory')
                self.step1LineEdit.setText(p)
                appInput["step2Option2_packPath"] = p

    def Step2Option2PathHandlerPart2(self):
        if self.option2RadioButton.isChecked():
            f = QFileDialog.getSaveFileName(self, 'Save .json template file', json_templates_dir, 'JSON Files (*.json)')
            self.option2LineEdit2.setText(f[0])
            appInput["step2Option2_jsonPath"] = f[0]

    def Step3PathHandler(self):
        f = QFileDialog.getSaveFileName(self, 'Save ResourcePack.zip', '', 'Zip Files (*.zip)')
        self.step3LineEdit.setText(f[0])
        appInput["step3_path"] = f[0]

    def Generate(self):
        print('Run the code')

    def GoToOutputPack(self):
        if appInput["step3_path"] != "UNDEFINED":
            os.startfile(appInput["step3_path"])


app = QApplication(sys.argv)
mainWindow = MainWindow()
sys.exit(app.exec_())
