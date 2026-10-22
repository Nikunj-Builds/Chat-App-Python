from tkinter import *
import paho.mqtt.client as mqtt
import queue
import random
import os

BROKER = "broker.hivemq.com"
PORT = 1883
ROOM = "your-room-name"
TOPIC = f"chat/{ROOM}"
MYNAME = "your-name"

bg_main = '#111b21'
bg_chat = '#202c33'
bg_input = '#2a3942'
bg_button = '#00a884'
text_main = '#e9edef'
FONT = ('Arial', 12)

c = None
msg_queue = queue.Queue()


def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe(TOPIC)
    msg_queue.put(f'   -- connected ({reason_code}) --')


def on_message(client, userdata, msg):
    text = msg.payload.decode()
    if text.startswith(f"{MYNAME}: "):
        return
    msg_queue.put(f'   {text}')


def on_disconnect(client, userdata, flags, reason_code, properties=None):
    msg_queue.put('   -- disconnected --')


def connect_to_server():
    global c
    client_id = f"{MYNAME}-{random.randint(1000, 9999)}"
    try:
        c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    except AttributeError:
        c = mqtt.Client(client_id=client_id)
    c.on_connect = on_connect
    c.on_message = on_message
    c.on_disconnect = on_disconnect
    try:
        c.connect(BROKER, PORT, 60)
        c.loop_start()
    except OSError as e:
        msg_queue.put(f'   -- connect failed: {e} --')


def send_messages(event=None):
    msg = entry.get()
    if msg == "":
        return
    chat_window.insert('end', f'   {MYNAME}: ', "me")
    chat_window.insert('end', f'{msg}\n')
    chat_window.see('end')
    if c is not None:
        try:
            c.publish(TOPIC, f"{MYNAME}: {msg}")
        except OSError:
            pass
    entry.delete(0, 'end')


def check_server():
    while not msg_queue.empty():
        text = msg_queue.get()
        stripped = text.strip()
        if ": " in stripped and not stripped.startswith('--'):
            name, msg = stripped.split(": ", 1)
            chat_window.insert('end', f'   {name}: ', "other")
            chat_window.insert('end', f'{msg}\n')
        else:
            chat_window.insert('end', f'{text}\n')
    chat_window.see('end')
    root.after(100, check_server)


root = Tk()
root.geometry('600x600')
root.title(f'Encrypted Chat - {MYNAME}')
root.configure(bg=bg_main)

# FIX 1: Added 'r' before string so Windows backslash doesn't act as escape character
# Agar logo image nahi mil rahi toh ye line error de sakti hai, isliye try-except bhi lagaya ja sakta hai
try:
    p1 = PhotoImage(file=r'C:\Users\Deepanshu Sagar\Downloads\chatapplogo.png')
    root.iconphoto(False, p1)
except Exception as e:
    print("Icon load nahi hua:", e)

chat_window = Text(root, bg=bg_chat, fg=text_main, font=FONT)
chat_window.tag_config("me", foreground="#00a884")
chat_window.tag_config("other", foreground="#e91e63")

input_frame = Frame(root, bg=bg_main)
input_frame.pack(side='bottom', padx=10, pady=(0, 10), fill='both')

entry = Entry(input_frame, bg=bg_input, fg=text_main, insertbackground=text_main, font=FONT)
entry.pack(side='left', padx=10, pady=10, expand=True, fill='x')
entry.bind('<Return>', send_messages)

send_btn = Button(input_frame, text='Send', bg=bg_button, fg='#ffffff', font=FONT, command=send_messages)
send_btn.pack(side='right', padx=(10, 0), pady=10)

chat_window.pack(padx=10, pady=10, fill='both', expand=True)

connect_to_server()
root.after(100, check_server)
root.mainloop()
