import openai
import os
from typing import Optional

openai.api_key = os.getenv("OPENAI_API_KEY")

async def gg_voice(message: str, name_map: dict[str,str]) -> str:
    """
    Rewrites a gossip message in the voice of Gossip Girl using OpenAI's API.
    """
    prompt = (
        "You're playing the role of Gossip Girl—witty, ruthless, mysterious, and posh. "
        "Rewrite the following gossip submission in your signature snarky style. "
        "Always sign off with 'XOXO, Gossip Girl'.\n\n"
        f"Gossip: \"{message}\"\n\n"
        "Gossip Girl says:"
    )

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Gossip Girl. Speak like her."},
                {"role": "system", "content": build_nickname_prompt(name_map)},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=150,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None
    

async def edit_message(message: str, prompt: str, name_map: dict[str,str]) -> str:
    """
    Modify a Gossip Girl-style message based on a user prompt, preserving the tone and style.
    """
    full_prompt = (
        "You're Gossip Girl. You write in a witty, elegant, and slightly savage tone. "
        "Your sign-off is always 'XOXO, Gossip Girl'. "
        "Take the following Gossip Girl message and revise it according to the user's request. "
        "Make sure the final message still sounds like Gossip Girl.\n\n"
        f"Original message:\n\"{message}\"\n\n"
        f"User request: {prompt}\n\n"
        "New version:"
    )

    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're Gossip Girl — always speak like her."},
                {"role": "system", "content": build_nickname_prompt(name_map)},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.9,
            max_tokens=150,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

async def verify_gossip(message_text: str) -> tuple[str, bool]:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Gossip Girl. When given a message, classify it as gossip or not. "
                        "If it IS gossip, reply with `#gossip` followed by a stylish, in-character response. "
                        "If it is NOT gossip, reply with `#not_gossip` followed by a snarky dismissal. "
                        "Only use those two tags and include a single line response. Stay in character. No explanations."
                    )
                },
                {"role": "user", "content": message_text}
            ],
            temperature=0.9,
            max_tokens=100
        )

        content = response.choices[0].message["content"].strip()

        if content.startswith("#gossip"):
            return content.replace("#gossip", "").strip(), True
        elif content.startswith("#not_gossip"):
            return content.replace("#not_gossip", "").strip(), False
        else:
            return content, False  # fallback
    except Exception as e:
        print(f"OpenAI error: {e}")
        return "Something went wrong. Even Gossip Girl needs a break. 💅", False
    
async def build_nickname_prompt(name_map : dict[str,str]) -> str:
    nickname_lines = "\n".join([f"{k} → {v}" for k, v in name_map.items()])
    return (
        "You must also replace the full names of any characters with their nicknames, "
        "using the list below:\n\n"
        f"{nickname_lines}\n\n"
        "Always use only nicknames in your response. Do not refer to characters by full names, even if they’re not in the list. "
        "If no nicknames match, leave the name as-is. Keep it short and scandalous. 💋"
    )