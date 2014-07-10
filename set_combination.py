def set_combination(lists):
    """
    Returns a list of all combinations created by picking the nth element from
    the nth list

    :param lists: a list of lists. From each list, an element will be chosen to form
        all possible combinations
    """

    combinations = []

    for i, next_list in enumerate(lists):
        for j, _ in enumerate(next_list):
            lists[i] = next_list[j:] + next_list[:j]
            combinations.append(zip(*lists))
    return combinations

print(set_combination([["a", "b", "c"], ["1", "2", "3"], ["x", "y", "z"]]))
