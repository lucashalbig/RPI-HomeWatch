from subprocess import check_output as co, CalledProcessError, call
from os import kill
from signal import SIGTERM
from sys import argv, executable
import sys

TEST_PNAME = 'motion'

def getpid(name = TEST_PNAME):
    try:
        o = co(['ps','-fC',name]).decode()
        ol = o.split('\n')
        del ol[0]
        for item in ol:
            il = item.split(' ')
        
            il_ = []
            for prop in il:
                if prop != '':
                    il_.append(prop)
            
            if il_ != []:
                user, pid, ppid, c, stime, tty, time, cmd = il_
                return int(pid), ''
            
    except CalledProcessError as e:
        return None, f'{name!r} nicht gefunden'

def handlepg(name = TEST_PNAME, mode = 'term'):
    pid, err = getpid()
    if pid != None:
        try:
            kill(pid, SIGTERM)
            return 'Erfolgreich beendet'
        except PermissionError:
            print('Besitzt nicht die ausreichenden Rechte, Befehl wird mit sudo auto-wiederholt...')
            if __name__ == '__main__':
                call(['sudo', executable, argv[0], name, 'tryingagain'])
            else:
                call(['sudo', executable, __name__ +'.py', name, 'tryingagain'])
            return 'Erfolgreich beendet'
    else:
        return f'FEHLER: {err}'
    
if __name__ == '__main__':
    print(f'Terminator v0.1, using processname {argv[1]!r}...')
    res = handlepg(argv[1])
    if len(argv) < 3:
        print(res)