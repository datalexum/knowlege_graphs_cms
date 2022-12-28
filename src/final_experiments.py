import csv

import numpy as np
from rdflib import Graph
from rdflib_hdt import optimize_sparql, HDTStore

from src.cms.count_min_sketch import CMS
from src.utils.count import count_object_object, count_object_subject, count_bound_object_subject, \
    noise_count_object_subject, noise_count_object_object, noise_count_bound_object_subject
from utils.hash import BasicHashFunction, UniversalHashFunction, IndipendentHashFunction
from utils.error import q_error
from utils.measure import measure_time
from query_templates.queries import object_object_join, object_subject_join, bound_object_subject_join

DATA_PATH = '../watdiv/watdiv_10M_lars.hdt'
RESULT_CSV = 'result.csv'

JOINS = [object_object_join, object_subject_join, bound_object_subject_join]
HASH_FUNCTION_GENERATORS = [BasicHashFunction, UniversalHashFunction, IndipendentHashFunction]
NOISE_REMOVAL_FUNCTIONS = [np.amin, np.median]
QUERY_WITHOUT_NOISE = [count_object_object, count_object_subject, count_bound_object_subject]
QUERY_WITH_NOISE = [noise_count_object_object, noise_count_object_subject, noise_count_bound_object_subject]

NUMBER_RUNS = 5
CMS_WIDTH = 32
CMS_DEPTH = 4

# TODO Find predicates
WHOLE_PREDICATE_1 = '<http://www.geonames.org/ontology#parentCountry>'
WHOLE_PREDICATE_2 = '<http://schema.org/nationality>'
PREDICATE_1 = '<parentCountry>'
PREDICATE_2 = '<nationality>'
OBJECT = ''
PREFIX_1 = '<http://www.geonames.org/ontology#>'
PREFIX_2 = '<http://schema.org/>'

WHOLE_PREDICATES = [[WHOLE_PREDICATE_1, WHOLE_PREDICATE_2], [], []]
PREDICATES = [[PREDICATE_1, PREDICATE_2], [], []]
PREFIXES = [[PREFIX_1, PREFIX_2], [], []]

optimize_sparql()
data_graph = Graph(store=HDTStore(DATA_PATH))

GROUND_TRUTH = []  # TODO Add ground truth

_calc_count = len(HASH_FUNCTION_GENERATORS) * 2 * NUMBER_RUNS * (len(QUERY_WITH_NOISE) + len(QUERY_WITHOUT_NOISE) * 2)

results_dict = {
    "Hash Function": [],
    "Noise Removal": [],
    "Ellapsed Time": [],
    "Join Type": [],
    "Add/Sub": [],
    "Q_Error": []
}

if __name__ == '__main__':
    print("PHASE 0 - Ground Truths")
    for idx, query in enumerate(JOINS):
        result, elapsed_time = measure_time(query, )
        GROUND_TRUTH.append([query.__name__, result])

    # In each Phase all 3 Join Types are tested, so for results regarding the overall comparison of Joins combine Phases 1-X
    print("PHASE 1 - Test without Noise Removal")
    for idx, query in enumerate(QUERY_WITHOUT_NOISE):
        for hash_function in HASH_FUNCTION_GENERATORS:
            for add_sub in (True, False):
                for run in range(NUMBER_RUNS):
                    cms_1 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH * 2, increment_decrement=add_sub,
                                hash_function_generator=hash_function())
                    cms_2 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH * 2, increment_decrement=add_sub,
                                hash_function_generator=hash_function())
                    if 'bound' in query.__name__:
                        count, e_time = measure_time(query, cms_1, cms_2, WHOLE_PREDICATE_1, WHOLE_PREDICATE_2, OBJECT, data_graph)
                    else:
                        count, e_time = measure_time(query, cms_1, cms_2, WHOLE_PREDICATE_1, WHOLE_PREDICATE_2, data_graph)

                    q_error = q_error(count, GROUND_TRUTH[idx])

                    results_dict["Hash Function"].append(hash_function.__name__)
                    results_dict["Noise Removal"].append('No')
                    results_dict["Add/Sub"].append(add_sub)
                    results_dict["Ellapsed Time"].append(e_time)
                    results_dict["Join Type"].append(' '.join(query.__name__.split('_')[1:]))
                    results_dict["Q_Error"].append(q_error)

    print("PHASE 2 - Test with Noise Removal")
    for idx, query in enumerate(QUERY_WITH_NOISE):
        for hash_function in HASH_FUNCTION_GENERATORS:
            for add_sub in (True, False):
                for noise_rem_funct in NOISE_REMOVAL_FUNCTIONS:
                    for run in range(NUMBER_RUNS):
                        cms_1 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH * 2, increment_decrement=add_sub,
                                    hash_function_generator=hash_function())
                        cms_2 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH * 2, increment_decrement=add_sub,
                                    hash_function_generator=hash_function())
                        if 'bound' in query.__name__:
                            count, e_time = measure_time(query, cms_1, cms_2, WHOLE_PREDICATE_1, WHOLE_PREDICATE_2,
                                                         OBJECT, data_graph, noise_rem_funct)
                        else:
                            count, e_time = measure_time(query, cms_1, cms_2, WHOLE_PREDICATE_1, WHOLE_PREDICATE_2,
                                                         data_graph, noise_rem_funct)

                        q_error = q_error(count, GROUND_TRUTH[idx])

                        results_dict["Hash Function"].append(hash_function.__name__)
                        results_dict["Noise Removal"].append(noise_rem_funct.__name__)
                        results_dict["Add/Sub"].append(add_sub)
                        results_dict["Ellapsed Time"].append(e_time)
                        results_dict["Join Type"].append(' '.join(query.__name__.split('_')[2:]))
                        results_dict["Q_Error"].append(q_error)

    with open(RESULT_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(results_dict.keys())
        writer.writerows(zip(*results_dict.values()))
