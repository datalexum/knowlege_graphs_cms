import logging

from src.cms.count_min_sketch import CMS
from src.database_loader.database_loader import DatabaseLoader
from src.query_templates.queries import object_object_join
import numpy as np
from src.utils.count import count_object_object,noise_count_object_object
from utils.hash import BasicHashFunctionGenerator
from rdflib import Graph


# TODO set prefix, check predicates
NUMBER_RUNS = 5
PREDICATE_1 = 'parentCountry'
PREDICATE_2 = 'nationality'
PREFIX_1 = '<http://www.geonames.org/ontology#>'
PREFIX_2 = '<http://schema.org/>'
WHOLE_PREDICATE_1 = '<http://www.geonames.org/ontology#parentCountry>'
WHOLE_PREDICATE_2 = '<http://schema.org/nationality>'
CMS_WIDTH = 16
CMS_DEPTH = 2


def ground_truth(graph):
    return len(object_object_join(data_graph=graph, predicate1=PREDICATE_1, predicate2=PREDICATE_2,
                                  pred_prefix_1=PREFIX_1, pred_prefix_2=PREFIX_2))


def naive_run(graph):
    results = []
    for i in range(NUMBER_RUNS):
        logging.info(f"Naive Approach - Starting {i}/{NUMBER_RUNS}")
        bhg = BasicHashFunctionGenerator()
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


def main():
    #TODO: Untersuchen: Add/Sub ist bei einem groß genugen CMS schlechter, noise removal bei zu kleinen?
    #
    optimize_sparql()

    data_graph = Graph(store=HDTStore("../watdiv/watdiv_10M_lars.hdt"))

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

    logging.info('Starting independent addsub CMS count...')
    addsub_counts = independent_addsub(data_graph)
    addsub_count = np.mean(addsub_counts)
    logging.info('...Independent CMS count finished.')

    print()

    logging.info('Starting independent noise removal min CMS count...')
    noiserem_min_counts = independent_noiserem_min(data_graph)
    noiserem_min_count = np.mean(noiserem_min_counts)
    logging.info('...Independent CMS count finished.')

    print()

    logging.info('Starting independent noise removal min CMS count...')
    noiserem_median_counts = independent_noiserem_min(data_graph)
    noiserem_median_count = np.mean(noiserem_median_counts)
    logging.info('...Independent CMS count finished.')

    print()

    results = {"Naive": naive_count,
               "Independent": indep_count,
               "Add/Sub": addsub_count,
               "Noise Removal min": noiserem_min_count,
               "Noise Removal median": noiserem_median_count}

    print()

    logging.info(f"Ground Truth:        {ground_count} Estimation Rate: 100%")
    logging.info(f"Naive:               {naive_count} Estimation Rate: {(results['Naive'] / ground_count) * 100: .2f}%")
    logging.info(
        f"Independent:         {indep_count} Estimation Rate: {(results['Independent'] / ground_count) * 100: .2f}%")
    logging.info(
        f"Add/Sub:             {addsub_count} Estimation Rate: {(results['Add/Sub'] / ground_count) * 100: .2f}%")
    logging.info(
        f"Noise Removal:       {noiserem_min_count} Estimation Rate: {(results['Noise Removal'] / ground_count) * 100: .2f}%")
    logging.info(
        f"Noise Removal:       {noiserem_median_count} Estimation Rate: {(results['Noise Removal'] / ground_count) * 100: .2f}%")
    best = list(results.keys())[np.argmin(np.abs(np.array(list(results.values())) - 100))]

    print()

    logging.info(f"The best approach is {best} with estimation rate {(results[best] / ground_count) * 100: .5f}%")


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    main()
