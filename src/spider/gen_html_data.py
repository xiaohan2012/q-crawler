from json import dump
def acc_sum(lis):
    total = 0
    for x in lis:
        total += x
        yield total

if __name__ == "__main__":
    aptc_scores = map(lambda l: float(l.strip().split()[1]), open("data/python/urls-apprentice.txt").readlines())
    bsl_scores = map(lambda l: float(l.strip().split()[1]), open("data/python/urls-baseline.txt").readlines())
    
    aptc_stat = acc_sum(aptc_scores[::100])
    bsl_stat = acc_sum(bsl_scores[::100])

    dump(list(aptc_stat), open('data/python/apprentice_stat.js', "w"))
    dump(list(bsl_stat), open('data/python/baseline_stat.js', "w"))    
