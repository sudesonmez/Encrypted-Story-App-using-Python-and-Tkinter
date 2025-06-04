import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os

STORY_FOLDER = "stories"
USER_FILE = os.path.join(STORY_FOLDER, "users.json")

if not os.path.exists(STORY_FOLDER):
    os.makedirs(STORY_FOLDER)

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as file:
        json.dump({}, file)

def load_users():
    with open(USER_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file)

def xor_encrypt(text, key):
    return ''.join(chr(ord(text[i]) ^ ord(key[i % len(key)])) for i in range(len(text)))

def xor_decrypt(text, key):
    return ''.join(chr(ord(text[i]) ^ ord(key[i % len(key)])) for i in range(len(text)))

def user_exists(username):
    users = load_users()
    return username in users

def save_user(username, password):
    users = load_users()
    users[username] = {"password": password, "stories": {}}
    save_users(users)

def check_user_login(username, password):
    users = load_users()
    return users.get(username, {}).get("password") == password

def save_encrypted_story(username, encrypted_text, key):
    users = load_users()
    if username in users:
        story_id = str(len(users[username]["stories"]) + 1)
        users[username]["stories"][story_id] = {"encrypted_text": encrypted_text, "key": key}
        save_users(users)

def load_encrypted_stories(username):
    users = load_users()
    return users.get(username, {}).get("stories", {})

def show_previous_stories(username):
    stories = load_encrypted_stories(username)
    if not stories:
        messagebox.showinfo("Bilgi", "Önceden şifrelenmiş hikaye bulunamadı!")
        return
    history_window = tk.Toplevel()
    history_window.title("Önceki Şifrelenmiş Hikayeler")
    history_window.geometry("450x500")
    history_window.configure(bg="white")
 # kullanıcı kendi arkaplanını koyabilir
    bg_image = Image.open(r"C:\Users\sudenur\Desktop\stories\background.png")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(history_window, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.image = bg_image
    
    tk.Label(history_window, text="Şifrelenmiş Hikayeler:", bg="white", font=("Helvetica", 14, "bold")).pack(pady=5)
    story_listbox = tk.Listbox(history_window, width=50, height=10)
    for story_id, story_data in stories.items():
        story_listbox.insert(tk.END, f"{story_id}: {story_data['encrypted_text']}")
    story_listbox.pack(pady=5)

    tk.Label(history_window, text="Seçilen Hikayeyi Çözmek İçin Anahtar Girin:", bg="white", font=("Helvetica", 12)).pack(pady=5)
    key_entry = tk.Entry(history_window, width=30, show="*")
    key_entry.pack(pady=5)
    
    decrypted_text_var = tk.StringVar()
    decrypted_label = tk.Label(history_window, textvariable=decrypted_text_var, height=4, width=50, wraplength=350, bg="lightgray")
    decrypted_label.pack(pady=5)
    
    def decrypt_selected():
        selected_index = story_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Hata", "Lütfen bir hikaye seçin!")
            return
        selected_id = story_listbox.get(selected_index).split(":")[0]
        story_data = stories.get(selected_id, {})
        encrypted_value = story_data.get("encrypted_text", "")
        correct_key = story_data.get("key", "")
        entered_key = key_entry.get().strip()
        if not entered_key:
            messagebox.showerror("Hata", "Lütfen şifreleme anahtarını girin!")
            return
        if entered_key != correct_key:
            messagebox.showerror("Hata", "Yanlış anahtar! Hikaye çözülemedi.")
            return
        decrypted_text_var.set(xor_decrypt(encrypted_value, entered_key))
    
    decrypt_button = tk.Button(history_window, text="Şifreyi Çöz", command=decrypt_selected)
    decrypt_button.pack(pady=5)

def main_window(username):
    window = tk.Tk()
    window.title(f"{username} - XOR Şifreleme ve Çözme")
    window.geometry("450x600")
    
    bg_image = Image.open(r"C:\Users\sudenur\Desktop\stories\background.png")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(window, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.image = bg_image
    
    encrypted_text = tk.StringVar()
    decrypted_text = tk.StringVar()
    
    def on_encrypt():
        text = text_entry.get("1.0", "end-1c").strip()
        key = key_entry.get().strip()
        if not text or not key:
            messagebox.showerror("Hata", "Lütfen hikaye ve anahtar girin!")
            return
        encrypted = xor_encrypt(text, key)
        encrypted_text.set(encrypted)
        save_encrypted_story(username, encrypted, key)
        messagebox.showinfo("Başarı", "Hikaye başarıyla şifrelendi!")
    
    def on_decrypt():
        encrypted_value = encrypted_text.get().strip()
        key = key_entry.get().strip()
        if not encrypted_value or not key:
            messagebox.showerror("Hata", "Lütfen şifrelenmiş hikaye ve anahtar girin!")
            return
        decrypted_text.set(xor_decrypt(encrypted_value, key))
    
    tk.Label(window, text="Anahtar:", font=("Helvetica", 12), bg="white").pack(pady=5)
    key_entry = tk.Entry(window, width=50, show="*")
    key_entry.pack(pady=5)
    
    tk.Label(window, text="Hikaye:", font=("Helvetica", 12), bg="white").pack(pady=5)
    text_entry = tk.Text(window, width=50, height=8)
    text_entry.pack(pady=5)
    
    encrypt_button = tk.Button(window, text="Şifrele", command=on_encrypt)
    encrypt_button.pack(pady=5)
    
    history_button = tk.Button(window, text="Önceki Hikayeler", command=lambda: show_previous_stories(username))
    history_button.pack(pady=10)
    
    window.mainloop()

def register_screen():
    window = tk.Tk()
    window.title("Kayıt Ol")
    window.geometry("450x300")
    
    bg_image = Image.open(r"C:\Users\sudenur\Desktop\stories\background.png")
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(window, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.image = bg_image
    
    tk.Label(window, text="Kullanıcı Adı:").pack(pady=10)
    username_entry = tk.Entry(window, width=30)
    username_entry.pack(pady=5)
    
    tk.Label(window, text="Şifre:").pack(pady=10)
    password_entry = tk.Entry(window, width=30, show="*")
    password_entry.pack(pady=5)
    
    def on_register():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre gereklidir!")
            return
        if user_exists(username):
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut!")
        else:
            save_user(username, password)
            messagebox.showinfo("Başarı", "Kayıt başarıyla tamamlandı!")
            window.destroy()
            login_screen()
    
    register_button = tk.Button(window, text="Kayıt Ol", command=on_register)
    register_button.pack(pady=20)
    
    window.mainloop()

def login_screen():
    window = tk.Tk()
    window.title("Giriş Yap")
    window.geometry("450x300")
    # kullanıcı kendi arkaplanını koyabilir
    bg_image = Image.open(r"C:\Users\sudenur\Desktop\stories\background.png") 
    bg_image = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(window, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.image = bg_image
    
    tk.Label(window, text="Kullanıcı Adı:").pack(pady=10)
    username_entry = tk.Entry(window, width=30)
    username_entry.pack(pady=5)
    
    tk.Label(window, text="Şifre:").pack(pady=10)
    password_entry = tk.Entry(window, width=30, show="*")
    password_entry.pack(pady=5)
    
    def on_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre gereklidir!")
            return
        if user_exists(username):
            if check_user_login(username, password):
                window.destroy()
                main_window(username)
            else:
                messagebox.showerror("Hata", "Yanlış şifre!")
        else:
            messagebox.showerror("Hata", "Kullanıcı bulunamadı!")
    
    login_button = tk.Button(window, text="Giriş Yap", command=on_login)
    login_button.pack(pady=20)
    
    register_button = tk.Button(window, text="Kayıt Ol", command=lambda: [window.destroy(), register_screen()])
    register_button.pack(pady=5)
    
    window.mainloop()

login_screen()
