from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(null=False, max_length=16)
    full_name = models.CharField(null=False, max_length=16)
    description = models.CharField(null=False, max_length=16)

    def __str__(self):
        return self.name


class Asset(models.Model):
    name = models.CharField(null=False, max_length=16)
    decription = models.CharField(null=False, max_length=16)
    type = models.CharField(null=False, max_length=16,
    choices=(('chr', 'Character'), ('prp', 'prop'), ('env', 'Environment')
             ))
    project = models.ForeignKey(to = Project, related_name='assets', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Sequence(models.Model):
    name = models.CharField(null=False, max_length=16)
    description = models.CharField(null=False, max_length=16)
    project = models.ForeignKey(to=Project, related_name='sequences', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

class Shot(models.Model):
    name = models.CharField(null=False, max_length=16)
    description = models.CharField(null=False, max_length=16)
    project = models.ForeignKey(to=Project, related_name='shots', on_delete=models.DO_NOTHING)
    sequence = models.ForeignKey(to=Sequence, related_name='shots', on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(null=False, max_length=16)
    description = models.CharField(null=False, max_length=16)
    project = models.ForeignKey(to=Project, related_name='tasks', on_delete=models.DO_NOTHING)
    shot = models.ForeignKey(to=Shot, related_name='tasks', on_delete=models.DO_NOTHING, null=True)
    asset = models.ForeignKey(to=Asset, related_name='tasks', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name

    def get_context(self):
        context = {}
        context.update(
            {
                'Project':self.project,
                'Task':self.name,
            }
        )
        if self.asset is not None:
            context.update({
                'Asset':self.asset.name,
                'Asset__type':self.asset.type,
            })
        elif self.shot is not None:
            context.update({
                'Shot':self.shot.name,
                'Sequence':self.shot.sequence,
            })
        else:
            return
        return context

    def get_work_rule(self, dcc):
        from pipeline_core.path.core import get_work_file_name
        workFileRules = get_work_file_name(dcc)
        if self.asset is not None:
            workFileRule = workFileRules[0]
        elif self.shot is not None:
            workFileRule = workFileRules[1]
        else:
            return
        return workFileRule

    def get_output_rule(self):
        from pipeline_core.path.core import get_output_path_rule
        rules = get_output_path_rule()
        if self.asset is not None:
            rule = rules[0]
        elif self.shot is not None:
            rule = rules[1]
        else:
            return
        return rule

    def get_work_path(self, dcc):
        from pipeline_core.path.const import PROJECT_ROOT
        context = self.get_context()
        workFileRule = self.get_work_rule(dcc)
        if dcc == 'maya':
            workFileRule = '/'.join(workFileRule.split('/')[:9])
        else:
            workFileRule = '/'.join(workFileRule.split('/')[:8])
        path = workFileRule.format(**context)
        path = PROJECT_ROOT + path
        return path

    def get_work_file(self, dcc,element, number):
        from pipeline_core.path.const import PROJECT_ROOT
        context = self.get_context()
        context.update({
            'Version__element':element,
            'Version__number':number
        })
        workFileRule = self.get_work_rule(dcc)
        path = workFileRule.format(**context)
        path = PROJECT_ROOT + path
        return path

    def get_taeget_version_path(self,element, number):
        from pipeline_core.path.const import PROJECT_ROOT
        context = self.get_context()
        context.update({
            'Version__element':element,
            'Version__number':number
        })
        outputRule = self.get_output_rule()
        path = outputRule.format(**context)
        path = PROJECT_ROOT + path
        return path




class Version(models.Model):
    name = models.CharField(null=False, max_length=16)
    number = models.CharField(null=False, max_length=16)
    element = models.CharField(null=False, max_length=16)
    description = models.CharField(null=False, max_length=16)
    project = models.ForeignKey(to=Project, related_name='versions', on_delete=models.DO_NOTHING)
    task = models.ForeignKey(to=Task, related_name='versions', on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name



