


def compare_conseq_points_binarize(target_vec, step):
    '''
     UP vs DOWN/NEURTRAL binarizer.
    '''
    feat_bin_vec_dict = {}
    bin_vec = []
    for i in range(len(target_vec) - step):
        if target_vec[i] < target_vec[i+step]:
            bin_vec.append(1) # UP
        else:
            bin_vec.append(0) # DOWN OR NEUTRAL

    return bin_vec


def topN_vs_others_binarize(self, input_vec, N):
    border = np.quantile(input_vec, float(N)/100)
    binary_vec = [1 if xi > border else 0 for xi in input_vec]

    return binary_vec


def binarize_target(target_vec, la_days, strategy="CompareConseq", N=None):
    '''
    '''
    LAY_binVec = {}
    if strategy == 'CompareConseq':
        for la_day in la_days:
            LAY_binVec[la_day] = compare_conseq_points_binarize(target_vec, la_day)
    elif strategy == "TopNVsOthers":
        for la_day in la_days:
            LAY_binVec[la_day] = compare_conseq_points_binarize(topN_vs_others_binarize(target_vec), la_day)
    else:
        Raise("Unknwon target binarization startegy {}".format(strategy))

    return LAY_binVec
