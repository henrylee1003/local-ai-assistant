import urllib.request
import json

def ask_ollama(prompt):
    url = "http://ollama:11434/api/generate"
    data = json.dumps({
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }).encode()

    req = urllib.request.Request(url, data=data,
          headers={"Content-Type": "application/json"})

    with urllib.request.urlopen(req) as res:
        result = json.loads(res.read())
        return result["response"]

print("問 AI：台灣最高的山是哪座？")
print(ask_ollama("台灣最高的山是哪座？用繁體中文回答。"))
