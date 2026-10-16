"""Independent bounded exact-source review04. No network or real provider calls.

Run with the existing bundled Python and -B. All mutation is confined here.
Fresh tests use a minimal retained legitimate synthetic case; they do not prove
real publication/merge actions or the mathematical theorem.
"""
from pathlib import Path
import copy, datetime, hashlib, importlib, json, subprocess, sys, zipfile

HERE = Path(__file__).resolve().parent
CASE = HERE.parent
RESULTS = []

def pin(path, base):
    raw = Path(path).read_bytes()
    return dict(path=Path(path).relative_to(base).as_posix(), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')

def result(label, fn):
    try:
        detail = fn()
    except BaseException as error:
        RESULTS.append(dict(label=label, outcome='FAIL', error_type=type(error).__name__, error=str(error)))
        write(HERE / 'RESULTS.json', RESULTS)
        raise
    RESULTS.append(dict(label=label, outcome='PASS', detail=detail))
    write(HERE / 'RESULTS.json', RESULTS)
    print(json.dumps(RESULTS[-1]), flush=True)

def rejected(fn):
    try:
        fn()
    except RuntimeError as error:
        return str(error)
    raise AssertionError('Expected semantic RuntimeError, but call accepted')

def imports():
    import urllib.request
    before = {p.relative_to(HERE).as_posix(): pin(p, HERE) for p in HERE.rglob('*') if p.is_file()}
    calls = []
    def trap(*args, **kwargs):
        calls.append(repr(args[:1]))
        raise AssertionError('Provider attempted during import')
    old_run, old_open = subprocess.run, urllib.request.urlopen
    subprocess.run, urllib.request.urlopen = trap, trap
    try:
        sys.path.insert(0, str(HERE))
        for name in ['release_binding', 'integrate_reviewed_pr', 'publish_preprint', 'append_verified_tracker', 'verify_published_readonly', 'verify_and_merge']:
            importlib.import_module(name)
    finally:
        subprocess.run, urllib.request.urlopen = old_run, old_open
    after = {p.relative_to(HERE).as_posix(): pin(p, HERE) for p in HERE.rglob('*') if p.is_file()}
    assert before == after and not calls
    return dict(all_six_imported=True, provider_calls=0, filesystem_changes=0)

def authenticate():
    frozen = json.loads((HERE / 'FROZEN_INPUTS.json').read_text())
    for e in frozen['rows']:
        assert pin(HERE / e['path'], HERE) == e
        assert pin(CASE / 'publication' / e['path'], CASE / 'publication') == e
    for e in frozen['scientific_files']:
        p = Path(e['path'])
        if not p.is_absolute(): p = CASE / p
        if not p.exists(): p = CASE / 'preprint' / e['path']
        raw = p.read_bytes()
        assert len(raw) == e.get('bytes', e.get('size')) and hashlib.sha256(raw).hexdigest() == e['sha256']
    import integrate_reviewed_pr as native
    source = native.frozen_source(CASE / 'preprint')
    intake = json.loads((CASE / 'initial_review_20261016/INTAKE.json').read_text())
    for e in intake['original_source_files']:
        n = e['native_path'][len(native.PREFIX):]
        raw = source['pr_update/5100015/history/original_submission_20261016/' + n]
        assert len(raw) == e['bytes'] and native.sha(raw) == e['sha256'] and native.blob(raw) == e['native_blob'] and e['native_mode'] == '100644'
    seals = []
    for folder in ['release_helpers_adversary_01', 'release_helpers_adversary_02', 'release_helpers_adversary_03', 'publication/native_repair_03']:
        r = CASE / folder
        manifest = json.loads((r / 'AUTHORED_MANIFEST.json').read_text())
        for e in manifest['files']:
            raw = (r / e['path']).read_bytes()
            assert len(raw) == e.get('bytes', e.get('size')) and hashlib.sha256(raw).hexdigest() == e['sha256']
        seals.append(dict(folder=folder, payloads=len(manifest['files']), manifest=pin(r/'AUTHORED_MANIFEST.json', CASE)))
    return dict(exact_current_six=True, scientific_files=230, source_zip_members=len(source), originals=23, authenticated_seals=seals)

def prepare_minimal():
    """Copy nonprivate tiny synthetic authority plus exact pin dependency closure."""
    archive = CASE / 'publication/native_repair_03/FIXTURES_receipt_01_recovered.zip'
    receipt = json.loads((CASE / 'publication/native_repair_03/FIXTURES_receipt_01_recovered.receipt.json').read_text())
    raw = archive.read_bytes()
    # The containing implementer seal has already authenticated this exact ZIP.
    assert hashlib.sha256(raw).hexdigest() == '9551745137e51fd7c7168967cafc88d354754e9dff2d8849438a3474848f6a9f'
    base = HERE / 'minimal_synthetic_case'
    assert not base.exists(), 'Use a fresh review capsule, never overwrite a previous run'
    base.mkdir()
    prefix = 'receipt_runs_01/joint_accepted/case/'
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        names = z.namelist()
        assert len(names) == len(set(names))
        authority = json.loads(z.read('receipt_runs_01/joint_accepted/LEGITIMATE_AUTHORITY.json'))
        selected = set()
        def take(relative):
            assert relative and not relative.startswith('/') and '..' not in Path(relative).parts
            member = prefix + relative
            assert member in names, relative
            if relative in selected: return
            body = z.read(member)
            target = base / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
            assert target.read_bytes() == body
            selected.add(relative)
            if relative.endswith('.json'):
                try: dependencies(json.loads(body))
                except (UnicodeError, json.JSONDecodeError): pass
        def dependencies(value):
            if type(value) is dict:
                if set(value) == {'path', 'bytes', 'sha256'} and prefix + str(value['path']) in names:
                    take(value['path'])
                for v in value.values(): dependencies(v)
            elif type(value) is list:
                for v in value: dependencies(v)
        for member in names:
            if member.startswith(prefix) and '/private_transport/' not in member:
                take(member[len(prefix):])
        dependencies(authority)
        p = authority['receipt']['live_release_evidence']['publication']
        q = authority['receipt']['live_release_evidence']['tracker']
        for folder, siblings in [
            (Path(p['inspect_readback']['path']).parent, ['LIVE_VERIFIED.json', 'DOWNLOAD_1.json', 'DOWNLOAD_2.json']),
            (Path(q['evidence']['properties']['path']).parent, ['LIVE_VERIFIED.json'])]:
            for sibling in siblings: take((folder / sibling).as_posix())
        # This fixed-path append intent is intentionally not a generic pin.
        take('publication/private_transport/tracker/APPEND_ATTEMPT.json')
        write(HERE / 'LEGITIMATE_AUTHORITY.json', authority)
        write(HERE / 'MINIMAL_FIXTURE_INPUTS.json', dict(synthetic_only=True, source_archive=pin(archive, CASE), source_members=len(names), retained_files=[pin(base/p, base) for p in sorted(selected)], omitted_native_provider_journals=True))
    return dict(selected_files=len(selected), selected_bytes=sum((base/p).stat().st_size for p in selected), original_archive_members=len(names), synthetic_only=True)

def validator_controls():
    import release_binding as rb
    import verify_and_merge as m
    case = HERE / 'minimal_synthetic_case'
    r, pub = case/'preprint', case/'publication'
    ctx = rb.context(r)
    z = rb.publication(r, pub, ctx)
    t = rb.tracker(r, pub, ctx, z)
    authority = json.loads((HERE/'LEGITIMATE_AUTHORITY.json').read_text())
    expected = authority['receipt']
    def validate(receipt=expected, fresh=expected):
        return m.validate_completion_receipt(receipt, fresh, r, pub, ctx, z, t, authority['release_utc'])
    validate()
    details = []
    def attack(label, change):
        bad = copy.deepcopy(expected)
        change(bad)
        error = rejected(lambda: validate(bad))
        details.append(dict(label=label, rejection=error))
    # All static fields are tested independently, including every nested pin list
    # as an exact JSON fact. No filesystem exception counts as a rejection.
    for key, value in expected.items():
        if key in {'utc', 'live_release_evidence'}: continue
        attack('missing_static_' + key, lambda d, k=key: d.pop(k))
        def substitute(d, k=key, v=value):
            d[k] = None if v is not None else 'changed'
        attack('substitute_static_' + key, substitute)
    attack('extra_static_key', lambda d: d.update(unreviewed_authority=True))
    attack('integer_bool_coercion', lambda d: d.update(case_completion_percent=True))
    attack('integer_float_coercion', lambda d: d.update(case_completion_percent=100.0))
    attack('nested_count_float_coercion', lambda d: d['program_counts'].__setitem__(0, 45.0))
    attack('nested_pin_size_float', lambda d: d['exact_native_body_readbacks'][0].__setitem__('bytes', float(d['exact_native_body_readbacks'][0]['bytes'])))
    for field in ['doi_url','tracker_range','case_completion_percent','actual_publication_tracker_native_merge_complete','exact_native_body_readbacks','merged']:
        values = {'doi_url':'https://doi.org/10.5281/zenodo.999999999','tracker_range':"'Wrong tab'!Z999:AC999",'case_completion_percent':1,'actual_publication_tracker_native_merge_complete':False,'exact_native_body_readbacks':[],'merged':False}
        attack('original03_' + field, lambda d, k=field: d.__setitem__(k, values[k]))
    attack('completion_before_release', lambda d: d.update(utc='2000-01-01T00:00:00+00:00'))
    attack('completion_future', lambda d: d.update(utc='2099-01-01T00:00:00+00:00'))
    attack('completion_non_UTC', lambda d: d.update(utc='2026-10-15T23:57:18-08:00'))
    attack('history_extra_top_key', lambda d: d['live_release_evidence'].update(unexpected=True))
    attack('history_missing_publication', lambda d: d['live_release_evidence'].pop('publication'))
    attack('history_pub_wrong_binding', lambda d: d['live_release_evidence']['publication']['release_binding'].__setitem__('clearance_sha256','0'*64))
    attack('history_tracker_wrong_receipt', lambda d: d['live_release_evidence']['tracker'].__setitem__('tracker_receipt_sha256','0'*64))
    attack('history_wrong_id_float', lambda d: d['live_release_evidence']['publication'].__setitem__('id',12345.0))
    attack('history_doi_fragment', lambda d: d['live_release_evidence']['publication']['doi_resolution'].__setitem__('resolved_url','https://zenodo.org/records/12345#wrong'))
    attack('history_inspect_path_traversal', lambda d: d['live_release_evidence']['publication']['inspect_readback'].__setitem__('path','publication/private_transport/zenodo_live/../INSPECT_READBACK.json'))
    attack('history_download_size_float', lambda d: d['live_release_evidence']['publication']['actual_public_file_downloads'][0].__setitem__('bytes',34.0))
    attack('history_download_false_flag', lambda d: d['live_release_evidence']['publication']['actual_public_file_downloads'][0].__setitem__('actual_public_download_byte_hash_match',False))
    attack('history_wrong_tracker_values', lambda d: d['live_release_evidence']['tracker']['values'].__setitem__(2,'https://doi.org/10.5281/zenodo.999999999'))
    attack('history_tracker_before_publication', lambda d: d['live_release_evidence']['tracker'].__setitem__('utc',authority['release_utc']))
    # Compare against a different fresh observation: historical dynamic values
    # remain valid and are not forced equal to freshly generated paths/times.
    fresh = copy.deepcopy(expected)
    fresh['utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    fresh['live_release_evidence'] = {'fresh_observation_only': 'not historical equality authority'}
    validate(expected, fresh)
    assert rb.context(r) == ctx
    write(HERE/'VALIDATOR_ATTACKS.json', details)
    return dict(legitimate_pass=True, attacks_rejected=len(details), fresh_expected_dynamic_values_not_forced_equal=True, direct_actual_validator=True, provider_calls=0)

def parser_controls():
    import verify_and_merge as m
    cases = ['{"x":1,"x":2}', '{"x":{"y":1,"y":2}}', '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}', '{"x":1e999}', b'\xff', '{broken']
    errors = [rejected(lambda x=x: m.strict_json(x)) for x in cases]
    assert m.strict_json('{"x":1,"s":"value","a":[true,null,1.25]}') == {'x':1,'s':'value','a':[True,None,1.25]}
    assert m.canonical_json(1) != m.canonical_json(True) != m.canonical_json(1.0)
    for value in [float('nan'),float('inf'),{1:'numeric-key'},(1,2)]:
        rejected(lambda v=value: m.canonical_json(v))
    return dict(strict_rejections=len(errors), non_JSON_rejections=4, positive_parse=True, errors=errors)

def actual_review_chains():
    import release_binding as rb
    whole=json.loads((CASE/'initial_review_20261016/ROOT_WHOLE_PACKAGE_ACCEPTANCE.json').read_text())
    assert rb.review_chain(CASE, whole['whole_package_reviews'], 'whole-package', rb.current_core(CASE/'preprint')) == (2,1)
    entries=[]
    for index in range(1,4):
        folder=CASE/('release_helpers_adversary_%02d'%index)
        entries.append(dict(assessment=pin(folder/'ASSESSMENT.json',CASE), authored_manifest=pin(folder/'AUTHORED_MANIFEST.json',CASE), source_freeze=pin(folder/'FROZEN_SOURCES.json',CASE), resolution=pin(CASE/('initial_review_20261016/ROOT_RELEASE_HELPER_REVIEW%02d_RESOLUTION.json'%index),CASE), supplements=[]))
    rows=json.loads((HERE/'FROZEN_INPUTS.json').read_text())['rows']
    folder=HERE/'SYNTHETIC_SUCCESSOR_PARSER_ONLY'
    folder.mkdir()
    stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    for e in rows: (folder/e['path']).write_bytes((HERE/e['path']).read_bytes())
    write(folder/'FROZEN_SOURCES.json',dict(frozen_utc=stamp,rows=rows,synthetic_only=True))
    (folder/'REPORT.md').write_text('SYNTHETIC PARSER SUCCESSOR ONLY: no scientific or release authority.\n')
    completed=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write(folder/'ASSESSMENT.json',dict(schema='pr209-release-helper-assessment-v1',reviewer='SYNTHETIC04_PARSER_ONLY',completed_utc=completed,verdict='PASS',frozen_sources=rows,mandatory_findings=[],optional_findings=[],synthetic_only=True))
    write(folder/'AUTHORED_MANIFEST.json',dict(files=[pin(p,folder) for p in sorted(folder.iterdir()) if p.is_file()]))
    entry=dict(assessment=pin(folder/'ASSESSMENT.json',CASE),authored_manifest=pin(folder/'AUTHORED_MANIFEST.json',CASE),source_freeze=pin(folder/'FROZEN_SOURCES.json',CASE),supplements=[])
    assert rb.review_chain(CASE,entries+[entry],'release-helper',rows)==(4,1)
    rejected(lambda: rb.review_chain(CASE,list(reversed(entries))+[entry],'release-helper',rows))
    rejected(lambda: rb.review_chain(CASE,entries+[entry,entry],'release-helper',rows))
    for index in range(3):
        bad=copy.deepcopy(entries+[entry]);bad[index].pop('resolution')
        rejected(lambda b=bad: rb.review_chain(CASE,b,'release-helper',rows))
    return dict(actual_whole_chain=[2,1],actual_prior_helper_seals_and_dispositions=3,synthetic_successor_parser_result=[4,1],synthetic_successor_not_authority=True,reordered_duplicate_or_missing_disposition_rejections=5)

def optimized():
    exits=[]
    for name in json.loads((HERE/'FROZEN_INPUTS.json').read_text())['rows']:
        run=subprocess.run([sys.executable,'-B','-O',str(HERE/name['path'])],capture_output=True)
        (HERE/(name['path']+'.optimized.stdout')).write_bytes(run.stdout)
        (HERE/(name['path']+'.optimized.stderr')).write_bytes(run.stderr)
        assert run.returncode==1 and b'RuntimeError' in run.stderr and not run.stdout
        exits.append(dict(source=name['path'],actual_exit=run.returncode))
    return exits

if __name__=='__main__':
    assert not (HERE/'RESULTS.json').exists(), 'Keep the original run immutable'
    result('six_inert_imports', imports)
    result('exact_sources_science_originals_and_prior_seals', authenticate)
    result('bounded_minimal_legitimate_synthetic_authority', prepare_minimal)
    result('actual_completion_validator_static_history_type_and_original03_attacks', validator_controls)
    result('actual_strict_JSON_parser', parser_controls)
    result('actual_review_chains_with_explicit_synthetic_successor', actual_review_chains)
    result('all_six_optimized_execution_rejected', optimized)
