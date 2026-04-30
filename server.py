import socket
import os #for existing files

#---The Casear encryption and decryption on SERVER side---
def encrypt(text, shift=3): #shifts every letter to right right 3 times.
    result = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result +=chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result

def decrypt(text, shift=3):
    return encrypt(text, -shift)

#Variables to be used + OTHERS
USERS_FILE = "users.txt"
LOG_FILE = "activity_log.txt"
REQS_FILE = "pending_requests.txt"
DECLINED_FILE = "declined_pages.txt"
BUFSIZE = 1024

#loading existing users
def load_users():
    users = {} #empty dictionary
    if not os.path.exists(USERS_FILE): #detects if file exists
        return users #just prints this if not existing
    with open(USERS_FILE, "r") as f: #proceeds to this if existing
        for line in f:
            line = line.strip() #removes spaces, new lines etc > just strips to str basically
            if "," in line:
                username, password = line.split(",", 1) #the 1 means it's just splits/separates from 1 comma
                users[username] = password #this adds as key and becomes a pair in the dictionary. So we can associate who has that password
    return users

#if new, save/append it to users.txt
def save_user(username, password):
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{password}\n")

#same with pages
def load_entries(filepath):
    entries = []
    if not os.path.exists(filepath): #uses the os module to check the existing file
        return entries
    with open(filepath, "r") as f: #open and read the file
        for line in f:
            line = line.strip()
            if "," in line:
                username, page = line.split(",",1)
                entries.append({"from": username, "page": page})
    return entries

def save_entries(filepath, entries):
    with open(filepath, "w") as f:
        for e in entries:
            f.write(f"{e['from']},{e['page']}\n")
            
def append_entry(filepath, username, page):
    with open(filepath, "a") as f:
        f.write(f"{username},{page}\n")

def auth(username, password):
    users = load_users()
    return username in users and users[username] == password # this applies the kyed pairing of the words from the above users.

def register(username, password):
    users = load_users()
    if username in users:
        return False
    save_user(username, password)
    return True



def log_action(action):
    with open(LOG_FILE, "a") as f:
        f.write(action + "\n")
    print("LOG:", action)

def send_menu(client):
    menu = (
        "\n ---MENU---\n"
        "1. Send a like request.\n"
        "2. List & Decline ALL requests.\n"
        "3. View Declined pages.\n"
        "4. Exit/Quit.\n"
        "Choose (1-4):"
    )
    client.send(encrypt(menu).encode())

    
#Client handler > not a separate file
def clientHandler(client, addr):
    print(f"\nConnection from {addr}")

    #LOGIN or REGISTER
    while True: #wrapping the below so it loops to login if invalid and not close the connection
        client.send(encrypt("Welcome to BookWorm! \n Type LOGIN or REGISTER:").encode())
        choice = decrypt(client.recv(BUFSIZE).decode()).strip().upper() #for upprcase

        client.send(encrypt("Username:").encode())
        username = decrypt(client.recv(BUFSIZE).decode()).strip()

        client.send(encrypt("Password:").encode())
        password = decrypt(client.recv(BUFSIZE).decode()).strip()

        if choice == "REGISTER":
            if register(username, password):
                client.send(encrypt(f"Account created. Welcome, {username}!").encode())
                log_action(f"New user registered: {username}")
                break
            else:
                client.send(encrypt(f"User already exists.").encode())
                log_action(f"New user registered: {username}")

        elif choice == "LOGIN":
            if auth(username, password):
                client.send(encrypt(f"Login Successful. Hello, {username}!").encode())
                log_action(f"User logged out: {username}")
                break
            else:
                client.send(encrypt("Invalid credentials. Try again.").encode())

        else:
            client.send(encrypt("Invalid option. Try again.").encode())
            

    #---MENU LOOP----
    while True:
        send_menu(client)
        option = decrypt(client.recv(BUFSIZE).decode()).strip()

        #Option 1: Send "Like" page request
        if option == "1":
            client.send(encrypt("Enter a page name to send a like request to ALL:").encode())
            page = decrypt(client.recv(BUFSIZE).decode()).strip()
            append_entry(REQS_FILE, username, page)
            log_action(f"{username} sent a like request for {page}")
            client.send(encrypt(f"Like request for '{page}' has been sent!").encode())

        #Option 2: List & ask to decline all
        elif option == "2":
            pending = load_entries(REQS_FILE)
            if not pending:
                client.send(encrypt("No pending requests.").encode())
            else:
                lines = [f"{i+1}. From: {e['from']} - Page: {e['page']}" for i, e in enumerate(pending)]
                msg = "-- Pending Requests -- \n" + "\n".join(lines) + "\n\nDecline all? (Y/N):"
                client.send(encrypt(msg).encode())
                answer = decrypt(client.recv(BUFSIZE).decode()).strip().upper()
                if answer == "Y":
                    for e in pending:
                        append_entry(DECLINED_FILE, username, e["page"])
                    save_entries(REQS_FILE, [])
                    log_action(f"{username} declines all pending requests")
                    client.send(encrypt(f"All {len(pending)} requests declined and saved to declined_pages.txt.").encode())
                else:
                    client.send(encrypt("No changes made.").encode())

        #Option 3: View declined pages
        elif option =="3":
            dec_list = [e for e in load_entries(DECLINED_FILE) if e["from"] == username]
            if not dec_list:
                client.send(encrypt("No declined pages yet.").encode())
            else:
                lines = [f"{i+1}. Page: {e['page']}" for i, e in enumerate(dec_list)]
                client.send(encrypt(f"--{username}'s Declined Pages --\n" + "\n".join(lines)).encode())

        #Option 4: Exit/quit
        elif option == "4":
            client.send(encrypt("Exiting...Goodbye!").encode())
            break
        else:
            client.send(encrypt("Invalid option, try again.").encode())

    client.close()
    print(f"Connection closed: {addr}")

#---MAIN----------
def main():
    HOST = "localhost"
    PORT = 6000
    BUFSIZE = 1024
    ADDRESS =(HOST, PORT)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #This is a "buffer" where if connection closes, you can still resuewithout it refusing due to port being in use.
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server.bind((ADDRESS))
    server.listen(3) #listens to incoming connections, the 3 is how many clients can queue
    print(f"BookWorm Server running on {ADDRESS}")

    while True:
        conn, addr = server.accept()
        clientHandler(conn, addr)

if __name__ == "__main__":
    main()
