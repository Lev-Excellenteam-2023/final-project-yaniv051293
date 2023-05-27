import time
import openai
from openai import APIError

conversation = []
conversation.append(
    {"role": "system", "content": f"you are a helpful AI that is explaining a PowerPoint presentation."})
openai.api_key = "sk-"# enter your key
max_retries = 3
retry_delay = 20  # Delay in seconds between retries


def explain_page(page: str):
    request = "Give me a brief explanation of this page, " \
              "Write the explanation as a short paragraph from an article:\n" + page
    return send_gpt_request(request)


def send_gpt_request(user_message:str)->str:
    conversation.append({"role": "user", "content": user_message})
    for retry in range(max_retries):
        try:
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation)
            assistant_reply = response['choices'][0]['message']['content']
            conversation.append({"role": "assistant", "content": assistant_reply})
            return assistant_reply
        except APIError as e:
            error_message = e.message
            # Handle the exception, e.g., log the error or display an error message
            print(f"API Error: {error_message}")
            print(f"Retrying... (attempt {retry+1}/{max_retries})")
            time.sleep(retry_delay)

    # If maximum retries reached without success, handle the failure
    print("Request failed after maximum retries")
    # Perform any necessary actions, such as displaying an error message or terminating the program
