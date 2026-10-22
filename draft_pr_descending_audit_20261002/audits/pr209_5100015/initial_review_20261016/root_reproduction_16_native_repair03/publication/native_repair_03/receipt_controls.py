"""Exact-source receipt repair controls. Providers and authority are synthetic.

One terminal workflow supplies legitimate authority. Six reported corruptions
exercise actual complete_merge. Other mutations directly exercise the actual
new validator without rewriting or replacing a candidate function.
"""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import contextlib, copy, io, json, traceback
import probes_joint_compact as C

H = C.H
HERE = Path(__file__).resolve().parent
H.L.b.RUNS = HERE / 'receipt_runs_01'
RESULTS = []


def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def check(label, call):
    started = datetime.now(timezone.utc).isoformat()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            detail = call()
        row = dict(label=label, PASS=True, detail=detail)
    except Exception as error:
        row = dict(label=label, PASS=False, error=repr(error), traceback=traceback.format_exc())
    row.update(start_utc=started, completed_utc=datetime.now(timezone.utc).isoformat())
    RESULTS.append(row)
    # Print the observed outcome before the optional metadata checkpoint.
    print(json.dumps(row, allow_nan=False), flush=True)
    dump(HERE / 'RESULTS_01.json', RESULTS)
    return row


def reject(call):
    try:
        call()
    except RuntimeError as error:
        return dict(type='RuntimeError', error=str(error))
    raise AssertionError('Expected explicit semantic RuntimeError')


def derive(f):
    rb = f.rb
    i, m = f.module('integrate_reviewed_pr.py'), f.module('verify_and_merge.py')
    ctx = rb.context(f.r)
    z, t = rb.publication(f.r, f.pub, ctx), rb.tracker(f.r, f.pub, ctx)
    api = i.NativeAPI(f.pub, 'receipt_repair_readonly', readonly=True)
    trees = i.NativeTrees(api)
    prep, built, packet, row = m.prepared_authority(f.r, f.pub, ctx, z, t, api, trees)
    progress = m.progress_baseline(f.r, f.pub, ctx, api, trees)
    intake = json.loads(i.safe_read(f.c, 'initial_review_20261016/INTAKE.json'))
    base = api('GET', 'git/commits/' + prep['main_parent'])
    args = m.load_merge(f.pub, ctx, built, packet, intake, z, progress, api, trees,
                       base, f.c.relative_to(f.root).as_posix() + '/')
    return m, ctx, z, t, prep['release_utc'], args, progress, api, trees


def main():
    with contextlib.redirect_stdout(io.StringIO()):
        f = C.terminal_fixture(True)
        m, ctx, z, t, release_utc, args, progress, api, trees = derive(f)
    path = f.pub / 'PR_MERGED.json'
    original_raw = path.read_bytes()
    original = json.loads(original_raw)
    fixed = len(f.mutations)
    dump(f.base / 'LEGITIMATE_AUTHORITY.json', dict(receipt=original, release_utc=release_utc,
        progress=progress, main_ref_intent_sha256=m.digest(f.pub / 'NATIVE_MERGE_REQUEST.json'),
        exact_source_inputs=H.FREEZE, synthetic_only=True))

    def validate(candidate):
        m.validate_completion_receipt(candidate, original, f.r, f.pub, ctx, z, t, release_utc)

    def baseline():
        validate(original)
        f.merge(True)
        assert path.read_bytes() == original_raw and len(f.mutations) == fixed
        fresh = sorted((f.pub / 'private_transport/zenodo_live').glob('*/LIVE_VERIFIED.json'))[-1]
        old_pin = original['live_release_evidence']['publication']['inspect_readback']['path']
        assert fresh.parent != (f.c / old_pin).parent
        assert json.loads(fresh.read_bytes())['utc'] != original['live_release_evidence']['publication']['utc']
        return dict(full_real_helper_workflow=True, fresh_paths_and_times_differ=True,
                    accepted_bytes_immutable=True, main_writes=H.main_writes(f))
    check('baseline_immutable_readonly_with_new_live_observations', baseline)

    for key, value in [('doi_url', 'https://doi.org/10.5281/zenodo.999999999'),
            ('tracker_range', "'Wrong tab'!Z999:AC999"), ('case_completion_percent', 1),
            ('actual_publication_tracker_native_merge_complete', False),
            ('exact_native_body_readbacks', []), ('merged', False)]:
        def full_corruption(key=key, value=value):
            changed = copy.deepcopy(original)
            changed[key] = value
            dump(path, changed)
            bad_raw = path.read_bytes()
            try:
                result = reject(lambda: m.complete_merge(f.r, f.pub, ctx, z, t, *args, progress, api, trees))
                assert path.read_bytes() == bad_raw and len(f.mutations) == fixed
                assert (f.pub / 'NATIVE_MERGE_REQUEST.json').read_bytes() == f.global_intent
                dump(f.base / ('REJECTED_' + key + '.json'), dict(changed_receipt=changed, result=result))
                return dict(result, unchanged_corrupt_bytes=True, no_provider_write=True, no_100_rewrite=True)
            finally:
                # Explicit synthetic artifact restoration; helpers never repair or overwrite it.
                path.write_bytes(original_raw)
        check('full_reported_' + key, full_corruption)

    for key, value in original.items():
        if key in {'utc', 'live_release_evidence'}:
            continue
        changed = copy.deepcopy(original)
        if type(value) is bool: changed[key] = not value
        elif type(value) is int: changed[key] = value + 1
        elif type(value) is str: changed[key] = value + 'SYNTHETIC_WRONG'
        elif type(value) is dict: changed[key] = {**value, 'SYNTHETIC_extra': True}
        elif type(value) is list: changed[key] = [] if value else [{'SYNTHETIC_wrong': True}]
        else: raise AssertionError('Uncovered static type')
        check('static_' + key, lambda changed=changed: reject(lambda: validate(changed)))

    for key in original:
        changed = copy.deepcopy(original)
        del changed[key]
        check('missing_' + key, lambda changed=changed: reject(lambda: validate(changed)))
    changed = {**original, 'SYNTHETIC_extra': True}
    check('unknown_top_level', lambda: reject(lambda: validate(changed)))

    coercions = [('PR', 209.0), ('merged', 1), ('case_completion_percent', 100.0),
        ('local_Git_index_ref_mutations', False), ('full_goal_active_incomplete', 1)]
    for key, value in coercions:
        changed = copy.deepcopy(original); changed[key] = value
        check('strict_type_' + key, lambda changed=changed: reject(lambda: validate(changed)))
    for label, mutate in [
        ('counts_boolean_zero', lambda x: x['program_counts'].__setitem__(3, False)),
        ('nested_pin_float', lambda x: x['exact_native_body_readbacks'][0].__setitem__('bytes', float(x['exact_native_body_readbacks'][0]['bytes']))),
        ('baseline_float', lambda x: x['progress_baseline']['previous_counts'].__setitem__(0, 44.0)),
        ('nested_nan', lambda x: x['progress_baseline'].__setitem__('bad', float('nan'))),
        ('nested_infinity', lambda x: x['progress_baseline'].__setitem__('bad', float('inf'))),
    ]:
        changed = copy.deepcopy(original); mutate(changed)
        check('strict_type_' + label, lambda changed=changed: reject(lambda: validate(changed)))

    def key_order():
        def reverse(x):
            if type(x) is dict: return {k: reverse(v) for k, v in reversed(list(x.items()))}
            if type(x) is list: return [reverse(v) for v in x]
            return x
        validate(reverse(original))
        return dict(object_key_order_irrelevant=True)
    check('valid_reordered_object_keys', key_order)

    for label, raw in [('duplicate', b'{"merged":true,"merged":false}'),
            ('duplicate_nested', b'{"x":{"n":1,"n":2}}'), ('NaN', b'{"n":NaN}'),
            ('Infinity', b'{"n":Infinity}'), ('minusInfinity', b'{"n":-Infinity}'),
            ('invalid_json', b'{'), ('invalid_utf8', b'"\xff"')]:
        check('strict_parser_' + label, lambda raw=raw: reject(lambda: m.strict_json(raw)))

    for label, value in [('invalid', 'bad'), ('nonUTC', '2026-01-01T00:00:00-01:00'),
            ('future', (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()),
            ('before_live', release_utc), ('boolean', True)]:
        changed = copy.deepcopy(original); changed['utc'] = value
        check('completion_utc_' + label, lambda changed=changed: reject(lambda: validate(changed)))

    # For semantic evidence tests, synchronize the retained LIVE_VERIFIED JSON
    # and update altered file pins in this synthetic sandbox. This tests actual
    # semantics rather than merely stopping at the outer retained-record check.
    def evidence_case(mutator, semantic=False):
        candidate = copy.deepcopy(original)
        saved = {}
        def write(p, raw):
            p = Path(p)
            saved.setdefault(p, p.read_bytes())
            p.write_bytes(raw)
        def update_pin(pin, mutate):
            p = f.c / pin['path']; obj = json.loads(p.read_bytes()); mutate(obj)
            write(p, (json.dumps(obj, indent=2) + '\n').encode())
            pin.update(bytes=p.stat().st_size, sha256=m.digest(p))
        try:
            mutator(candidate['live_release_evidence'], update_pin, write)
            if semantic:
                evidence = candidate['live_release_evidence']
                for kind, pin in [('publication', evidence['publication']['inspect_readback']),
                                  ('tracker', evidence['tracker']['evidence']['properties'])]:
                    live = (f.c / pin['path']).parent / 'LIVE_VERIFIED.json'
                    write(live, (json.dumps(evidence[kind], indent=2) + '\n').encode())
            return reject(lambda: validate(candidate))
        finally:
            for p, raw in saved.items(): p.write_bytes(raw)
            assert path.read_bytes() == original_raw and len(f.mutations) == fixed

    simple = [
        ('extra_root', lambda e,u,w: e.__setitem__('extra', True)),
        ('missing_tracker', lambda e,u,w: e.pop('tracker')),
        ('publication_extra', lambda e,u,w: e['publication'].__setitem__('extra', True)),
        ('publication_missing', lambda e,u,w: e['publication'].pop('doi_url')),
        ('tracker_extra', lambda e,u,w: e['tracker'].__setitem__('extra', True)),
        ('tracker_missing', lambda e,u,w: e['tracker'].pop('values')),
        ('publication_binding', lambda e,u,w: e['publication']['release_binding'].__setitem__('metadata_sha256','0'*64)),
        ('publication_receipt', lambda e,u,w: e['publication'].__setitem__('publication_receipt_sha256','0'*64)),
        ('tracker_receipt', lambda e,u,w: e['tracker'].__setitem__('tracker_receipt_sha256','0'*64)),
        ('provider_id_float', lambda e,u,w: e['publication'].__setitem__('id', float(z['id']))),
        ('doi', lambda e,u,w: e['publication'].__setitem__('doi_url','https://doi.org/10.5281/zenodo.999')),
        ('tracker_range', lambda e,u,w: e['tracker'].__setitem__('updated_range',"'Wrong tab'!A2:D2")),
        ('tracker_values', lambda e,u,w: e['tracker']['values'].__setitem__(0,'SYNTHETIC wrong problem')),
        ('pin_hash', lambda e,u,w: e['publication']['inspect_readback'].__setitem__('sha256','0'*64)),
        ('pin_bytes_bool', lambda e,u,w: e['publication']['inspect_readback'].__setitem__('bytes',True)),
        ('traversal', lambda e,u,w: e['publication']['inspect_readback'].__setitem__('path','../escape')),
        ('early_publication', lambda e,u,w: e['publication'].__setitem__('utc','2020-01-01T00:00:00+00:00')),
        ('future_tracker', lambda e,u,w: e['tracker'].__setitem__('utc',(datetime.now(timezone.utc)+timedelta(days=1)).isoformat())),
        ('reversed_observations', lambda e,u,w: e['publication'].__setitem__('utc', original['utc'])),
        ('retained_live_body', lambda e,u,w: w((f.c/e['publication']['inspect_readback']['path']).parent/'LIVE_VERIFIED.json',b'{}')),
    ]
    for label, mutate in simple:
        check('historical_' + label, lambda mutate=mutate: evidence_case(mutate))

    def provider(e, update, write, mutate): update(e['publication']['inspect_readback'], mutate)
    def tracker_file(e, update, key, mutate): update(e['tracker']['evidence'][key], mutate)
    semantic = [
        ('provider_title', lambda e,u,w: provider(e,u,w,lambda v:v.__setitem__('title','WRONG'))),
        ('provider_files_type', lambda e,u,w: provider(e,u,w,lambda v:v['files'][0].__setitem__('size',float(v['files'][0]['size'])))),
        ('provider_doi', lambda e,u,w: provider(e,u,w,lambda v:v.__setitem__('doi','10.5281/zenodo.999'))),
        ('provider_resolution', lambda e,u,w: provider(e,u,w,lambda v:v['doi_resolution'].__setitem__('http_status',500))),
        ('properties_grid', lambda e,u,w: tracker_file(e,u,'properties',lambda v:v['sheets'][0]['properties']['gridProperties'].__setitem__('rowCount',True))),
        ('properties_tab', lambda e,u,w: tracker_file(e,u,'properties',lambda v:v['sheets'][0]['properties'].__setitem__('title','Wrong tab'))),
        ('target_range', lambda e,u,w: tracker_file(e,u,'target_readback',lambda v:v['response'].__setitem__('range',"'Wrong tab'!A119:D119"))),
        ('target_body', lambda e,u,w: tracker_file(e,u,'target_readback',lambda v:v['response']['values'][0].__setitem__(1,'WRONG'))),
        ('target_schema', lambda e,u,w: tracker_file(e,u,'target_readback',lambda v:v.__setitem__('extra',True))),
        ('scan_coverage', lambda e,u,w: tracker_file(e,u,'after_scan',lambda v:v['response'].__setitem__('range',"'Math Puzzles'!A1:D1114"))),
        ('scan_unique', lambda e,u,w: tracker_file(e,u,'after_scan',lambda v:v['response']['values'].append(copy.deepcopy(t['values'])))),
        ('pins_schema', lambda e,u,w: e['tracker']['evidence'].__setitem__('extra',e['tracker']['evidence']['properties'])),
        ('download_schema', lambda e,u,w: e['publication']['actual_public_file_downloads'][0].__setitem__('extra',True)),
        ('download_bool_size', lambda e,u,w: e['publication']['actual_public_file_downloads'][0].__setitem__('bytes',True)),
        ('download_flag', lambda e,u,w: e['publication']['actual_public_file_downloads'][0].__setitem__('actual_public_download_byte_hash_match',1)),
        ('payload_bytes', lambda e,u,w: w(f.c/e['publication']['actual_public_file_downloads'][0]['payload']['path'],b'WRONG')),
    ]
    for label, mutate in semantic:
        check('historical_semantic_' + label, lambda mutate=mutate: evidence_case(mutate, True))

    # Retained late completion guards: exact source, same accepted terminal state.
    for kind in ['body', 'ref', 'event', 'main']:
        check('late_native_' + kind, lambda kind=kind: C.drift_case(f, kind, True))
    check('late_unknown_readonly_recovery', lambda: C.unknown_case(f, 'main', True))
    check('once_modes_remain_forbidden', lambda: C.write_modes_stay_forbidden(f, True))
    check('valid_foreign_descendant_immutable', lambda: C.valid_foreign_recovery(f, True))
    assert path.read_bytes() == original_raw and len(f.mutations) == fixed and H.main_writes(f) == 1
    f.trace()
    archive = H.archive_completed_group(HERE, H.L.b.RUNS, 'receipt_01')
    print(json.dumps(dict(fixture_archive=archive)), flush=True)
    summary = dict(utc=datetime.now(timezone.utc).isoformat(), controls=len(RESULTS),
        all_pass=all(x['PASS'] for x in RESULTS), exact_candidate_sources=True,
        fixture_archive=archive, case_completion_percent=65, release_authority=False)
    dump(HERE / 'SUMMARY_01.json', summary)
    print(json.dumps(summary), flush=True)
    return 0 if summary['all_pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
