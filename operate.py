import tensorflow as tf
import numpy as np
import os
from import_rss import get_blogs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def readfile(filename):
    file = open(filename, "r")
    file_contents = file.readlines()
    # print(file_contents)

    col_names = file_contents[0].strip().split('\t')[1:]
    # print(col_names)
    row_names = []
    data = []

    for line in file_contents[1:]:
        p = line.strip().split('\t')
        row_names.append(p[0])
        data.append([float(x) for x in  p[1:]])

    return row_names, col_names, data

def input_fn():
  return tf.compat.v1.train.limit_epochs(
      tf.convert_to_tensor(dataset), num_epochs=1)

elixir_feeds = ["https://medium.com/feed/@minatsilvester", "https://medium.com/feed/@qertoip",
"https://medium.com/feed/@stueccles", "https://medium.com/feed/@anton.mishchuk"]

get_blogs("elixir", [], elixir_feeds)
num_clusters = 5
kmeans = tf.compat.v1.estimator.experimental.KMeans(num_clusters = num_clusters, use_mini_batch = False)

num_iterations = 10
previous_centers = None
row_names, col_names, data = readfile('blogdata.txt')

for i in data:
    print(len(i))
# raw_dataset = tf.data.TFRecordDataset('blogdata.txt')
# dataset = tf.convert_to_tensor(data)
# print(dataset)
dataset = data[:len(data)-3]
print(dataset)
print(input_fn())
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
            individual_clusters.append(row_names[j])
    clusters.append(individual_clusters)
    individual_clusters = []

for cluster in clusters:
    print(cluster)
