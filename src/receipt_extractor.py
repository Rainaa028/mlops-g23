import json, os, re
from pathlib import Path
import lmstudio as lms

IMAGE = Path("data/raw/nota-sample.png")
MODEL = os.environ["LM_STUDIO_MODEL"]

# Siapkan gambar untuk VLM
image = lms.prepare_image(str(IMAGE))
model = lms.llm(MODEL)
chat = lms.Chat()

chat.add_user_message(
    "Baca nota. Ekstrak merchant, tanggal, item, subtotal, pajak, dan total. "
    "Keluarkan JSON valid. Jika pajak tidak terlihat, isi 0. Jangan mengarang.",
    images=[image],
)

prediction = model.respond(chat)
content = prediction.content.strip()

# Bersihkan wrapper markdown ```json ... ``` jika ada
if "```" in content:
    content = re.sub(r"^```(?:json)?\s*", "", content, flags=re.MULTILINE)
    content = re.sub(r"\s*```$", "", content, flags=re.MULTILINE)

result = json.loads(content.strip())

# Simpan hasil ke folder reports
Path("reports/receipt.json").write_text(
    json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
)

print(json.dumps(result, indent=2, ensure_ascii=False))
