import pywhatkit as kit

def get_number():
    """Get the WhatsApp number with country code."""
    return input("Enter the phone number (with country code, e.g., +27605077578): ")

def get_msg():
    """Get the message to send."""
    return input("Enter the message to send: ")

def get_time():
    """Get the hour and minute to send the message."""
    hour = int(input("Enter the hour (24-hour format, e.g., 14 for 2 PM): "))
    minute = int(input("Enter the minute: "))
    return hour, minute

# Collect information from the user
number = get_number()
message = get_msg()
hour, minute = get_time()

# Send the message
kit.sendwhatmsg(number, message, hour, minute)
