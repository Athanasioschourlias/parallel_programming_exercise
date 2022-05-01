import csv
import logging
import urllib.request
import time
import bs4
import concurrent.futures

import numpy
import requests
import threading
import _thread
import multiprocessing
import os
import Monitor as mon
import signal

with open(os.path.join(os.getcwd(), "task_3", "wikipedia", "wikipedia_urls" + ".txt"), 'r') as f:
    file_content = f.read()
    articles_urls = file_content.split('\n')


def article_scraper(url):
    response = requests.get(url)
    if response is not None:
        html = bs4.BeautifulSoup(response.text, 'html.parser')
        title = html.select("#firstHeading")[0].text
        paragraphs = html.select("p")
        textual_data = " ".join([para.text for para in paragraphs[0:5]])
    return textual_data.split(" ")


def pos_neg_words():
    with open(os.path.join(os.getcwd(), "task_3", "words", "positive_words" + ".txt"), 'r') as fp:
        file_pos_content = fp.read()
        lpositive_words = file_pos_content.split('\n')

    with open(os.path.join(os.getcwd(), "task_3", "words", "negative_words" + ".txt"), 'r') as fn:
        file_neg_content = fn.read()
        lnegative_words = file_neg_content.split('\n')

    return lpositive_words, lnegative_words


def article_sentiment_analysis(num_article):
    lpos_words, lneg_words = pos_neg_words()
    article_words = article_scraper(articles_urls[num_article])
    spos_words, sneg_words, sarticle_words = set(lpos_words), set(lneg_words), set(article_words)
    num_pos_words = len(spos_words.intersection(sarticle_words))
    num_neg_words = len(sneg_words.intersection(sarticle_words))
    # print(num_pos_words,num_neg_words, end=" ")
    if num_pos_words == num_neg_words or num_pos_words + 1 == num_neg_words or num_pos_words == num_neg_words + 1: return \
        articles_urls[num_article].split("/")[-1], "neutral"
    return (articles_urls[num_article].split("/")[-1], "positive") if num_pos_words > num_neg_words else (
        articles_urls[num_article].split("/")[-1], "negative")


def run_analysis(start, stop):
    for i in range(start, stop):
        article_sentiment_analysis(i)


def run_multiprocessing_experiment(process_num=6):
    # Number of processes
    N = process_num
    # Building the tuples of how the article should be devided
    data = []
    for x in range(N):
        start = int(x * numpy.floor((len(articles_urls) / N)))
        end = int(start + numpy.floor((len(articles_urls) / N)))
        if x != N - 1:
            data.append((start, end)) if end <= len(articles_urls) else data.append((start, len(articles_urls)))
        else:
            data.append((start, len(articles_urls)))
    print(data)
    start_time = time.time()
    with multiprocessing.Pool(N) as p:
        # from documentation we know that starmap_async maintains order of the result.
        # So its safe to asume that we would not have ANY race condition at the end.
        p.starmap(
            run_analysis,
            data
        )
    return time.time() - start_time


def run_multithreading_experiment(thread_num=4):
    N = thread_num
    # Building the tuples of how the article should be devided
    data = []
    for x in range(N):
        start = int(x * numpy.floor((len(articles_urls) / N)))
        end = int(start + numpy.floor((len(articles_urls) / N)))
        if x != N - 1:
            data.append((start, end)) if end <= len(articles_urls) else data.append((start, len(articles_urls)))
        else:
            data.append((start, len(articles_urls)))
    print(data)
    threads = list()
    start_time = time.time()
    for start, end in data:
        t = threading.Thread(target=run_analysis, args=(start, end))
        threads.append(t)
        t.start()

    for index, thread in enumerate(threads):
        thread.join()
    return time.time() - start_time


if __name__ == '__main__':
    a = mon.Monitor([], [])
    stop_threads = False

    t1 = threading.Thread(target=a.monitor_cpu, args=(lambda: stop_threads,))
    t2 = threading.Thread(target=a.monitor_ram, args=(lambda: stop_threads,))

    # starting monitoring threads
    t1.start()
    t2.start()

    # Multiprocessing experiment
    # total_time = run_multiprocessing_experiment()

    # Multithreading experiment
    total_time = run_multithreading_experiment(10)

    # Stoping our monitoring threads
    stop_threads = True
    t1.join()
    t2.join()

    # writing raw data to coresponding csv files
    run_name = 'Mutlithreading_run_2_12_threads'
    with open(os.path.join(os.getcwd(), "task_3", "out", "Total_time" + ".csv"), 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([run_name, str(total_time)])

    a.save_cpu_ram(os.path.join(os.getcwd(), "task_3", "out", run_name + ".csv"), ["CPU", "RAM"])

    # Creating the vizulization for the data
    b = mon.VizualizeMonitoring(a.cpu_util, a.ram_util)
    b()
