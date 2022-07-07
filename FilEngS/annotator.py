import csv
import os
import pickle
import re
from collections import Counter

import pandas as pd


class Annotator:
 
    # default constructor
    def __init__(self, load_dir=None, datadir='data'):
        dictionary = open(datadir + '/es_dict.pkl', "rb")
        self.es_dict = pickle.load(dictionary)
        
        # EMOJI MODIFIERS
        self.SKIN_MODS = r'[\U0001F3FB-\U0001F3FF]' # unicode range for light to dark skin tone
        self.MOD1 = r'\U0000FE0F'                   # variant selector-16
        self.MOD_PATTERN = self.SKIN_MODS + "|" + self.MOD1

        # EMOJI REGEX - specify range of emojis to count
        self.EMOJIS_REG = [
            #r'[\U000000a6-\U000000ae]',
            r'[\U000006de-\U000006e9]',
            r'[\U000021aa-\U00002b50]',
            r'[\U0000fffc-\U0000fffd]',
            r'[\U0001f0cf-\U0001f4fb]',
            r'[\U0001f504-\U0001f64f]',
            r'[\U0001f680-\U0001f6c0]',
        ]
        self.PATTERN = r'[\U000000a6-\U000000ae]'
        for reg in self.EMOJIS_REG:
           self. PATTERN = self.PATTERN + '|' + reg 
       
        if load_dir == None:
            self.load_dir = './'
        else:
            self.load_dir = load_dir

        self.extension = '.csv'
        self.save_dir1 = 'Tweets Emojis/'
        self.save_dir2 = 'Tweets No Emojis/'
        self.save_dir3 = 'Tweets Metrics/'

        if not os.path.exists(self.save_dir1):
            os.makedirs(self.save_dir1)

        if not os.path.exists(self.save_dir2):
            os.makedirs(self.save_dir2)
 
        if not os.path.exists(self.save_dir3):
            os.makedirs(self.save_dir3)

    # a method for printing data members
    def tag_sentiments(self, tweets_df, filename):
        # File Open
        tweets_df['score'] = 0.0 # add score row
        tweets_df['contains_emoji'] = False 
        
        # Clean Emojis Modifiers
        df_rec = tweets_df.to_records()
        for row in df_rec:
            text = str(tweets_df.at[row[0], 'cleaned'])
            tweets_df.at[row[0], 'cleaned'] = re.sub(self.MOD_PATTERN, '', text) # Remove Modifiers
        
        # Emoji Counters
        Ctr = Counter()
        Unique_ctr = Counter()
        
        # Counts emojis and scores tweets with emojis
        for row in df_rec:
            text = str(tweets_df.at[row[0], 'cleaned'])
            emoji_found = re.findall(self.PATTERN, text) 
            if len(emoji_found) > 0:
                # Count Unique Emojis
                unique_emojis = set(emoji_found)
                for ue in unique_emojis:
                    if self.es_dict['Score'].get(ue) != None:
                        Unique_ctr[ue] += 1
                # Score Emojis
                tweets_df.at[row[0], 'contains_emoji'] = True # row[0] is index
                for emoji in emoji_found:
                    if self.es_dict['Score'].get(emoji) != None:
                        Ctr[emoji] += 1
                        tweets_df.at[row[0], 'score'] = tweets_df.at[row[0], 'score'] + self.es_dict['Score'].get(emoji)
                        
        # Separate Positive and Negative Tweets              
        tweets_emoji_df = tweets_df[tweets_df['contains_emoji'] == True].copy()
        tweets_no_emoji_df = tweets_df[tweets_df['contains_emoji'] == False]
        tweets_emoji_rec = tweets_emoji_df.to_records()
        tweets_emoji_df['is_positive'] = True
        
        for row in tweets_emoji_rec:
            if tweets_emoji_df.at[row[0], 'score'] < 0: 
                tweets_emoji_df.at[row[0], 'is_positive'] = False
                
        # Save Tweets
        tweets_emoji_df.to_csv(self.save_dir1+filename+'_emoji'+self.extension, encoding='utf-8', quoting=csv.QUOTE_ALL)
        print(filename+'_emoji'+self.extension + " saved")
        tweets_no_emoji_df.to_csv(self.save_dir2+filename+'_no_emoji'+self.extension, encoding='utf-8', quoting=csv.QUOTE_ALL)
        print(filename+'_no_emoji'+self.extension + " saved")
        
        # Metrics
        # Positive Tweets
        tweets_positive = tweets_emoji_df[tweets_emoji_df['is_positive'] == True]
        pos_ctr = Counter()
        pos_unique_ctr = Counter()

        tweets_pos_rec = tweets_positive.to_records()
        for row in tweets_pos_rec:
            emoji_found = re.findall(self.PATTERN, str(tweets_positive.at[row[0], 'cleaned'])) 
            if len(emoji_found) > 0:
                # Count Unique Emojis
                unique_emojis = set(emoji_found)
                for ue in unique_emojis:
                    if self.es_dict['Score'].get(ue) != None:
                        pos_unique_ctr[ue] += 1
                for emoji in emoji_found:
                    if self.es_dict['Score'].get(emoji) != None:
                        pos_ctr[emoji] += 1
                        
        tweets_negative = tweets_emoji_df[tweets_emoji_df['is_positive'] == False]
        neg_ctr = Counter()
        neg_unique_ctr = Counter()

        tweets_neg_rec = tweets_negative.to_records()
        for row in tweets_neg_rec:
            emoji_found = re.findall(self.PATTERN, str(tweets_negative.at[row[0], 'cleaned'])) 
            if len(emoji_found) > 0:
                # Count Unique Emojis
                unique_emojis = set(emoji_found)
                for ue in unique_emojis:
                    if self.es_dict['Score'].get(ue) != None:
                        neg_unique_ctr[ue] += 1
                for emoji in emoji_found:
                    if self.es_dict['Score'].get(emoji) != None:
                        neg_ctr[emoji] += 1
        
        #Save Metrics
        count_df = pd.DataFrame.from_dict(Ctr, orient='index')
        count_df = count_df.rename(columns={0:'total_count'})

        unique_count_df = pd.DataFrame.from_dict(Unique_ctr, orient='index')
        unique_count_df = unique_count_df.rename(columns={0:'unique_count'})

        pos_unique_count_df = pd.DataFrame.from_dict(pos_unique_ctr, orient='index')
        pos_unique_count_df = pos_unique_count_df.rename(columns={0:'unique_count_in_positive_tweets'})

        pos_count_df = pd.DataFrame.from_dict(pos_ctr, orient='index')
        pos_count_df = pos_count_df.rename(columns={0:'total_count_in_positive_tweets'})

        neg_unique_count_df = pd.DataFrame.from_dict(neg_unique_ctr, orient='index')
        neg_unique_count_df = neg_unique_count_df.rename(columns={0:'unique_count_in_negative_tweets'})

        neg_count_df = pd.DataFrame.from_dict(neg_ctr, orient='index')
        neg_count_df = neg_count_df.rename(columns={0:'total_count_in_negative_tweets'})
        
        metrics_df = count_df.join(unique_count_df, how="outer")
        mpos_df = pos_count_df.join(pos_unique_count_df, how="outer")
        mneg_df = neg_count_df.join(neg_unique_count_df, how="outer")
        metrics_df = metrics_df.join(mpos_df, how="outer")
        metrics_df = metrics_df.join(mneg_df, how="outer")
        metrics_df = metrics_df.fillna(0).sort_values('total_count', ascending=False)#.applymap(np.int64)
        
        metrics_df.to_csv(self.save_dir3+filename+'_metrics'+self.extension, encoding='utf-8', quoting=csv.QUOTE_ALL)
        print(filename+'_metrics'+self.extension+" saved")
  