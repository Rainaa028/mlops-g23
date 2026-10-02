import os
from openai import OpenAI

client = OpenAI(
    base_url=os.getenv("LM_STUDIO_URL", "http://127.0.0.1:1234/v1"),
    api_key="lm-studio"
)

prompt = "Jawab JSON dengan kunci summary, priority, reason, missing_info. Tiket: Pembayaran gagal dan saldo terpotong."
resp = client.chat.completions.create(
    model=os.environ["LM_STUDIO_MODEL"],
    messages=[{"role": "user", "content": prompt}],
)
print(resp.choices[0].message.content)
