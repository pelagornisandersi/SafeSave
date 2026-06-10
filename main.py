import customtkinter as ctk
from database import (
    save_password,
    get_passwords,
    delete_password
)
from encryption import encrypt_password
from encryption import decrypt_password
from auth import *
from encryption import *
import pyperclip
from password_generator import generate_password

master_password = None

ctk.set_appearance_mode("dark")
#ctk.set_default_color_theme("green")

app = ctk.CTk()
app.configure(
    fg_color="#0D0D0D"
    )
app.geometry("1920x1080")

app.title("SafeSave")

# login frame
login_frame = ctk.CTkFrame(
    app,
    fg_color="#161616",
    corner_radius=20
)

startup_frame = ctk.CTkFrame(
    app,
    fg_color="#0D0D0D"
)

startup_frame.pack(
    expand=True,
    fill="both"
)

startup_label = ctk.CTkLabel(
    startup_frame,

    text="INITIALIZING...",

    text_color="#00FF9C",

    font=("Montserrat", 28, "bold")
)

startup_label.pack(expand=True)


startup_messages = [
    "INITIALIZING SYSTEM...",
    "LOADING AES ENGINE...",
    "VERIFYING DATABASE...",
    "ESTABLISHING SECURE SESSION...",
    "ACCESS READY"
]

current_message = 0


def animate_startup():

    global current_message

    if current_message < len(startup_messages):

        startup_label.configure(
            text=startup_messages[current_message]
        )

        current_message += 1

        app.after(
            1000,
            animate_startup
        )

    else:

        startup_frame.destroy()

        login_frame.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )

def save_data():

    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    salt = load_salt()

    encrypted_password = encrypt_password(
        password,
        master_password,
        salt
    )

    save_password(
        website,
        username,
        encrypted_password
    )

    website_entry.delete(0, "end")
    username_entry.delete(0, "end")
    password_entry.delete(0, "end")

    print("Password Saved Securely")

def remove_password(record_id):

    delete_password(record_id)

    show_passwords()



def show_passwords():

    records = get_passwords()

    salt = load_salt()

    # clear old widgets
    for widget in password_frame.winfo_children():
        widget.destroy()

    for record in records:

        record_id = record[0]
        website = record[1]
        username = record[2]
        encrypted_password = record[3]

        decrypted_password = decrypt_password(
            encrypted_password,
            master_password,
            salt
        )

        # row frame
        row = ctk.CTkFrame(
            password_frame,
            fg_color="#161616",
            corner_radius=12
        )
        row.pack(
            fill="x",
            padx=10,
            pady=5
        )

        # website label
        website_label = ctk.CTkLabel(
            row,
            text=website,
            width=150,
            anchor="w"
        )

        website_label.pack(
            side="left",
            padx=10
        )

        # username label
        username_label = ctk.CTkLabel(
            row,
            text=username,
            width=150,
            anchor="w"
        )

        username_label.pack(
            side="left",
            padx=10
        )

        # copy button
        copy_button = ctk.CTkButton(
            row,
            text="Copy Password",
            width=120,
            command=lambda p=decrypted_password:
                copy_password(p)
        )

        copy_button.pack(
            side="right",
            padx=10
        )

        delete_button = ctk.CTkButton(
        row,
        text="Delete",
        width=80,
        fg_color="darkred",
        hover_color="red",
        command=lambda r=record_id:
            remove_password(r)
        )

        delete_button.pack(
            side="right",
            padx=5
        )



def copy_password(password):

    pyperclip.copy(password)

    print("Password copied!")

def generate_new_password():

    password = generate_password()

    password_entry.delete(0, "end")

    password_entry.insert(0, password)

password_visible = False


def toggle_password():

    global password_visible

    if password_visible:

        password_entry.configure(show="*")

        show_button.configure(text="Show")

        password_visible = False

    else:

        password_entry.configure(show="")

        show_button.configure(text="Hide")

        password_visible = True


def open_vault():

    login_frame.destroy()

    # vault frame
    vault_frame = ctk.CTkFrame(
        app,
        fg_color="#161616",
        corner_radius=20
    )

    vault_frame.pack(
        expand=True,
        fill="both",
        padx=20,
        pady=20
    )

    # title
    title = ctk.CTkLabel(
        vault_frame,
        text="SafeSave",
        font=("Montserrat", 46, "bold"),
        text_color="#00FF9C"
    )

    title.pack(pady=20)

    # main content frame
    content_frame = ctk.CTkFrame(
        vault_frame,
        fg_color="transparent"
    )

    content_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    # LEFT PANEL
    left_frame = ctk.CTkFrame(
        content_frame,
        fg_color="#1E1E1E",
        border_color="#00FF9C",
        border_width=2,
        corner_radius=15,
        width=400
    )

    left_frame.pack(
        side="left",
        fill="y",
        padx=10,
        pady=10
    )

    # RIGHT PANEL
    right_frame = ctk.CTkFrame(
    content_frame,
    fg_color="#1E1E1E",
    corner_radius=15
    )   
    
    right_frame.pack(
        side="right",
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # WEBSITE ENTRY
    global website_entry

    website_entry = ctk.CTkEntry(
        left_frame,
        width=320,
        height=45,
        placeholder_text="Website",

        fg_color="#111111",
        border_color="#00FF9C",
        border_width=2,

        text_color="#00FF9C"
    )

    website_entry.pack(pady=15)

    # USERNAME ENTRY
    global username_entry

    username_entry = ctk.CTkEntry(
        left_frame,
        width=320,
        height=45,
        placeholder_text="Username / Email",

        fg_color="#111111",
        border_color="#00FF9C",
        border_width=2,

        text_color="#00FF9C"
    )

    username_entry.pack(pady=15)

    # PASSWORD ENTRY
    global password_entry

    password_entry = ctk.CTkEntry(
        left_frame,
        width=320,
        height=45,
        placeholder_text="Password",
        show="*",

        fg_color="#111111",
        border_color="#00FF9C",
        border_width=2,

        text_color="#00FF9C"
    )

    password_entry.pack(pady=15)

    # SHOW BUTTON
    global show_button

    show_button = ctk.CTkButton(
        left_frame,
        text="Show Password",
        width=320,
        height=40,

        command=toggle_password,

        fg_color="#00E5FF",
        hover_color="#00B8CC",

        text_color="black"
    )

    show_button.pack(pady=10)

    # GENERATE BUTTON
    generate_button = ctk.CTkButton(
        left_frame,
        text="Generate Strong Password",
        width=320,
        height=40,

        command=generate_new_password,

        fg_color="#00FF9C",
        hover_color="#00CC7A",

        text_color="black"
    )

    generate_button.pack(pady=10)

    # SAVE BUTTON
    save_button = ctk.CTkButton(
        left_frame,
        text="Save Password",
        width=320,
        height=40,

        command=save_data,

        fg_color="#00FF9C",
        hover_color="#00CC7A",

        text_color="black"
    )

    save_button.pack(pady=10)

    # VIEW BUTTON
    view_button = ctk.CTkButton(
        left_frame,
        text="Refresh Vault",
        width=320,
        height=40,

        command=show_passwords,

        fg_color="#222222",
        hover_color="#333333",

        border_color="#00FF9C",
        border_width=2,

        text_color="#00FF9C"
    )

    view_button.pack(pady=10)

    # RIGHT PANEL TITLE
    saved_label = ctk.CTkLabel(
        right_frame,
        text="PASSWORD DATABASE",
        font=("Montserrat", 24, "bold"),
        text_color="#00E5FF"
    )

    saved_label.pack(pady=15)

    # PASSWORD FRAME
    global password_frame

    password_frame = ctk.CTkScrollableFrame(
        right_frame,
        fg_color="#111111",
        corner_radius=10
    )

    password_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

def login():

    global master_password

    entered_password = (
        master_password_entry.get()
    )

    # first time setup
    if not master_password_exists():

        setup_master_password(
            entered_password
        )

        master_password = entered_password

        open_vault()

    else:

        if verify_master_password(
            entered_password
        ):

            master_password = entered_password

            open_vault()

        else:

            error_label.configure(
                text="Wrong Password"
            )

master_password_entry = ctk.CTkEntry(
    login_frame,
    width=400,
    height=50,
    placeholder_text="Enter Master Password",
    show="*",

    fg_color="#1E1E1E",
    border_color="#00FF9C",
    border_width=2,

    text_color="#00FF9C",

    corner_radius=10
)
master_password_entry.pack(pady=20)

error_label = ctk.CTkLabel(
    login_frame,
    text="",
    text_color="#FF003C",
    font=("Montserrat", 14, "bold")
)
error_label.pack(pady=5)


login_button = ctk.CTkButton(
    login_frame,

    text="UNLOCK VAULT",

    width=220,
    height=50,

    command=login,

    fg_color="#00FF9C",
    hover_color="#00CC7A",

    text_color="black",

    corner_radius=12,

    font=("Montserrat", 16, "bold")
)
login_button.pack(pady=30)



animate_startup()
app.mainloop()