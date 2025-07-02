import openai

openai.api_key = 'API-KEY'
file = r"chat_history.txt"


def write_to_history(file, role, content):
    f = open(file, "a")
    f.write(f"{role}:{content}\n")
    f.close()


def read_history(file):
    res = []
    with open(file, "r") as f:
        for line in f:
            content_type = line.split(':')[0] #prompt/response
            content = line.split(':')[1].rstrip("\n")
            user_or_assistant = "user" if content_type == "prompt" else "assistant"
            d = {"role": user_or_assistant, "content": content}
            res.append(d)
    return res


def get_completion(prompt, model="gpt-4o-mini"):
    #update message history with latest prompt
    write_to_history(file, "user", prompt)
    messages = read_history(file)

    #fetch response
    response = openai.ChatCompletion.create(model=model, messages=messages, temperature=0)
    answer = response.choices[0].message["content"]

    #write latest response to chat history file
    write_to_history(file, "assistant", answer.replace("\n", " "))

    return answer


while True:
    print(get_completion(input("Enter your question: ")))
