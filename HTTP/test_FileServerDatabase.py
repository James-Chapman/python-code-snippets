# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#
# Copyright (C) James Chapman 2019
#

import threading
import pytest
from FileServerDatabase import FileServerDatabase
from parameterized import parameterized, parameterized_class

db = FileServerDatabase()


@pytest.mark.incremental
class Test_FileServerDatabase(object):

    #@pytest.mark.skip(reason="I want to manually inspect the DB")
    def test_createDatabaseTables(self):
        db.createDatabaseTables()
        assert (1)

    def test_insert(self):
        assert(db.insertFile('Bitwarden-Installer-1.12.0.exe'))

    def test_read(self):
        rows = db.getFileContentFromName('Bitwarden-Installer-1.12.0.exe')
        print("test_read")
        for r in rows:
            print(r)
        assert(1)

    #@pytest.mark.skip(reason="I want to manually inspect the DB")
    def test_deleteDatabaseTables(self):
        db.deleteDatabaseTables()
        assert (1)
