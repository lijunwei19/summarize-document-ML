# Training Model Section
Summarize_model - created by Li Junwei 
BUEC500 Final project 
This folder contain all the elements for tainning model. No enough computing resource and time to run training model completely(only 3% about 3-4hours). 
 
 
## Guide  
   Continue trainning it,<strong> more accuracy</strong>
   Use the trained model to summarize reviews. 
   
## model detail
### Learning Type
    1.  abstractiv text summarizers

### Algorithm
    1.  prepare dataset 
    2.  data pre-processing
        a. cleaning
        b. Tokenization
        c. word embedding using conceptNet Numberbatch
        d. vectorization 
    3.  Designing LSTM Bi-directional Encoders & Deconders
    4.  Train and  testing then save the model
    5.  Take user input and summarize document 

## More accuracy 
### Pre-requisites lib
    python 3.5
    tensorflow 1.1.0
    Numpy
    pandas
    Nltk
 