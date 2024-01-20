import pandas as pd 
from common.nlpBase import preprocessKOR

def Content2Keyword(CookedPost_list):
    '''개별 post의 contents와 title 정보를 통해 해당 게시물의 corpus를 저장하고 keyword를 분석하는 함수입니다. 
  Args:
    CookedPost_list (list) : 데이터 전처리 과정에서 얻은 Post 클래스를 원소로 저장한 리스트입니다.

  Return:
    corpus, keyword property가 추가된 KeywordAdded_list를 리턴합니다.
    '''
    CookedPost_list = CookedPost_list
    KeywordAdded_list = []

    ''' 사전에 정의한 Post의 클래스 정보는 아래와 같다.
        class Post():
        id = 'YYMMDD-#####'
        user = ''
        views = 0
        likes = 0
        replies = 0
        title = 'what a wonderful world.'
        contents = 'This is the whole sentence of the single post.'
        corpus = []
        keywords = []
        url = 'https://gall.dcinside.com'
        '''
    for post in CookedPost_list:
        tmp_title = post.title
        tmp_contents = post.contents
        tmp_wholePie = tmp_title + ' ' + tmp_contents

        tmp_corpus, tmp_word2id, tmp_id2word = preprocessKOR(tmp_wholePie)

        tmp_corpusWord = [tmp_id2word[id_] for id_ in tmp_corpus]
        post.corpus = tmp_corpusWord
        
        tmp_statistics_wordID = {}

        cnt = 0
        for id in sorted(tmp_corpus):

            if cnt == 0:
                tmp_word = tmp_id2word[id]

            elif tmp_word == tmp_id2word[id]:

                if not tmp_word in tmp_statistics_wordID.keys():
                    tmp_statistics_wordID[tmp_word] = 2

                else:
                    tmp_statistics_wordID[tmp_word] +=1

            else:
                tmp_word = tmp_id2word[id]

            cnt+=1

        tmp_sorted_list = sorted(tmp_statistics_wordID, key = lambda x: tmp_statistics_wordID[x], reverse = True)

        #corpus의 양이 적을 경우 빈 리스트가 형성될 수 있다는 것 또한 고려해야 한다.
        index_ = int(len(tmp_sorted_list)*0.2)

        if index_ != 0:
            post.keywords = tmp_sorted_list[:index_]
            KeywordAdded_list.append(post)

    return KeywordAdded_list


def dataTransformation(CookedPost_list):
    '''데이터 전처리 과정에서 얻은 Post 클래스를 원소로 저장한 리스트를 pandas 형태로 가공하는 함수입니다. 
  Args:
    CookedPost_list (list) : 데이터 전처리 과정에서 얻은 Post 클래스를 원소로 저장한 리스트입니다.

  Return:
    CookedPost_list를 pandas dataFrame 형태로 변환하여 리턴합니다.
    '''

    dataFrame_empty = pd.DataFrame(columns = ['ID', 'USER NAME', 'VIEWS', 'LIKES', 'REPLIES', 'TITLE', 'CONTENTS', 'CORPUS', 'KEYWORDS', 'URL'])
     #열은 columns로 지정, 행은 index로 지정 (dtypes should be LIST)
    ''' 사전에 정의한 Post의 클래스 정보는 아래와 같다.
        class Post():
        id = 'YYMMDD-#####'
        user = ''
        views = 0
        likes = 0
        replies = 0
        title = 'what a wonderful world.'
        contents = 'This is the whole sentence of the single post.'
        corpus = []
        keywords = []
        url = 'https://gall.dcinside.com'
        '''
    CookedPost_list = CookedPost_list

    #저장하고자 하는 데이터를 넣는 작업 (조회수를 기준으로 정렬할 것임.)
    cnt = 1
    for post in sorted(CookedPost_list, key = lambda x: x.views, reverse = True):
        # print(post.contents)
        dataFrame_empty.loc[cnt] = [post.id, post.user, post.views, post.likes, post.replies, post.title, post.contents, post.corpus, post.keywords, post.url]
        cnt+=1

        if cnt == len(CookedPost_list):
            dataFrame_result = dataFrame_empty


    return dataFrame_result
