from db.crud import get_db
nickname_map: dict[str, str] = {}

async def get_nickname_map(force_reload: bool = False) -> dict[str, str]:
    global nickname_map
    if nickname_map and not force_reload:
        return nickname_map

    characters = (await get_db()).Characters.ListAll()
    nickname_map = {
        character.display_name: character.nickname
        for character in characters
        if character.display_name and character.nickname
    }

    return nickname_map
