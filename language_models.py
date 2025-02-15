
############################################################
# Language Models 
############################################################

import math
import re
import random
import string

############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    return re.findall(r"[\w]+|["+string.punctuation+"]", text)

def ngrams(n, tokens):
    tokens = ["<START>"] * (n - 1) + tokens + ["<END>"]
    ngrams_list = []

    for i in enumerate(tokens):
      if i[0] >= (n - 1):
        tokens_tuple = tuple(tokens[i[0] - n + 1:i[0]])
        ngrams_list.append((tokens_tuple, i[1]))
    return ngrams_list

class NgramModel(object):

  def __init__(self, n):
      self.n = n
      self.dictionary = {}
      self.internal_counts = {}

  def update(self, sentence):
    tokenized = tokenize(sentence)

    for i in ngrams(self.n, tokenized):
      if i[0] not in self.dictionary.keys():
        updated_dict = {i[1]: 1}
        self.dictionary[i[0]] = updated_dict
      else:
        token = self.dictionary.get(i[0])
        if i[1] not in token:
          token[i[1]] = 1
        else:
          token[i[1]] += 1

      if i[0] in self.internal_counts.keys():
        self.internal_counts[i[0]] += 1
      else:
        self.internal_counts[i[0]] = 1
        

  def prob(self, context, token):
    if context in self.dictionary.keys():
      dict_context = self.dictionary[context]
      if token in dict_context:
        numerator = (dict_context[token])
        denominator = self.internal_counts[context]
        soln = numerator / denominator
        return soln
    return 0.0
              

  def random_token(self, context):
      r = random.random()
      if context not in self.dictionary.keys():
        return None
      T = sorted(self.dictionary[context].keys())
      created = self.dictionary[context]
      for x in enumerate(T):
        result = sum([created[i] for i in T[:x[0]]])
        x0 = created[T[(x[0])]]
        ic = self.internal_counts
        res_over_context = (result / ic[context])
        updated_res_oc = (result + x0) / ic[context]
        if r >= res_over_context and r < updated_res_oc:
          return x[1]
      
  
  def random_text(self, token_count):
    token = ' '
    tokenlist = []
    tokenlist2 = []

    if self.n == 1:
      for i in range(0, token_count):
        tokenlist2.append(self.random_token(()))
      return token.join(tokenlist2)

    else:
      start1 = ("<START>",) * (self.n - 1)
      start2 = ("<START>",) * (self.n - 1)
      
      for j in range(0, token_count):
        rt1 = self.random_token(start1)
        tokenlist.append(rt1)

        if rt1 != "<END>":
            start1 = start1[1:] + (rt1,)
        else:
            start1 = start2
      return ' '.join(tokenlist)

  def perplexity(self, sentence):
    perplexity = 0.0
    tokenized = tokenize(sentence)
    length_tokenized = len(tokenize(sentence))

    for i in ngrams(self.n, tokenized):
      soln = self.prob(i[0], i[1])
      log = math.log(soln)
      perplexity += log
    exponentiated = math.exp(perplexity)
    return math.pow((1/exponentiated), 1 / (length_tokenized + 1))



def create_ngram_model(n, path):
  ngram_model = NgramModel(n)
  read_file = open(path)
  for line in read_file:
    ngram_model.update(line)
  return ngram_model
  

#tests
# print(ngrams(1, ["a", "b", "c"]))
# print(ngrams(2, ["a", "b", "c"]))
# print(ngrams(3, ["a", "b", "c"]))

# print('********SPACER*********')

# #update
# m = NgramModel(1)
# m.update("a b c d")
# m.update("a b a b")
# print(m.prob((), "a"))
# print(m.prob((), "c"))
# print(m.prob((), "<END>"))
# m = NgramModel(2)
# m.update("a b c d")
# m.update("a b a b")
# print(m.prob(("<START>",), "a"))
# print(m.prob(("b",), "c"))
# print(m.prob(("a",), "x"))
# print('********SPACER*********')
# print('random_token')

# m = NgramModel(1)
# m.update("a b c d")
# m.update("a b a b")
# random.seed(1)
# print([m.random_token(()) for i in range(25)])

# m = NgramModel(1)
# m.update("a b c d")
# m.update("a b a b")
# random.seed(1)
# print(m.random_text(13))

# m = NgramModel(2)
# m.update("a b c d")
# m.update("a b a b")
# random.seed(2)
# print(m.random_text(15))

# m = NgramModel(1)
# m.update("a b c d")
# m.update("a b a b")
# print(m.perplexity("a b"))

# m = NgramModel(2)
# m.update("a b c d")
# m.update("a b a b")
# print(m.perplexity("a b"))
