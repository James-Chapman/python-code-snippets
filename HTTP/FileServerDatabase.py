# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#
# Copyright (C) James Chapman 2019
#

import sqlite3

class FileServerDatabase:

    _databaseFile = ":memory"
    _connection = None

    def __init__(self):
        self._databaseFile = "fileStore.db"
        self._connection = sqlite3.connect(self._databaseFile)
        cur = self._connection.cursor()
        cur.execute("ATTACH DATABASE '%s' AS 'FileStore';" % (self._databaseFile))

    def __del__(self):
        self._connection.close()

    def createDatabaseTables(self):
        cur = self._connection.cursor()
        cur.execute("""CREATE TABLE files(files_id INTEGER PRIMARY KEY AUTOINCREMENT, fileMD5_id INT, fileSHA1_id INT, fileDetails_id INT, fileContent_id INT);""")
        cur.execute("""CREATE TABLE fileMD5(fileMD5_id INTEGER PRIMARY KEY AUTOINCREMENT, files_id INT, fileMD5 TEXT);""")
        cur.execute("""CREATE TABLE fileSHA1(fileSHA1_id INTEGER PRIMARY KEY AUTOINCREMENT, files_id INT, fileSHA1 TEXT);""")
        cur.execute("""CREATE TABLE fileDetails(fileDetails_id INTEGER PRIMARY KEY AUTOINCREMENT, files_id INT, fileName TEXT, fileDescription TEXT, fileSize INT);""")
        cur.execute("""CREATE TABLE fileContent(fileContent_id INTEGER PRIMARY KEY AUTOINCREMENT, files_id INT, fileBlob BLOB);""")

    def deleteDatabaseTables(self):
        cur = self._connection.cursor()
        cur.execute("DROP TABLE files;")
        cur.execute("DROP TABLE fileMD5;")
        cur.execute("DROP TABLE fileSHA1;")
        cur.execute("DROP TABLE fileDetails;")
        cur.execute("DROP TABLE fileContent;")

    def getFileContentFromName(self, fileName):
        cur = self._connection.cursor()
        cur.execute("SELECT * FROM fileContent INNER JOIN files ON fileContent.files_id = files.files_id;")
        return cur

    def insertFile(self, fileName):
        f = open(fileName, "rb")
        data = f.read()
        f.close()
        cur = self._connection.cursor()
        cur.execute("INSERT INTO fileDetails (fileName) VALUES ('%s');" %(fileName))
        cur.execute("SELECT fileDetails_id FROM fileDetails;")
        details_id = cur.fetchone()
        print(details_id[0])
        cur.execute("INSERT INTO fileContent (fileBlob) VALUES (?)", (sqlite3.Binary(data),))
        cur.execute("SELECT fileContent_id FROM fileContent;")
        content_id = cur.fetchone()
        print(content_id[0])
        cur.execute("INSERT INTO files (fileDetails_id, fileContent_id) VALUES (%d, %d);" %(details_id[0], content_id[0]))
        return cur

    #def getDetailsFromFileName(self, fileName):
