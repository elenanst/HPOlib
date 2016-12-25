from hyperopt import hp
space = {'C': hp.quniform('C', 1, 5,1),
         'Sigma': hp.loguniform('alpha', -10, 2)}
