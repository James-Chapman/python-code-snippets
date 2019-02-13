# -*- coding: utf-8 -*-
#!/usr/bin/env python3

# TODO:
# File IO in python is pathetically slow, put the logic into a DLL, expose a C-call API and then wrap this
# class around that to have super fast FileIO in python.

class FileHandler:

    m_filePath = ""
    m_isOpenRead = False
    m_isOpenWrite = False
    m_fileHandle = None
    m_fileSize = 0

    def __init__(self, filepath, mode):
        self.m_filePath = filepath
        try:
            self.m_fileHandle = open(filepath, mode)
        except:
            return
        if ('r+' in mode) or ('w+' in mode):
            self.m_isOpenRead = True
            self.m_isOpenWrite = True
        if ('r' in mode):
            self.m_isOpenRead = True
        if ('w' in mode):
            self.m_isOpenRead = True
        self.m_fileHandle.seek(0, 2)
        self.m_fileSize = self.m_fileHandle.tell()
        self.m_fileHandle.seek(0, 0)

    def __del__(self):
        if (not self.m_isOpenRead) and (not self.m_isOpenWrite):
            return
        self.m_fileHandle.close()

    def readData(self, size=0):
        if (self.m_isOpenRead):
            if (size == 0):
                return self.m_fileHandle.read()
            else:
                return self.m_fileHandle.read(size)

    def getSize(self):
        return self.m_fileSize
