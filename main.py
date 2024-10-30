import pywhatkit as kit

def get_number():
    """Get the WhatsApp number with country code, ensuring it contains only digits and no spaces."""
    while True:
        number = input("Enter the phone number (with country code, e.g., +27605077578): ")
        
        if number.startswith("+") and number[1:].isdigit():
            return number
        else:
            print("Invalid format. Please ensure it starts with + and contains only digits, with no spaces.")

def get_msg():
    """Get the message to send."""
    return input("Enter the message to send: ")

def get_time():
    """Get the hour and minute to send the message."""
    hour = int(input("Enter the hour (24-hour format, e.g., 14 for 2 PM): "))
    minute = int(input("Enter the minute: "))
    return hour, minute


number = get_number()
message = get_msg()
hour, minute = get_time()


kit.sendwhatmsg(number, message, hour, minute)
