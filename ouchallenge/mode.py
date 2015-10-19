# Solution found at http://stackoverflow.com/a/27714192


def stat_mode(list_in):
    '''Returns a list of the most common occuring value(s) from list
    argument.'''
    cnt_dict = {}
    for num in list_in:
        count = list_in.count(num)
        if num not in cnt_dict.keys():
            cnt_dict[num] = count
    max_count = 0
    for key in cnt_dict:
        if cnt_dict[key] >= max_count:
            max_count = cnt_dict[key]
    corr_keys = []
    for corr_key, count_value in cnt_dict.items():
        if cnt_dict[corr_key] == max_count:
            corr_keys.append(corr_key)
    if max_count == 0 and len(cnt_dict) != 1:
        return 'No Mode availalbe for this data set.'
    else:
        corr_keys = sorted(corr_keys)
        return corr_keys
