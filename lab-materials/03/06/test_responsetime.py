from llm_usage import infer_with_template
import requests
import json
import time

max_response_time = 3

def send_request(endpoint):
    response = requests.get(endpoint)
    return response

def test_responsetime():
    TEMPLATE = """
あなたは、親切で、礼儀正しく、正直なアシスタントです。
常に気配りと尊重をもって接し、真摯にサポートします。できる限り有用な返答を提供しますが、安全を確保します。
有害で、倫理に反する、偏見のある、または否定的な内容は避けます。返答が公正でポジティブなものであることを確認します。
提供された質問に対し、自信に満ちた態度で30文字以内で答えて下さい。

### 質問:
{silly_question}

### 回答:
"""
    
    start = time.perf_counter()
    response = infer_with_template("Who saw a saw saw a salsa?", TEMPLATE)
    response_time = time.perf_counter() - start

    if response_time>max_response_time:
        raise Exception(f"Response took {response_time} which is greater than {max_response_time}")

    print(f"Response time was OK at {response_time} seconds")

    with open("responsetime_result.json", "w") as f:
        json.dump({
            "response_time": response_time
        }, f)

if __name__ == '__main__':
    test_responsetime()