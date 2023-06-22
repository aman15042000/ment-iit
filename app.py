import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session
from urllib.parse import urlencode
from urllib.parse import parse_qs, unquote
import ast
import re
# %matplotlib inline
# %config InlineBackend.figure_format = 'retina'

import secrets
secret_key = secrets.token_hex(16)


app = Flask(__name__)
counter = 0

@app.route('/', methods=['GET', 'POST'])

def initiate():
    global counter
    counter+=1
    if request.method == 'POST':
        Rank = request.form.get("rank")
        Category = request.form.get('category')
        gender = request.form.get('gender')
        Adv = request.form.get('rank-type')
        round = request.form.get('round')
        rt = ""
        if(Adv == "Jee-adv"):
            rt = "IIT"
        else:
            rt = "othclg"

        session['catg'] = Category
        session['gen'] = gender
        session['rankType'] = rt
        session['r'] = round
        # round = 6
        usr = {'rank': Rank, 'category': Category, 'Gender': gender, 'jee-adv': rt, 'Round': round}
        print(Rank, Category, gender, rt)
        lst_clg = getclg(usr)
        # fileN = 'pref_lst' + usr['category'] + usr['Gender'] + rt + '.csv'
        # rt = pd.read_csv(fileN)
        pref_lst = getPrefList(lst_clg)
        return redirect(url_for('show_results', pref_lst=pref_lst))

    else:
        return render_template('home.html', cnt = counter)


@app.route('/result')
def show_results():
    pref_lst = request.args.get('pref_lst')
    url = request.url
    parsed_url = parse_qs(url)
    pref_lst_values = parsed_url.get('pref_lst', [])
    decoded_values = [unquote(value) for value in pref_lst_values]

    lst = []
    for item in decoded_values:
        values = ast.literal_eval(item)
        college_name = values[0]
        branch_name = values[1]
        rank = values[2]

        lst.append((college_name, branch_name, rank))
    # lst = pref_lst_values
    print("No of clg in lst ", len(lst))
    print("no. of clg ", len(pref_lst_values))
    print(lst)
    return render_template('result.html', lst = lst)



def getclg(usr):
    lst_clg = []
    file = '2022' + usr['Round'] + usr['category'] + usr['jee-adv'] + '.csv'
    print(file)
    dfr1 = pd.read_csv(file)
    rs = dfr1.shape[0]
    t = (int(usr['rank'])/10)
    if t <= 50 and int(usr['rank']) < 400:
        t = 100
    for r in range(rs):
        if int(usr['rank']) - t <= int(dfr1.loc[r, 'Closing Rank']):
            if usr['Gender'] == dfr1.loc[r, 'Gender']:
                if dfr1.loc[r, 'Academic Program Name'] == "Architecture (5 Years, Bachelor of Architecture)" and usr['jee-adv'] == "othclg":
                    continue
                else:
                    lst_clg.append((dfr1.loc[r, 'Institute'], dfr1.loc[r, 'Academic Program Name']))
                # if dfr1.loc[r, 'Institute'] in dict:
                #     dict[dfr1.loc[r, 'Institute']].append(dfr1.loc[r, 'Academic Program Name'])
                # else:
                #     dict[dfr1.loc[r, 'Institute']] = []
                #     dict[dfr1.loc[r, 'Institute']].append(dfr1.loc[r, 'Academic Program Name'])
    return lst_clg

# def getPrefList(df, lst_clg):
#     pr = []
#     rows = df.shape[0]
#     cols = df.shape[1]
#     for i in range(rows):
#         pr.append((df.loc[i, 'Institute'], df.loc[i, 'Academic Program Name']))
#     standard_dict = {t: i for i, t in enumerate(pr)}
#     print(standard_dict)
#     pref_lst = sorted(lst_clg, key=lambda x: standard_dict.get(x, str('inf')))

#     t = session.get('catg')
#     h = session.get('rankType')
#     g = session.get('gen')
#     fileName = '2022r1' + t + h+ '.csv'
#     # print(fileName)
#     df = pd.read_csv(fileName)
#     dict_ = {}
#     for i in range(df.shape[0]):
#         dict_[df.loc[i, 'Institute'] + df.loc[i, 'Academic Program Name'] + df.loc[i, 'Gender']] = df.loc[i, 'Closing Rank']
#     # print(dict_)
#     final_lst = []
#     for i in pref_lst[:25]:
#         final_lst.append((i[0], i[1], str(dict_[i[0]+i[1]+g])))
#     # for j in final_lst:
#         # print(j)
#     return final_lst[:25]
def getPrefList(lst_clg):
    
    t = session.get('catg')
    h = session.get('rankType')
    g = session.get('gen')
    er  = session.get('r')
    fileName = '2022'+ er + t + h + '.csv'
    # print(fileName)
    df = pd.read_csv(fileName)
    dict_ = {}
    for i in range(df.shape[0]):
        dict_[df.loc[i, 'Institute'] + df.loc[i, 'Academic Program Name'] + df.loc[i, 'Gender']] = df.loc[i, 'Closing Rank']
    # print(dict_)
    final_lst = []
    for i in lst_clg:
        if i[1] == "Architecture (5 Years, Bachelor of Architecture)" and h == "othclg":
            continue
        else:
            final_lst.append((i[0], i[1], int(dict_[i[0]+i[1]+g])))
    sorted_list = sorted(final_lst, key=lambda x: x[2])
    # print(sorted_list)
    return sorted_list[:350]


if __name__ == '__main__':
    app.secret_key = secret_key
    app.run()
