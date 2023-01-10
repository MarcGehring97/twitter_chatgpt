import openai

openai.api_key = "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"

def chatgpt(prompt):
    # Generate a response
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    return response