import itertools

def get_ways_to_split_nitems_to_kbins(nitems, kbins, item_separator="┃", item_symbol="🧍"):
    items = [item_symbol] * nitems
    separators = [item_separator] * (kbins - 1) # 3 bins = item separators
    symbols = items + separators
    ways = set(itertools.permutations(symbols))
    return ways


def get_ways_to_split_list_in_kbins(items, kbins, item_separator="┃", item_symbol="🧍"):
    
    separation_ways = get_ways_to_split_nitems_to_kbins(
        len(items),
        kbins,
        item_separator=item_separator,
        item_symbol=item_symbol)

    ways_pos_separators = [
        [i for i in range(len(w)) if w[i] == item_separator]
        for w in separation_ways]

    ways = []
    for pos_separators in ways_pos_separators:
        aux = list(items)
        for p in pos_separators:
            aux.insert(p, item_separator)
        ways.append(aux)
    
    return ways

def enumerate_ways(ways):
    for i, way in enumerate(sorted(["".join(map(str,w)) for w in ways])):
        print(f"{i+1:>3}  {way}")