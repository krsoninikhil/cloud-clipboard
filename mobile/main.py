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

import utils
from utils import SERVER_URI

import base64
import urllib

class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
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

    def store_data(self, token):
        """
        Stores the 'token' in json format.
        """
        store = JsonStore('data.json')
        store.put('creds', token=token)
        self.manager.current = 'CloudCB'
    
    def login(self, button):
        token = "%s:%s" % (self.username_w.text, self.password_w.text)
        token = base64.b64encode(token.encode('utf-8')).decode('utf-8')
        login_res = UrlRequest(
            "%scheck-creds/" % SERVER_URI,
            req_headers = {'Authorization': "Basic %s" % token},
            on_success = self.store_data(token),
            on_error = utils.show_error,
            on_failure = self.show_failure
        )

    def show_failure(self, req, res):
        print('Request: ', req)
        print('Response: ', res)
        if req.resp_status:
            self.manager.current = 'Login'


class CloudCBScreen(Screen):

    def __init__(self, auth_token, **kwargs):
        super(CloudCBScreen, self).__init__(**kwargs)
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
            on_error = utils.show_error,
            on_failure = self.show_failure
        )        
        
    def paste(self, req, res):
        # todo: this losses currently copied text, so store it somewhere
        Clipboard.copy(res['text'])
        self.update_cloud_clip()
        
    def upload(self, *args):
        # payload = urllib.parse.urlencode({'text': self.copy()})  # python3
        payload = urllib.urlencode({'text': self.copy()})  # python2
        self.header['Content-type'] = 'application/x-www-form-urlencoded'
        copy_res = UrlRequest(
            self.url,
            req_headers = self.header,
            req_body = payload,
            on_success = self.update_cloud_clip,
            on_error = utils.show_error,
            on_failure = self.show_failure
        )

    def copy(self):
        return Clipboard.paste()

    def update_cloud_clip(self, *args):
        self.cloud_clip.text = self.copy()

    def show_failure(self, req, res):
        print('Request: ', req)
        print('Response: ', res)
        if req.resp_status:
            self.manager.current = 'Login'

        
        
class MyApp(App):

    def get_data(self, key):
        store = JsonStore('data.json')
        if store.exists(key):
            return store.get(key)['token']
        return None

    def build(self):
        self.title = "Cloud Clipboard"
        auth_token = self.get_data('creds')
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
