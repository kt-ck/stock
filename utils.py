import requests
import time
import re


def splitQueryName(query_name):
    # 返回 交易所，代码
    reg = re.compile(r'([a-z]+)', flags=re.I)
    which = re.search(reg, query_name)
    begin, end = which.span()
    return query_name[begin:end], query_name[end:]


def concernedCode():
    # 白酒: 茅台、五粮液、汾酒、泸州老窖、洋河股份、酒鬼酒、古井贡、
    # 光伏: 隆基、阳光电源、通威股份、中环、先导智能、特变电工、天合光能、福斯特、正泰电器
    return {
        "sh": ['600519', '600809', '601012', '600438', '600089', '688599', '601877', '603806', '000001'],
        "sz": ['000858', '000568', '300274', '002129', '300450', '002304', '000799', '000596'],
    }


def getNameFromCode(query_name):
    SH = {
        '600519': '贵州茅台',
        '600809': '山西汾酒',
        '601012': '隆基股份',
        '600438': '通威股份',
        '600089': '特变电工',
        '688599': '天合光能',
        '601877': '正泰电器',
        '603806': '福斯特',
        '000001': '上证指数'
    }
    SZ = {
        '002415': '海康威视',
        '000568': '泸州老窖',
        '300274': '阳光电源',
        '002129': '中环股份',
        '300450': '先导智能',
        '002304': '洋河股份',
        '000799': '酒鬼酒',
        '000596': '古井贡'

    }
    market, code = splitQueryName(query_name)
    if market == 'sz':
        return SZ[code]
    else:
        return SH[code]


def getLabel():
    return ['price', 'gain', 'rate', 'volume', 'turnover', 'market value']


def getBeginIndexFromTencent():
    return 3


def getDataFromTencent(query_name):
    # 股票名字, 代码， 当前价格，涨跌，涨跌率，成交量，成交额，总市值
    res = requests.get("https://qt.gtimg.cn/q=s_"+query_name)
    text = res.content.decode("gbk")
    text_list = text.split('"')[1].split("~")

    label_list = getLabel()

    market, _ = splitQueryName(query_name)
    if market == 'sz' or market == 'sh':
        endIndex = len(text_list)-1
    elif market == 'hk':
        endIndex = len(text_list)

    text_list = [text_list[index]
                 for index in range(getBeginIndexFromTencent(), endIndex) if text_list[index] != ""]
    obj = {}

    if len(label_list) == len(text_list):
        for i in range(len(label_list)):
            obj[label_list[i]] = text_list[i]
        obj["state"] = True
    else:
        obj["state"] = False
    return obj


def getDate():
    t = time.localtime()
    return str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday)


if __name__ == "__main__":
    print(getNameFromCode('BABA.N'))
