import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest
from kivy.core.clipboard import Clipboard
from kivy.storage.jsonstore import JsonStore

from constants import SERVER_URI

import base64

class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username_w = TextInput(multiline=False)
        self.password_w = TextInput(password=True, multiline=False)
        self.login_btn = Button(text='Login')
        self.login_btn.bind(on_press=self.login)

        layout = GridLayout()
        layout.cols = 2
        layout.add_widget(Label(text='Username'))
        layout.add_widget(self.username_w)
        layout.add_widget(Label(text='Password'))
        layout.add_widget(self.password_w)
        layout.add_widget(self.login_btn)

        self.add_widget(layout)

    def store_data(self, data):
        """
        Stores the 'data' in json format.
        """
        store = JsonStore('data.json')
        token = "%s:%s" % (data['username'], data['password'])
        token = base64.b64encode(token.encode('utf-8')).decode('utf-8')
        store.put('creds', token=token)
        self.add_widget(Label(text='Success! Credential verified and stored.'))
        self.manager.current = 'CloudCB'
    
    def login(self, button):
        creds = {
            'username': self.username_w.text,
            'password': self.password_w.text
        }
        login_res = UrlRequest(
            "%scheck-creds/" % SERVER_URI,
            on_success = self.store_data(creds)
        )


class CloudCBScreen(Screen):

    def __init__(self, auth_token, **kwargs):
        super().__init__(**kwargs)
        self.header = {'Authorization': "Basic %s" % auth_token}
        self.url = SERVER_URI + 'copy-paste/'       
        self.cloud_clip = TextInput(text="Fetching...")
        
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Cloud Clipboard\n'))
        layout.add_widget(Label(text='Current text on cloud clipboard:'))
        layout.add_widget(self.cloud_clip)
        layout.add_widget(Button(text='Refresh', on_press=self.download))
        layout.add_widget(Button(text='Update Cloud Clipboard', on_press=self.upload))
        self.add_widget(layout)

        self.download()

    def download(self, *args):
        self.paste_res = UrlRequest(
            self.url,
            req_headers = self.header,
            on_success = self.paste,
            on_error = self.show_error,
            on_failure = self.show_error
        )        
        
    def paste(self, req, res):
        # todo: this losses currently copied text, so store it somewhere
        print("pastecalled")
        Clipboard.copy(res['text'])
        self.update_cloud_clip()

    def upload(self, *args):
        payload = {'text': self.copy()}
        copy_res = UrlRequest(
            self.url,
            req_headers = self.header,
            req_body = payload,
            on_success = self.update_cloud_clip,
            on_error = self.show_error,
            on_failure = self.show_error
        )

    def copy(self):
        return Clipboard.paste()

    def update_cloud_clip(self, *args):
        self.cloud_clip.text = self.copy()
        
    def show_error(self, req, error):
        print(
            "Errors: %s" % error,
            "Request: %s" % req.__dict__,
            "This seems unusual. Please file a bug report with above details",
            "at https://github.com/krsoninikhil/cloud-clipboard/issues"
        )

        
class MyApp(App):

    def get_data(self, key):
        store = JsonStore('data.json')
        if store.exists(key):
            return store.get(key)['token']
        return None

    def build(self):
        self.title = "Cloud Clipboard"
        auth_token = self.get_data('basic_auth')
        sm = ScreenManager()
        s2 = CloudCBScreen(auth_token, name='CloudCB')
        s1 = LoginScreen(name='Login')
        sm.add_widget(s1)
        sm.add_widget(s2)
        if auth_token:
            sm.current = 'CloudCB'
        else:
            sm.current = 'Login'

        return sm


if __name__ == '__main__':
    MyApp().run()
