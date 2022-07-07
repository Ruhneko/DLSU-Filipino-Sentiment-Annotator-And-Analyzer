# Filipino English Sentiment Tagger (FilEngS)
!!! IN PROGRESS !!!

## Dependencies
- emoji
- pandas
- sklearn
- tensorflow
- seaborn
- demoji
- scikeras
- gensim
- pinoy tweetokinzer : https://github.com/atmarges/pinoy_tweetokenize

### FilEngS Data folder


https://drive.google.com/drive/folders/16Eol_A6Xr_vMBqaWq9bUO_LrhPS-oBeI?usp=sharing


By default place it in the same directory as your python code/jupyter notebook. 


You may assign a different location if you choose, but it needs to be specified on code intialization (see below)

## Installation
pip install git+https://github.com/Ruhneko/Filipino-English-Sentiment-Tagger.git

## API

### Tokenizer
Tokenizes a tweet content contained in a Series and returns a Dataframe with the ``cleaned`` and ``sequence length`` columns.
```python
from FilEngs import Tokenizer
tweets_df = pd.read_csv('file.csv', index_col=[0])
tokenize = Tokenizer()
tweets_df['cleaned', 'sequence_length'] = tokenize.clean(tweets_df['tweet'])
```

### Annotator
Annotates a DataFrame with the ``cleaned`` column and saves the results into 3 files, each in their resepctive folder:  Tweets Emojis folder: ***yourFileName_emoji.csv*** and Tweets No Emojis folder: ***yourFileName_no_emoji.csv*** and Tweets Metrics folder: ***yourFileName_metrics.csv***

```python
from FilEngS import Annotator
annotate = Annotator(<your folder>, <theFilEngS data folder>)
annotate.tag_sentiments(<your csv file>)
```

### Classifier/Analyzer
Classify data with our pre-built model. Set ``strip=True`` to strip emojis.
```python
from FilEngS import SentiClassifier
classifier = SentiClassifier(<theFilEngS data folder>)
X_tweets = <your tweets>
predictions = classifier.predict(X_tweets, strip=False)
```

**or**

Test our models performance on your own annotations
```python
from FilEngS import Classifier
classifier = Classifier(< theFilEngS data folder>)
X_tweets = <your tweets>
y_labels = <your annotations>
rep = classifier.pred_report(X_tweets, y_labels, strip=False)
```

## Additional Data Sources

**Thyphoon Yolanda Related Tweets**

***imperialjoseph@rocketmail.com***

Imperial, J. M., Orosco, J., Mazo, S. M., & Maceda, L. (2019). Sentiment
analysis of typhoon related tweets using standard and bidirectional recurrent
neural networks.

**COVID-19 Vaccine Related Tweets**

***charlyn.villavicencio@bulsu.edu.ph***

Villavicencio, C., Macrohon, J. J., Inbaraj, X. A., Jeng, J.-H., & Hsieh, J.-G. (2021). Twitter Sentiment Analysis towards COVID-19 Vaccines in the Philippines Using Naïve Bayes. Information, 12(5), 204. https://doi.org/10.3390/info12050204

## Developers

Sean Co, Nicholas Custodio, Alexis Dela Cruz, Martin Sanchez

Adviser:

Edward Tighe

DLSU College of Computer Studies
