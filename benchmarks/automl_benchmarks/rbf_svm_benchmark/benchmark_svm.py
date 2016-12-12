import time
import HPOlib.benchmarks.benchmark_util as benchmark_util
import HPOlib.benchmarks.call_svm as call_svm
import sys
sys.path.append('/home/elena/R_ws/automl/HPOlib/HPOlib')
import wrapping_util as wrapping_util


def main(params, **kwargs):
    # get dataset from .config
    print 'Params: ', params,
    y = call_svm.save_svm(params, **kwargs)
    #y = params["C"]
    print 'Result: ', y
    return float(y)

if __name__ == "__main__":
    starttime = time.time()
    args, params = benchmark_util.parse_cli()
    parser = wrapping_util.load_experiment_config_file()
    dataset = parser.get('HPOLIB', 'dataset')
    params['dataset'] = dataset
    result = main(params, **args)
    duration = time.time() - starttime
    print result
    print "Result for ParamILS: %s, %f, 1, %f, %d, %s" % \
        ("SAT", abs(duration), result, -1, str(__file__))
