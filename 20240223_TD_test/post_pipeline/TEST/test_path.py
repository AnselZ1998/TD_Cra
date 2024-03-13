import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'post_pipeline.settings'
django.setup()
from pipeline_db.models import Task
'''task = Task.objects.get(id = 1)
print(task.get_work_path('maya'))
print(task.get_work_file('maya', 'bg', 'v001'))
print(task.get_target_version_path('bg', 'v55445'))'''

from pipeline_core.dcc.context import Context
f = f'C:/Ansel/TD_PyProject/TD/20240223_TD_test/CXS_1/asset/chr/assetCXS_1_0/mod/work/nuke/bg/assetCXS_1_0_bg_v001.nk'
Context.from_file('nuke', f)
print(Context.task.name, Context.project.name, Context.element, Context.number)
