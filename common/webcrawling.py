import requests
from requests import get
from bs4 import BeautifulSoup

def URLRequest(page_num = '1', ftrset = '1', base_url = 'https://gall.dcinside.com/board/lists/'):
   
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

  response = get(f"{base_url}?id=dcbest&page={parameter.page_num}&_dcbest={parameter.ftrset}", headers=headers)
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
  # /이 함수는 기존에 URLRequest 함수를 통해서 리턴한 beautifulSoup 타입의 URL내부 컨텐츠를 Post 단위로 분리해서 List 형태로 취하는 데이터 정제함수이다. 
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
    
    

