import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
from kivy.core.clipboard import Clipboard
from kivy.storage.jsonstore import JsonStore

from constants import SERVER_URI

import base64

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.username_w = TextInput(multiline=False)
        self.password_w = TextInput(password=True, multiline=False)
        self.login_btn = Button(text='Login')
        self.login_btn.bind(on_press=self.login)
        
        self.add_widget(Label(text='Username'))
        self.add_widget(self.username_w)
        self.add_widget(Label(text='Password'))
        self.add_widget(self.password_w)
        self.add_widget(self.login_btn)

    def store_data(self, data):
        """
        Stores the 'data' in json format.
        """
        store = JsonStore('data.json')
        token = "%s:%s" % (data['username'], data['password'])
        token = base64.b64encode(token.encode('utf-8')).decode('utf-8')
        store.put('basic_auth', token=token)
    
    def login(self, button):
        self.creds = {
            'username': self.username_w.text,
            'password': self.password_w.text
        }
        login_res = UrlRequest(
            SERVER_URI+'check-creds/',
            on_success = self.store_data(self.creds)
        )
        self.add_widget(Label(text='Success! Credential verified and stored.'))


class CloudcbScreen(BoxLayout):

    def __init__(self, auth_token):
        self.add_widget(Label(text='Cloud Clipboard'))
        self.add_widget(Label(text='Currently text on you local clipboard:'))
        self.add_widget(Label(text=self.copy()))
        self.add_widget(Button(text='Copy this to Cloud-cb', on_press=upload))
        self.add_widget(Button(text='Update from Cloud-cb', on_press=download))

        self.header = "Authentication: Basic %s" % auth_token
        self.url = SERVER_URI + 'copy-paste/'

    def download(self, btn):
        self.paste_res = UrlRequest(self.url, req_headers=header,
                                    on_success=self.paste)
        
    def paste(self, result):
        # todo: this losses currently copied text, so store it somewhere
        Clipboard.copy(self.result['text'])

    def copy(self):
        return Clipboard.paste()

    def upload(self, btn):
        self.copy_res = UrlRequest(self.url, req_headers=header,
                                   req_body=self.copy())

class MyApp(App):

    def get_data(self, key):
        store = JsonStore("%s.json" % key)
        if store.exists(key):
            return store.get(key)
        return None

    def build(self):
        
        creds = self.get_data('credentials')
        if creds:
            return Cloudcb(creds)
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
