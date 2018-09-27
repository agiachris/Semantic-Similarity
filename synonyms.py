import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    similar_keys = []
    numerator = 0
    
    if (norm(vec2) or norm(vec1)) == 0:
        return (-1)
    
    for keys in vec1.keys():
        if keys in vec2.keys():
            similar_keys.append(keys)
    
    for keys in similar_keys:
        numerator += vec1[keys] * vec2[keys]
            
    return (numerator / (norm(vec1) * norm(vec2)))

def sim_euc(vec1, vec2):
    diff_keys = {}
    for keys in vec1.keys():
        if keys in vec2.keys():
            diff_keys[keys] = vec1[keys] - vec2[keys]
        elif keys not in vec2.keys():
            diff_keys[keys] = vec1[keys]
    for keys in vec2.keys():
        if keys not in vec1.keys():
            diff_keys[keys] = -vec2[keys]
    return norm(diff_keys) * -1
    
    
def sim_euc_norm(vec1,vec2):
    diff_keys = {}
    for keys in vec1.keys():
        if keys in vec2.keys():
            diff_keys[keys] = vec1[keys]/norm(vec1) - vec2[keys]/norm(vec2)
        elif keys not in vec2.keys():
            diff_keys[keys] = vec1[keys]/norm(vec1)
    for keys in vec2.keys():
        if keys not in vec1.keys():
            diff_keys[keys] = -vec2[keys]/norm(vec2)
    return norm(diff_keys) * -1


def build_semantic_descriptors(sentences):
    d = {}
   
    for i in range(len(sentences)):
        for j in sentences[i]:
                if j in d:
                    for k in sentences[i]:
                        if k != j:
                            if k in d[j]:
                                d[j][k] += 1
                            else:
                                d[j][k] = 1
                else:
                    d[j] = {}
                    for k in sentences[i]:
                        if k != j:
							if k in d[j]:
								d[j][k] += 1
							else:
								d[j][k] = 1
    
    return d
    
        
def build_semantic_descriptors_from_files(filenames):
    sentences = []
    combined_books = ""
    for i in range (len(filenames)):
        combined_books += str(open(filenames[i], "r", encoding="latin1").read())
    combined_books = combined_books[: int(len(combined_books) * 1.0)] # Used when taking the percentage of 
    combined_books = combined_books.lower()                           # file to test Time vs Accuracy based    
    combined_books = combined_books.replace("?", ".")                 # on the the percentage of file used
    combined_books = combined_books.replace("\n", "")
    combined_books = combined_books.replace("!", ".")
    combined_books = combined_books.split(". ")
    
    for i in range(len(combined_books)):
        sentences.append(combined_books[i].split(" "))
        
    return build_semantic_descriptors(sentences)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max_similarity = 0
    max_word = ""
    if word in semantic_descriptors:
        for i in choices:
            if i in semantic_descriptors:
                if similarity_fn(semantic_descriptors[word], semantic_descriptors[i]) > max_similarity:
                    max_similarity = similarity_fn(semantic_descriptors[word], semantic_descriptors[i])
                    max_word = i 
        
    return max_word
                
                
def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    x = str((open(filename, "r", encoding="latin1")).read())
    x = x.split("\n")
    test_list = []
    
    for z in range(len(x)):
        test_list.append(x[z].split(" "))
        
    choices = []
    correct = 0
    total_count = 0
    for i in range(len(test_list) - 1):
        total_count += 1
        word = test_list[i][0]
        choices = test_list[i][2:]
        if most_similar_word(word, choices, semantic_descriptors, similarity_fn) == test_list[i][1]:
            correct += 1
    
        choices = []
        
    return ((correct/total_count) * 100)

    
if __name__ ==  "__main__":
    
    filenames = ["war_and_peace.txt", "swanns_way.txt"]
    vec1 = {'a': 1, 'b' : 2, 'c':3}
    vec2 = {'b' : 4, 'c' : 5, 'd': 6}
    print(cosine_similarity(vec1, vec2))
    
    print(build_semantic_descriptors([["i", "am", "a", "sick", "man"],
["i", "am", "a", "spiteful", "man"],
["i", "am", "an", "unattractive", "man"],
["i", "believe", "my", "liver", "is", "diseased"],
["however", "i", "know", "nothing", "at", "all", "about", "my",
"disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]],
))
    
    import time
    start = time.time()
    print(run_similarity_test("test.txt", build_semantic_descriptors_from_files(filenames), cosine_similarity))
    end = time.time()
    print(end - start)