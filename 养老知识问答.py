from http import HTTPStatus
from dashscope import Application
import os
import re

user_question = input("Ask a question or provide a prompt for a recipe: ")
def call_agent_app():
    response = Application.call(app_id='36bec8a1536540f29c11166a553f8ffc',
                                prompt=user_question,
                                api_key=os.getenv("DASHSCOPE_API_KEY"),

                                )
    # if response.status_code != HTTPStatus.OK:
    #     print('request_id=%s, code=%s, message=%s\n' % (response.request_id, response.status_code, response.message))
    # else:
    #     print('request_id=%s\n output=%s\n usage=%s\n' % (response.request_id, response.output, response.usage))

    cleaned_text = re.sub(r'<ref>\[.*?\]</ref>', '', response.output.text)
    print(cleaned_text)
    # print(response.output.text)
    # print(response.output.doc_references)


if __name__ == '__main__':
    call_agent_app()