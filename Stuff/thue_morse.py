# this isn't very universal bc it generates
def generate_thue_morse(power, sym1, sym2):
    thue_morse = [sym1,sym2]
    for i in range(power-1): # -1 bc starts as ^1
        addition = []
        for turn in thue_morse:
            addition.append(sym2 if turn==sym1 else sym1)
        thue_morse.extend(addition)

    return thue_morse
