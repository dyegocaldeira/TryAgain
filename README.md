# TryAgain

Requirements:

`airodump-ng`
```bash
$ sudo apt install aircrack-ng -y
```
Python 3

### How to use

Run the **TryAgain** script.
```bash
$ git clone https://github.com/dyegocaldeira/TryAgain
$ cd TryAgain
$ chmod +x wifi.py
$ sudo python3 wifi.py -h
usage: wifi.py [-h] -i INTERFACE

Crack WiFi Vivo

required arguments:
  -i INTERFACE, --interface INTERFACE
                        Network interface that will be used as a monitor

```



### TODO

- [x] Create functional script.
- [x] Improve conditionals
- [x] Run `airodump-ng` on _script_;
