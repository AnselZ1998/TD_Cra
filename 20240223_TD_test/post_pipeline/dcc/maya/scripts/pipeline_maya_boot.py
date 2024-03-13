# -*- coding: utf-8 -*-

from maya import OpenMaya, mel, cmds
import pymel.core as pm
import pipeline_maya.utils as utils
from pipeline_db.set import setup
from pipeline_core.dcc.context import Context
from pipeline_core.ui.project_manager import ProjectManager


def init_env(*args, **kwargs):
    Context.init()
    utils.set_workspace(utils.get_current_file())


utils.add_on_script_load(init_env)
utils.add_on_script_save(init_env)


PIPELINE_MAYA_SHELFS = [
    {
        'name': 'playblast',
        'label': 'Playblast',
        'command': 'from pipeline_maya.export import show_playblast_ui; window = show_playblast_ui()',
    },
    {
        'name': 'export_mod',
        'label': 'Export Mod',
        'command': 'from pipeline_maya.export import show_export_mod_ui; window = show_export_mod_ui()',
    },
    {
        'name': 'export_ani',
        'label': 'Export Ani',
        'command': 'from pipeline_maya.export import show_export_ani_ui; window = show_export_ani_ui()',
    }
]


if OpenMaya.MGlobal.mayaState() == OpenMaya.MGlobal.kInteractive:
    # create shelf
    utils.clear_pipeline_shelf()
    for index, shelfDict in enumerate(PIPELINE_MAYA_SHELFS):
        utils.add_shelf_button(
            name=shelfDict.get('name', ''),
            label=shelfDict.get('label', ''),
            command=shelfDict.get('command', ''),
        )

    # create project manager tab
    mayaProjectManager = ProjectManager()
    utils.create_tab(
        'ProjectManagerDock',
        mayaProjectManager,
        label='Project Manager'
    )

