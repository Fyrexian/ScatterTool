import random

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
        self.scatterscene = ScatterScene()
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
        self.scatter_btn.clicked.connect(self._scatter)
        self.scatterOGButton.clicked.connect(self._selectOG)
        """self.folder_browse_btn.clicked.connect(self._browse_folder)
        self.save_increment_btn.clicked.connect(self._save_increment)"""

    @QtCore.Slot()
    def _save_increment(self):
        self._set_scenefile_properties_from_ui()
        self.scenefile.save_increment()
        self.ver_sbx.setValue(self.scenefile.ver)

    @QtCore.Slot()
    def _scatter(self):
        """Save the Scene"""
        self._set_scenefile_properties_from_ui()
        """self.scenefile.save()"""
        self.scatterscene.scatter()

    @QtCore.Slot()
    def _selectOG(self):
        selected = cmds.ls(sl=True)
        print(selected[0])
        self.scatterOG.setText(selected[0])

    def _set_scenefile_properties_from_ui(self):
        self.scatterscene.scalenumbermin = self.RandomScalemin.value()
        self.scatterscene.scalenumbermax = self.RandomScalemax.value()
        self.scatterscene.rotationNumbermin = self.RandomRotationmin.value()
        self.scatterscene.rotationNumbermax = self.RandomRotationmax.value()
        self.scatterscene.objecttoscatter = self.scatterOG.text()
        """self.scenefile.folder_path = self.folder_le.text()
        self.scenefile.descriptor = self.descriptor_le.text()
        self.scenefile.task = self.task_le.text()
        self.scenefile.ver = self.ver_sbx.value()
        self.scenefile.ext = self.ext_lbl.text()"""

    """@QtCore.Slot()
    def _browse_folder(self):
        Opens a dialogue box to browse the folder
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self, caption="Select Folder", dir=self.folder_le.text(),
            options=QtWidgets.QFileDialog.ShowDirsOnly |
                    QtWidgets.QFileDialog.DontResolveSymlinks)
        self.folder_le.setText(folder)"""

    def _create_button_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
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
        layout.addWidget(self.scatterOGButton, 0, 2)
        layout.addWidget(QtWidgets.QLabel("Obj to Scatter on:"), 0, 3)
        layout.addWidget(self.scatterTo, 0, 4)
        layout.addWidget(self.scatterToButton, 0, 6)
        return layout

    def _create_objscaler_ui(self):
        """min settings"""
        self.RandomScalemin = QtWidgets.QDoubleSpinBox()
        self.RandomScalemin.setValue(self.scatterscene.scalenumbermin)
        self.RandomScalemin.setFixedWidth(100)
        """max settings"""
        self.RandomScalemax = QtWidgets.QDoubleSpinBox()
        self.RandomScalemax.setValue(self.scatterscene.scalenumbermax)
        self.RandomScalemax.setFixedWidth(100)
        """self.RandomScale = QtWidgets.setValue(self.scatterscene.scalenumber)"""
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Random Scale Min(only numbers):"), 0, 0)
        layout.addWidget(self.RandomScalemin, 0, 1)
        layout.addWidget(QtWidgets.QLabel("Random Scale Max(only numbers):"), 0, 2)
        layout.addWidget(self.RandomScalemax, 0, 3)
        return layout

    def _create_objrotation_ui(self):
        """min settings"""
        self.RandomRotationmin = QtWidgets.QDoubleSpinBox()
        self.RandomRotationmin.setValue(self.scatterscene.rotationNumbermin)
        self.RandomRotationmin.setFixedWidth(100)
        """max settings"""
        self.RandomRotationmax = QtWidgets.QDoubleSpinBox()
        self.RandomRotationmax.setValue(self.scatterscene.rotationNumbermax)
        self.RandomRotationmax.setFixedWidth(100)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Random Rotation Min(only numbers):"), 0, 0)
        layout.addWidget(self.RandomRotationmin, 0, 1)
        layout.addWidget(QtWidgets.QLabel("Random Rotation Max(only numbers):"), 0, 2)
        layout.addWidget(self.RandomRotationmax, 0, 3)
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

    def scattertest(self):
        verts = cmds.ls("pPlane1.vtx[*]", flatten=True)
        print(verts)
        self.scatter(verts)

    def scatter(verts, scatter_obj='pSphere1', align=True):
        for point in verts:
            print(point)
            pos = cmds.xform([point], query=True, worldSpace=True, translation=True)
            scatter_instance = cmds.instance(scatter_obj, name="scat_inst")
            cmds.move(pos[0], pos[1], pos[2], scatter_instance, worldSpace=True)
            if align:
                const = cmds.normalConstraint([point], scatter_instance)
                cmds.delete(const)


class ScatterScene:
    def __init__(self):
        self.verts = cmds.ls("pPlane1.vtx[*]", flatten=True)
        self.objecttoscatter = "pCube1"
        self.scalenumbermin = .1
        self.scalenumbermax = .2
        self.scalerandomnumber = .5
        self.rotationNumbermin = 3
        self.rotationNumbermax = 5


    def scattertest(self):
        """verts = cmds.ls("pPlane1.vtx[*]", flatten=True)"""
        print(self.verts)
        self.scatter()

    def scatter(self, align=True):
        scatter_obj = self.objecttoscatter
        for point in self.verts:
            print(point)
            pos = cmds.xform([point], query=True, worldSpace=True, translation=True)
            scatter_instance = cmds.instance(scatter_obj, name="scat_inst"+point)
            cmds.move(pos[0], pos[1], pos[2], scatter_instance, worldSpace=True)
            self.scalerandomnumber = random.uniform(self.scalenumbermin,self.scalenumbermax)
            cmds.scale(self.scalerandomnumber, self.scalerandomnumber,self.scalerandomnumber, scatter_instance, absolute=True)
            self.scalerandomnumber = random.uniform(self.rotationNumbermin, self.rotationNumbermax)
            if align:
                const = cmds.normalConstraint([point], scatter_instance)
                cmds.delete(const)
            cmds.rotate(self.scalerandomnumber, self.scalerandomnumber, self.scalerandomnumber, scatter_instance,
                        relative=True, componentSpace=True)

    """scene_file = SceneFile("D:/sandbox/tank_model_v001.ma")"""
    """scene_file = SceneFile("D:/sandbox/tank_model_v001.ma")
    verts = cmds.ls("pPlane1.vtx[*]", flatten=True)
    print(verts)
    scatter(verts)"""
