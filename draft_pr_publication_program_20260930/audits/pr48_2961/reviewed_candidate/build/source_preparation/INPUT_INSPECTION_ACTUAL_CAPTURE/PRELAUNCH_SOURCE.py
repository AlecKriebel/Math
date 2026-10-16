"""Read complete already-closed first-party inputs; never run production code."""
import datetime as dt, hashlib, json, os, stat
from pathlib import Path
F=Path(__file__).absolute().parent;A=F.parent;R=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):
    assert not p.is_symlink() and not any(q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode)
    return p.read_bytes()
def row(p):
    b=raw(p);return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
def encode(o):return (json.dumps(o,indent=2,allow_nan=False)+'\n').encode()
closed={
 'original':('ORIGINAL_PREPARATION_MANIFEST.json','278e4fd39b5a13c7a181e3f7d494420c41ea4082fa8ab9add34229671a1be3b4',574,'pr48-original-preparation-self-only-manifest/v1'),
 'root':('root_original_actual_reproduction_v2/MANIFEST.json','f4d8a828e659c5f233053fb3309c38c8d3fe1c90520d6abef2d73b30df7776e9',254,'pr48-root-original-complete-reproduction-self-only-closure/v1'),
 'algebra':('algebra_cocycle_family/MANIFEST.json','127120bc00894444c01d44b49739685f03f229361a10568f1aec4f52c001dcd3',489,'pr48-algebra-cocycle-family-self-only-closure/v1'),
 'smooth':('smooth_geometry_family/MANIFEST.json','7248e58e1a86cc6aa574233826d5d8b645858917ab7c94836091d74235a3bdef',268,'pr48-smooth-geometry-family-closure-manifest/v1')}
pins={};allrows={};structured_exceptions={};bytes_read=0
for key,(name,expected,count,schema) in closed.items():
    p=A/name;mraw=raw(p);assert sha(mraw)==expected;m=json.loads(mraw);assert m['schema']==schema and m['files_count']==len(m['files'])==count
    root=p.parent;members=[]
    for item in m['files']:
        q=root/item['path'];r=row(q);assert r['bytes']==item['bytes'] and r['sha256']==item['sha256'] and r['full_mode']==0o444
        b=raw(q);bytes_read+=len(b);members.append(r);allrows[r['path']]=r
        if q.suffix in {'.json','.jsonl'}:
            try:json.loads(b)
            except (json.JSONDecodeError,UnicodeDecodeError):
                if q.suffix=='.jsonl':
                    try:
                        assert b.strip();[json.loads(line) for line in b.splitlines() if line.strip()]
                    except (json.JSONDecodeError,UnicodeDecodeError,AssertionError):structured_exceptions[r['path']]=dict(r,interpretation='IMMUTABLE_LITERAL_ARCHIVED_FAILED_OR_NONJSON_STREAM')
                else:structured_exceptions[r['path']]=dict(r,interpretation='IMMUTABLE_LITERAL_ARCHIVED_FAILED_OR_NONJSON_STREAM')
    if key=='original':
        names=set(m['authorship_root_files'])
        for d in m['authorship_directory_roots']:names.update(q.relative_to(root).as_posix() for q in (root/d).rglob('*') if q.is_file())
    else:names={q.relative_to(root).as_posix() for q in root.rglob('*') if q.is_file()}-{p.name}
    assert names=={r['path'] for r in m['files']};assert stat.S_IMODE(p.stat().st_mode)==0o444
    dirs={q.parent.relative_to(root).as_posix() for item in m['files'] for q in [root/item['path']]}
    actualdirs=[]
    for d in sorted({parent.relative_to(root).as_posix() for item in m['files'] for parent in (root/item['path']).parents if parent==root or root in parent.parents}):
        actualdirs.append({'path':d,'full_mode':stat.S_IMODE((root/d).stat().st_mode)})
    pins[key]={'manifest':row(p),'schema':schema,'root':root.relative_to(R).as_posix(),'self_name':p.name,'members':members,'directories':actualdirs,'authorship_root_files':m.get('authorship_root_files'),'authorship_directory_roots':m.get('authorship_directory_roots')}
    allrows[row(p)['path']]=row(p)
external=[]
externaldirs=[A/'original_preparation_closure_actual_capture']+sorted((A.parent/'pr45_9900007').glob('root_pr48*_actual_capture'))
for d in externaldirs:
    files=[]
    for q in sorted(d.iterdir()):assert q.is_file();files.append(row(q));allrows[row(q)['path']]=row(q)
    cap=json.loads(raw(d/'CAPTURE.json'));assert cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and cap['pid']>0 and type(cap['exit_code']) is int
    for stream in ['stdout','stderr']:
        b=raw(d/cap[stream]['path']);assert len(b)==cap[stream]['bytes'] and sha(b)==cap[stream]['sha256']
    external.append({'directory':d.relative_to(R).as_posix(),'members':files,'complete_capture':cap})
for name in ['snapshot_manifest.json','original_pr_metadata.json','ROOT_COMPLETE_RAW_SQL_AUDIT.json','ROOT_MATHEMATICAL_REVIEW.md']:
    r=row(A/name);allrows[r['path']]=r
rootresult=json.loads(raw(A/'root_original_actual_reproduction_v2/ROOT_REPRODUCTION_RESULT.json'))
assert len(rootresult['complete_actual_Git_captures'])==38 and len(rootresult['complete_actual_helper_captures'])==4
assert all(c['source'] is None and c['source_unchanged'] is None and c['schema']=='pr48-root-readonly-git-actual-capture/v1' for c in rootresult['complete_actual_Git_captures'])
assert all(type(c['source']) is dict and c['source_unchanged'] is True and c['schema']=='pr48-root-unchanged-helper-actual-capture/v1' for c in rootresult['complete_actual_helper_captures'])
record={'schema':'pr48-fixed-current-source-inputs/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_inspector_pid':os.getpid(),'status':'SOURCE_ONLY_ROOT_PREREQUISITES_PENDING','closed_inputs':pins,'external_completed_captures':external,'fixed_rows':sorted(allrows.values(),key=lambda r:r['path']),'exact_literal_structured_exceptions':sorted(structured_exceptions.values(),key=lambda r:r['path']),'read_bytes':bytes_read,'production_builder_executed':False,'ROOT_prerequisites_authored':False,'future_acceptance_approved':False}
(F/'STATIC_INPUT_BINDINGS.json').write_bytes(encode(record));print(json.dumps({'status':'PASS_COMPLETE_SOURCE_INPUT_READ','unique_fixed_bodies':len(allrows),'read_bytes':bytes_read,'archived_exact_json_exceptions':len(structured_exceptions),'ROOT_Git_captures':38,'ROOT_typed_helper_captures':4,'production_builder_executed':False},indent=2))
