import json
import os

SERVER_DATA_FOLDER = 'server_data/'

os.makedirs(SERVER_DATA_FOLDER, exist_ok=True)

async def save_server_data(guild_id: int, team_name: str, message_id: int, channel_id: int, role_id: int, category_id: int):
    server_file = os.path.join(SERVER_DATA_FOLDER, f"server_data_{guild_id}.json")

    server_data = load_server_data(guild_id)

    server_data[team_name] = {
    "role_id": role_id,
    "category_id": category_id,
    "interaction_message": {
        "message_id": message_id,
        "channel_id": channel_id
    }
}

    with open(server_file, 'w') as f:
        json.dump(server_data, f, indent=4)

def load_server_data(guild_id: int):
    server_file = os.path.join(SERVER_DATA_FOLDER, f"server_data_{guild_id}.json")
    
    try:
        with open(server_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

async def delete_server_data(guild_id, team_name):
    # Load existing server data
    server_data = load_server_data(guild_id)
    
    if team_name in server_data:
        team_data = server_data.pop(team_name)  
        role_id = team_data["role_id"]
        category_id = team_data["category_id"]
        message_id = team_data["interaction_message"]["message_id"]
        channel_id = team_data["interaction_message"]["channel_id"]

        await save_server_data(guild_id, team_name, message_id, channel_id, role_id, category_id)