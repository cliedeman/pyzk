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
    user_timezone = conn.get_user_timezone_set(uid=1)
    print ("UID  : %s" % user_timezone.uid)
    print ("TZ 1 : %s"% user_timezone.tz1)
    print ("TZ 2 : %s"% user_timezone.tz2)
    print ("TZ 3 : %s"% user_timezone.tz3)
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
