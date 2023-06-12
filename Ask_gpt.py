import openai
import aiohttp

conversation = [{"role": "system", "content": f"you are a helpful AI that is explaining a PowerPoint presentation."}]
openai.api_key = "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"  # enter your key


async def send_gpt_request(user_message: str):
    """
    Sends a request to the GPT-3.5-turbo model for generating text based on a user message.

    :param user_message: The message from the user to be used as a prompt for text generation.
    :return: A dictionary containing the response from the GPT-3.5-turbo model.
    """
    # Set engine and parameters
    engine = "gpt-3.5-turbo"
    max_tokens = 512

    # Generate text from prompt asynchronously
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            "https://api.openai.com/v1/chat/completions",  # Updated endpoint URL
            headers={
                "Authorization": f"Bearer {openai.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "messages": [{"role": "system", "content": "You are a helpful assistant."},
                             {"role": "user", "content": user_message}],
                "max_tokens": max_tokens,
                "model": engine  # Add the model parameter
            }
        )
        return await response.json()

