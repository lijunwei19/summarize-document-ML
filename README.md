# Summarize-Document-ML
   BUEC 500 project  -------  Li Junwei, Li Jingyi,     04/01/2020
# User Story 
   Nowadays, many documents are generated in our life, people often need spend a lot of time to read and understanding those content. as a programmer, we want to find a easily and efficient novel method that can help human quickly grasp the main idea of article or news. 


<strong>Dataset we use</strong>
Kaggle- Amazon Reviews dataset


![amazon reviews](https://github.com/lijunwei19/summarize-document-ML/blob/master/Image/a3ce6cec71d51c08af3260dee424137.png)


# How to use our project

<li>  git clone https://github.com/lijunwei19/summarize-document-ML.git </li>
<li>  Recommand using ancaonda build <strong> python 3.5 tensorflow == 1.1.0 </strong></li> 
<li> pip install tensorflow==1.1.0 </li>
<li>  pip install nltk </li>
<li> pip install selectorlib </li>
<li>pip install requests </li>
<li> pip install Flask-WTF</li>
<li> pip install email-validator</li>
<li> pip install Flask</li>
<li> pip install Flask-Jsonpify</li>
      



#  demo
![home](https://github.com/lijunwei19/summarize-document-ML/blob/master/Image/home.png)
![Data_display](https://github.com/lijunwei19/summarize-document-ML/blob/master/Image/Data_display.png)
![text_reivews](https://github.com/lijunwei19/summarize-document-ML/blob/master/Image/text_reviews.png)
![summarized_button](https://github.com/lijunwei19/summarize-document-ML/blob/master/Image/summarize_button.png)
![summarized_reviews](https://github.com/lijunwei19/summarize-document-ML/blob/master/Image/summarized_rewiews.png)
![pie_star](https://github.com/lijunwei19/summarize-document-ML/blob/master/Image/pie_star.png)
![login](https://github.com/lijunwei19/summarize-document-ML/blob/master/Image/login.png)
![register](https://github.com/lijunwei19/summarize-document-ML/blob/master/Image/register.png)


   
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


