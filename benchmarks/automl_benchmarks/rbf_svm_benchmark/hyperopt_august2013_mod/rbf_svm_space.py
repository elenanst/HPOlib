from hyperopt import hp
space = {'C': hp.quniform('C', 0, 24, 1),
         'Sigma': hp.uniform('alpha', 0, 13)}
