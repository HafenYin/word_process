import requests
import json


def ai_response(api_key: str, url: str, model: str, system_prompt: str, user_input: str, temperature=0.6):
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "temperature": temperature
    }

    response = requests.post(
        url=url,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        data=json.dumps(data)
    )

    return response


if __name__ == '__main__':
    response = ai_response(
        '',
        url='http://43.134.8.116:9090/v1/chat/completions',
        model="glm-4-flash",
        system_prompt='介绍一下你自己',
        user_input='你是谁，你是谁开发的'
    )

    if response.status_code == 200:
        print(response.json())
        reply = response.json()['choices'][0]['message']['content']
        print("AI：", reply)
    else:
        print("请求失败，状态码：", response.status_code)
        print("错误信息：", response.text)
