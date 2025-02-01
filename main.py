from telethon.sync import TelegramClient, events
from tqdm.asyncio import tqdm
from dotenv import load_dotenv
from os import getenv
from re import match
load_dotenv()
DATA = [getenv("SESSION_NAME"), getenv("API_ID"), getenv("API_HASH")]
if all(x is None for x in DATA):
    raise Exception("Specify the Telegram credentials in .env!")
session, api_id, api_hash = DATA
client = TelegramClient(
    session,
    api_id,
    api_hash,
)
prompt_messages = ["Are you sure you want to delete all the messages in {}?", "The action is irreversible."]


def check_channel_valid(channel_username):
    return match(r"""^(?=(?:[0-9_]*[a-z]){3})[a-z0-9_]{5,}$""", channel_username)
async def main():
    channel_to_parse = input("Enter the channel username: ")
    if not check_channel_valid:
        raise Exception("Unexpected error. Enter the valid channel username")
    for prompt in prompt_messages:
        print(prompt.format(channel_to_parse) if '{}' in prompt else prompt)
    confirm = input("Type 'yes' to confirm: ")
    if confirm.lower() != "yes":
        print("Exiting...")
        return

    last_id = (await client.get_messages(channel_to_parse))[0].id
    async for message in tqdm(client.iter_messages(channel_to_parse), total=last_id):
        try:
            await message.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")
            return None

with client:
    client.loop.run_until_complete(main())
# if anything use asyncio.run(main())
