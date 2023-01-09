import copy
import csv
import json
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
import openpyxl

with open('/home/alsch/PycharmProjects/knowlege_graphs_cms/src/experiments/final_experiment_config_2.json', 'r') as f:
    CONFIG = json.load(f)

with open('/home/alsch/PycharmProjects/knowlege_graphs_cms/src/experiments/final_experiment_testdata_2.json', 'r') as f:
    QUERY_DATA = json.load(f)

QUERY_DATA['ground_result'] = []
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


def calculate_ground_truth(excelsheet, excelfile, start):
    excelsheet["A3"] = "Ground Truths amount:"
    excelsheet["B3"] = AMOUNT_QUERIES

    for idx in range(0, AMOUNT_QUERIES):
        function_name = '_'.join(QUERY_DATA['function'][idx].split('_')[1:]) + '_join'
        query_function = getattr(src.query_templates.queries, function_name)
        result, elapsed_time = measure_time(query_function, data_graph,
                                            QUERY_DATA['prefixes'][idx], QUERY_DATA['endings'][idx])
        QUERY_DATA['ground_result'].append(len(result))
        QUERY_DATA['ground_time'].append(elapsed_time)
        pbar.update(1)

        excelsheet[f'A{idx + 4}'] = QUERY_DATA['endings'][idx][0]
        excelsheet[f'B{idx + 4}'] = time.time() - start


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


def run_experiments(excelsheets, excelfile, excelfile2, start):
    global results_dict
    noise_removal_functions = [getattr(np, i) for i in CONFIG['noise_removal_functions']]
    if CONFIG['run_without_removal']: noise_removal_functions.append(None)
    """
    tqdm.write("Precalculating results...")
    s = time.time_ns()
    p1_result = src.utils.count.obj_predicate_query(data_graph, QUERY_DATA['prefixes'][0][0],
                                                    QUERY_DATA['endings'][0][0])
    p1_result = [result.obj for result in p1_result]
    tqdm.write("Calculation of p1 finished!")
    p2_result = src.utils.count.sub_predicate_query(data_graph, QUERY_DATA['prefixes'][0][1],
                                                    QUERY_DATA['endings'][0][1])
    p2_result = [result.sub for result in p2_result]
    tqdm.write("Calculation of p2 finished!")


    global DUR_OFFSET
    #DUR_OFFSET = time.time_ns() - s
    tqdm.write(f"Calculating results took {DUR_OFFSET/1e+9} Seconds!")
    """
    current_excel_index = AMOUNT_QUERIES + 5
    excelsheets[0][f'A{current_excel_index}'] = "Starting CMS tests number runs = " + str(CONFIG['number_runs'])
    lazinesscounters = [current_excel_index + 1, 1]
    for idx in range(AMOUNT_QUERIES):
        query_time_start = time.time()
        excelsheets[0][f'A{lazinesscounters[0]}'] = "Starte nächste Query"
        excelsheets[0][f'B{lazinesscounters[0]}'] = QUERY_DATA['endings'][idx][0]
        lazinesscounters[0] = lazinesscounters[0] + 1

        p1_start = time.time()
        # p1 & p2
        p1_result = src.query_templates.queries.obj_predicate_query(data_graph, QUERY_DATA['prefixes'][idx][0],
                                                                    QUERY_DATA['endings'][idx][0])
        p1 = [results.result for results in p1_result]
        p1_end = time.time() - p1_start
        p2_start = time.time()
        countname = QUERY_DATA['function'][idx]
        if countname == 'count_object_object':
            p2_result = src.query_templates.queries.obj_predicate_query(data_graph, QUERY_DATA['prefixes'][idx][1],
                                                                        QUERY_DATA['endings'][idx][1])
        elif countname == 'count_object_subject':
            p2_result = src.query_templates.queries.sub_predicate_query(data_graph, QUERY_DATA['prefixes'][idx][1],
                                                                        QUERY_DATA['endings'][idx][1])
        elif countname == 'count_bound_object_subject':
            p2_result = src.query_templates.queries.bound_sub_predicate_query(data_graph, QUERY_DATA['prefixes'][idx][1],
                                                                              QUERY_DATA['endings'][idx][1])
        p2 = [results.result for results in p2_result]
        p2_end = time.time() - p2_start
        excelsheets[1][f'A{lazinesscounters[1]}'] = "Calculating time p1 & p2 reused until mentioned again "
        excelsheets[1][f'B{lazinesscounters[1]}'] = p1_end
        excelsheets[1][f'C{lazinesscounters[1]}'] = p2_end
        lazinesscounters[1] = lazinesscounters[1] + 1
        for add_sub in [True, False] if CONFIG['add_sub'] else [False]:
            for hash_function in CONFIG["hash_functions"]:
                hash_function = getattr(src.utils.hash, hash_function)
                for run in range(CONFIG['number_runs']):
                    cms_1_start = time.time()
                    cms_1 = CMS(width=QUERY_DATA['cms_size'][idx], depth=CONFIG['cms_depth'],
                                increment_decrement=add_sub,
                                hash_function_generator=hash_function())
                    for result in p1:
                        cms_1.count(result)
                    cms_1_end = time.time() - cms_1_start

                    cms_2_start = time.time()
                    cms_2 = CMS(width=QUERY_DATA['cms_size'][idx], depth=CONFIG['cms_depth'],
                                increment_decrement=add_sub,
                                hash_function_generator=hash_function())
                    for result in p2:
                        cms_2.count(result)
                    cms_2_end = time.time() - cms_2_start

                    excelsheets[1][
                        f'A{lazinesscounters[1]}'] = "Calculating time CMS1 & CMS2 reused until mentioned again "
                    excelsheets[1][f'B{lazinesscounters[1]}'] = cms_1_end
                    excelsheets[1][f'C{lazinesscounters[1]}'] = cms_2_end
                    lazinesscounters[1] = lazinesscounters[1] + 1

                    for noise_rem_function in noise_removal_functions:
                        print(noise_rem_function)
                        #
                        # this loop is only for excel sheets, not needed in final experiment
                        #
                        for lazyidx, sheet in enumerate(excelsheets):
                            sheet[f'A{lazinesscounters[lazyidx]}'] = "Starte nächste Config"
                            sheet[f'B{lazinesscounters[lazyidx]}'] = str(hash_function)
                            if add_sub:
                                sheet[f'C{lazinesscounters[lazyidx]}'] = "add_sub"
                            else:
                                sheet[f'C{lazinesscounters[lazyidx]}'] = "no add_sub"
                            sheet[f'D{lazinesscounters[lazyidx]}'] = "noise_rem_function: "
                            sheet[f'E{lazinesscounters[lazyidx]}'] = str(noise_rem_function)
                            sheet[f'F{lazinesscounters[lazyidx]}'] = "run NR: "
                            sheet[f'G{lazinesscounters[lazyidx]}'] = run + 1
                        lazinesscounters[0] = lazinesscounters[0] + 1
                        lazinesscounters[1] = lazinesscounters[1] + 1
                        count_time_start = time.time()
                        run_cms_count(add_sub, hash_function, idx, noise_rem_function,
                                      data_graph, p1, p2, cms_1, cms_2)
                        count_time_end = time.time() - count_time_start
                        excelsheets[0][f'A{lazinesscounters[0]}'] = "run done"
                        excelsheets[0][f'B{lazinesscounters[0]}'] = time.time() - start
                        excelsheets[1][f'A{lazinesscounters[1]}'] = "run done"
                        excelsheets[1][f'B{lazinesscounters[1]}'] = count_time_end
                        lazinesscounters[0] = lazinesscounters[0] + 1
                        lazinesscounters[1] = lazinesscounters[1] + 1
                        pbar.update(1)

        excelsheets[0][f'A{lazinesscounters[0]}'] = "Query beendet " + QUERY_DATA['endings'][idx][0]
        excelsheets[0][f'B{lazinesscounters[0]}'] = time.time() - start
        lazinesscounters[0] = lazinesscounters[0] + 3
        excelsheets[1][f'A{lazinesscounters[1]}'] = "Query beendet " + QUERY_DATA['endings'][idx][0]
        excelsheets[1][f'B{lazinesscounters[1]}'] = time.time() - query_time_start
        lazinesscounters[1] = lazinesscounters[1] + 3

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

    excelfile.save("Overall times.xlsx")
    excelfile2.save("Individual times.xlsx")


def main():
    excelfile = openpyxl.Workbook()
    excelfile2 = openpyxl.Workbook()
    excelsheet = excelfile.active
    excelsheet2 = excelfile2.active
    excelsheet["A1"] = "Task"
    excelsheet["B1"] = "Current Time"
    excelsheets = [excelsheet, excelsheet2]
    start = time.time()
    excelsheet["A2"] = "Ground truth Start"
    excelsheet["B2"] = time.time() - start

    tqdm.write("PHASE 0 - Ground Truths")
    calculate_ground_truth(excelsheet, excelfile, start)
    tqdm.write(str(QUERY_DATA))
    # In each Phase all 3 Join Types are tested, so for results regarding the overall comparison of Joins combine
    # Phases 1-X
    tqdm.write("PHASE 1 - Test without Noise Removal")
    run_experiments(excelsheets, excelfile, excelfile2, start)
    excelfile.save("TimesAndBottlenecks.xlsx")


if __name__ == '__main__':
    main()
