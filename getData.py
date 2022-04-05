import pandas as pd
from utils import getDataFromTencent, getDate, getLabel, concernedCode
import numpy as np
import os


def downloadData(code_list, save_dir="./data/"):
    today = getDate()
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for code in code_list:
        obj = getDataFromTencent(code)

        if obj["state"]:
            label = getLabel()
            data_list = []
            for each in label:
                data_list.append(obj[each])
            label.append("time")
            data_list.append(today)
            data_pd = pd.DataFrame(
                np.array(data_list).reshape(1, len(data_list)))
            data_pd.to_csv(save_dir + "{}.csv".format(code),
                           mode='a', header=label)
        else:
            with open('downloadErr.log', 'a+') as f:
                f.writelines(code + ": download error! " + today)


if __name__ == "__main__":
    code_obj = concernedCode()

    code = ["sh" + each for each in code_obj["sh"]]
    code += ["sz" + each for each in code_obj["sz"]]

    downloadData(code)
