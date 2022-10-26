import discord
from discord.ext import commands
from utils.Database import Database
from utils.query_tools import get_ner, get_intent
from utils.recomendation import sim_wine_recommend, reg_recommend
from utils.FindWine import FindWine

intents = discord.Intents.default()
client = commands.Bot(command_prefix='!',intents=intents)

@client.event
async def on_ready():
    game = discord.Game("당신을 위해 대기하는 중")
    await client.change_presence(status=discord.Status.online, activity=game)
    print('Welcome to WBTI!')

@client.event
async def on_message(message):
    # SENDER가 BOT일 경우 반응을 하지 않도록 한다.
    query = str(message.content)
    if message.author.bot:
        return None

    if message.content == '소개':
        embed = discord.Embed(title='WBTI 이용법을 알려드릴게요!',
                              description='이모지를 사용해서 원하는 페이지로 이동할 수 있어요.', colour=0x00FFFF)
        embed.add_field(name='> 이용법', value="원하는 와인의 특성(당도, 산미, 바디감, 타닌감)을 입력하시거나, 좋아하는 와인을 입력하세요", inline=False)
        embed.add_field(name='> 당도', value="당도(Sweetness)는 단맛의 정도를 의미합니다.", inline=False)
        embed.add_field(name='> 산미', value="산미(Acidity)는 신맛의 정도를 의미합니다.", inline=False)
        embed.add_field(name='> 바디감', value="바디감(Body)은 와인의 농도와 점도를 의미합니다.", inline=False)
        embed.add_field(name='> 타닌감', value="타닌감(Tannic)은 떫은 맛, 쌉싸름한 맛의 정도를 의미합니다.", inline=False)
        await message.channel.send(embed=embed)

    intent = get_intent(query)
    #DB 연결

    # 의도에 따라 와인id 추출
    if intent == '와인 기반':
        wine_id = sim_wine_recommend(query)

        db = Database()
        f = FindWine(db)
        wine = ''
        if '레드와인' in query:
            sql = f"SELECT * FROM data_redwine WHERE wineid = {wine_id}"
            wine = db.execute(sql)
        elif '화이트와인' in query:
            sql = f"SELECT * FROM data_whitewine WHERE wineid = {wine_id}"
            wine = db.execute(sql)
        info_list = []
        for i in range(0, len(wine[0])):
            a = wine[0][i]
            info_list.append(a)

        # 가격 정수처리, 특성값 %로 변환
        for i in range(12, 16):
            info_list[i] = str(round(wine[0][i] * 100, 1)) + "%"
        info_list[9] = int(wine[0][9])

        answer = f.search_answer(13, info_list)
        await message.channel.send(answer)
        return None

    elif intent == '특성 기반':
        ner_list = get_ner(query)
            # 질문 db에서 질의 후 특성값 저장
        wine_id = reg_recommend(ner_list)
        # 답변 내용 구성
        db = Database()
        f = FindWine(db)
        wine = ''
        if ner_list[4] == '레드와인':
            sql = f"SELECT * FROM data_redwine WHERE wineid = {wine_id}"
            wine = db.execute(sql)
        elif ner_list[4] == '화이트와인':
            sql = f"SELECT * FROM data_whitewine WHERE wineid = {wine_id}"
            wine = db.execute(sql)
        info_list = []
        for i in range(0, len(wine[0])):
            a =wine[0][i]
            info_list.append(a)

        # 가격 정수처리, 특성값 %로 변환
        for i in range(12, 16):
            info_list[i] = str(round(wine[0][i] * 100, 1)) + "%"
        info_list[9] = int(wine[0][9])

        answer = f.search_answer(7,info_list)
        await message.channel.send(answer)

    else:
        msg = '그건 몰라요!'
        await message.channel.send(str(msg))
        return None






client.run("MTAyNjc3MjE1OTA1NTUzMjAzMg.GJmsLV.Cr268zZa2tUNoyNtxIb_wIiTXaxn9AXwZqXXGM")