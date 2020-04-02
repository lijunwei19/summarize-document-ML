# summarize-document-ML
BUEC 500 project  
Li Junwei, Li Jingyi, 
04/01/2020
# User Story 
Nowadays, many documents are generated in our life, people often need spend a lot of time to read and understanding those content. as a programmer, we want to find a easily and efficient novel method that can help human quickly grasp the main idea of article or news. 

# Algorithm
deep learning 
abstractiv text summarizers
RNN 

1.  prepare dataset 
2.  data pre-processing
    a. cleaning
    b. Tokenization
    c. word embedding using conceptNet Numberbatch
    d. vectorization 
3.  Designing LSTM Bi-directional Encoders & Deconders
4.  Train and  testing then save the model
5.  Take user input and summarize document 



# dataset for training 
Amazon-Fine-Food-Review 
DUC (document Understanding Conference) dataset 
CNN / Daily Mail Dataset
Gigaword Dataset

# pre-requisites 
python 3.7
Numpy
pandas
Nltk
tensor flow
PyRouge 
