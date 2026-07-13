import urllib.request
import json
import datetime

def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate(expression):
    try:
        return str(eval(expression))
    except:
        return "計算錯誤"

TOOLS_DESCRIPTION = """
你有以下工具可以使用：
- get_time: 取得目前時間，不需要輸入值
- calculate: 計算數學式，輸入數學表達式如 "2+2" 或 "100*0.8"

規則：
1. 只有在「真的需要」查時間或算數學時才使用工具。
2. 如果要使用工具，你的回應必須「只有」這兩行，不要加任何其他文字：
TOOL: tool_name
INPUT: input_value
3. 如果不需要工具（例如常識問題），直接用自然語言回答，絕對不要提到 TOOL 這個字。

範例：
問：現在幾點？
答：
TOOL: get_time
INPUT: None

問：台灣的首都是哪裡？
答：台灣的首都是台北。
"""

def call_ollama(messages, temperature=0):
    url = "http://ollama:11434/api/chat"
    data = json.dumps({
        "model": "llama3.2",
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature}
    }).encode()

    req = urllib.request.Request(url, data=data,
          headers={"Content-Type": "application/json"})

    with urllib.request.urlopen(req) as res:
        result = json.loads(res.read())
        return result["message"]["content"]

def run_agent(user_input):
    print(f"\n用戶：{user_input}")
    messages = [
        {"role": "system", "content": TOOLS_DESCRIPTION},
        {"role": "user", "content": user_input}
    ]
    response = call_ollama(messages)
    print(f"Agent 思考：{response}")

    first_line = response.strip().split("\n")[0]

    if first_line.startswith("TOOL:"):
        lines = response.split("\n")
        tool_name = ""
        tool_input = ""
        for line in lines:
            if line.startswith("TOOL:"):
                tool_name = line.replace("TOOL:", "").strip()
            if line.startswith("INPUT:"):
                tool_input = line.replace("INPUT:", "").strip()

        # 關鍵新增：去掉頭尾可能出現的引號（單引號或雙引號）
        tool_input = tool_input.strip('"').strip("'")

        if tool_name == "get_time":
            tool_result = get_current_time()
        elif tool_name == "calculate":
            tool_result = calculate(tool_input)
        else:
            tool_result = "找不到這個工具"

        print(f"工具執行：{tool_name}({tool_input}) = {tool_result}")

        messages.append({"role": "assistant", "content": response})
        messages.append({"role": "user",
            "content": f"工具已經執行完畢，結果是：{tool_result}。"
                       f"請直接告訴用戶答案是「{tool_result}」，"
                       f"不要自己重新計算或修改這個數字。"})
        final_response = call_ollama(messages)
        print(f"最終答案：{final_response}")
    else:
        print(f"最終答案：{response}")

run_agent("現在幾點？")
run_agent("1234 乘以 5678 是多少？")
run_agent("台灣的首都是哪裡？")