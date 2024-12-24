from random import randint
import sympy as sp

class KnapsackCipher:
    @staticmethod
    def gen_superincreasing_sequence(size, first_el=1, rand_range = [1, 5]):
        res = [first_el]
        for _ in range(1, size):
            res.append(sum(res) + randint(*rand_range))
        return res


    @staticmethod
    def generate_keys(size, m_range = [1, 5]):
        seq = KnapsackCipher.gen_superincreasing_sequence(size)
        m = sum(seq) + randint(*m_range)

        w = randint(2, m - 1)
        while sp.gcd(w, m) != 1:
            w = randint(2, m - 1)

        pub = [(w * x) % m for x in seq]

        prv = (seq, m, w)
        return pub, prv


    @staticmethod
    def encode(text, pub):
        pub_len = len(pub)
        result = []
        for el in text:
            bin = [
                int(bit) for bit in format(ord(el), f"0{pub_len}b")
            ]
            result.append(sum(b * pk for b, pk in zip(bin, pub)))

        return result


    @staticmethod
    def decode(text, prv):
        seq, m, w = prv
        w_inv = sp.mod_inverse(w, m)
        result = ""
        for el in text:
            t = (el * w_inv) % m
            bin = []
            for x in reversed(seq):
                if t >= x:
                    bin.append(1)
                    t -= x
                else:
                    bin.append(0)

            result += chr(int("".join(map(str, reversed(bin))), 2))

        return result