import json

with open('vocab_to_int.json', 'r') as openfile: 
    # Reading from json file 
    vocab_to_int = json.load(openfile) 
with open('int_to_vocab.json', 'r') as openfile:    
    # Reading from json file 
    int_to_vocab = json.load(openfile) 

with open('sorted_clean_Text_Summary_dic.json', 'r') as openfile: 
    # Reading from json file 
    sorted_clean_Text_Summary_dic = json.load(openfile) 

sorted_texts = sorted_clean_Text_Summary_dic['Text']
cleasorted_summariesn_summaries = sorted_clean_Text_Summary_dic['Summary']
