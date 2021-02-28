import argparse
import time
import traceback

import serial
from pyspectator.processor import Cpu

par = argparse.ArgumentParser()
par.add_argument('-p', '--port', default='/dev/ttyUSB0')
par.add_argument('-b', '--baud', default=9600)
par.add_argument('--timeout', default=5)
args = par.parse_args()


def main():
    cpu = Cpu(monitoring_latency=1)
    with serial.Serial(args.port, args.baud, timeout=args.timeout) as fan, cpu:
        while True:
            print(f'Temp: {cpu.temperature}')
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
