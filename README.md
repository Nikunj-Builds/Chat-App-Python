# Chat-App-Python — Chat Over the Internet

Python
Platform
GUI
Dependencies

Chat-App-Python is a small multi-client desktop chat application built with
Python. It uses a free public MQTT broker as the relay, so devices can chat
from anywhere over the internet — no server to run, no port forwarding, and
no VPN such as Tailscale. A Tkinter client gives each device a dark,
WhatsApp-style chat window.

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [How it works](#how-it-works)
- [Project files](#project-files)
- [Functions reference](#functions-reference)
- [Installation](#installation)
  - [Windows](#windows)
  - [Linux](#linux)
- [Configuration](#configuration)
- [Usage](#usage)
- [How messages travel](#how-messages-travel)
- [Security note](#security-note)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Credits](#credits)

---

## About

Chat-App-Python is a single program, `main.py`, that runs on every device
that wants to chat:

1. It connects to a free public **MQTT broker** over the internet.
2. It subscribes to a **topic** that is built from a shared room name.
3. Every message you send is published to that topic, and the broker
   delivers it to every other device subscribed to the same topic.

Because the broker does the relaying, there is no server program to start,
no IP address to type in, and no VPN required. Two people just need to use
the **same room name**.

---

## Features

- Chat over the internet through a free public MQTT broker — no server to host.
- Tkinter desktop client with a WhatsApp-style dark theme.
- Messages are delivered to every device in the same room.
- Each message is prefixed with the sender's display name.
- Colour-coded names — your own messages in green, others in pink.
- Automatic reconnection handled by the MQTT client loop.
- Runs on Windows, Linux and macOS.

---

## How it works


| Component | Role                                                                     |
| --------- | ------------------------------------------------------------------------ |
| Broker    | A public MQTT server (`broker.hivemq.com`) that relays messages.         |
| `main.py` | Connects to the broker, publishes your messages, and shows incoming ones. |


Messages travel as plain text in the form `Name: message`. Your client
publishes that text to the topic, the broker forwards it to every other
subscriber, and each client draws it in its chat window. A message you sent
also comes back to you from the broker; the client ignores that copy because
it has already shown your message locally.

---

## Project files


| File               | Purpose                                          | Created when    |
| ------------------ | ------------------------------------------------ | --------------- |
| `main.py`          | The chat client. Run on each device that chats.  | You download it |
| `requirements.txt` | Dependency list (`paho-mqtt`).                   | You download it |
| `README.md`        | This documentation.                              | You download it |
| `LICENSE`          | MIT license text.                                | You download it |


---

## Functions reference

### Client (`main.py`)

- `on_connect(client, userdata, flags, reason_code, properties=None)` — called
automatically once the broker connection is established. Subscribes to the
topic and reports success in the chat window.
- `on_message(client, userdata, msg)` — called automatically when a message
arrives on the topic. Skips your own messages (they are already shown
locally) and puts the rest into a queue.
- `on_disconnect(client, userdata, flags, reason_code, properties=None)` —
called automatically if the connection drops. Reports it in the chat window.
- `connect_to_server()` — builds the MQTT client with a unique client id,
wires up the callbacks, connects to the broker, and starts the background
network loop.
- `send_messages(event=None)` — reads the input box, shows your message in the
window, and publishes `"Name: message"` to the topic.
- `check_server()` — runs on a timer. Takes messages out of the queue and draws
them in the window. The queue is used because MQTT callbacks run on a
background thread, while the Tkinter interface must only be updated from the
main thread.

---

## Installation

Follow the section for your operating system.

### Windows

**1. Install Python**

- Download Python 3.8 or newer from [https://www.python.org/downloads/](https://www.python.org/downloads/).
- During install, **tick "Add Python to PATH"**.
- Verify in Command Prompt:
  ```bat
  python --version
  ```

**2. Get the app**

- Clone the repository (or download the ZIP and extract it):
  ```bat
  git clone https://github.com/Nikunj-Builds/Chat-App-Python.git
  cd Chat-App-Python
  ```

**3. Create a virtual environment**

```bat
python -m venv .venv
```

**4. Activate the virtual environment**

```bat
.venv\Scripts\activate
```

Your prompt now starts with `(.venv)`. (In PowerShell, if activation is
blocked, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.)

**5. Install the dependencies**

```bat
pip install -r requirements.txt
```

**6. Run it** — see [Usage](#usage).

### Linux

**1. Install Python and Tk**

- Most distros ship Python 3. Check it:
  ```bash
  python3 --version
  ```
- Install the Tk library (needed by the client's GUI):
  ```bash
  sudo apt install python3-tk        # Debian / Ubuntu
  sudo dnf install python3-tkinter   # Fedora
  ```

**2. Get the app**

```bash
git clone https://github.com/Nikunj-Builds/Chat-App-Python.git
cd Chat-App-Python
```

**3. Create and activate a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**4. Install the dependencies**

```bash
pip install -r requirements.txt
```

**5. Run it** — see [Usage](#usage).


## Configuration

Open `main.py` and set the values at the top of the file.


| Variable | Default               | Meaning                                                             |
| -------- | --------------------- | ------------------------------------------------------------------- |
| `BROKER` | `broker.hivemq.com`   | Address of the MQTT broker. Any public broker works.                |
| `PORT`   | `1883`                | Broker port. `1883` is the standard plain MQTT port.                |
| `ROOM`   | `your-room-name`      | Shared room name. **Everyone who should chat must use the same value.** |
| `MYNAME` | `your-name`           | Display name for this device — set a different name on each device. |


`TOPIC` is built automatically from `ROOM` as `chat/<ROOM>`, so changing
`ROOM` changes the topic everyone meets on.

---

## Usage

**1. Set your details** in `main.py` — give each device its own `MYNAME`, and
give every device the same `ROOM`.

**2. Start the app** on each device:

```bash
python3 main.py
```

The window opens and shows `-- connected (Success) --`.

**3. Type a message** and press **Enter** (or click **Send**). It appears on
every other device in the same room, prefixed with your display name.

That is the whole setup — there is no server to start first and no IP
address to exchange.

---

## How messages travel

```
Device A  ──publish──▶  MQTT broker  ──deliver──▶  Device B
   ▲                                                   │
   └──────────────── same topic (chat/<ROOM>) ──────────┘
```

Every device subscribes to the same topic, so the broker fans each message
out to all of them. Devices only need an internet connection and the same
room name — they can be on different networks, different cities, or different
countries.

---

## Security note

Messages are sent as **plain text** and the broker is **public**. Anyone who
knows the room name can subscribe to the topic and read the messages. Do not
send sensitive information without adding your own encryption — for example,
encrypting each message with a shared secret before publishing and decrypting
it after receiving.

---

## Troubleshooting

- `ModuleNotFoundError: No module named 'paho'` — the package is not installed.
Run `pip install -r requirements.txt` with the virtual environment active. Note
that the package is installed as `paho-mqtt` but imported as `paho.mqtt.client`.
- `pip` **says "No matching distribution found for paho"** — the package name is
`paho-mqtt`, not `paho`.
- `ModuleNotFoundError: No module named 'tkinter'` — install Tk for your OS
(Linux: `sudo apt install python3-tk`).
- **Stuck on "connect failed"** — you have no internet connection, or the broker
is unreachable. Check your connection and confirm `BROKER` and `PORT` are
correct.
- **Messages do not reach the other device** — make sure both devices use the
**same** `ROOM` value, and that both show `-- connected (Success) --`.
- **Your own message appears twice** — the broker sends your message back to you.
The client skips it by comparing against `MYNAME`, so make sure each device has
a **different** `MYNAME`.
- `pip` **says "Can not perform a '--user' install"** — you are inside a venv;
just run `pip install -r requirements.txt` normally with the venv active.

---

## License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for the full license text.

## Credits

Built with Python — [Tkinter](https://docs.python.org/3/library/tkinter.html)
for the GUI and [paho-mqtt](https://pypi.org/project/paho-mqtt/) for the
networking, relaying through the public
[HiveMQ](https://www.hivemq.com/mqtt/public-mqtt-broker/) broker.
