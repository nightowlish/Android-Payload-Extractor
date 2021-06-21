from docopt import docopt

import sys
import shutil
import logging

import config
import exceptions
import validity_checker
import data_extractor
import sdk_handler
import emu_handler
import disk_monitor
import garbage_man


def check_dependencies(logger):
    for tool in config.TOOLS:
        if not shutil.which(tool):
            raise(exceptions.MissingDependency(tool))

def get_stdout_logger(debug):
    root = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    if debug:
        root.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.INFO)
        handler.setLevel(logging.INFO)
    formatter = logging.Formatter(config.LOGGING_FORMAT)
    handler.setFormatter(formatter)
    root.addHandler(handler)
    return root

def rename_apk(args):
    if args['APK'].endswith('.apk'):
        return args
    new_name = '{}.apk'.format(args['APK'])
    try:
        shutil.copyfile(args['APK'], new_name)
    except Exception as e:
        raise exceptions.RenameException(args['APK'], e)
    args['APK'] = new_name
    return args

def do_logic(args, logger):
    logger.debug('Will run ctchr with arguments: \n{}'.format(args))
    vc = validity_checker.ValidityChecker(args['APK'], logger=logger)
    if not vc.apk:
        raise exceptions.InvalidAPK(args['APK'])

    data = data_extractor.DataExtractor(args, logger=logger)
    logger.debug('Extracted data: {}'.format(data.data))

    sh = sdk_handler.SDKHandler(data.data['min_sdk'], data.data['target_sdk'], data.data['max_sdk'], data.data['abis'], args['--tag'], logger=logger)
    if sh.need_install:
        sh.do_install()

    eh = emu_handler.EmuHandler(sh.system_image, args['APK'], data.data, logger=logger)
    eh.handle_installation()

    dm = disk_monitor.DiskMonitor(data.data['package_name'], data.data['launcher_activity'], logger=logger)
    dm.start_app()
    dm.start_monitor()    
    
    gm = garbage_man.GarbageMan(args['APK'], data.data['package_name'], logger=logger)
    gm.cleanup(eh)


    


    
def main():
    args = docopt(config.USAGE)

    args = rename_apk(args)

    logger = get_stdout_logger(args['--verbose'])

    check_dependencies(logger)
    
    do_logic(args, logger)


if __name__ == '__main__':
    main()