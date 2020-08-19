import PySimpleGUI as sg
import pathlib
import os
import json

sg.ChangeLookAndFeel('Dark')
darkmode=True

win_w=90
win_h=25
file=None

jsonpath = '../HY/hybrid/db/dataset.json'
pythonpath='../HY/hybrid/skills/'

menu_layout=[['File', ['New (Ctrl+N)', 'Save (Ctrl+S)', ' --- ', 'Exit']],
            ['Tools', ['Switch lang (Ctrl+O)']],
            ['Customize', ['dark mode']],
            ['Help', ['About', 'How To']]]

layout= [[sg.Menu(menu_layout)],
        [sg.Button('test!')],
        [sg.Button('hy update')],
        [sg.Text('New File', font=('Consolas', 10), size=(win_w, 1), key='_INFO_')],
        [sg.Multiline(font=('Consolas', 11), size=(win_w, win_h), key='_BODY_')]]

win = sg.Window('hyDev console', layout=layout, margins=(0, 0), resizable=True, return_keyboard_events=True, finalize=True)
win.maximize()
win['_BODY_'].expand(expand_x=True, expand_y=True)

def new_file():
    win['_BODY_'].update(value='')
    win['_INFO_'].update(value='New File')
    file=None
    return file

def switch_lang(at:str):
    #print(at)
    f=lambda : 'templates/json.json' if at=='py' else 'templates/python.py'
    filename = f() #sg.popup_get_file('Open', no_window=True)
    if filename:
        file = pathlib.Path(filename)
        win['_BODY_'].update(value=file.read_text())
        win['_INFO_'].update(value=file.absolute())
        return file

def save_file(file):
    '''Save file instantly if already open; otherwise use `save-as` popup'''
    if file:
        file.write_text(values.get('_BODY_'))
        sg.popup_no_buttons('Saved', auto_close=True, auto_close_duration=0.6)
    else:
        save_file_as()

def update_hybrid():
    n=0
    hyjson=pathlib.Path(jsonpath)
    #hypy = pathlib.Path(pythonpath)
    for file in os.listdir(pythonpath):
        n+=1
    f=open(pythonpath+'skill_'+str(n)+'.py', 'w+')
    f.close()
    hypy=pathlib.Path(pythonpath+'skill_'+str(n)+'.py')
    hypy.write_text(open('templates/python.py').read())
    #edit hybrid's json file
    x=json.loads(open(jsonpath).read())
    datas = json.loads(open('templates/json.json').read())
    x['intents'][datas['OriginalIntent']['name']+'Intent'] = datas['OriginalIntent'].copy()
    f=open(jsonpath, 'w+')
    f.write(json.dumps(x))
    f.close()
    #print(x)
    #print(hypy.read_text())
    print('[*] Done')

def test():
    runnable = pathlib.Path('templates/python.py')
    exec(runnable.read_text())

def save_file_as():
    '''Save new file or save existing file with another name'''
    filename = sg.popup_get_file('Save As', save_as=True, no_window=True)
    if filename:
        file = pathlib.Path(filename)
        file.write_text(values.get('_BODY_'))
        window['_INFO_'].update(value=file.absolute())
        return file

def how_to():
    text='sto ancora scrivendo i tutorial :('
    sg.popup_auto_close(text, title='how to', auto_close=False)

def about_me():
    '''A short, pithy quote'''
    sg.popup_no_wait('ciao, sono un programmatore di 14 anni, ho creato 3 intelligenze artificiali, video giochi e strumenti come calcolatrici ecc. spero ti piacerà hydev console!')

file=pathlib.Path('templates/python.py')
win['_BODY_'].update(value=file.read_text())
win['_INFO_'].update(value=file.absolute())
actual_type='py'
while True:
    event, values = win.read()
    if event in('Exit', None):
        break
    if event in ('New (Ctrl+N)', 'n:78'):
        file = new_file()
    if event in ('Switch lang (Ctrl+O)', 'o:79'):
        file = switch_lang(actual_type)
        if actual_type=='py':
            actual_type='json'
        elif actual_type=='json':
            actual_type='py'
    if event in ('Save (Ctrl+S)', 's:83'):
        save_file(file)
    if event in ('Save As',):
        file = save_file_as() 
    if event in ('How To',):
        how_to()
    if event in ('test!',):
        test()
    if event in ('hy update',):
        update_hybrid()
    if event in ('About',):
        about_me()
    if event in ('dark mode'):
        #tha hell why isn't this working? holy shit
        if darkmode:
            sg.ChangeLookAndFeel('LightGreen1')
            darkmode=False
        else:
            sg.ChangeLookAndFeel('Dark')
            darkmode=True
