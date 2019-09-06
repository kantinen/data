#!/usr/bin/env python3

import codecs
from collections import namedtuple
import csv
import os.path
import sys
import time
import yaml

def parse_amount(text):
    return int(text.replace(',', '').replace('.',''))

def parse_dt(date_text, time_text):
    text = date_text + ' ' + time_text
    return time.strptime(text, '%d-%m-%Y %H:%M')

Entry = namedtuple('Entry', ['kind', 'amount', 'dt', 'msg', 'fee'])

def read_entry(row):
    kind = row[0]
    amount = parse_amount(row[1])
    dt = parse_dt(row[2], row[3])
    msg = row[4]
    if kind == 'Gebyr':
        assert row[5] == ''
        fee = None
    elif row[5] == 'Afventer':
        fee = None
    else:
        fee = parse_amount(row[5])
    return Entry(kind, amount, dt, msg, fee)

def read_entries(entries_path):
    data = []
    with codecs.open(entries_path, 'r', 'utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader) # skip header
        for row in reader:
            data.append(read_entry(row))
    return data

def read_ruleset(ruleset_path):
    with open(ruleset_path) as f:
        return yaml.load(f,  Loader=yaml.FullLoader)

def get_dt(dt_str):
    return time.strptime(dt_str, '%d.%m.%Y %H:%M')

def make_dt(dt):
    return time.strftime('%d.%m.%Y %H:%M', dt)

eval_context = {
    'getDT': get_dt
}

def categorise_entry(ruleset, entry):
    entry_dict = entry._asdict()
    for category in ruleset:
        for rule in category['rules']:
            if eval(rule['python'], eval_context, entry_dict):
                entry_dict['category'] = category['category']
                return entry_dict

def categorise(ruleset, entries):
    return [
        categorise_entry(ruleset, entry)
        for entry in entries
    ]

def basename(path):
    return os.path.splitext(os.path.basename(path))[0]

def writecs(path, fieldnames, entries):
    with open(path, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for e in entries:
            e['dt'] = make_dt(e['dt'])
            writer.writerow(e)

def writers(path, results):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Konto', 'Opgør'])
        for r in results:
            writer.writerow(r)

def main():
    ruleset_path = sys.argv[1]
    entries_path = sys.argv[2]
    basepath = basename(entries_path)
    cpath = basepath + "c.csv"
    rpath = basepath + "r.csv"

    ruleset = read_ruleset(ruleset_path)
    entries = read_entries(entries_path)

    entries = categorise(ruleset, entries)
    fieldnames = list(entries[0].keys())
    writecs(cpath, fieldnames, entries)

    sums = {category['category']: sum(entry['amount'] for entry in entries
                                      if entry['category'] == category['category'])
            for category in ruleset}
    writers(rpath, sorted(sums.items()))

if __name__ == "__main__":
    main()
