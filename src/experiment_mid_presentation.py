import logging

from src.cms.count_min_sketch import CMS
from src.database_loader.database_loader import DatabaseLoader
from src.query_templates.queries import object_object_join
import numpy as np

from src.utils.count import count_object_object
from utils.hash import BasicHashFunctionGenerator

# TODO set prefix, check predicates
NUMBER_RUNS = 5
PREDICATE_1 = 'gn:parentCountry'
PREDICATE_2 = 'sorg:nationality'
PREFIX = ''
CMS_WIDTH = 20
CMS_DEPTH = 4


def ground_truth(graph):
    return len(object_object_join(data_graph=graph, predicate1=PREDICATE_1, predicate2=PREDICATE_2,
                                  pred_prefix_1=PREFIX, pred_prefix_2=PREFIX))


def naive_run(graph):
    results = []
    for i in range(NUMBER_RUNS):
        logging.info(f"Naive Approach - Starting {i}/{NUMBER_RUNS}")
        bhg = BasicHashFunctionGenerator()
        cms_1 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH, hash_function_generator=bhg)
        cms_2 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH, hash_function_generator=bhg)
        count = count_object_object(cms_1, cms_2, PREDICATE_1, PREDICATE_2, graph)
        results.append(count)
    return results


def independent_hash(graph):
    results = []
    for i in range(NUMBER_RUNS):
        logging.info(f"Independent Approach - Starting {i}/{NUMBER_RUNS}")
        cms_1 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH)
        cms_2 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH)
        count = count_object_object(cms_1, cms_2, PREDICATE_1, PREDICATE_2, graph)
        results.append(count)
    return results


def independent_addsub(graph):
    results = []
    for i in range(NUMBER_RUNS):
        logging.info(f"Add/Sub Approach - Starting {i}/{NUMBER_RUNS}")
        cms_1 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH * 2, increment_decrement=True)
        cms_2 = CMS(width=CMS_WIDTH, depth=CMS_DEPTH * 2, increment_decrement=True)
        count = count_object_object(cms_1, cms_2, PREDICATE_1, PREDICATE_2, graph)
        results.append(count)
    return results


def independent_noiserem(graph):
    results = []
    # TODO Add Noise Removal run
    return results


def main():
    # TODO change to WatDiv
    datalist = [["../data/yago-1.0.0-turtle.ttl",
                 "ttl"]]
    Loader = DatabaseLoader(datalist)
    data_graph = Loader.return_Databases()

    logging.info('Calculating ground truth...')
    ground_count = ground_truth(data_graph)
    logging.info('...Ground truth calculation finished.')

    print()

    logging.info('Starting naive CMS count...')
    naive_counts = naive_run(data_graph)
    naive_count = np.mean(naive_counts)
    logging.info('...Naive CMS count finished.')

    print()

    logging.info('Starting independent CMS count...')
    indep_counts = independent_hash(data_graph)
    indep_count = np.mean(indep_counts)
    logging.info('...Independent CMS count finished.')

    print()

    logging.info('Starting independent CMS count...')
    addsub_counts = independent_addsub(data_graph)
    addsub_count = np.mean(addsub_counts)
    logging.info('...Independent CMS count finished.')

    print()

    logging.info('Starting independent CMS count...')
    noiserem_counts = independent_noiserem(data_graph)
    noiserem_count = np.mean(noiserem_counts)
    logging.info('...Independent CMS count finished.')

    results = {"Naive": naive_count,
               "Independent": indep_count,
               "Add/Sub": addsub_count,
               "Noise Removal": noiserem_count}

    print()

    logging.info(f"Ground Truth:        {ground_count} Estimation Rate: 100%")
    logging.info(f"Naive:               {naive_count} Estimation Rate: {(results['Naive'] / ground_count) * 100: .2f}%")
    logging.info(
        f"Independent:         {indep_count} Estimation Rate: {(results['Independent'] / ground_count) * 100: .2f}%")
    logging.info(
        f"Add/Sub:             {addsub_count} Estimation Rate: {(results['Add/Sub'] / ground_count) * 100: .2f}%")
    logging.info(
        f"Noise Removal:       {noiserem_count} Estimation Rate: {(results['Noise Removal'] / ground_count) * 100: .2f}%")

    best = list(results.keys())[np.argmin(np.abs(np.array(list(results.values())) - 100))]

    print()

    logging.info(f"The best approach is {best} with estimation rate {(results[best] / ground_count) * 100: .5f}%")


if __name__ == '__main__':
    main()
