import logging

from zipfile import ZipFile

import config


class ValidityChecker:

    def __init__(self, filepath, dex=False, apk=True, archive=False, logger=None):
        '''
        Checks whether the file found at filepath is a valid DEX (if dex == True) or APK file (if apk == True). 
        Variables self.dex and self.apk will be set accordingly.
        File parsing exceptions are considered logging.DEBUG level due to checking invalid files as well.
        '''
        self.filepath = filepath
        self.archive = None
        self.dex = None
        self.apk = None
        self.logger = logger if logger else logging
        self.magic = None
        self.archive_files = None
        try:
            with open(self.filepath, 'rb') as f:
                self.magic = f.read(8)
        except Exception as e:
            self.logger.exception('Could not read from file {}: {}'.format(filepath, e))
            return

        if dex:
            self.dex = self.check_dex()
        if archive or apk:
            self.archive = self.check_archive()
        if apk:
            self.apk = self.check_apk()

    def check_dex(self):
        if self.magic in config.VALID_DEX_MAGICS:
            self.logger.debug('File {} is a valid DEX file'.format(self.filepath))
            return True
        else:
            self.logger.debug('File {} is not a valid DEX due to magic not matching'.format(self.filepath))
            return False

    def check_apk(self):
        if not self.archive:
            return False
        if any([filename not in self.archive_files for filename in config.APK_FILES]):
            self.logger.debug('File {} is not a valid APK due to missing archive files')
            return False
        self.logger.debug('File {} is a valid APK file'.format(self.filepath))
        return True

    def check_archive(self):
        if not any([self.magic.startswith(magic) for magic in config.VALID_APK_MAGICS]):
            self.logger.debug('File {} is not a valid archive due to magic not matching'.format(self.filepath))
            return False    
        try:
            self.archive_files = ZipFile(self.filepath).namelist()
            return True
        except:
            self.logger.debug('Could not parse file {} as a zip archive'.format(self.filepath))
            return False
    