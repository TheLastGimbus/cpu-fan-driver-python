# Custom CPU fan driver
### *Python daemon code*

TL;DR my fan driver didn't work so I made a *custom Arduino board* connected to my fan (through mosfet transistor), that
communicates with a *custom script* through USB UART to set the speed of the fan

This is the python script that
1. Gets the temperature with `sensors` command because I can't do that any other way
2. Checks if it's above certain treshold
3. If it is, keeps slowly turning the fan faster and faster until it isn't

This should be run as systemd service, thus a [`cpu-fan-driver.service.template`](cpu-fan-driver.service.template) is here

It communicates with [The Arduino](https://github.com/TheLastGimbus/cpu-fan-driver-arduino) though USB UART, sending and receiving a single byte
