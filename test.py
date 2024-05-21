from hazm import word_tokenize
from hazm import Normalizer
from hazm import Stemmer, Lemmatizer
s = 'به گزارش خبرگزاری فارس، کنفدراسیون فوتبال آسیا (AFC) در نامه ای رسمی به فدراسیون فوتبال ایران و باشگاه گیتی پسند زمان  قرعه کشی جام باشگاه های فوتسال آسیا را رسماً اعلام کرد.'
print('s:')
print(s)
normalizer = Normalizer()
normalizer.normalize(s)
print('normalized:')
print(s)
print('tokenized:')
s = word_tokenize(s)
print(s)
stemmer = Stemmer()
print('stemmed:')
for i in s:
    print(stemmer.stem(i), end=' ')
lemmatizer = Lemmatizer()
print('lemmatized:')
for i in s:
    print(lemmatizer.lemmatize(i), end=' ')
