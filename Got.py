import google.generativeai as genai

API_KEY = "AIzaSyBKkhLmuAuyYt14v4fnb9B78QEHz7T59cQ"

genai.configure(api_key=API_KEY)

print("Chat with Gemini! Type 'exit' to quit.")

model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    response = chat.send_message(user_input)
    print("Gemini:", response.text)