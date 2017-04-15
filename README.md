# cloud-clipboard

> I need a url on my mobile. Don't want to type it. Don't want to message myself.

Cloud Clipboard shares the data on clipboard across your devices. So it allows to copy on one device and paste on another.

Currently supported platforms: Linux, Android

# Setup

- Download or clone this repo and change your directory to it. You only need `cloud.py` on desktop.
- Install requirements by running

```bash
pip install -r server/requirements.txt
```

- Register yourself by running

```bash
python cloudcb.py register <username> <password>
```

- Install this [apk](https://github.com/krsoninikhil/cloud-clipboard/raw/master/mobile/bin/CloudClipboard-0.1-debug.apk) on your mobile.
- You're done.

# Instructions to use

- Copy the text.
- Execute this command to copy to cloud-clipboard if you are on desktop

```bash
python cloud.py copy <username> <password>
```

- Open the app on your mobile to get that text on mobile's clipboard (This will not be required from next update).
- Execute this command to update your desktop's clipboard to the text copied on other devices

```bash
python cloud.py paste <username> <password>
```

# License

[MIT License](https://nks.mit-license.org/)