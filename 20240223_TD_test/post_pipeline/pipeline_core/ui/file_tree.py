# -*- coding: utf-8 -*-


import os
from pipeline_core.util.qt_wrap import *
from pipeline_core.path.file import get_dirs, get_detail_of_path, get_sequences


class FileTreeItem(QTreeWidgetItem):
    def __init__(self, detailDict, parent=None):
        super(FileTreeItem, self).__init__(parent)

        self.name = detailDict["name"]
        self.type = detailDict["type"]
        self.filePath = detailDict["file path"]
        self.is_seq = detailDict.get("is_sequence")
        self.frame_range = detailDict.get("frame range")
        self.isFile = not self.type == 'folder'

        self.setText(0, self.name)
        self.setText(1, self.type)

        if self.is_seq:
            self.setText(0, self.name + " " + self.frame_range)
            self.setText(1, self.type + " sequence")

    def get_file_path(self, add_frame=False):
        if add_frame and self.frame_range is not None:
            return self.filePath + ' ' + self.frame_range
        else:
            return self.filePath


class FileTree(QTreeWidget):
    def __init__(
            self,
            *args, **kwargs
    ):
        super(FileTree, self).__init__(*args, **kwargs)

        self.root_path = None

        self.setHeaderLabels(["name", "type"])
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setSortingEnabled(True)
        self.sortByColumn(3, Qt.DescendingOrder)
        self.setColumnWidth(0, 200)
        self.setAnimated(True)
        self.setRootIsDecorated(False)

    def set_dir(self, dir_path):
        self.root_path = dir_path
        self.refresh_tree()

    def refresh_tree(self):
        self.clear()
        if os.path.isdir(self.root_path):
            self.add_folder(self.root_path, parent_item=self)
            self.expandAll()

    def add_folder(self, path, parent_item):
        allFiles = []
        allFileDetail = []

        for i in get_dirs(path):
            allFiles.append(get_detail_of_path(i))

        for i in get_sequences(path):
            allFileDetail.append(get_detail_of_path(i))

        for detail in allFileDetail:
            allFiles.append(detail)

        for detail in allFiles:
            self.add_item(detail, parent_item)

    def add_item(self, detail, parent_item):
        type = detail['type']
        fileItem = FileTreeItem(detail)
        if parent_item is self:
            self.addTopLevelItem(fileItem)
        else:
            parent_item.addChild(fileItem)

        if type == 'folder':
            self.add_folder(detail['file path'], parent_item=fileItem)


def main():
    import sys
    from pipeline_core.util.const import PIPELINE_CODE_ROOT
    app = QApplication(sys.argv)
    w = FileTree()
    w.set_dir(PIPELINE_CODE_ROOT)

    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

