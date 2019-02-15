# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#
# Copyright (C) James Chapman 2019
#

import sqlite3
from FileTools import *

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
        try:
            cur.execute("""SELECT name FROM sqlite_sequence WHERE type = 'table' AND name = 'files';""")
            cur.fetchall()
        except sqlite3.OperationalError:
            cur.execute("""CREATE TABLE `files`(
            `files_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
            `fileMD5_id` INTEGER, 
            `fileSHA1_id` INTEGER, 
            `fileDetails_id` INTEGER, 
            `fileContent_id` INTEGER
            );""")
        try:
            cur.execute("""SELECT name FROM sqlite_sequence WHERE type = 'table' AND name = 'fileMD5';""")
            cur.fetchall()
        except sqlite3.OperationalError:
            cur.execute("""CREATE TABLE `fileMD5`(
            `fileMD5_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
            `files_id` INTEGER, 
            `MD5Hash` TEXT UNIQUE
            );""")
        try:
            cur.execute("""SELECT name FROM sqlite_sequence WHERE type = 'table' AND name = 'fileSHA1';""")
            cur.fetchall()
        except sqlite3.OperationalError:
            cur.execute("""CREATE TABLE `fileSHA1`(
            `fileSHA1_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
            `files_id` INTEGER, 
            `SHA1Hash` TEXT UNIQUE
            );""")
        try:
            cur.execute("""SELECT name FROM sqlite_sequence WHERE type = 'table' AND name = 'fileDetails';""")
            cur.fetchall()
        except sqlite3.OperationalError:
            cur.execute("""CREATE TABLE `fileDetails`(
            `fileDetails_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
            `files_id` INTEGER, 
            `fileName` TEXT, 
            `fileDescription` TEXT, 
            `fileSize` INTEGER
            );""")
        try:
            cur.execute("""SELECT name FROM sqlite_sequence WHERE type = 'table' AND name = 'fileContent';""")
            cur.fetchall()
        except sqlite3.OperationalError:
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
                    INNER JOIN fileDetails ON fileDetails.files_id = fileContent.files_id
                    WHERE fileName = '%s';""" %fileName)
        return cur.fetchall()

    def getFileMD5FromName(self, fileName):
        cur = self._connection.cursor()
        cur.execute("""SELECT MD5Hash FROM files
                    INNER JOIN fileContent ON fileContent.files_id = files.files_id
                    INNER JOIN fileDetails ON fileDetails.files_id = fileContent.files_id
                    INNER JOIN fileMD5 on fileMD5.files_id = fileDetails.files_id
                    WHERE fileName = '%s';""" % fileName)
        return cur.fetchall()

    def getFileSHA1FromName(self, fileName):
        cur = self._connection.cursor()
        cur.execute("""SELECT SHA1Hash FROM files
                    INNER JOIN fileContent ON fileContent.files_id = files.files_id
                    INNER JOIN fileDetails ON fileDetails.files_id = fileContent.files_id
                    INNER JOIN fileSHA1 on fileSHA1.files_id = fileDetails.files_id
                    WHERE fileName = '%s';""" % fileName)
        return cur.fetchall()

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

            md5sum = generateMd5Hash(data)
            cur.execute("INSERT INTO fileMD5 (files_id, MD5Hash) VALUES (?, ?);", (files_id[0], md5sum))
            cur.execute("SELECT fileMD5_id FROM fileMD5 ORDER BY fileMD5_id desc;")
            md5_id = cur.fetchone()
            self._connection.commit()

            sha1sum = generateSha1Hash(data)
            cur.execute("INSERT INTO fileSHA1 (files_id, SHA1Hash) VALUES (?, ?);", (files_id[0], sha1sum))
            cur.execute("SELECT fileSHA1_id FROM fileSHA1 ORDER BY fileSHA1_id desc;")
            sha1_id = cur.fetchone()
            self._connection.commit()

            sql1 = "UPDATE files SET fileMD5_id = '%d' WHERE files_id = '%d';" % (md5_id[0], files_id[0])
            sql2 = "UPDATE files SET fileSHA1_id = '%d' WHERE files_id = '%d';" % (sha1_id[0], files_id[0])
            for sql in [sql1, sql2]:
                cur.execute(sql)
            self._connection.commit()

            return True
        except Exception as e:
            print(e)
            return False

    #def getDetailsFromFileName(self, fileName):
