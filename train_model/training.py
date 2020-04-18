from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer 
from keras.preprocessing.sequence import pad_sequences
from attention import AttentionLayer
from tensorflow.keras.layers import Input, LSTM, Embedding, Dense, Concatenate, TimeDistributed
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping
from matplotlib import pyplot
from keras import backend as K 
import pandas as pd 
import numpy as np
import os
import tensorflow as tf


def Token(max_text_len,max_summary_len, cleaned_data_file, Training=True ):
    # loading training data
    data=pd.read_csv(cleaned_data_file)
    cleaned_text =np.array(data['cleaned_text'])
    if Training:
        cleaned_summary=np.array(data['cleaned_summary'])

    # choose the length text and summary between 0-max
    short_text=[]
    if Training:
        short_summary=[]
        for i in range(len(cleaned_text)):
            if(len(cleaned_summary[i].split())<=max_summary_len and len(cleaned_text[i].split())<=max_text_len):
                short_text.append(cleaned_text[i])        
                short_summary.append(cleaned_summary[i])

    else:
        for i in range(len(cleaned_text)):
            if(len(cleaned_text[i].split())<=max_text_len):
                short_text.append(cleaned_text[i])        

    if Training:      
        df=pd.DataFrame({'text':short_text,'summary':short_summary})
    else:
        df=pd.DataFrame({'text':short_text})

    # add 'start' and "end " token on sentence
    if Training: 
        df['summary'] = df['summary'].apply(lambda x : 'sostok '+ x + ' eostok')

    # split data into training and testing 
    if Training: 
        x_tr,x_val,y_tr,y_val=train_test_split(np.array(df['text']),np.array(df['summary']),test_size=0.1,random_state=0,shuffle=True) 
    else:
        x_tr,x_val,y_tr,y_val=train_test_split(np.array(df['text']),np.array(df['text']),test_size=0.00001,random_state=0,shuffle=False) 
    
    # Preparing the Tokenizer
    #prepare a tokenizer for reviews on training data
    x_tokenizer = Tokenizer() 
    x_tokenizer.fit_on_texts(list(x_tr))

    #proportion rare words and its total coverage in the entire text
    thresh=4
    cnt=0
    tot_cnt=0
    freq=0
    tot_freq=0

    for key,value in x_tokenizer.word_counts.items():
        tot_cnt=tot_cnt+1
        tot_freq=tot_freq+value
        if(value<thresh):
            cnt=cnt+1
            freq=freq+value

    
    #prepare a tokenizer for reviews on training data
    x_tokenizer = Tokenizer(num_words=tot_cnt-cnt) 
    x_tokenizer.fit_on_texts(list(x_tr))

    #convert text sequences into integer sequences
    x_tr_seq    =   x_tokenizer.texts_to_sequences(x_tr) 
    if Training:
        x_val_seq   =   x_tokenizer.texts_to_sequences(x_val)

    #padding zero upto maximum length
    x_tr    =   pad_sequences(x_tr_seq,  maxlen=max_text_len, padding='post')

    if Training:
        x_val   =   pad_sequences(x_val_seq, maxlen=max_text_len, padding='post')

    #size of vocabulary ( +1 for padding token)
    x_voc   =  x_tokenizer.num_words + 1

    if Training:
        #prepare a tokenizer for reviews on training data
        y_tokenizer = Tokenizer()   
        y_tokenizer.fit_on_texts(list(y_tr))

        thresh=6

        cnt=0
        tot_cnt=0
        freq=0
        tot_freq=0

        for key,value in y_tokenizer.word_counts.items():
            tot_cnt=tot_cnt+1
            tot_freq=tot_freq+value
            if(value<thresh):
                cnt=cnt+1
                freq=freq+value
        #prepare a tokenizer for reviews on training data
        y_tokenizer = Tokenizer(num_words=tot_cnt-cnt) 
        y_tokenizer.fit_on_texts(list(y_tr))

        #convert text sequences into integer sequences
        y_tr_seq    =   y_tokenizer.texts_to_sequences(y_tr) 
        y_val_seq   =   y_tokenizer.texts_to_sequences(y_val) 

        #padding zero upto maximum length
        y_tr    =   pad_sequences(y_tr_seq, maxlen=max_summary_len, padding='post')
        y_val   =   pad_sequences(y_val_seq, maxlen=max_summary_len, padding='post')

        #size of vocabulary
        y_voc  =   y_tokenizer.num_words +1

        print(y_tokenizer.word_counts['sostok'],len(y_tr)   )

        ind=[]
        for i in range(len(y_tr)):
            cnt=0
            for j in y_tr[i]:
                if j!=0:
                    cnt=cnt+1
            if(cnt==2):
                ind.append(i)

        y_tr=np.delete(y_tr,ind, axis=0)
        x_tr=np.delete(x_tr,ind, axis=0)
        ind=[]
        for i in range(len(y_val)):
            cnt=0
            for j in y_val[i]:
                if j!=0:
                    cnt=cnt+1
            if(cnt==2):
                ind.append(i)

        y_val=np.delete(y_val,ind, axis=0)
        x_val=np.delete(x_val,ind, axis=0)
        return x_voc, y_voc, x_tr, y_tr, x_val, y_val
    else:
        return x_tr, x_voc, x_tokenizer

def Building_model(max_text_len, max_summary_len,cleaned_data_file):
    x_voc, y_voc, x_tr, y_tr, x_val, y_val = Token(max_text_len,max_summary_len, cleaned_data_file )
    K.clear_session()

    latent_dim = 300
    embedding_dim=100

    # Encoder
    encoder_inputs = Input(shape=(max_text_len,))

    #embedding layer
    enc_emb =  Embedding(x_voc, embedding_dim,trainable=True)(encoder_inputs)

    #encoder lstm 1
    encoder_lstm1 = LSTM(latent_dim,return_sequences=True,return_state=True,dropout=0.4,recurrent_dropout=0.4)
    encoder_output1, state_h1, state_c1 = encoder_lstm1(enc_emb)

    #encoder lstm 2
    encoder_lstm2 = LSTM(latent_dim,return_sequences=True,return_state=True,dropout=0.4,recurrent_dropout=0.4)
    encoder_output2, state_h2, state_c2 = encoder_lstm2(encoder_output1)

    #encoder lstm 3
    encoder_lstm3=LSTM(latent_dim, return_state=True, return_sequences=True,dropout=0.4,recurrent_dropout=0.4)
    encoder_outputs, state_h, state_c= encoder_lstm3(encoder_output2)

    # Set up the decoder, using `encoder_states` as initial state.
    decoder_inputs = Input(shape=(None,))

    #embedding layer
    dec_emb_layer = Embedding(y_voc, embedding_dim,trainable=True)
    dec_emb = dec_emb_layer(decoder_inputs)

    decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True,dropout=0.4,recurrent_dropout=0.2)
    decoder_outputs,decoder_fwd_state, decoder_back_state = decoder_lstm(dec_emb,initial_state=[state_h, state_c])

    # Attention layer
    attn_layer = AttentionLayer(name='attention_layer')
    attn_out, attn_states = attn_layer([encoder_outputs, decoder_outputs])

    # Concat attention input and decoder LSTM output
    decoder_concat_input = Concatenate(axis=-1, name='concat_layer')([decoder_outputs, attn_out])

    #dense layer
    decoder_dense =  TimeDistributed(Dense(y_voc, activation='softmax'))
    decoder_outputs = decoder_dense(decoder_concat_input)

    # Define the model 
    model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

    
    model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy')
    print(model.summary() )
    import pickle 
    import numpy as np 
    saved_model = pickle.dumps(model) 

    return model,x_tr, y_tr, x_val, y_val

def Training_model(model,x_tr, y_tr, x_val, y_val):
    ### store trained models
    checkpoint_path = "training_1/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    # Create a callback that saves the model's weights
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                    save_weights_only=True,
                                                    verbose=1)
    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1,patience=2)

    history=model.fit([x_tr,y_tr[:,:-1]], 
                      y_tr.reshape(y_tr.shape[0],y_tr.shape[1], 1)[:,1:] ,
                      epochs=50,callbacks=[cp_callback],batch_size=128, 
                      validation_data=([x_val,y_val[:,:-1]], y_val.reshape(y_val.shape[0],y_val.shape[1], 1)[:,1:]))

    # plot 
    pyplot.plot(history.history['loss'], label='train')
    pyplot.plot(history.history['val_loss'], label='test')
    pyplot.legend()
    pyplot.show()


def main():
    # setting traing maximum sentence length for text and summary
    max_text_len=30
    max_summary_len=8
    cleaned_data_file = "amazon-fine-food-reviews/cleaned.csv"
    model,x_tr, y_tr, x_val, y_val = Building_model(max_text_len, max_summary_len,cleaned_data_file)
    Training_model(model,x_tr, y_tr, x_val, y_val)

if __name__ =="__main__":
    main()
