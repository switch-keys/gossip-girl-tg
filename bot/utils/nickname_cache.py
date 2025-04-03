from db.crud import get_db
nickname_map: dict[str,dict[str, str]] = {}

async def get_nickname_map(force_reload: bool = False) -> dict[str, dict[str, str]]:
    global nickname_map
    if nickname_map and not force_reload:
        return nickname_map
    async with get_db() as db:
        characters = await db.Characters.ListAll()
        nickname_map = {
            character.display_name: {
                "nickname": character.nickname,
                "pronouns": character.pronouns.value
            }
            for character in characters
            if character.display_name and character.nickname
        }

    return nickname_map
