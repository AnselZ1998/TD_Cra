# -*- coding: utf-8 -*-

class Context(object):
    task = None
    asset = None
    shot = None
    project = None

    element = 'master'
    number = None

    @classmethod
    def get_field(cls, key):
        if key == 'Assset':
            return cls.asset.name
        if key == 'Shot':
            return cls.shot.name
        if key == 'Task':
            return cls.task.name
        if key == 'Version__element':
            return cls.element
        if key == 'Version__number':
            return cls.number
        if key == 'Entity':
            return cls.asset.name if cls.asset is not None else cls.shot.name

    @classmethod
    def set_task(cls, task):
        cls.task = task
        cls.asset = task.asset
        cls.shot = task.shot
        cls.project = task.project

    @classmethod
    def from_file(cls, dcc, file):
        from pipeline_core.path.core import get_work_file_rule, match_path
        from pipeline_core.path.const import PROJECT_ROOT
        from pipeline_db.models import Task

        file = file.replace(PROJECT_ROOT, '')

        workFilesRules = get_work_file_rule(dcc)
        for index, pathRule in enumerate(workFilesRules):
            matchResult = match_path(file, pathRule)
            if matchResult['allMatch']:
                matchDict = matchResult['matchDict']
                if index == 0:
                    task = Task.objects.filter(
                        name__exact=matchDict['Task'],
                        asset__name__exact=matchDict['Asset'],
                        asset__type__exact=matchDict['Asset__type'],
                        project__name__exact=matchDict['Project'],
                    )[0]
                else:
                    task = Task.objects.filter(
                        name__exact=matchDict['Task'],
                        shot__name__exact=matchDict['Shot'],
                        shot__sequence__name__exact=matchDict['Sequence'],
                        project__name__exact=matchDict['Project'],
                    )[0]
                cls.set_task(task)
                cls.element = matchDict.get('Version__element', 'master')
                cls.number = matchDict.get('Version__number')
                return

    @classmethod
    def init(cls):
        from .wrap import DccWrap
        print('init context')
        cls.from_file(DccWrap.get_dcc_name(), DccWrap.get_current_file())