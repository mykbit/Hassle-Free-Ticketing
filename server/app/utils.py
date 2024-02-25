import io
import csv
import sys
import typing
import datetime
from .models import get_latest

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

def filter_payments(statements):
    lastest = get_latest()
    toReturn = []
    if lastest:
        lastest = lastest[0]
    else:
        lastest = datetime.datetime(1,1,1,0,0,0)

    for transfer in statements:
        if transfer['Type'] == 'TRANSFER' and transfer['Product'] == 'Current' and ('From ' in transfer['Description'])and not ('-' in transfer['Amount']):
            transferTime = datetime.datetime.strptime(transfer['Completed Date'], '%Y-%m-%d %H:%M:%S')
            if transferTime >= lastest:
                toReturn.append({'timestamp':transfer['Completed Date'],'Description':transfer['Description'], 'Amount':transfer['Amount']})
    
    return toReturn