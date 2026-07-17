import re
import nltk
nltk.download("punkt_tab")
from nltk.tokenize import word_tokenize
nltk.download("stopwords")
from nltk.corpus import stopwords, wordnet
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger_eng")
from nltk.stem import WordNetLemmatizer


class TextCleaner:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))

    def clean(self, text):
        text = text.lower()
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"\S+@\S+", "", text)
        text = re.sub(r"#\w+", "", text)
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize(self, text):
        tokens = word_tokenize(text)
        return tokens
    
    def remove_stopwords(self, tokens):
        filtered = [t for t in tokens if t.lower() not in self.stop_words]
        return filtered
    
    def lemmatize_tokens(self, tokens):
        tagged_tokens = nltk.pos_tag(tokens)

        lemmatized_token = []
        for word, tag in tagged_tokens:
            if tag.startswith('J'):
                pos = wordnet.ADJ
            elif tag.startswith('V'):
                pos = wordnet.VERB
            elif tag.startswith('R'):
                pos = wordnet.ADV
            else:
                pos = wordnet.NOUN
            
            lemma = self.lemmatizer.lemmatize(word, pos=pos)
            lemmatized_token.append(lemma)
        
        return lemmatized_token

    def process(self, text):
        print(f"Raw Text: \n{text}\n")

        cleanedtext = self.clean(text)
        print(f"Text After Applying Cleaning: \n{cleanedtext}\n")

        tokens = self.tokenize(cleanedtext)
        print(f"Tokens of cleaned text: \n{tokens}\n")

        filtered_tokens = self.remove_stopwords(tokens)
        print(f"Filtered token: \n{filtered_tokens}\n")

        lemmatized_tokens = self.lemmatize_tokens(filtered_tokens)
        print(f"Lemmatized Tokens: \n{lemmatized_tokens}\n")

        return lemmatized_tokens


sample = """
    Just watched an AMAZING cricket match!! 🏏 
    Check highlights at https://cricinfo.com or email us at cricket@news.com
    #IPL2024 #Cricket The batting was absolutely incredible... 
    Don't miss the replays, they're running all matches again!!!
"""

t = TextCleaner()
t.process(sample)