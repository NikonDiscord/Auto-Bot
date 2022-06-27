# coging
import disnake
import json
import asyncio
import aiohttp

from other import print1 as print
from disnake.ext import commands

client = commands.Bot(
    intents=disnake.Intents.all(),
    help_command=None,
    test_guilds=json.load(open("cfg.json"))['guild_id']
)


@client.event
async def on_ready():
    print("AutoMod ready to work.")
    await client.change_presence(
        status=disnake.Status.dnd,
        activity=disnake.Game("PING = BAN")
    )


def find_element_in_list(element, list_element):
    try:
        index_element = list_element.index(element)
        return index_element
    except ValueError:
        return None


@client.event
async def on_message(message):
    config = json.load(open("cfg.json"))
    match config['ban']:
        case True:
            if message.author.id in config['admins']:
                if "ban" in message.content.lower().split(" "):
                    embed1 = disnake.Embed()
                    embed1.title = "you are in the ban"
                    embed1.description = f"""never ping anyone for no reason!!!"""
                    embed1.color = 0xFF0000
                    msg = await message.channel.fetch_message(message.reference.message_id)
                    await msg.reply("<:angry_ping:973979129676455966> RIGHT NOW YOU WILL GO TO THE BAN!!!!")
                    await asyncio.sleep(3)
                    try:
                        await msg.author.send(embed=embed1)
                    except:
                        pass
                    await msg.author.ban(reason="пинганул админа", delete_message_days=0)
        case False: pass
    match config['echo']:
        case True:
            if message.channel.id in config['channels']:
                if message.author.id in config['admins']:
                    ref_embed = None
                    if message.reference:
                        ref_msg = await message.channel.fetch_message(message.reference.message_id)
                        ref_embed = disnake.Embed(
                            title="Jump to message", url=ref_msg.jump_url, timestamp=ref_msg.created_at)
                        author_name = None
                        if ref_msg.author.nick:
                            author_name = ref_msg.author.nick + \
                                " (" + ref_msg.author.name + "#" + \
                                ref_msg.author.discriminator + ")"
                        else:
                            author_name = ref_msg.author.name + "#" + ref_msg.author.discriminator
                        ref_embed.set_author(name=author_name)
                        optimized_content = (
                            ref_msg.content[:2047] + "…") if len(ref_msg.content) > 2048 else ref_msg.content
                        ref_embed.description = optimized_content
                        avatar_url = None
                        if ref_msg.author.guild_avatar:
                            avatar_url = ref_msg.author.guild_avatar.url
                        elif ref_msg.author.avatar:
                            avatar_url = ref_msg.author.avatar.url
                        else:
                            avatar_url = ref_msg.author.default_avatar.url
                        ref_embed.set_thumbnail(url=avatar_url)
                        if ref_msg.attachments:
                            attachments = []
                            for attachment in ref_msg.attachments:
                                attachments.append({"name": attachment.filename, "url": attachment.proxy_url, "index": find_element_in_list(
                                    attachment, ref_msg.attachments)})
                            attachments_strings = []
                            for attachment in attachments:
                                attachments_strings.append(f"[Attachment {attachment['index']}]({attachment['url']})")
                            ref_embed.add_field(
                                name="Attachments", value=", ".join(attachments_strings))

                    await message.delete()
                    webhook_url = config['hooks'][str(message.channel.id)]
                    async with aiohttp.ClientSession() as session:
                        sel_hook = disnake.Webhook.from_url(
                            url=webhook_url, session=session)
                        username = message.author.nick if message.author.nick else message.author.name
                        avatar_url = None
                        if message.author.guild_avatar:
                            avatar_url = message.author.guild_avatar.url
                        elif message.author.avatar:
                            avatar_url = message.author.avatar.url
                        else:
                            avatar_url = message.author.default_avatar.url
                        files = []
                        for attachment in message.attachments:
                            attachment_size = round(
                                attachment.size / 1024 / 1024)
                            if attachment_size >= 8:
                                file = disnake.File(fp=open(
                                    "too_large_file.png", "rb"), filename=attachment.filename + ".png", spoiler=attachment.is_spoiler())
                            else:
                                file = await attachment.to_file()
                            files.append(file)
                        whook_msg = await sel_hook.send(
                            username=username,
                            avatar_url=avatar_url,
                            content=message.content,
                            files=files,
                            embed=ref_embed,
                            wait=True
                        )
                        messages_db = json.load(open("./messages.json", "r+"))
                        messages_db.update({whook_msg.id: message.author.id})
                        json.dump(messages_db, open("./messages.json", "w+"))
        case False: pass


@client.slash_command(
    name="echo",
    options=[
        disnake.Option(name="turn", required=True, choices=[
                       disnake.OptionChoice("on", "1"), disnake.OptionChoice("off", "0")])
    ],
    default_member_permissions=disnake.Permissions(8)
)
async def _echo(iter):
    choice = iter.options.get("turn")
    config = json.load(open("cfg.json"))
    match choice:
        case "1":
            config['echo'] = True
            json.dump(config, open("cfg.json", "w"), indent=4)
            await iter.send("echo_bot turned on.")
        case "0":
            config['echo'] = False
            json.dump(config, open("cfg.json", "w"), indent=4)
            await iter.send("echo_bot turned off.")


@client.slash_command(
    name="ban",
    options=[
        disnake.Option(name="turn", required=True, choices=[
                       disnake.OptionChoice("on", "1"), disnake.OptionChoice("off", "0")])
    ],
    default_member_permissions=disnake.Permissions(8)
)
async def _ban(iter):
    choice = iter.options.get("turn")
    config = json.load(open("cfg.json"))
    match choice:
        case "1":
            config['echo'] = True
            json.dump(config, open("cfg.json", "w"), indent=4)
            await iter.send("automod_ban turned on.")
        case "0":
            config['echo'] = False
            json.dump(config, open("cfg.json", "w"), indent=4)
            await iter.send("automod_ban turned off.")


@client.slash_command(
    name="addhook",
    options=[disnake.Option(
        name="channel", type=disnake.OptionType.channel, required=True)],
    default_member_permissions=disnake.Permissions(8)
)
async def _addhook(iter):
    channel = iter.options.get("channel")
    config = json.load(open("cfg.json"))
    try:
        whook = await channel.create_webhook(name="for automod")
        to_cfg = {channel.id: whook.url}
        config['hooks'].update(to_cfg)
        json.dump(config, open("cfg.json", "w"), indent=4)
        await iter.send("hook for " + channel.mention + " added to echo_bot.")
    except Exception as e:
        await iter.send(e)


@client.slash_command(
    name="addchannel",
    options=[disnake.Option(
        name="channel", type=disnake.OptionType.channel, required=True)],
    default_member_permissions=disnake.Permissions(8)
)
async def _addchannel(iter):
    channel = iter.options.get("channel")
    config = json.load(open("cfg.json"))
    config['channels'].append(channel.id)
    json.dump(config, open("cfg.json", "w"), indent=4)
    await iter.send(channel.mention + " added to echo_bot.")


@client.slash_command(
    name="addadmin",
    options=[disnake.Option(
        name="admin", type=disnake.OptionType.user, required=True)],
    default_member_permissions=disnake.Permissions(8)
)
async def _addadmin(iter):
    user = iter.options.get("admin")
    config = json.load(open("cfg.json"))
    config['admins'].append(user.id)
    json.dump(config, open("cfg.json", "w"), indent=4)
    await iter.send(user.mention + " added to echo_bot.")


@client.slash_command(
    name="delchannel",
    options=[disnake.Option(
        name="channel", type=disnake.OptionType.channel, required=True)],
    default_member_permissions=disnake.Permissions(8)
)
async def _delchannel(iter):
    channel = iter.options.get("channel")
    config = json.load(open("cfg.json"))
    config['channels'].remove(channel.id)
    json.dump(config, open("cfg.json", "w"), indent=4)
    await iter.send(channel.mention + " deleted from echo_bot.")


@client.slash_command(
    name="deladmin",
    options=[disnake.Option(
        name="admin", type=disnake.OptionType.user, required=True)],
    default_member_permissions=disnake.Permissions(8)
)
async def _deladmin(iter):
    user = iter.options.get("admin")
    config = json.load(open("cfg.json"))
    config['admins'].remove(user.id)
    json.dump(config, open("cfg.json", "w"), indent=4)
    await iter.send(user.mention + " removed from echo_bot.")


@client.message_command(
    name="Edit Webhook Message"
)
async def _edit_msg(iter):
    target = iter.target
    user = iter.author
    with open("messages.json") as f:
        messages_db = json.loads(f.read())
    if user.id == messages_db.get(str(target.id)):
        config = json.load(open("cfg.json"))
        webhook_url = config['hooks'][str(target.channel.id)]
        modal = disnake.ui.Modal(
            title="Editing webhook message", custom_id="edit_msg_form", components=[])
        modal.add_text_input(
            label="New message content",
            custom_id="new_msg_content",
            value=target.content,
            placeholder="Write your text here as you writing messages...",
            style=disnake.TextInputStyle.long,
            min_length=1,
            max_length=2048
        )
        try:
            await iter.response.send_modal(modal)
            modal_input = await client.wait_for("modal_submit", check=lambda x: x.author == iter.author and x.custom_id == "edit_msg_form", timeout=600)
        except asyncio.TimeoutError:
            return await iter.send("You took too long to respond to the form. Try again.", ephemeral=True)
        components = [
            disnake.ui.Select(
                custom_id="new_msg_attachments_clear",
                placeholder="Clear the message attachments?",
                options=[
                    disnake.SelectOption(
                        label="Yes, do it",
                        description="On message editing, his attachments will be cleaned.",
                        value="yes"
                    ),
                    disnake.SelectOption(
                        label="Nope, nevermind",
                        description="On message editing, his attachments will be keeped.",
                        value="no"
                    )
                ]
            ),
            disnake.ui.Select(
                custom_id="new_msg_reference_clear",
                placeholder="Clear the message reply to another message?",
                options=[
                    disnake.SelectOption(
                        label="Yes, do it",
                        description="On message editing, his reference will disappear.",
                        value="yes"
                    ),
                    disnake.SelectOption(
                        label="Nope, nevermind",
                        description="On message editing, his reference will be keeped.",
                        value="no"
                    )
                ]
            )
        ]
        clear_attachments = None
        clear_reference = None
        try:
            await modal_input.send("pre-last step:", components=[components[0]], ephemeral=True)
            user_select = await client.wait_for("dropdown", check=lambda x: x.author == iter.author and x.data.custom_id == "new_msg_attachments_clear", timeout=600)
            value = user_select.data.values[0]
            if value:
                clear_attachments = value
            else:
                clear_attachments = "no"
            await modal_input.edit_original_message("last step (please wait a bit before choosing an option):", components=[components[1]])
            user_select = await client.wait_for("dropdown", check=lambda x: x.author == iter.author and x.data.custom_id == "new_msg_reference_clear", timeout=600)
            value = user_select.data.values[0]
            if value:
                clear_reference = value
            else:
                clear_reference = "no"
        except asyncio.TimeoutError:
            return await iter.send("You took too long to respond to the message. Try again.", ephemeral=True)
        async with aiohttp.ClientSession() as session:
            sel_hook = disnake.Webhook.from_url(
                url=webhook_url, session=session)
            msg = await sel_hook.fetch_message(target.id)
            embeds = [] if clear_reference == "yes" else msg.embeds
            attachments = [] if clear_attachments == "yes" else msg.attachments
            await sel_hook.edit_message(target.id, content=modal_input.text_values.get("new_msg_content"), embeds=embeds, attachments=attachments)
            return await modal_input.edit_original_message("Message edited successfully.", components=[])
    else:
        await iter.send("You cannot edit this post because you are not the author.", ephemeral=True)


@client.message_command(
    name="Delete Webhook Message"
)
async def _delete_message(iter):
    target = iter.target
    user = iter.author
    with open("messages.json") as f:
        messages_db = json.loads(f.read())
    if user.id == messages_db.get(str(target.id)):
        config = json.load(open("cfg.json"))
        webhook_url = config['hooks'][str(target.channel.id)]
        components = [
            disnake.ui.Button(
                custom_id="btn_yes",
                style=disnake.ButtonStyle.danger,
                label="Yes, do it"
            ),
            disnake.ui.Button(
                custom_id="btn_no",
                style=disnake.ButtonStyle.success,
                label="Nope, nevermind"
            )
        ]
        await iter.send("Are you sure you want to delete this message?", components=components, ephemeral=True)
        try:
            button_click = await client.wait_for("button_click", check=lambda x: x.author == user and x.data.custom_id in ['btn_yes', 'btn_no'], timeout=600)
            match button_click.data.custom_id:
                case "btn_yes":
                    async with aiohttp.ClientSession() as session:
                        sel_hook = disnake.Webhook.from_url(
                            url=webhook_url, session=session)
                        await sel_hook.delete_message(target.id)
                        return await iter.edit_original_message("The message was successfully deleted.", components=[])
                case "btn_no":
                    return await iter.edit_original_message("The deletion of the message has been undone.", components=[])
        except TimeoutError:
            return await iter.edit_original_message("You took too long to respond to the message. Try again.")
    else:
        await iter.send("You cannot delete this message because you are not the author.", ephemeral=True)


client.run(open("token.txt").read())
