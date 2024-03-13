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
    description = models.CharField(null=False, max_length=16)
    type = models.CharField(max_length=16, null=False,
    choices=(('chr','Character'),('prp','Prop'), ('env', 'Environment'))
    )
    project = models.ForeignKey(to = Project, related_name = 'assets', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

class Sequence(models.Model):
    name = models.CharField(null=False, max_length=16)
    description = models.CharField(null=False, max_length=16)
    project = models.ForeignKey(to = Project, related_name = 'sequences', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

class Shot(models.Model):
    name = models.CharField(null=False, max_length=16)
    description = models.CharField(null=False, max_length=16)
    sequence = models.ForeignKey(to = Sequence, related_name = 'shots', on_delete=models.DO_NOTHING)
    project = models.ForeignKey(to = Project, related_name = 'shots', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(null=False, max_length=16)
    description = models.CharField(null=False, max_length=16)
    asset = models.ForeignKey(to=Asset, related_name='tasks', on_delete=models.DO_NOTHING, null=True)
    shot = models.ForeignKey(to=Shot, related_name='tasks', on_delete=models.DO_NOTHING, null=True)
    project = models.ForeignKey(to=Project, related_name='tasks', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    def get_context(self):
        context = {}
        context.update(
            {
                'Project':self.project.name,
                'Task':self.name
            }
        )
        if self.asset is not None:
            context.update(
                {
                    'Asset':self.asset.name,
                    'Asset__type': self.asset.type,
                }
            )
        elif self.shot is not None:
            context.update(
                {
                    'Shot':self.shot.name,
                    'Sequence':self.shot.sequence.name

                }
            )
        return context

    def get_work_rule(self, dcc):
        from pipeline_core.path.core import get_work_file_rule
        workFileRules = get_work_file_rule(dcc)
        if self.asset is not None:
            workFileRules = workFileRules[0]
        elif self.shot is not None:
            workFileRules = workFileRules[1]
        else:
            return
        return workFileRules

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

    def get_work_file(self, dcc, element, number):
        from pipeline_core.path.const import PROJECT_ROOT
        context = self.get_context()
        workFileRule = self.get_work_rule(dcc)
        context.update({
            'Version__element': element,
            'Version__number': number,
        })
        path = workFileRule.format(**context)
        path = PROJECT_ROOT + path
        return path

    def get_target_version_path(self, element, number):
        from pipeline_core.path.const import PROJECT_ROOT
        context = self.get_context()
        outputRule = self.get_output_rule()
        context.update({
            'Version__element': element,
            'Version__number': number,
        })
        path = outputRule.format(**context)
        path = PROJECT_ROOT + path
        return path
    def create_version(self, element, number):
        version = Version.objects.create(
            project=self.project,
            task=self,
            element=element,
            number=number,
            name='{}-{}'.format(element, number)
        )
        return version

    def get_version(self, element, number):
        query = Version.objects.filter(
            task__id__exact=self.id,
            element__exact=element,
            number__exact=number
        )
        try:
            version = query[0]
        except:
            return
        return version

    def get_or_create_version(self, element, number):
        version = self.get_version(element, number)
        if version is None:
            version = self.create_version(element, number)
        return version
class Version(models.Model):
    name = models.CharField(null=False, max_length=16)
    element = models.CharField(null=False, max_length=16)
    number = models.CharField(null=False, max_length=16)
    description = models.CharField(null=False, max_length=16)
    task = models.ForeignKey(to=Task, related_name='versions', on_delete=models.DO_NOTHING)
    project = models.ForeignKey(to=Project, related_name='versions', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name