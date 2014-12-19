
QUESTION = 'Do you know this? '

import sys
import os
import tty
import termios
import  tty

#_, orig, yes, no = sys.argv
_, orig, yes, no = (None, '/Users/miburr/Dropbox/Japanese-Word-Frequency-List-1-3000.txt', '/tmp/yes', '/tmp/no')

#if os.path.exists(yes):
#    print 'bail'
#    sys.exit(1)
#if os.path.exists(no):
#    print 'bail'
#    sys.exit(1)

orig = open(orig, 'r')

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_settings)
    return ch

known = set()
for path in yes, no:
    if os.path.exists(path):
        with open(path, 'r') as f:
            known.update(f.readlines())

with open(yes, 'a') as yes, open(no, 'a') as no:
    for line in orig:
        if line in known:
            continue
        answer = None
        while answer not in ('y', 'n', '\r'):
            print QUESTION, '[{0}] '.format(line.rstrip('\n')),
            answer = getch().lower()
            print ''
            if answer in ('y', '\r'):   ####### FIXME
                yes.write(line)
            elif answer in ('n',):
                no.write(line)
            elif answer in ('q',):
                sys.exit(0)
            else:
                print '>>>{0}<<<'.format(repr(answer))
