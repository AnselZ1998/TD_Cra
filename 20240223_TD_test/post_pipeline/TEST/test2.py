from pipeline_core.path.const import WORK_FILE_RULES, OUTPUT_FILE_RULES
from pipeline_core.path.core import match_path, convert_to_pattern

path = '/proj/asset/chr/assetA/mod/work/nuke/bgg/assetA_bgg_V001.nk'
pattern = WORK_FILE_RULES['nuke'][0]
print(match_path(path, pattern))