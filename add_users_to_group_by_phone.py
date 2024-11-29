from telethon import TelegramClient
from telethon.tl.functions.contacts import AddContactRequest
from telethon.tl.functions.messages import AddChatUserRequest

# Replace with your own API ID and API Hash
api_id = 'YOUR_API_ID'  # Your API ID
api_hash = 'YOUR_API_HASH'  # Your API Hash
group_id = 'YOUR_GROUP_ID'  # Your group ID (can be fetched by username or chat ID)

# Read phone numbers from the text file
with open('phone_numbers.txt', 'r') as file:
    phone_numbers = [line.strip() for line in file.readlines()]

# Create the client session
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Start the client
    await client.start()

    # Get the group entity (by username or chat ID)
    group_entity = await client.get_entity(group_id)

    # Loop through the list of phone numbers
    for phone_number in phone_numbers:
        try:
            # Add contact by phone number
            contact = await client(AddContactRequest(
                phone_number=phone_number,  # Phone number to add
                first_name="New",           # You can provide a first name
                last_name="Contact"         # You can provide a last name
            ))

            # Now you can get the contact's user ID
            user_entity = await client.get_entity(contact.user)

            # Add user to the group
            await client(AddChatUserRequest(
                chat_id=group_entity.id,  # The group ID
                user_id=user_entity.id,   # The user ID
                fwd_limit=10               # Optional: limits forwarded messages (default: 10)
            ))
            print(f"Successfully added {phone_number} to the group!")

        except Exception as e:
            print(f"Failed to add {phone_number}: {e}")

    # Disconnect after completing the operation
    await client.disconnect()

# Run the script
import asyncio
asyncio.run(main())
