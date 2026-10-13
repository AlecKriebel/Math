#!/usr/bin/env python3
"""NEW Root-frozen compact MAIN builder proposal. No provider writes/ref commands."""
from pathlib import Path
import hashlib, os, stat, sys, types
sys.dont_write_bytecode = True
COMMON_SHA = 'fa1f5d4611e75a53848d56afccdfd1cd7582eaa912e1e882ffa9e5d92f1c5b5e'
helper = Path(__file__).absolute().parent / 'checkpoint_common.py'
for component in reversed([helper, *helper.parents]):
    if os.path.lexists(component):
        if stat.S_ISLNK(component.lstat().st_mode): raise RuntimeError('Source symlink rejected')
if os.path.lexists(helper.parent / '__pycache__'): raise RuntimeError('Source cache rejected')
common_body = helper.read_bytes()
if hashlib.sha256(common_body).hexdigest() != COMMON_SHA: raise RuntimeError('Exact helper pin differs')
common = types.ModuleType('sealed_checkpoint_common'); common.__file__ = str(helper)
exec(compile(common_body, str(helper), 'exec'), common.__dict__)
globals().update({k: v for k, v in common.__dict__.items() if not k.startswith('__')})

def rewrite_tree(reader, before_oid, selected, prefix=b'', rewritten=None):
    """Hash raw ancestors; retain EVERY untouched raw entry/mode, including links/submodules."""
    if rewritten is None: rewritten = []
    entries = dict(reader.tree(before_oid)) if before_oid is not None else {}
    immediate = {}
    for name, value in selected.items():
        part, separator, rest = name.partition(b'/')
        immediate.setdefault(part, []).append((separator, rest, value))
    for name, changes in immediate.items():
        direct = [value for separator, rest, value in changes if not separator]
        require(not direct or len(changes) == 1, 'Selected file/ancestor collision')
        if direct:
            require(name not in entries or entries[name][0] != b'40000', 'Directory replaced by selected leaf')
            entries[name] = direct[0][:2]
        else:
            require(name not in entries or entries[name][0] == b'40000', 'Existing leaf used as new directory')
            sub = {rest: value for separator, rest, value in changes}
            old = entries[name][1] if name in entries else None
            new = rewrite_tree(reader, old, sub, prefix + name + b'/', rewritten)
            entries[name] = b'40000', new
    body = tree_encode(entries); after_oid = oid('tree', body)
    if after_oid != before_oid:
        rewritten.append({'directory_b64': base64.b64encode(prefix.rstrip(b'/')).decode(),
            'before': before_oid, 'after': after_oid, 'raw_bytes': len(body), 'sha256': sha(body),
            'body_base64': base64.b64encode(body).decode()})
    return after_oid

class MemoryTrees:
    def __init__(self, raw_reader, changed):
        self.raw = raw_reader
        self.changed = {}
        for row in changed:
            body = base64.b64decode(row['body_base64'], validate=True)
            require(oid('tree', body) == row['after'] and len(body) == row['raw_bytes'] and sha(body) == row['sha256'],
                    'Constructed complete raw tree identity differs')
            require(row['after'] not in self.changed or self.changed[row['after']] == body,
                    'Repeated tree OID has different full raw bodies')
            self.changed[row['after']] = body
    def tree(self, ident):
        if ident not in self.changed: return self.raw.tree(ident)
        body = self.changed[ident]; result = {}; off = 0
        while off < len(body):
            space = body.index(b' ', off); zero = body.index(b'\0', space + 1)
            result[body[space + 1:zero]] = body[off:space], body[zero + 1:zero + 21].hex(); off = zero + 21
        require(tree_encode(result) == body, 'Constructed tree framing changed')
        return result
    def walk(self, ident, prefix=b''):
        rows = {}
        for name, value in self.tree(ident).items():
            path = prefix + name; rows[path] = value
            if value[0] == b'40000': rows.update(self.walk(value[1], path + b'/'))
        return rows

def main():
    selection, approval, bodies, inputs, certificate, context = freeze_gate('build', Path(__file__).absolute())
    current_commit,current_tree=certificate['current_commit'],certificate['current_tree']
    reader_context=certificate['reader_context']
    names = ['BEGIN.json', 'PROOF.json', 'TREE_PAYLOAD.json', 'COMMIT_PAYLOAD.json', 'COMMIT.raw',
             'TREE_OBJECTS.json', 'BLOB_PAYLOADS.json', 'CANDIDATE_FULL_ROWS.nul.gz',
             'SOURCE_INPUT_VALIDATION.json', 'STAGE_COMPLETED.json']
    stage = Stage(CHECKPOINT / 'private_candidate_v04', names)
    stage.json('BEGIN.json', {'UTC': utc(), 'source_only_private_build': True, 'provider_writes': 0,
               'primary_git_access': 0, 'all_future_outputs_reserved_before_any_Git_dispatch': names})
    config_pin = certificate['input_pins']['baseline_driver_config']
    require(Path(config_pin['path']) == Path(reader_context['driver']) / 'config', 'Baseline config not literal NI owned input')
    module, reader = owned_reader(selection, Path(reader_context['driver']), Path(reader_context['objects']), Path(reader_context['root']),
                                  config_sha=config_pin['sha256'])
    try:
        kind, raw_main = reader.get(current_commit)
        require(kind == 'commit' and raw_main == inputs['main_raw_commit'], 'Full baseline commit differs')
        root, parents, message = commit_header(raw_main)
        require(root == current_tree and parents == certificate['current_parents'], 'Baseline raw root/sole historical parent differs')
        before = reader.walk(current_tree)
        require(census(before) == gzip.decompress(inputs['main_full_rows']), 'Full baseline raw census differs')
        leaves = {p: v for p, v in before.items() if v[0] != b'40000'}
        directories = {p: v for p, v in before.items() if v[0] == b'40000'}
        require(len(leaves) == certificate['current_counts']['leaves'] and len(directories) == certificate['current_counts']['directories'], 'Full baseline counts differ')
        context = validate_baseline_context(selection, inputs, set(bodies), certificate)
        historical_module, historical_reader = owned_reader(selection, NI / 'reader.git', NI / 'private_objects', NI,
            config_sha=selection['inputs']['historical_driver_config']['sha256'])
        try:
            kind, adc_raw=historical_reader.get(ADC)
            require(kind=='commit' and adc_raw==inputs['adc_raw_commit'], 'Fixed ADC raw object differs')
            require(historical_reader.walk(ADC_TREE)==context['adc_rows'], 'Whole fixed ADC raw census differs')
            kind, historical_raw = historical_reader.get(ADC_PARENT)
            require(kind=='commit' and historical_raw==inputs['historical_parent_raw_commit'], 'Historical peer parent raw object differs')
            historical_root, _, _ = commit_header(historical_raw)
            require(historical_reader.walk(historical_root)==context['historical_rows'], 'Whole historical peer-parent raw census differs')
        finally: historical_reader.close()
        require(before==context['current_rows'], 'Current raw store does not match certified complete census')
        delta=context['protected_paths']
        changed = []; candidate_tree = rewrite_tree(reader, current_tree, bodies, rewritten=changed)
        after = MemoryTrees(reader, changed).walk(candidate_tree)
        distinct_raw_trees = validate_changed_tree_records(changed, before, after, candidate_tree, current_tree)
        allowed = set(bodies)
        require({p: v for p, v in after.items() if v[0] != b'40000' and p not in allowed} ==
                {p: v for p, v in leaves.items() if p not in allowed}, 'An unselected baseline leaf changed')
        rewritten_paths = {base64.b64decode(v['directory_b64']) for v in changed}
        require({p: v for p, v in after.items() if v[0] == b'40000' and p not in rewritten_paths} ==
                {p: v for p, v in directories.items() if p not in rewritten_paths}, 'Unrewritten directory changed')
        require(all(after.get(p) == before.get(p) for p in delta), 'A peer added/deleted/mode/OID path changed')
        foreign_current_entries_preserved(before,after,context['foreign_all_paths'],set(bodies))
        require(all(after[p] == value[:2] for p, value in bodies.items()), 'Selected mode/body identity differs')
        timestamp = str(selection['commit_unix_seconds']).encode()
        actor = b'Alec Kriebel <me@aleckriebel.com> ' + timestamp + b' +0000'
        raw_commit = b'tree ' + candidate_tree.encode() + b'\nparent ' + current_commit.encode() + b'\nauthor ' + actor + b'\ncommitter ' + actor + b'\n\n' + selection['commit_message'].encode()
        candidate_commit = oid('commit', raw_commit)
        blob_payloads = [{'path': name.decode(), 'oid': value[1],
                          'payload': {'content': base64.b64encode(value[2]).decode(), 'encoding': 'base64'}}
                         for name, value in bodies.items()]
        tree_payload = {'base_tree': current_tree, 'tree': [{'path': name.decode(), 'mode': value[0].decode(),
                        'type': 'blob', 'sha': value[1]} for name, value in bodies.items()]}
        commit_payload = {'tree': candidate_tree, 'parents': [current_commit], 'message': selection['commit_message'],
                          'author': dict(ACTOR, date=selection['commit_date_utc']),
                          'committer': dict(ACTOR, date=selection['commit_date_utc'])}
        proof = {'schema': 'pr262-new-main-findings-private-proof-v4', 'source_version':SOURCE_VERSION, 'UTC': utc(), 'baseline': current_commit,
                 'before_tree': current_tree, 'candidate_commit': candidate_commit, 'candidate_tree': candidate_tree,
                 'sole_parent': current_commit, 'selection_sha256': sha((FREEZE_ROOT / 'SELECTION.json').read_bytes()),
                 'selected_count': len(bodies), 'rewritten_ancestor_count': len(changed),
                 'distinct_rewritten_tree_object_count': len(distinct_raw_trees),
                 'baseline_leaf_count': len(leaves), 'baseline_directory_count': len(directories),
                 'candidate_leaf_count': sum(v[0] != b'40000' for v in after.values()),
                 'candidate_directory_count': sum(v[0] == b'40000' for v in after.values()),
                 'before_full_raw_census_sha256': sha(census(before)), 'after_full_raw_census_sha256': sha(census(after)),
                 'peer76_literal_paths_sha256': sha(dump(selection['peer_delta_literal_paths'])),
                 'peer76_all_unselected_modes_paths_oids_preserved': True,
                 'all_current_foreign_entries_preserved':True, 'all_protected_leaf_paths_preserved':True,
                 'baseline_certificate_sha256':selection['current_baseline_certificate_sha256'],
                 'baseline_counts':certificate_counts(certificate,context['protected_paths']),
                 'foreign_delta_literal_paths_sha256':sha(dump(selection['foreign_delta_literal_paths'])),
                 'foreign_delta_record_sha256':sha(inputs['foreign_delta']),
                 'all_unselected_main_leaves_preserved': True, 'all_unrewritten_main_directories_preserved': True,
                 'raw_commit_bytes': len(raw_commit), 'raw_commit_sha256': sha(raw_commit),
                 'tree_objects_sha256': sha(dump(changed)), 'blob_payloads_sha256': sha(dump(blob_payloads)),
                 'tree_payload_sha256': sha(dump(tree_payload)), 'commit_payload_sha256': sha(dump(commit_payload)),
                 'provider_mutations': 0, 'primary_git_access': 0, 'not_provider_authority': True}
        stage.write('COMMIT.raw', raw_commit); stage.json('TREE_OBJECTS.json', changed)
        stage.json('BLOB_PAYLOADS.json', blob_payloads); stage.json('TREE_PAYLOAD.json', tree_payload)
        stage.json('COMMIT_PAYLOAD.json', commit_payload)
        stage.write('CANDIDATE_FULL_ROWS.nul.gz', gzip.compress(census(after), mtime=0))
        stage.json('SOURCE_INPUT_VALIDATION.json', {'selection_sha256': proof['selection_sha256'],
                   'all_explicit_full_source_and_frozen_body_pins_verified': True,
                   'all_certified_current_entries_and_protected_paths_accounted_for': True,
                   'baseline_certificate_sha256':proof['baseline_certificate_sha256']})
        stage.json('PROOF.json', proof)
    finally:
        reader.close()
    stage.finish()
    print('Private candidate prepared. No provider objects or references changed.')

if __name__ == '__main__': main()
