#!/usr/bin/env python3
"""Inert PR108 input builder. No native preparation, assess, gates or services.

Run with a reviewed Python using env -i and -E -S -B. The only subprocesses
are local read-only Git commands. Output stays in this preparation folder.
The main parent and sealed helper directory are mandatory explicit arguments.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import argparse, datetime, hashlib, importlib.util, json, os, re, shutil, stat, subprocess

HERE = Path(__file__).absolute().parent
A = HERE.parent
C = A.parents[2]
R = Path('/Users/alec/Documents/Math')
P = 'unsolved_math_prioritization/'
N = P + 'attempts/30003996/'
ORIGINAL = A / 'original_source_authentication_20261006'
BASE_NAMES = ['queue.py', 'manifest.json', 'policy.json', 'catalog.json', 'assessments.json', 'state.json',
              'history.jsonl', 'assessment_history.jsonl', 'ranking.csv', 'summary.json', 'SHORTLIST.md', 'QUEUE.md']
PACKAGE_SHA = '61f08bd60185b6ef2382fb279fe77d59958974c07c4a44976cc7289eafca8c38'
DOI = '10.5281/zenodo.23181280'
ORIGINAL_HEAD = '3526d46bf143b08e5055ffa7728c6278e9f958ea'
JOURNAL = []
READS = {}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def canonical(obj):
    return (json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def regular(path):
    require(path.is_absolute(), 'Absolute path required')
    require(not any(p.is_symlink() for p in [*path.parents, path]), 'Nonruntime symlink input')
    info = path.stat()
    require(stat.S_ISREG(info.st_mode), 'Nonregular input')
    return info

def metadata_pin(path, private=False):
    """Stream into a digest only. Private configuration bodies are never retained."""
    info = regular(path)
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    after = regular(path)
    require((info.st_size, info.st_mtime_ns) == (after.st_size, after.st_mtime_ns), 'Input changed while hashing')
    pin = {'path': str(path), 'bytes': info.st_size, 'sha256': h.hexdigest()}
    READS[str(path)] = {**pin, 'body_retained': False, 'private_metadata_only': private,
                       'mode': oct(stat.S_IMODE(info.st_mode))}
    return pin

def local_pin(path):
    pin = metadata_pin(path)
    require(path.is_relative_to(A), 'Nongate input outside target audit')
    return {**pin, 'path': str(path.relative_to(C))}

def body(path, expected=None):
    info = regular(path)
    require(info.st_size <= 8 * 1024 * 1024, 'Audit body cap')
    data = path.read_bytes()
    pin = {'path': str(path.relative_to(C)), 'bytes': len(data), 'sha256': sha(data)}
    if expected is not None:
        require(pin == expected, 'Existing receipt pin changed: ' + str(path))
    READS[str(path)] = {**pin, 'body_retained': False, 'parsed_privately': True}
    return data

def json_body(path, expected=None):
    return json.loads(body(path, expected))

def command(argv, env, cap=32 * 1024 * 1024):
    """Bounded local Git read; keep full-stream hashes and 4096-byte prefixes only."""
    require(Path(argv[0]).name == 'git', 'Only local read-only Git subprocesses')
    require(argv[1] in ['show', 'rev-parse', 'symbolic-ref', 'ls-tree'], 'Disallowed Git operation')
    began = now()
    proc = subprocess.Popen(argv, cwd=C, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        out, err = proc.communicate(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill(); proc.communicate(); raise ValueError('Read-only Git deadline') from None
    require(len(out) <= cap and len(err) <= 65536, 'Read-only Git output cap')
    JOURNAL.append({'argv': argv, 'cwd': str(C), 'PID': proc.pid, 'UTC_start': began, 'UTC_end': now(),
                    'exit_code': proc.returncode, 'environment': env, 'ambient_inherited': False,
                    'stdout_bytes': len(out), 'stdout_sha256': sha(out), 'stderr_bytes': len(err), 'stderr_sha256': sha(err),
                    'stdout_prefix_hex': out[:4096].hex(), 'stderr_prefix_hex': err[:4096].hex()})
    require(proc.returncode == 0, 'Read-only Git failed')
    return out

def private_configuration(common):
    """Discover only location bodies; hash configuration/auth files without inspection."""
    locations = []
    dotgit = C / '.git'
    if dotgit.is_dir():
        require(not dotgit.is_symlink(), 'Git directory symlink')
        gitdir = dotgit
    else:
        data = dotgit.read_bytes()
        require(len(data) <= 4096 and data.startswith(b'gitdir: '), 'Git directory pointer')
        pointer = Path(data[8:].decode().strip())
        gitdir = (pointer if pointer.is_absolute() else C / pointer).resolve()
        locations.append(metadata_pin(dotgit, private=True))
    pointer_path = gitdir / 'commondir'
    if pointer_path.exists():
        data = pointer_path.read_bytes()
        require(len(data) <= 4096, 'Git common-directory pointer cap')
        pointer = Path(data.decode().strip())
        commondir = (pointer if pointer.is_absolute() else gitdir / pointer).resolve()
        locations.append(metadata_pin(pointer_path, private=True))
    else:
        commondir = gitdir
    configs = [metadata_pin(commondir / 'config', private=True)]
    if (gitdir / 'config.worktree').exists():
        configs.append(metadata_pin(gitdir / 'config.worktree', private=True))
    ghdir = Path('/Users/alec/.config/gh')
    ghfiles = sorted(p for p in ghdir.iterdir() if p.is_file())
    require({p.name for p in ghfiles} == {'config.yml', 'hosts.yml'}, 'Existing GH config inventory changed')
    ghpins = [metadata_pin(p, private=True) for p in ghfiles]
    require({p['path']: p['bytes'] for p in ghpins} == {str(ghdir / 'config.yml'): 824, str(ghdir / 'hosts.yml'): 204}, 'Known GH configuration sizes changed')
    require(all(stat.S_IMODE(regular(Path(p['path'])).st_mode) == 0o600 for p in ghpins), 'Private GH file mode')
    return gitdir, commondir, locations, configs, ghdir, ghpins

def build(args):
    require(re.fullmatch('[0-9a-f]{40}', args.main_parent), 'Explicit complete main parent')
    D = args.helper_dir.absolute()
    require(D.parent == A / 'native_publication_integration_plan_20261006' and D.name == 'corrected_v5', 'Corrected V5 helper only')
    require((D / 'SEAL_RECEIPT.json').is_file() and (D / 'CORE_FAMILY_MANIFEST.json').is_file(), 'Await sealed corrected V5 contract')
    # Import only the pure guard module; prepare and worker entry points are never imported or called.
    spec = importlib.util.spec_from_file_location('pr108_reviewed_input_guards', D / 'v3_guards.py')
    g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
    require(sys.flags.ignore_environment and sys.flags.no_site and sys.flags.dont_write_bytecode, 'Builder requires -E -S -B')
    require(dict(os.environ) == g.COMMON_ENV, 'Builder requires exact clean startup environment')
    family = json_body(D / 'CORE_FAMILY_MANIFEST.json')
    program_files = [local_pin(D / name) for name in g.PROGRAMS]
    require({Path(p['path']).name: {k: p[k] for k in ['bytes', 'sha256']} for p in program_files} == family['program_files'], 'Sealed helper family differs')
    helper_context_pins = [local_pin(D / n) for n in ['CORE_FAMILY_MANIFEST.json', 'SEAL_RECEIPT.json', 'PLAN.md', 'CONFIG_TEMPLATE_DO_NOT_RUN.json', 'EXECUTION_INPUTS_TEMPLATE_DO_NOT_RUN.json', 'AFFECTED_PATH_RULES.json']]
    template = json_body(D / 'EXECUTION_INPUTS_TEMPLATE_DO_NOT_RUN.json')
    effective = template['effective']
    require(set(effective) == g.CHOICES, 'Sealed helper effective contract differs')
    git_executable = Path('/opt/homebrew/bin/git').resolve()
    gh_executable = Path('/opt/homebrew/bin/gh').resolve()
    python_executable = Path('/opt/homebrew/bin/python3').resolve()
    require(Path(sys.executable).resolve() == python_executable, 'Actual builder Python runtime differs')
    runtime = {'python_executable': str(python_executable), 'python_version': sys.version,
               'git_executable': str(git_executable), 'gh_executable': str(gh_executable)}
    for role in ['python', 'git', 'gh']:
        runtime[role + '_binary'] = {k: v for k, v in metadata_pin(Path(runtime[role + '_executable'])).items() if k != 'path'}
    shell_pin = metadata_pin(Path('/bin/sh'))
    gitdir, commondir, locations, configs, ghdir, ghpins = private_configuration(g.COMMON_ENV)
    environment = {'schema': 'pr108-reviewed-process-environment/v3', 'ambient_inheritance': False,
                   'credentials_in_environment_or_receipts': False,
                   'python': {'argv_prefix': g.PYTHON_PREFIX, 'environment': g.COMMON_ENV},
                   'initial_launcher': {'program': 'launch_review_bundle.sh', 'shell': '/bin/sh', 'environment': g.COMMON_ENV},
                   'git': {'environment': g.GIT_ENV, 'repository_directory': str(C), 'repository_location_pins': locations, 'repository_config_pins': configs},
                   'gh': {'environment': {**g.GH_ENV_FIXED, 'GH_CONFIG_DIR': str(ghdir)}, 'config_pins': ghpins, 'expected_login': 'AlecKriebel'}}
    g.validate_environment_policy(environment)
    require(command([str(git_executable), 'rev-parse', 'HEAD'], g.GIT_ENV, 4096).decode().strip() == args.main_parent, 'Explicit main parent stale')
    require(command([str(git_executable), 'symbolic-ref', '--short', 'HEAD'], g.GIT_ENV, 4096).strip() == b'main', 'Only main permitted')
    require(not command([str(git_executable), 'ls-tree', '-r', '--name-only', args.main_parent, '--', N], g.GIT_ENV, 4096), 'Native target already materialized in main')
    require(not (C / N).exists(), 'Materialized native attempt already exists')
    baseline, native_pins = {}, []
    for name in BASE_NAMES:
        data = command([str(git_executable), 'show', args.main_parent + ':' + P + name], g.GIT_ENV)
        pin = {'path': P + name, 'bytes': len(data), 'sha256': sha(data)}
        local = C / P / name
        require(not local.is_symlink(), 'Native materialized baseline symlink')
        if local.exists():
            require({k: v for k, v in metadata_pin(local).items() if k != 'path'} == {k: pin[k] for k in ['bytes', 'sha256']}, 'Native materialized baseline differs: ' + name)
        else:
            READS[str(local)] = {'path': str(local), 'materialized': False, 'baseline_authenticated_by_explicit_main_blob': pin}
        native_pins.append(pin); baseline[name] = data
    oldass = json.loads(baseline['assessments.json'])['30003996']
    target = next(row for row in json.loads(baseline['catalog.json']) if row['id'] == '30003996')
    require(target['local_status'] == 'queued' and target['turns_used'] == 0 and '30003996' not in json.loads(baseline['state.json']), 'Native target baseline requires reconciliation')
    require(oldass.get('review_hash') == '9a2816afbdd3750d36f550dc6e91c7201aa024344a7b83fdb420aafe6c86df0d' and oldass.get('review_policy') == '2.0-five-turn-proof', 'Target desk assessment source/policy')
    registry, usage = {}, {}
    def add(pin, consumer):
        g.pin_shape(pin)
        path = C / pin['path']
        require(path.is_relative_to(A) and pin['bytes'] <= 8 * 1024 * 1024, 'Registry scope/cap')
        actual = local_pin(path)
        require(actual == pin, 'Referenced receipt pin mismatch')
        require(pin['path'] not in registry or registry[pin['path']] == pin, 'Conflicting same-path pin')
        registry[pin['path']] = pin
        usage.setdefault(pin['path'], set()).add(consumer)
        return pin
    def add_path(path, consumer):
        return add(local_pin(path), consumer)
    auth = {role: add_path(ORIGINAL / name, 'prepare:original_authentication:' + role) for role, name in [
        ('blob_manifest', 'ORIGINAL_BLOB_MANIFEST.json'), ('queue_projection', 'QUEUE_STATUS_PROJECTION.json'),
        ('sourcepair', 'SOURCEPAIR_AUTHENTICATION.json'), ('selected_prior', 'SELECTED_IMPORTED_PRIOR_REPORT.json')]}
    blob = json_body(C / auth['blob_manifest']['path'], auth['blob_manifest'])
    require(blob['source_head'] == ORIGINAL_HEAD and blob['literal_status'] == 'claimed_solved' and blob['original_author_effort'] == '2/5', 'Original identity')
    auth['original_files'] = []
    for item in sorted(blob['files'], key=lambda x: x['relative_path']):
        path = ORIGINAL / 'original_attempt' / g.relative(item['relative_path'])
        pin = {'path': str(path.relative_to(C)), 'bytes': item['bytes'], 'sha256': item['sha256']}
        auth['original_files'].append(add(pin, 'prepare:original_file'))
    require({str((C / p['path']).relative_to(ORIGINAL / 'original_attempt')) for p in auth['original_files']} == g.ORIGINAL_NAMES, 'Original fifteen names')
    diagnostics = [add_path(p, 'prepare:effective_diagnostics') for p in sorted((A / 'repaired_diagnostics_v1').rglob('*')) if p.is_file()]
    require(len(diagnostics) == 10, 'Effective diagnostic inventory changed')
    package_root = A / 'publication_ready_package_v2'
    package_pin = add_path(package_root / 'PACKAGE_MANIFEST.json', 'prepare:package_manifest')
    require(package_pin['sha256'] == PACKAGE_SHA, 'Frozen package manifest changed')
    package = json_body(C / package_pin['path'], package_pin)
    package_files = {}
    for item in package['files']:
        path = package_root / g.relative(item['relative_path'])
        pin = {'path': str(path.relative_to(C)), 'bytes': item['bytes'], 'sha256': item['sha256']}
        add(pin, 'prepare:logical_package_file')
        package_files[item['relative_path']] = body(path, pin)
    require(len(package_files) == 46, 'Frozen package logical inventory')
    pub_pin = add_path(A / 'ROOT_ACTUAL_PUBLICATION_RECEIPT_20261006.json', 'prepare:actual_publication_receipt')
    publication = json_body(C / pub_pin['path'], pub_pin)
    require(publication['DOI'] == DOI and publication['package_manifest_sha256'] == PACKAGE_SHA, 'Actual publication binding')
    add(publication['metadata_response'], 'publication_check:metadata')
    for item in publication['payload_readbacks']:
        add(item['downloaded_file'], 'publication_check:logical_payload')
        add(item['HTTP_GET_receipt'], 'publication_check:HTTP_custody')
        if item['transport'] == 'zip_member':
            add(item['archive_file'], 'publication_check:archive')
    sheet_pin = add_path(A / 'ROOT_ACTUAL_GOOGLE_SHEET_SERVICE_RECEIPT_20261006.json', 'prepare:actual_Sheet_receipt')
    sheet = json_body(C / sheet_pin['path'], sheet_pin)
    require(sheet['schema'] == 'pr108-actual-gws-sheet-service-receipt/v2' and sheet['DOI'] == DOI and sheet['row_index'] == 31 and sheet['range'] == "'Math Puzzles'!A31:D31" and sheet['values'][1] == '', 'Actual target Sheet binding')
    for role, record in sheet['processes'].items():
        for field in ['stdout_pin', 'stderr_pin']:
            add(record[field], 'validate_sheet:' + role + ':' + field)
        if role == 'write':
            add(record['request_body_pin'], 'validate_sheet:append_body')
    # Existing evidence selected for proposed future gates. These are not new gates.
    selected = {
        'mathematics': ['ROOT_MATHEMATICAL_GATE_20261006.json', 'ROOT_MATH_FAMILY_AUTHENTICATION_20261006.json'],
        'priority': ['ROOT_PRIORITY_GATE_20261006.json', 'ROOT_PRIORITY_ADJUDICATION_20261006.md', 'ROOT_CLASSICAL_V2_PRIORITY_AUTHENTICATION_20261006.json', 'ROOT_FRESH_PRIORITY_ADVERSARY_AUTHENTICATION_20261006.json'],
        'package': ['ROOT_PUBLICATION_SOURCE_V2_AUTHENTICATION_20261006.json', 'ROOT_PUBLICATION_READY_PACKAGE_V2_SEAL_20261006.json', 'ROOT_READY_PACKAGE_REPRODUCTION_V2_20261006.json', 'ROOT_READY_FOR_PUBLICATION_20261006.json'],
        'whole_package_R1': ['ROOT_WHOLE_PACKAGE_R1_AUTHENTICATION_20261006.json', 'whole_publication_package_round1_20261006/REPORT.md', 'whole_publication_package_round1_20261006/VERDICT.json', 'whole_publication_package_round1_20261006/REVIEW_MANIFEST.json', 'whole_publication_package_round1_20261006/SEAL.json'],
        'whole_package_R2': ['ROOT_WHOLE_PACKAGE_R2_AUTHENTICATION_20261006.json', 'whole_publication_package_round2_20261006/REPORT.md', 'whole_publication_package_round2_20261006/VERDICT.json', 'whole_publication_package_round2_20261006/REVIEW_MANIFEST.json', 'whole_publication_package_round2_20261006/SEAL.json'],
        'pre_execution_adversary': [],
        'final': ['ROOT_ACTUAL_PUBLICATION_AND_TRACKER_AUTHENTICATION_20261006.json', 'actual_publication_tracker_adversary_20261006/REPORT.md', 'actual_publication_tracker_adversary_20261006/VERDICT.json', 'actual_publication_tracker_adversary_20261006/REVIEW_MANIFEST.json', 'actual_publication_tracker_adversary_20261006/SEAL.json']}
    gate_usage = {role: [add_path(A / name, 'gate_checked_artifact:' + role) for name in paths] for role, paths in selected.items()}
    # Additional actual publication custody and fresh independent target-only readbacks.
    final_extra = [publication['metadata_HTTP_GET_receipt'], publication['actual_publish_command']]
    for item in publication['individual_upload_downloads']:
        final_extra.extend([item['body'], item['HTTP_GET_receipt']])
    # Dedup bodies stay private but are retained as exact audit inputs.
    dedup = sheet['DOI_dedup_actual_execution']
    final_extra.append(dedup)
    execution = json_body(C / dedup['path'], dedup)
    for field in ['stdout', 'stderr']:
        pin = execution[field]
        path = Path(pin['path'])
        if path.is_absolute():
            require(path.is_relative_to(A), 'Dedup custody scope')
            pin = {**pin, 'path': str(path.relative_to(C))}
        elif not str(path).startswith(str(A.relative_to(C)) + '/'):
            pin = {**pin, 'path': str(((C / dedup['path']).parent / path).relative_to(C))}
        final_extra.append(pin)
    for name in ['fresh_record.json', 'fresh_record.json.HTTP_GET.json', 'fresh_root_dependent_spanning_trees.pdf',
                 'fresh_root_dependent_spanning_trees.pdf.HTTP_GET.json', 'fresh_root_dependent_spanning_trees_support.zip',
                 'fresh_root_dependent_spanning_trees_support.zip.HTTP_GET.json', 'fresh_gws_execution.json', 'fresh_gws_started.json',
                 'fresh_gws_stdout.bin', 'fresh_gws_stderr.bin']:
        final_extra.append(local_pin(A / 'actual_publication_tracker_adversary_20261006' / name))
    gate_usage['final'].extend(add(pin, 'gate_checked_artifact:final') for pin in final_extra)
    # Explicit F01 repair artifact is already one logical package file; bind the R1/R2 usage.
    correction = next(p for p in registry.values() if p['path'].endswith('/source_preparation/CORRECTION_LEDGER.json'))
    gate_usage['whole_package_R1'].append(add(correction, 'gate_checked_artifact:whole_package_R1'))
    gate_usage['whole_package_R2'].append(add(correction, 'gate_checked_artifact:whole_package_R2'))
    gate_usage['pre_execution_adversary'] = [add(pin, 'gate_checked_artifact:pre_execution_adversary') for pin in [package_pin, auth['sourcepair'], pub_pin, sheet_pin]]
    sourcepair = json_body(C / auth['sourcepair']['path'], auth['sourcepair'])
    source_pins = {p['path']: {k: p[k] for k in ['bytes', 'sha256']} for p in sourcepair['input_pins']}
    source_cache = R / P / 'cache/catalog.sqlite'
    raw = {name: source_pins[str(R / P / 'cache' / name)] for name in ['problems.json', 'research_results.json']}
    source_cache_pin = source_pins[str(source_cache)]
    native_manifest = json.loads(baseline['manifest.json'])
    require(native_manifest['revision'] == '37e53eabe540fb458758e198be61634bd02ee008' and all(native_manifest['files'][name] == pin for name, pin in raw.items()), 'Native baseline raw/revision binding')
    for path, expected in [(source_cache, source_cache_pin), *[(R / P / 'cache' / n, pin) for n, pin in raw.items()]]:
        actual = metadata_pin(path)
        require({k: actual[k] for k in ['bytes', 'sha256']} == expected, 'Shared original raw/SQL pin changed')
    require(not any(Path(str(source_cache) + suffix).exists() for suffix in ['-wal', '-shm', '-journal']), 'SQL writer sidecar present')
    effective.update(main_parent=args.main_parent, native_baseline_pins=native_pins, queue_py_sha256=native_pins[0]['sha256'],
                     source_cache_pin=source_cache_pin, raw_source_pins=raw, original_authentication_pins=auth,
                     effective_diagnostics_pins=diagnostics, package={'root': str(package_root.relative_to(C)), 'manifest': package_pin},
                     publication={'receipt': pub_pin}, google_sheet={'receipt': sheet_pin, 'row_index': 31, 'values': sheet['values'], 'existing_chat_authorized': False},
                     assessment=oldass, campaign_note='Published attributed NP-completeness resolution; original claimed_solved effort 2/5, structured ledger absent, extra central proof turns 0; bounded recorded priority review and clean repaired-package R2.',
                     runtime=runtime, environment_policy=environment)
    effective['capacity_policy']['future_commit_overhead_bytes'] = 16 * 1024 * 1024
    require(effective['capacity_policy']['headroom_bytes'] == 32 * 1024 * 1024 and effective['capacity_policy']['runtime_overhead_bytes'] == 8 * 1024 * 1024, 'Reserve contract')
    manifest = {'schema': template['schema'], 'template_only': False, 'effective': effective,
                'program_files': program_files, 'input_files': sorted(registry.values(), key=lambda p: p['path'])}
    manifest_bytes = canonical(manifest)
    g.validate_execution_manifest(manifest, manifest_bytes)
    require(len(registry) <= 256 and sum(p['bytes'] for p in registry.values()) <= 32 * 1024 * 1024, 'Exact input registry capacity')
    require(set(registry) == set(usage) and all(v for v in usage.values()), 'Unrepresented registry usage')
    # Provisional allocation is complete with each future gate at its allowed maximum.
    copies = [(N + 'publication/authenticated_inputs/' + str((C / p['path']).relative_to(A)), p['bytes']) for p in registry.values()]
    copies += [(N + 'historical_original/' + str((C / p['path']).relative_to(ORIGINAL / 'original_attempt')), p['bytes']) for p in auth['original_files']]
    copies += [(N + ('EFFECTIVE_DIAGNOSTICS_README.md' if (C / p['path']).relative_to(A / 'repaired_diagnostics_v1').as_posix() == 'README.md' else (C / p['path']).relative_to(A / 'repaired_diagnostics_v1').as_posix()), p['bytes']) for p in diagnostics]
    source_record_pin = next(p for p in auth['original_files'] if p['path'].endswith('/source_record.json'))
    copies += [(N + 'source_record.json', source_record_pin['bytes']), (N + 'prior_imported_report.json', auth['selected_prior']['bytes']), (N + 'publication/EXECUTION_INPUTS.json', len(manifest_bytes))]
    gate_slots = {role: {'bytes': 65536} for role in g.GATE_ROLES}
    capacity = g.capacity_inventory(native_pins, [('bundle/' + name, size) for name, size in copies], gate_slots, package_files, effective['capacity_policy'], effective['process_policy'])
    free = shutil.disk_usage(D).free
    capacity.update(UTC=now(), observed_free_bytes=free, current_capacity_sufficient=free >= capacity['required_free_bytes'],
                    gate_sizes_are_conservative_maxima=True, exact_final_gate_sizes_require_fresh_capacity_plan=True)
    private_pins = [sheet['processes']['metadata']['stdout_pin']]
    # Minimum privacy exclusions: metadata enumerates other tabs; DOI-column dedup enumerates other rows.
    dedup_stdout = next(pin for pin in final_extra if pin['path'].endswith('/tracker_postpub_DOI_dedup/stdout.bin'))
    private_pins.append(dedup_stdout)
    privacy = {'schema': 'pr108-exact-private-export-exclusions/v1', 'exclusions': [
        {'input_pin': pin, 'candidate_affected_path': N + 'publication/authenticated_inputs/' + str((C / pin['path']).relative_to(A)),
         'reason': 'Non-target Sheet tabs and metadata' if pin == private_pins[0] else 'Non-target Sheet DOI rows',
         'internal_verification': 'Retain exact pinned bytes privately; remove only this offered file from separately reviewed public export.'} for pin in private_pins],
        'private_runtime_configuration': locations + configs + ghpins,
        'runtime_configuration_in_input_files': False,
        'released_receipts_keep_original_pin_references': True,
        'private_originals_must_be_retained_for_reproduction': True,
        'execution_inputs_remain_unchanged_by_public_export_filter': True,
        'helper_archives_every_reviewed_input_into_private_candidate': True,
        'public_export_requires_parent_exact_allowlist_review': True}
    require(command([str(git_executable), 'rev-parse', 'HEAD'], g.GIT_ENV, 4096).decode().strip() == args.main_parent, 'Main changed during inert build')
    output = HERE / ('draft_' + sha(manifest_bytes)[:16])
    output.mkdir(exist_ok=False)
    outputs = {'EXECUTION_INPUTS_DRAFT.json': manifest_bytes, 'PROPOSED_GATE_CHECKED_ARTIFACT_USAGE.json': canonical(gate_usage),
               'EXACT_INPUT_USAGE.json': canonical({path: sorted(consumers) for path, consumers in sorted(usage.items())}),
               'CAPACITY_PLAN_WITH_RESERVED_GATES.json': canonical(capacity), 'PRIVATE_EXPORT_EXCLUSIONS.json': canonical(privacy),
               'READ_SCOPE_AND_RUNTIME_METADATA.json': canonical({'reads': list(READS.values()), 'helper_context_pins': helper_context_pins,
                    'runtime_shell_pin': shell_pin, 'private_body_validation_deferred_to_guarded_parent_run': True,
                    'Git_directory': str(gitdir), 'Git_common_directory': str(commondir), 'expected_GH_login_supplied_by_parent': 'AlecKriebel',
                    'no_fresh_GH_or_service_authentication_by_builder': True}),
               'READ_ONLY_GIT_PROCESS_JOURNAL.json': canonical({'actual_builder_PID': os.getpid(), 'records': JOURNAL})}
    receipt = {'schema': 'pr108-inert-execution-input-preparation/v1', 'UTC': now(), 'actual_builder_PID': os.getpid(),
               'main_parent': args.main_parent, 'helper_directory': str(D), 'execution_inputs_sha256': sha(manifest_bytes),
               'registry_files': len(registry), 'registry_bytes': sum(p['bytes'] for p in registry.values()),
               'required_free_bytes': capacity['required_free_bytes'], 'observed_free_bytes': free,
               'capacity_sufficient_at_snapshot': capacity['current_capacity_sufficient'],
               'native_prepare_assess_export_execution_count': 0, 'service_call_count': 0, 'new_central_proof_search_turns': 0,
               'mathematical_discovery_complete_percent': 100, 'inert_input_preparation_complete_percent': 100,
               'remaining': 'Parent seals exact final main/config choices, validates private configurations, independently reviews frozen manifest, issues seven fresh gates, and separately commissions any later native operation.'}
    outputs['PREPARATION_RECEIPT.json'] = canonical(receipt)
    for name, data in outputs.items():
        (output / name).write_bytes(data)
    pins = [{'relative_path': name, 'bytes': len(data), 'sha256': sha(data)} for name, data in sorted(outputs.items())]
    (output / 'PACKET_MANIFEST.json').write_bytes(canonical({'schema': 'pr108-inert-preparation-packet/v1', 'files': pins}))
    print(json.dumps({'output': str(output), 'execution_inputs_sha256': sha(manifest_bytes), 'input_count': len(registry),
                      'input_bytes': receipt['registry_bytes'], 'required_free_bytes': capacity['required_free_bytes'], 'observed_free_bytes': free,
                      'capacity_sufficient': capacity['current_capacity_sufficient'], 'native_execution_count': 0, 'service_calls': 0}))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--helper-dir', type=Path, required=True)
    parser.add_argument('--main-parent', required=True)
    build(parser.parse_args())
