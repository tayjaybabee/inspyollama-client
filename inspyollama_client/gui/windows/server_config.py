import PySimpleGUI as psg
from inspyollama_client.config import Config


def layout():
    return [
        [psg.Text('Server Config', font=('Helvetica', 20))],
        [psg.Text('Server Host:'), psg.InputText(key='server_ip')],
        [psg.Text('Server Port:'), psg.InputText(key='server_port')],
        [psg.Button('Save', key='save_server_config')]
    ]

class ServerConfigWindow:
    def __init__(self):
        self.window = psg.Window('Server Config', layout())
        self.server_ip = None
        self.server_port = None

    def run(self):
        while True:
            event, values = self.window.read()
            if event == psg.WIN_CLOSED:
                break
            if event == 'save_server_config':
                self.server_ip = values['server_ip']
                self.server_port = values['server_port']
                break
        self.window.close()
        return self.server_ip, self.server_port

