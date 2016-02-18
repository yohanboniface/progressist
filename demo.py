import sys
import time

try:
    import psutil
except ImportError:
    psutil = None
from progresso import Bar


def loop():
    for i in range(20):
        time.sleep(0.2)
        yield True


def call(bar):
    for x in bar.iter(loop()):
        continue


def demo_default():
    bar = Bar(total=20, prefix="Default:")
    call(bar)


def demo_custom_done_char():
    bar = Bar(total=20, done_char='█', prefix="Custom fill character:")
    call(bar)


def demo_custom_remain_char():
    """Custom empty fill character."""
    bar = Bar(total=20, done_char='◉', remain_char='◯',
              prefix="Custom empty fill char:")
    call(bar)


def demo_with_eta():
    bar = Bar(total=20, template='With ETA: {progress} ETA: {eta:%H:%M:%S}')
    call(bar)


def demo_with_avg():
    bar = Bar(total=20, template='With Average: {progress} Avg: {avg} loop/s')
    call(bar)


def demo_with_custom_color():
    bar = Bar(total=20, remain_char='-', invisible_chars=11,
              template="\r\033[34mCustom color: {progress}\033[39m")
    call(bar)


def demo_with_custom_class():

    class MyBar(Bar):

        @property
        def swap(self):
            if not psutil:
                return "psutil not installed"
            return psutil.swap_memory().total

    bar = MyBar(total=20,
                template='Custom class with custom info: '
                         '{progress} Swap: {swap}')
    call(bar)


def demo_spinner():

    bar = Bar(total=20, prefix="Spinner", progress='{spinner}')
    call(bar)


def demo_spinner_without_total():

    bar = Bar(progress='{spinner}',
              template='Spinner without total: {progress} '
                       'Elapsed: {elapsed}')
    call(bar)


def demo_reverse_bar():

    class MyBar(Bar):

        @property
        def bar(self):
            done_chars = int(self.fraction * self.free_space)
            remain_chars = self.free_space - done_chars
            return (self.remain_char * remain_chars
                    + self.done_char * done_chars)

    bar = MyBar(total=20, template="{percent} {progress} Reverse bar")
    call(bar)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        globals()[sys.argv[1]]()
    else:
        for name, func in globals().copy().items():
            if name.startswith('demo_'):
                func()
