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
    return ['股票代码', '当前价格', '昨收', '开盘', '成交量', '外盘', '内盘', '涨跌', '涨跌%', '最高', '最低', '成交额', '换手率', 'ttm市盈率', '振幅', '流通市值', '总市值', 'if市净率', '量比', '均价', '动态市盈率', '静态市盈率']


def getDataFromTencent(query_name):
    res = requests.get("https://qt.gtimg.cn/q="+query_name)
    text = res.content.decode("gbk")
    text_list = text.split('"')[1].split("~")
    text_list = [each for each in text_list if each != "" and each != " "]

    index_list = [2, 3, 4, 5, 6, 7, 8, 30, 31, 32, 33, 36,
                  37, 38, 41, 42, 43, 44, 47, 49, 50, 51]
    obj = {}
    if len(text_list) > len(index_list):
        label_list = getLabel()
        for index in range(len(index_list)):
            obj[label_list[index]] = text_list[index_list[index]]
        obj["state"] = True
    else:
        obj["state"] = False

    return obj


def getDate():
    t = time.localtime()
    return str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday)


if __name__ == "__main__":
    getDataFromTencent('sh600519')
