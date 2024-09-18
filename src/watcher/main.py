import os
import discord
from discord.ext import commands
import dotenv

dotenv.load_dotenv()


class Watcher(commands.Bot):
    def __init__(
        self,
    ):
        intents = discord.Intents.default()
        intents.typing = False
        intents.message_content = True
        intents.dm_messages = True
        intents.guild_messages = True

        super().__init__(intents=intents, command_prefix="aw.")

    async def setup_hook(self) -> None:
        for name in os.listdir("src/watcher/cogs"):
            if not name.startswith("__"):
                try:
                    await bot.load_extension(
                        f"cogs.{name[:-3] if name.endswith('.py') else name}"
                    )
                except Exception as e:
                    print("読み込み中にエラーが発生しました。\n", e)


bot = Watcher()


@bot.listen("on_ready")
async def ready():
    print(f"{bot.user.name}#${bot.user.discriminator}でログインしています。")


if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
