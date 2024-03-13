import time

from pipeline_core.util.qt_wrap import *
from pipeline_core.ui.file_tree import *
from pipeline_core.ui.version_tree import *
from pipeline_core.dcc.context import Context
from pipeline_core.dcc.wrap import DccWrap

from pipeline_core.path.util import version_up


#这个类是一个设置文本的，传入具体字符串
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


class TESTUI(QWidget):
    def __init__(self):
        super(TESTUI, self).__init__()
        #启动UI
        self.initui()
        #连接也启动
        self.create_connect()
        #刷新一下project
        self.refresh_projects()
        self.refresh_info()

    def initui(self):
        self.setObjectName('test_ui')

        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)


        #inforLayout
        self.infoLayout = QHBoxLayout()
        #当前的信息
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

        #定义上层和下层
        self.upLayout = QHBoxLayout()
        self.downLayout = QHBoxLayout()

        #定义几个ListWeidge
        self.projectList = QListWidget()
        self.assetTypeList = QListWidget()
        self.assetList = QListWidget()
        self.sequenceList = QListWidget()
        self.shotList = QListWidget()
        self.taskList = QListWidget()

        #加上一个转换页
        self.switchTab1 = QTabWidget()

        #加一个box，水平放入
        self.assetBox = QWidget()
        self.assetLayout = QHBoxLayout()
        self.assetLayout.addWidget(self.assetTypeList)
        self.assetLayout.addWidget(self.assetList)
        self.assetBox.setLayout(self.assetLayout)

        #同理shotbox
        self.shotBox = QWidget()
        self.shotLayout = QHBoxLayout()
        self.shotLayout.addWidget(self.sequenceList)
        self.shotLayout.addWidget(self.shotList)
        self.shotBox.setLayout(self.shotLayout)

        #把他俩放入swichtap中
        self.switchTab1.addTab(self.assetBox, 'asset')
        self.switchTab1.addTab(self.shotBox, 'shot')

        #第二个页面
        self.switchTab2 = QTabWidget()
        #导入filetree

        self.workFileTree = FileTree()
        #放一些按钮
        #保存按钮
        self.saveButton = QPushButton('Save')
        #saveas菜单
        self.saveAsButton = QToolButton()
        self.saveAsMenu = QMenu(self.saveAsButton)
        self.saveAsButton.setMenu(self.saveAsMenu)
        #当按钮被点击时，菜单会显示出来。按钮本身还会显示一个小箭头来表示存在一个菜单。设置一个方式
        self.saveAsButton.setPopupMode(QToolButton.InstantPopup)
        self.openButton = QPushButton('Open')
        self.workButtonLayout = QHBoxLayout()
        self.workButtonLayout.addWidget(self.saveButton)
        self.workButtonLayout.addWidget(self.saveAsButton)
        self.workButtonLayout.addWidget(self.openButton)
        #把work区域做好了
        self.workBox = QWidget()
        self.workLayout = QVBoxLayout()
        self.workBox.setLayout(self.workLayout)
        self.workLayout.addWidget(self.workFileTree)
        self.workLayout.addLayout(self.workButtonLayout)

        #底下的都做好了
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




        #显示上层
        self.upLayout.addWidget(self.projectList)
        self.upLayout.addWidget(self.switchTab1)
        #显示下层
        self.downLayout.addWidget(self.taskList)
        self.downLayout.addWidget(self.switchTab2)

        #全部加到里面
        self.masterLayout.addLayout(self.infoLayout)
        self.masterLayout.addLayout(self.upLayout)
        self.masterLayout.addLayout(self.downLayout)
    #连接方法
    def create_connect(self):
        #project动
        self.projectList.itemSelectionChanged.connect(self.project_changed)
        self.assetTypeList.itemSelectionChanged.connect(self.assettype_changed)
        self.assetList.itemSelectionChanged.connect(self.asset_changed)
        self.sequenceList.itemSelectionChanged.connect(self.sequence_changed)
        self.shotList.itemSelectionChanged.connect(self.shot_changed)
        self.taskList.itemSelectionChanged.connect(self.task_changed)
        '''self.versionTree.itemSelectionChanged.connect(self.version_changed)

        self.saveButton.clicked.connect(self.save_clicked)
        self.openButton.clicked.connect(self.open_clicked)
        self.loadButton.clicked.connect(self.load_clicked)'''




    #TASKchange
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
    #saveas，然后拉去所有的element，然后可以添加new

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



    #所有的镜头会更新task
    def shot_changed(self):
        if len(self.shotList.selectedItems()) == 0:
            return
        selected = self.shotList.selectedItems()[0]
        #shot地下说有的task
        self.taskList.clear()
        for t in selected.entity.tasks.all():
            item = EntityListItem(t)
            self.taskList.addItem(item)


    #改变场次
    def sequence_changed(self):
        if len(self.sequenceList.selectedItems()) == 0:
            return
        selected = self.sequenceList.selectedItems()[0]
        #请调镜头的列表
        self.shotList.clear()
        #加入当前场次的列表
        for t in selected.entity.shots.all():
            item = EntityListItem(t)
            self.shotList.addItem(item)


    #改变资产
    def asset_changed(self):
        if len(self.assetList.selectedItems()) == 0:
            return
        selected = self.assetList.selectedItems()[0]

        self.taskList.clear()
        for t in selected.entity.tasks.all():
            item = EntityListItem(t)
            self.taskList.addItem(item)


    def assettype_changed(self):
        if len(self.assetTypeList.selectedItems()) == 0:
            return
        selected = self.assetTypeList.selectedItems()[0]
        #把后面的assetlist清掉
        self.assetList.clear()

        type = selected.type
        project = selected.project
        assets = project.assets.filter(type__exact=type)
        for a in assets:
            item = EntityListItem(a)
            self.assetList.addItem(item)

    def project_changed(self):

        if len(self.projectList.selectedItems()) == 0:
            return
        #找到选择的第一个
        selected = self.projectList.selectedItems()[0]
        #列表的每一项都是一个entity对象
        project = selected.entity
        #清除资产和资产类型
        self.assetTypeList.clear()
        self.assetList.clear()
        #获取所有资产
        assets = project.assets.all()
        #创建一个资产类型列表
        assettypes = []
        for a in assets:
            if a.type not in assettypes:
                assettypes.append(a.type)
        #加到列表里
        for type in assettypes:
            item = AssetTypeItem(type, project)
            self.assetTypeList.addItem(item)
        #同理，加上场次和镜头
        self.sequenceList.clear()
        self.shotList.clear()
        for seq in project.sequences.all():
            item = EntityListItem(seq)
            self.sequenceList.addItem(item)



        #启动时刷新一下project列表
    def refresh_projects(self):
        #从models里面导入Project
        from pipeline_db.models import Project
        #清一下project列表
        self.projectList.clear()
        #获得所有的project列表
        projects = Project.objects.all()
        for project in projects:
            #project对象传到了En里面了
            #en就是一个专门settext的封包
            item = EntityListItem(project)
            #设置完文本加到列表里
            self.projectList.addItem(item)


    def refresh_info(self, *args, **kwargs):
        print('refresh info')
        #获取任务
        task = Context.task
        if task is None:
            return
        #如果不为空，，设置项目名称
        self.projectLabel.setText(task.project.name)
        #如果资产不为空，设置镜头不可见，并设置名称
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


        #还没有点击
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


if __name__ =='__main__':
    import sys
    from pipeline_db.set import setup
    app = QApplication(sys.argv)
    test = TESTUI()
    test.show()
    sys.exit(app.exec_())