from discord.ext import commands
import requests
import discord
from bs4 import BeautifulSoup

TOKEN = "TOKEN HERE"


intents = discord.Intents.default()
intents.message_content = True

def checkAddress(address):
    if len(address) == 34 and address.startswith("9"):
        return True
    return False

bot = commands.Bot(command_prefix=':', intents=intents)

@bot.event
async def on_ready():
    global live
    await bot.tree.sync()
    print("We have logged in as", bot.user)

@bot.hybrid_command(brief="Calculate mining profit for a given hashrate",description="Calculate mining profit for a given hashrate")
async def mprofit(ctx, kh):
    try:
        data = requests.post("https://mp.magizap.com/calculate/mining",json={"hashrate":str(kh)},timeout=5).json()
    except requests.exceptions.Timeout:
        await ctx.send("The request timed out. Please try again later. Magizap api might be down.")
        return
    msg = "Profit per hour: "+str(data["h_m"])+"\n"
    msg += "Profit per day: "+str(data["d_m"])+"\n"
    msg += "Profit per week: "+str(data["w_m"])+"\n"
    msg += "Network Statistics\n"
    msg += "Mining difficulty: "+str(data["m_a"])+"\n"
    msg += "Block value: "+str(data["m_b"])+"\n"
    msg += "Network hashrate:" + str(data["m_c"])+"\n"
    await ctx.send(msg)


@bot.hybrid_command(brief="Calculate staking profit for a given number of XMG",description="Calculate staking profit for a given number of XMG")
async def stakeprofit(ctx, xmg):
    try:
        data = requests.post("https://mp.magizap.com/calculate/staking",json={"balance":str(xmg)},timeout=5).json()
    except requests.exceptions.Timeout:
        await ctx.send("The request timed out. Please try again later. Magizap api might be down.")
        return
    msg = "Profit per hour: "+str(data["h_s"])+"\n"
    msg += "Profit per day: "+str(data["d_s"])+"\n"
    msg += "Profit per week: "+str(data["w_s"])+"\n"
    msg += "Network Statistics\n"
    msg += "Staking difficulty: "+str(data["s_a"])+"\n"
    msg += "Staking interest: "+str(data["s_b"])+"\n"
    msg += "Network staking weight:" + str(data["s_c"])+"\n"
    
    await ctx.send(msg)


@bot.hybrid_command(brief="Get miner information for a given address in bowserlab pool",description="Get miner information for a given address in bowserlab pool")
async def minersbowserlab(ctx, address):
    if not checkAddress(address):
        await ctx.send("Invalid address")
        return
    msg=""
    try:
        data = requests.get(
            "https://bowserlab.ddns.net:8080/api/walletEx?address="+address).json()

        msg += "## Count: "+str(len(data["miners"]))+"\n"
        msg += "---------------------------------\n"
        for miner in data["miners"]:
            msg += "Version: "+miner["version"]+"\n"
            msg += "Algo: "+miner["algo"]+"\n"
            msg += "Accepted: "+str(miner["accepted"])+"\n"
            msg += "Rejected: "+str(miner["rejected"])+"\n"
            msg += "\n"
    except:
        pass
    try:
        data2 = requests.get("https://bowserlab.ddns.net:8080/site/wallet_miners_results?address="+address).content
        soup = BeautifulSoup(data2, 'html5lib')
        dat = soup.find_all("table", {"class": "dataGrid2"})
        dat = dat[0].find_all("tr", {"class": "ssrow"})
        tmp=[]
        tmp2=[]
        for elm in dat:
            tmp+=(elm.find_all("td"))
        for elm in tmp:
            if elm.find("b"):
                tmp2.append(elm.find("b").text)
                continue
            tmp2.append(elm.text)

        msg += "## Summary\n"
        msg += "---------------------------------\n"

        for i in range(len(tmp2)//4):
            msg+="Algo: "+(tmp2[i*4])+"\n"
            msg+="Workers: "+(tmp2[i*4+1])+"\n"
            msg+="Hashrate: "+(tmp2[i*4+2])+"\n"
    except:
        pass
    if msg=="":
        await ctx.send("bowserlab.ddns.net api down. Please try again later.")
        return
    await ctx.send(msg)


@bot.hybrid_command(brief="Get wallet stats for a given address in bowserlab pool",description="Get wallet stats for a given address in bowserlab pool")
async def walletstatsbowserlab(ctx, address):
    if not checkAddress(address):
        await ctx.send("Invalid address")
        return
    data = requests.get(
        "https://bowserlab.ddns.net:8080/api/wallet?address="+address).json()
    # msg = "Unsold: "+str(data["unsold"])+"\n"
    msg=""
    msg += "Balance: "+str(data["balance"])+"\n"
    msg += "Unpaid: "+str(data["unpaid"])+"\n"
    msg += "Paid24h: "+str(data["paid24h"])+"\n"
    msg += "Total: "+str(data["total"])+"\n"
    if msg=="":
        await ctx.send("bowserlab.ddns.net api down. Please try again later.")
        return
    await ctx.send(msg)



@bot.hybrid_command(brief="Get miner information for a given address in Lidonia pool",description="Get miner information for a given address in Lidonia pool")
async def minerslidonia(ctx, address):
    if not checkAddress(address):
        await ctx.send("Invalid address")
        return
    msg=""
    try:
        data = requests.get(
            "http://lidonia.com/api/walletEx?address="+address, verify=False, headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0"}).json()

        msg += "## Count: "+str(len(data["miners"]))+"\n"
        msg += "---------------------------------\n"
        for miner in data["miners"]:
            msg += "Version: "+miner["version"]+"\n"
            msg += "Algo: "+miner["algo"]+"\n"
            msg += "Accepted: "+str(miner["accepted"])+"\n"
            msg += "Rejected: "+str(miner["rejected"])+"\n"
            msg += "\n"
    except:
        pass
    try:
        data2 = requests.get("http://lidonia.com/site/wallet_miners_results?address="+address, verify=False, headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0"}).content
        soup = BeautifulSoup(data2, 'html5lib')
        dat = soup.find_all("table", {"class": "dataGrid2"})
        dat = dat[0].find_all("tr", {"class": "ssrow"})
        tmp=[]
        tmp2=[]
        for elm in dat:
            tmp+=(elm.find_all("td"))
        for elm in tmp:
            if elm.find("b"):
                tmp2.append(elm.find("b").text)
                continue
            tmp2.append(elm.text)

        msg += "## Summary\n"
        msg += "---------------------------------\n"

        for i in range(len(tmp2)//4):
            msg+="Algo: "+(tmp2[i*4])+"\n"
            msg+="Workers: "+(tmp2[i*4+1])+"\n"
            msg+="Hashrate: "+(tmp2[i*4+2])+"\n"
    except:
        pass
    if msg=="":
        await ctx.send("lidonia.com api down. Please try again later.")
        return
    await ctx.send(msg)


@bot.hybrid_command(brief="Get wallet stats for a given address in Lidonia pool",description="Get wallet stats for a given address in Lidonia pool")
async def walletstatslidonia(ctx, address):
    if not checkAddress(address):
        await ctx.send("Invalid address")
        return
    data = requests.get(
        "http://lidonia.com/api/wallet?address="+address, verify=False, headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0"}).json()
    # msg = "Unsold: "+str(data["unsold"])+"\n"
    msg=""
    msg += "Balance: "+str(data["balance"])+"\n"
    msg += "Unpaid: "+str(data["unpaid"])+"\n"
    msg += "Paid24h: "+str(data["paid24h"])+"\n"
    msg += "Total: "+str(data["total"])+"\n"
    if msg=="":
        await ctx.send("lidonia.com api down. Please try again later.")
        return
    await ctx.send(msg)

@bot.hybrid_command(brief="Show credits",description="Show credits about the bot, and the projects and persons that made this bot possible.")
async def credits(ctx):
    await ctx.send("This bot is made by @notlucasz228. \nYou can find the source code at github.com/zlc1004/maigbot.\nThis bot uses the magizap api for mining and staking profit calculations. \nThis bot uses the bowserlab and lidonia api for pool information. \nThis bot uses the discord.py library for discord bot creation. \nThis bot uses the requests library for making http requests. \nThis bot uses the beautifulsoup library for parsing html content.")
    
bot.run(TOKEN)
