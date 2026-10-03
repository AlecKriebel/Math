"""SOURCE collector only: hash exact completed evidence in place; no Git calls."""
import json
import stat
from common import N, R, path, plain_ref, digest, encoded, need, now

P = R / 'draft_pr_publication_program_20260930'
A45 = P / 'audits/pr45_9900007'
fixed = {}
dirs = {}


def addfile(q):
    row = plain_ref(q)
    need(row['path'] not in fixed or fixed[row['path']] == row, 'Different duplicate file')
    fixed[row['path']] = row
    return row


def complete(q):
    need(q.is_dir() and not q.is_symlink(), 'Exact family directory')
    members = [q] + sorted(q.rglob('*'))
    files = []
    for v in members:
        need(not v.is_symlink(), 'No family symlinks')
        if v.is_dir():
            s = v.lstat()
            dirs[str(v.relative_to(R))] = dict(path=str(v.relative_to(R)), full_mode=stat.S_IMODE(s.st_mode))
        else:
            files.append(addfile(v))
    return files


def closed_family(relative, index_name, expected_sha, count, closer, reader):
    q = P / relative
    index = q / index_name
    need(digest(index.read_bytes()) == expected_sha, 'Exact genuine closed manifest')
    m = json.loads(index.read_bytes())
    rows = m.get('files', m.get('entries'))
    declared = set()
    for z in rows:
        name = z.get('path', z.get('name'))
        v = path(name) if name.startswith('/') is False and name.startswith('draft_pr_') else (q / name)
        if name.startswith('/'):
            v = __import__('pathlib').Path(name)
        need(v.is_relative_to(q), 'Declared source confined to its family')
        declared.add(v)
        if v == index:
            continue
        actual = plain_ref(v)
        need(actual['bytes'] == z['bytes'] and actual['sha256'] == z['sha256'], 'Closed family complete body')
        mode = z.get('mode', z.get('mode_07777'))
        if mode is not None:
            mode = int(mode, 8) if isinstance(mode, str) else mode
            need(actual['full_mode'] == mode, 'Closed family declared full mode')
    actual_files = complete(q)
    need({q / index_name} | declared == {R / z['path'] for z in actual_files}, 'Exact complete family topology')
    need(len(actual_files) == count and all(z['full_mode'] == 0o444 for z in actual_files), 'Exact frozen family count/mode')
    return dict(root=str(q.relative_to(R)), files=count, bytes=sum(z['bytes'] for z in actual_files),
                genuine_closed_index=plain_ref(index), ROOT_closer_pid=closer, ROOT_separate_reader_pid=reader,
                authority='Existing SOURCE custody only; no new mathematical acceptance')


def main():
    families = [
        closed_family('audits/pr55_30006309/current_preparation_family', 'MANIFEST.json', '37ec91934159bdedc383aa9f0908d79d65642788bf88ae155da9c94300daa4ff', 65, 77987, 78217),
        closed_family('audits/pr56_10300016/current_preparation_family', 'MANIFEST.json', '6dc02992edfec4db1eef09c40f88ba56525e776be80c85eb8037df45f7f951e9', 66, 23089, 23720),
        closed_family('audits/pr57_30003354/original_preparation_family', 'SELF_MANIFEST.json', '8d34ae0c031c53d422d2e130ce1b9ee3049fda5080e0e92bf7ab66fa63f504f1', 151, 13986, 14235),
        closed_family('audits/pr57_30003354/endpoint_analytic_adversary_family', 'SELF_MANIFEST.json', '5111c61093f062e541d73e82d2c9acf60196c8ffbb2eeae0d090bb9048cc57ee', 28, 16794, 16910),
        closed_family('audits/pr48_2961/post_push_foreign_epoch_adversary', 'SELF_MANIFEST.json', '5493fc07f4a9e8911f18c828b296e1eeb6357a24d59eb9b5ee5c0027030c5a4a', 20, 10695, 10940),
    ]
    a57 = P / 'audits/pr57_30003354'
    geo = a57 / 'geometric_topology_adversary_family'
    source = geo / 'SOURCE.json'
    need(digest(source.read_bytes()) == 'a1cf90b5a6a9f6dd29cb2314d411a6748e8a29d1096b4c4e4a6bcbb2ae5f5d3f', 'Exact geometry SOURCE')
    g = json.loads(source.read_bytes())
    declared = set()
    for z in g['files']:
        v = geo / z['relative_path']
        need(v.is_relative_to(geo), 'Geometry confined path')
        actual = plain_ref(v)
        need(actual['bytes'] == z['bytes'] and actual['sha256'] == z['sha256'] and actual['full_mode'] == int(z['full_mode_07777'], 8), 'Geometry whole body and mode')
        declared.add(v)
    geo_files = complete(geo)
    need(len(geo_files) == 70 and declared | {source} == {R / z['path'] for z in geo_files}, 'Geometry exact70 topology')
    external = []
    for name, sha in [('ROOT_GEOMETRIC_FAMILY_CLOSE.json', '03275370d55ffc22892d00320b711666812655cad992e584f846e913f4983004'), ('ROOT_GEOMETRIC_FAMILY_READBACK.json', 'eb83f3b0bc3a4cb1c9829d1b4e5762db476f7b29e070cb5877ac9d9d4b063326')]:
        z = addfile(a57 / name)
        need(z['sha256'] == sha and z['full_mode'] == 0o444, 'Exact outside ROOT geometry receipt')
        external.append(z)
    caps = []
    wanted = [77987,78217,23089,23720,13986,14235,16794,16910,16686,10695,10940,31666,32726,25978,26937,27063]
    candidates = {}
    for v in A45.glob('*/CAPTURE.json'):
        cap = json.loads(v.read_bytes())
        pid = cap.get('pid', cap.get('actual_pid'))
        if pid in wanted:
            need(pid not in candidates, 'Unique genuine ROOT capture PID')
            candidates[pid] = (v, cap)
    need(set(candidates) == set(wanted), 'All16 exact actual CAP sets found')
    for pid in wanted:
        v, cap = candidates[pid]
        need(cap['actual_execution'] and cap['completed'] and cap['exit_code'] == 0 and cap['operator_unchanged'], 'Actual completed ROOT CAP')
        members = complete(v.parent)
        need({__import__('pathlib').Path(z['path']).name for z in members} == {'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}, 'Exact CAP4 topology')
        need(digest((v.parent/'prelaunch_operator.py').read_bytes()) == cap['operator_sha256'], 'Actual prelaunch operator wholebody')
        for key in ['stdout','stderr']:
            body = (v.parent/(key+'.bin')).read_bytes()
            need(len(body) == cap[key]['bytes'] and digest(body) == cap[key]['sha256'], 'Whole complete retained ROOT stream')
        caps.append(dict(pid=pid, metadata=plain_ref(v), started_utc=cap['started_utc'], finished_utc=cap['finished_utc'],
                         exact_CAP4_root=str(v.parent.relative_to(R)), role='Previously executed ROOT source/storage operation, not approval of this checkpoint'))
    storage = P / 'storage_compression_20261003'
    frozen_storage = [addfile(storage / name) for name in ['PLAN.md','RESEARCH_LOG.md','V2PLAN.md','compress_completed.py','compress_completed_v2.py']]
    need(all(z['full_mode'] == 0o444 for z in frozen_storage), 'FrozenV1/V2 source full mode')
    operations = []
    for name, pid in [('pilot_h6k3r187',25978),('reconciled_0gay9tgy',26937),('pr47-stdout_79qnbj5l',27063)]:
        q = storage / name
        rows = complete(q)
        need({__import__('pathlib').Path(z['path']).name for z in rows} == {'ditto.stderr.bin','ditto.stdout.bin','helper.prelaunch.py','prelaunch.json','prepared.json','receipt.json'}, 'Exact lean operation6files, no index copies')
        receipt = json.loads((q/'receipt.json').read_bytes())
        need(receipt['status'] == 'COMPRESSED' and receipt['source_replaced'] is True and receipt['operator_pid'] == pid, 'Genuine successful storage receipt')
        need(digest((q/'helper.prelaunch.py').read_bytes()) == receipt['helper_sha256'] == frozen_storage[-1]['sha256'], 'Exact executed storageV2 source')
        before, after = receipt['before'], receipt['after']
        need(before['sha256'] == after['sha256'], 'Original logical body unchanged')
        for key in ['st_size','st_mode','st_uid','st_gid','st_mtime_ns']:
            need(before['stat'][key] == after['stat'][key], 'Original byte/mode/owner/time custody')
        need(before['acl_base64'] == after['acl_base64'], 'Original ACL unchanged')
        need(all(after['xattrs'].get(k) == val for k,val in before['xattrs'].items()), 'Original xattrs unchanged')
        operations.append(dict(actual_receipt=plain_ref(q/'receipt.json'), operator_pid=pid, saved_allocated_bytes=receipt['saved_allocated_bytes']))
    need(sum(z['saved_allocated_bytes'] for z in operations) == 78127104, 'Exact three operation savings')
    journals = [addfile(P/'audits/pr56_10300016/ROOT_CURRENT_RESEARCH_LOG_20261003.md'), addfile(a57/'ROOT_RESEARCH_LOG_20261003_1537.md')]
    own_files = [str(q.relative_to(R)) for q in sorted(N.rglob('*')) if q.is_file() and q.name not in ['RESEARCH_LOG.md','SOURCE_READY.json'] and '__pycache__' not in q.parts]
    # A currently running collector writes these three streams/metadata after
    # returning. This is only a literal future own path domain; READY later
    # requires every file to exist and hashes its actual completed bytes.
    for q in N.glob('source_*_actual_capture'):
        if q.is_dir():
            own_files.extend(str((q/name).relative_to(R)) for name in ['prelaunch_operator.py','prelaunch_common.py','stdout.bin','stderr.bin','CAPTURE.json'])
    own_files = sorted(set(own_files + [str((N/'SCOPE.json').relative_to(R)), str((N/'SOURCE_READY.json').relative_to(R))]))
    need(not any('private_primary_reading_cache' in p or p.startswith('unsolved_math_prioritization/') for p in fixed), 'No private publication cache or native bodies; archived original source paths remain allowed')
    scope = dict(schema='ROOT-exact-owned-research-checkpoint-scope/v1', prepared_utc=now(), source_only=True,
                 fixed_files=[fixed[k] for k in sorted(fixed)], fixed_directories=[dirs[k] for k in sorted(dirs)], closed_families=families,
                 externally_validated_geometry=dict(root=str(geo.relative_to(R)), files=70, source_index=plain_ref(source), SELF_MANIFEST_present=False, outside_ROOT_receipts=external, ROOT_closer_pid=31666, ROOT_reader_pid=32726,
                    ROOT_reading_qualification='ROOT read universal report, controls, source/custody and named hypotheses; did not personally inspect six images or every full published PDF.'),
                 actual_A45_CAP4_sets=caps, frozen_storage_V1_V2=frozen_storage, actual_storage_operations=operations, total_actual_storage_savings_bytes=78127104,
                 ROOT_current_journals_at_20261003T153806Z=journals,
                 runtime_stamped_log_paths=[str((N/'RESEARCH_LOG.md').relative_to(R))], new_preparation_source_paths=own_files,
                 forbidden_native_paths=['unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/catalog.json','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.json',str((P/'inventory.json').relative_to(R)),str((P/'review_state.json').relative_to(R)),str((P/'review_history.json').relative_to(R)),str((P/'RESEARCH_LOG.md').relative_to(R))],
                 exclusions=['PR58 unclosed original SOURCE','active PR47V2, PR57 priority and storageV3','private primary publication bodies/images/cache','large original temporary index bodies and pr47 raw stdout','native QUEUE/catalog/state/history/inventory','other chat bodies and logs','1215 checkpoint changes'],
                 dated_context=dict(formal_accepted_inventory='37/180', PR48='Genuine merge209581 and push completed; native bookkeeping pending', PR55='already_solved1/5; no paper', PR56='unsolved2/5; no paper', PR57='math PASS claimed_solved1/5; priority final adjudication pending; no paper/publication'),
                 new_math_or_priority_verdict=False, ROOT_review_of_this_SOURCE_not_claimed=True, stage_commit_push_executed=False)
    (N/'SCOPE.json').write_bytes(encoded(scope))
    print(encoded(dict(status='PREPARED_SOURCE_SCOPE_ONLY', selected_fixed_files=len(fixed), selected_fixed_directories=len(dirs), selected_bytes=sum(z['bytes'] for z in fixed.values()), SCOPE=plain_ref(N/'SCOPE.json'), no_git_calls=True)).decode(), end='')


if __name__ == '__main__':
    main()
