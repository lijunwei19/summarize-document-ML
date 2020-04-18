import matplotlib.pyplot as plt
import pandas as pd 

def plot_text_len_distribution(file_name):
    data=pd.read_csv(file_name)
    text_word_count = []
    summary_word_count = []

    # populate the lists with sentence lengths
    for i in data['cleaned_text']:
        text_word_count.append(len(i.split()))

    for i in data['cleaned_summary']:
        summary_word_count.append(len(i.split()))

    length_df = pd.DataFrame({'text':text_word_count, 'summary':summary_word_count})

    length_df.hist(bins = 30)
    plt.show()

def main():
    plot_text_len_distribution("amazon-fine-food-reviews/cleaned.csv")

if __name__ == '__main__':
    main()