from openai import OpenAI
import os
user_question = input("Ask a question or provide a prompt for a recipe: ")
def get_response():
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"), # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
    )
    completion = client.chat.completions.create(
        model="qwen-max",
        messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                  {'role': 'user', 'content': user_question}]
        )
    # print(completion.model_dump_json())
    print(f"回复内容：{completion.choices[0].message.content}")

if __name__ == '__main__':
    get_response()