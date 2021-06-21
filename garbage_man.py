import os
import shutil
import logging

import config


class GarbageMan:
    def __init__(self, apk_path, package_name, logger=None):
        self.package_name = package_name
        self.apktool_dir = config.APKTOOL_DIR.format(apk_path)
        self.logger = logger if logger else logging

    def cleanup(self, emu_handler):
        self.cleanup_file(config.ADB_LOG)
        self.cleanup_file(config.APKTOOL_LOG)
        self.cleanup_file(config.AVDMANAGER_LOG)
        self.cleanup_file(config.SDKMANAGER_LOG)
        self.cleanup_file(config.EMULATOR_LOG)
        self.cleanup_dir(self.package_name)
        self.cleanup_dir(self.apktool_dir)
        emu_handler.kill_avd()
        emu_handler.delete_avd()

    def cleanup_file(self, file_name):
        try:
            os.remove(file_name)
        except Exception as e:
            self.logger.debug('Could not remove file {}: {}'.format(file_name, e))

    def cleanup_dir(self, dir_name):
        try:
            shutil.rmtree(dir_name)
        except Exception as e:
            self.logger.debug('Could not remove directory {}: {}'.format(dir_name, e))
        
        
        