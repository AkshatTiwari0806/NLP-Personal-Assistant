import openai

openai.api_key = "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"

responses = []
while True:
    user_input = input("You: ")  # Prompt the user to enter their message
    user_message = {"role": "user", "content": user_input}  # Create the user message

    # Define the system messages and user message
    base_messages = [
        {"role": "system", "content": "You are a helpful assistant built to generate legal documents template in detailed simpler terms for users."},
        {"role": "system", "content": "You're trained on white collar jobs like company management, lawyers, accountants, financial and insurance jobs, consultants, and computer programmers"},
        user_message  # Include the user's message in the messages list
    ]

    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=base_messages + responses
    )

    response = chat_completion.choices[0].message.content
    print(f"AI: {response}\n")

    responses.append({
        "role": "assistant",
        "content": response
    })

    # Optionally, you can add a condition to exit the loop
    if user_input.lower() == "exit":
        break
