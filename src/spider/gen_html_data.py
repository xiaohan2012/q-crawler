from json import dumps
def acc_sum(lis):
    total = 0
    for x in lis:
        total += x
        yield total

if __name__ == "__main__":
    aptc_scores = map(lambda l: float(l.strip().split()[1]), open("data/python/urls-apprentice.txt").readlines())
    bsl_scores = map(lambda l: float(l.strip().split()[1]), open("data/python/urls-baseline.txt").readlines())
    
    aptc_stat = acc_sum(aptc_scores)
    bsl_stat = acc_sum(bsl_scores)

    with open('apprentice_stat.js', "w") as f:
        stat_str = dumps(list(aptc_stat)[::250])
        f.write("var apprentice_data = %s;" %(stat_str))

    with open('baseline_stat.js', "w") as f:
        stat_str = dumps(list(bsl_stat)[::250])
        f.write("var baseline_data = %s;" %(stat_str))
