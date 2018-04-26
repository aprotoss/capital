# -*- coding: utf-8 -*-
from cmd import Cmd
from capital import Capital
import sys
import inspect
    
#sys.coinit_flags = 0
import pythoncom

NOTE = '[NOTE] '
WARNING= '[WARNING] '
PROMPT = '(cmd) '

class ShellPrompt(Cmd):
    def __init__(self, parent=None):
        super(ShellPrompt, self).__init__(parent)

        self.prompt = PROMPT


    def default(self, line):
        if line[:2] == 'SK':
            try:
                self.capital.setCMD(*line.split())
            except:
                print(WARNING + 'command not found')
        else:
            print(WARNING + 'command not found')

    def emptyline(self):
        pass
    
    def preloop(self):
        self._apistart(None)

    def do_exit(self , args):
        print(NOTE + 'start to exit progress...')
        self._apistop(None)
        return True

    def do_bye(self, args):
        self.do_exit(args)

    def _apistart(self, args):
        print(NOTE + 'start the capital thread')
        self.capital = Capital()
        self.capital.start()

    def _apistop(self, args):
        print(NOTE + 'stop the capital thread')
        if self.capital:
            self.capital.stop()
            del self.capital
            self.capital = None

if __name__ == '__main__':
    print('--- Start ---')
    shell = ShellPrompt()
    shell.cmdloop('--- Shell ---')

