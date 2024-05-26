import csv
import argparse

parser = argparse.ArgumentParser(description='Update ZK Users.')
parser.add_argument('ip', type=str, help='device ip address')
parser.add_argument('--port', type=int, help='device port', default=4370, required=False)
parser.add_argument('--password', type=int, help='device password', default=0, required=False)
parser.add_argument('--dry-run', help='Do not make updates', default=True,
                    required=False, action='store_true')

args = parser.parse_args()

from zk import ZK

conn = None

zk = ZK(args.ip, port=args.port, timeout=5, password=args.password, ommit_ping=False)
try:
    from struct import pack, unpack
    pack('H', 1)
    conn = zk.connect()
    conn.disable_device()

    serialNumber = conn.get_serialnumber()
    print(f"Connected. Serial Number: {serialNumber}.")

    users = conn.get_users()
    usersByUid = {user.uid: user for user in users}
    timezoneByUid = dict()

    for user in users:
        timezoneByUid[user.uid] = conn.get_user_timezone_set(user.uid)

    print('Fetching Data Complete')

    with open(F"export.csv", mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader, None)  # skip the headers

        # Uid,SerialNumber,OldDeviceUserId,NewDeviceUserId,DeviceName,WorkforceName,MatchQuality
        for row in reader:
            [uidString, rowSerialNumber, oldUserId, newUserId, deviceName, workforceName, match] = row
            uid = int(uidString)

            if serialNumber == rowSerialNumber:
                print(f"Processing Uid: {uid}, Username: {workforceName}")

                user = usersByUid[uid]

                if not user:
                    print('User not found')
                    continue

                if user.user_id == newUserId:
                    print('User already updated')
                elif user.user_id == oldUserId:
                    if args.dry_run:
                        print(f'Dry Run. UserId {user.user_id} -> {newUserId}')
                    else:
                        # conn.set_user(user.uid, user.name, user.privilege, user.password, user.group_id, newUserId, user.card)
                        # tz = timezoneByUid[user.uid]
                        # conn.set_user_timezone_set(tz.flag, tz.tz1, tz.tz2, tz.tz3)
                        print('User Updated')
                else:
                    print(F'Unexpected User ID. Expected: {oldUserId}, Actual: {user.user_id}')

    conn.enable_device()
except Exception as e:
    print("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()