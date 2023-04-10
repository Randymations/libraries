from datetime import datetime
import os

def xprint(s, *args, **kwargs):
    s2 = ''
    for i in range(len(s)):
        s2 += s[i]
        if s[i] == '\n':
            s2 += ' '
    print(f' {s2}', *args, **kwargs)

def timeprint(message):
    print(f'[{datetime.now().time()}] ', end='')
    xprint(message)

def xinput(s, check, default=None, lower=True, fail=None):
    if fail is not None:
        fail = ' -- '+fail
    while True:
        xprint(s+' > ', end='')
        t = input().strip()
        if t == '' and default is not None:
            return default
        if lower:
            t = t.lower()
        if check(t):
            return t
        xprint('Invalid input'+fail)

def navigation(s, nav, setback=None, miscrun=lambda: None):

    def back():
        raise Jumpback
    def check(t):
        return t in choices

    if setback is None:
        s += ' [b]ack'
        nav['b'] = back
    else:
        nav[setback] = back

    choices = list(nav.keys())
    try:
        while True:
            try:
                nav[xinput(s, check, choices[0], True, 'Enter only a character inside []')]()
            except Cancel:
                pass
            miscrun()
    except Jumpback:
        pass

class Jumpback(Exception):
    pass
class Cancel(Exception):
    pass

def boolin(s, y=True):
    def check(t):
        return t in options
    options = ['y', 'yes', 'n', 'no']
    if xinput(s+(' [Y/n]' if y else ' [y/N]'), check, 'y' if y else 'n', True, 'Enter only y/yes or n/no') in options[0:2]:
        return True
    return False

def error(s, e=None):
    xprint('ERROR: '+s)
    if e is not None:
        xprint(str(e))

def picklist(picks, render=None):
    def check(t):
        return (t != '' and (((t.isdigit()) and (int(t) in range(len(choices)))) or ((t[0] == '/') and (t[1:] in choices)) or (t == '#')))
    if render is None:
        def render(choice):
            return choice
    choices = list(picks)
    for i in range(len(choices)):
        xprint(f'[{i}] {render(choices[i])}')
    t = xinput(f'Enter [0-{len(choices)-1}], /OPTION, or [#] (cancel)', check, None, False, f'Accepted range [0-{len(choices)-1}], /OPTION, or [#] (cancel)')
    if t == '#':
        raise Cancel
    if t.isdigit():
        return choices[int(t)]
    return t[1:]

def list_files(extensions=[], directory='.'):
    files = []
    try:
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                for extension in extensions:
                    if file.endswith(extension):
                        files.append(file)
    except OSError as e:
        error('Unable to read directory', e)
        if not boolin('Retry?'):
            raise Jumpback
    return files
