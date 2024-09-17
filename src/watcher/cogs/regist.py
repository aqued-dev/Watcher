import os
import gspread
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials
import dotenv


class SheetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        dotenv.load_dotenv()

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]

        credentials = {
            "type": "service_account",
            "project_id": os.getenv("PROJECT_ID"),
            "private_key_id": os.getenv("PRIVATE_KEY_ID"),
            "private_key": os.getenv("PRIVATE_KEY"),
            "client_email": os.getenv("CLIENT_EMAIL"),
            "client_id": os.getenv("CLIENT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
        }

        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
        self.gc = gspread.authorize(creds)

        self.SPREAD_SHEET_KEY = os.getenv("SPREAD_SHEET_KEY")
        self.workbook = self.gc.open_by_key(self.SPREAD_SHEET_KEY)
        self.worksheet = self.workbook.worksheets()[0]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.channel.id != int(
            os.getenv("SHEET_CHANNEL_ID")
        ):
            return

        print(message.content)

        rows = self.worksheet.get_all_values()

        next_empty_row = len(rows) + 1
        for i, row in enumerate(rows):
            if not any(row):
                next_empty_row = i + 1

        self.worksheet.update_cell(next_empty_row, 1, message.content)


async def setup(bot):
    await bot.add_cog(SheetCog(bot))
