class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self, mode='oneChar'): return self.impl(mode)


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self, mode = 'oneChar'):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            result=''
            while True:
                ch = self.getCh(sys)
                if mode == 'multiChar':
                    if '\x1b' not in ch and '\x7f' not in ch and '\r' not in ch and '\t' not in ch and '\x18' not in ch:
                        print(ch, end='', flush=True)
                        result = result+ch
                    if ch == '\x7f' and len(result)>0:
                        print("\x1b[D \x1b[D", end='', flush=True)
                        result = result[:len(result)-1]
                    if '\r' in ch: break
                    if '\x1b' in ch:
                        result = ch
                        break
                    if '\t' in ch:
                        result = ch
                        break
                    if '\x18' in ch:
                        result = ch
                        break
                else:
                    result = ch
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return result

    def getCh(self, sys):
        ch = sys.stdin.read(1)
        if ch ==  '\x1b':
            ch = ch + sys.stdin.read(2)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()
