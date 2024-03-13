# -*- coding: utf-8 -*-
# __author__ = 'XingHuan'
# 2/22/2018

import os
from .sequence import is_sequence, get_sequences


def get_dirs(folder):
    dirs = []
    for f in os.listdir(u'%s' % folder):
        absPath = os.path.join(folder, f).replace("\\", "/")
        if os.path.isdir(absPath):
            dirs.append(absPath)
    return dirs


def get_files(folder):
    files = []
    for f in os.listdir(u'%s' % folder):
        absPath = os.path.join(folder, f).replace("\\", "/")
        if os.path.isfile(absPath):
            files.append(absPath)
    return files


def get_detail_of_path(path):
    if isinstance(path, dict):
        keys = list(path.keys())
        if "files" in keys and "filename" in keys and "is_sequence" in keys:
            filename = path["filename"]
            isSequence = path["is_sequence"]
            frameRange = "%s-%s" % (path["first_frame"], path["last_frame"]) if path["is_sequence"] else None
            name = os.path.basename(filename)
            ext = os.path.splitext(filename)[1]
            if len(ext.split('.')) > 1:
                type = os.path.splitext(filename)[1].split(".")[1]
            else:
                type = ''

            return {
                "name": name,
                "type": type,
                "file path": filename,
                "is_sequence": isSequence,
                "frame range": frameRange
            }
        else:
            return {
                "name": "unknow",
                "type": "unknow",
                "file path": "unknow"
            }
    else:
        if os.path.isdir(path):
            name = os.path.basename(path)
            return {
                "name": name,
                "type": "folder",
                "file path": path
            }
        elif is_sequence(path):
            data = get_sequences(path)[0]
            filename = data["filename"]
            name = os.path.basename(filename)
            type = os.path.splitext(filename)[1].split(".")[1]
            frameRange = "%s-%s" % (data["first_frame"], data["last_frame"]) if data["is_sequence"] else None
            return {
                "name": name,
                "type": "%s sequence" % type,
                "file path": path,
                "frame range": frameRange
            }
        else:
            name = os.path.basename(path)
            type = os.path.splitext(path)[1].split(".")[-1]
            return {
                "name": name,
                "type": type,
                "file path": path
            }

