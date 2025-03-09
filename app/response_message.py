from linebot.v3.messaging import TextMessage
from linebot.v3.webhooks import MessageEvent
import requests
import emoji
import random 

# def response_message(event):
#     print(event)
#     return TextMessage(text="Hello ja")


DICTIONARY_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

# กำหนด emoji สำหรับแต่ละประเภทของคำ
emoji_dict = {
    "Word": ["📖", "🔤", "📝"],
    "noun": ["📦", "📚", "📜"],
    "verb": ["🚀", "🏃", "💪"],
    "adjective": ["🌟", "✨", "🔥"],
    "adverb": ["🎯", "📢", "🚀"],
    "other": ["🔹", "🔸", "⚡"]  # สำหรับประเภทที่ไม่รู้จัก
}

def get_definition(word):
    response = requests.get(f"{DICTIONARY_API_URL}{word}")
    
    if response.status_code == 200:
        data = response.json()
        
        # ใช้ dict เพื่อเก็บ definitions ตามประเภทของคำ
        definitions_by_pos = {}

        # วนลูปดึงข้อมูลของคำ
        for meaning in data[0]["meanings"]:
            part_of_speech = meaning["partOfSpeech"]  # เช่น "noun", "verb"

            # ตรวจสอบว่ามี part_of_speech นี้ใน dict หรือยัง
            if part_of_speech not in definitions_by_pos:
                definitions_by_pos[part_of_speech] = []  # ถ้ายังไม่มี ให้สร้าง list ใหม่
            
            # วนลูปดึง definitions ทั้งหมด
            for definition_data in meaning["definitions"]:
                definition = definition_data["definition"]  # ดึง definition
                
                # ตรวจสอบว่ามี synonyms หรือไม่
                synonyms = definition_data.get("synonyms", [])  # ดึง synonyms ถ้ามี
                
                # สร้างข้อความแสดงผลของ definition
                if synonyms:
                    definition_text = f"{definition} (Synonyms: {', '.join(synonyms)})"
                else:
                    definition_text = definition
                
                # เพิ่ม definition เข้า list ของ part_of_speech นั้น
                definitions_by_pos[part_of_speech].append(definition_text)

        # สร้างข้อความผลลัพธ์ โดยเพิ่ม emoji
        result_text = f"Word {random.choice(emoji_dict['Word'])}: {word}\n"
        for pos, defs in definitions_by_pos.items():
            emoji_for_pos = random.choice(emoji_dict.get(pos, emoji_dict["other"]))
            result_text += f"\n{pos.capitalize()} {emoji_for_pos}:\n- " + "\n- ".join(defs)

        return TextMessage(text=result_text)
    
    return TextMessage(text="Word not found")

