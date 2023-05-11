import orjson
from itertools import islice


def quick_json_dumps(item):
    return str(orjson.dumps(item), encoding='utf-8')


def quick_json_loads(item):
    return orjson.loads(item)


def quick_jsonl_file_iterator(json_file):
    with open(json_file, 'r', encoding='utf-8') as stream:
        for line in stream:
            yield orjson.loads(line)

def chunk_iterator(iterable, chunk_size):
    iterator = iter(iterable)
    while True:
        chunk = list(islice(iterator, chunk_size))
        if chunk:
            yield chunk
        else:
            break