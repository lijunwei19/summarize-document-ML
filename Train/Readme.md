# Training Model Section
<small>Summarize_model - created by Li Junwei 
BUEC500 Final project </small>

<strong>This folder contain all the elements for tainning model.</strong> 

<strong>No enough computing resource and time to run training model completely(only 3% about 3-4hours). </strong>
 
 
<strong>Dataset we use</strong>
Kaggle- Amazon Reviews dataset
![amazon reviews](https://www.google.com/search?q=amazon+review+image&safe=active&rlz=1C5CHFA_enUS866US867&tbm=isch&source=iu&ictx=1&fir=-iq6RlCNvpSvdM%253A%252C8Uiv9AbOhY3c_M%252C_&vet=1&usg=AI4_-kQzLJFImNnZsNwyvq1OZjXwfNeknQ&sa=X&ved=2ahUKEwi114Ll6froAhV5lnIEHeUaD2QQ9QEwCXoECAoQJQ#imgrc=-iq6RlCNvpSvdM:)
 
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
 
