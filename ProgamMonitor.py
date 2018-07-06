import schedule
import time
import psutil
import subprocess
import configparser


program_info_list = []
interval = 60

def read_config_file():
    '''解析配置文件'''
    print('{} 开始解析配置文件...'.format(time.asctime()))
    config = configparser.ConfigParser()
    program_list = []
    try:
        config.read('ProgramMonitor.ini')
        count = 0
        if config.has_option('main', 'count'):
            count = config.getint('main', 'count')
        if config.has_option('main', 'interval'):
            global interval
            interval = config.getint('main', 'interval')

        if count is None:
            return

        for i in range(count):
            section_name = 'program-{}'.format(i+1)
            program = {}
            if config.has_option(section_name, 'name'):
                program['name'] = config.get(section_name, 'name')
            else:
                continue
            if config.has_option(section_name, 'path'):
                program['path'] = config.get(section_name, 'path')
            program_list.append(program)
        global program_info_list
        program_info_list = program_list
        print('{} 解析配置文件成功...'.format(time.asctime()))

    except Exception as e:
        print(' 读取配置文件出错.')
        print(e)

def check(pname):
    print('{} 检查进程 {} 是否存在...'.format(time.asctime(), pname))
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            if pinfo['name'].lower() == pname.lower():
                return True
    print('{} 没有找到进程: {}'.format(time.asctime(), pname))
    return False

def check_and_run():
    global  program_info_list
    for program in program_info_list:
        try:
            pname = program['name']
            if pname[-4:] != '.exe':
                pname = pname + '.exe'
            if check(pname):
                return

            file_path = pname
            if program.has_key('path'):
                ppath = program['path']
                if ppath[-1] != '\\':
                    ppath = '{}{}'.format(ppath, '\\')
                file_path = '{}{}'.format(ppath, pname)

            print('{} 准备启动进程 {}'.format(time.asctime(), pname))
            cp = subprocess.Popen(file_path, start_new_session = True)
        except Exception as e:
            print('{} 在启动程序 {} 时发生异常...'.format(time.asctime(), pname))
            print(str(e))

read_config_file()
if len(program_info_list) > 0:
    print('{} 程序将每 {} 秒检查一次...'.format(time.asctime(), interval))
    schedule.every(interval).seconds.do(check_and_run)
    check_and_run()
    while True:
        schedule.run_pending()
        time.sleep(1)
else:
    print('{} 没有需要监控的文件，程序结束...'.format(time.asctime()))
