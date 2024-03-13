# -*- coding: utf-8 -*-

from pipeline_core.util.qt_wrap import *


class VersionTreeItem(QTreeWidgetItem):
    def __init__(self, version):
        super(VersionTreeItem, self).__init__()

        self.version = version

        self.setText(0, self.version.number)
        self.setText(1, self.version.name)


class VersionTree(QTreeWidget):
    def __init__(self):
        super(VersionTree, self).__init__()

        self.versions = []

        self.create_context_menu()

    def create_context_menu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.contextMenu = QMenu(self)
        self.openOutputPathAction = QAction('Open Path', self.contextMenu)
        self.renderQtAction = QAction('Render Qt', self.contextMenu)

        self.contextMenu.addAction(self.openOutputPathAction)
        self.contextMenu.addAction(self.renderQtAction)

        self.openOutputPathAction.triggered.connect(self.open_output_path)
        self.renderQtAction.triggered.connect(self.render_qt)
        self.customContextMenuRequested.connect(self.show_menu)

    def show_menu(self):
        self.contextMenu.move(QCursor.pos())
        self.contextMenu.show()

    def render_qt(self):
        import os
        cmd = 'render_qt -v {}'.format(self.selectedItems()[0].version.id)
        os.system(cmd)

    def open_output_path(self):
        path = self.selectedItems()[0].version.get_output_path()
        import webbrowser
        webbrowser.open(path)

    def set_versions(self, versions):
        self.versions = versions
        self.refresh()

    def refresh(self):
        versionDict = {}
        self.clear()

        for v in self.versions:
            if v.element not in versionDict:
                versionDict[v.element] = []
            versionDict[v.element].append(v)
        for element, versions in versionDict.items():
            elementItem = QTreeWidgetItem()
            elementItem.setText(0, element)
            self.addTopLevelItem(elementItem)
            for version in versions:
                versionItem = VersionTreeItem(version)
                elementItem.addChild(versionItem)

        self.expandAll()

