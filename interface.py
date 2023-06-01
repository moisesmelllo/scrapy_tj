import PySimpleGUI as sg
url = ''


def interface():

    sg.theme('Reddit')

    layout = [
        [sg.Text('Digite a url da empresa: ')],
        [sg.Input(key='url')],
        [sg.Button('Consultar')],
        [sg.Text('', key='status')],
        [sg.Text('', key='spinner', visible=False)]
    ]

    window = sg.Window('Tela de consulta', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Consultar':
            window['Consultar'].update(disabled=True),
            window['status'].update('Consultando...')
            window['spinner'].update('⣾', visible=True)
            global url
            url = values['url']
            return url