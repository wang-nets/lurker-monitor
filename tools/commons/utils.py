#! -*- coding: utf-8 -*-
import importlib

DOT_CHAR = '.'


class ModuleLoader(object):

    @staticmethod
    def load_module(module_path=None):
        if module_path is not None:
            last_index = module_path.rindex(DOT_CHAR)
            pkg_name = module_path[0: last_index]
            package = importlib.import_module(pkg_name)
            clazz = getattr(package, module_path[last_index+1:])
        return clazz

    @staticmethod
    def load_modules(module_paths=[]):
        module_objs = []
        for module_path in module_paths:
            module_objs.append(ModuleLoader.load_module(module_path))
        return module_objs