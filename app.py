from flask import Flask, render_template, request, redirect, url_for
import pywhatkit as kit

app = Flask(__name__)

def is_valid_number(number):
    """Ensures the number contains only digits and is the right length."""
    return number.isdigit() and 7 <= len(number) <= 15

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get form data
        country_code = request.form.get("country_code")
        phone_number = request.form.get("number")
        message = request.form.get("message")
        hour = int(request.form.get("hour"))
        minute = int(request.form.get("minute"))

        # Combine country code and phone number
        full_number = country_code + phone_number

        # Validate phone number
        if not is_valid_number(phone_number):
            return "Invalid phone number format. Please enter digits only and exclude the leading zero."

        # Send WhatsApp message using pywhatkit
        try:
            kit.sendwhatmsg(full_number, message, hour, minute)
            return redirect(url_for("success"))
        except Exception as e:
            return f"An error occurred: {e}"

    return render_template("index.html")

@app.route("/success")
def success():
    return "Message scheduled successfully!"

if __name__ == "__main__":
    app.run(debug=True)
