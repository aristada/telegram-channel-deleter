from telethon.sync import TelegramClient, events
from tqdm.asyncio import tqdm
from dotenv import load_dotenv
import os


load_dotenv()

client = TelegramClient(
    os.getenv("SESSION_NAME"),
    os.getenv("API_ID"),
    os.getenv("API_HASH"),
)

async def main():
    channel_to_parse = input("Enter the channel username: ")

    # get user confirmation
    print(f"Are you sure you want to delete all messages in {channel_to_parse}?")
    print("This action is irreversible.")
    confirm = input("Type 'yes' to confirm: ")
    if confirm != "yes":
        print("Exiting...")
        return

    last_id = (await client.get_messages(channel_to_parse))[0].id
    async for message in tqdm(client.iter_messages(channel_to_parse), total=last_id):
        try:
            await message.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")
        
        
            
        
    
        

with client:
    client.loop.run_until_complete(main())