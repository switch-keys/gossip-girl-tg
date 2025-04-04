from openai import AsyncOpenAI
import os
from typing import Optional

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def gg_voice(message: str, name_map: dict[str,str]) -> str:
    """
    Rewrites a gossip message in the voice of Gossip Girl using OpenAI's API.
    """
    prompt = (
        "You're playing the role of Gossip Girl—witty, ruthless, dramatic, mysterious, and posh. "
        "Rewrite the following gossip submission in your signature snarky style and don't be afraid to add some fluff, but don't make the message too long. "
        "Make sure that the content of the gossip submission can still be very obviously and explicitly understood from your rewritten response. Do not make it too cryptic."
        "Make your response X-rated if the content of the gossip is. Sex, drugs, and cursing are all OK. "
        "Refer to the Upper East Side as the Upper West Side instead. "
        "Always sign off with 'XOXO, Gossip Girl'.\n\n"
        f"{build_nickname_prompt(name_map)}"
        f"Gossip: \"{message}\"\n\n"
        "Gossip Girl says:"
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are Gossip Girl. Speak like her."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.95,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None
    
async def gg_snark(gg_message: str, user_reply: str) -> str:
    try:
        prompt = (
            "You're playing Gossip Girl: witty, ruthless, snarky, and posh.\n\n"
            "Someone just replied to one of your iconic blasts in the group chat.\n"
            "Your job is to respond with a sharp, snarky comment — a roast that drips with class and venom.\n\n"
            "Make your response X-rated if the reply demands it. Sex, drugs, and cursing are all OK. "
            "Refer to the Upper East Side as the Upper West Side instead. "
            f"Gossip Girl’s original message:\n\"{gg_message}\"\n\n"
            f"Their reply:\n\"{user_reply}\"\n\n"
            "Your comeback:"
        )

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.95,
            max_tokens=100
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[Snark Error] {e}")
        return None

async def edit_message(message: str, prompt: str, name_map: dict[str,str]) -> str:
    """
    Modify a Gossip Girl-style message based on a user prompt, preserving the tone and style.
    """
    full_prompt = (
        "You're Gossip Girl. You write in a witty, elegant, and slightly savage tone. "
        "Your sign-off is always 'XOXO, Gossip Girl'. "
        "Take the following Gossip Girl message and revise it according to the user's request. "
        "Make sure that the content of the gossip submission can still be very obviously and explicitly understood from your rewritten response. Do not make it too cryptic. "
        "Make your response X-rated if the content of the gossip is that way. Sex, drugs, and cursing are all OK. "
        "Refer to the Upper East Side as the Upper West Side instead. "
        "Make sure the final message still sounds like Gossip Girl.\n\n"
        f"{build_nickname_prompt(name_map)}"
        f"Original message:\n\"{message}\"\n\n"
        f"User request: {prompt}\n\n"
        "New version:"
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You're Gossip Girl — always speak like her."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.95,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

async def verify_gossip(message_text: str, name_map: dict[str,str]) -> tuple[str, bool]:
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Gossip Girl. When given a message, classify it as gossip or not. "
                        "If it IS gossip, reply with `#gossip` followed by a stylish, in-character response. "
                        "The gossip is not about the person who sent it, so refer to the people as such."
                        "If it is NOT gossip, reply with `#not_gossip` followed by a snarky dismissal. "
                        "Only use those two tags and include a single line response. Stay in character. No explanations."
                        "Refer to the Upper East Side as the Upper West Side instead. "
                        f"{build_nickname_prompt(name_map)}"
                    )
                },
                {"role": "user", "content": message_text}
            ],
            temperature=0.9,
            max_tokens=100
        )

        content = response.choices[0].message.content.strip()

        if content.startswith("#gossip"):
            return content.replace("#gossip", "").strip(), True
        elif content.startswith("#not_gossip"):
            return content.replace("#not_gossip", "").strip(), False
        else:
            return content, False  # fallback
    except Exception as e:
        print(f"OpenAI error: {e}")
        return "Something went wrong. Even Gossip Girl needs a break. 💅", False
    
def build_nickname_prompt(name_map : dict[str,dict[str,str]]) -> str:
    nickname_lines = "\n".join([f'{display_name} → "{info["nickname"]}" ({info["pronouns"]})' 
                                for display_name, info in name_map.items()])
    return (
        "You must also replace the full names of any characters with their nicknames and use the correct pronouns when referring to them, "
        "using the list below:\n\n"
        f"{nickname_lines}\n\n"
        "Always use only the nicknames in your response. Do not refer to characters by full names, even if they’re not in the list. "
        "If no nicknames match, leave the name as-is. Keep it short and scandalous. 💋"
        "If you can't match the pronouns then use they/them. "
    )