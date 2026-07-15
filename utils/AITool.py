from openai import OpenAI
from utils.EnvironTool import config

class AIHandler:
    def __init__(self, sysprompt: str) -> None:
        self.client = OpenAI(
            api_key=config.get("API_KEY", ""),
            base_url=config.get("API_HOST", ""),
            # config for cloudflare
            default_headers={
                "User-Agent": "curl/8.0.0",
            }
        )
        self.sysprompt = sysprompt
    def send_request(self, text, history=[]):
        messages=[
            {"role": "system", "content": self.sysprompt},
            *history,
            {"role": "user", "content": f"标记内是用户输入。\n<start>{text}<end>"},
        ]
        response = self.client.chat.completions.create(
            model=config.get("MODEL_NAME", ""),
            messages=messages
        )
        return response.choices[0].message.content, messages
