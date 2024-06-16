try:
    from time import ticks_us, ticks_diff
except ImportError:
    from time import time_ns

    def ticks_us(): return int(time_ns() * 1000)
    def ticks_diff(a, b): return a - b

class RandomForestClassifier:
    """
    # RandomForestClassifier(base_estimator=deprecated, bootstrap=True, ccp_alpha=0.0, class_name=RandomForestClassifier, class_weight=None, criterion=gini, estimator=DecisionTreeClassifier(), estimator_params=('criterion', 'max_depth', 'min_samples_split', 'min_samples_leaf', 'min_weight_fraction_leaf', 'max_features', 'max_leaf_nodes', 'min_impurity_decrease', 'random_state', 'ccp_alpha'), max_depth=None, max_features=sqrt, max_leaf_nodes=8, max_samples=None, min_impurity_decrease=0.0, min_samples_leaf=1, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=8, n_jobs=None, num_outputs=3, oob_score=False, package_name=everywhereml.sklearn.ensemble, random_state=None, template_folder=everywhereml/sklearn/ensemble, verbose=0, warm_start=False)
    """

    def __init__(self):
        """
        Constructor
        """
        self.latency = 0
        self.predicted_value = -1

        self.votes = [0.00000000000, 0.00000000000, 0.00000000000]

    def predict(self, x):
        """
        Predict output from input vector
        """
        self.predicted_value = -1
        started_at = ticks_us()

        self.votes = [0.00000000000, 0.00000000000, 0.00000000000]

        idx, score = self.tree0(x)
        self.votes[idx] += score
        
        idx, score = self.tree1(x)
        self.votes[idx] += score
        
        idx, score = self.tree2(x)
        self.votes[idx] += score
        
        idx, score = self.tree3(x)
        self.votes[idx] += score
        
        idx, score = self.tree4(x)
        self.votes[idx] += score
        
        idx, score = self.tree5(x)
        self.votes[idx] += score
        
        idx, score = self.tree6(x)
        self.votes[idx] += score
        
        idx, score = self.tree7(x)
        self.votes[idx] += score

        # get argmax of votes
        max_vote = max(self.votes)
        self.predicted_value = next(i for i, v in enumerate(self.votes) if v == max_vote)

        self.latency = ticks_diff(ticks_us(), started_at)
        return self.predicted_value

    def latencyInMicros(self):
        """
        Get latency in micros
        """
        return self.latency

    def latencyInMillis(self):
        """
        Get latency in millis
        """
        return self.latency // 1000

    def tree0(self, x):
        """
        Random forest's tree #0
        """
        if x[8] < 0.3369999974966049:
            if x[20] < 0.05650000087916851:
                return 0, 465.0
            else:
                if x[12] < -0.04700000025331974:
                    if x[18] < 0.08949999883770943:
                        return 1, 455.0
                    else:
                        return 2, 460.0
                else:
                    if x[17] < -2.074999988079071:
                        if x[7] < 0.09999999776482582:
                            if x[23] < 3.631500005722046:
                                return 1, 455.0
                            else:
                                return 1, 455.0
                        else:
                            return 0, 465.0
                    else:
                        return 0, 465.0
        else:
            return 2, 460.0

    def tree1(self, x):
        """
        Random forest's tree #1
        """
        if x[16] < -26.763500213623047:
            return 2, 452.0
        else:
            if x[8] < 0.12150000035762787:
                if x[22] < 11.505000114440918:
                    return 0, 476.0
                else:
                    if x[22] < 14.55649995803833:
                        return 1, 452.0
                    else:
                        return 0, 476.0
            else:
                if x[16] < -8.605999946594238:
                    if x[6] < 0.07450000196695328:
                        return 1, 452.0
                    else:
                        return 1, 452.0
                else:
                    if x[19] < 0.023000000044703484:
                        return 1, 452.0
                    else:
                        return 0, 476.0

    def tree2(self, x):
        """
        Random forest's tree #2
        """
        if x[11] < 18.433500289916992:
            if x[14] < -0.06399999931454659:
                return 1, 456.0
            else:
                if x[23] < 7.019500017166138:
                    if x[22] < 11.505000114440918:
                        return 0, 484.0
                    else:
                        return 1, 456.0
                else:
                    return 1, 456.0
        else:
            if x[9] < 38.940500259399414:
                if x[20] < 0.08349999785423279:
                    return 0, 484.0
                else:
                    return 1, 456.0
            else:
                if x[20] < 0.10300000011920929:
                    return 0, 484.0
                else:
                    return 2, 440.0

    def tree3(self, x):
        """
        Random forest's tree #3
        """
        if x[10] < 58.624000549316406:
            if x[6] < 0.08550000190734863:
                if x[19] < 0.014500000048428774:
                    return 0, 468.0
                else:
                    if x[20] < 0.05250000022351742:
                        return 0, 468.0
                    else:
                        if x[12] < -0.04050000011920929:
                            return 0, 468.0
                        else:
                            if x[17] < -2.4114999771118164:
                                return 1, 448.0
                            else:
                                return 0, 468.0
            else:
                if x[11] < 4.668999910354614:
                    return 0, 468.0
                else:
                    return 1, 448.0
        else:
            return 2, 464.0

    def tree4(self, x):
        """
        Random forest's tree #4
        """
        if x[10] < 52.70400047302246:
            if x[10] < 28.86900043487549:
                if x[14] < -0.051500000059604645:
                    if x[16] < -8.605999946594238:
                        if x[6] < 0.07450000196695328:
                            return 1, 439.0
                        else:
                            return 1, 439.0
                    else:
                        if x[11] < 10.436500072479248:
                            return 0, 478.0
                        else:
                            return 1, 439.0
                else:
                    return 0, 478.0
            else:
                return 1, 439.0
        else:
            if x[20] < 0.09650000184774399:
                return 0, 478.0
            else:
                return 2, 463.0

    def tree5(self, x):
        """
        Random forest's tree #5
        """
        if x[10] < 58.624000549316406:
            if x[14] < -0.051500000059604645:
                if x[12] < -0.04700000025331974:
                    if x[8] < 0.5230000019073486:
                        return 1, 462.0
                    else:
                        return 2, 458.0
                else:
                    if x[10] < 28.86900043487549:
                        if x[21] < 10.161999702453613:
                            if x[15] < -7.598999977111816:
                                return 1, 462.0
                            else:
                                return 0, 460.0
                        else:
                            return 0, 460.0
                    else:
                        return 1, 462.0
            else:
                return 0, 460.0
        else:
            return 2, 458.0

    def tree6(self, x):
        """
        Random forest's tree #6
        """
        if x[8] < 0.3369999974966049:
            if x[20] < 0.05650000087916851:
                if x[8] < 0.08549999818205833:
                    return 0, 480.0
                else:
                    return 0, 480.0
            else:
                if x[12] < -0.04700000025331974:
                    return 1, 458.0
                else:
                    if x[16] < -8.605999946594238:
                        if x[14] < -0.09849999845027924:
                            return 1, 458.0
                        else:
                            if x[14] < -0.07750000059604645:
                                return 0, 480.0
                            else:
                                return 1, 458.0
                    else:
                        return 0, 480.0
        else:
            return 2, 442.0

    def tree7(self, x):
        """
        Random forest's tree #7
        """
        if x[13] < -0.04700000025331974:
            if x[10] < 50.62899971008301:
                return 0, 465.0
            else:
                return 2, 460.0
        else:
            if x[7] < 0.03150000050663948:
                return 0, 465.0
            else:
                if x[6] < 0.079500000923872:
                    if x[12] < -0.04050000011920929:
                        return 0, 465.0
                    else:
                        if x[22] < 10.864500045776367:
                            return 0, 465.0
                        else:
                            return 1, 455.0
                else:
                    if x[6] < 0.15700000524520874:
                        return 1, 455.0
                    else:
                        return 2, 460.0