import asyncio
import AutoKrs  # Import your AutoKrs module here

# Initialize an empty list to store KRS values
KRS_list = []

# Collect KRS values from user input
while True:
    KRS = input("Enter a KRS value (or press Enter to finish): ")
    if not KRS:
        break
    KRS_list.append(KRS)

async def run_main(KRS):
    await AutoKrs.main(KRS)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    for KRS in KRS_list:
        loop.run_until_complete(run_main(KRS))
