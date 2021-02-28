import argparse
import json
import subprocess
import time

import serial

par = argparse.ArgumentParser()
par.add_argument('-p', '--port', type=str, default='/dev/ttyUSB0')
par.add_argument('-b', '--baud', type=int, default=9600)
par.add_argument('--timeout', type=int, default=5)
par.add_argument('--min-speed', type=int, default=80)
par.add_argument('--max-temp', type=int, default=65)
args = par.parse_args()

MIN_SPEED = int(args.min_speed)
MAX_SPEED = 255
MAX_TEMP = int(args.max_temp)


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


print(f'Maximum temperature when the fan will kick in: {MAX_TEMP}')
print(f'Minimum x/255 value of fan speed: {MIN_SPEED}')

with serial.Serial(args.port, args.baud, timeout=args.timeout) as fan:
    fan_speed = 0
    while True:
        if get_temp() > MAX_TEMP:
            if fan_speed < MIN_SPEED:
                fan_speed = MIN_SPEED
            if fan_speed < MAX_SPEED:
                fan_speed += 10
        else:
            fan_speed = 0

        print(f'Temperature: {get_temp()} C, speed: {fan_speed}/255')
        packet = bytearray()
        packet.append(fan_speed)  # This is where fan value goes
        fan.write(packet)
        res = fan.read()
        if res != b'1':
            print(f'Some error: {res}')

        time.sleep(15)
