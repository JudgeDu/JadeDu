import re
import html
import jieba
import jieba.analyse
from sklearn.metrics.pairwise import cosine_similarity



class CosineSimilarity(object):


    def __init__(self, content_x1, content_y2):
        self.s1 = content_x1
        self.s2 = content_y2

    @staticmethod
    def extract_keyword(content):
        re_exp = re.compile(r'(<style>.*?</style>)|(<[^>]+>)', re.S)
        content = re_exp.sub(' ', content)
        content = html.unescape(content)
        seg = [i for i in jieba.cut(content, cut_all=True) if i != '']
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=False)
        return keywords

    @staticmethod
    def one_hot(word_dict, keywords):
        cut_code = [0] * len(word_dict)
        for word in keywords:
            cut_code[word_dict[word]] += 1
        return cut_code

    def main(self, path_stopwords):
        jieba.analyse.set_stop_words(path_stopwords)
        keywords1 = self.extract_keyword(self.s1)
        keywords2 = self.extract_keyword(self.s2)
        union = set(keywords1).union(set(keywords2))
        word_dict = {}
        i = 0
        for word in union:
            word_dict[word] = i
            i += 1
        s1_cut_code = self.one_hot(word_dict, keywords1)
        s2_cut_code = self.one_hot(word_dict, keywords2)
        sample = [s1_cut_code, s2_cut_code]
        try:
            sim = cosine_similarity(sample)
            return sim[1][0]
        except Exception as e:
            print(e)
            return 0.0

if __name__ == '__main__':
    path_orig = r'C:\Users\lenovo\Desktop\测试文本\orig.txt'
    path_orig_del = r'C:\Users\lenovo\Desktop\测试文本\orig_0.8_del.txt'
    path_stopwords = r'C:\Users\lenovo\Desktop\测试文本\stopwords.txt'
    with open(path_orig, mode='r', encoding='utf-8', newline='') as x, \
         open(path_orig_del, mode='r', encoding='utf-8', newline='') as y:
        neirong_x = x.read()
        neirong_y = y.read()
        similarity = CosineSimilarity(neirong_x, neirong_y)
        similarity = similarity.main(path_stopwords=path_stopwords)
        print('相似度: %.1f%%' % (similarity * 100))
        f3 = open(r'C:\Users\lenovo\Desktop\测试文本\result.txt', 'w')
        f3.write('文本相似度为:' + str(similarity * 100) + '%')