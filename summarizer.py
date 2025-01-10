import requests
from bs4 import BeautifulSoup
from IPython.display import display, Markdown
from openai import OpenAI

openai = OpenAI()

class Website:
    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title.string if soup.title else "No title"
        for irrelevant in soup(["script", "style", "img", "input"]):
            irrelevant.decompose()

        self.text = soup.get_text()

ed = Website("https://www.youtube.com/")

system_prompt = "You are an AI summarizing a webpage in max 250 words and analyze the content of the page and provides a short summary, ignoring text that might be negative related. Respond in markdown format."

def user_prompt_for(website):
    user_prompt = f"Summarize the content of the webpage: {website.title}"
    user_prompt += "\nthe contents of the webpage as follows; \
        please provide a summary of the content of the page in markdown. \
        if it is a long article, you can provide a summary of the main points."

    user_prompt += website.text
    return user_prompt

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

def summarize(website):
    website = Website(website)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_for(website)
    )

    return  response.choices[0].message.content

def display_summary(website):
    summary = summarize(website)
    print(summary)

display_summary("https://cnn.com")