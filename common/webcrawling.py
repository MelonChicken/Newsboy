import requests
from requests import get
from bs4 import BeautifulSoup

def URLRequest(page_num = '1', ftrset = '1', intended_date = 'YYYY-MM-DD', base_url = 'https://gall.dcinside.com/board/lists/'):
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
      page_num = '1'

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
    keywords = []
    url = 'https://gall.dcinside.com'
  
  RawPost_list = soup_innerContent

  CookedPost_list = []

  for post in RawPost_list:
    print('\n\n')
    #print(post)

    tmp_post = Post()
    written_date = post.find('td', class_ = 'gall_date').attrs['title'] #YYYY-MM-DD
    cooked_written_date = written_date[2:4] + written_date[5:7] + written_date[8:10]
    #string을 index로 접근할 때에는 [a:b]가 a이상 b미만임을 기억해야 한다.
    #print(f'cooked_date is {cooked_written_date}')

    tmp_post.id = f'{cooked_written_date}-{post.find("td", class_ = "gall_num").text}'
    print(f'tmp_post.id = {tmp_post.id}')
    
    tmp_post.user = post.find('span', class_ = 'nickname').attrs['title']
    tmp_ip = post.find('span', class_ = 'ip')

    if tmp_ip != None:
      tmp_post.user = f'{tmp_post.user} {tmp_ip.text}'

    print(f'tmp_post.user = {tmp_post.user}')

    tmp_post.views = int(post.find('td', class_ = 'gall_count').text)
    print(f'tmp_post.views = {tmp_post.views}')

    tmp_post.likes = int(post.find('td', class_ = 'gall_recommend').text)
    print(f'tmp_post.likes = {tmp_post.likes}')
    
    tmp_post.replies = int(post.find("span", class_ = 'reply_num').text[1:-1])
    print(f'tmp_post.replies = {tmp_post.replies}')

    tmp_postA = post.find('td', class_ = "gall_tit").find('a')
    #print(f'tmp_postA = {tmp_postA}')
    tmp_post.title = tmp_postA.text
    print(f'tmp_post.title = {tmp_post.title}')
    
    tmp_post.url = tmp_post.url + tmp_postA.attrs['href']
    print(f'tmp_post.url = {tmp_post.url}')

    CookedPost_list.append(tmp_post)

    #print(CookedPost_list)
  return CookedPost_list
    
def DateChecker(page_num = '1', ftrset = '1', intended_date = 'YYYY-MM-DD', base_url = 'https://gall.dcinside.com/board/lists/'):
  '''입력받은 URL에 대하여 분석하고자 하는 날짜의 게시물들을 타겟팅하는 함수입니다. 디시인사이드 실시간베스트에 특화된 함수입니다.
  Args:
    page_num (int) : 크롤링하고자 하는 페이지 넘버입니다.
    ftrset (int) : 디시인사이드가 제공하는 실시간 베스트, 실베 라이트, 실베 나이트의 필터링 설정입니다.
    intended_date (str) : 분석하고자하는 날짜를 저장합니다.
    base_url (str) : 디시인사이드 실시간베스트 url을 기본 값으로 세팅했습니다.
  Return:
    해당 날짜의 게시물을 담고 있는 페이지 범위를 int 자료형으로 리턴합니다.
  '''
  class params() :
      page_num = '1'

      ftrset = '1'


  # 헤더 설정
  headers = {
      'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

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
    date_tracker = []
    check_date = ''
    for post in soup_userContent:
      tmp_date = str(post.find('td', class_ = "gall_date").attrs['title'][:10])
      if check_date == '':
        check_date = tmp_date
      elif check_date == tmp_date:
        continue
      else:
        #if (tmp_date == target_date) or (check_date == target_date):

    