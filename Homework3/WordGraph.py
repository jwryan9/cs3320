from string import ascii_lowercase

class WordGraph:
    def __init__(self, word_list):
        self.graphDict = {}
        word_list = sorted(word_list)
        for word in word_list:
            self.graphDict.update({word: ''})

        for word in word_list:
            results = try_letter_insert_dict(word, self.graphDict)
            results.extend(try_letter_swap_dict(word, self.graphDict))
            results.extend(try_letter_remove_dict(word, self.graphDict))
            self.graphDict[word] = results

        self.graph_for_cc_search = self.graphDict

        for node in self.graphDict:
            print(str(node) + ': ' + str(self.graphDict[node]))

    def bfs_shortest_path(self, word1, word2):
        """
        Uses breadth first search to find shortest path between two words in the graph
        :param word1: origin on graph
        :param word2: destination on graph
        :return: path if found else message
        """
        word_count = 0
        if word1 not in self.graphDict.keys():
            return word1 + ' not in graph'
        if word2 not in self.graphDict.keys():
            return word2 + ' not in graph'
        queue = [(word1, [word1])]
        while queue:
            word, path = queue.pop(0)
            for next_word in self.graphDict[word]:
                word_count += 1
                if word_count > len(self.graphDict.keys()):
                    return 'No path from ' + word1 + ' to ' + word2
                if next_word in path:
                    continue
                elif next_word == word2:
                    return path + [next_word]
                else:
                    queue.append((next_word, path + [next_word]))
        return 'No path from ' + word1 + ' to ' + word2

    def dfs(self, start, visited=set()):
        """
        gets a list of connected components using dfs
        :param start: vetex to search from
        :return: list of connected components
        """
        stack = [start]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.update([vertex])
                for element in self.graph_for_cc_search[vertex]:
                    if element in visited:
                        self.graph_for_cc_search[vertex].remove(element)
                stack.extend(self.graph_for_cc_search[vertex])
                self.graph_for_cc_search.pop(vertex)
        return visited

    def number_of_components(self):
        """
        Counts the number of connected components in the graph
        :return: number of connected components
        """
        # run dfs for first vertex of graph to initialize visited
        visited = self.dfs(next(iter(self.graph_for_cc_search.keys())))
        num_cc = 1
        while self.graph_for_cc_search:
            vertex = next(iter(self.graph_for_cc_search))
            visited = self.dfs(vertex, visited)
            num_cc +=1
        return num_cc


def try_letter_swap_dict(word, word_dict):
    """
    Attempts to match words in dictionary by swapping letters
    :param word: word to match
    :param word_dict: dictionary of all words
    :return: list of matching words
    """
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
    """
    Attempts to match words in dictionary by inserting letters
    :param word: word to match
    :param word_dict: dictionary of all words
    :return: list of matching words
    """
    match_list = []
    for i in range(len(word) + 1):
        for let in ascii_lowercase:
            word_temp = word[:i] + let + word[i:]
            if word_temp in word_dict and word_temp not in match_list:
                match_list.append(word_temp)
    return match_list


def try_letter_remove_dict(word, word_dict):
    """
    Attempts to match words in dictionary by removing letters
    :param word: word to match
    :param word_dict: dictionary of all words
    :return: list of matching words
    """
    match_list = []
    for i in range(len(word) + 1):
        word_temp = word[:i] + word[i+1:]
        if word_temp in word_dict and word_temp not in match_list:
            match_list.append(word_temp)
    return match_list


def main():
    file = 'sgb-words.txt'
    with open(file) as f:
        words = f.read().split()
    g = WordGraph(words)
    print(g.number_of_components())
    g2 = WordGraph(words)
    print(g2.bfs_shortest_path('mumps', 'mummy'))


if __name__ == '__main__':
    main()
