

class Resulter():
    def __init__(self) -> None:
        pass

    def make_results(self, table) -> list[str]:
        res = []
        if table:
            for j in range(table):
                for i in range(table[j]):
                    if all(table[j][i] == "+", i != 0):
                        res.append(f"{j} - {i}")
        return res

