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
        self.setMinimumWidth(600)
        self.setMaximumHeight(300)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scatterscene = ScatterScene()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scattertool")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.Scatters_lay = self._create_objselector_ui()
        self.Scale_lay = self._create_objscaler_ui()
        self.Rotation_lay = self._create_objrotation_ui()
        self.VertexTitle_lbl = QtWidgets.QLabel("Scatter to Vertexes?")
        self.VertexTitle_lbl.setStyleSheet("font: bold 15px")
        self.VertexRandom_lay = self._vertexrandom_ui()
        self.Settings_lbl = QtWidgets.QLabel("Settings:")
        self.Settings_lbl.setStyleSheet("font: bold 13px")
        self.VertexSelector_lay = self._create_vertexselector_ui()
        self.NormalChecker_lay = self._normal_contstraint_ui()
        self.button_lay = self._create_button_ui()
        self.button_lay2 = self._create_button_ui2()
        self.button_lay3 = self._undo_btn_ui3()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.Scatters_lay)
        self.main_lay.addWidget(self.VertexTitle_lbl)
        self.main_lay.addLayout(self.VertexSelector_lay)
        self.main_lay.addLayout(self.VertexRandom_lay)
        self.main_lay.addWidget(self.Settings_lbl)
        self.main_lay.addLayout(self.Scale_lay)
        self.main_lay.addLayout(self.Rotation_lay)
        self.main_lay.addStretch()
        self.main_lay.addLayout(self.NormalChecker_lay)
        self.main_lay.addLayout(self.button_lay)
        self.main_lay.addLayout(self.button_lay2)
        self.main_lay.addLayout(self.button_lay3)
        self.setLayout(self.main_lay)

    def create_connections(self):
        self.scatter_btn.clicked.connect(self._scatter)
        self.scatterOGButton.clicked.connect(self._selectOG)
        self.scatterToButton.clicked.connect(self._selectTarget)
        self.scatterVX_ToButton.clicked.connect(self._scatterVX_To)
        self.scatterVX_btn.clicked.connect(self._scatter2)
        self.undo_btn.clicked.connect(self._deleteLastScatter)

    @QtCore.Slot()
    def _scatter(self):
        """scatters"""
        self._set_scenefile_properties_from_ui()
        self.scatterscene.scatter()

    @QtCore.Slot()
    def _scatter2(self):
        """scatters"""
        self._set_scenefile_properties_from_ui()
        self.scatterscene.scatter2()

    @QtCore.Slot()
    def _selectOG(self):
        selected = cmds.ls(sl=True)
        print(selected[0])
        self.scatterOG.setText(selected[0])

    @QtCore.Slot()
    def _selectTarget(self):
        selected = cmds.ls(sl=True)
        print(selected[0])
        self.scatterTo.setText(selected[0])

    @QtCore.Slot()
    def _scatterVX_To(self):
        verts = cmds.ls(selection=True, flatten=True)
        selected = cmds.ls(sl=True)
        print(verts)
        self.scatterVX_To.setText(verts[0])
        self.scatterscene.vertexesToTarget = verts

    def _deleteLastScatter(self):
        self.scatterscene.deleteLastScatter()

    def _set_scenefile_properties_from_ui(self):
        self.scatterscene.scalenumbermin = self.RandomScalemin.value()
        self.scatterscene.scalenumbermax = self.RandomScalemax.value()
        self.scatterscene.rotationNumbermin = self.RandomRotationmin.value()
        self.scatterscene.rotationNumbermax = self.RandomRotationmax.value()
        self.scatterscene.objecttoscatter = self.scatterOG.text()
        self.scatterscene.objecttoTarget = self.scatterTo.text()
        self.scatterscene.randomVertexes = self.RandomVertexes.value()
        self.scatterscene.NormalChecker1 = self.NormalChecker.checkState()

    def _create_button_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        return layout

    def _create_objselector_ui(self):
        self.scatterOG = QtWidgets.QLineEdit()
        self.scatterOGButton = QtWidgets.QPushButton("Select")
        self.scatterTo = QtWidgets.QLineEdit()
        self.scatterToButton = QtWidgets.QPushButton("Select")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Obj to Scatter:"), 0, 0)
        layout.addWidget(self.scatterOG, 1, 0)
        layout.addWidget(self.scatterOGButton, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Obj to Scatter on:"), 0, 0)
        layout.addWidget(self.scatterTo, 1, 0)
        layout.addWidget(self.scatterToButton, 0, 0)
        return layout

    def _create_objscaler_ui(self):
        """min settings"""
        self.RandomScalemin = QtWidgets.QDoubleSpinBox()
        self.RandomScalemin.setValue(self.scatterscene.scalenumbermin)
        self.RandomScalemin.setFixedWidth(100)
        self.RandomScalemin.setMaximum(999)
        """max settings"""
        self.RandomScalemax = QtWidgets.QDoubleSpinBox()
        self.RandomScalemax.setValue(self.scatterscene.scalenumbermax)
        self.RandomScalemax.setFixedWidth(100)
        self.RandomScalemax.setMaximum(999)
        """self.RandomScale = QtWidgets.setValue(self.scatterscene.scalenumber)"""
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Random Scale Min(only numbers):"), 0, 0)
        layout.addWidget(self.RandomScalemin, 1, 0)
        layout.addWidget(QtWidgets.QLabel("Random Scale Max(only numbers):"), 1, 1)
        layout.addWidget(self.RandomScalemax, 4, 1)
        return layout

    def _create_objrotation_ui(self):
        """min settings"""
        self.RandomRotationmin = QtWidgets.QDoubleSpinBox()
        self.RandomRotationmin.setValue(self.scatterscene.rotationNumbermin)
        self.RandomRotationmin.setFixedWidth(100)
        self.RandomRotationmin.setMaximum(360)
        """max settings"""
        self.RandomRotationmax = QtWidgets.QDoubleSpinBox()
        self.RandomRotationmax.setValue(self.scatterscene.rotationNumbermax)
        self.RandomRotationmax.setFixedWidth(100)
        self.RandomRotationmax.setMaximum(360)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Random Rotation Min(only numbers):"), 0, 0)
        layout.addWidget(self.RandomRotationmin, 1, 0)
        layout.addWidget(QtWidgets.QLabel("Random Rotation Max(only numbers):"), 1, 1)
        layout.addWidget(self.RandomRotationmax, 4, 1)
        return layout

    def _normal_contstraint_ui(self):
        self.NormalChecker = QtWidgets.QCheckBox()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Align to the normals:"), 0, 0)
        layout.addWidget(self.NormalChecker, 1, 0)
        return layout

    def _undo_btn_ui3(self):
        self.undo_btn = QtWidgets.QPushButton("Undo Last Scatter")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.undo_btn)
        return layout

    """--------------------------------------------------------------------------------------------------------------"""
    """Vertex layout"""

    def _create_button_ui2(self):
        self.scatterVX_btn = QtWidgets.QPushButton("Scatter to Vertexes")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatterVX_btn)
        return layout

    def _create_vertexselector_ui(self):
        """vertex selector"""
        self.scatterVX_To = QtWidgets.QLineEdit()
        self.scatterVX_ToButton = QtWidgets.QPushButton("Select")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Vertexes to Scatter on:"), 0, 0)
        layout.addWidget(self.scatterVX_To, 0, 0)
        layout.addWidget(self.scatterVX_ToButton, 0, 0)
        return layout

    def _vertexrandom_ui(self):
        self.RandomVertexes = QtWidgets.QSpinBox()
        self.RandomVertexes.setFixedWidth(100)
        self.RandomVertexes.setMinimum(0)
        self.RandomVertexes.setMaximum(100)
        self.RandomVertexes.setValue(100)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Random Percentage(only whole numbers):"), 0, 0)
        layout.addWidget(self.RandomVertexes, 1, 1)
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
        self.objecttoTarget = "pSphere1"
        self.verts = cmds.ls(self.objecttoTarget+".vtx[*]", flatten=True)
        """print(self.verts)"""
        self.objecttoscatter = "pCube1"
        self.scalenumbermin = .1
        self.scalenumbermax = .2
        self.scalerandomnumber = .5
        self.scalerandomnumber2 = .5
        self.scalerandomnumber3 = .5
        self.rotationNumbermin = 3
        self.rotationNumbermax = 5

        self.vertexesToTarget = cmds.ls(self.objecttoTarget+".vtx[*]", flatten=True)
        self.randomVertexes = 100
        self.NormalChecker1 = False;
        self.LastScatterGroup = [0, 1]
        del self.LastScatterGroup[:]


    def scattertest(self):
        """verts = cmds.ls("pPlane1.vtx[*]", flatten=True)"""
        print(self.verts)
        """self.scatter()"""

    def scatter(self, align=True):
        self.verts = cmds.ls(self.objecttoTarget + ".vtx[*]", flatten=True)
        del self.LastScatterGroup[:]
        print(self.verts)
        scatter_obj = self.objecttoscatter
        for point in self.verts:
            print(point)
            pos = cmds.xform([point], query=True, worldSpace=True, translation=True)
            scatter_instance = cmds.instance(scatter_obj, name=self.objecttoscatter+"_scat_inst_"+point)
            self.LastScatterGroup.append(scatter_instance)
            cmds.move(pos[0], pos[1], pos[2], scatter_instance, worldSpace=True)
            self.scalerandomnumber = random.uniform(self.scalenumbermin,self.scalenumbermax)
            self.scalerandomnumber2 = random.uniform(self.scalenumbermin, self.scalenumbermax)
            self.scalerandomnumber3 = random.uniform(self.scalenumbermin, self.scalenumbermax)
            cmds.scale(self.scalerandomnumber, self.scalerandomnumber2,self.scalerandomnumber3, scatter_instance, absolute=True)
            self.scalerandomnumber = random.uniform(self.rotationNumbermin, self.rotationNumbermax)
            self.scalerandomnumber2 = random.uniform(self.rotationNumbermin, self.rotationNumbermax)
            self.scalerandomnumber3 = random.uniform(self.rotationNumbermin, self.rotationNumbermax)
            if not self.NormalChecker1:
                if align:
                    const = cmds.normalConstraint([point], scatter_instance)
                    cmds.delete(const)
            else:
                const = cmds.normalConstraint([point], scatter_instance, aimVector=[0.0, 1.0, 0.0])
            cmds.rotate(self.scalerandomnumber, self.scalerandomnumber2, self.scalerandomnumber3, scatter_instance,
                        relative=True, componentSpace=True)

    def scatter2(self, align=True):
        scatter_obj = self.objecttoscatter
        len(self.vertexesToTarget)
        del self.LastScatterGroup[:]
        random_amount = int(round(len(self.vertexesToTarget) * (self.randomVertexes*.01)))
        print(random_amount)
        percentage_selection = random.sample(self.vertexesToTarget, k=random_amount)
        for vert in percentage_selection:
            pos = cmds.xform([vert], query=True, worldSpace=True, translation=True)
            scatter_instance = cmds.instance(scatter_obj, name=self.objecttoscatter+"_scat_inst_"+vert)
            self.LastScatterGroup.append(scatter_instance)
            cmds.move(pos[0], pos[1], pos[2], scatter_instance, worldSpace=True)
            nconst = cmds.normalConstraint([vert], scatter_instance)
            cmds.delete(nconst)
            self.scalerandomnumber = random.uniform(self.scalenumbermin, self.scalenumbermax)
            self.scalerandomnumber2 = random.uniform(self.scalenumbermin, self.scalenumbermax)
            self.scalerandomnumber3 = random.uniform(self.scalenumbermin, self.scalenumbermax)
            cmds.scale(self.scalerandomnumber, self.scalerandomnumber2, self.scalerandomnumber3, scatter_instance,
                       absolute=True)
            self.scalerandomnumber = random.uniform(self.rotationNumbermin, self.rotationNumbermax)
            self.scalerandomnumber2 = random.uniform(self.rotationNumbermin, self.rotationNumbermax)
            self.scalerandomnumber3 = random.uniform(self.rotationNumbermin, self.rotationNumbermax)
            if not self.NormalChecker1:
                if align:
                    const = cmds.normalConstraint([vert], scatter_instance)
                    cmds.delete(const)
            else:
                const = cmds.normalConstraint([vert], scatter_instance, aimVector=[0.0, 1.0, 0.0])
            cmds.rotate(self.scalerandomnumber, self.scalerandomnumber2, self.scalerandomnumber3, scatter_instance,
                        relative=True, componentSpace=True)

    def deleteLastScatter(self):
        for eachSel in self.LastScatterGroup:
            cmds.select(eachSel)
            cmds.delete(eachSel)


    """scene_file = SceneFile("D:/sandbox/tank_model_v001.ma")"""
    """scene_file = SceneFile("D:/sandbox/tank_model_v001.ma")
    verts = cmds.ls("pPlane1.vtx[*]", flatten=True)
    print(verts)
    scatter(verts)"""
