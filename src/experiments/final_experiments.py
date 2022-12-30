import csv
import json

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

with open('/home/alsch/PycharmProjects/knowlege_graphs_cms/src/experiments/final_experiment_testdata.json', 'r') as f:
    QUERY_DATA = json.load(f)

QUERY_DATA['ground_result'] = []
QUERY_DATA['ground_time'] = []

AMOUNT_QUERIES = len(QUERY_DATA['function'])

optimize_sparql()
data_graph = Graph(store=HDTStore(CONFIG['data_path']))

_calc_count = AMOUNT_QUERIES * len(CONFIG['hash_functions']) * (len(CONFIG['noise_removal_functions'])+CONFIG['run_without_removal']) * (1+CONFIG['add_sub']) * CONFIG['number_runs'] + AMOUNT_QUERIES
pbar = tqdm(total=_calc_count, colour='#FF69B4')

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
    for idx in range(AMOUNT_QUERIES):
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


def run_cms_count(add_sub, hash_function, idx, noise_rem_function, data_graph):
    cms_1 = CMS(width=CONFIG['cms_width'], depth=CONFIG['cms_depth'] * 2, increment_decrement=add_sub,
                hash_function_generator=hash_function())
    cms_2 = CMS(width=CONFIG['cms_width'], depth=CONFIG['cms_depth'] * 2, increment_decrement=add_sub,
                hash_function_generator=hash_function())
    count_function = getattr(src.utils.count, QUERY_DATA['function'][idx])
    count, e_time = measure_time(count_function, cms_1, cms_2,  QUERY_DATA['prefixes'][idx], QUERY_DATA['endings'][idx],
                                 data_graph, noise_rem_function)
    add_result(idx, hash_function, noise_rem_function, add_sub, e_time, count)


def run_experiments():
    noise_removal_functions = [getattr(np, i) for i in CONFIG['noise_removal_functions']]
    if CONFIG['run_without_removal']: noise_removal_functions.append(None)

    for idx in range(AMOUNT_QUERIES):
        for hash_function in CONFIG["hash_functions"]:
            for add_sub in [True, False] if CONFIG['add_sub'] else [False]:
                for noise_rem_function in noise_removal_functions:
                    for run in range(CONFIG['number_runs']):
                        run_cms_count(add_sub, getattr(src.utils.hash, hash_function), idx, noise_rem_function, data_graph)
                        pbar.update(1)


def save_results():
    with open(CONFIG['result_file'], 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(results_dict.keys())
        writer.writerows(zip(*results_dict.values()))


def main():
    tqdm.write("PHASE 0 - Ground Truths")
    calculate_ground_truth()
    tqdm.write(str(QUERY_DATA))
    # In each Phase all 3 Join Types are tested, so for results regarding the overall comparison of Joins combine
    # Phases 1-X
    tqdm.write("PHASE 1 - Test without Noise Removal")
    run_experiments()
    save_results()


if __name__ == '__main__':
    main()
