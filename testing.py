# """ import sys
# sys.path.append('..')
# from common.nlpBase import preprocessKOR, create_co_matrix, most_similar

# import konlpy
# from konlpy.tag import Okt, Hannanum, Kkma

# sample_text01 = "용서는 곧 사랑이다. 고결하고 아름다운 사랑의 형태이다. 사랑이 없는 사람은 쉽게 용서하지 못한다. 용서는 평화와 행복을 그 보답으로 준다. 그대, 용서함으로써 행복 하라! 용감한 자만이 용서할 줄 알고 비겁한 자는 용서하지 않는다. 용서는 남에게는 자주 베풀지만 자신에게는 베풀지 마라. 누군가가 당신에게 피해를 입혔다면 인내심을 가지고 그들을 대하라. 부드러운 말은 상처를 소독한다. 용서는 상처를 치유하고, 망각은 흉터를 지운다. 상처를 낫게 하려고 논쟁을 벌이는 것보다 조용히 상처를 기다리는 편이 더 낫다. 용서가 신성하듯이 극도의 어려움을 참고 견디는 것은 훌륭하다. 용서하는 것은 아름답다.용서하지 않으면 분노를 되새김질하게 되고 과거의 기억과 상처에 매달리게 되면서 자기 자신의 노예가 되는 것이다. 상처에 집착하는 것은 자기 자신을 불행하게 만든다. 용서는 자신을 위해 상처를 떨쳐버리는 것이다. 상처의 진정한 치유는 용서에서 온다. 용서는 자신 안에 갇힌 에너지를 밖으로 내보내 세상에서 선한 일을 하는데 쓸 수 있게 한다. 용서는 삶 속에서 실천할 수 있는 큰 수행이다. 용서할 때는 마음에 문을 열 수 있다. 용서하는 마음은 상처 준 이들을 받아들이는 마음이다. 진정한 용서는 마음의 쇠사슬에 묶여 있던 이들을 위안해주고 안심시켜 주는 일이다. 자신을 멍들게 하고 파괴시킨 미움과 원망의 마음에서 스스로 벗어나는 일이다. 그대를 고통스럽게 만든 사람에게 나쁜 감정을 키워나가면 그대 자신의 마음의 평화만 깨어질 뿐이다. 그대가 그를 용서한다면, 그대 마음은 평온을 되찾을 것이다. 누군가를 용서한다는 것은 알고 보면 자신을 위한 것이다. 타인을 용서치 못하면 스스로 건너야 하는 다리를 부스는 것이나 마찬가지다. 죄를 저지를 자와 피해를 입은 자, 모두에게 용서가 필요한 법이다. 약자는 결코 용서할 수가 없다. 용서는 강자의 속성이다. 증오는 사랑만이 극복할 수 있다. 용서할 수는 있어도 잊을 수는 없다고 하는 말은 용서할 수 없다는 말이다. 잊어버리는 것이 용서해주는 것이다. 결혼은 30%의 사랑과 70%의 용서이다. 남을 꾸짖는 마음으로 자신을 꾸짖고 자신을 용서하는 마음으로 남을 용서하라. 대장부는 남을 용서해야 마땅하지만 남의 용서를 받는 사람이 되어서는 안 된다. 다른 사람을 용서하되, 자신은 용서하지 마라"
# #다음 세개의 함수는 KoNLPy 내 분석기이다. 이외에도 Komoran, Mecab등이 있는데, 현재 품질이 가장 좋은 것은 Mecab이다.

# okt = Okt() #Open Korea Text

# print("okt 명사 추출:", okt.nouns(sample_text01))

# corpus, word_to_id, id_to_word = preprocessKOR(sample_text01)

# vocab_size = len(word_to_id)
# C = create_co_matrix(corpus, vocab_size)

# most_similar('그대', word_to_id, id_to_word, C, top=5) """

from common.webcrawling import PreprocessPost, URLRequest, DateChecker_Handle, postContentScrapping
from common.postPreprocess import dataTransformation, Content2Keyword
sample = postContentScrapping(PreprocessPost(URLRequest()))

sample = Content2Keyword(sample)

sample = dataTransformation(sample)[['CORPUS', 'KEYWORDS']]
print(sample)
#date_postNum = DateChecker_Handle(intended_date='2024-01-12')

#[date_1 : 123 date_2 : 001 date_3 : 111 totalPostNum]