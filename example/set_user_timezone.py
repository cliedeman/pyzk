# -*- coding: utf-8 -*-
import os
import sys

CWD = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(CWD)
sys.path.append(ROOT_DIR)

from zk import ZK


conn = None
zk = ZK('192.168.2.201', port=4370)
try:
    conn = zk.connect()
    conn.set_user_timezone_set(uid=1, tz1=3, tz2=2, tz3=1)

    user_timezone = conn.get_user_timezone_set(uid=1)
    print("Flag  : %s" % user_timezone.flag)
    print("TZ 1 : %s" % user_timezone.tz1)
    print("TZ 2 : %s" % user_timezone.tz2)
    print("TZ 3 : %s" % user_timezone.tz3)

    conn.set_user_timezone_set(uid=1, tz1=1, tz2=2, tz3=3)

    user_timezone = conn.get_user_timezone_set(uid=1)
    print("Flag  : %s" % user_timezone.flag)
    print("TZ 1 : %s" % user_timezone.tz1)
    print("TZ 2 : %s" % user_timezone.tz2)
    print("TZ 3 : %s" % user_timezone.tz3)

    # Disable user timezones
    conn.set_user_timezone_set(uid=1, tzflag=False)

    user_timezone = conn.get_user_timezone_set(uid=1)
    print("Flag  : %s" % user_timezone.flag)
    print("TZ 1 : %s" % user_timezone.tz1)
    print("TZ 2 : %s" % user_timezone.tz2)
    print("TZ 3 : %s" % user_timezone.tz3)
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
