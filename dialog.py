from PySide2 import QtWidgets, QtGui
import upco_leader
import pathlib
from PIL import Image, ImageColor

class Settings(QtWidgets.QDialog):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setFixedWidth(225)
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
		self.spin_width = QtWidgets.QSpinBox()
		self.spin_width.setRange(1,9999)
		self.lay_dimensions.addWidget(self.spin_width, 2, 0)

		self.lbl_by = QtWidgets.QLabel('x')
		self.lay_dimensions.addWidget(self.lbl_by, 2, 1)

		self.lbl_height = QtWidgets.QLabel("Height")
		self.lay_dimensions.addWidget(self.lbl_height, 1, 2)
		self.spin_height = QtWidgets.QSpinBox()
		self.spin_height.setRange(1,9999)
		self.lay_dimensions.addWidget(self.spin_height, 2, 2)

		self.spacer_horizontal = QtWidgets.QSpacerItem(1,1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.lay_dimensions.addItem(self.spacer_horizontal, 2, 3, 2, 1)

		self.lbl_aspect = QtWidgets.QLabel("Aspect")
		self.lay_dimensions.addWidget(self.lbl_aspect, 1, 4)
		self.spin_aspect = QtWidgets.QDoubleSpinBox()
		self.spin_aspect.setDecimals(3)
		self.spin_aspect.setRange(0.001, 999)
		self.spin_aspect.setSingleStep(0.01)
		self.lay_dimensions.addWidget(self.spin_aspect, 2, 4)

		# Output dir
		self.grp_output = QtWidgets.QGroupBox("Output Path")
		self.lay_output = QtWidgets.QHBoxLayout()
		self.grp_output.setLayout(self.lay_output)
		self.lay_main.addWidget(self.grp_output)

		self.txt_output = QtWidgets.QLineEdit()
		self.lay_output.addWidget(self.txt_output)

		self.btn_browse = QtWidgets.QPushButton("...")
		self.btn_browse.setAutoDefault(False)
		self.btn_browse.setFixedWidth(30)
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
		
		try:
			width, height = self.cmb_presets.itemData(idx)
		except:
			return
		
		self.spin_aspect.blockSignals(True)
		self.spin_width.blockSignals(True)
		self.spin_height.blockSignals(True)

		self.spin_width.setValue(width)
		self.spin_height.setValue(height)
		self.spin_aspect.setValue(width/height)
		
		self.spin_width.blockSignals(False)
		self.spin_height.blockSignals(False)
		self.spin_aspect.blockSignals(False)
	
	def updateAspectRatio(self):
		width = self.spin_width.value()
		height= self.spin_height.value()

		self.cmb_presets.blockSignals(True)
		self.cmb_presets.setCurrentIndex(self.cmb_presets.count()-1)
		self.cmb_presets.blockSignals(False)

		self.spin_aspect.blockSignals(True)
		self.spin_aspect.setValue(width/height)
		self.spin_aspect.blockSignals(False)
	
	def setAspectRatio(self):
		self.spin_height.blockSignals(True)

		height = self.spin_width.value() // self.spin_aspect.value()
		if height % 2: height+=1
		self.spin_height.setValue(height)
		self.spin_height.blockSignals(False)
	
	def browseForOutput(self, *args, **kwargs):
		path = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose output directory", self.txt_output.text())
		if path:
			self.txt_output.setText(path)
	
	def validateForm(self):
		if self.txt_title.text().strip() and self.txt_output.text().strip():
			self.btn_ok.setEnabled(True)
		else:
			self.btn_ok.setEnabled(False)

	def renderLeader(self):
		width  = self.spin_width.value()
		height = self.spin_height.value()
		width_active  = width * 0.85
		height_active = height * 0.9

		frame_start = 8600
		frame_count = 8 * 24

		try:
			path_output = pathlib.Path(self.txt_output.text())
			path_output.mkdir(exist_ok=True, parents=True)

		except Exception as e:
			print(f"Error: {e}")
			return
		
		self.prog_status.setRange(frame_start, frame_start + frame_count)

		# Draw reticle
		reticle = upco_leader.drawFrameOverlay(frame_width=width, frame_height=height, active_width=width_active, active_height=height_active)
		star    = upco_leader.drawStar(spokes=48 ,radius=int(width * 0.04))


		for x in range(frame_start, frame_start + frame_count):
			self.prog_status.setValue(x)

			if x < ((frame_start + frame_count) - (2*24)):
				#print(x,  ((frame_start + frame_count) - (2*24)))
				frame = Image.new("RGBA", (width, height), ImageColor.getrgb("rgba(128,128,128,255)"))
				frame.alpha_composite(reticle)
				frame.alpha_composite(star, dest=(400,200))
				frame.alpha_composite(star, dest=(400, height-200-star.height))
				frame.alpha_composite(star, dest=(width-400-star.width, 200))
				frame.alpha_composite(star, dest=(width-400-star.width, height-200-star.height))
			
			else:
				#print(x,  ((frame_start + frame_count) - (2*24)))
				frame = Image.new("RGBA", (width, height), ImageColor.getrgb("rgba(0,0,0,255)"))

			count = upco_leader.drawCountdown(radius=600,frame = x-frame_start)
			#print(width//2, count.width//2, height//2, count.height//2)
			frame.alpha_composite(count, dest=(width//2 - count.width//2, height//2 - count.height//2))

			frame_output = path_output / f"{self.txt_title.text().strip()}_{width}x{height}.{str(x).zfill(6)}.tif"
			frame.save(str(frame_output))
			






if __name__ == "__main__":

	app = QtWidgets.QApplication()

#	app.setStyle("Fusion")

	wnd_settings = Settings()
	wnd_settings.show()

	# Project Title Set
	wnd_settings.btn_ok.setEnabled(False)
	wnd_settings.txt_title.textChanged.connect(wnd_settings.validateForm)
	wnd_settings.txt_output.textChanged.connect(wnd_settings.validateForm)

	# Aspect Ratio Calculator
	wnd_settings.spin_width.valueChanged.connect(wnd_settings.updateAspectRatio)
	wnd_settings.spin_height.valueChanged.connect(wnd_settings.updateAspectRatio)
	wnd_settings.spin_aspect.valueChanged.connect(wnd_settings.setAspectRatio)

	# Presets
	wnd_settings.cmb_presets.currentIndexChanged.connect(wnd_settings.setSizeFromPreset)
	wnd_settings.cmb_presets.addItem("Project: 4096 x 2160", (4096,2160))
	wnd_settings.cmb_presets.insertSeparator(wnd_settings.cmb_presets.count())
	wnd_settings.cmb_presets.addItem("4K: 4096 x 2160", (4096,2160))
	wnd_settings.cmb_presets.addItem("4K: 4096 x 1716", (4096,1716))
	wnd_settings.cmb_presets.addItem("4K: 3996 x 2160", (3996,2160))
	wnd_settings.cmb_presets.addItem("4K: 3840 x 2160", (3840,2160))
	wnd_settings.cmb_presets.insertSeparator(wnd_settings.cmb_presets.count())
	wnd_settings.cmb_presets.addItem("2K: 2048 x 1080", (2048,1080))
	wnd_settings.cmb_presets.addItem("2K: 2048 x 858", (2048,858))
	wnd_settings.cmb_presets.addItem("2K: 1998 x 1080", (1998,1080))
	wnd_settings.cmb_presets.insertSeparator(wnd_settings.cmb_presets.count())
	wnd_settings.cmb_presets.addItem("HD: 1920 x 1080", (1920,1080))
	wnd_settings.cmb_presets.addItem("Custom...")

	# Output directory
	wnd_settings.btn_browse.clicked.connect(wnd_settings.browseForOutput)

	# Generate
	wnd_settings.btn_ok.clicked.connect(wnd_settings.renderLeader)

	app.exec_()