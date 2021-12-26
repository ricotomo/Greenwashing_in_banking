import pandas as pd
import re
import csv 

def build_query():
    #Build query from company accounts and ESG keywords
    #https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query

    df_keywords = pd.read_csv ('keywords.csv')
    df_accounts = pd.read_csv ('accounts.csv')
    print("dataframe:")
    print(df_keywords.head())
    print(df_accounts.head())

    query=str("")

    #iterate over accounts
    for index, row in df_accounts.iterrows():
        curr_account=row['Username']
        #iterate through keywords
        for index, row in df_keywords.iterrows():
            if index == len(df_keywords)-1:
                query=query+(curr_account + " " + row['word'])
            else:
                query=query+(curr_account + " " + row['word'] + " OR ")
    return query

def split_query(query):
    access_lvl="elevated"
    other_rules = " -is:retweet"
    if access_lvl == "academic":
        rule_len = (1024 - len(other_rules))
    else:
        rule_len =( 512 - len(other_rules))

    sized_queries=[]
    chunks = re.split('(OR)', query)  # Splitting from 'OR'
    print(chunks)
    curr_q=""
    for index, chunk in enumerate(chunks):
        print(curr_q)
        print(len(curr_q))
        if ((len(curr_q) + len(chunk)) < rule_len):
            curr_q= curr_q + chunk
        elif index == (len(chunks)-1):
            #entered if we reach the end of the list
            if curr_q[-1] == 'R' and curr_q[-2] == 'O':
                print("entered OR removal")
                curr_q = curr_q[:len(curr_q) - 2]
            sized_queries.append(curr_q+ other_rules)
        else:
            #checks if there is an OR before we add our additional rules. If there is we need to remove it or get and error
            if curr_q[-1] == 'R' and curr_q[-2] == 'O':
                print("entered OR removal")
                curr_q = curr_q[:len(curr_q) - 2]
            sized_queries.append(curr_q + other_rules)
            #makes sure we dont start with an OR
            if chunk == "OR":
                curr_q=""
            else:
                curr_q=chunk
        
        
    return (sized_queries)