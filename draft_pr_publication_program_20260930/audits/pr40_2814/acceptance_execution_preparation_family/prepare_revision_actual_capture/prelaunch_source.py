#!/usr/bin/env python3
"""Own source/data authoring utility; never import or execute prepared candidates."""
import ast
import datetime as dt
import difflib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
A = HERE.parent
R = A.parents[2]
OLD = A / 'acceptance_preparation_family'
AUDIT = A / 'acceptance_static_adversary_family'
NEW = HERE / 'integration_source_revision'
ORIGINAL_PIN = 'a7bbde5e024a6e432d7456586651208b3f365170cfc80112e0b98de1cae4c39b'
AUDIT_PIN = '84b0e1c5364fac20617c1242e36c0d5b9130ea2784de81d3557ae8cbe94ab526'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def parse(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def row(path, base):
    raw = path.read_bytes()
    return {'path': path.relative_to(base).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}


def encode(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def dump(path, obj):
    with path.open('xb') as stream:
        stream.write(encode(obj))


def closure(base, name, pin, count):
    raw = (base / name).read_bytes()
    require(sha(raw) == pin, 'Closed input manifest pin changed')
    obj = parse(raw)
    rr = obj['files']
    require(type(rr) is list and len(rr) == count, 'Closed input count changed')
    names = set()
    for z in rr:
        require(type(z) is dict and type(z['path']) is str and type(z['bytes']) is int and z['bytes'] >= 0, 'Typed rows required')
        p = PurePosixPath(z['path'])
        require(not p.is_absolute() and '..' not in p.parts and p.as_posix() == z['path'] and z['path'] not in names, 'Canonical unique member required')
        names.add(z['path'])
        f = base / z['path']
        require(f.is_file() and not f.is_symlink(), 'Regular closed file required')
        data = f.read_bytes()
        require(len(data) == z['bytes'] and sha(data) == z['sha256'], 'Closed input member changed')
    require(name not in names, 'Literal root self exclusion required')
    actual_files, actual_dirs = set(), set()
    for p in base.rglob('*'):
        require(not p.is_symlink() and (p.is_file() or p.is_dir()), 'Unsafe closed topology')
        (actual_files if p.is_file() else actual_dirs).add(p.relative_to(base).as_posix())
    expected_dirs = {p.as_posix() for n in names for p in PurePosixPath(n).parents if p.as_posix() != '.'}
    require(actual_files == names | {name} and actual_dirs == expected_dirs, 'Closed exact recursive membership changed')
    return row(base / name, R)


def replace_once(text, before, after):
    require(text.count(before) == 1, 'Expected unique source preimage missing: ' + before[:70])
    return text.replace(before, after, 1)


def main():
    created = dt.datetime.now(dt.timezone.utc).isoformat()
    old_pin = closure(OLD, 'PREPARATION_MANIFEST.json', ORIGINAL_PIN, 12)
    audit_pin = closure(AUDIT, 'FIRST_PARTY_MANIFEST.json', AUDIT_PIN, 22)
    old_inventory = [row(p, OLD) for p in sorted(OLD.rglob('*')) if p.is_file()]
    current = A / 'reviewed_candidate'
    current_pin = closure(current, 'MANIFEST.json', '8de92d903edaec7471f4ecc3df443b7e779732b0ee83cdec507c22025bfae25f', 239)
    require(all(p.stat().st_mode & 0o777 == 0o444 for p in current.rglob('*') if p.is_file()), 'Current mode0444 changed')
    snapshot = parse((A / 'snapshot_manifest.json').read_bytes())
    original_rows = []
    for z in snapshot['files']:
        raw = (A / 'source_snapshot' / z['path']).read_bytes()
        require(raw == (current / z['path']).read_bytes() == (current / 'original_archive' / z['path']).read_bytes(), 'Original13/current/archive changed')
        original_rows.append(row(A / 'source_snapshot' / z['path'], R))
    require(len(original_rows) == 13 and sha((A / 'source_snapshot/SOURCE_STATUS.md').read_bytes()) == 'c232697fb80c20a88efe7db12390d9bda2d7f5c2fdc96e5cfad3a98a8cfdf16c', 'Original source status differs')
    require(not NEW.exists() and not NEW.is_symlink(), 'Retain existing preparation; never overwrite')
    NEW.mkdir()
    sources = ['pr40_guards.py', 'seal_final_evidence.py', 'integrate_reviewed_partial.py', 'state_mirror_reconciliation.py', 'verify_post_acceptance.py']
    contents = {name: (OLD / name).read_text() for name in sources}
    g = replace_once(contents['pr40_guards.py'], 'A = HERE.parent\n', 'A = HERE.parents[1]\n')
    before = """    if exclusive: require(not p.exists(),'Existing output: inspect before retry')
    tmp=p.with_name(p.name+'.pr40-tmp')
    with tmp.open('xb') as s: s.write(raw); s.flush(); os.fsync(s.fileno())
    os.replace(tmp,p)
"""
    after = """    if exclusive: require(not p.exists(),'Existing output: inspect before retry')
    tmp=p.with_name(p.name+'.pr40-tmp')
    with tmp.open('xb') as s: s.write(raw); s.flush(); os.fsync(s.fileno())
    if exclusive:
        # Atomic absent-only publication of complete fsynced bytes. On failure
        # retain the completed temp and any intervening target for inspection.
        os.link(tmp,p,follow_symlinks=False)
        tmp.unlink()
    else:
        os.replace(tmp,p)
"""
    g = replace_once(g, before, after)
    before = 'def basis():\n    inputs=load(HERE/\'INPUT_BINDINGS.json\')\n'
    after = """def utc_clock(value,context):
    require(type(value) is str and value and value==value.strip(),context+': ISO UTC clock required')
    try:
        clock=dt.datetime.fromisoformat(value[:-1]+'+00:00' if value.endswith('Z') else value)
    except (TypeError,ValueError):
        raise ValueError(context+': invalid ISO UTC clock')
    require(clock.tzinfo is not None and clock.utcoffset()==dt.timedelta(0),context+': timezone-aware UTC required')
    return clock


def revision_basis():
    revision=load(HERE/'REVISION_BINDINGS.json')
    required(revision,{'schema':'pr40-acceptance-source-revision-bindings/v1','original_preparation_manifest_sha256':'a7bbde5e024a6e432d7456586651208b3f365170cfc80112e0b98de1cae4c39b','closed_static_audit_manifest_sha256':'84b0e1c5364fac20617c1242e36c0d5b9130ea2784de81d3557ae8cbe94ab526','original_preparation_members':12,'closed_static_audit_members':22,'prepared_helpers_imported_or_executed':False,'actual_execution_pending':True},'Closed source revision inputs')
    check(R,revision['immutable_revision_inputs'])
    manifest(A/'acceptance_preparation_family','PREPARATION_MANIFEST.json',revision['original_preparation_manifest_sha256'],12)
    manifest(A/'acceptance_static_adversary_family','FIRST_PARTY_MANIFEST.json',revision['closed_static_audit_manifest_sha256'],22)


def basis():
    revision_basis()
    inputs=load(HERE/'INPUT_BINDINGS.json')
"""
    g = replace_once(g, before, after)
    before = "    require(type(cap['started_utc']) is str and cap['started_utc'] and type(cap['finished_utc']) is str and cap['finished_utc'],'Actual clocks required')\n"
    after = """    started=utc_clock(cap['started_utc'],'Actual capture start')
    finished=utc_clock(cap['finished_utc'],'Actual capture finish')
    require(started<=finished,'Actual capture clocks reversed')
    require(started<=utc_clock(receipt['utc'],'Actual final reconciliation clock')<=finished,'Reconciliation clock outside genuine capture interval')
"""
    g = replace_once(g, before, after)
    before = "    cb=ps['reconciliation_capture'].parent; check(cb,[cap['stdout'],cap['stderr']]); require(sha(regular(cb,'prelaunch_source.py').read_bytes())==cap['source_sha256'],'Actual prelaunch source changed')\n"
    after = """    cb=ps['reconciliation_capture'].parent
    require(ps['reconciliation_capture'].name=='CAPTURE.json' and cb.parent==A,'Literal CAPTURE.json in a new adjacent root capture required')
    streams=rows([cap['stdout'],cap['stderr']])
    stream_names={z['path'] for z in streams}
    require(len(stream_names)==2 and all(len(relative(n).parts)==1 and n not in {'CAPTURE.json','prelaunch_source.py'} for n in stream_names),'Two distinct declared root stream basenames disjoint from capture/source required')
    require(len({'CAPTURE.json','prelaunch_source.py'}|stream_names)==4,'Exactly four distinct capture members required')
    check(cb,streams); require(sha(regular(cb,'prelaunch_source.py').read_bytes())==cap['source_sha256'],'Actual prelaunch source changed')
"""
    g = replace_once(g, before, after)
    before = "    exact(cb,{ps['reconciliation_capture'].name,'prelaunch_source.py',cap['stdout']['path'],cap['stderr']['path']})\n"
    after = "    exact(cb,{'CAPTURE.json','prelaunch_source.py'}|stream_names)\n"
    g = replace_once(g, before, after)
    before = "    require(type(fresh['reason']) is str and fresh['reason'] and type(fresh['current_head']) is str and re.fullmatch('[0-9a-f]{40}',fresh['current_head']),'Explicit dated root rebase reason/HEAD required')\n"
    after = """    created=utc_clock(fresh['created_utc'],'Actual root fresh preimage creation')
    require(created<=dt.datetime.now(dt.timezone.utc),'Fresh root preimage creation clock is in the future')
    require(type(fresh['reason_date_utc']) is str and fresh['reason_date_utc']==created.date().isoformat(),'Root rebase reason date must match the actual UTC creation date')
    require(type(fresh['reason']) is str and fresh['reason']==fresh['reason'].strip() and len(fresh['reason'])>=40 and len(fresh['reason'].split())>=6,'Substantive root-reviewed rebase reason required; a token such as yes is insufficient')
    require(type(fresh['current_head']) is str and re.fullmatch('[0-9a-f]{40}',fresh['current_head']),'Explicit fresh main HEAD required, independently of archived replay HEAD')
"""
    g = replace_once(g, before, after)
    contents['pr40_guards.py'] = g
    contents['integrate_reviewed_partial.py'] = replace_once(contents['integrate_reviewed_partial.py'], 'current_pr=40); inventory_guard(before_inv,inv)', 'current_pr=41); inventory_guard(before_inv,inv)')
    contents['state_mirror_reconciliation.py'] = replace_once(contents['state_mirror_reconciliation.py'], "    inv=g.load(g.B/'inventory.json'); inventory_guard(g.load(g.A/'integration_inventory_before.json'),inv); g.require(inv['completed_count']==30", "    inv=g.load(g.B/'inventory.json'); inventory_guard(g.load(g.A/'integration_inventory_before.json'),inv); g.required(inv,{'current_pr':41,'completed_count':30},'PostPR40 next-target metadata'); g.require(inv['completed_count']==30")
    for name, text in contents.items():
        ast.parse(text, filename=name)
        with (NEW / name).open('x') as stream:
            stream.write(text)
    with (NEW / 'INPUT_BINDINGS.json').open('xb') as stream:
        stream.write((OLD / 'INPUT_BINDINGS.json').read_bytes())
    scope = parse((OLD / 'SCIENTIFIC_SCOPE.json').read_bytes())
    require(scope['credited_existing_coverage'][2] == 'cusped orientable and nonorientable: published Kuhlmann operative full proof with retained lattice/point-selection qualifications', 'Scientific scope preimage differs')
    scope['credited_existing_coverage'][2:] = [
        'cusped orientable: published Kuhlmann2006 Theorem1.1 operative full proof with retained lattice/point-selection qualifications',
        'cusped nonorientable: Xia2110.14376v1 Theorems1.2/4.1 direct cusp argument with retained qualifications; credited preprint, no cover-descent shortcut or peer-review claim'
    ]
    dump(NEW / 'SCIENTIFIC_SCOPE.json', scope)
    draft = parse((OLD / 'DRAFT_FINAL_PLAN.json').read_bytes())
    draft['scientific_scope'] = scope
    draft['draft_prepared_utc'] = created
    require(draft['preparation_manifest_sha256'] is None and all(draft[k] is False for k in ['root_full_current_read_completed','root_full_whole_read_completed','independent_whole_current_pass']), 'Future root flags must remain false/null')
    dump(NEW / 'DRAFT_FINAL_PLAN.json', draft)
    revision_inputs = [old_pin, audit_pin, row(AUDIT / 'REPORT.md', R), row(AUDIT / 'ASSESSMENT.json', R), current_pin, row(A / 'source_snapshot/SOURCE_STATUS.md', R)]
    revision_inputs += [row(OLD / n, R) for n in ['INPUT_BINDINGS.json','SCIENTIFIC_SCOPE.json','DRAFT_FINAL_PLAN.json']]
    dump(NEW / 'REVISION_BINDINGS.json', {'schema':'pr40-acceptance-source-revision-bindings/v1','created_utc':created,'original_preparation_manifest_sha256':ORIGINAL_PIN,'closed_static_audit_manifest_sha256':AUDIT_PIN,'original_preparation_members':12,'closed_static_audit_members':22,'immutable_revision_inputs':revision_inputs,'original13_source_rows':original_rows,'original_current239_unchanged':True,'prepared_helpers_imported_or_executed':False,'actual_execution_pending':True,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0})
    contract = (OLD / 'CONTRACT.md').read_text()
    contract = replace_once(contract, 'This NEW preparation family contains proposed sources, not an actual acceptance or an execution result.', 'This NEW adjacent source revision supersedes the original source-only preparation for future execution. It contains proposed sources, not an actual acceptance or an execution result. Original closed preparation12+self and closed static audit22+self remain exact and are checked on every immutable-basis reconciliation through REVISION_BINDINGS.json. The revision path is acceptance_execution_preparation_family/integration_source_revision; HERE.parents[1] is the PR40 audit anchor.')
    contract = replace_once(contract, 'The exact scientific scope is `SCIENTIFIC_SCOPE.json`. SOURCE_STATUS stays unchanged.', 'The exact scientific scope is `SCIENTIFIC_SCOPE.json`. Published Kuhlmann2006 Theorem1.1 covers orientable cusps; Xia2110.14376v1 Theorems1.2/4.1 supplies the direct nonorientable cusped scope as a credited preprint. Both matching complete scope copies carry this distinction. SOURCE_STATUS stays unchanged.')
    contract = replace_once(contract, 'CAPTURE.json (or another explicit capture filename), prelaunch_source.py identical to the sealed sealer, and full stdout/stderr regular files.', 'literal CAPTURE.json, literal prelaunch_source.py identical to the sealed sealer, and two declared root stream basenames for complete stdout/stderr. Both names must be distinct from each other and disjoint from the capture/source reserved names; no nested stream paths are allowed. The capture directory is a NEW direct child of the PR40 audit folder and its exact recursive membership is four regular files, without extra directories.')
    contract = replace_once(contract, 'nonempty started_utc/finished_utc;', 'parseable timezone-aware UTC started_utc/finished_utc with start at or before finish and the final reconciliation receipt UTC inside that interval;')
    contract = replace_once(contract, 'approved_by_root true, nonempty dated reason, actual current_head40hex and13 unique full typed path/size/SHA rows covering all native files and inventory listed by NATIVE.', 'approved_by_root true, actual created_utc as an aware UTC ISO clock no later than the invocation clock, reason_date_utc equal to created_utc\'s YYYY-MM-DD UTC date, and a substantive stripped reason of at least40 characters and six whitespace-separated words. This lexical guard rejects a token such as yes; root\'s explicit approved review and pin provide the substantive justification, rather than claiming an automated semantic proof. Include actual current_head40hex and13 unique full typed path/size/SHA rows covering all native files and inventory listed by NATIVE. The fresh HEAD is checked against actual current main at preflight, separately from the older dated replay/freeze HEAD; routine checkpoint publication does not rewrite or require equality to that older head.')
    contract = replace_once(contract, 'marks only PR40 complete in inventory.', 'marks only PR40 complete in inventory, with completed_count30 and current_pr41 for the next target. Mirror/post additionally require those exact typed values.')
    contract += '\n## Exclusive evidence publication\n\nFor exclusive=True, every complete temp is opened exclusively, fully written, flushed and fsynced before atomic os.link(tmp,target,follow_symlinks=False) publication in the same directory. An intervening target causes atomic failure; the existing target and completed temp remain for inspection. The temp is unlinked only after successful publication, then the directory is fsynced. The preliminary absence check is an early diagnostic, not the atomic guarantee. Nonexclusive administration keeps explicit os.replace semantics. Partial final directories and failed temps are retained; no automatic cleanup or retry is claimed. None of the prepared sources was imported or executed in producing this source revision.\n'
    with (NEW / 'CONTRACT.md').open('x') as stream:
        stream.write(contract)
    changes = [
        {'id':'S1','change':'Split published Kuhlmann orientable and Xia v1 direct nonorientable cusp credit globally in both new scope copies; original SOURCE_STATUS unchanged'},
        {'id':'S2','change':'Parse aware UTC clocks, require ordered interval and receipt UTC containment'},
        {'id':'S3','change':'Literal adjacent CAPTURE/source and two distinct declared root stream basenames; exact four-file closure'},
        {'id':'S4','change':'Fsynced complete temp with atomic hardlink absent-only publication; unlink only after success and retain failure temp'},
        {'id':'S5','change':'Actual aware UTC creation date, matching reason_date_utc, substantive root reason and separately fresh actual HEAD'},
        {'id':'S6','change':'Advance inventory current_pr to41 after PR40 and require typed41 during mirror/post'}
    ]
    dump(NEW / 'CHANGE_RECORD.json', {'schema':'pr40-acceptance-source-revision-change-record/v1','created_utc':created,'changes':changes,'old_preparation_manifest':old_pin,'closed_static_audit_manifest':audit_pin,'report':row(AUDIT/'REPORT.md',R),'assessment':row(AUDIT/'ASSESSMENT.json',R),'old_preparation_preserved':True,'current239_and_original13_preserved':True,'full_problem_solved':False,'partial_valid':True,'novelty_claimed':False,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0,'actual_candidate_import_or_execution':False,'fresh_independent_static_review':'PENDING','actual_execution':'PENDING'})
    diff = []
    for name in sources + ['SCIENTIFIC_SCOPE.json','DRAFT_FINAL_PLAN.json','CONTRACT.md']:
        diff.extend(difflib.unified_diff((OLD/name).read_text().splitlines(keepends=True),(NEW/name).read_text().splitlines(keepends=True),fromfile='original/'+name,tofile='revision/'+name))
    with (NEW/'SOURCE_CHANGES.patch').open('x') as stream:
        stream.write(''.join(diff))
    source_rows = [{**row(NEW / name, R),'lines':len((NEW/name).read_text().splitlines())} for name in sources]
    dump(NEW/'STATIC_SOURCE_REVIEW.json', {'schema':'pr40-acceptance-source-revision-static-data-review/v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'AST_AND_BYTE_IDENTITY_CHECKED_ONLY','sources':source_rows,'prepared_helpers_imported_compiled_or_executed':False,'independent_review_pending':True,'actual_execution_pending':True,'old_preparation_members':12,'closed_static_audit_members':22,'current_members':239,'original_scientific_files':13,'full_problem_solved':False,'scientific_discovery_completion_percent':0,'source_revision_completion_percent':100,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0})
    with (NEW/'README.md').open('x') as stream:
        stream.write('# PR40 revised acceptance sources\n\nThis source-only adjacent revision repairs closed audit S1–S6. Read CONTRACT.md, CHANGE_RECORD.json and SOURCE_CHANGES.patch before review. The five sources are prepared proposals; none was imported, compiled or executed here. All actual final reconciliation/integration/mirror/post gates remain pending. New root flags stay false and preparation hash stays null. Root must read the whole revision and obtain a fresh independent static review before any actual helper execution.\n\nThe original closed12+self preparation and static22+self audit remain exact, along with original13/SOURCE_STATUS and current239/all216 dependencies. Original0/5,new0,audit0; scientific discovery0%; source revision100%; no new theorem, paper, DOI, tracker or release. Never add execution evidence inside this closed revision. Future root evidence belongs directly in the PR40 audit folder.\n')
    with (NEW/'RESEARCH_LOG.md').open('x') as stream:
        stream.write('# PR40 acceptance source revision log\n\n## '+created+' — Source-only repair checkpoint\n\nIndependently checked the six closed audit findings against all five original sources, contracts, report/assessment and original source-status attribution. Prepared the separate revised sources and complete matching scope/draft/contract. Original preparation12+self/static22+self/original13/current239 remain byte unchanged; relocation uses the explicit audit ancestor. No prepared helper import, compilation or execution, scientific proof attempt, Git/native/shared/remote mutation or outside contact. Source revision100%; independent static review and actual integration pending; scientific discovery0%; original0/5,new0,audit0. Parent root owns publication after review.\n')
    # Repeat retained preimages after all own writes; no execution of candidates.
    closure(OLD,'PREPARATION_MANIFEST.json',ORIGINAL_PIN,12)
    closure(AUDIT,'FIRST_PARTY_MANIFEST.json',AUDIT_PIN,22)
    closure(current,'MANIFEST.json',current_pin['sha256'],239)
    require(old_inventory == [row(p,OLD) for p in sorted(OLD.rglob('*')) if p.is_file()], 'Original preparation modified')
    for p in NEW.glob('*.json'):
        parse(p.read_bytes())
    files = [row(p,NEW) for p in sorted(NEW.rglob('*')) if p.is_file()]
    dump(NEW/'PREPARATION_MANIFEST.json',{'schema':'pr40-acceptance-source-revision-closure/v1','status':'CLOSED_SOURCE_ONLY_INDEPENDENT_REVIEW_PENDING','closed_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'self_excluded_paths':['PREPARATION_MANIFEST.json'],'files_count':len(files),'files':files,'directories':[],'foreign_excluded_prefixes':[],'scratch_exclusions':[],'original_preparation_manifest_sha256':ORIGINAL_PIN,'closed_static_audit_manifest_sha256':AUDIT_PIN,'prepared_helper_import_compile_or_execution':False,'actual_integration_pending':True,'source_revision_completion_estimate_percent':100,'scientific_completion_estimate_percent':0,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0})
    closure(NEW,'PREPARATION_MANIFEST.json',sha((NEW/'PREPARATION_MANIFEST.json').read_bytes()),len(files))
    for p in NEW.iterdir():
        p.chmod(0o444)
    print(json.dumps({'status':'SOURCE_REVISION_CLOSED_ONLY','prepared_helpers_executed':False,'authored_files':len(files),'preparation_manifest':row(NEW/'PREPARATION_MANIFEST.json',R),'independent_static_review':'PENDING','actual_integration':'PENDING'},sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
