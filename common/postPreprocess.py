import pandas as pd 
def dataTransformation(CookedPost_list):
    '''데이터 전처리 과정에서 얻은 Post 클래스를 원소로 저장한 리스트를 pandas 형태로 가공하는 함수입니다. 
  Args:
    CookedPost_list (list) : 데이터 전처리 과정에서 얻은 Post 클래스를 원소로 저장한 리스트입니다.

  Return:
    CookedPost_list를 pandas dataFrame 형태로 변환하여 리턴합니다.
    '''

    dataFrame_empty = pd.DataFrame(columns = ['ID', 'USER NAME', 'VIEWS', 'LIKES', 'REPLIES', 'TITLE', 'CONTENTS', 'KEYWORDS', 'URL']) #열은 columns로 지정, 행은 index로 지정 (dtypes should be LIST)
    ''' 사전에 정의한 Post의 클래스 정보는 아래와 같다.
        class Post():
        id = 'YYMMDD-#####'
        user = ''
        views = 0
        likes = 0
        replies = 0
        title = 'what a wonderful world.'
        contents = 'This is the whole sentence of the single post.'
        keywords = []
        url = 'https://gall.dcinside.com'
        '''
    CookedPost_list = CookedPost_list

    #저장하고자 하는 데이터를 넣는 작업 (조회수를 기준으로 정렬할 것임.)
    cnt = 1
    for post in sorted(CookedPost_list, key = lambda x: x.views, reverse = True):
        print(post.contents)
        dataFrame_empty.loc[cnt] = [post.id, post.user, post.views, post.likes, post.replies, post.title, post.contents, post.keywords, post.url]
        cnt+=1

        if cnt == len(CookedPost_list):
            dataFrame_result = dataFrame_empty


    return dataFrame_result
