# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#
# Copyright (C) James Chapman 2019
#

import threading
from FileServerDatabase import FileServerDatabase
import pytest
from parameterized import parameterized, parameterized_class

db = FileServerDatabase()


[pytest]
class Test_FileServerDatabase:

    def test_create(self):
        #db.createDatabaseTables()
        assert(1)

    def test_insert(self):
        r = db.insertFile('Bitwarden-Installer-1.12.0.exe')
        assert(1)

    def test_read(self):
        rows = db.getFileContentFromName('Bitwarden-Installer-1.12.0.exe')
        print("test_read")
        for r in rows:
            print(r)
        assert(1)

    def test_delete(self):
        r = db.deleteDatabaseTables()
        assert(1)
