class InvalidAPK(Exception):
    def __init__(self, filepath):
        super().__init__('File {} is not a valid APK file.'.format(filepath))

class MissingDependency(Exception):
    def __init__(self, dependency):
        super().__init__('Dependency {} is missing. Please add it to your path before proceeding.'.format(dependency))
        
class RenameException(Exception):
    def __init__(self, filename, exc):
        super().__init__('Could not rename file {}: {}'.format(filename, exc))

class FaultyDecompilation(Exception):
    def __init__(self, apk_path, output_dir):
        super().__init__('Decompilation of file {} into directory {} was not successful'.format(apk_path, output_dir))

class MissingManifest(Exception):
    def __init__(self, manifest_path):
        super().__init__('Manifest file not found at location {}'.format(manifest_path))

class InvalidManifestFile(Exception):
    def __init__(self, manifest_path, exc):
        super().__init__('Could not parse manifest file found at {}: {}'.format(manifest_path, exc))

class NoMatchingSystemImage(Exception):
    def __init__(self, min_api, target_api, max_api, abis, tag):
        super().__init__('Could not find a matching system image for api {} {} {} abis {} tag {}'.format(min_api, target_api, max_api, abis, tag))

class SystemImageInstallFailed(Exception):
    def __init__(self, image_data):
        super().__init__('System image install failed for image {}'.format(image_data))

class FailedAVDCreation(Exception):
    def __init__(self, name):
        super().__init__('Failed to create AVD {}'.format(name))

class FailedPull(Exception):
    def __init__(self, dir_name):
        super().__init__('Failed to pull files to {}'.format(dir_name))

class SDKManagerFailure(Exception):
    def __init__(self, exc):
        super().__init__('SDK manager failed: {}'.format(exc))

class FailedInstallation(Exception):
    def __init__(self, exc):
        super().__init__('Failed to install application: {}'.format(exc))

class MalformedLog(Exception):
    def __init__(self, exc):
        super().__init__('Malformed log could not be parsed: {}'.format(exc))






    
