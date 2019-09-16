from __future__ import unicode_literals
from wxpy import *
from wechat_sender import listener

bot=Bot('bot.pkl')
listener.listen(bot)