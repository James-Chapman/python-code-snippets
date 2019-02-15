# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#
# Copyright (C) James Chapman 2019
#

import pytest
from FileServerDatabase import FileServerDatabase
from parameterized import parameterized, parameterized_class

db = FileServerDatabase()

@pytest.mark.incremental
class Test_FileServerDatabase(object):

    @pytest.mark.skip(reason="I want to manually inspect the DB")
    def test_createDatabaseTables(self):
        db.createDatabaseTables()
        assert (1)

    def test_insertFile(self):
        assert(db.insertFile('Bitwarden-Installer-1.12.0.exe'))

    def test_getFileContentFromName(self):
        rows = db.getFileContentFromName('Bitwarden-Installer-1.12.0.exe')
        assert(rows)

    def test_getFileMD5FromName(self):
        rows = db.getFileMD5FromName('Bitwarden-Installer-1.12.0.exe')
        print("MD5: %s" % str(rows[0][0]))
        assert (rows)

    def test_getFileSHA1FromName(self):
        rows = db.getFileSHA1FromName('Bitwarden-Installer-1.12.0.exe')
        print("SHA1: %s" % str(rows[0][0]))
        assert (rows)

    @pytest.mark.skip(reason="I want to manually inspect the DB")
    def test_deleteDatabaseTables(self):
        db.deleteDatabaseTables()
        assert (1)


pytest.main()
