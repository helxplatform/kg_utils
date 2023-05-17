import glob
import os
import pathlib
import orjson as json
from kg_utils.merging import DiskGraphMerger, DEFAULT_EDGE_PROPERTIES_THAT_SHOULD_BE_SETS, DEFAULT_NODE_PROPERTIES_THAT_SHOULD_BE_SETS
import shutil


def jsonl_iter(file_name):
    # iterating over jsonl files
    with open(file_name) as stream:
        for line in stream:
            # yield on line at time
            yield json.loads(line)


def json_iter(json_file,entity_key):
    with open(json_file) as stream:
        data = json.loads(stream.read())
        return data[entity_key]


def clean_up_dir(dir):
    if pathlib.Path(dir).exists():
        shutil.rmtree(dir)

if __name__ == '__main__':
    # create a disk merger with default paramters
    disk_merger = DiskGraphMerger(node_properties_that_should_be_sets=DEFAULT_NODE_PROPERTIES_THAT_SHOULD_BE_SETS,
                                  edge_properties_that_should_be_sets=DEFAULT_EDGE_PROPERTIES_THAT_SHOULD_BE_SETS)
    # we could use chain to create a single iterable mixed of lists and generator functions
    from itertools import chain
    # chain the node iterators
    nodes = chain(
        jsonl_iter('./data/graph_2_nodes.jsonl'),
        json_iter('./data/graph1.json', 'nodes')
    )
    # chain the edge iterators
    edges = chain(
        jsonl_iter('./data/graph_2_edges.jsonl'),
        json_iter('./data/graph1.json', 'edges')
    )

    # Disk merger needs  temporary directory, set it up if it doesn't exist
    clean_up_dir('./tmp')

    if not pathlib.Path('./tmp').exists():
        os.mkdir('./tmp')

    # clean up files in temp

    # set the temp_directory attribute here.
    disk_merger.temp_directory = './tmp'

    # perform merge nodes on the nodes
    disk_merger.merge_nodes(nodes)
    # perform merge edges on the edges
    disk_merger.merge_edges(edges)

    # create an output directory
    if not pathlib.Path('./output').exists():
        os.mkdir('./output')

    # stream out nodes to nodes.jsonl file
    with open('./output/nodes.jsonl', 'w') as stream:
        for nodes in disk_merger.get_merged_nodes_jsonl():
            stream.write(json.dumps(nodes).decode('utf-8') + '\n')

    # stream out edges to edges.jsonl file
    with open('./output/edges.jsonl', 'w') as stream:
        for edges in disk_merger.get_merged_edges_jsonl():
            stream.write(json.dumps(edges).decode('utf-8') + '\n')

    # clear dir and data
    # clean_up_dir('./output')
    clean_up_dir('./tmp')