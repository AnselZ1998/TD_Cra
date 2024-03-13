# -*- coding: utf-8 -*-


MAYA_EXTS = [
    '.mb',
    '.ma',
]

EXT_TYPE_MAP = {
    '.mb': 'mayaBinary',
    '.ma': 'mayaAscii',
    '.obj': 'OBJexport',
}
FILE_RULE_LIST = [
    ("fluidCache", "cache/nCache/fluid"),
    ("images", "images"),
    ("offlineEdit", "scenes/edits"),
    ("furShadowMap", "renderData/fur/furShadowMap"),
    ("iprImages", "renderData/iprImages"),
    ("scripts", "scripts"),
    ("renderData", "renderData"),
    ("fileCache", "cache/nCache"),
    ("eps", "data"),
    ("shaders", "renderData/shaders"),
    ("3dPaintTextures", "sourceimages/3dPaintTextures"),
    ("translatorData", "data"),
    ("mel", "scripts"),
    ("furFiles", "renderData/fur/furFiles"),
    ("OBJ", "data"),
    ("particles", "cache/particles"),
    ("scene", "scenes"),
    ("alembicCache", "cache/alembic"),
    ("sourceImages", "sourceimages"),
    ("furEqualMap", "renderData/fur/furEqualMap"),
    ("clips", "clips"),
    ("furImages", "renderData/fur/furImages"),
    ("depth", "renderData/depth"),
    ("sceneAssembly", "sceneAssembly"),
    ("teClipExports", "Time Editor/Clip Exports"),
    ("movie", "movies"),
    ("audio", "sound"),
    ("bifrostCache", "cache/bifrost"),
    ("autoSave", "autosave"),
    ("mayaAscii", "scenes"),
    ("move", "data"),
    ("sound", "sound"),
    ("diskCache", "data"),
    ("illustrator", "data"),
    ("mayaBinary", "scenes"),
    ("templates", "assets"),
    ("furAttrMap", "renderData/fur/furAttrMap"),
    ("timeEditor", "Time Editor"),
]
