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
        cur.execute("""SELECT `name` FROM `sqlite_master` WHERE type='table';""")
        tables = cur.fetchall()
        for t in tables:
            print(t)
        cur.execute("""CREATE TABLE `files`(
        `files_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
        `fileMD5_id` INTEGER, 
        `fileSHA1_id` INTEGER, 
        `fileDetails_id` INTEGER, 
        `fileContent_id` INTEGER
        );""")
        cur.execute("""CREATE TABLE `fileMD5`(
        `fileMD5_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
        `files_id` INTEGER, 
        `fileMD5` TEXT UNIQUE
        );""")
        cur.execute("""CREATE TABLE `fileSHA1`(
        `fileSHA1_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
        `files_id` INTEGER, 
        `fileSHA1` TEXT UNIQUE
        );""")
        cur.execute("""CREATE TABLE `fileDetails`(
        `fileDetails_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
        `files_id` INTEGER, 
        `fileName` TEXT, 
        `fileDescription` TEXT, 
        `fileSize` INTEGER
        );""")
        cur.execute("""CREATE TABLE `fileContent`(
        `fileContent_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
        `files_id` INTEGER, 
        `fileBlob` BLOB
        );""")
        self._connection.commit()

    def deleteDatabaseTables(self):
        cur = self._connection.cursor()
        cur.execute("DROP TABLE files;")
        cur.execute("DROP TABLE fileMD5;")
        cur.execute("DROP TABLE fileSHA1;")
        cur.execute("DROP TABLE fileDetails;")
        cur.execute("DROP TABLE fileContent;")
        self._connection.commit()

    def getFileContentFromName(self, fileName):
        cur = self._connection.cursor()
        cur.execute("""SELECT fileBlob FROM files
INNER JOIN fileContent ON fileContent.files_id = files.files_id
INNER JOIN fileDetails on fileDetails.files_id = fileContent.files_id
WHERE fileName = '%s';""" %fileName)
        return cur.fetchall()

    def getFileMD5FromName(self, fileName):
        pass

    def getFileSHA1FromName(self, fileName):
        pass

    def insertFile(self, fileName):
        try:
            f = open(fileName, "rb")
            data = f.read()
            f.close()

            cur = self._connection.cursor()
            cur.execute("INSERT INTO fileDetails (fileName) VALUES ('%s');" %(fileName))
            cur.execute("SELECT fileDetails_id FROM fileDetails ORDER BY fileDetails_id desc;")
            details_id = cur.fetchone()
            self._connection.commit()

            cur.execute("INSERT INTO fileContent (fileBlob) VALUES (?)", (sqlite3.Binary(data),))
            cur.execute("SELECT fileContent_id FROM fileContent ORDER BY fileContent_id desc;")
            content_id = cur.fetchone()
            self._connection.commit()

            cur.execute("INSERT INTO files (fileDetails_id, fileContent_id) VALUES (%d, %d);" %(details_id[0], content_id[0]))
            cur.execute("SELECT files_id FROM files ORDER BY files_id desc;")
            files_id = cur.fetchone()
            self._connection.commit()

            sql1 = "UPDATE fileDetails SET files_id = '%d' WHERE fileDetails_id = '%d';" % (files_id[0], details_id[0])
            sql2 = "UPDATE fileContent SET files_id = '%d' WHERE fileContent_id = '%d';" % (files_id[0], content_id[0])
            for sql in [sql1, sql2]:
                cur.execute(sql)
            self._connection.commit()
            return True
        except Exception as e:
            print(e)
            return False

    #def getDetailsFromFileName(self, fileName):
