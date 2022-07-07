import csv
import re
import tweetokenize.tokenizer as tt
import emoji
import pandas as pd


class Tokenizer:
    
    def __init__(self):
        ZEROWIDTH = r"[\u200d]+" # ZEROWIDTH SEPARATOR
        SKIN_MODS = r'[\U0001F3FB-\U0001F3FF]' # unicode range for light to dark skin tone
        MOD1 = r'\U0000FE0F'                   # variant selector-16
        MOD2 = r'\U00002642'                   # Gender symbol female 
        MOD3 = r'\U00002640'                   # Gender symbol male


        self.MOD_PATTERN = SKIN_MODS + "|" + MOD1 + "|" + MOD2 + "|" + MOD3 +  "|" + ZEROWIDTH
        self.mentions = r"@[^ ]+"
        self.links = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+"
        self.repeating = r'([A-Za-z])\1{3,}'
        self.foreign = r"[^\x00-\xff\u2000-\u26FF]+" #Non Ascii Character or Unicode Symbols
        self.tokenizer = tt.Tokenizer(custom_hashtags=False, ignorestopwords=False, lowercase=True, normalize=3)
        self.cleaned = []
        self.length = []

    def clean(self, tweets, save_dir='./'):
        self.cleaned.clear()
        self.length.clear()
        for i in range(len(tweets)):
            text = str(tweets[i])
            text = text.lower() # lowercase
            text = re.sub(self.mentions, 'MENTION', text) # convert mentions to <mentions>
            text = re.sub(self.links, 'LINK', text) # convert links to <links>
            text = re.sub(self.repeating, r'\1\1\1', text) # normalize repeating letts
            text = emoji.demojize(text) # convert :) to :happy:
            text = re.sub(self.foreign, ' FSF ', text) # convert all non ascii to <foreign>
            text = emoji.emojize(text) # convert back :happy: to :) emoji
            text = re.sub(self.MOD_PATTERN, '', text) 
            tokens = self.tokenizer.tokenize(text)
            tokenized_string = ''
            for tk in tokens:
                tokenized_string = tokenized_string + tk + ' '        
            self.cleaned.append(tokenized_string)  # update the row text
            self.length.append(len(tokens))
        
        results = {'cleaned':self.cleaned,'sequence_length':self.length}
        return pd.DataFrame(results)