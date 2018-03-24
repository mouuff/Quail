
import os
import shutil
from abc import ABC, abstractmethod
from .. import builder


class SolutionBase(ABC, builder.BuilderAction):
    ''' The goal of this interface is to be able to resolve solution files
    comming from anywhere.
    current goals are:
    - from builtin data (added with pyinstaller)
    - from local directory
    - over network
    '''
    def __init__(self):
        self._hook = None

    def set_hook(hook):
        '''set progression hook'''
        self._hook = hook

    def _update_progress(self, percent):
        ''' This function will be called to update solution progression
        while downloading.
        It will call
        '''
        if self._hook:
            self._hook(percent)
        print(str(percent) + '%')

    @abstractmethod
    def local(self):
        '''returns True if solution is stored locally,
        and if there is any corruption, it will not try again
        '''
        pass

    @abstractmethod
    def open(self):
        '''Open solution if needed
        (planned for unzipping, connecting to network, etc)
        return False if failed to open
        '''
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def walk(self):
        '''Iter files
        returns iterator,
        iter file solution relative path
        same output as os.walk
        '''
        pass

    @abstractmethod
    def retrieve_file(self, relpath):
        ''' Retrieve file from solution and returns file path'''
        pass
