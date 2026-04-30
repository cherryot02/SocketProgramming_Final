CYSE250 – BOOKWORM

Socket Programming Project - Cherry May A. Ang

## **Project description and goal**

BookWorm is a playful rename for Facebook. There’s no real association with it, but it simulates the idea of a social media site with huge limitations. It has login and registers options. Users can create page name and send a “like” requests to all the users in Bookworm. Users are not allowed to accept, just decline all the requests can be made. This socket programming project uses TCP/IP for the traffic and uses Caesar Cipher (only shifts 3) for encryption and decryption.

The main goal is for me to be able to use what I have learned to run an auto-decline like requests pages that are sent on Facebook. Although, this is completely out of what I started with using Selenium, it helped me understand the usage of functions, lists, dictionaries, statements, and loops.

## **Features and functionality**

I used Visual Studio Code (VS Code) to write the program. I also used the internal terminal on VS Code, so I don’t have to bring up a new window. Additionally, I used Wireshark to confirm if the payload in the socket is being encrypted. Although Caesar cipher is very weak, this still gives me an idea and visual look on how things work at the network level.

**User Authentication**

- Users are welcomed and asked to LOGIN or REGISTER
- Existing users can login with credential verification.
- Imported a module called “getpass” so password is typed but is invisible.
- Imported a module called “os” to check existing files.
- Username and password is stored in users.txt. in “username,password” format.
- Failed login attempts will provide a message.

**Main menu loop (4 options)**

Option 1 – Send a like request

Option 2 – List and decline ALL requests

Option 3 – View Declined pages – Shows only the logged in user’s declined pages.

Option 4 – Exit/Quit – closes the server connection and logs out user.

## **Technologies used**

- Visual Studio Code
- Wireshark
- Additional resources:
- Python docs
- Stack Overflow
- W3Schools
- YouTube videos

## **Instructions to run the program**

This is very limited, since this is barebones, there’s no UI or web server to run this program.
You will need the python files to be downloaded, ideally in one folder.

Because this is a client-server connection, we’ll have to run server.py first, then client.py.

If using VS Code, you should be able to run in using VS Code’s dedicated terminal.

If not using VS code, you can run in using PowerShell or cmd terminal, make sure to change directories to that folder the files are on and then “run server,py” then “run client.py”

## **Explanation of encryption, decryption, and authentication processes**

- Loops
- While loops
- For loops
- Functions (def)
- Encrypt(text, shift=3)
- Devrypt(text, shift=3)
- Load\_users()
- Save\_user(username,password)
- Auth(username, password)
- Register(username,password)
- Log\_action (action)
- Send\_menu(client)
- clientHandler(client, addr)
- main()
- Lists and dictionaries
- Users = {} – dictionary for users and password
- Entries = [] – this is for the users who entered page names

Socket programming (client-server architecture)
- Server = server = socket.socket(socket.AF\_INET, socket.SOCK\_STREAM)
- server.connect(ADDRESS) – in client.py, client connects

- File handling (e.g., storing user credentials or data)
- Users open files, read and append actions
- Ex. with open(USERS\_FILE, "r") as f:
- Encryption and decryption techniques (https://www.w3resource.com/python-exercises/string/python-data-type-string-exercise-25.php)
- Used Caesar Cipher since it’s simplest and we also used in the labs.

Authentication mechanisms
- To use authenticate , 1 it uses the decryption/encryption techniques .
- To verify, we need to compare the inputs on username and password.
- If duplicates > it will prompt that User already exists and loops back to login.

## **Challenges and limitations**

There were a lot that I could not take down because it was a lot of trial and error. Like at first I had an option to accept, and it created a new file of accepted file, but I ended up disregarding that as it made it complicated and went away from the point of my goal, which is to decline all requests.

Initially, I thought it would be close to how I started my auto-decline personal project but it’s completely different since that uses HTML tags and launches chrome etc. This one is its own server and client, so it does not apply. There are a few things I can do.

But I took down some of the bugs on the last few stretches of trying to run the program.

The one good thing on VS Code is it highlights an area if there were missed variables that I did not call and which lines are creating the error. It also tells me the error below if server.py is not running with the connection refused error.


**Bug 1:**

Encoding and decoding syntax – I was actually following the lab and lecture on the send and receive encryption but it did not include the .encode / .decode of the strings or prompts.
ex. client.send(encrypt("Invalid option. Goodbye.").encode()) instead of client.send(encrypt("Invalid option. Goodbye.")

> it’s applying the Caesar cipher because I defined it as such and it’s reading it as str so it will encrypt/decrypt with the str 26 alphabet not the actual bytes.

**Bug 2: on Users.txt**

I have created existing users.txt. With test1,test1 (username,password) in it. The problem I had is then when I register and it appends the new user; it does not go to line 2. So the temp fix, if I still wanted that existing user, is once new user is added, I manually separated the appended user, that fixes it. That also caused a mismatch on the password > I can demonstrate.

**Bug 3:**

I was missing the .encode() syntax and was forgetting to put the ().

**Bug 4:**

I doubled encrypted a few lines. Since there were a lot of repeats of send/receive so once I added the same line twice, I copied and pasted it and forgotten to make the appropriate edits, causing the encryption and send recv functions to break.

Ex. On server.py

    #LOGIN or REGISTER

    client.send(encrypt("Welcome to BookWorm! \n Type LOGIN or REGISTER:").encode())

    choice = encrypted(client.recv(BUFSIZE).decode()).strip().upper() #for upprcase

corrected:

    #LOGIN or REGISTER

    client.send(encrypt("Welcome to BookWorm! \n Type LOGIN or REGISTER:").encode())

    choice = decrypt(client.recv(BUFSIZE).decode()).strip().upper() #for upprcase

**Bug 5: Many other mistype and indentation errors**

I had many errors in indentation and misspellings. Every run program shows me where it was wrong. There were MANY of them and I kept going back and forth.

**Other Limitations**

### 1. After the choices (MENU), I don’t have an option to go back to login or log out. It closes the connection instead so I will have to run the client file again.
### 2. It is not a full social media site where I can accept or decline invites.
### 3. Input validation is non-existent; the most is that if it’s an incorrect number option or no matching credentials.
