import random
import numpy as np
import re


class BookCipher:
    def __init__(self, text: str, seed: int = 5, with_clean = True):
        self.text = text

        if with_clean:
            clean_text = re.sub("\s|,|\.|\(|\)|\-|–", "", text).lower()
        else:
            clean_text = text

        n = int(np.floor(np.sqrt(len(clean_text))))
        table = []
        t = 0

        for i in range(n):
            table.append(list(clean_text[t:t+n]))
            t += n + random.randint(0, min(n // seed, seed))

            if len(table[-1]) < n:
                n = i
                table = np.array(table[:-1])[:n, :n]
                break
        else:
            table = np.array(table)

        self.n = n
        self.table = table


    def encode(self, message: str) -> str:
        encoded_msg = ""
        for l in message:
            x, y = np.where(self.table == l.lower())

            if x.size:
                t = random.randint(0, x.size - 1)
                encoded_msg += f"{x[t]}|{y[t]}{'u' if l.isupper() else ''}-"
            elif l == " ":
                encoded_msg += " -"
            else:
                raise ValueError(f"Not such letter in alphabet: {l}")

        return encoded_msg


    def decode(self, message: str) -> str:
        splitted_msg = message.split("-")[:-1]
        decoded_msg = ""
        for el in splitted_msg:
            splitted_el = re.split("\||u", el)

            try:
                if len(splitted_el) > 1:
                    x, y = int(splitted_el[0]), int(splitted_el[1])

                    if x > self.n or y > self.n:
                        continue

                    l: str = self.table[x, y]
                    l = l.upper() if el.find("u") > -1 else l
                else:
                    l = splitted_el[0]
            except:
                continue

            decoded_msg += l

        return decoded_msg