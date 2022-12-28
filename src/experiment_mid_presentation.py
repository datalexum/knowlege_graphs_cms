import logging

from rdflib_hdt import optimize_sparql, HDTStore

from src.cms.count_min_sketch import CMS
from src.query_templates.queries import object_object_join
import numpy as np
from src.utils.count import count_object_object, noise_count_object_object
from src.utils.error import q_error
from src.utils.measure import measure_time
from utils.hash import BasicHashFunction
from rdflib import Graph

NUMBER_RUNS = 1
PREDICATE_1 = 'parentCountry'
PREDICATE_2 = 'nationality'
PREFIX_1 = '<http://www.geonames.org/ontology#>'
PREFIX_2 = '<http://schema.org/>'
WHOLE_PREDICATE_1 = '<http://www.geonames.org/ontology#parentCountry>'
WHOLE_PREDICATE_2 = '<http://schema.org/nationality>'
CMS_WIDTH = 32
CMS_DEPTH = 4


def ground_truth(graph):
    return len(object_object_join(data_graph=graph, predicate1=PREDICATE_1, predicate2=PREDICATE_2,
                                  pred_prefix_1=PREFIX_1, pred_prefix_2=PREFIX_2))


def naive_run(graph):
    results = []
    for i in range(NUMBER_RUNS):
        logging.info(f"Naive Approach - Starting {i}/{NUMBER_RUNS}")
        bhg = BasicHashFunction()
        cms_1 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH, hash_function_generator=bhg)
        cms_2 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH, hash_function_generator=bhg)
        count = count_object_object(cms_1, cms_2, WHOLE_PREDICATE_1, WHOLE_PREDICATE_2, graph)
        results.append(count)
    return results


def independent_hash(graph):
    results = []
    for i in range(NUMBER_RUNS):
        logging.info(f"Independent Approach - Starting {i}/{NUMBER_RUNS}")
        cms_1 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH)
        cms_2 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH)
        count = count_object_object(cms_1, cms_2, WHOLE_PREDICATE_1, WHOLE_PREDICATE_2, graph)
        results.append(count)
    return results


def independent_addsub(graph):
    results = []
    for i in range(NUMBER_RUNS):
        logging.info(f"Add/Sub Approach - Starting {i}/{NUMBER_RUNS}")
        cms_1 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH * 2, increment_decrement=True)
        cms_2 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH * 2, increment_decrement=True)
        count = count_object_object(cms_1, cms_2, WHOLE_PREDICATE_1, WHOLE_PREDICATE_2, graph)
        results.append(count)
    return results


def independent_noiserem_min(graph):
    results = []
    for i in range(NUMBER_RUNS):
        logging.info(f"Noise Removal Approach - Starting {i}/{NUMBER_RUNS}")
        cms_1 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH)
        cms_2 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH)
        count = noise_count_object_object(cms_1, cms_2, WHOLE_PREDICATE_1, WHOLE_PREDICATE_2, graph, np.amin)
        results.append(count)
    return results


def independent_noiserem_median(graph):
    results = []
    for i in range(NUMBER_RUNS):
        logging.info(f"Noise Removal Approach - Starting {i}/{NUMBER_RUNS}")
        cms_1 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH)
        cms_2 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH)
        count = noise_count_object_object(cms_1, cms_2, WHOLE_PREDICATE_1, WHOLE_PREDICATE_2, graph, np.median)
        results.append(count)
    return results


def naive_noiserem_median(graph):
    results = []
    for i in range(NUMBER_RUNS):
        logging.info(f"Naive Approach - Starting {i}/{NUMBER_RUNS}")
        bhg = BasicHashFunction()
        cms_1 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH, hash_function_generator=bhg)
        cms_2 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH, hash_function_generator=bhg)
        count = noise_count_object_object(cms_1, cms_2, WHOLE_PREDICATE_1, WHOLE_PREDICATE_2, graph, np.median)
        results.append(count)
    return results


def naive_noiserem_min(graph):
    results = []
    for i in range(NUMBER_RUNS):
        logging.info(f"Naive Approach - Starting {i}/{NUMBER_RUNS}")
        bhg = BasicHashFunction()
        cms_1 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH, hash_function_generator=bhg)
        cms_2 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH, hash_function_generator=bhg)
        count = noise_count_object_object(cms_1, cms_2, WHOLE_PREDICATE_1, WHOLE_PREDICATE_2, graph, np.amin)
        results.append(count)
    return results


def main():
    optimize_sparql()

    data_graph = Graph(store=HDTStore("../watdiv/watdiv_10M_lars.hdt"))

    logging.info('Calculating ground truth...')
    ground_count, ellapsed_ground = measure_time(ground_truth, data_graph)
    logging.info('...Ground truth calculation finished.')

    print()

    logging.info('Starting naive CMS count...')
    naive_counts, ellapsed_naive = measure_time(naive_run, data_graph)
    ellapsed_naive = ellapsed_naive / NUMBER_RUNS
    naive_count = np.mean(naive_counts)
    logging.info('...Naive CMS count finished.')

    print()

    logging.info('Starting independent CMS count...')
    indep_counts, ellapsed_indep = measure_time(independent_hash, data_graph)
    ellapsed_indep = ellapsed_indep / NUMBER_RUNS
    indep_count = np.mean(indep_counts)
    logging.info('...Independent CMS count finished.')

    print()

    logging.info('Starting independent addsub CMS count...')
    addsub_counts, ellapsed_addsub = measure_time(independent_hash, data_graph)
    ellapsed_addsub = ellapsed_addsub / NUMBER_RUNS
    addsub_count = np.mean(addsub_counts)
    logging.info('...Independent CMS count finished.')

    print()

    logging.info('Starting independent noise removal min CMS count...')
    noiserem_min_counts, ellapsed_noiserem_min = measure_time(independent_noiserem_min, data_graph)
    ellapsed_noiserem_min = ellapsed_noiserem_min / NUMBER_RUNS
    noiserem_min_count = np.mean(noiserem_min_counts)
    logging.info('...Independent CMS count finished.')

    print()

    logging.info('Starting independent noise removal min CMS count...')
    noiserem_median_counts, ellapsed_noiserem_median = measure_time(naive_noiserem_median, data_graph)
    ellapsed_noiserem_median = ellapsed_noiserem_median / NUMBER_RUNS
    noiserem_median_count = np.mean(noiserem_median_counts)
    logging.info('...Independent CMS count finished.')

    print()

    logging.info('Starting naive noise removal min CMS count...')
    noiserem_naive_min_counts, ellapsed_noiserem_naive_min = measure_time(naive_noiserem_min, data_graph)
    ellapsed_noiserem_naive_min = ellapsed_noiserem_naive_min / NUMBER_RUNS
    noiserem_naive_min_count = np.mean(noiserem_median_counts)
    logging.info('...naive CMS count finished.')

    print()

    logging.info('Starting naive noise removal median CMS count...')
    noiserem_naive_median_counts, ellapsed_noiserem_naive_median = measure_time(naive_noiserem_median, data_graph)
    ellapsed_noiserem_naive_median = ellapsed_noiserem_naive_median / NUMBER_RUNS
    noiserem_naive_median_count = np.mean(noiserem_median_counts)
    logging.info('...naive CMS count finished.')

    print()

    results = {"Naive": (naive_count, ellapsed_naive),
               "Independent": (indep_count, ellapsed_indep),
               "Add/Sub": (addsub_count, ellapsed_addsub),
               "Noise Removal min": (noiserem_min_count, ellapsed_noiserem_min),
               "Noise Removal median": (noiserem_median_count, ellapsed_noiserem_median),
               "Noise Removal min naive": (noiserem_naive_min_count, ellapsed_noiserem_naive_min),
               "Noise Removal median naive": (noiserem_naive_median_count, ellapsed_noiserem_naive_median)}
    print(results)

    logging.info(f"Ground Truth:        {ground_count} Q-Error: 0%, Execution Time: {ellapsed_ground/1000000.0}ms")
    for key in results:
        logging.info(
            f"{key}:\t\t\t{results[key]}\tQ-Error: {q_error(results[key][0], ground_count) * 100: .2f}%, Execution Time: {results[key][1]/1000000.0}ms")

    q_error_list = np.fromiter((q_error(xi[0], ground_count) for xi in results.values()), float)

    best = list(results.keys())[np.argmin(q_error_list)]

    print()
    print(q_error_list)
    logging.info(f"The best approach is {best} with Q-Error rate {np.min(q_error_list) *  100: .2f}%")


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    main()
