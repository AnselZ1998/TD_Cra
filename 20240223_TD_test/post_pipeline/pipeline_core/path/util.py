# -*- coding: utf-8 -*-
import re


def version_up(ver):
    if ver is None:
        return 'v001'
    match = re.match(r"\D*(?P<num>\d+)\D*", ver)
    if match:
        lastVerNum = match.groupdict()["num"]
        verNumLenth = len(lastVerNum)
        format = "%0"+"%sd" % verNumLenth
        newVerNum = format % (int(lastVerNum) + 1)
        return ver.replace(lastVerNum, newVerNum)
    else:
        return "v001"
