import numpy as np
from konlpy.tag import Okt


def preprocess(text):

    text = text.lower() ##영어인 경우 상정
    text = text.replace('.', ' .')
    words = text.split(' ')
    word_to_id = {}
    id_to_word = {}

    for word in words:
        if word not in word_to_id:
            new_id = len(word_to_id)
            word_to_id[word] = new_id
            id_to_word[new_id] = word
    corpus = np.array([word_to_id[w] for w in words])

    return corpus, word_to_id, id_to_word


def preprocessKOR(text):
    okt = Okt()
    words = okt.nouns(text)
    word_to_id = {}
    id_to_word = {}

    for word in words:
        if word not in word_to_id:
            new_id = len(word_to_id)
            word_to_id[word] = new_id
            id_to_word[new_id] = word
    corpus = np.array([word_to_id[w] for w in words])

    return corpus, word_to_id, id_to_word

#corpus, word_to_id, id_to_word = preprocessKOR("용서는 곧 사랑이다. 고결하고 아름다운 사랑의 형태이다. 사랑이 없는 사람은 쉽게 용서하지 못한다. 용서는 평화와 행복을 그 보답으로 준다. 그대, 용서함으로써 행복 하라! 용감한 자만이 용서할 줄 알고 비겁한 자는 용서하지 않는다. 용서는 남에게는 자주 베풀지만 자신에게는 베풀지 마라. 누군가가 당신에게 피해를 입혔다면 인내심을 가지고 그들을 대하라. 부드러운 말은 상처를 소독한다. 용서는 상처를 치유하고, 망각은 흉터를 지운다. 상처를 낫게 하려고 논쟁을 벌이는 것보다 조용히 상처를 기다리는 편이 더 낫다. 용서가 신성하듯이 극도의 어려움을 참고 견디는 것은 훌륭하다. 용서하는 것은 아름답다.용서하지 않으면 분노를 되새김질하게 되고 과거의 기억과 상처에 매달리게 되면서 자기 자신의 노예가 되는 것이다. 상처에 집착하는 것은 자기 자신을 불행하게 만든다. 용서는 자신을 위해 상처를 떨쳐버리는 것이다. 상처의 진정한 치유는 용서에서 온다. 용서는 자신 안에 갇힌 에너지를 밖으로 내보내 세상에서 선한 일을 하는데 쓸 수 있게 한다. 용서는 삶 속에서 실천할 수 있는 큰 수행이다. 용서할 때는 마음에 문을 열 수 있다. 용서하는 마음은 상처 준 이들을 받아들이는 마음이다. 진정한 용서는 마음의 쇠사슬에 묶여 있던 이들을 위안해주고 안심시켜 주는 일이다. 자신을 멍들게 하고 파괴시킨 미움과 원망의 마음에서 스스로 벗어나는 일이다. 그대를 고통스럽게 만든 사람에게 나쁜 감정을 키워나가면 그대 자신의 마음의 평화만 깨어질 뿐이다. 그대가 그를 용서한다면, 그대 마음은 평온을 되찾을 것이다. 누군가를 용서한다는 것은 알고 보면 자신을 위한 것이다. 타인을 용서치 못하면 스스로 건너야 하는 다리를 부스는 것이나 마찬가지다. 죄를 저지를 자와 피해를 입은 자, 모두에게 용서가 필요한 법이다. 약자는 결코 용서할 수가 없다. 용서는 강자의 속성이다. 증오는 사랑만이 극복할 수 있다. 용서할 수는 있어도 잊을 수는 없다고 하는 말은 용서할 수 없다는 말이다. 잊어버리는 것이 용서해주는 것이다. 결혼은 30%의 사랑과 70%의 용서이다. 남을 꾸짖는 마음으로 자신을 꾸짖고 자신을 용서하는 마음으로 남을 용서하라. 대장부는 남을 용서해야 마땅하지만 남의 용서를 받는 사람이 되어서는 안 된다. 다른 사람을 용서하되, 자신은 용서하지 마라")
#print(corpus)
def create_co_matrix(corpus, vocab_size, window_size=1): #동시발생행렬을 자동으로 만들기 위한 함수
                                                         #vocab_size는 word_to_id의 length를 구하면 된다. 다시말해 단어의 개수를 입력하는 파라미터이다.
    corpus_size = len(corpus)
    co_matrix = np.zeros((vocab_size, vocab_size), dtype=np.int32) ##co_matrix 초기화

    for idx, word_id in enumerate(corpus): #주변단어를 세고 이를 co_matrix에 저장한다. (one-hot vector가 아님을 유념하자)
        for i in range(1, window_size + 1):
            left_idx = idx - i
            right_idx = idx + i

            if left_idx>=0:
                left_word_id = corpus[left_idx]
                co_matrix[word_id, left_word_id] +=1

            if right_idx < corpus_size:
                right_word_id = corpus[right_idx]
                co_matrix[word_id, right_word_id] += 1
    return co_matrix

def cos_similarity(x, y, eps = 1e-8):
    nx = x / (np.sqrt(np.sum(x**2)) + eps) #각 벡터의 norm을 계산한다.
    ny = y / (np.sqrt(np.sum(y**2)) + eps)
    return(np.dot(nx, ny))

def most_similar(query, word_to_id, id_to_word, word_matrix, top=5):
    #검색어를 꺼낸다
    if query not in word_to_id:
        print('%s(을)를 찾을 수 없습니다.' % query)
        return

    print('\n[query] '+query)
    query_id = word_to_id[query]
    query_vec = word_matrix[query_id]

    #코사인 유사도를 계산한다.
    vocab_size = len(id_to_word)
    similarity = np.zeros(vocab_size)
    for i in range(vocab_size):
        similarity[i] = cos_similarity(word_matrix[i], query_vec)

    #코사인 유사도를 기준으로 내림차순으로 출력한다.

    count = 0
    for i in (-1*similarity).argsort(): #argsort()는 넘파이 배열의 원소를 오름차순으로 정렬하며, 이때의 반환값은 배열의 "인덱스"이다.
        if id_to_word[i] == query:
            continue
        print(' %s: %s' % (id_to_word[i], similarity[i]))

        count +=1
        if count>=top:
            return

def ppmi (C, verbose=False, eps=1e-8):
    #C는 동시발생 행렬이고, verbose는 진행상황 출력 여부를 결정하는 플래그이다.
    M = np.zeros_like(C, dtype=np.float32) #동시발생행렬의 크기와 동일한 크기의 행렬을 만든다.
    print(f'M = {M}\n')

    N = np.sum(C)
    print(f'N = {N}\n')

    S = np.sum(C, axis=0)
    print(f'S = {S}\n')

    total = C.shape[0] * C.shape[1]
    print(f'total = {total}')

    for i in range(C.shape[0]):
        for j in range(C.shape[1]):
            pmi = np.log2(C[i, j]*N/(S[j]*S[i])+eps)
            M[i, j] = max(0, pmi)

            if verbose:
                cnt+=1
                if cnt%(total//100+1) == 0:
                    print('%.1f%% 완료' % (100*cnt/total))

    return M
