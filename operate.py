import tensorflow as tf
import numpy as np
import os
from import_rss import get_blogs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# def readfile(filename):
#     file = open(filename, "r")
#     file_contents = file.readlines()
#     # print(file_contents)
#
#     col_names = file_contents[0].strip().split('\t')[1:]
#     # print(col_names)
#     titles = []
#     data = []
#
#     for line in file_contents[1:]:
#         p = line.strip().split('\t')
#         titles.append(p[0])
#         data.append([float(x) for x in  p[1:]])
#
#
#     return titles, col_names, data

# def input_fn():
#   return tf.compat.v1.train.limit_epochs(
#       tf.convert_to_tensor(data), num_epochs=1)


def start(keyword, user_read_urls, feeds):
    elixir_feeds = ["https://medium.com/feed/@minatsilvester", "https://medium.com/feed/@qertoip",
    "https://medium.com/feed/@stueccles", "https://medium.com/feed/@anton.mishchuk"]
    titles, data = get_blogs("elixir", [], elixir_feeds)
    # titles, data = get_blogs(keyword, user_read_urls, feeds)
    print(data)
    num_clusters = 6
    kmeans = tf.compat.v1.estimator.experimental.KMeans(num_clusters = num_clusters, use_mini_batch = False)
    num_iterations = 10
    previous_centers = None

    def input_fn():
      return tf.compat.v1.train.limit_epochs(
          tf.convert_to_tensor(data), num_epochs=1)

        # titles, col_names, data = readfile('blogdata.txt')

    # for i in data:
    #     print(len(i))
        # print(len(col_names))
        # print(data)
        # raw_dataset = tf.data.TFRecordDataset('blogdata.txt')
        # dataset = tf.convert_to_tensor(data)
        # dataset = data[:len(data)-3]
        # print(input_fn())
        # print(dataset)
    for _ in range(num_iterations):
        kmeans.train(input_fn)
        cluster_centers = kmeans.cluster_centers()
        if previous_centers is not None:
            print('delta:', cluster_centers - previous_centers)
        previous_centers = cluster_centers
        print('score:', kmeans.score(input_fn))
    print('cluster centers:', cluster_centers)

    cluster_indices = list(kmeans.predict_cluster_index(input_fn))


    clusters = []
    individual_clusters = []
    print(cluster_indices)
    for i in range(num_clusters):
        for j in range(len(cluster_indices)):
            if i == cluster_indices[j]:
                individual_clusters.append(titles[j])
        clusters.append(individual_clusters)
        individual_clusters = []

    for cluster in clusters:
        print(cluster)

# keyword = input("Enter the keyword\n")
# user_feed_str = input("Enter the feed urls seperated by ',' or enter none if no data available\n")
# feed_str = input("enter the feed urls seperated by a ','\n")
#
# if(user_feed_str == "none"):
#     user_read_urls = []
# else:
#     user_read_urls = user_feed_str.split(',')
#
# feeds = feed_str.split(',')
#
#
# start(keyword, user_read_urls, feeds)
start("elixir", [], ["https://medium.com/feed/@minatsilvester", "https://medium.com/feed/@qertoip",
"https://medium.com/feed/@stueccles", "https://medium.com/feed/@anton.mishchuk"])
