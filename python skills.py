############################################################
# CIS 521: Python Skills Homework
############################################################
import string
from typing import List, Any

from nltk.corpus import stopwords

student_name = "Naomi Maranga"

# This is where your grade report will be sent.
student_email = "kmaranga@seas.upenn.edu"

############################################################
# Section 1: Python Concepts
############################################################

python_concepts_question_1 = """
Python being a strongly typed language means that the variables have a type which matters when performing 
operations on said variables. Dynamic typing on the other hand means that the type of variable is automatically 
determined by the assigned object and is determined only during runtime. It's worth noting that methods in  
python don't have type signatures. 

An example of strong typing is when python doesn't allow variables of two different types to be added together 
for example if x = 5 and y = "cat", the operation x + y throws an error since variable x is of type integer and y
is a string. Variables of the same type can however be added together such as if x = 5 and z = 2, x + z would 
yield 7 and if y = "cat" and a = "my", a + y would yield "my cat" 

An example of dynamic typing is when initializing a variable say x = 3 and then later on changing the variable 
x to another type such as x = "dog". This changes the variable type from integer in x = 3 to string in x = "dog" 
and any later calls to x would return the most current version of x which would be the string "dog". 
"""

python_concepts_question_2 = """ 
The type error that results when we try creating this dictionary is as a result of using a list to store the 2D
points i.e as a hash argument whereas lists are unhashable objects and as such can't be used as keys in dictionaries
since they're mutable. 

An alternative to this code would be to use a tuple to store 2D points as these are hashable and the resulting 
code would be: 
points_to_names = {(0, 0): "home", (1, 2): "school", (-1, 1): "market"}
 """

python_concepts_question_3 = """
The function concatenate2 is significantly faster than the function concatenate1 for large inputs since concatenate1
requires looping through the strings and this becomes quite time intensive for larger inputs while concatenate2
uses the .join built in function which is much faster for larger inputs 
"""


############################################################
# Section 2: Working with Lists
############################################################

def extract_and_apply(l, p, f):
    return [f(x) for x in l if p(x)]


def concatenate(seqs):
    return [i for substring in seqs for i in substring]

# seqs = [[1, 2], [3, 4], [5, 6]]
# print(concatenate(seqs))

def transpose(matrix):
    trans = matrix.copy()
    trans = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    return trans

# sample_matrix = [[1, 2, 3]]
# print(transpose(sample_matrix))


############################################################
# Section 3: Sequence Slicing
############################################################

def copy(seq):
    return seq[:]
# sequence = ["a", "b", "c"]
# print(copy(sequence))


def all_but_last(seq):
    return seq[: -1]
# sequence = ["a", "b", "c"]
# print(all_but_last(sequence))


def every_other(seq):
    return seq[:: 2]
# sequence = ["a", "b", "c"]
# print(every_other(sequence))


############################################################
# Section 4: Combinatorial Algorithms
############################################################

def prefixes(seq):
    for i in range(len(seq) + 1):
        yield seq[:i]
# seq_prefix = [1, 2, 3]
# print(list(prefixes(seq_prefix)))


def suffixes(seq):
    for i in range(len(seq) + 1):
        yield seq[i:]
# seq_suffix = [1, 2, 3]
# print(list(suffixes(seq_suffix)))

def slices(seq):
    for i in range(len(seq) + 1):
        for j in range(i + 1, len(seq) + 1):
            yield seq[i:j]
# seq_slices = [1, 2, 3]
# print(list(slices(seq_slices)))

############################################################
# Section 5: Text Processing
############################################################

def normalize(text):
    normalized = ' '.join(text.split()).lower()
    return normalized

# text_norm = "This is an example"
# text_2 = "       EXTRA  SPACE   . "
# print(normalize(text_norm))
# print(normalize(text_2))

def no_vowels(text):
    table = text.maketrans(dict.fromkeys('aeiouAEIOU'))
    vowel_removed = text.translate(table)
    return vowel_removed

# text_normal = "This is an example"
# print(no_vowels(text_normal))

def digits_to_words(text):
    digits = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six',
              '7': 'seven', '8': 'eight', '9': 'nine'}
    return " ".join([digits[i] for i in text if i in digits])

# zipcode = "19104"
# print(digits_to_words(zipcode))

def to_mixed_case(name):
    name = name.split("_")
    temp = ''.join([x.lower().capitalize() for x in name])
    temp2 = temp[:1].lower() + temp[1:]
    return temp2

# test = "i_don't_know"
# print(to_mixed_case(test))

############################################################
# Section 6: Polynomials
############################################################

class Polynomial(object):
    def __init__(self, polynomial):
        self.polynomial = tuple(polynomial)

    def get_polynomial(self):
        return self.polynomial

    def __neg__(self):
        neg_list = list(self.polynomial)
        new_neg_list = []
        for t in neg_list:
            t_neg = t[0] * -1
            t = (t_neg, t[1])
            new_neg_list.append(t)

        return Polynomial(new_neg_list)

    def __add__(self, other):
        return Polynomial(self.polynomial + other.polynomial)

    def __sub__(self, other):
        other = -other
        return Polynomial(self.polynomial + other.polynomial)

    def __mul__(self, other):
        final_list = []
        for t in self.polynomial:
            for t1 in other.polynomial:
                (coeff1, power1) = t
                (coeff2, power2) = t1
                ans_coeff = coeff1 * coeff2
                ans_power = power1 + power2
                final_list.append((ans_coeff, ans_power))
        return Polynomial(final_list)

    def __call__(self, x):
        call_self = list(self.polynomial)
        return sum([t[0] * (x ** t[1]) for t in call_self])

    def simplify(self):
        simplify_list = self.polynomial
        new_sim_list = []
        list_of_powers = []
        for t in range(len(simplify_list)):
            coeff1 = simplify_list[t][0]
            power1 = simplify_list[t][1]
            if power1 not in list_of_powers:
                for s in range(t + 1, len(simplify_list)):
                    coeff2 = simplify_list[s][0]
                    power2 = simplify_list[s][1]
                    # combine terms with a common power
                    if power1 == power2:
                        coeff1 += coeff2

                list_of_powers.append(power1)
                # check if terms have coefficient zero
                if coeff1 == 0:
                    if coeff2 == 0:
                        new_sim_list.append((coeff1, power1))
                else:
                    new_sim_list.append((coeff1, power1))
        # sort remaining terms in descending order
        new_sim_list.sort(key=lambda x: x[1], reverse=True)
        self.polynomial = tuple(new_sim_list)
        return simplify_list

    def __str__(self):
        new_str = list(self.polynomial)
        readable_str = ""  # our final answer - a human-readable string
        for t in range(len(new_str)):
            helper = ""
            # check if positive or negative
            if new_str[t][0] < 0:
                sign = '-'
            else:
                sign = '+'
            coeff1 = abs(new_str[t][0])  # coeffs with magnitude 0 should always have a positive sign
            if t != 0:
                helper += sign + " "

            else:
                if sign == '-':
                    helper = helper + sign

            if coeff1 == 1:
                if new_str[t][1] == 0:
                    helper = helper + str(coeff1)
            else:
                helper = helper + str(coeff1)
            # omit power portion if power is 1
            if new_str[t][1] == 1:
                helper = helper + 'x'
            elif new_str[t][1] > 1:
                helper = helper + 'x^' + str(new_str[t][1])
            else:
                helper = helper + ''
            if t != len(new_str) - 1:
                helper = helper + ' '
            readable_str = readable_str + helper
        return readable_str


# p = Polynomial([(0, 1), (2, 3)])
# print(str(p))
# print(str(p * p))
# print(str(-p * p))
# q = Polynomial([(1, 1), (2, 3)])
# print(str(q))
# print(str(q * q))
# print(str(-q * q))

# p = Polynomial([(2, 1), (1, 0)])
# q = -p + (p * p)
# print(q.get_polynomial())
# q.simplify()
# print(q.get_polynomial())
#
# p = Polynomial([(2, 1), (1, 0)])
# q = p - p
# q.get_polynomial()
# q.simplify()
# print(q.get_polynomial())


############################################################
# Section 7: Python Packages
############################################################
import numpy as np
def sort_array(list_of_matrices):
    # for i, n in enumerate(list_of_matrices):
    #     new_arr = []
    #     new_arr[i, :n.shape[0], :n.shape[1]] = n
    #     sorted_arr = np.sort(new_arr, kind=None, order=None)
    #
    #     #sorted_arr = np.sort(i, kind=None, order=None)
    #
    # return sorted_arr
    list_of_matrices = np.concatenate([n.ravel() for n in list_of_matrices])
    sorted_arr = np.sort(list_of_matrices, kind=None, order=None)
    reversed_arr = sorted_arr[::-1]
    return reversed_arr


# matrix1 = np.array([[1, 2], [3, 4]])
# matrix2 = np.array([[5, 6, 7], [7, 8, 9], [0, -1, -2]])
# print(sort_array([matrix1, matrix2]))

import nltk

nltk.download('stopwords')


def POS_tag(sentence):
    sentence = sentence.lower()
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))  # to lowercase,
    sentence = nltk.word_tokenize(sentence)  # tokenize & punctuation
    sentence = [word for word in sentence if word not in stopwords.words('english')]  # remove stopwords
    sentence = nltk.pos_tag(sentence)  # conduct pos tagging and return a list of tuples
    return sentence


############################################################
# Section 8: Feedback
############################################################

feedback_question_1 = """
about 7 hours
"""

feedback_question_2 = """
understanding exactly what was required in the polynomial section of the homework was a little diffciult. A little more 
explanation on how the functions are intended to work would have been really helpful 
OH my GOODNESS THE apostrophe AND .title() WAS such A nightmare :/ i.e iDon'TLikeIt :(
"""

feedback_question_3 = """
generator functions are the GOAT :)
"""
