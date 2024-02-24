import io
import csv
import sys
import typing

def stream_to_iterable(stream, chunk_size = 1024):
    content = b''
    chunk_size = 1024

    while True:
        chunk = stream.read(chunk_size)
        content += chunk
        if len(chunk) == 0:
            break

    return io.StringIO(content.decode())

def is_csv_valid(f: typing.Iterable[str], header: list[str]):
    current_position = f.tell()
    first_line = f.readline()
    f.seek(current_position)
    _header = first_line.strip().split(',')
    print(header, file=sys.stderr)
    print(_header, file=sys.stderr)
    return _header == header

def parse_csv(f: typing.Iterable[str]):
    reader = csv.DictReader(f, delimiter=",")
    return list(reader)
