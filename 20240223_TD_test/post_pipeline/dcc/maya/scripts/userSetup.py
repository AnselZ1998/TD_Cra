# -*- coding: utf-8 -*-

import pymel.core as pm


def init():
    pm.general.evalDeferred('from pipeline_maya_boot import *')


if __name__ == "__main__":
    init()
