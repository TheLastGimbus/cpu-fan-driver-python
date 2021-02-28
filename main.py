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
args = par.parse_args()


# This is customisable per machine
def get_temp():
    s = subprocess.run('sensors -j'.split(), capture_output=True)
    out = json.loads(s.stdout)
    out = out['coretemp-isa-0000']
    temp = 0
    for core_key in list(out)[1:]:
        core = out[core_key]
        print(core)
        temp = max(temp, core[list(core)])
    return temp


def main():
    with serial.Serial(args.port, args.baud, timeout=args.timeout) as fan:
        while True:
            print(f'Temp: {get_temp()}')
            packet = bytearray()
            packet.append(10)  # This is where fan value goes
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
