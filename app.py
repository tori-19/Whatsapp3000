from flask import Flask, render_template, request, redirect, url_for
import pywhatkit as kit
import threading
from datetime import datetime

app = Flask(__name__)

# List to hold scheduled messages
scheduled_messages = []
message_id_counter = 1  # Simple counter to create unique IDs for messages

def is_valid_number(number):
    return number.isdigit() and 7 <= len(number) <= 15

def send_message_later(message):
    number = message['number']
    msg = message['text']
    hour = message['hour']
    minute = message['minute']
    delay = message['delay']
    threading.Timer(delay, kit.sendwhatmsg, [number, msg, hour, minute]).start()

@app.route("/", methods=["GET", "POST"])
def home():
    global message_id_counter
    if request.method == "POST":
        try:
            country_code = request.form.get("country_code")
            phone_number = request.form.get("number")
            message = request.form.get("message")
            date = request.form.get("date")
            hour = int(request.form.get("hour"))
            minute = int(request.form.get("minute"))
            
            if not is_valid_number(phone_number):
                return "Invalid phone number format. Please enter digits only and exclude the leading zero."
            
            full_number = country_code + phone_number
            message_time = datetime.strptime(f"{date} {hour}:{minute}", "%Y-%m-%d %H:%M")

            delay = (message_time - datetime.now()).total_seconds()
            if delay < 60:
                return "Please schedule the message at least 1 minute in the future."

            # Create a message object
            message_obj = {
                'id': message_id_counter,
                'number': full_number,
                'text': message,
                'hour': hour,
                'minute': minute,
                'delay': delay
            }
            scheduled_messages.append(message_obj)  # Add to scheduled messages
            send_message_later(message_obj)  # Schedule the message

            message_id_counter += 1  # Increment the ID counter
            return render_template("index.html", scheduled_messages=scheduled_messages, message_scheduled=True)

        except Exception as e:
            return f"An error occurred: {e}. Please check inputs and try again."

    return render_template("index.html", scheduled_messages=scheduled_messages)

@app.route("/edit/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    if request.method == "POST":
        # Get the updated message details
        country_code = request.form.get("country_code")
        phone_number = request.form.get("number")
        message = request.form.get("message")
        date = request.form.get("date")
        hour = int(request.form.get("hour"))
        minute = int(request.form.get("minute"))

        full_number = country_code + phone_number
        message_time = datetime.strptime(f"{date} {hour}:{minute}", "%Y-%m-%d %H:%M")
        delay = (message_time - datetime.now()).total_seconds()

        # Update the scheduled message
        for msg in scheduled_messages:
            if msg['id'] == message_id:
                msg['number'] = full_number
                msg['text'] = message
                msg['hour'] = hour
                msg['minute'] = minute
                msg['delay'] = delay
                return redirect(url_for("home"))  # Redirect to home to see updated messages

        return "Message not found."

    # Find the message to edit
    message_to_edit = next((msg for msg in scheduled_messages if msg['id'] == message_id), None)
    return render_template("edit_message.html", message=message_to_edit)

if __name__ == "__main__":
    app.run(debug=True)
