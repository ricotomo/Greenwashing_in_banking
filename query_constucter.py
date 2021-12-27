import pandas as pd
import re
import csv 

def build_query(verbose):
    #Build query from company accounts and ESG keywords
    #https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query

    df_keywords = pd.read_csv ('keywords.csv')
    df_accounts = pd.read_csv ('accounts.csv')
    if verbose:
        print("dataframe of build_query():")
        print(df_keywords.head())
        print(df_accounts.head())

    query=str("")
    info=[]
    #iterate over accounts
    for index, row in df_accounts.iterrows():
        curr_account=row['Username']
        institution=row['Company']
        #iterate through keywords
        for index, row in df_keywords.iterrows():
            if index == len(df_keywords)-1:
                query=query+(curr_account + " " + row['word'])
            else:
                query=query+(curr_account + " " + row['word'] + " OR ")
        info.append([institution, query])
        query=str("")
    return info

## work in progress change this so it uses info including company name

def split_query(query, verbose):
    access_lvl="elevated"
    other_rules = " -is:retweet"
    if access_lvl == "academic":
        rule_len = (1024 - len(other_rules))
    else:
        rule_len =( 512 - len(other_rules))

    sized_queries=[]
    chunks = re.split('(OR)', query)  # Splitting from 'OR'
    if verbose:
        print(chunks)
    curr_q=""
    for index, chunk in enumerate(chunks):
        if verbose:
            print(curr_q)
            print(len(curr_q))
        if ((len(curr_q) + len(chunk)) < rule_len):
            curr_q= curr_q + chunk
        elif index == (len(chunks)-1):
            #entered if we reach the end of the list
            if curr_q[-1] == 'R' and curr_q[-2] == 'O':
                if verbose:
                    print("entered OR removal")
                curr_q = curr_q[:len(curr_q) - 2]
            sized_queries.append(curr_q+ other_rules)
        else:
            #checks if there is an OR before we add our additional rules. If there is we need to remove it or get and error
            if curr_q[-1] == 'R' and curr_q[-2] == 'O':
                if verbose:
                    print("entered OR removal")
                curr_q = curr_q[:len(curr_q) - 2]
            sized_queries.append(curr_q + other_rules)
            #makes sure we dont start with an OR
            if chunk == "OR":
                curr_q=""
            else:
                curr_q=chunk
        
        
    return (sized_queries)