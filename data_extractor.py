import os
import glob
import time
import logging

from xml.dom import minidom

import config
import exceptions


class DataExtractor:
    def __init__(self, args, logger=None):
        self.args = args
        self.logger = logger if logger else logging
        self.apk_path = args['APK']
        self.output_dir = config.APKTOOL_DIR.format(self.apk_path)
        self.manifest_path = config.APKTOOL_MANIFEST.format(self.output_dir)
        self.libs_path = config.APKTOOL_LIBS.format(self.output_dir)
        self.data = {'package_name': None, 'launcher_activity': None, 'target_sdk': config.DEFAULT_SDK, 'min_sdk': config.DEFAULT_SDK, 'max_sdk': config.DEFAULT_SDK}
        
        self.logger.info('Decoding APK...')
        self.decode_apk()
        self.logger.info('Extracting data...')
        self.extract_data()

    def decode_apk(self):
        command = config.APKTOOL_COMMAND.format(config.APKTOOL, self.output_dir, self.apk_path, config.APKTOOL_LOG)
        self.logger.debug('Will decode APK using arguments: {}'.format(command))
        os.system(command)
        time.sleep(1)
        if not os.path.isdir(self.output_dir):              
            raise exceptions.FaultyDecompilation(self.apk_path, self.output_dir)
        if not os.path.isfile(self.manifest_path):
            raise exceptions.MissingManifest(self.manifest_path)
    
    def extract_data(self):
        self.data['abis'] = self.get_matching_abis()
        try:
            xml = minidom.parse(self.manifest_path)
        except Exception as e:
            raise exceptions.InvalidManifestFile(self.manifest_path, e)
        if not xml:
            raise exceptions.InvalidManifestFile(self.manifest_path, 'invalid XML file')
        self.populate_sdk(xml)
        self.populate_main_activity(xml)

    def get_matching_abis(self):
        if self.args['--abi']:
            return [self.args['--abi']]
        return [dirname for dirname in os.listdir(self.libs_path) if os.path.isdir(os.path.join(self.libs_path, dirname))]        

    def populate_sdk(self, xml):
        if self.args['--api']:
            self.data['target_sdk'] = self.args['--api']
            self.data['min_sdk'] = self.args['--api']
            self.data['max_sdk'] = self.args['--api']
            return

        uses_sdk_tag = xml.getElementsByTagName('uses-sdk')
        if uses_sdk_tag:
            uses_sdk_tag = uses_sdk_tag[0]
            min_sdk = uses_sdk_tag.getAttribute('android:minSdkVersion') 
            max_sdk = uses_sdk_tag.getAttribute('android:maxSdkVersion')
            target_sdk = uses_sdk_tag.getAttribute('android:targetSdkVersion')
            self.data['target_sdk'] = target_sdk if target_sdk else config.DEFAULT_SDK
            self.data['min_sdk'] = min_sdk if min_sdk else self.data['target_sdk']
            self.data['max_sdk'] = max_sdk if max_sdk else self.data['target_sdk']

        manifest_tag = xml.getElementsByTagName('manifest')
        if manifest_tag:
            compile_sdk = manifest_tag[0].getAttribute('android:compileSdkVersion')
            self.data['target_sdk'] = compile_sdk
            self.data['min_sdk'] = self.data['target_sdk']
            self.data['max_sdk'] = self.data['target_sdk']
        else:
            raise exceptions.InvalidManifestFile(self.manifest_path, 'missing manifest tag')            

    def populate_main_activity(self, xml):
        if self.args['--packagename'] and self.args['--launcher']:
            self.data['package_name'] = self.args['--packagename']
            self.data['launcher_activity'] = self.args['--launcher']
            return

        manifest_tag = xml.getElementsByTagName('manifest')
        if manifest_tag:
            self.data['package_name'] = manifest_tag[0].getAttribute('package')
        else:
            raise exceptions.InvalidManifestFile(self.manifest_path, 'missing manifest tag')            

        activity_tag = xml.getElementsByTagName('activity')
        if not activity_tag:
            raise exceptions.InvalidManifestFile(self.manifest_path, 'missing manifest activity')
        
        for activity in activity_tag:
            for child in activity.childNodes:
                if child.nodeName != 'intent-filter':
                    continue
                categories = child.getElementsByTagName('category')
                if not categories:
                    continue
                for category in categories:                    
                    if category.getAttribute('android:name') != config.CATEGORY_LAUNCHER:
                        continue
                    activity_name = activity.getAttribute('android:name')
                    activity_name = self.data['package_name'] if activity_name.startswith('.') else activity_name                        
                    self.data['launcher_activity'] = activity_name                        
                    return
        raise exceptions.InvalidManifestFile(self.manifest_path, 'missing launcher activity')


        
        
        





