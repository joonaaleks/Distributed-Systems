import xmlrpc.client
import datetime

server = xmlrpc.client.ServerProxy("http://localhost:3000")


def add_note():
    topic = input("Enter topic: ")
    note = input("Enter note: ")
    text = input("Enter text: ")
    date = datetime.datetime.today()
    timestamp = date.strftime("%m/%d/%Y - %H:%M:%S")
    result = server.add_note(topic, note, text, timestamp)
    print(result)


def get_notes():
    topic = input("Search notes with topic: ")
    notes = server.get_notes(topic)
    if notes == "No notes found!":
        print(notes)
    else:
        print("Notes: ")
        for note in notes:
            print(note)


def menu():
    i = 0
    while i == 0:
        choice = input(
            "Choose an option by entering the number:\n1. Add note\n2. Get notes\n3. Quit\n")
        if choice == "1":
            add_note()
        elif choice == "2":
            get_notes()
        elif choice == "3":
            i = 1
        else:
            print("Invalid choice")


menu()
