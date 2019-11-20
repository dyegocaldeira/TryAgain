# TryAgain

This script works in conjunction with `airodump-ng`.


### How to use

You must run `airodump-ng` to get all the surrounding networks.
```bash
$ airodump-ng -w {nameCsv} --output-format csv {interface}
```
Run the **TryAgain** script.
```bash
$ git clone https://github.com/dyegocaldeira/TryAgain
$ cd TryAgain
$ chmod +x wifi.py
$ python wifi.py
```
After the script has been executed, you will be prompted for the `.csv` file name generated in step 1.
```bash
$ python wifi.py
Run airodump-ng -w \{name\} --output-format csv {interface}
to get all the surrounding networks .csv
Archive .csv Airodump-ng: networks.csv
```
After informing the `.csv` file the script will present the networks and its supposed passwords.


### TODO

- [x] Create functional script.
- [ ] Improve conditionals
- [ ] Accept `.csv` file as argument or run `airodump-ng` on _script_;
