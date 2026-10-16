#!/usr/bin/env python3
"""Exact recursive JSON types for an explicit frozen metadata allowlist only."""
import argparse
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re


class Rejected(ValueError):
    def __init__(self, kind, where, detail):
        super().__init__(detail); self.kind, self.where = kind, where


def require(value, kind, where, message):
    if not value: raise Rejected(kind, where, message)


def load(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate_key', str(path), 'Duplicate JSON key: '+key)
            result[key] = value
        return result
    def constant(value): raise Rejected('JSON', str(path), 'Non-JSON numeric constant: '+value)
    return json.loads(path.read_bytes(), object_pairs_hook=pairs, parse_constant=constant)


def canonical(value, where):
    path = PurePosixPath(value)
    require(value and '\\' not in value and path.as_posix() == value and not {'.','..'}.intersection(path.parts),
            'path', where, 'Canonical path required')


def validate(value, index, definitions, where='$'):
    node = definitions[index]
    types = {'object':dict, 'array':list, 'null':type(None), 'boolean':bool, 'integer':int, 'number':float, 'string':str}
    require(type(value) is types[node['type']], 'type', where, 'Expected '+node['type']+', got '+type(value).__name__)
    if node['type'] == 'object':
        require(set(value) == set(node['fields']), 'keys', where, 'Exact required keys/null fields required; missing='+str(sorted(set(node['fields'])-set(value)))+', extra='+str(sorted(set(value)-set(node['fields']))))
        for key, child in node['fields'].items(): validate(value[key], child, definitions, where+'/'+key)
        if node.get('path_row'): canonical(value['path'], where+'/path')
        if node.get('path_keys'):
            for key in value: canonical(key, where+'/'+key)
    elif node['type'] == 'array':
        require(len(value) == len(node['items']), 'shape', where, 'Exact list length/element shapes required')
        paths = []
        for position, child in enumerate(node['items']):
            validate(value[position], child, definitions, where+'/'+str(position))
            if definitions[child].get('path_row'): paths.append(value[position]['path'])
        require(len(paths) == len(set(paths)), 'duplicate_path', where, 'Unique canonical path rows required')
    else:
        if node.get('hex'): require(re.fullmatch('[0-9a-f]{'+str(node['hex'])+'}', value) is not None, 'hex', where, 'Lowercase exact-length hexadecimal identifier required')
        if node.get('nonempty'): require(bool(value.strip()), 'label', where, 'Nonempty label required')
        if node.get('nonnegative'): require(value >= 0 and (type(value) is int or math.isfinite(value)), 'count', where, 'Nonnegative finite size/byte/count required')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--schema', type=Path, required=True)
    parser.add_argument('--audit-root', type=Path, required=True)
    parser.add_argument('--single-entry')
    parser.add_argument('--single-file', type=Path)
    args = parser.parse_args(); schema = load(args.schema)
    entries = {row['path']:row for row in schema['entries']}
    current = None
    try:
        require(bool(args.single_entry) == bool(args.single_file), 'arguments', '$', 'Isolated control arguments must be paired')
        names = [args.single_entry] if args.single_entry else sorted(entries)
        for current in names:
            require(current in entries, 'allowlist', '$', 'Only approved named metadata may be parsed')
            row = entries[current]; path = args.single_file if args.single_entry else args.audit_root/current
            require(path.is_file() and not path.is_symlink(), 'file', current, 'Regular nonsymlink metadata required')
            value = load(path); validate(value, row['schema'], schema['definitions'])
            if 'exact_JSON' in row:
                actual = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',',':'))
                require(actual == row['exact_JSON'], 'content', current, 'Whole imported source/prior contents and types must remain exact')
            if not args.single_entry:
                raw = path.read_bytes()
                require(len(raw) == row['size'] and hashlib.sha256(raw).hexdigest() == row['sha256'], 'pin', current, 'Whole approved metadata bytes/SHA changed')
        print(json.dumps({'status':'ACCEPTED_TYPED_METADATA', 'entries':len(names), 'isolated_control':bool(args.single_entry)}, indent=2))
    except (Rejected, json.JSONDecodeError) as error:
        print(json.dumps({'status':'REJECTED_TYPED_METADATA','entry':current,'kind':getattr(error,'kind','JSON'),
                          'where':getattr(error,'where',str(args.single_file or args.audit_root)),'reason':str(error)}, indent=2))
        raise SystemExit(1)


if __name__ == '__main__': main()
