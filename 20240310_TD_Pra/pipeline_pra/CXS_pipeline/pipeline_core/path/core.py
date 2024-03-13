import os
import re
from .const import PROJECT_ROOT, WORK_FILE_RULES, OUTPUT_FILE_RULES


def get_work_file_name(dcc):
    return WORK_FILE_RULES.get(dcc)

def get_output_path_rule():
    return OUTPUT_FILE_RULES
def convert_to_pattern(path_Rule):
    valueList = []
    patternList = []

    for c in path_Rule.split('/'):
        patternStr = c.replace('.', '\.')
        citem = re.findall(r"(?<={).*?(?=})", c)
        if len(citem) > 0:
            for ci in citem:
                if ci not in valueList:
                    valueList.append(ci)



                exist = False
                for i in patternList:
                    if i.find('(?P<%s>.*)' % ci) != -1:
                        exist = True
                        pass
                if exist:
                    patternStr = patternStr.replace('{%s}' % ci, '(?P=%s)' % ci)
                else:
                    patternStr = patternStr.replace('{%s}' % ci, '(?P<%s>.*)' % ci)

        patternList.append(patternStr)
    return valueList, patternList



def match_path(path, pathRule):
    valueList, patternList = convert_to_pattern(pathRule)
    print(valueList, patternList)
    pathList = path.split('/')

    patternListNum = len(patternList)

    allMatch = True
    matchDict = {}
    for i in valueList:
        matchDict[i] = None

    for i in range(patternListNum):
        patternStr = '/'.join(patternList[:i+1]) + '$'
        pathStr = '/'.join(pathList[:i+1])
        match = re.match(patternStr, pathStr)
        if re.match(patternStr, pathStr):
            matchDict.update(match.groupdict())
        else:
            allMatch = False

    return {
        'allMatch':allMatch,
        'matchDict':matchDict
    }


