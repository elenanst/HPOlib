#!/usr/bin/env python
import os
import sys
sys.path.append('../HPOlib')
import wrapping_util as wrapping_util
import logging
logging.basicConfig()
import ConfigParser
import subprocess 
import csv
import shutil

datasets_repo = "/home/elena/R_ws/automl/ADS_workspace/datasets_repo"
opt_repo = "/home/elena/R_ws/automl/ADS_workspace/opt_repo"
benchmarks_repo = "../benchmarks/automl_benchmarks/rbf_svm_benchmark"
config_file = "config.cfg"
script_path = os.path.dirname(os.path.realpath(__file__))

# load datasets from repo
datasets = []
for root, dirs, files in os.walk(datasets_repo):
    for fi in files:
        if fi.split(".")[-1] == 'csv':
            datasets.append(root + '/' + fi)

# for each one
for dataset in datasets:
    print dataset
    # get name of dataset
    start = dataset.rindex( '/' ) + len('/' )
    end = dataset.rindex( ".csv", start )
    dataset_name = dataset[start:end]

    # create dataset directory
    dataset_opt_repo = opt_repo + '/' + dataset_name 
    if not os.path.exists(dataset_opt_repo):
      os.makedirs(dataset_opt_repo)

    # create benchmark by
    # 1. loading .cfg
    config = ConfigParser.ConfigParser()
    config_path = benchmarks_repo + '/' + config_file
    config.readfp(open(config_path))
    # 2. changing label dataset
    dataset = config.set('HPOLIB', 'dataset', dataset)
    # delete previous experiment directory
    os.chdir(benchmarks_repo)
    run_command = ["echo hyperopt_august2013_mod_*"] 
    process = subprocess.Popen(run_command, shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
    old_exp_dir, err = process.communicate()
    shutil.rmtree(old_exp_dir.rstrip('\n'), ignore_errors=True)
    # optimize with HPOlib-run using tpe and svm
    
    run_command = ["HPOlib-run", "-o", "../../../optimizers/tpe/hyperopt_august2013_mod"]
    subprocess.call(run_command)

    # save plots with HPOlib-plot
    run_command = ["echo basename hyperopt_*/hyperopt_*.pkl"] 
    process = subprocess.Popen(run_command, shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
    pkl_file, err = process.communicate()  
    print pkl_file 
    start = pkl_file.index( "basename" ) + len("basename" )
    end = pkl_file.index( "/", start )
    experiment_dir = pkl_file[(start+1):end] + '/'
    print experiment_dir
    pkl_file = pkl_file[9:-1]
    run_command = ["HPOlib-plot", dataset_name, pkl_file, "-s", opt_repo + '/' + dataset_name + "_Plots", "--maxvalue", "1000"]
    subprocess.call(run_command)

    # create csv with optimized hyperparameters for each dataset
    opt_hparams = []
    run_command = ["HPOlib-getBest" + " " + pkl_file + " " + "-k" + " "  + "1"]
    process = subprocess.Popen(run_command, shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
    opt_hyper = process.communicate()
    start = opt_hyper[0].index("C = ") + len("C = ")
    end =  opt_hyper[0].rindex(",")
    C_value = opt_hyper[0][start:end] 
    start = opt_hyper[0].index("Sigma = ") + len("Sigma = ")
    Sigma_value = opt_hyper[0][start:] 
    opt_hparams.append(float(C_value))
    opt_hparams.append(float(Sigma_value))
    print float(C_value)
    opt_hyper_file = opt_repo + '/' + dataset_name + "_opt.csv"
    os.chdir(script_path)
    writer = csv.writer(open(opt_hyper_file, 'w'))
    writer.writerow(opt_hparams)
    
   
