import argparse
import time
import traceback

import serial

par = argparse.ArgumentParser()
par.add_argument('-p', '--port', default='/dev/ttyUSB0')
par.add_argument('-b', '--baud', default=9600)
par.add_argument('--timeout', default=5)
args = par.parse_args()


def main():
    with serial.Serial(args.port, args.baud, timeout=args.timeout) as fan:
        while True:
            packet = bytearray()
            packet.append(10)  # This is where fan value goes
            fan.write(packet)
            res = fan.read()
            if res != b'1':
                print('Some error!')
            time.sleep(5)


while True:
    try:
        main()
    except Exception as e:
        if e is KeyboardInterrupt:
            exit(0)
        traceback.print_exc()
        time.sleep(5)
