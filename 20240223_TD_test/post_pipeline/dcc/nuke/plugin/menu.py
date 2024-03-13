# -*- coding: utf-8 -*-

import nuke
import nukescripts
import pipeline_core
from pipeline_core.ui.project_manager import ProjectManager


def register_project_manager():
    return nukescripts.panels.registerWidgetAsPanel(
        'ProjectManager',
        'ProjectManager',
        'ProjectManager',
        True
    )


def add_to_panel():
    if nuke.getPaneFor('ProjectManager'):
        pass
    else:
        pane = nuke.getPaneFor('Properties.1')
        projectPanel = register_project_manager()
        projectPanel.addToPane(pane)


add_to_panel()




tool_menu = nuke.menu('Nuke').addMenu('Pipeline')
tool_menu.addCommand('ProjectManager', add_to_panel, '')

