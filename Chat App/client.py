import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
import customtkinter

host = socket.gethostbyname(socket.gethostname())
port = 55555

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.nickname = None
        self.get_nickname()

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def get_nickname(self):
        self.nickname_window = tkinter.Tk()
        self.nickname_window.configure(bg='gray10')
        self.nickname_window.title('Chat Application')
        self.nickname_window.geometry('400x200')

        label = customtkinter.CTkLabel(self.nickname_window, text='Chat Application', font=customtkinter.CTkFont(size=20, weight='bold'))
        label.pack(padx=20, pady=(20,10))

        self.nickname_entry = customtkinter.CTkEntry(self.nickname_window, placeholder_text='Enter Username', width=200, font=customtkinter.CTkFont(size=12))
        self.nickname_entry.pack(padx=20, pady=5)

        button = customtkinter.CTkButton(self.nickname_window, text='Submit', command=self.submit_nickname)
        button.pack(padx=20, pady=5)

        self.nickname_window.mainloop()

    def submit_nickname(self):
        self.nickname = self.nickname_entry.get()
        self.nickname_window.destroy()

    def gui_loop(self):

        self.chat_window = tkinter.Tk()
        self.chat_window.title("Chat App")
        self.chat_window.geometry(f"{1100}x{580}")
        self.chat_window.configure(bg='gray10')

        # configure grid layout
        self.chat_window.grid_columnconfigure(1, weight=1)
        self.chat_window.grid_columnconfigure((2, 3), weight=0)
        self.chat_window.grid_rowconfigure((0, 1, 2), weight=1)

        # configure widgets
        self.text_area = tkinter.scrolledtext.ScrolledText(self.chat_window, width=250)
        self.text_area.grid(row=0, column=1, columnspan=3, rowspan=3, padx=(20), pady=(20), sticky="nsew")
        self.text_area.config(state='disabled', bg='grey20', fg='lightgray')

        self.input_area = customtkinter.CTkEntry(self.chat_window, placeholder_text="Type Message...")
        self.input_area.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        send_button = customtkinter.CTkButton(self.chat_window, text='Send', border_width=2, text_color=("gray10", "#DCE4EE"), command=self.write)
        send_button.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.gui_done = True

        self.chat_window.protocol('WM_DELETE_WINDOW', self.stop)

        self.chat_window.mainloop()

    def write(self):
        message = f'{self.nickname}: {self.input_area.get()}\n'
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('0', 'end')

    def stop(self):
        self.running = False
        self.chat_window.quit()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')

            except ConnectionAbortedError:
                break

            except:
                print('Error')
                self.sock.close()
                break

client = Client(host, port)
