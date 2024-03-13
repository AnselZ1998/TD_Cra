# -*- coding: utf-8 -*-
import nuke
import os


def get_dcc_name():
    return 'nuke'


def is_in_gui():
    return nuke.env['gui']


def get_current_frame():
    return nuke.frame()


def get_frame_range():
    return nuke.root().knob("first_frame").value(), nuke.root().knob("first_frame").value()


def get_current_file():
    return nuke.root().knob("name").value()


def save_as(file):
    print("save as {}".format(file))
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))
    nuke.scriptSaveAs(file)


def save(file=None):
    if file is None:
        file = get_current_file()
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))
    nuke.scriptSave(file)


def open_script(file):
    print("open " + file)
    nuke.scriptOpen(file)


def get_selection():
    return nuke.selectedNodes()


def clear_selection():
    for n in nuke.selectedNodes():
        n.setSelected(False)


def get_node_name(node):
    return node.knob("name").value()


def add_knob(node, knob_type, name, label=None):
    if label is None:
        label = name
    knob = node.knob(name)
    if knob is None:
        knob = getattr(nuke, knob_type)(name, label)
        node.addKnob(knob)
    return knob


def refresh_all_writes_label():
    for node in nuke.allNodes("Write"):
        node["label"].setValue(node["label"].value())


def isGeoFilename(filename):
    filenameLower = filename.lower()
    _, ext = os.path.splitext(filenameLower)

    if ext in ['.fbx', '.obj', '.abc']:
        return True
    else:
        return False


def isAbcFilename(filename):
    filenameLower = filename.lower()
    _, ext = os.path.splitext(filenameLower)

    if ext in ['.abc']:
        return True
    else:
        return False


def isCameraFilename(filename):
    filenameLower = filename.lower()
    name, ext = os.path.splitext(filenameLower)

    if ext in ['.abc'] and filenameLower.find('cam') != -1:
        return True
    else:
        return False


def isDeepFilename(filename):
    filenameLower = filename.lower()
    _, ext = os.path.splitext(filenameLower)

    if ext in ['.dtex', '.dshd', '.deepshad']:
        return True
    else:
        return False


def isAudioFilename(filename):
    filenameLower = filename.lower()
    _, ext = os.path.splitext(filenameLower)

    if ext in ['.wav', '.wave', '.aif', '.aiff']:
        return True
    else:
        return False


def isNkFileName(filename):
    filenameLower = filename.lower()
    _, ext = os.path.splitext(filenameLower)
    if ext in [".nk"]:
        return True
    else:
        return False


def isSeqFile(filename):
    stripped = nuke.stripFrameRange(filename)
    if stripped == filename:
        return False
    else:
        return True


def load_file(f, version):
    from pipeline_core.path.sequence import is_sequence, get_sequences

    defaulttype = "Read"

    isAbc = False
    isNk = isNkFileName(f)
    isCam = False

    stripped = nuke.stripFrameRange(f)
    nodeType = defaulttype
    if isAudioFilename(stripped):
        nodeType = "AudioRead"
    if isGeoFilename(stripped):
        nodeType = "ReadGeo2"
    if isDeepFilename(stripped):
        nodeType = "DeepRead"
    if isCameraFilename(stripped):
        nodeType = 'Camera2'
        isCam = True

    if isAbc:
        nuke.createScenefileBrowser(f, "")
    elif isNk:
        nuke.nodePaste(f)
    else:
        try:
            node = nuke.createNode(nodeType, "file {" + f + "}", inpanel=False)
            if is_sequence(f):
                seq = get_sequences(f)[0]
                node['first'].setValue(seq['first_frame'])
                node['origfirst'].setValue(seq['first_frame'])
                node['last'].setValue(seq['last_frame'])
                node['origlast'].setValue(seq['last_frame'])
            if isCam:
                node.knob('read_from_file').setValue(True)

            if version.task.name == 'plate':
                ccversion = version.task.get_version('color', version.number)
                if ccversion is not None:
                    ccnode = nuke.createNode('OCIOCDLTransform')
                    ccnode.setInput(0, node)
                    ccnode.knob('read_from_file').setValue(True)
                    ccnode.knob('file').setValue(ccversion.get_file('origin'))

        except RuntimeError as err:
            nuke.message(err.args[0])


def add_on_script_save(func):
    nuke.addOnScriptSave(func)


def add_on_script_close(func):
    nuke.addOnScriptClose(func)


def add_on_script_load(func):
    nuke.addOnScriptLoad(func)

