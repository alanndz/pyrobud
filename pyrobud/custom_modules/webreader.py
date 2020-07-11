"""
Articles Scraper Module for pyrobud userbot
Author: yshalsager <ysh-alsager@hotmail.com>

And Translate with specific languange and upload to telegraph
Re-Author: alanndz <alanmahmud0@gmail.com>
This module is used to get the content of an article without leaving Telegram.

Dependencies: newspaper3k
"""
import re

from newspaper import Article, ArticleException
from telegraph import Telegraph
from googletrans import Translator

from pyrobud import command, module

class WebReader(module.Module):
    name: str = "WebReader"
    disabled: bool = False
    regex: str = r'(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.' \
                 r'[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*))'

    @command.desc("Scrap article content, translate and upload to telegraph")
    @command.alias("wread", "wr")
    @command.usage("[url] [language(optional)]")
    async def cmd_webreader(self, ctx: command.Context) -> str:
        if len(ctx.input.split()) > 1:
            lang = ctx.input.split()[1]
        else: lang = None

        tgr = Telegraph()
        tl = Translator()

        url: str = ctx.input or ctx.segments[1]
        url: str = re.search(self.regex, url).group(1)

        article: Article = Article(url)

        try:
            await ctx.respond("Getting text ...")
            article.download()
            article.parse()
            text = f"{article.text}"
        except ArticleException:
            return "Failed to scrape the article!"

        if lang:
            try:
                await ctx.respond("Translating Text ...")
                text = tl.translate(text, dest=lang)
            except ValueError as err:
                return "Error: `{}`".format(str(err))
            text = text.text

        await ctx.respond("Uploading to telegraph ...")
        tgr.create_account(short_name='alanndz')
        response = tgr.create_page(
            "{}".format(article.title),
            html_content="<p>{}!</p>".format(text.replace("\n", "<br>"))
        )

        return ('https://telegra.ph/{}'.format(response['path']))
