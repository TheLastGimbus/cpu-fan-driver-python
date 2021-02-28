import argparse
import json
import subprocess
import time
import traceback

import serial

par = argparse.ArgumentParser()
par.add_argument('-p', '--port', default='/dev/ttyUSB0')
par.add_argument('-b', '--baud', default=9600)
par.add_argument('--timeout', default=5)
par.add_argument('--min-speed', default=60)
par.add_argument('--max-temp', default=70)
args = par.parse_args()

MAX_VALUE = 255


# This is customisable per machine
def get_temp():
    s = subprocess.run('sensors -j'.split(), capture_output=True)
    out = json.loads(s.stdout)
    out = out['coretemp-isa-0000']
    temp = 0
    for core_key in list(out)[1:]:
        core = out[core_key]
        temp = max(temp, core[list(core)[0]])
    return temp


def main():
    with serial.Serial(args.port, args.baud, timeout=args.timeout) as fan:
        while True:
            fan_speed = args.min_speed
            while get_temp() > args.max_temp:
                if fan_speed < MAX_VALUE:
                    fan_speed += 5
                    print(f'New speed: {fan_speed}')
                packet = bytearray()
                packet.append(fan_speed)  # This is where fan value goes
                fan.write(packet)
                res = fan.read()
                if res != b'1':
                    print(f'Some error: {res}')
                time.sleep(5)

            time.sleep(5)


while True:
    try:
        main()
    except Exception as e:
        if e is KeyboardInterrupt:
            exit(0)
        traceback.print_exc()
        time.sleep(5)
