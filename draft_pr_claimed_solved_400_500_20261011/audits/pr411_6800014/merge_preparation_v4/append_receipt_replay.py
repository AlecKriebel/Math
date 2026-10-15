#!/usr/bin/env python3
"""Offline ADMIN receipt replay. Virtual assets/clock are explicit test doubles.

No native requests, asset bytes, scientific files, plans or mutations are run.
The authentic archived response bytes are copied before fault injection.
"""
import argparse
import ast
import base64
import copy
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import types

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BINDING = ('root_administration_inputs/ACTUAL_NATIVE_BINDINGS_integrate_20261013T0559.json', '468f5a3d06800773916954eb90220d59d81d6f7178bb3d7baec1c2591991e7dc')
STOP = ('root_administration_inputs/ROOT_MERGE_APPEND_ENCODER_STOP.json', '6c5296b63fa09b371164cd644c6f36777c23a016eaf8a8d35777e9a0817d8702')
V3 = 'ed85c2b6386ffa3750eba56f4450adf304b6040db37476dbce3e08ae997858de'
V4 = 'e4c9bd76594127b23cf6439df0b2c7a965f39b8f027d6debdb7cdf8e393aaa14'


def pretty(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class VirtualAsset:
    def __init__(self, size, sha, md5):
        self.size, self.sha, self.md5 = size, sha, md5
    def __len__(self):
        return self.size


class Fixture:
    def __init__(self, root, binding, originals):
        root.mkdir(parents=True, exist_ok=False)
        self.root, self.binding, self.docs = root, copy.deepcopy(binding), {}
        for section in ('publication', 'sheet'):
            for key, ref in list(self.binding[section].items()):
                if isinstance(ref, dict) and set(ref) == {'path', 'sha256'}:
                    name = section + '_' + key + '.json'
                    self.docs[name] = json.loads(originals[ref['path']])
                    self.binding[section][key] = {'path': name, 'sha256': ref['sha256']}
                    (root / name).write_bytes(originals[ref['path']])
    def doc(self, section, key):
        return self.docs[self.binding[section][key]['path']]
    def save(self, section, key):
        ref = self.binding[section][key]
        raw = pretty(self.docs[ref['path']])
        (self.root / ref['path']).write_bytes(raw)
        ref['sha256'] = hashlib.sha256(raw).hexdigest()
    def join(self, key):
        native = self.doc('sheet', key + '_native')
        native['stdout_base64'] = base64.b64encode(pretty(self.doc('sheet', key + '_response'))).decode()
        self.save('sheet', key + '_native')
        self.save('sheet', key + '_response')
    def append_hash(self, encoder=pretty):
        doc = self.doc('sheet', 'append_intent')
        doc['intent']['payload_sha256'] = hashlib.sha256(encoder(doc['payload'])).hexdigest()
        self.save('sheet', 'append_intent')
    def unicode_row(self):
        row = self.binding['sheet']['expected_row']
        row[3] = 'Synthetic administration note: café ∑; newline\nquoted "cell".'
        self.doc('sheet', 'batch_response')['valueRanges'][1]['values'] = [row]
        self.join('batch')
        self.doc('sheet', 'append_intent')['payload']['values'] = [row]
        self.append_hash()
        self.doc('sheet', 'append_response')['updates']['updatedData']['values'] = [row]
        self.join('append')


def run(candidate, fixture, approved, when):
    pub = fixture.binding['publication']
    public = fixture.doc('publication', 'legacy_public_response')
    native = fixture.doc('publication', 'public_native_response')
    byname = {x.get('key', x.get('filename')): x for x in public['files']}
    class OfflineAPI:
        def production_record(self, record_id, native=False):
            if record_id != 23331232:
                raise RuntimeError('unexpected record id')
            return fixture.doc('publication', 'public_native_response' if native else 'legacy_public_response')
        def production_asset(self, record_id, name, size):
            pin = next(x for x in approved['assets'] if x['name'] == name)
            checksum = byname[name]['checksum']
            if not checksum.startswith('md5:'):
                raise RuntimeError('expected actual MD5 metadata')
            return VirtualAsset(size, pin['sha256'], checksum[4:])
    real_digest, real_hashlib, real_dt = candidate.digest, candidate.hashlib, candidate.dt
    candidate.digest = lambda value: value.sha if isinstance(value, VirtualAsset) else real_digest(value)
    candidate.hashlib = types.SimpleNamespace(sha256=real_hashlib.sha256, md5=lambda value: types.SimpleNamespace(hexdigest=lambda: value.md5) if isinstance(value, VirtualAsset) else real_hashlib.md5(value))
    class Clock(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return when
    candidate.dt = types.SimpleNamespace(datetime=Clock, timezone=datetime.timezone, timedelta=datetime.timedelta)
    try:
        result = candidate.evidence(fixture.root, fixture.binding, approved, OfflineAPI())
        candidate.evidence_fresh(result)
        return True, 'ADMIN joins passed under explicit virtual asset hashes and archived-window clock'
    except candidate.Stop as exc:
        return False, str(exc)
    finally:
        candidate.digest, candidate.hashlib, candidate.dt = real_digest, real_hashlib, real_dt


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--case', type=Path, required=True)
    p.add_argument('--private-dir', type=Path, required=True)
    args = p.parse_args()
    args.private_dir.mkdir(parents=True, exist_ok=False)
    current = load(HERE / 'pr411_admin.py', 'v4')
    baseline_path = args.case / 'merge_preparation_v3/pr411_admin.py'
    for path, pin in ((HERE / 'pr411_admin.py', V4), (baseline_path, V3)):
        current.need(hashlib.sha256(path.read_bytes()).hexdigest() == pin, 'helper exact source pin differs')
    before, after = ast.parse(baseline_path.read_text()), ast.parse((HERE / 'pr411_admin.py').read_text())
    current.need(len(before.body) == len(after.body), 'top-level node set changed')
    changed = [getattr(a, 'name', '<nonfunction>') for a, b in zip(before.body, after.body) if ast.dump(a) != ast.dump(b)]
    current.need(changed == ['evidence'], 'unauthorized top-level source change')
    baseline = load(baseline_path, 'v3')
    binding_raw = current.read_local(args.case, *BINDING)
    binding = json.loads(binding_raw)
    stop_raw = current.read_local(args.case, *STOP)
    originals = {}
    for section in ('publication', 'sheet'):
        for ref in binding[section].values():
            if isinstance(ref, dict) and set(ref) == {'path', 'sha256'}:
                originals[ref['path']] = current.read_local(args.case, ref['path'], ref['sha256'])
    original_result = json.loads(originals[binding['publication']['result']['path']])
    approved = {'assets': [{'name': x['name'], 'bytes': x['size'], 'sha256': x['sha256']} for x in original_result['asset_hashes']]}
    times = [datetime.datetime.fromisoformat(json.loads(originals[binding['sheet'][key]['path']])['intent']['utc']) for key in ('metadata_intent', 'batch_intent')]
    when = max(times) + datetime.timedelta(seconds=1)
    results = []
    def check(tag, modify=None, expect=False, candidate=current, clock=when):
        f = Fixture(args.private_dir / tag, binding, originals)
        if modify:
            modify(f)
        passed, detail = run(candidate, f, approved, clock)
        results.append({'control': tag, 'expected_accept': expect, 'actual_accept': passed, 'detail': detail})
        current.need(passed is expect, 'unexpected control outcome: ' + tag + ': ' + detail)
    def edit(section, key, fn):
        def action(f):
            fn(f.doc(section, key))
            f.save(section, key)
        return action
    def payload_change(fn):
        def action(f):
            fn(f.doc('sheet', 'append_intent')['payload'])
            f.append_hash()
        return action
    def response_change(fn):
        def action(f):
            fn(f.doc('sheet', 'append_response'))
            f.join('append')
        return action
    check('authentic_archived_v3_expected_stop', expect=False, candidate=baseline)
    check('authentic_archived_v4_virtual_boundary', expect=True)
    check('synthetic_unicode_pretty_newline', Fixture.unicode_row, True)
    check('compact_payload_hash', lambda f: f.append_hash(current.encoded))
    check('pretty_missing_newline', lambda f: f.append_hash(lambda v: pretty(v)[:-1]))
    check('pretty_indent4', lambda f: f.append_hash(lambda v: (json.dumps(v,sort_keys=True,indent=4,ensure_ascii=False)+'\n').encode()))
    def ascii_unicode(f):
        f.unicode_row()
        f.append_hash(lambda v: (json.dumps(v,sort_keys=True,indent=2,ensure_ascii=True)+'\n').encode())
    check('unicode_ascii_escaped_hash', ascii_unicode)
    check('payload_extra_key', payload_change(lambda v: v.update(extra=True)))
    check('payload_missing_dimension', payload_change(lambda v: v.pop('majorDimension')))
    check('payload_wrong_dimension', payload_change(lambda v: v.update(majorDimension='COLUMNS')))
    check('payload_no_row', payload_change(lambda v: v.update(values=[])))
    check('payload_extra_row', payload_change(lambda v: v['values'].append(copy.deepcopy(v['values'][0]))))
    for index in range(4):
        check('payload_wrong_cell_' + str(index), payload_change(lambda v,i=index: v['values'][0].__setitem__(i,'changed')))
    check('payload_bool_cell', payload_change(lambda v: v['values'][0].__setitem__(3, True)))
    check('payload_numeric_cell', payload_change(lambda v: v['values'][0].__setitem__(3, 1)))
    check('payload_extra_cell', payload_change(lambda v: v['values'][0].append('extra')))
    check('append_wrong_intent_target', edit('sheet','append_intent',lambda v:v['intent']['params'].update(range="'Math Puzzles'!A77:D77")))
    check('append_wrong_native_target', edit('sheet','append_native',lambda v:v['params'].update(spreadsheetId='wrong')))
    check('append_bool_returncode', edit('sheet','append_native',lambda v:v.update(returncode=False)))
    check('append_raw_parsed_divergence', edit('sheet','append_response',lambda v:v['updates'].update(updatedCells=3)))
    check('append_wrong_row', response_change(lambda v:v['updates'].update(updatedRange="'Math Puzzles'!A78:D78")))
    check('append_wrong_spreadsheet', response_change(lambda v:v.update(spreadsheetId='wrong')))
    check('append_bool_updatedrows', response_change(lambda v:v['updates'].update(updatedRows=True)))
    check('append_bad_counts', response_change(lambda v:v['updates'].update(updatedCells=3)))
    check('wrong_result_doi', edit('publication','result',lambda v:v.update(doi='10.5281/zenodo.23331231')))
    check('wrong_result_status', edit('publication','result',lambda v:v.update(status='published_verified')))
    check('stale_archived_virtual_clock', clock=when+datetime.timedelta(seconds=301))
    check('future_archived_virtual_clock', clock=min(times)-datetime.timedelta(seconds=1))
    def corrupt(f):
        ref=f.binding['sheet']['append_intent']
        (f.root/ref['path']).write_bytes(b'{}\n')
    check('receipt_hash_corruption', corrupt)
    output={'result':'PASS_OFFLINE_ADMIN_APPEND_REPLAY','controls':len(results),'results':results,'source_sha256':V4,'baseline_source_sha256':V3,'changed_top_level_nodes':changed,'unchanged_other_top_level_nodes':len(before.body)-1,'actual_binding_sha256':BINDING[1],'actual_stopped_plan_proof_sha256':STOP[1],'archived_virtual_clock':when.isoformat(),'scientific_files_or_asset_bytes_opened':0,'native_requests':0,'native_mutations':0,'boundary':'Authentic archived ADMIN JSON and private copied fault fixtures only. All three asset byte checks use explicitly pinned virtual hashes/length/MD5; clock is explicitly fixed inside original GET window. This is not fresh native verification or production phase success.'}
    (args.private_dir/'RESULT.json').write_bytes(pretty(output))
    print(json.dumps(output,sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
