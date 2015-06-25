"""
This is yet another Alarm test
"""

from common.test import BaseTest

class AlarmTempTest(BaseTest):
    """Simple alarm temp test
    """

    ID = "T3"
    REQS = []

class XTest(BaseTest):
    """Simple  test
    """

    ID = "T6"
    REQS = ["R1.4", "R3"]
