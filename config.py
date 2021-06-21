import os


USAGE = '''
    Usage: 
        ctchr.py data (APK) 
        ctchr.py extract (APK) [--abi ABI] [--tag TAG] [--api API] [(--packagename PKG --launcher LAUNCHER)] [-v]

    Arguments:
        APK         required input file; an APK file
        
    Options:
        -h --help           print usage
        -v --verbose        verbose logging
        --abi ABI           the ABI of the emulator (e.g. x86); will be taken the APK if not specified
        --tag TAG           the tag of the emulator [default: google_apis]
        --api API           the Android API level of the emulator; will be taken from the APK if not specified 
        --packagename PKG   the package name of the APK (e.g. com.example); used in comination with LAUNCHER 
        --launcher LAUNCHER the full name of the launcher activity of the APK (e.g. com.package.MainActivity)
    '''


LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

APKTOOL = 'apktool'
AVDMANAGER = 'avdmanager'
SDKMANAGER = 'sdkmanager'
EMULATOR = 'emulator'
ADB = 'adb'

TOOLS = [APKTOOL, AVDMANAGER, SDKMANAGER, EMULATOR, ADB]
APKTOOL_DIR = '{}.out'
APKTOOL_LIBS = os.path.join('{}', 'lib')
APKTOOL_LOG = '_apktool.log'
APKTOOL_COMMAND = '{} d -f -s -o {} {} > {} 2>&1'
APKTOOL_MANIFEST = os.path.join('{}', 'AndroidManifest.xml')

SDKMANAGER_LOG = '_sdkmanager.log'
SDKMANAGER_LIST_AVAILABLE = '{} --list > {} 2>&1'.format(SDKMANAGER, SDKMANAGER_LOG)
SDKMANAGER_LIST_INSTALLED = '{} --list_installed > {} 2>&1'.format(SDKMANAGER, SDKMANAGER_LOG)
SDKMANAGER_INSTALL = '{} --install "{}" > {} 2>&1'
SYSTEM_IMAGE_FORMAT = 'system-images;android-{};{};{}'

AVDMANAGER_LOG = '_avdmanager.log'
AVDMANAGER_CREATE = 'echo no | {} --verbose create avd --force --name {} --package {} --tag {} --abi {} --device "{}" > {} 2>&1'
AVDAMANGER_DELETE = '{} --verbose delete avd -n {} > {} 2>&1'

EMULATOR_LOG = '_emulator.log'
EMULATOR_LIST = '{} -list-avds > {} 2>&1'.format(EMULATOR, EMULATOR_LOG)
EMULATOR_INIT_TIMEOUT = 60
EMULATOR_TIMEOUT = 5
EMULATOR_FINAL_TIMEOUT = 10

DEVICE_NAME = 'emulator-5554'
DEVICE_TYPE = 'Nexus 5X'

ADB_LOG = '_adb.log'
ADB_INSTALL = '{} -s {} install {} > {} 2>&1'
ADB_CHECK_BOOT_COMPLETED = '{} -s {} shell getprop init.svc.bootanim > {} 2>&1'
ADB_PORT = 5037
ADB_HOST = '127.0.0.1'
ADB_AM_START = '{} -s {} shell am start -n {}/{}'
ADB_CP = '{} -s {} shell su 0 cp -R /data/data/{} /sdcard/{} > {} 2>&1'
ADB_PULL = '{} -s {} pull /sdcard/{} > {} 2>&1'
ADB_KILL = '{} -s {} emu kill > {} 2>&1'

OUTPUT_DIR = '{}_{}_extracted'
CATEGORY_LAUNCHER = 'android.intent.category.LAUNCHER'

KILL_TIMEOUT = 10
HASH_BUFF_SIZE =  65536 # 64KB
MONITOR_TIME = 10 * 60 # 10 minutes 
MONITOR_TIC = 5 
EXTRACTION_DIRECTORY = 'ctchr_extracted_files'
DEFAULT_SDK = 22
TIMEOUT = 30

# magic DEX constants taken from https://cs.android.com/android/platform/superproject/+/master:dalvik/tools/dexdeps/src/com/android/dexdeps/DexData.java
VALID_DEX_MAGICS = [b'dex\n035\x00', b'dex\n037\x00', b'dex\n038\x00', b'dex\n039\x00']
# magic APK constants taken from https://en.wikipedia.org/wiki/ZIP_(file_format)
VALID_APK_MAGICS = [b'PK\x03\x04', b'PK\x05\x06', b'PK\x07\x08']
# files necessary to be present in the ZIP archive to be a valid APK
APK_FILES = ['AndroidManifest.xml', 'classes.dex', 'META-INF/MANIFEST.MF']
