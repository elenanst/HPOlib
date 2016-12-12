import logging
import sys


logger = logging.getLogger("HPOlib.call_svm")

import subprocess as subprocess


def save_svm(params, **kwargs):
    if "C" not in params or "Sigma" not in params:
        raise ValueError("No params found ['C', 'Sigma']\n")
    C = params["C"]
    Sigma = params["Sigma"]
    dataset = params["dataset"]
    # Something that has the __len__ attribute is some kind of sequence
    # if hasattr(C, "__len__") or hasattr(Sigma, "__len__"):
    #    C = C[0]
    #     Sigma = Sigma[0]
    C = float(C)
    Sigma = float(Sigma)
    dataset = str(dataset)
    return float(svm(C = C, Sigma = Sigma, dataset = dataset))

def svm(C, Sigma, dataset):
    # Define command and arguments
    command = 'Rscript'
    path2script = '/home/elena/R_ws/automl/HPOlib/HPOlib/benchmarks/R_scripts/my_svm.R'
    # Variable number of args in a list
    args = [str(C), str(Sigma), dataset]
    # Build subprocess command
    cmd = [command, path2script] + args
    # check_output will run the command and store to result
    try:
        result = subprocess.check_output(cmd, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        output = e.output
        print output
    return float(result)
