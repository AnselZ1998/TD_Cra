# -*- coding: utf-8 -*-

from pipeline_core.util.qt_wrap import *
from pipeline_core.dcc.wrap import DccWrap
from .version_tree import VersionTree
from .file_tree import FileTree
from pipeline_core.dcc.context import Context
from pipeline_core.path.util import version_up


class EntityListItem(QListWidgetItem):
    def __init__(self, entity):
        super(EntityListItem, self).__init__()

        self.entity = entity
        self.setText(entity.name)


class AssetTypeItem(QListWidgetItem):
    def __init__(self, type, project):
        super(AssetTypeItem, self).__init__()

        self.type = type
        self.project = project
        self.setText(type)


class ProjectManager(QWidget):
    def __init__(self):
        super(ProjectManager, self).__init__()

        self.init_ui()
        self.create_connect()
        self.refresh_projects()
        self.refresh_info()

        DccWrap.add_on_script_load(self.refresh_info)
        DccWrap.add_on_script_save(self.refresh_info)

    def init_ui(self):
        self.setObjectName('ProjectManager')

        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.infoLayout = QHBoxLayout()
        self.projectLabel = QLabel()
        self.assetLabel = QLabel()
        self.shotLabel = QLabel()
        self.taskLabel = QLabel()
        self.elementLabel = QLabel()
        self.infoLayout.addWidget(self.projectLabel)
        self.infoLayout.addWidget(self.assetLabel)
        self.infoLayout.addWidget(self.shotLabel)
        self.infoLayout.addWidget(self.taskLabel)
        self.infoLayout.addWidget(self.elementLabel)

        self.upLayout = QHBoxLayout()
        self.downLayout = QHBoxLayout()

        self.projectList = QListWidget()
        self.assetTypeList = QListWidget()
        self.assetList = QListWidget()
        self.sequenceList = QListWidget()
        self.shotList = QListWidget()
        self.taskList = QListWidget()

        self.switchTab1 = QTabWidget()

        self.assetBox = QWidget()
        self.assetLayout = QHBoxLayout()
        self.assetLayout.addWidget(self.assetTypeList)
        self.assetLayout.addWidget(self.assetList)
        self.assetBox.setLayout(self.assetLayout)

        self.shotBox = QWidget()
        self.shotLayout = QHBoxLayout()
        self.shotLayout.addWidget(self.sequenceList)
        self.shotLayout.addWidget(self.shotList)
        self.shotBox.setLayout(self.shotLayout)

        self.switchTab1.addTab(self.assetBox, 'asset')
        self.switchTab1.addTab(self.shotBox, 'shot')

        self.switchTab2 = QTabWidget()

        self.workFileTree = FileTree()
        self.saveButton = QPushButton('Save')
        self.saveAsButton = QToolButton()
        self.saveAsMenu = QMenu(self.saveAsButton)
        self.saveAsButton.setMenu(self.saveAsMenu)
        self.saveAsButton.setPopupMode(QToolButton.InstantPopup)
        self.openButton = QPushButton('Open')
        self.workButtonLayout = QHBoxLayout()
        self.workButtonLayout.addWidget(self.saveButton)
        self.workButtonLayout.addWidget(self.saveAsButton)
        self.workButtonLayout.addWidget(self.openButton)

        self.workBox = QWidget()
        self.workLayout = QVBoxLayout()
        self.workBox.setLayout(self.workLayout)
        self.workLayout.addWidget(self.workFileTree)
        self.workLayout.addLayout(self.workButtonLayout)

        self.versionTree = VersionTree()
        self.outputFileTree = FileTree()
        self.loadButton = QPushButton('Load')

        self.outputBox = QWidget()
        self.outputLayout = QHBoxLayout()
        self.outputBox.setLayout(self.outputLayout)
        self.outputFileLayout = QVBoxLayout()
        self.outputFileLayout.addWidget(self.outputFileTree)
        self.outputFileLayout.addWidget(self.loadButton)
        self.outputLayout.addWidget(self.versionTree)
        self.outputLayout.addLayout(self.outputFileLayout)

        self.switchTab2.addTab(self.workBox, 'work')
        self.switchTab2.addTab(self.outputBox, 'output')

        self.upLayout.addWidget(self.projectList)
        self.upLayout.addWidget(self.switchTab1)

        self.downLayout.addWidget(self.taskList)
        self.downLayout.addWidget(self.switchTab2)

        self.masterLayout.addLayout(self.infoLayout)
        self.masterLayout.addLayout(self.upLayout)
        self.masterLayout.addLayout(self.downLayout)

    def create_connect(self):
        self.projectList.itemSelectionChanged.connect(self.project_changed)
        self.assetTypeList.itemSelectionChanged.connect(self.assettype_changed)
        self.assetList.itemSelectionChanged.connect(self.asset_changed)
        self.sequenceList.itemSelectionChanged.connect(self.sequence_changed)
        self.shotList.itemSelectionChanged.connect(self.shot_changed)
        self.taskList.itemSelectionChanged.connect(self.task_changed)
        self.versionTree.itemSelectionChanged.connect(self.version_changed)

        self.saveButton.clicked.connect(self.save_clicked)
        self.openButton.clicked.connect(self.open_clicked)
        self.loadButton.clicked.connect(self.load_clicked)

    def refresh_projects(self):
        from pipeline_db.models import Project
        self.projectList.clear()
        projects = Project.objects.all()
        for project in projects:
            item = EntityListItem(project)
            self.projectList.addItem(item)

    def project_changed(self):
        if len(self.projectList.selectedItems()) == 0:
            return
        selected = self.projectList.selectedItems()[0]
        project = selected.entity

        self.assetTypeList.clear()
        self.assetList.clear()

        assets = project.assets.all()
        assettypes = []
        for a in assets:
            if a.type not in assettypes:
                assettypes.append(a.type)
        for type in assettypes:
            item = AssetTypeItem(type, project)
            self.assetTypeList.addItem(item)

        self.sequenceList.clear()
        self.shotList.clear()
        for seq in project.sequences.all():
            item = EntityListItem(seq)
            self.sequenceList.addItem(item)

    def assettype_changed(self):
        if len(self.assetTypeList.selectedItems()) == 0:
            return
        selected = self.assetTypeList.selectedItems()[0]

        self.assetList.clear()
        type = selected.type
        project = selected.project
        assets = project.assets.filter(type__exact=type)
        for a in assets:
            item = EntityListItem(a)
            self.assetList.addItem(item)

    def asset_changed(self):
        if len(self.assetList.selectedItems()) == 0:
            return
        selected = self.assetList.selectedItems()[0]

        self.taskList.clear()
        for t in selected.entity.tasks.all():
            item = EntityListItem(t)
            self.taskList.addItem(item)

    def sequence_changed(self):
        if len(self.sequenceList.selectedItems()) == 0:
            return
        selected = self.sequenceList.selectedItems()[0]

        self.shotList.clear()
        for t in selected.entity.shots.all():
            item = EntityListItem(t)
            self.shotList.addItem(item)

    def shot_changed(self):
        if len(self.shotList.selectedItems()) == 0:
            return
        selected = self.shotList.selectedItems()[0]

        self.taskList.clear()
        for t in selected.entity.tasks.all():
            item = EntityListItem(t)
            self.taskList.addItem(item)

    def task_changed(self):
        if len(self.taskList.selectedItems()) == 0:
            return
        selected = self.taskList.selectedItems()[0]
        task = selected.entity
        self.refresh_from_task(task)

    def refresh_from_task(self, task):
        dcc = DccWrap.get_dcc_name()
        if dcc is not None:
            taskPath = task.get_work_path(dcc)
            self.workFileTree.set_dir(taskPath)

        versions = task.versions.all()
        self.versionTree.set_versions(versions)
        self.refresh_saveas(task)

    def version_changed(self):
        if len(self.versionTree.selectedItems()) == 0:
            return
        selected = self.versionTree.selectedItems()[0]
        version = selected.version
        outputPath = version.get_output_path()
        self.outputFileTree.set_dir(outputPath)
        self.outputFileTree.version = version

    def refresh_saveas(self, task):
        versions = task.versions.all()
        elements = []
        for v in versions:
            if v.element not in elements:
                elements.append(v.element)
        elements.append('New...')
        self.saveAsMenu.clear()
        for e in elements:
            action = QAction(e, self.saveAsMenu)
            self.saveAsMenu.addAction(action)
            action.triggered.connect(self.save_as_action_triggered)

    def save_as_action_triggered(self):
        element = self.sender().text()
        if element == 'New...':
            element, r = QInputDialog.getText(None, 'New Element', 'Name:')
            if not r:
                return
        self.save_as_element(element)

    def save_as_element(self, element):
        number = Context.number
        currentTask = Context.task
        if len(self.taskList.selectedItems()) > 0:
            task = self.taskList.selectedItems()[0].entity
        else:
            task = Context.task
        if currentTask != None and task.id != currentTask.id:
            next = number
        else:
            next = version_up(number)
        file = task.get_work_file(DccWrap.get_dcc_name(), element, next)
        DccWrap.save_as(file)
        self.workFileTree.refresh_tree()

    def save_clicked(self):
        element = Context.element
        self.save_as_element(element)

    def open_clicked(self):
        file = self.workFileTree.selectedItems()[0].get_file_path()
        DccWrap.open_script(file)

    def load_clicked(self):
        file = self.outputFileTree.selectedItems()[0].get_file_path()
        version = self.versionTree.selectedItems()[0].version
        DccWrap.load_file(file, version)

    def refresh_info(self, *args, **kwargs):
        print('refresh info')
        task = Context.task
        if task is None:
            return
        self.projectLabel.setText(task.project.name)
        if task.asset is not None:
            self.shotLabel.setVisible(False)
            self.assetLabel.setVisible(True)
            self.assetLabel.setText(task.asset.name)
        if task.shot is not None:
            self.assetLabel.setVisible(False)
            self.shotLabel.setVisible(True)
            self.shotLabel.setText(task.shot.name)
        self.taskLabel.setText(task.name)
        self.elementLabel.setText(Context.element)

        if len(self.taskList.selectedItems()) == 0:
            self.expand_task(task)

    def expand_task(self, task):
        project = task.project
        for i in range(self.projectList.count()):
            item = self.projectList.item(i)
            if item.entity == project:
                item.setSelected(True)

        asset = task.asset
        if asset is not None:
            assettype = task.asset.type
            for i in range(self.assetTypeList.count()):
                item = self.assetTypeList.item(i)
                if item.type == assettype:
                    item.setSelected(True)

            for i in range(self.assetList.count()):
                item = self.assetList.item(i)
                if item.entity == asset:
                    item.setSelected(True)

        shot = task.shot
        if shot is not None:
            sequence = task.shot.sequence
            for i in range(self.sequenceList.count()):
                item = self.sequenceList.item(i)
                if item.entity == sequence:
                    item.setSelected(True)

            for i in range(self.shotList.count()):
                item = self.shotList.item(i)
                if item.entity == shot:
                    item.setSelected(True)

        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            if item.entity == task:
                item.setSelected(True)


def main():
    import sys
    app = QApplication(sys.argv)
    w = ProjectManager()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


