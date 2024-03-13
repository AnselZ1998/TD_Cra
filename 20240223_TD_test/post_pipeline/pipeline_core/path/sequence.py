# -*- coding: utf-8 -*-


import os
import re


SEQ_PATTERN = re.compile(r'(?P<prefix>^.+[._])(?P<frame>#+|%\d*d|\$F\d*)(?P<suffix>[._].+$)')
SEQ_PATTERN_WITH_DIGIT = re.compile(r'(?P<prefix>^.+[._])(?P<frame>#+|%\d*d|\$F\d*|\d+)(?P<suffix>[._].+$)')


def get_frame_glob(path):
    match = SEQ_PATTERN.match(path)
    if match:
        return match.group('frame')


def replace_frame_glob(path, frame=1, frame_glob=None):
    if frame_glob is None:
        frame_glob = get_frame_glob(path)
    if '#' in frame_glob and isinstance(frame, int):
        length = len(frame_glob)
        frameP = '%0' + str(length) + 'd'
        frame = frameP % frame
    return path.replace(frame_glob, str(frame))


def sequence_equal(file1, file2):
    match1 = SEQ_PATTERN.match(os.path.basename(file1))
    match2 = SEQ_PATTERN.match(os.path.basename(file2))

    if match1 and match2:
        temp1 = file1.replace(match1.group('frame'), '')
        temp2 = file2.replace(match2.group('frame'), '')
        return temp1 == temp2
    else:
        return file1 == file2


def is_sequence(path):
    result = SEQ_PATTERN.match(os.path.basename(path))
    if result:
        return True
    return False


def get_sequences(path, only_sequence=False):
    """
    :return:
        'filename': '../sequence.####.exr',
        'files': ['../sequence.0001.exr', '../sequence.0002.exr', ...],
        'first_frame': '0001',
        'last_frame': '0003',
        'frame_length': 3,
        'frames': ['0001', '0002', ...],
        'non_digit_part': '../sequence..exr',
        'is_sequence': True
    """

    IMAGES = [
        "tif", "tiff",
        "jpg", "jpeg",
        "bmp",
        "png", "tga",
        "tx", "tex", "rat", "hdr",
        "exr", "dpx",
        "pic", "vdb", "bgeo", "bgeo.sc"
    ]

    def get_sequence_groups(_files=[], only_sequence=True):
        reg = re.compile(r'(?P<base>^.+[._])(?P<frame_num>\d+)(?P<ext>[._].+$)')
        _files.sort()
        seq_groups = []

        for _f in _files:
            _basename = os.path.basename(_f)
            _ext = _basename.split('.')[-1].lower()
            _dirname = os.path.dirname(_f)
            _result = reg.search(_basename)
            if not _result or _ext not in IMAGES:
                if not only_sequence:
                    grp_data = {
                        'filename': _f,
                        'is_sequence': False,
                        'non_digit_part': _f,
                        'frame_length': 0,
                        'first_frame': 0,
                        'last_frame': 0,
                        'frames': [],
                        'files': [_f],
                        'has_padding': False
                    }
                    seq_groups.append(grp_data)
                    continue
                else:
                    continue

            base = _result.group('base')
            ext = _result.group('ext')
            frame_num = _result.group('frame_num')
            frame_length = len(frame_num)
            non_digit_part = os.path.join(_dirname, base + ext).replace("\\", "/")

            find_seq_grp = False
            for seq_group in seq_groups:
                if non_digit_part == seq_group['non_digit_part']:
                    if frame_length != seq_group['frame_length']:
                        seq_group['has_padding'] = False

                    seq_group['files'].append(_f)
                    seq_group['frame_length'] = frame_length
                    seq_group['frames'].append(frame_num)
                    find_seq_grp = True

            if not find_seq_grp:
                grp_data = {
                    'filename': os.path.join(_dirname, base + '#' * frame_length + ext).replace("\\", "/"),
                    'is_sequence': True,
                    'non_digit_part': non_digit_part,
                    'frame_length': frame_length,
                    'frames': [frame_num],
                    'files': [_f],
                    'has_padding': True
                }
                seq_groups.append(grp_data)

        for grp in seq_groups:
            if not grp.get('frames', 0):
                continue

            grp['first_frame'] = int(min(grp['frames'], key=int))
            grp['last_frame'] = int(max(grp['frames'], key=int))

        for seq in seq_groups:
            if 'files' in seq and len(seq['files']) == 1:
                seq['is_sequence'] = False
                seq['filename'] = seq['files'][0]

        return seq_groups

    files = []
    if isinstance(path, list):
        return get_sequence_groups(path, only_sequence)

    elif os.path.isdir(path):
        for f in os.listdir(path):
            f = os.path.join(path, f).replace("\\", "/")

            if os.path.isfile(f):
                files.append(f)

        return get_sequence_groups(files, only_sequence)

    basename = os.path.basename(path)
    dirname = os.path.dirname(path)
    result = SEQ_PATTERN_WITH_DIGIT.match(basename)
    if result:
        matched_files = []
        pattern = '({prefix})(\d+)({suffix})'.format(prefix=result.group('prefix'), suffix=result.group('suffix'))
        pattern = re.compile(pattern)
        for f in os.listdir(dirname):
            if re.match(pattern, f):
                matched_files.append(os.path.join(dirname, f).replace("\\", "/"))
        matched_files.sort()
        return get_sequence_groups(matched_files, only_sequence)
    else:
        return get_sequence_groups([path], only_sequence)

