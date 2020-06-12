from PySide2 import QtWidgets, QtGui

class Settings(QtWidgets.QDialog):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setFixedWidth(200)
		self.setWindowTitle("UPCO Leader")

		self.lay_main = QtWidgets.QVBoxLayout()
		self.setLayout(self.lay_main)

		self.setupWidgets()
	
	def setupWidgets(self):

		# Project Title
		self.grp_title = QtWidgets.QGroupBox("Project Title")
		self.lay_main.addWidget(self.grp_title)
		self.lay_title = QtWidgets.QVBoxLayout()
		self.grp_title.setLayout(self.lay_title)
		self.txt_title = QtWidgets.QLineEdit()
		self.lay_title.addWidget(self.txt_title)

		#Dimensions
		self.grp_dimensions = QtWidgets.QGroupBox("Dimensions")
		self.lay_dimensions = QtWidgets.QGridLayout()
		self.lay_dimensions.setSpacing(4)
		self.grp_dimensions.setLayout(self.lay_dimensions)
		self.lay_main.addWidget(self.grp_dimensions)
		
		# Presets
		self.cmb_presets = QtWidgets.QComboBox()
		self.lay_dimensions.addWidget(self.cmb_presets, 0, 0, 1, 5)
		
		# Manual entries
		self.val_int = QtGui.QIntValidator(1, 9999)
		
		self.lbl_width = QtWidgets.QLabel("Width")
		self.lay_dimensions.addWidget(self.lbl_width, 1, 0)
		self.txt_width = QtWidgets.QLineEdit()
		self.txt_width.setValidator(self.val_int)
		self.lay_dimensions.addWidget(self.txt_width, 2, 0)

		self.lbl_by = QtWidgets.QLabel('x')
		self.lay_dimensions.addWidget(self.lbl_by, 2, 1)

		self.lbl_height = QtWidgets.QLabel("Height")
		self.lay_dimensions.addWidget(self.lbl_height, 1, 2)
		self.txt_height = QtWidgets.QLineEdit()
		self.txt_height.setValidator(self.val_int)
		self.lay_dimensions.addWidget(self.txt_height, 2, 2)

		self.lay_dimensions.addItem(QtWidgets.QSpacerItem(20, 1), 2, 3)

		self.lbl_aspect = QtWidgets.QLabel("Aspect")
		self.lay_dimensions.addWidget(self.lbl_aspect, 1, 4)
		self.txt_aspect = QtWidgets.QLineEdit()
		self.lay_dimensions.addWidget(self.txt_aspect, 2, 4)

		# Output dir
		self.grp_output = QtWidgets.QGroupBox("Output Path")
		self.lay_output = QtWidgets.QHBoxLayout()
		self.grp_output.setLayout(self.lay_output)
		self.lay_main.addWidget(self.grp_output)

		self.txt_output = QtWidgets.QLineEdit()
		self.lay_output.addWidget(self.txt_output)

		self.btn_browse = QtWidgets.QPushButton("...")
		self.btn_browse.setAutoDefault(False)
		self.btn_browse.setFixedWidth(40)
		self.lay_output.addWidget(self.btn_browse)

		# Buttons
		self.box_buttons = QtWidgets.QWidget()
		self.lay_main.addWidget(self.box_buttons)
		self.lay_buttons = QtWidgets.QHBoxLayout()
		self.lay_buttons.setMargin(0)
		self.box_buttons.setLayout(self.lay_buttons)
		self.btn_ok = QtWidgets.QPushButton("Generate")
		self.btn_ok.setDefault(True)
		self.lay_buttons.addWidget(self.btn_ok)
		self.btn_cancel = QtWidgets.QPushButton("Cancel")
		self.btn_cancel.setAutoDefault(False)
		self.lay_buttons.addWidget(self.btn_cancel)

		# Status
		self.prog_status = QtWidgets.QProgressBar()
		self.prog_status.setTextVisible(False)
		self.lay_main.addWidget(self.prog_status)
	
	def setSizeFromPreset(self, idx):
		
		self.txt_aspect.blockSignals(True)
		width, height = self.cmb_presets.itemData(idx)
		
		self.txt_width.setText(str(width))
		self.txt_height.setText(str(height))
		
		self.txt_aspect.blockSignals(False)
		self.updateAspectRatio()
	
	def updateAspectRatio(self):
		width = self.txt_width.text()
		height= self.txt_height.text()
		
		if width.isnumeric() and height.isnumeric():
			try:
				self.txt_aspect.setText(str(round(int(width)/int(height), 2)))
			except:
				pass
	
	def browseForOutput(self, *args, **kwargs):
		path = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose output directory")
		if path:
			self.txt_output.setText(path)



if __name__ == "__main__":

	app = QtWidgets.QApplication()

	wnd_settings = Settings()
	wnd_settings.show()

	# Aspect Ratio Calculator
	wnd_settings.txt_width.textChanged.connect(wnd_settings.updateAspectRatio)
	wnd_settings.txt_height.textChanged.connect(wnd_settings.updateAspectRatio)

	# Presets
	wnd_settings.cmb_presets.currentIndexChanged.connect(wnd_settings.setSizeFromPreset)
	wnd_settings.cmb_presets.addItem("Project: 4096 x 2048", (4096,2048))
	wnd_settings.cmb_presets.insertSeparator(1)
	wnd_settings.cmb_presets.addItem("4K: 4096 x 2048", (4096,2048))
	wnd_settings.cmb_presets.addItem("2K: 2048 x 1168", (2048,1168))
	wnd_settings.cmb_presets.addItem("HD: 1920 x 1080", (1920,1080))

	# Output directory
	wnd_settings.btn_browse.clicked.connect(wnd_settings.browseForOutput)

	app.exec_()