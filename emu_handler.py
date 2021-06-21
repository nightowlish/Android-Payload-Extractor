import os
import time
import logging
import subprocess

import config
import exceptions


class EmuHandler:
    def __init__(self, system_image, apk_path, apk_data, logger=None):
        self.system_image = system_image
        self.apk_path = apk_path
        self.apk_data = apk_data
        self.logger = logger if logger else logging
    
        temp, self.api, self.tag, self.abi = self.system_image.split(';')
        self.api = self.api.split('-')[1]
        self.name = 'emu_{}_{}_{}_{}'.format(self.api, self.tag, self.abi, int(time.time()))

    def handle_installation(self):
        try:
            self.create_avd()
            self.start_avd()
            self.install_apk()
        except Exception as e:
            raise exceptions.FailedInstallation(e)
        
    def create_avd(self):
        self.logger.info('Creating AVD...')
        command = config.AVDMANAGER_CREATE.format(config.AVDMANAGER, self.name, self.system_image, self.tag, self.abi, config.DEVICE_TYPE, config.AVDMANAGER_LOG)
        self.logger.debug('Will create AVD with the following parameters: {}'.format(command))
        os.system(command)
        if not self.emulator_exists(self.name):
            raise exceptions.FailedAVDCreation(self.name)

    def start_avd(self):
        self.logger.info('Starting AVD...')
        proc = subprocess.Popen([config.EMULATOR, '@{}'.format(self.name)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(config.EMULATOR_INIT_TIMEOUT)
        command = config.ADB_CHECK_BOOT_COMPLETED.format(config.ADB, config.DEVICE_NAME, config.ADB_LOG)
        while True:
            os.system(command)
            try:
                with open(config.ADB_LOG, 'r') as f:
                    output = f.read().strip()
                    if output == 'stopped':
                        break
                    time.sleep(config.EMULATOR_TIMEOUT)
            except Exception as e:
                raise exceptions.MalformedLog(e)
        time.sleep(config.EMULATOR_FINAL_TIMEOUT)
        
    def list_avds(self):
        os.system(config.EMULATOR_LIST)

    def emulator_exists(self, name):
        self.list_avds()
        try:
            with open(config.EMULATOR_LOG, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == name:
                        return True
                return False        
        except Exception as e:
            raise exceptions.MalformedLog(e)
        

    def install_apk(self):
        self.logger.info('Installing APK {} on AVD {}...'.format(self.apk_path, self.name))
        command = config.ADB_INSTALL.format(config.ADB, config.DEVICE_NAME, self.apk_path, config.ADB_LOG)
        self.logger.debug('Installing APK with the following parameters: {}'.format(command))
        os.system(command)        

    def delete_avd(self):
        self.logger.info('Deleting AVD...')
        command = config.AVDAMANGER_DELETE.format(config.AVDMANAGER, self.name, config.AVDMANAGER_LOG)
        self.logger.debug('Deleting AVD with the following parameters: {}'.format(command))
        os.system(command)
        if self.emulator_exists(self.name):
            self.logger.info('Failed to delete AVD.')
        
    def kill_avd(self):
        self.logger.info('Killing AVD...')
        command = config.ADB_KILL.format(config.ADB, config.DEVICE_NAME, config.ADB_LOG)
        self.logger.debug('Killing with parameters: {}'.format(command))
        os.system(command)
        time.sleep(config.KILL_TIMEOUT)
