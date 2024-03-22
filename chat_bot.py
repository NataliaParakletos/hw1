import pickle
from address_book import AddressBook, Field, Name, Phone, Birthday, Record
from datetime import datetime, timedelta

def input_error(func): 
    def inner(*args, **kwargs): 
        try: 
            return func(*args, **kwargs) 
        except ValueError: 
            return "Give me name and phone please." 
        except KeyError: 
            return "Contact not found." 
        except IndexError:
            return "Enter the argument for the command."
    return inner 

def parse_input(user_input): 
    cmd, *args = user_input.split() 
    cmd = cmd.strip().lower() 
    return cmd, args

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

@input_error
def add_contact(args, address_book): 
    name = args[0]
    phones = args[1:]
    record = Record(name)
    for phone in phones:
        record.add_phone(phone)
    address_book.add_record(record) 
    return "Contact added." 

@input_error
def change_contact(args, address_book): 
    record = address_book.find(args[0])
    if record:
        record.edit_phone(record.phones[0].value, args[1])
        return("Contact updated.")
    else:
        return("Contact not found.")


@input_error
def show_phone(args, address_book): 
    record = address_book.find(args[0])
    if record:
        return(f"Phone number for {args[0]}: {record.phones[0].value}")
    else:
        return("Contact not found.")
    
@input_error
def deletephone(args, address_book):
    record = address_book.find(args[0])
    if len(args) < 2:
        print("Enter both name and phone number to delete.")
    else:
        record = address_book.find(args[0])
        if record:
            record.delete_phone(args[1])
            print("Phone number deleted.")
        else:
            print("Contact not found.")

@input_error 
def add_birthday(args, address_book): 
    name = args[0] 
    birthday = args[1] 
    record = address_book.find(name) 
    if record: 
        record.add_birthday(Birthday(birthday)) 
        return "Birthday added." 
    else: 
        return "Contact not found." 

@input_error 
def show_birthday(args, address_book): 
    record = address_book.find(args[0]) 
    if record and record.birthday: 
        return f"{args[0]}'s birthday: {record.birthday.value}" 
    elif record and not record.birthday: 
        return f"{args[0]} has no specified birthday." 
    else: 
        return "Contact not found." 

@input_error     
def show_upcoming_birthdays(address_book):  
    result = "Upcoming birthdays within the next week:\n"  
    today = datetime.today()  
    upcoming_birthdays = False 
    for record in address_book.values():  
        if record.birthday:  
            bday = datetime.strptime(record.birthday.value, '%d.%m.%Y')  
            bday = bday.replace(year=today.year)
            if today < bday < today + timedelta(days=7):  
                result += f"{record.name.value}: {record.birthday.value}\n"  
                upcoming_birthdays = True 
    if not upcoming_birthdays: 
        result += "No upcoming birthdays within the next week.\n"  
    return result 


@input_error    
def show_all(address_book): 
    result = "Contacts list:\n" 
    for record in address_book.values(): 
        result += f"{record.name.value}: "
        for phone in record.phones:
            result += f"{phone.value}, "
        result += f"{record.birthday.value if record.birthday else 'No birthday specified'}\n"
    return result

def main(): 
    address_book=load_data()

    print("Welcome to the assistant bot!") 
    while True: 
        user_input = input("Enter a command: ") 
        command, args = parse_input(user_input) 

        if command in ["close", "exit"]: 
            print("Good bye!")
            save_data(address_book) 
            break 
        elif command == "hello": 
            print("How can I help you?") 
        elif command == "add":
            print(add_contact(args, address_book))
        elif command == "update": 
            print(change_contact(args, address_book))
        elif command == "deletephone":
            print(deletephone(args, address_book))  
        elif command == "phone" and args: 
            print(show_phone(args, address_book))
        elif command == "add_birthday" and args: 
            print(add_birthday(args, address_book))
        elif command == "show_birthday" and args: 
            print(show_birthday(args, address_book))


        elif command == "birthdays": 
            print(show_upcoming_birthdays(address_book))


        elif command == "all": 
            print(show_all(address_book))
        else: 
            print("Invalid command.") 


if __name__ == "__main__": 
    main=input_error(main)
    main()