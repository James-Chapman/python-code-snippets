# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#
# Copyright (C) James Chapman 2019
#

import pytest
from FileTools import *
from parameterized import parameterized, parameterized_class

def test_extractPKCS7():
    data = extractPKCS7('Bitwarden-Installer-1.12.0.exe')
    print(data)


if __name__ == '__main__':
    pytest
