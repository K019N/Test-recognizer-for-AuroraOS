

class Resulter():
    def __init__(self) -> None:
        pass

    def make_results(self, table) -> list[str]:
        res = {}
        if any(table):
            for j in range(len(table)):
                for i in range(len(table[j])):
                    if all((table[j][i] == "+", i != 0)):
                        res[j] = i
        return res

    def compare(self, results, answers):
        mark = 0
        for i in results:
            if results[i] == answers[i]:
                mark += 1
        return mark
        
