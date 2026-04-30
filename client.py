import socket
import getpass #this is for the password being invisble

#---The Casear encryption and decryption on client side---
def encrypt(text, shift=3):#shifts every letter to right right 3 times.
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

#---Main---------------
def main():
    HOST = "localhost"
    PORT = 6000
    BUFSIZE = 1024
    ADDRESS = (HOST, PORT)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # There's a problem, undefined socket. ?
    server.connect(ADDRESS)
    print("Welcome to BookWorm!\n") #\n to break

    while True: 
        prompt = decrypt(server.recv(BUFSIZE).decode())
        print(f"BookWorm | {prompt}")
        choice = input("You: ").strip()
        server.send(encrypt(choice).encode())

        prompt = decrypt(server.recv(BUFSIZE).decode())
        print(f"BookWorm | {prompt}")
        username = input("You: ").strip()
        server.send(encrypt(username).encode())

        prompt = decrypt(server.recv(BUFSIZE).decode())
        print(f"BookWorm | {prompt}")
        password = getpass.getpass("You: ").strip()
        server.send(encrypt(password).encode())

        response = decrypt(server.recv(BUFSIZE).decode())
        print(f"BookWorm | {response}\n")

        if "created" in response or "Hello" in response:
            break
        
    #--MENU--------
    while True:
        prompt = decrypt(server.recv(BUFSIZE).decode())
        print(f"\nBookworm | {prompt}")
        option = input("You:").strip()
        server.send(encrypt(option).encode())
        
        #Option 1: Send "Like" page request
        if option == "1": #Put quote because this is a str not an int
            response = decrypt(server.recv(BUFSIZE).decode())
            print(f"BookWorm | {response}")
            page = input("You: ").strip()
            server.send(encrypt(page).encode())
            final = decrypt(server.recv(BUFSIZE).decode())
            print(f"BookWorm | {final}")

        #Option 2: List & ask to decline all
        elif option == "2":
            response = decrypt(server.recv(BUFSIZE).decode())
            print(f"{response}")
            if "No pending" not in response:
                answer = input("You: ").strip()
                server.send(encrypt(answer).encode())
                final = decrypt(server.recv(BUFSIZE).decode())
                print(f"{final}")

        #Option 3&4: View declined and quit
        elif option == "3":
            exit = decrypt(server.recv(BUFSIZE).decode())
            print(f"BookWorm | {exit}")
            break

        elif option == "4":
            response = decrypt(server.recv(BUFSIZE).decode())
            print(f"BookWorm | {response}")
            break

        else:
            final = decrypt(server.recv(BUFSIZE).decode())
            print(f"BookWorm | {final}")

    server.close()
    print("\n Disconnected from BookWorm.")


if __name__ == "__main__":
    main()

