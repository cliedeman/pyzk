import csv
import argparse

parser = argparse.ArgumentParser(description='Dump ZK Users.')
parser.add_argument('ip', type=str, help='device ip address')
parser.add_argument('--port', type=int, help='device port', default=4370, required=False)
parser.add_argument('--password', type=int, help='device password', default=0, required=False)
parser.add_argument('--include-attendance', help='Include attendance data', default=False,
                    required=False, action='store_true')

args = parser.parse_args()

from zk import ZK, const

conn = None

zk = ZK(args.ip, port=args.port, timeout=5, password=args.password, ommit_ping=False)
try:
    conn = zk.connect()
    conn.disable_device()

    serialNumber = conn.get_serialnumber()
    print(f"Connected. Serial Number: {serialNumber}.")
    users = conn.get_users()
    print(f"Users Retrieved.")

    timezones = dict()

    for user in users:
        tz = conn.get_user_timezone_set(user.uid)
        timezones[user.uid] = tz

    print(f"Timezones Retrieved.")

    attendances = []
    if args.include_attendance:
        attendances = conn.get_attendance()
        print(f"Attendances Retrieved.")

    # CSV file setup
    with open(F"{serialNumber}.users.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        # write the header
        headers = ['UID', 'Name', 'Privilege', 'Password', 'Group ID', 'User ID', 'User Card', 'User Timezones Enabled', 'Timezone 1', 'Timezone 2', 'Timezone 3']

        if args.include_attendance:
            headers.append('Last Attendance')

        writer.writerow(headers)

        # write user data to the CSV file
        for user in users:
            privilege = 'Admin' if user.privilege == const.USER_ADMIN else 'User'
            tz = timezones[user.uid]

            row = [user.uid, user.name, privilege, user.password, user.group_id, user.user_id, user.card, tz.flag, tz.tz1, tz.tz2, tz.tz3]

            if args.include_attendance:
                user_attendances = [x.timestamp for x in attendances if x.user_id == user.user_id]

                if len(user_attendances) > 0:
                    latest_timestamp = max(user_attendances)
                    row.append(latest_timestamp.isoformat())

            writer.writerow(row)

    conn.enable_device()
except Exception as e:
    print("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()