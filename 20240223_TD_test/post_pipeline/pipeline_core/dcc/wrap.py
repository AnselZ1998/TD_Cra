# -*- coding: utf-8 -*-

import importlib


def default_func(*args, **kwargs):
    return


def get_default_func(func_name):
    print('default func', func_name)
    return default_func


class DccWrap(object):
    dcc_wrap_module = None

    @classmethod
    def get_wrap_func(cls, func_name):
        if cls.dcc_wrap_module is not None:
            imported_module = importlib.import_module(cls.dcc_wrap_module)
            if hasattr(imported_module, func_name):
                func = getattr(imported_module, func_name)
            else:
                func = get_default_func(func_name)
        else:
            func = get_default_func(func_name)
        return func

    @classmethod
    def get_dcc_name(cls):
        func = cls.get_wrap_func('get_dcc_name')
        if func == default_func:
            return
        return func()

    @classmethod
    def is_in_gui(cls):
        func = cls.get_wrap_func('is_in_gui')
        if func == default_func:
            return False
        return func()

    @classmethod
    def get_current_file(cls):
        func = cls.get_wrap_func('get_current_file')
        return func()

    @classmethod
    def save(cls):
        func = cls.get_wrap_func('save')
        return func()

    @classmethod
    def save_as(cls, filepath):
        func = cls.get_wrap_func('save_as')
        return func(filepath)

    @classmethod
    def open_script(cls, filepath):
        func = cls.get_wrap_func('open_script')
        return func(filepath)

    @classmethod
    def get_current_frame(cls):
        func = cls.get_wrap_func('get_current_frame')
        return func()

    @classmethod
    def get_frame_range(cls):
        func = cls.get_wrap_func('get_frame_range')
        return func()

    @classmethod
    def load_file(cls, file, version):
        func = cls.get_wrap_func('load_file')
        return func(file, version)

    @classmethod
    def add_on_script_load(cls, on_script_load):
        func = cls.get_wrap_func('add_on_script_load')
        return func(on_script_load)

    @classmethod
    def add_on_script_save(cls, on_script_save):
        func = cls.get_wrap_func('add_on_script_save')
        return func(on_script_save)
