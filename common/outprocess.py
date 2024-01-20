from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import matplotlib.pyplot as plt

""" #데이터를 할때마다 크롤링하면 테스트 시간이 너무 길어지므로 파일을 저장하여 진행한다.
file_name = 'test.xlsx'
test_excel = pd.read_excel(file_name, engine= 'openpyxl')

#엑셀파일 안에 들어있는 Keywords는 string 형태로 저장되어있기 때문에 고쳐줬다.
keyWord_list = list(test_excel['KEYWORDS'])
keyWord_list = [literal_eval(item) for item in keyWord_ list]"""

def Keyword2Wordcloud(post_dataFrame):
    '''pandas dataframe 형태로 저장되어있는 post 관련 정보들을 받아서 그 중 keywords 부분을 워드클라우드를 통해 시각화하는 함수입니다.
    Args:
        post_dataFrame (pandas dataFrame) : pandas dataframe 형태로 post 관련 정보를 저장한 인수

    returns:
        None  
    '''
    keyWords_list = post_dataFrame['KEYWORDS'].values.tolist()
    stopWord_list = list(pd.read_table('sources\\Korean_StopWords.txt', sep=', '))
    totalKeyword_list = sum(keyWords_list, [])

    #리스트 형태의 keywords를 모두 합쳐서 워드 클라우드 진행
    whole_keywords = (' ').join(totalKeyword_list)

    #불용어 설정 추가 (source의 txt 파일 사용)
    for word in stopWord_list:
        STOPWORDS.add(word)

    wordcloud = WordCloud(width = 1024, height=768, background_color='white',
                        max_words=100, stopwords=STOPWORDS, 
                        font_path='sources\\font\\한국기계연구원_Light.ttf').generate(whole_keywords)
    #.generate method는 단어별 출현 빈도수를 비율로 반환하는 딕셔너리 형태의 객체를 반환한다. (하지만 자료형은 여전히 wordcloud이다.)
    plt.figure(figsize=(8,6))
    plt.imshow(wordcloud)
    plt.axis("off") #눈금 제거
    plt.show()

    wordcloud.to_file('test\\test.jpg')
