import copy
import csv
import json
import os
import pickle
import sys
import time

sys.path.append('./')

import numpy as np
from rdflib import Graph
from rdflib_hdt import optimize_sparql, HDTStore

from src.cms.count_min_sketch import CMS
import src.query_templates.queries
import src.utils.count

from tqdm import tqdm
import src.utils.hash
from src.utils.error import q_error
from src.utils.measure import measure_time

with open('/home/alsch/PycharmProjects/knowlege_graphs_cms/src/experiments/final_experiment_config.json', 'r') as f:
    CONFIG = json.load(f)

with open('/home/alsch/PycharmProjects/knowlege_graphs_cms/src/experiments/final_experiment_testdata_2.json', 'r') as f:
    QUERY_DATA = json.load(f)

QUERY_DATA['ground_result'] = [] if 'ground_result' not in QUERY_DATA.keys() else QUERY_DATA['ground_result']
QUERY_DATA['ground_time'] = []

AMOUNT_QUERIES = len(QUERY_DATA['function'])
START_FROM = 0
DUR_OFFSET = 0

optimize_sparql()
data_graph = Graph(store=HDTStore(CONFIG['data_path']))

_calc_count = AMOUNT_QUERIES * len(CONFIG['hash_functions']) * (
        len(CONFIG['noise_removal_functions']) + CONFIG['run_without_removal']) * (1 + CONFIG['add_sub']) * CONFIG[
                  'number_runs'] + AMOUNT_QUERIES
pbar = tqdm(total=_calc_count, colour='#FF69B4')
pbar.update(START_FROM)

results_dict = {
    "Endings": [],
    "Hash Function": [],
    "Noise Removal": [],
    "Ellapsed Time": [],
    "Join Type": [],
    "Add/Sub": [],
    "Q_Error": [],
    "Count": []
}


def calculate_ground_truth():
    for idx in range(0, AMOUNT_QUERIES):
        function_name = '_'.join(QUERY_DATA['function'][idx].split('_')[1:]) + '_join'
        query_function = getattr(src.query_templates.queries, function_name)
        result, elapsed_time = measure_time(query_function, data_graph,
                                            QUERY_DATA['prefixes'][idx], QUERY_DATA['endings'][idx])
        QUERY_DATA['ground_result'].append(len(result))
        QUERY_DATA['ground_time'].append(elapsed_time)
        pbar.update(1)


def add_result(idx, hash_function, noise, add_sub, time_ellapsed, cms_count):
    results_dict["Hash Function"].append(hash_function.__name__)
    results_dict["Noise Removal"].append('No' if noise is None else noise.__name__)
    results_dict["Add/Sub"].append(add_sub)
    results_dict["Ellapsed Time"].append(time_ellapsed)
    results_dict["Join Type"].append(' '.join(QUERY_DATA['function'][idx].split('_')[1:]))
    results_dict["Q_Error"].append(q_error(cms_count, QUERY_DATA['ground_result'][idx]))
    results_dict["Count"].append(cms_count)
    results_dict["Endings"].append(QUERY_DATA['endings'][idx])
    tqdm.write(str(results_dict))



def run_cms_count(add_sub, hash_function, idx, noise_rem_function, data_graph, p1, p2, cms_1, cms_2):
    count_function = getattr(src.utils.count, QUERY_DATA['function'][idx])
    count, e_time = count_function(copy.deepcopy(cms_1), copy.deepcopy(cms_2), QUERY_DATA['prefixes'][idx],
                                   QUERY_DATA['endings'][idx],
                                   data_graph, True, noise_rem_function, p1, p2)
    add_result(idx, hash_function, noise_rem_function, add_sub, e_time + DUR_OFFSET, count)


def generate_file_name(join: str, prefix, ending):
    name = join + '_' + prefix[1:-1].replace('/', '_') + ending + '.pickle'
    return name


def run_experiments():
    global results_dict
    noise_removal_functions = [getattr(np, i) for i in CONFIG['noise_removal_functions']]
    if CONFIG['run_without_removal']: noise_removal_functions.append(None)

    for idx in range(AMOUNT_QUERIES):

        files = os.listdir(CONFIG['precalculated_path'])
        p1_filename = generate_file_name('count_object_object', QUERY_DATA['prefixes'][idx][0],
                                         QUERY_DATA['endings'][idx][0])

        if p1_filename in files:
            with open(os.path.join(CONFIG['precalculated_path'], p1_filename), 'rb') as p1_file:
                p1 = pickle.load(p1_file)
        else:
            p1_result = src.query_templates.queries.obj_predicate_query(data_graph, QUERY_DATA['prefixes'][idx][0],
                                                                        QUERY_DATA['endings'][idx][0])
            p1 = [results.result for results in p1_result]
            with open(os.path.join(CONFIG['precalculated_path'], p1_filename), 'wb') as p1_file:
                pickle.dump(p1, p1_file)

        countname = QUERY_DATA['function'][idx]
        p2_filename = generate_file_name('count_object_object', QUERY_DATA['prefixes'][idx][1],
                                         QUERY_DATA['endings'][idx][1])

        if p2_filename in files:
            with open(os.path.join(CONFIG['precalculated_path'], p2_filename), 'rb') as p2_file:
                p2 = pickle.load(p2_file)
        else:
            if countname == 'count_object_object':
                p2_result = src.query_templates.queries.obj_predicate_query(data_graph, QUERY_DATA['prefixes'][idx][1],
                                                                            QUERY_DATA['endings'][idx][1])
            elif countname == 'count_object_subject':
                p2_result = src.query_templates.queries.sub_predicate_query(data_graph, QUERY_DATA['prefixes'][idx][1],
                                                                            QUERY_DATA['endings'][idx][1])
            elif countname == 'count_bound_object_subject':
                p2_result = src.query_templates.queries.bound_sub_predicate_query(data_graph,
                                                                                  QUERY_DATA['prefixes'][idx][1],
                                                                                  QUERY_DATA['endings'][idx][1])
            p2 = [results.result for results in p2_result]
            with open(os.path.join(CONFIG['precalculated_path'], p2_filename), 'wb') as p2_file:
                pickle.dump(p2, p2_file)

        for add_sub in [True, False] if CONFIG['add_sub'] else [False]:
            for hash_function in CONFIG["hash_functions"]:
                hash_function = getattr(src.utils.hash, hash_function)
                for run in range(CONFIG['number_runs']):
                    cms_1 = CMS(width=QUERY_DATA['cms_size'][idx], depth=CONFIG['cms_depth'],
                                increment_decrement=add_sub,
                                hash_function_generator=hash_function())
                    for result in p1:
                        cms_1.count(result)

                    cms_2 = CMS(width=QUERY_DATA['cms_size'][idx], depth=CONFIG['cms_depth'],
                                increment_decrement=add_sub,
                                hash_function_generator=hash_function())
                    for result in p2:
                        cms_2.count(result)

                    for noise_rem_function in noise_removal_functions:
                        run_cms_count(add_sub, hash_function, idx, noise_rem_function,
                                      data_graph, p1, p2, cms_1, cms_2)
                        pbar.update(1)

        with open(f"{CONFIG['result_file']}{idx} + .txt", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(results_dict.keys())
            writer.writerows(zip(*results_dict.values()))

        results_dict = {
            "Endings": [],
            "Hash Function": [],
            "Noise Removal": [],
            "Ellapsed Time": [],
            "Join Type": [],
            "Add/Sub": [],
            "Q_Error": [],
            "Count": []
        }


def main():
    tqdm.write("PHASE 0 - Ground Truths")
    if len(QUERY_DATA['ground_result']) == 0:
        calculate_ground_truth()
    tqdm.write(str(QUERY_DATA))
    # In each Phase all 3 Join Types are tested, so for results regarding the overall comparison of Joins combine
    # Phases 1-X
    tqdm.write("PHASE 1 - Test without Noise Removal")
    run_experiments()


if __name__ == '__main__':
    main()
