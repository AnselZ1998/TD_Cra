# -*- coding: utf-8 -*-

import os
from pipeline_core.util.qt_wrap import *
from pipeline_core.ui.frame import FrameRangeWidget
from pipeline_core.dcc.context import Context
from .utils import playblast, export


class PlayblastWindow(QWidget):
    def __init__(self):
        super(PlayblastWindow, self).__init__()

        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.frameRangeWidget = FrameRangeWidget()
        self.exportButton = QPushButton('Export')

        self.masterLayout.addWidget(self.frameRangeWidget)
        self.masterLayout.addWidget(self.exportButton)

        self.exportButton.clicked.connect(self.export_clicked)

    def export_clicked(self):
        element = 'playblast'
        filetype = 'jpg'

        version = Context.task.get_or_create_version(element, Context.number)
        versionPath = version.get_output_path()
        filename = '{entity}_{element}_{number}'.format(
            entity=Context.get_field('Entity'),
            element=element,
            number=Context.number
        )
        file = '{version}/{ext}/{filename}'.format(
            version=versionPath,
            ext=filetype,
            filename=filename
        )
        if not os.path.exists(os.path.dirname(file)):
            os.makedirs(os.path.dirname(file))

        file = playblast(
            file,
            startFrame=self.frameRangeWidget.get_frame_range()[0],
            endFrame=self.frameRangeWidget.get_frame_range()[1],
        )

        version.set_file(filetype, file.replace(versionPath, ''))


class ExportWindow(QWidget):
    def __init__(self):
        super(ExportWindow, self).__init__()

        self.masterLayout = QFormLayout()
        self.setLayout(self.masterLayout)

        self.frameRangeWidget = FrameRangeWidget()
        self.typeChoose = QButtonGroup()
        self.typeChoose.setExclusive(False)
        self.typeLayout = QHBoxLayout()
        for t in ['abc', 'fbx', 'obj', 'mb']:
            check = QCheckBox(t)
            check.setObjectName(t)
            self.typeChoose.addButton(check)
            self.typeLayout.addWidget(check)
        self.exportButton = QPushButton('Export')

        self.masterLayout.addRow('Frame:', self.frameRangeWidget)
        self.masterLayout.addRow('Type:', self.typeLayout)
        self.masterLayout.addWidget(self.exportButton)

        self.exportButton.clicked.connect(self.export_clicked)

    def export_clicked(self):
        pass


class ExportModWindow(ExportWindow):
    def export_clicked(self):
        element = 'master'
        filetypes = [i.objectName() for i in self.typeChoose.buttons() if i.isChecked()]

        version = Context.task.get_or_create_version(element, Context.number)
        versionPath = version.get_output_path()
        if not os.path.exists(versionPath):
            os.makedirs(versionPath)

        for filetype in filetypes:
            filename = '{entity}_{element}_{number}'.format(
                entity=Context.get_field('Entity'),
                element=element,
                number=Context.number
            )
            file = '{version}/{filename}.{ext}'.format(
                version=versionPath,
                ext=filetype,
                filename=filename
            )
            export(file, exportRoot='|master', options={'frameRange': self.frameRangeWidget.get_frame_range()})
            version.set_file(filetype, file.replace(versionPath, ''))


class ExportAniWindow(ExportWindow):
    def export_clicked(self):
        filetypes = [i.objectName() for i in self.typeChoose.buttons() if i.isChecked()]
        from .utils import get_pynode
        node = get_pynode('|master|chr')
        for child in node.getChildren():
            element = str(child.split(':')[0])

            version = Context.task.get_or_create_version(element, Context.number)
            versionPath = version.get_output_path()
            if not os.path.exists(versionPath):
                os.makedirs(versionPath)

            for filetype in filetypes:
                filename = '{entity}_{element}_{number}'.format(
                    entity=Context.get_field('Entity'),
                    element=element,
                    number=Context.number
                )
                file = '{version}/{filename}.{ext}'.format(
                    version=versionPath,
                    ext=filetype,
                    filename=filename
                )
                export(file, exportRoot='|master|chr|{}'.format(child), options={'frameRange': self.frameRangeWidget.get_frame_range()})
                version.set_file(filetype, file.replace(versionPath, ''))


def show_playblast_ui():
    w = PlayblastWindow()
    w.show()
    return w


def show_export_mod_ui():
    w = ExportModWindow()
    w.show()
    return w


def show_export_ani_ui():
    w = ExportAniWindow()
    w.show()
    return w



