import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import networkx as nx
import seaborn as sn


def sigmoid(x):
    return 1/(1 + np.exp(-x))

def func1(title_list):
    stopword = ['Reuters',"'s",'``',"''",',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%','-','“','”','’','–','‘']
    stops = set(stopwords.words("english"))
    content = []
    content2 = []
    for i in title_list:
        tokenized_text = word_tokenize(i)
        temp_list = []
        for j in tokenized_text:
            if j not in stopword:
                if j not in stops:
                    content.append(j)
                    temp_list.append(j)
        content2.append(temp_list)

    relationships = {}
    for item in content:
        if item not in relationships:
            relationships[item] = {}
    for line in content2:
        for name1 in line:
            for name2 in line:
                if name1 == name2:
                    continue
                if relationships[name1].get(name2) is None:
                    relationships[name1][name2] = 1
                else:
                    relationships[name1][name2] = relationships[name1][name2] + 1
    co_occur_by_records = [[name, v, w] for name, edges in relationships.items() for v, w in edges.items() if w > 2]
    np.random.shuffle(co_occur_by_records)
    temp_matrix = pd.DataFrame()
    for i in co_occur_by_records:
        temp_matrix.at[i[0], i[1]] = i[2]
    co_occurrence_matrix_by_records = pd.DataFrame()
    for i in temp_matrix:
        for j in temp_matrix:
            co_occurrence_matrix_by_records.at[i, j] = temp_matrix.at[i, j]

    count_by_records = [i[2] for i in co_occur_by_records]
    co_occur_by_records_sig = []
    for i in co_occur_by_records:
        co_occur_by_records_sig.append([i[0], i[1], sigmoid((i[2] - np.mean(count_by_records))/np.std(count_by_records))])

    plt.figure(figsize=(25,25))
    g = nx.Graph()
    g.add_weighted_edges_from(co_occur_by_records_sig)
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, alpha=0.8,node_size=[val*50 for (node, val) in g.degree()])
    nx.draw_networkx_edges(g, pos, alpha=0.2)
    for p in pos:
        pos[p][1] = pos[p][1] + 0.03
    nx.draw_networkx_labels(g, pos, font_size = 16, alpha=0.8)
    plt.savefig('report/Related_word/img/knowledge_graph.png')

    plt.figure(figsize=(20,20))
    sn.heatmap(co_occurrence_matrix_by_records,cmap='YlGnBu')
    plt.savefig('report/Related_word/img/co_occurence_matrix.png')
    return co_occur_by_records

def return_associate(keyword , co_occur_by_records):
    return [items[1] for items in co_occur_by_records if keyword.lower() == items[0].lower()]

def return_ticker(keyword):
    df = pd.read_csv('txtfile/ticker.csv')
    for company in df['Security']:
        if keyword.lower() in company.lower():
            return df['Symbol'][df[df['Security']==company].index[0]]

