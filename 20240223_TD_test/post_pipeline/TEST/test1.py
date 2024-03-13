import os
import random
import django
os.environ["DJANGO_SETTINGS_MODULE"] = 'post_pipeline.settings'
django.setup()
from pipeline_db.models import *

project_name = ['CXS_1', 'CXS_2', 'CXS_3', 'CXS_4', 'CXS_5']
types = ['chr', 'prp', 'env']

for i in range(5):
    projectname = project_name[i]
    print(projectname)
    project = Project.objects.create(
        name = projectname,
        full_name = f'长相思_{i}'

    )
    for j in range(int(random.random() * 20) + 5):
        assertname = f'asset{projectname}_{j}'
        print(assertname)
        asset = Asset.objects.create(
            name = assertname,
            type = types[int(random.random() * 3)],
            project = project
        )
        #模型，贴图，绑定
        for t in ['mod', 'tex', 'rig']:
            task = Task.objects.create(
                name = t,
                asset = asset,
                project = project,
            )
    for j in range(int(random.random() * 10) + 2):
        seqname = f'seq_{projectname}_{j}'
        print(seqname)
        sequence = Sequence.objects.create(
            name = seqname,
            project = project,
        )

        for k in range(int(random.random() * 30) + 2):
            shotname = f'A002_b00{k}'
            print(shotname)
            shot = Shot.objects.create(
                name = shotname,
                sequence = sequence,
                project = project,
            )
            #动画，特效，灯光，合成
            for t in ['ani', 'efx', 'lgt', 'cmp']:
                task = Task.objects.create(
                    name=t,
                    shot = shot,
                    project=project,
                )