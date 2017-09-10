# cloud-clipboard

> I need a url on my mobile. Don't want to type it. Don't want to message myself.

Cloud Clipboard shares the data on clipboard across your devices. So it allows to copy on one device and paste on another.

Currently supported platforms: Linux, Windows, Android

# Setup

- Download or clone this repo and change your directory to it. You only need `cloud.py` on desktop.
- This scipt depends on `requests` and `pyperclip` python package, the later one also uses `xsel` system package. So install them by running

```bash
pip install requests pyperclip
apt-get install xsel
```

- Register yourself by running

```bash
python cloudcb.py register <username> <password>
```

- Replace `<username>` with your username and `<password>` with your password.
- Install this [apk](https://github.com/krsoninikhil/cloud-clipboard/raw/master/mobile/bin/CloudClipboard-1.0-debug.apk) on your mobile.

# Adding keyboard shortcuts

- Run the script with keyboard shortcuts analogous to `Ctrl + C` and `Ctrl + V`

### For Linux

- Add a keyboard shortcut `Alt + C` to run the below command

```bash
gnome-terminal --command "python3 /home/nks/Projects/cloud-clipboard/cloudcb.py copy <username> <password>"
```

- Add another keyboard shortcut `Alt + P` to run the below command

```bash
gnome-terminal --command "python3 /home/nks/Projects/cloud-clipboard/cloudcb.py paste <username> <password>"
```

### For Windows

- Right click and select `New -> Shortcut`
- Add the following line as path location and click OK

```bash
C:\Windows\System32\cmd.exe /c python C:\Users\nik\Downloads\cloudcb.py copy <username> <password>
```

- Replace the file path accordingly.
- Right click on shortcut icon and go to `properties`.
- Type the suitable keyboard shortcut and click Apply.

# Instructions to use

- Copy the text.
- Execute this command to copy to cloud-clipboard if you are on desktop or just press `Alt + C` if you have added the shortcut

```bash
python cloudcb.py copy <username> <password>
```

- Open the app on your mobile to get that text on mobile's clipboard.
- Execute this command to update your desktop's clipboard to the text copied on other devices or just press `Alt + P`

```bash
python cloudcb.py paste <username> <password>
```

# License

[MIT License](https://nks.mit-license.org/)
