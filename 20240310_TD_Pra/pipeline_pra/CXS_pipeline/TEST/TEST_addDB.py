
import os
import random
from CXS_pipeline.setup import setup
from CXS_db.models import *
project = ['CXS_1', 'CXS_2']
types = ['chr', 'prp', 'env']


for i,j in enumerate(project):
    print(j)
    project = Project.objects.create(
        name = str(j),
        full_name = f'长相思{i}'
    )

    for a in range(int(random.random() * 20) + 5):
        typename = random.randint(0, 2)
        name = f'{j}_{a}'
        print(name)
        assets = Asset.objects.create(
            name = name,
            type = types[typename],
            project = project
        )

        for t in ['mod', 'tex', 'rig']:
            print(t)
            task = Task.objects.create(
                name = t,
                asset = assets,
                project = project
            )
    for s in range(int(random.random() * 20) + 5):
        sequencename = f'seq_{j}_{s}'
        print(sequencename)
        sequence = Sequence.objects.create(
            name = sequencename,
            project = project,
        )

        for sh in range(int(random.random() * 30) + 2):
            shotname = f'A002_b00{sh}'
            print(shotname)
            shot = Shot.objects.create(
                name=shotname,
                sequence=sequence,
                project=project,
            )
            # 动画，特效，灯光，合成
            for t in ['ani', 'efx', 'lgt', 'cmp']:
                print(t)
                task = Task.objects.create(
                    name=t,
                    shot=shot,
                    project=project,
                )


