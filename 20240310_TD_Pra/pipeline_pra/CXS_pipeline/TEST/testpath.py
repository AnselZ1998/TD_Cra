from CXS_pipeline.setup import setup
from CXS_db.models import Task

task = Task.objects.get(id=1)
print(task.get_work_path('maya'))
print(task.get_work_file('nuke','bg','v001'))
print(task.get_taeget_version_path('bg', 'v001'))