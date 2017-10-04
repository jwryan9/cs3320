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
            self.graphDict[word] = results

        self.graph_for_cc_search = self.graphDict

        for node in self.graphDict:
            print(str(node) + ': ' + str(self.graphDict[node]))

    def verticies(self):
        return list(self.graphDict.keys())

    def edges(self):
        return list(self.graphDict.keys())

    def number_of_components(self):
        result = []
        nodes = set()
        number_of_connected_components = 0

        return number_of_connected_components

    def shortest_path(self, start, goal):
        try:
            return next(self.bfs_paths(start, goal))
        except:
            return None

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
        visited = self.dfs(next(iter(self.graphDict.keys())))
        num_cc = 1
        while self.graph_for_cc_search:
            vertex = next(iter(self.graph_for_cc_search))
            visited = self.dfs(vertex, visited)
            num_cc +=1
        return num_cc


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
    # words = ['to', 'too', 'two', 'fire', 'for', 'fir', 'fore', 'tor']
    g = WordGraph(words)
    print(g.number_of_components())


if __name__ == '__main__':
    main()
