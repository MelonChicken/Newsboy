import numpy as np
import konlpy
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