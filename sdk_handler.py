import os
import logging

import config
import exceptions

class SDKHandler:
    def __init__(self, min_sdk, target_sdk, max_sdk, abis, tag, logger=None):
        self.min_sdk = int(min_sdk)
        self.target_sdk = int(target_sdk)
        self.max_sdk = int(max_sdk)
        self.abis = abis
        self.tag = tag
        self.logger = logger if logger else logging

        self.final_api = None
        self.final_abi = None
        self.system_image = None
        self.need_install = self.check_need_install()

    def check_need_install(self):
        os.system(config.SDKMANAGER_LIST_INSTALLED)
        datas = self.get_sdkmanager_data(config.SDKMANAGER_LOG)
        for data in datas:
            self.final_abi = data['abi']
            self.final_api = data['api']
            if data['api'] == self.target_sdk:
                break
        if not self.final_api or not self.final_abi:
            self.logger.info('Did not find a good system image already installed')
            return True
        self.system_image = config.SYSTEM_IMAGE_FORMAT.format(self.final_api, self.tag, self.final_abi)
        self.logger.debug('Found good installed system image: SDK {} ABI {} TAG {}'.format(self.final_api, self.final_abi, self.tag))
        return False

    def do_install(self):
        self.set_image_to_install()
        self.logger.info('Will install system image {}'.format(self.system_image))
        command = config.SDKMANAGER_INSTALL.format(config.SDKMANAGER, self.system_image, config.SDKMANAGER_LOG)
        self.logger.debug('Install command: {}'.format(command))
        os.system(command)
        install_failed = self.check_need_install()
        if install_failed:
            raise exceptions.SystemImageInstallFailed(self.system_image)

    def set_image_to_install(self):
        os.system(config.SDKMANAGER_LIST_AVAILABLE)
        datas = self.get_sdkmanager_data(config.SDKMANAGER_LOG)
        if not datas:
            raise exceptions.NoMatchingSystemImage(self.min_sdk, self.target_sdk, self.max_sdk, self.abis, self.tag)
        target_data = [d for d in datas if d['api'] == self.target_sdk]
        if target_data:
            perfect_data = [d for d in target_data if 'x86' in d['abi']]
            if perfect_data:
                final_data = perfect_data[0]
            else:
                final_data = target_data[0]
        else:
            final_data = datas[0]
        self.system_image = config.SYSTEM_IMAGE_FORMAT.format(final_data['api'], final_data['tag'], final_data['abi'])            

    def get_sdkmanager_data(self, filename):
        data = []
        try:
            with open(filename, 'r') as f:
                for line in f.readlines():
                    line = line.strip().split()
                    if not line or not line[0].startswith('system-images;'):
                        continue
                    temp, api, tag, abi = line[0].split(';')
                    try:
                        api = int(api.split('-')[1])
                    except:
                        continue
                    if tag != self.tag:
                        continue
                    if not abi in self.abis:
                        continue
                    if self.min_sdk > api or api > self.max_sdk:
                        continue
                    data.append({'api': api, 'tag': tag, 'abi': abi})
        except Exception as e:
            raise exceptions.SDKManagerFailure(e)
        return data
    



