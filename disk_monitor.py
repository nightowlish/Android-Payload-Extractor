import os
import time
import shutil
import hashlib
import logging
import subprocess

import config
import exceptions
import validity_checker


class DiskMonitor:
    def __init__(self, package_name, launcher_activity, logger=None):
        self.package_name = package_name
        self.launcher_activity = launcher_activity
        self.logger = logger if logger else logging

        self.file_hashes = set()
        self.output_dir = config.OUTPUT_DIR.format(package_name, int(time.time()))
        os.mkdir(self.output_dir)

    def start_app(self):
        command = config.ADB_AM_START.format(config.ADB, config.DEVICE_NAME, self.package_name, self.launcher_activity)
        os.system(command)

    def copy_files(self):
        command = config.ADB_CP.format(config.ADB, config.DEVICE_NAME, self.package_name, self.package_name, config.ADB_LOG)
        self.logger.debug('Copying all files to sdcard: {}'.format(command))
        os.system(command)

    def pull_files(self):
        command = config.ADB_PULL.format(config.ADB, config.DEVICE_NAME, self.package_name, config.ADB_LOG)
        self.logger.debug('Pulling all the files to local: {}'.format(command))
        os.system(command)

    def check_file(self, file_path):        
        self.logger.debug('Checking file {}'.format(file_path))
        vc = validity_checker.ValidityChecker(file_path, dex=True, apk=False, archive=True, logger=self.logger)
        if not vc.dex and not vc.archive:
            return
        file_hash = hashlib.md5()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(config.HASH_BUFF_SIZE)
                if not data:
                    break
                file_hash.update(data)
        file_hash = file_hash.hexdigest()
        if file_hash in self.file_hashes:   
            self.logger.debug('File was already extracted!')
            return
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(self.output_dir, '{}_{}'.format(int(time.time()), file_name))
        shutil.copyfile(file_path, destination_path)
        self.file_hashes.add(file_hash)
        self.logger.info('Found file for extraction {} with hash {}'.format(file_name, file_hash))
        
    def check_files(self):
        if not os.path.isdir(self.package_name):
            time.sleep(config.TIMEOUT)
            return
            # raise exceptions.FailedPull(self.package_name)
        for root, dirs, files in os.walk(self.package_name):
            for f in files:                
                self.check_file(os.path.join(root, f))

    def start_monitor(self):
        end_time = time.time() + config.MONITOR_TIME
        while time.time() < end_time:
            self.copy_files()            
            self.pull_files()
            self.check_files()
            time.sleep(config.MONITOR_TIC)
        self.logger.info('Timeout reached! Extracted {} files.'.format(len(self.file_hashes)))



