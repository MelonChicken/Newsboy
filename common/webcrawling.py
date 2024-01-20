from urllib import response
import requests
from requests import get
from bs4 import BeautifulSoup

def URLRequest(page_num = 1, ftrset = '1', intended_date = 'YYYY-MM-DD', base_url = 'https://gall.dcinside.com/board/lists/'):
  '''입력받은 URL에 대하여 웹스크래핑을 하는 함수입니다. 디시인사이드 실시간베스트에 특화된 함수입니다.
  Args:
    page_num (int) : 크롤링하고자 하는 페이지 넘버입니다.
    ftrset (int) : 디시인사이드가 제공하는 실시간 베스트, 실베 라이트, 실베 나이트의 필터링 설정입니다.
    intended_date (str) : 분석하고자하는 날짜를 저장합니다.
    base_url (str) : 디시인사이드 실시간베스트 url을 기본 값으로 세팅했습니다.
  Return:
    크롤링한 내용이 BeautifulSoup 자료형으로 리턴됩니다.
  '''
  class params() :
      page_num = 1

      ftrset = '1'


  # 헤더 설정
  headers = {
      'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

  # 1 : 실시간 베스트
  # 2 : 실시간 베스트? 1하고 2의 차이를 모르겠음
  # 3 : 실베 라이트 (무슨 내용인지 모르겠음)
  # 4 : 실시간 베스트 & 실베 라이트
  # 5 : 실베 나이트 (무슨 내용인지 모르겠음 ㅋㅋㅋㅋ)
  # 6 : 실시간 베스트 & 실베 나이트
  # 7 : 실시간 베스트? 1, 2 와의 차이를 모르겠음
  # 8 : 실베 라이트 & 실베 나이트
  # 9 : ALL

  parameter = params()
  parameter.page_num = page_num
  parameter.ftrset = ftrset

  response = get(f"{base_url}?id=dcbest&list_num=100&page={parameter.page_num}&_dcbest={parameter.ftrset}", headers=headers)
  # 목표는 디시인사이드 실시간 베스트 갤러리 타겟팅한 크롤링 진행

  # Extract the data from the response

  if response.status_code != 200:
    print(f"Can't request website, and the response code is {response.status_code}. \n")
    return False
  else:
  # print(response)
  #  print(response.url)
    resp_content = response.content
    soup_content = BeautifulSoup(resp_content, 'html.parser')
    # Print the data
    soup_innerContent = soup_content.find('tbody').find_all('tr', class_ = "us-post")

    #각 tbody내에서 tr 태그가 있는 컨텐츠 하나하나를 dictionary의 item으로 받는다.
    #각 게시물들은 us-post라는 클래스명을 가지고 있는걸 확인   

    return soup_innerContent
  
def PreprocessPost(soup_innerContent, intended_date = 'YYYY-MM-DD'):
  """이 함수는 기존에 URLRequest 함수를 통해서 리턴한 beautifulSoup 타입의 URL내부 컨텐츠를 Post 단위로 분리해서 List 형태로 취하는 데이터 정제함수입니다.
  
  Args:
    soup_innerContent (bs4)  : URLRequest를 통해 얻은 크롤링 대상 본문 전체입니다.
    intended_date (str) : 크롤링하고자하는 대상 날짜를 입력합니다. (하지만 현재로서는 URLRequest로 먼저 날짜 선별을 하는것이 더 효율적이기 때문에 실질적인 기능은 없는 인자입니다.)
  
  Return:
    Post 클래스로 저장된 각각의 게시물 정보들을 저장한 리스트 변수 Cookedpost_list를 리턴합니다.
         """
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
  
  RawPost_list = soup_innerContent

  CookedPost_list = []

  for post in RawPost_list:
    #print('\n\n')
    #print(post)

    tmp_post = Post()
    written_date = post.find('td', class_ = 'gall_date').attrs['title'] #YYYY-MM-DD
    cooked_written_date = written_date[2:4] + written_date[5:7] + written_date[8:10]
    #string을 index로 접근할 때에는 [a:b]가 a이상 b미만임을 기억해야 한다.
    #print(f'cooked_date is {cooked_written_date}')

    tmp_post.id = f'{cooked_written_date}-{post.find("td", class_ = "gall_num").text}'
    #print(f'tmp_post.id = {tmp_post.id}')
    
    tmp_post.user = post.find('span', class_ = 'nickname').attrs['title']
    tmp_ip = post.find('span', class_ = 'ip')

    if tmp_ip != None:
      tmp_post.user = f'{tmp_post.user} {tmp_ip.text}'

    #print(f'tmp_post.user = {tmp_post.user}')

    tmp_post.views = int(post.find('td', class_ = 'gall_count').text)
    #print(f'tmp_post.views = {tmp_post.views}')

    tmp_post.likes = int(post.find('td', class_ = 'gall_recommend').text)
    #print(f'tmp_post.likes = {tmp_post.likes}')
    
    tmp_post.replies = post.find("span", class_ = 'reply_num').text[1:-1]
    #보이스 리플이라는 댓글 기능은 댓글 카운트 시 '/'를 통해 구분하므로 이로인해 발생하는 오류를 막아주기 위해 조건 추가
    if '/' in tmp_post.replies:
       tmp_post.replies = (tmp_post.replies).split('/')
       tmp_post.replies = int(tmp_post.replies[0]) + int(tmp_post.replies[1])
    else:
       tmp_post.replies = int(tmp_post.replies)
    #print(f'tmp_post.replies = {tmp_post.replies}')

    tmp_postA = post.find('td', class_ = "gall_tit").find('a')
    #print(f'tmp_postA = {tmp_postA}')
    tmp_post.title = tmp_postA.text
    #print(f'tmp_post.title = {tmp_post.title}')
    
    tmp_post.url = tmp_post.url + tmp_postA.attrs['href']
    #print(f'tmp_post.url = {tmp_post.url}')

    CookedPost_list.append(tmp_post)

    #print(CookedPost_list)
  return CookedPost_list

def postContentScrapping (CookedPost_list):
  '''데이터 전처리 과정에서 얻은 Post 클래스를 원소로 저장한 리스트를 인수로 받아 해당 post의 content를 저장하여 리스트를 다시 리턴하는 함수입니다.
  Args:
    CookedPost_list (list) : 데이터 전처리 과정에서 얻은 Post 클래스를 원소로 저장한 리스트입니다.
  Return:
    Content를 추가한 CookedPost_list를 리턴합니다.
  '''
  CookedPost_list = CookedPost_list
  ContentAddedPost_list = []
  for post in CookedPost_list:
    
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

    response = get(post.url, headers=headers)

    if response.status_code != 200:
      print(f"Can't request website, and the response code is {response.status_code}. \n")
      post.contents = f"Can't request website, and the response code is {response.status_code}. \n"
      ContentAddedPost_list.append(post)
      continue
    
    else:
       resp_content = response.content
       #print(resp_content)
       soup_content = BeautifulSoup(resp_content, 'html.parser')
       if soup_content == None:
          print('cannot find the content')
       
       post_content = soup_content.find('div', class_ = 'writing_view_box').get_text()
       post_content = post_content.replace('&nbsp;', '  ')

       post.contents = post_content
       ContentAddedPost_list.append(post)
       #print(f"Current Post's title is {ContentAddedPost_list[-1].title} and content is {ContentAddedPost_list[-1].content}")
       
  return ContentAddedPost_list


             


def DateChecker(page_num = 1, ftrset = '1', intended_date = 'YYYY-MM-DD', base_url = 'https://gall.dcinside.com/board/lists/'):
  
  '''입력받은 URL에 대하여 분석하고자 하는 날짜의 게시물들을 타겟팅하는 함수입니다. 디시인사이드 실시간베스트에 특화된 함수입니다.
  Args:
    page_num (int) : 크롤링하고자 하는 페이지 넘버입니다.
    ftrset (str) : 디시인사이드가 제공하는 실시간 베스트, 실베 라이트, 실베 나이트의 필터링 설정입니다.
    intended_date (str) : 분석하고자하는 날짜를 저장합니다.
    base_url (str) : 디시인사이드 실시간베스트 url을 기본 값으로 세팅했습니다.
  Return:
    게시물들의 게시 날짜를 리스트 안에 int로 저장한 변수 date_collect를 리턴합니다. 
  '''
  class params() :
      page_num = 1

      ftrset = '1'

  # 헤더 설정
  headers = {
      'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
  #parammeter 변수 저장
  parameter = params()
  parameter.page_num = page_num
  parameter.ftrset = ftrset

  response = get(f"{base_url}?id=dcbest&list_num=100&page={parameter.page_num}&_dcbest={parameter.ftrset}", headers=headers)
  # 목표는 디시인사이드 실시간 베스트 갤러리 타겟팅한 크롤링 진행

  # Extract the data from the response

  if response.status_code != 200:
    print(f"Can't request website, and the response code is {response.status_code}. \n")
    return False
  else:
  # print(response)
  #  print(response.url)
    resp_content = response.content
    soup_content = BeautifulSoup(resp_content, 'html.parser')
    target_date = intended_date    
    # Print the data
    soup_userContent = soup_content.find('tbody').find_all('tr', class_ = "us-post")
    #특정 날에 게시물이 얼마정도 있는지 int 형태를 통해 저장한다.
    # date_tracker['YYYY-MM-DD'] = ####
    #해당 값을 한페이지 당 게시물 (100) 수로 나눈다면 페이지가 자동으로 계산될 것.
    date_collect = []

    for post in soup_userContent:
      tmp_date = str(post.find('td', class_ = "gall_date").attrs['title'][:10])

      date_collect.append(tmp_date)

  return date_collect, page_num

def Bookmarker(date_postNum ={}, date_collect = ['Need to be initialized'], postNum = 0, page_num = 1, ftrset = '1', intended_date = 'YYYY-MM-DD', base_url = 'https://gall.dcinside.com/board/lists/'):
  ''' DateChecker를 통해 얻은 게시날짜 모음을 분석하는 함수로, 목표는 게시물 날짜 구별입니다.

      Args:
        기존 DateChecker의 args를 저장합니다.
        date_postNum (dict) : bookmarker를 통해 얻은 페이지 정보를 저장하는 dictionary 변수입니다.
        date_collect (list) : DateChecker 를 통해 얻은 해당 페이지의 게시 날짜 리스트입니다.
        postNum (int) : bookmarker 과정 중 지금까지 확인한 게시물의 수를 저장하는 int 변수입니다. 
      
      Return:
        (1) 날짜별 저장된 게시물 수를 dictionary 형태로 리턴합니다. 
        (2) 지금까지 확인한 게시물의 수를 int로 리턴합니다.

  '''
  date_postNum = date_postNum
  
  #for문 안에서 현재 트래킹하고 있는 날짜를 구분하기 위한 변수
  current_date = ''

  #전체 게시물 수를 저장하기 위한 변수
  postNum = postNum

  for item in date_collect:
    tmp_date = item
    #print(f'\n##현재 접근중인 게시 날짜는 다음과 같습니다. {item}##\n')
    if len(list(date_postNum.keys())) != 0:
      if current_date == '':
        current_date = tmp_date
        postNum += 1

      elif current_date == tmp_date:
         postNum +=1
         #print('1-1')

      else:
        date_postNum[current_date] = postNum - sum(date_postNum.values())
        #print(f'current_date = {current_date}[{date_postNum[current_date]}]\npostNum = {postNum}')
        current_date = tmp_date
        postNum +=1
        #print('1-2')
         
    else:
      if current_date == '':
        current_date = tmp_date
        postNum += 1
        #print('2-1')
      
      elif current_date == tmp_date:
        postNum += 1
        #print('2-2')

      else:
        date_postNum[current_date] = postNum
        #print(f'\nINITIALIZED\ncurrent_date = {current_date}[{date_postNum[current_date]}]\npostNum = {postNum}')
        current_date = tmp_date
        postNum +=1
        #print('2-3')


  return date_postNum, postNum
      


def DateChecker_Handle (flag = False, page_num = 1, postNum = 0, intended_date = '2024-01-11', 
  date_postNum = {}):
  '''DateChecker 함수와 bookmarker 함수를 사용해 게시 날짜에 따른 게시물 수를 정리하는 함수입니다.
    Args:
      flag (boolean) : 원하는 날짜의 게시물 수를 찾을 때까지 while문을 진행시키는 플래그 역할의 boolean 변수입니다.
      page_num (int) : 검색을 시작하는 page number를 설정하는 integer 변수입니다.
      postNum (int) : 검색 과정에서 수합한 게시물의 총 개수를 저장하는 integer 변수입니다.
      intended_date (str) : 알아내고자 하는 날짜를 저장하는 string 변수입니다.
      date_postNum (dictionary) : 게시날짜를 key로, 게시물 수를 value로 저장하는 dictionary 변수입니다.
    Return:
      (1) 특정 게시 날짜에 업로드된 최초의 게시물의 페이지 위치와 날짜를 저장한 dictionary 변수를 리턴합니다.
  '''
  flag = False
  page_num = 1
  postNum = 0
  intended_date = '2024-01-11'
  date_postNum = {}

  while not (flag):
      date_collect, page_num = DateChecker(page_num=page_num, intended_date=intended_date)
      date_postNum, postNum = Bookmarker(date_postNum=date_postNum, date_collect= date_collect, page_num=page_num, postNum=postNum)

      if intended_date in date_postNum.keys():
          flag = True
          #print(f'게시 날짜에 따른 게시물 수는 다음과 같습니다. {date_postNum}')
          """  elif page_num == 10:
          flag = True
          print(f'[overflowError] 게시 날짜에 따른 게시물 수는 다음과 같습니다. {date_postNum}')"""
      
      else:
          page_num += 1

      # print('#'*10)
      # print(f'현재 page_num은 {page_num-1}이고, date_postNum 상태는 아래와 같습니다. \n {date_postNum}\n')
      # print(f'현재 postNum은 {postNum}입니다.')
      # print('#'*10)
  date_postNum['totalPostNum'] = postNum

  
  datekeyList = sorted(date_postNum.keys(), reverse=True)[1:]
  date_page = {}
  cnt = 0

  for key in datekeyList:
      cnt += date_postNum[key]
      
      flag = int(str(cnt)[-1])
      if flag == 0:
          date_page[key] = int(cnt/100)
      else:
          date_page[key] = int(cnt/100) + 1
      
  return date_page
