#! -*- coding: UTF-8 -*-
import threading


def singleton(clazz, *args, **kwargs):
    __instances = dict()
    lock = threading.Lock()

    def get_instance():
        try:
            lock.acquire()
            if clazz not in __instances:
                __instances[clazz] = clazz(*args, **kwargs)
        finally:
            lock.release()
        return __instances[clazz]

    return get_instance