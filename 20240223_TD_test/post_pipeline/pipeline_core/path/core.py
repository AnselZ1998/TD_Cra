# -*- coding: utf-8 -*-
import os
import re
from .const import WORK_FILE_RULES, OUTPUT_FILE_RULES


def get_work_file_rule(dcc):
    return WORK_FILE_RULES.get(dcc)


def get_output_path_rule():
    return OUTPUT_FILE_RULES


def convert_to_pattern(pathRule):
    valueList = []
    patternList = []

    for c in pathRule.split('/'):
        patternStr = c.replace('.', '\.')
        valueItem = re.findall(r'(?<={).*?(?=})', c)
        if len(valueItem) > 0:
            for item in valueItem:
                if item not in valueList:
                    valueList.append(item)
                exist = False
                for i in patternList:
                    if i.find('(?P<%s>.*)' % item) != -1:
                        exist = True
                        pass

                if exist:
                    patternStr = patternStr.replace('{%s}' % item, '(?P=%s)' % item)
                else:
                    patternStr = patternStr.replace('{%s}' % item, '(?P<%s>.*)' % item)
        else:
            pass

        patternList.append(patternStr)

    return valueList, patternList


def match_path(path, pathRule):
    valueList, patternList = convert_to_pattern(pathRule)

    pathList = path.split('/')
    patternListNum = len(patternList)

    allMatch = True
    matchDict = {}
    for value in valueList:
        matchDict[value] = None
    for i in range(patternListNum):
        patternStr = '/'.join(patternList[:i+1]) + '$'
        pathStr = '/'.join(pathList[:i+1])
        match = re.match(patternStr, pathStr)
        if match:
            matchDict.update(match.groupdict())
        else:
            allMatch = False
            pass

    return {
        'allMatch': allMatch,
        'matchDict': matchDict
    }



