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
    _cursor = None

    def __init__(self):
        self._databaseFile = "fileStore.db"
        self._connection = sqlite3.connect(self._databaseFile)
        c = self._connection.cursor()
        c.execute("ATTACH DATABASE '%s' AS 'FileStore';" % (self._databaseFile))
        self._connection.commit()

    def __del__(self):
        self._connection.close()

    def _createFilesTable(self):
        c = self._connection.cursor()
        try:
            c.execute("SELECT name FROM sqlite_sequence WHERE type = 'table' AND name = 'files';")
        except:
            c.execute("""CREATE TABLE `files`(
                        `files_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                        `fileMD5_id` INTEGER,
                        `fileSHA1_id` INTEGER,
                        `fileDetails_id` INTEGER,
                        `fileContent_id` INTEGER
                        );""")
        self._connection.commit()

    def _createFileMD5Table(self):
        c = self._connection.cursor()
        try:
            c.execute("""SELECT name FROM sqlite_sequence WHERE type = 'table' AND name = 'fileMD5';""")
        except:
            c.execute("""CREATE TABLE `fileMD5`(
                        `fileMD5_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                        `files_id` INTEGER,
                        `MD5Hash` TEXT UNIQUE
                        );""")
        self._connection.commit()

    def _createFileSHA1Table(self):
        c = self._connection.cursor()
        try:
            c.execute("""SELECT name FROM sqlite_sequence WHERE type = 'table' AND name = 'fileSHA1';""")
        except:
            c.execute("""CREATE TABLE `fileSHA1`(
                `fileSHA1_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                `files_id` INTEGER,
                `SHA1Hash` TEXT UNIQUE
                );""")
        self._connection.commit()

    def _createFileDetailsTable(self):
        c = self._connection.cursor()
        try:
            c.execute("""SELECT name FROM sqlite_sequence WHERE type = 'table' AND name = 'fileDetails';""")
        except:
            c.execute("""CREATE TABLE `fileDetails`(
                `fileDetails_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                `files_id` INTEGER,
                `fileName` TEXT,
                `fileDescription` TEXT,
                `fileSize` INTEGER
                );""")
        self._connection.commit()

    def _createFileContentTable(self):
        c = self._connection.cursor()
        try:
            c.execute("""SELECT name FROM sqlite_sequence WHERE type = 'table' AND name = 'fileContent';""")
        except:
            c.execute("""CREATE TABLE `fileContent`(
                `fileContent_id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                `files_id` INTEGER,
                `fileBlob` BLOB
                );""")
        self._connection.commit()

    def createDatabaseTables(self):
        self._createFilesTable()
        self._createFileMD5Table()
        self._createFileSHA1Table()
        self._createFileContentTable()
        self._createFileDetailsTable()

    def deleteDatabaseTables(self):
        c = self._connection.cursor()
        c.execute("DROP TABLE files;")
        c.execute("DROP TABLE fileMD5;")
        c.execute("DROP TABLE fileSHA1;")
        c.execute("DROP TABLE fileDetails;")
        c.execute("DROP TABLE fileContent;")
        self._connection.commit()

    def getFileContentFromName(self, fileName):
        c = self._connection.cursor()
        c.execute("""SELECT fileBlob FROM files
                    INNER JOIN fileContent ON fileContent.files_id = files.files_id
                    INNER JOIN fileDetails ON fileDetails.files_id = fileContent.files_id
                    WHERE fileName = :fileName;""", {"fileName": fileName})
        return c.fetchall()

    def getFileMD5FromName(self, fileName):
        c = self._connection.cursor()
        c.execute("""SELECT MD5Hash FROM files
                    INNER JOIN fileContent ON fileContent.files_id = files.files_id
                    INNER JOIN fileDetails ON fileDetails.files_id = fileContent.files_id
                    INNER JOIN fileMD5 on fileMD5.files_id = fileDetails.files_id
                    WHERE fileName = :fileName;""", {"fileName": fileName})
        return c.fetchall()

    def getFileSHA1FromName(self, fileName):
        c = self._connection.cursor()
        c.execute("""SELECT SHA1Hash FROM files
                    INNER JOIN fileContent ON fileContent.files_id = files.files_id
                    INNER JOIN fileDetails ON fileDetails.files_id = fileContent.files_id
                    INNER JOIN fileSHA1 on fileSHA1.files_id = fileDetails.files_id
                    WHERE fileName = :fileName;""", {"fileName": fileName})
        return c.fetchall()

    def insertFile(self, fileName):
        try:
            f = open(fileName, "rb")
            data = f.read()
            f.close()

            c = self._connection.cursor()

            c.execute("INSERT INTO fileDetails (fileName) VALUES (:name);", {"name": fileName})
            c.execute("SELECT fileDetails_id FROM fileDetails ORDER BY fileDetails_id desc;")
            details_id = c.fetchone()

            c.execute("INSERT INTO fileContent (fileBlob) VALUES (:data)", (sqlite3.Binary(data),))
            c.execute("SELECT fileContent_id FROM fileContent ORDER BY fileContent_id desc;")
            content_id = c.fetchone()

            c.execute("INSERT INTO files (fileDetails_id, fileContent_id) VALUES (:details_id, :content);", {"details_id": details_id[0], "content": content_id[0]})
            c.execute("SELECT files_id FROM files ORDER BY files_id desc;")
            files_id = c.fetchone()

            c.execute("UPDATE fileDetails SET files_id = :files_id WHERE fileDetails_id = :fileDetails_id;", {"files_id": files_id[0], "fileDetails_id": details_id[0]})
            c.execute("UPDATE fileContent SET files_id = :files_id WHERE fileContent_id = :fileContent_id;", {"files_id": files_id[0], "fileContent_id": content_id[0]})

            md5sum = generateMd5Hash(data)
            c.execute("INSERT INTO fileMD5 (files_id, MD5Hash) VALUES (:files_id, :md5);", {"files_id": files_id[0], "md5": md5sum})
            c.execute("SELECT fileMD5_id FROM fileMD5 ORDER BY fileMD5_id desc;")
            md5_id = c.fetchone()

            sha1sum = generateSha1Hash(data)
            c.execute("INSERT INTO fileSHA1 (files_id, SHA1Hash) VALUES (:files_id, :sha1);", {"files_id": files_id[0], "sha1": sha1sum})
            c.execute("SELECT fileSHA1_id FROM fileSHA1 ORDER BY fileSHA1_id desc;")
            sha1_id = c.fetchone()

            c.execute("UPDATE files SET fileMD5_id = :md5 WHERE files_id = :files_id;", {"md5": md5_id[0], "files_id": files_id[0]})
            c.execute("UPDATE files SET fileSHA1_id = :sha1 WHERE files_id = :files_id;", {"sha1": sha1_id[0], "files_id": files_id[0]})

            self._connection.commit()

            return True
        except sqlite3.IntegrityError as integerr:
            print("File already in DB")
            self._connection.rollback()
            return True
        except Exception as e:
            print(str(e))
            self._connection.rollback()
            raise(e)
    #def getDetailsFromFileName(self, fileName):
