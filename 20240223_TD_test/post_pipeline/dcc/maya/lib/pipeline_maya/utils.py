# -*- coding: utf-8 -*-


import pymel.core as pm
from maya import cmds, mel, utils, OpenMaya
import subprocess
import os
from .const import *


def get_dcc_name():
    return 'maya'


def is_in_gui():
    isMayaInBatchMode = OpenMaya.MGlobal.mayaState() == OpenMaya.MGlobal.kBatch
    return not isMayaInBatchMode


def get_current_file():
    currentFile = cmds.file(q=True, sn=True)
    return currentFile


def set_workspace(mayafile):
    project_path = os.path.dirname(os.path.dirname(os.path.dirname(mayafile)))
    cmds.workspace(create=project_path)
    cmds.workspace(directory=project_path)
    cmds.workspace(project_path, openWorkspace=True)
    for i in FILE_RULE_LIST:
        cmds.workspace(fileRule=list(i))
    cmds.workspace(saveWorkspace=True)
    return project_path


def get_maya_type(filepath):
    # ma/mb
    ext = os.path.splitext(filepath)[-1]
    filetype = EXT_TYPE_MAP.get(ext)
    return filetype


def get_current_frame():
    return cmds.currentTime(q=True)


def get_frame_range():
    startF = cmds.playbackOptions(query=True, minTime=True)
    endF = cmds.playbackOptions(query=True, maxTime=True)
    return [startF, endF]


def set_current_frame(frame):
    cmds.currentTime(frame)


def save_as(filepath):
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    cmds.file(rename=filepath)
    cmds.file(save=True, type=get_maya_type(filepath))


def save():
    filepath = get_current_file()
    if filepath != '':
        cmds.file(save=True, type=get_maya_type(filepath))


def open_script(filepath):
    cmds.file(
        filepath,
        open=True,
        force=True,
        options='v=0;p=17;f=0',
        ignoreVersion=1,
        type=get_maya_type(filepath)
    )


def create_tab(
        dock_name,
        widget,
        label='WidgetLabel',
        dockTab='Channel Box / Layer Editor'
):
    cmds.workspaceControl(dock_name, uiScript='', label=label)
    cmds.control(str(widget.objectName()), e=True, p=dock_name)
    tab_result = mel.eval('getUIComponentDockControl("{}", false)'.format(dockTab))
    cmds.workspaceControl(dock_name, e=True, tabToControl=(tab_result, -1))


def node_exist(nodeName):
    return pm.objExists(nodeName)


def get_pynode(nodeName):
    try:
        return pm.PyNode(nodeName)
    except:
        return None


def create_node(path):
    current = path
    if not node_exist(current):
        parent = '|'.join(current.split('|')[:-1])
        if parent == '':
            cmds.createNode('transform', n=current.split('|')[-1])
        else:
            create_node(parent)
            cmds.createNode('transform', n=current.split('|')[-1], p=parent)


# add shelf button
def get_pipeline_shelf_tab():
    topLevelShelf = pm.melGlobals['gShelfTopLevel']
    mainShelf = pm.ui.PyUI(topLevelShelf)

    shelfName = 'Pipeline'
    shelfTabName = '{}|{}'.format(mainShelf, shelfName)
    if not pm.shelfLayout(shelfTabName, q=True, exists=True):
        pm.shelfLayout(shelfName, parent=mainShelf)

    shelfTabLayout = pm.ui.ShelfLayout(shelfTabName)
    return shelfTabLayout


def clear_pipeline_shelf():
    shelfTabLayout = get_pipeline_shelf_tab()
    children = shelfTabLayout.getChildArray() or list()
    for child in children:
        pm.deleteUI(child, control=True)


def add_shelf_button(
        name='',
        label='',
        command='',
):
    shelfTabLayout = get_pipeline_shelf_tab()

    options = {}
    options['enable'] = True
    options['flat'] = True
    options['font'] = 'plainLabelFont'
    options['rpt'] = True
    options['w'] = 35
    options['h'] = 35
    options['mw'] = 1
    options['mh'] = 1
    options['olc'] = [0.8, 0.8, 0.8]
    options['olb'] = [0, 0, 0, 0.2]

    options['annotation'] = label
    options['sourceType'] = 'python'
    options['command'] = command
    options['imageOverlayLabel'] = label

    options['image'] = 'commandButton.png'

    btn = pm.shelfButton(
        parent=shelfTabLayout,
        docTag=name,
        label=label,
        **options
    )

    return btn


# import
def reference_file(file, namespace='', parent=None):
    file_path = cmds.file(
        file,
        r=True,
        ignoreVersion=True,
        mergeNamespacesOnClash=False,
        ns=namespace
    )

    ref_node = cmds.referenceQuery(file_path, rfn=True)
    ref_ns = cmds.referenceQuery(file_path, ns=True)

    # if none, delete
    nodes = cmds.referenceQuery(ref_node, nodes=True)
    if nodes is None:
        cmds.file(rr=True, referenceNode=ref_node)
    else:
        node = nodes[0]
        if parent is not None:
            create_node(parent)
            cmds.parent(node, parent)

    return ref_node, node


def load_file(file, version):
    asset = version.task.asset
    assettype = asset.type

    importPath = '|master|{}'.format(assettype)
    namespace = asset.name

    reference_file(file, namespace=namespace, parent=importPath)


# export

def export_abc(
        exportPath='',
        exportRoot='',
        frameRange=None,
):
    job_flags = '-uvWrite -root {} -file {}'.format(exportRoot, exportPath)
    if frameRange is not None:
        job_flags += ' -frameRange {} {}'.format(frameRange[0], frameRange[1])
    job_flags += ' -ro'
    cmds.AbcExport(j=job_flags)


def export(
        exportPath,
        exportSelected=False,
        exportRoot='',
        options=None
):
    print('export:', exportPath, exportRoot)
    exportExt = os.path.splitext(exportPath)[-1]
    if not os.path.exists(os.path.dirname(exportPath)):
        os.makedirs(os.path.dirname(exportPath))

    if not exportRoot.startswith('|'):
        exportRoot = '|' + exportRoot

    if not exportSelected:
        cmds.select(exportRoot)

    if exportExt == '.abc':
        if options is None:
            options = {}
        frameRange = options.get('frameRange')
        export_abc(
            exportPath,
            exportRoot,
            frameRange=frameRange
        )

    else:
        # obj, mb, fbx
        optionsStr = ''
        if options is None:  # default options
            if exportExt == '.mb':
                optionsStr = 'v=0;'
            elif exportExt == '.obj':
                optionsStr = ''
            elif exportExt == '.fbx':
                optionsStr = ''
        else:
            if 'frameRange' in options:
                frameRange = options['frameRange']
                optionsStr += 'animation=1;'
                optionsStr += 'startTime={};'.format(frameRange[0])
                optionsStr += 'endTime={};'.format(frameRange[1])

        if exportExt == '.mb':
            exportTyp = 'mayaBinary'
        elif exportExt == '.obj':
            exportTyp = 'OBJexport'
        elif exportExt == '.fbx':
            exportTyp = 'FBX Export'

        cmds.file(
            exportPath,
            pr=True,
            es=True,
            force=True,
            options=optionsStr,
            typ=exportTyp
        )


def playblast(
        filename='',
        startFrame=1,
        endFrame=1,
        format='image',
        size=None
):
    """
    :param filename: str
    :param startFrame: int
    :param endFrame: int
    :param format: qt, image
    :param size: list
    :return:
    """

    options = {}
    options['filename'] = filename
    options['startTime'] = startFrame
    options['endTime'] = endFrame
    options['format'] = format
    options['viewer'] = False
    options['framePadding'] = 4
    options['forceOverwrite'] = True
    options['quality'] = 100
    if size is not None:
        options['percent'] = 100
        options['widthHeight'] = size

    imageFormat = cmds.getAttr('defaultRenderGlobals.imageFormat')
    if format == 'image':
        # set format to jpg
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)
        finalFile = filename + '.####.jpg'
    else:
        finalFile = filename + '.mov'

    try:
        cmds.playblast(**options)
    except:
        print('playblast failed', format, filename)
    finally:
        cmds.setAttr('defaultRenderGlobals.imageFormat', imageFormat)

    return finalFile


# callbacks
def add_callback(msg, func):
    OpenMaya.MSceneMessage.addCallback(msg, func)


def add_on_script_load(func):
    add_callback(OpenMaya.MSceneMessage.kAfterOpen, func)


def add_on_script_save(func):
    add_callback(OpenMaya.MSceneMessage.kAfterSave, func)


def add_on_script_close(func):
    pass


