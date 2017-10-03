from string import ascii_lowercase


class WordGraph:
    def __init__(self, word_list):
        self.graphDict = {}
        self.numberOfConnectedComponents = 0

        for word in word_list:
            self.graphDict.update({word: ''})

        for word in word_list:
            results = try_letter_insert_dict(word, self.graphDict)
            results.extend(try_letter_swap_dict(word, self.graphDict))
            self.numberOfConnectedComponents += len(results)
            self.graphDict[word] = results

        print(self.graphDict)
        print(len(self.graphDict))

    def number_of_components(self):
        return self.numberOfConnectedComponents

    def shortest_path(self, word1, word2, path=[]):
        path.append(word1)

        if word1 == word2:
            return path

        if word1 not in self.graphDict:
            return None

        shortest = None
        for word in self.graphDict[word1]:
            if word not in path:
                newpath = self.shortest_path(word, word2, path)

                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest


def try_letter_swap_dict(word, word_dict):
    match_list = []
    for i in range(len(word)):
        for let in ascii_lowercase:
            word_as_list = list(word)
            word_as_list[i] = let
            word_temp = ''.join(word_as_list)
            if word_temp in word_dict and word_temp not in match_list:
                match_list.append(word_temp)
    return match_list


def try_letter_insert_dict(word, word_dict):
    match_list = []
    for i in range(len(word)):
        for let in ascii_lowercase:
            word_temp = word[:i] + let + word[i:]
            if word_temp in word_dict and word_temp not in match_list:
                match_list.append(word_temp)
    return match_list


def main():
    file = 'sgb-words.txt'
    with open(file) as f:
        words = f.read().split()
    words = ['to', 'too', 'two', 'for', 'fire', 'four', 'tour', 'dire']
    g = WordGraph(words)
    shortestpath = g.shortest_path('for', 'tour')
    print(shortestpath)


if __name__ == '__main__':
    main()
