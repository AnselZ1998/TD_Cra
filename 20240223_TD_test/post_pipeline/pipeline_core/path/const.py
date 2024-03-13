PROJECT_ROOT = 'C:/Ansel/TD_PyProject/TD/20240223_TD_test'

WORK_FILE_RULES = {
    'nuke':[
        '/{Project}/asset/{Asset__type}/{Asset}/{Task}/work/nuke/{Version__element}/{Asset}_{Version__element}_{Version__number}.nk',
        '/{Project}/shot/{Sequence}/{Shot}/{Task}/work/nuke/{Version__element}/{Shot}_{Version__element}_{Version__number}.nk',
    ],
    'maya': [
        '/{Project}/asset/{Asset__type}/{Asset}/{Task}/work/maya/scenes/{Asset}_{Task}_{Version__number}.ma',
        '/{Project}/shot/{Sequence}/{Shot}/{Task}/work/maya/scenes/{Shot}_{Task}_{Version__number}.ma',
    ],
    'houdini': [
        '/{Project}/asset/{Asset__type}/{Asset}/{Task}/work/houdini/{Asset}_{Task}_{Version__number}.hip',
        '/{Project}/shot/{Sequence}/{Shot}/{Task}/work/houdini/{Shot}_{Task}_{Version__number}.hip',
    ],
    'blender': [
        '/{Project}/asset/{Asset__type}/{Asset}/{Task}/work/blender/{Asset}_{Task}_{Version__number}.blend',
        '/{Project}/shot/{Sequence}/{Shot}/{Task}/work/blender/{Shot}_{Task}_{Version__number}.blend',
    ],

}

OUTPUT_FILE_RULES = [

    '/{Project}/asset/{Asset__type}/{Asset}/{Task}/output/{Version__element}/{Version__number}',
    '/{Project}/shot/{Sequence}/{Shot}/{Task}/output/{Version__element}/{Version__number}',

]