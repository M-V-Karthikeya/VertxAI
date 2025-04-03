import pandas as pd 

data = pd.read_json('Data/investors.json')

def clean(s):
    l = []
    if(',' in s):
        s = s.split(',')
    else:
        s = [s]
    for i in s:
        if(i.strip()):
            l.append(i.strip().lower())
    return l

stages = []
for i in list(data['Stage']):
    stages+=clean(i)
stages = list(set(stages))

models = []
for i in list(data['Type']):
    models+=clean(i)
models = list(set(models))

industries = []
for i in range(len(list(data['Industry']))):
    if(data['Industry'][i]!=data['Overview'][i]):
        i = data['Industry'][i]
        industries+=clean(i)
industries = list(set(industries))

countries = []
for i in list(data['Countries']):
    countries+=clean(i)
countries = list(set(countries))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_overview(desc,inv_data):
    scores = []
    tfidf = TfidfVectorizer()
    for i in inv_data['Overview']:
        text = [desc,i]
        tfidf_emb = tfidf.fit_transform(text).toarray()
        cos_sim = cosine_similarity(tfidf_emb[0].reshape(1,-1),tfidf_emb[1].reshape(1,-1))[0][0]
        scores.append(int(cos_sim*100)+1)
    return scores

def match_industry(industry,inv_data):
    scores = []
    for i in inv_data['Industry']:
        score = 0
        inds = clean(i)
        for j in industry:
            if(j in inds):
                score+=15
        scores.append(score)
    return scores

def match_stage(stage,inv_data):
    scores = []
    for i in inv_data['Stage']:
        score = 0
        st = clean(i)
        for j in stage:
            if(j in st):
                score+=10
        scores.append(score)
    return scores

def match_region(region,inv_data):
    scores = []
    for i in inv_data['Countries']:
        score = 0
        country = clean(i)
        for j in region:
            if(j in country):
                score+=5
        scores.append(score)
    return scores

def match_model(model,inv_data):
    scores = []
    for i in inv_data['Type']:
        score = 0
        mod = clean(i)
        for j in model:
            if(j in mod):
                score+=5
        scores.append(score)
    return scores

def match_funds(funds,inv_data):
    scores = []
    for i in inv_data['Cheque_range']:
        score = 0
        i = i.replace('$',"").lower().replace('k','000').replace('m','000000').split('-')
        if(len(i)==1):
            min_fund = int(i[0].strip())
            max_fund = min_fund
        else:
            min_fund,max_fund = int(i[0].strip()),int(i[1].strip())
        if min_fund <= funds <= max_fund:
            score+=30
        scores.append(score)
    return scores

def match(founders_input,data):
    s_over,s_in,s_st,s_re,s_mo,s_fu = match_overview(founders_input['desc'],data),match_industry(founders_input['industry'],data),match_stage(founders_input['stage'],data),match_region(founders_input['region'],data),match_model(founders_input['model'],data),match_funds(founders_input['funds'],data)
    scores = []
    for i in range(len(s_over)):
        res = s_over[i]+s_in[i]+s_st[i]+s_re[i]+s_mo[i]+s_fu[i]
        scores.append([i,res])
    scores = sorted(scores,key=lambda x:x[1],reverse=True)
    indices = []
    rank = []
    for i in scores[:30]:
        indices.append(i[0])
        rank.append(i[1])
    df = data.loc[indices]
    df['Score'] = rank
    return df

import streamlit as sl
sl.title("Investor Matching Platform")

desc = sl.text_area("Describe your startup:")
industry = sl.multiselect("Select Industry:",industries)
stage = sl.multiselect("Select Stage:",stages)
region = sl.multiselect("Select Region:",countries)
model = sl.multiselect("Select Model:",models)
funds = sl.number_input("Funding Needed ($):")

if sl.button("Find Investors"):
    user_input = {"desc": desc, "industry": industry, "stage": stage, "region": region, "model": [model], "funds": funds}
    df = match(user_input,data)
    sl.dataframe(df)
    sl.download_button("Download CSV", df.to_csv(index=False), "matched_investors.csv", "text/csv")