import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np #繪製mask圖形




def cloud(image, text, max_word, max_font, random):
    lines = []
    with open('net/home/stopwords_en.txt') as f:
        lines = [line.rstrip() for line in f]
    stopwords = set(STOPWORDS)
    stopwords.update(['us', 'one', 'will', 'said', 'now', 'well', 'man', 'may',
    'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
    'put', 'seem', 'asked', 'made', 'half', 'much',
    'certainly', 'might', 'came', 'definition', 'S'])
    stopwords.update(lines)


    wc = WordCloud(
    background_color="white",
    colormap="hot",
    max_words=max_word,
    mask=image,
    stopwords=stopwords,
    max_font_size=max_font,
    random_state=random
    )
    #文字處理

    # generate word cloud
    wc.generate(text)

    # create coloring from image
    image_colors = ImageColorGenerator(image)

    plt.figure(figsize=(200,200))
    plt.imshow(wc, interpolation="bilinear")
    wc.to_file('report/keyword/img/wordcloud.png')












