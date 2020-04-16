from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import pandas as pd 
import warnings
import json
import re
import numpy as np
def pre_text(file_name):
    # setting the max display
    pd.set_option("display.max_colwidth", 200)

    # ignore warnings
    warnings.filterwarnings("ignore")

    #reading data from csv file
    data=pd.read_csv(file_name   ,nrows=100000)

    #drop repeat text data and NaN invalid data
    data.drop_duplicates(subset=['Text'],inplace=True)
    data.dropna(axis=0,inplace=True)

    return data


def load_Abb_dic(dic_json_file_name):
    #load maping Abbre dic
    with open(dic_json_file_name) as f:
        contraction_mapping = json.load(f) 
        return contraction_mapping

def text_cleaner(text,num, contraction_mapping):
# 1.Convert everything to lowercase    2.Remove HTML tags    3.Contraction mapping     4.Remove (‘s)
# 5.Remove any text inside the parenthesis ( )               6.Eliminate punctuations and special characters
# 7.Remove stopwords                                         8.Remove short words
    stop_words = set(stopwords.words('english')) 
    newString = text.lower()
    newString = BeautifulSoup(newString, "lxml").text
    newString = re.sub(r'\([^)]*\)', '', newString)
    newString = re.sub('"','', newString)
    newString = ' '.join([contraction_mapping[t] if t in contraction_mapping else t for t in newString.split(" ")])    
    newString = re.sub(r"'s\b","",newString)
    newString = re.sub("[^a-zA-Z]", " ", newString) 
    newString = re.sub('[m]{2,}', 'mm', newString)
    if(num==0):
        tokens = [w for w in newString.split() if not w in stop_words]
    else:
        tokens=newString.split()
    long_words=[]
    for i in tokens:
        if len(i)>1:                                                 #removing short word
            long_words.append(i)   
    return (" ".join(long_words)).strip()


def final_cleaned_reviews(file_name, dic_json_file_name ):
    # loading dic for abbreative word 
    contraction_mapping = load_Abb_dic(dic_json_file_name)

    # drop repeat data and invalid data in csv file 'text' section
    data = pre_text(file_name)

    # clean data 
    cleaned_text = []
    for t in data['Text']:
        cleaned_text.append(text_cleaner(t,0,contraction_mapping)) 


    cleaned_summary = []
    for t in data['Summary']:
        cleaned_summary.append(text_cleaner(t,1,contraction_mapping))
    
    data['cleaned_text']=cleaned_text
    data['cleaned_summary']=cleaned_summary

    data.replace('', np.nan, inplace=True)
    data.dropna(axis=0,inplace=True)

    df = data[['cleaned_text','cleaned_summary']]
    df.to_csv('amazon-fine-food-reviews/cleaned.csv')

def main():
    file_name = "amazon-fine-food-reviews/Reviews.csv"
    dic_json_file_name = 'amazon-fine-food-reviews/MapAbbWord_dic.json'
    final_cleaned_reviews(file_name,dic_json_file_name )
    
if __name__ == "__main__":
    main()

