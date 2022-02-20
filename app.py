import discord
from discord.ext import commands
from instagrapi import Client
import os

FolderToClear = "photos"
for filename in os.listdir(FolderToClear):
    file_path = os.path.join(FolderToClear, filename)
    os.remove(file_path)

DiscordToken = "REDACTED"
Intents = discord.Intents(messages=True, members=True, guilds=True)
DiscordClient = commands.Bot(command_prefix="~", intents=Intents)
DiscordClient.remove_command('help')

@DiscordClient.event
async def on_ready():
    await DiscordClient.change_presence(activity=discord.Game(name='made by oskar#1000'))
    print("Up and running!")

@DiscordClient.command()
async def post(Ctx, *, Caption: str):
    Guild = await DiscordClient.fetch_guild(944800674099650570)
    Role = Guild.get_role(944855822662508555)

    if Role in Ctx.author.roles:
        AttachmentPath = None
        InstagramClient = None

        MessageContent = f"💦 Initiating content post with caption `{Caption}`."
        Message = await Ctx.reply(MessageContent)
        MessageContent = MessageContent + "\n🧠 Logging into Instagram..."
        await Message.edit(content = MessageContent)
        try:
            InstagramClient = Client()
            InstagramClient.login("blancheofsaintandre", "REDACTED")
            MessageContent = MessageContent + "\n✅ Logged into Instagram!"
            await Message.edit(content = MessageContent)
        except Exception as e:
            MessageContent = MessageContent + f"\n:x: Login failed!\nError message:\n```fix\n{e}\n```"
            await Message.edit(content = MessageContent)
            return

        MessageContent = MessageContent + "\n🖼 Saving image..."
        await Message.edit(content = MessageContent)

        try:
            Attachment = Ctx.message.attachments[0]
            AttachmentPath = "photos/" + Attachment.filename
            await Attachment.save(AttachmentPath)
            MessageContent = MessageContent + f"\n✅ Saved image as `{AttachmentPath}`!"
            await Message.edit(content = MessageContent)
        except Exception as e:
            MessageContent = MessageContent + f"\n:x: Image save failed!\nError message:\n```fix\n{e}\n```"
            await Message.edit(content = MessageContent)
            return

        MessageContent = MessageContent + "\n#️⃣ Attempting to post with hashtags..."
        await Message.edit(content = MessageContent)

        try:
            NewCaption = f"{Caption}\n\n#blanche #blancheofsaintandre #blanche1k\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.#psychic #love #tarot #psychicreading #spiritual #tarotcards #twinflame #spirituality #psychicreadings #meditation #healing #astrology #crystals #tarotreading #lovespells #spiritualawakening #psychicmedium #soulmate #chakra #witch #medium #tarotreader #chakras #psychicreader #lightworker"
            Posted = InstagramClient.photo_upload(AttachmentPath, NewCaption)
            Code = Posted.dict()["code"]
            MessageContent = MessageContent + f"\n✅ Image was successfully posted!\nhttps://instagram.com/p/{Code}\n:point_right: Prompt ended."
            await Message.edit(content = MessageContent)
        except Exception as e:
            MessageContent = MessageContent + f"\n:x: Post failed!\nError message:\n```fix\n{e}\n```\nMake sure that the image uploaded was originally saved to your computer, not copy/pasted."
            await Message.edit(content = MessageContent)
            return

    else:
        Message = await Ctx.reply(":x: Not authorized!")
    

DiscordClient.run(DiscordToken)
