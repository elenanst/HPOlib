from hyperopt import hp
space = {'C': hp.loguniform('C', -5, 15),
         'Sigma': hp.loguniform('alpha', -15, 3)}
