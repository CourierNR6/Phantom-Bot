EASTEREGG = {
    "info" : "Hallo! ich bin der DND Bot und wurde von CourierNr6 und TheFeThrone geschrieben. Viel Spaß beim Rollen!",
    "easteregg" : "Ostern ist vorbei. Such wo anders",
}

def hideEasterEggs(bot):
    for egg_name, egg_message in EASTEREGG.items():
        @bot.command(name=egg_name)
        async def egg(ctx, egg_message = egg_message):
            user = ctx.author
            mention = user.mention
            send_text = f'{mention} {egg_message}'
            await ctx.send(send_text)