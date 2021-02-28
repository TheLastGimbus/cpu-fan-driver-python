import argparse
import json
import subprocess
import time
import traceback

import serial

par = argparse.ArgumentParser()
par.add_argument('-p', '--port', type=str, default='/dev/ttyUSB0')
par.add_argument('-b', '--baud', type=int, default=9600)
par.add_argument('--timeout', type=int, default=5)
par.add_argument('--min-speed', type=int, default=60)
par.add_argument('--max-temp', type=int, default=70)
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
        fan_speed = int(args.min_speed)
        while True:
            print(f'Temperature: {get_temp()}')
            if get_temp() > args.max_temp:
                if fan_speed < MAX_VALUE:
                    fan_speed += 5
                    print(f'New speed: {fan_speed}')
            else:
                fan_speed = int(args.min_speed)
            packet = bytearray()
            packet.append(fan_speed)  # This is where fan value goes
            fan.write(packet)
            res = fan.read()
            if res != b'1':
                print(f'Some error: {res}')

            time.sleep(5)


while True:
    try:
        main()
    except Exception as e:
        if e is KeyboardInterrupt:
            exit(0)
        traceback.print_exc()
        time.sleep(5)
