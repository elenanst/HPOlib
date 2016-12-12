import subprocess as subprocess

def svm(C, Sigma):
    # Define command and arguments
    command = 'Rscript'
    path2script = '/home/elena/R_ws/automl/optimization_workspace/HPOlib/HPOlib/benchmarks/R_scripts/my_svm.R'
    # Variable number of args in a list
    args = [str(C), str(Sigma)]
    # Build subprocess command
    cmd = [command, path2script] + args
    # check_output will run the command and store to result
    try:
        result = subprocess.check_output(cmd, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        output = e.output
        print output
    return int(result)
