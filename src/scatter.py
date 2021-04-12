from pymel.core.system import Path
import pymel.core as pmc
import logging
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

log = logging.getLogger(__name__)

def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """Smart Class UI Class"""
    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter")
        self.setMinimumWidth(500)
        self.setMaximumHeight(200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scenefile = SceneFile()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scattertool")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.Scatters_lay = self._create_objselector_ui()
        self.Scale_lay = self._create_objscaler_ui()
        self.Rotation_lay = self._create_objrotation_ui()
        """self.filename_lay = self._create_filename_ui()"""
        self.button_lay = self._create_button_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.Scatters_lay)
        self.main_lay.addLayout(self.Scale_lay)
        self.main_lay.addLayout(self.Rotation_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    def create_connections(self):
        self.save_btn.clicked.connect(self._save)
        """self.folder_browse_btn.clicked.connect(self._browse_folder)
        self.save_increment_btn.clicked.connect(self._save_increment)"""



    @QtCore.Slot()
    def _save_increment(self):
        self._set_scenefile_properties_from_ui()
        self.scenefile.save_increment()
        self.ver_sbx.setValue(self.scenefile.ver)


    @QtCore.Slot()
    def _save(self):
        """Save the Scene"""
        self._set_scenefile_properties_from_ui()
        self.scenefile.save()

    def _set_scenefile_properties_from_ui(self):
        self.scenefile.folder_path = self.folder_le.text()
        self.scenefile.descriptor = self.descriptor_le.text()
        self.scenefile.task = self.task_le.text()
        self.scenefile.ver = self.ver_sbx.value()
        self.scenefile.ext = self.ext_lbl.text()

    @QtCore.Slot()
    def _browse_folder(self):
        """Opens a dialogue box to browse the folder"""
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self, caption="Select Folder", dir=self.folder_le.text(),
            options=QtWidgets.QFileDialog.ShowDirsOnly |
            QtWidgets.QFileDialog.DontResolveSymlinks)
        self.folder_le.setText(folder)


    def _create_button_ui(self):
        self.save_btn = QtWidgets.QPushButton("Scatter")
        """self.save_increment_btn = QtWidgets.QPushButton("Save Increment")
        layout.addWidget(self.save_increment_btn)"""
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.save_btn)
        return layout

    """
    def _create_filename_ui(self):
        layout = self._create_filename_headers()
        self.descriptor_le = QtWidgets.QLineEdit(self.scenefile.descriptor)
        self.descriptor_le.setMinimumWidth(50)
        self.task_le = QtWidgets.QLineEdit(self.scenefile.task)
        self.task_le.setFixedWidth(50)
        self.ver_sbx = QtWidgets.QSpinBox()
        self.ver_sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.ver_sbx.setFixedWidth(50)
        self.ver_sbx.setValue(self.scenefile.ver)

        layout.addWidget(self.descriptor_le, 1, 0)
        layout.addWidget(QtWidgets.QLabel("_"), 1, 1)
        layout.addWidget(self.task_le, 1, 2)
        layout.addWidget(QtWidgets.QLabel("_v"), 1, 3)
        layout.addWidget(self.ver_sbx, 1, 4)

        return layout

    def _create_filename_headers(self):
        self.descriptor_header_lbl = QtWidgets.QLabel("Random Scale(numbers only)")
        self.descriptor_header_lbl.setStyleSheet("font: bold")
        self.task_header_lbl = QtWidgets.QLabel("Task")
        self.task_header_lbl.setStyleSheet("font: bold")
        self.ver_header_lbl = QtWidgets.QLabel("Version")
        self.ver_header_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.descriptor_header_lbl, 0, 0)
        layout.addWidget(self.task_header_lbl, 0, 2)
        layout.addWidget(self.ver_header_lbl, 0, 4)
        return layout"""

    def _create_objselector_ui(self):

        self.scatterOG = QtWidgets.QLineEdit()
        self.scatterOGButton = QtWidgets.QPushButton("Select")
        self.scatterTo = QtWidgets.QLineEdit()
        self.scatterToButton = QtWidgets.QPushButton("Select")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Obj to Scatter:"), 0, 0)
        layout.addWidget(self.scatterOG, 0, 1)
        layout.addWidget(self.scatterOGButton, 0 , 2)
        layout.addWidget(QtWidgets.QLabel("Obj to Scatter on:"), 0, 3)
        layout.addWidget(self.scatterTo, 0, 4)
        layout.addWidget(self.scatterToButton, 0, 6)
        return layout

    def _create_objscaler_ui(self):
        self.RandomScale = QtWidgets.QLineEdit()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Random Scale(only numbers):"), 0, 0)
        layout.addWidget(self.RandomScale, 0, 0)
        return layout

    def _create_objrotation_ui(self):
        self.RandomRotation = QtWidgets.QLineEdit()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Random Rotation(only numbers):"), 0, 0)
        layout.addWidget(self.RandomRotation, 0, 0)
        return layout


class SceneFile(object):
    """An abstract representation of a Scene file."""

    def __init__(self, path=None):
        self._folder_path = Path(cmds.workspace(query=True,
                                                rootDirectory=True)) / "scenes"
        self.descriptor = 'main'
        self.task = 'model'
        self.ver = 1
        self.ext = '.ma'
        scene = pmc.system.sceneName()
        if not path and scene:
            path = scene
        if not path and not scene:
            log.info("Initialize with default properties")
            return
        self._init_from_path(path)

    @property
    def folder_path(self):
        return self._folder_path

    @folder_path.setter
    def folder_path(self, val):
        self._folder_path = Path(val)

    @property
    def filename(self):
        pattern = "{descriptor}_{task}_v{ver:03d}{ext}"
        return pattern.format(descriptor=self.descriptor,
                              task=self.task,
                              ver=self.ver,
                              ext=self.ext)

    @property
    def path(self):
        return self.folder_path / self.filename

    def _init_from_path(self, path=None):
        path = Path(path)
        self.folder_path = path.parent
        self.ext = path.ext
        self.descriptor, self.task, ver = path.name.stripext().split("_")
        self.ver = int(ver.split("v")[-1])

    def save(self):
        """saves the scenefile"""
        try:
            return pmc.system.saveAs(self.path)
        except RuntimeError as err:
            log.warning("Missing directories in path. Creating folders.")
            self.folder_path.makedirs_p()
            return pmc.system.saveAs(self.path)

    def next_avail_ver(self):
        pattern = "{descriptor}_{task}_v*{ext}".format(
            descriptor=self.descriptor, task=self.task, ext=self.ext)
        matching_scenefiles = []
        for file_ in self.folder_path.files():
            if file_.name.fnmatch(pattern):
                matching_scenefiles.append(file_)
        if not matching_scenefiles:
            return 1
        matching_scenefiles.sort(reverse=True)
        latest_scenefile = matching_scenefiles[0]
        latest_scenefile = latest_scenefile.name.stripext()
        latest_version_num = int(latest_scenefile.split("_v")[-1])
        return latest_version_num + 1

    def save_increment(self):
        """Increments"""
        self.ver = self.next_avail_ver()
        self.save()