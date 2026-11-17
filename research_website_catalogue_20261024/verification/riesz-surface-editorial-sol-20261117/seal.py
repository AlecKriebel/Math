"""Passive finite private packet seal; does not import or rerun the builder."""
import datetime, hashlib, json, os
from pathlib import Path
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P/'verification/riesz-surface-editorial-sol-20261117'
SOURCE = P/'papers/23202994/sources'
TERMINALS = {'MANIFEST.json','FINAL.json'}

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def pin(path):
    a = path.lstat()
    assert stat.S_ISREG(a.st_mode) and not path.is_symlink()
    fd = os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        opened = os.fstat(fd)
        assert (a.st_dev,a.st_ino) == (opened.st_dev,opened.st_ino)
        chunks = []
        while True:
            part = os.read(fd,1048576)
            if not part:
                break
            chunks.append(part)
        z = os.fstat(fd)
        assert (opened.st_dev,opened.st_ino,opened.st_size,opened.st_mode,opened.st_mtime_ns,opened.st_ctime_ns) == (z.st_dev,z.st_ino,z.st_size,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
        assert (path.lstat().st_dev,path.lstat().st_ino) == (z.st_dev,z.st_ino)
        raw = b''.join(chunks)
        assert len(raw) == z.st_size
        return dict(bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),MD5=hashlib.md5(raw).hexdigest(),mode=format(stat.S_IMODE(z.st_mode),'04o'))
    finally:
        os.close(fd)

def census(root):
    files,dirs = {},{}
    pending = [root]
    while pending:
        here = pending.pop()
        a = here.lstat()
        assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
        for path in sorted(here.iterdir()):
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            if stat.S_ISDIR(info.st_mode):
                assert not path.is_symlink()
                dirs[rel] = format(stat.S_IMODE(info.st_mode),'04o')
                pending.append(path)
            else:
                files[rel] = pin(path)
        z = here.lstat()
        assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns) == (z.st_dev,z.st_ino,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
    return dict(root=str(root),root_mode=format(stat.S_IMODE(root.lstat().st_mode),'04o'),files=files,directories=dirs)

def read(name):
    return json.loads((OWN/name).read_bytes())

def write(name,value):
    with (OWN/name).open('x') as stream:
        json.dump(value,stream,indent=2)
        stream.write('\n')

started = now()
execution = read('EXECUTION.json')
assert execution['exit_code'] == 0 and execution['stdout_bytes'] == execution['stderr_bytes'] == 0 and execution['builder_unchanged']
assert pin(OWN/'prepare.py')['SHA256'] == execution['builder_SHA256']
assert read('PREPARATION_RESULT.json')['status'] == 'READY_FOR_INDEPENDENT_FACT_REVIEW'
source = census(SOURCE)
assert source == read('SOURCE_GUARDS_BEFORE.json') == read('SOURCE_GUARDS_AFTER.json')
assert (len(source['files']),len(source['directories'])) == (39,15)
write('SOURCE_GUARDS_FINAL.json',source)
collision = read('COLLISION_AND_CSS.json')
assert pin(Path(collision['stylesheet_path'])) == collision['stylesheet_before'] == collision['stylesheet_after']
for path in collision['collision_after']['checked_paths']:
    assert not os.path.lexists(path)
model = read('page-model.json')
assert all(model[k] is None for k in ('canonical_url','base_url','production_url','actual_publication_date','AA','follow_up'))
assert model['robots'] == 'noindex, nofollow' and not model['publication_authority']
assert [a['name'] for a in model['native_asset_order']] == ['paper.pdf','source-and-verification.zip']
for asset in model['native_asset_order']:
    assert pin(OWN/asset['local_path']) == {k:asset[k] for k in ('bytes','SHA256','MD5','mode')}
write('COPY_READ_AND_INPUT_PINS.json',dict(schema='row190-private-copy-full-reading-v1',UTC=now(),personally_read_actual_full_article_HEAD_BODY_MAIN=True,personally_read_actual_full_model_Bib=True,personally_read_full_saved_builder_runner_template_before_one_attempt=True,personally_read_full_saved_seal_before_invocation=True,scientific_clearance=dict(path='verification/root-clearance-23202994-20261117.json',pin=pin(P/'verification/root-clearance-23202994-20261117.json')),root_review=dict(path='papers/23202994/reviews/root-continuation-20261117/ROOT_REVIEW.md',pin=pin(P/'papers/23202994/reviews/root-continuation-20261117/ROOT_REVIEW.md')),source_terminal_pins={name:source['files'][name] for name in ('SOURCE_MANIFEST.json','SOURCE_FINAL.json')},scripts={name:pin(OWN/name) for name in ('prepare.py','invoke_once.py','seal.py')},source_schemas=['source-custody-manifest-v1 entries list with kind/path/mode_octal/sha256/MD5','source-custody-final-v1; payload37 plus2terminal controls; whole39/15'],new_scientific_runs=0,old_helper_imports=0,network_requests=0,W_Git_Sheet_writes=0,rendered_or_live_certificate=False))
finished = now()
with (OWN/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n'+finished+' — Actual completearticle/head/main/model/Bib read; freshfinalsource39/15 exact,2nativeassets exact, CSS unchanged, proposedtarget still absent. Completefiniteprivatepacket sealed, completion100% for editorialpreparation; independentfact/rootcopyreview pending. Quiescentstop.\n')
write('SEAL_EXECUTION.json',dict(schema='private-editorial-passive-seal-v1',started_UTC=started,finished_UTC=finished,argv=['python3','-B',str(OWN/'seal.py')],source39_15_exact=True,prepare_attempts=1,prepare_exit=0,seal_personally_read_before_one_invocation=True,scope='Own private packet data only; no source/helper execution or production authority'))
extent = census(OWN)
assert not (set(extent['files'])&TERMINALS)
payload = [dict(path=name,bytes=data['bytes'],SHA256=data['SHA256'],mode=oct(int(data['mode'],8))) for name,data in sorted(extent['files'].items())]
dirs = [dict(path=name,mode=oct(int(mode,8))) for name,mode in sorted(extent['directories'].items())]
names = sorted(set(extent['files'])|TERMINALS)
manifest = dict(schema='finite-private-editorial-manifest-v1',UTC=finished,root=str(OWN),root_mode=oct(int(extent['root_mode'],8)),payload_files=payload,directories=dirs,actual_file_count_including_terminal_controls=len(names),actual_child_directory_count=len(dirs),terminal_control_topology=[dict(path=name,kind='file',mode='0o644') for name in sorted(TERMINALS)],excluded_terminal_controls=sorted(TERMINALS),scope='Complete actual finite namespace; only exact terminal circular/self-hash pair excluded from payload hashes; no hidden/empty/ignored exclusions',hidden_paths=[p for p in sorted(set(extent['files'])|set(extent['directories'])) if any(c.startswith('.') for c in p.split('/'))],empty_files=[p for p,v in sorted(extent['files'].items()) if v['bytes']==0],empty_directories=[p for p in sorted(extent['directories']) if not any(q.startswith(p+'/') for q in set(extent['files'])|set(extent['directories']))])
write('MANIFEST.json',manifest)
write('FINAL.json',dict(schema='private-editorial-FINAL-v1',UTC=finished,record_id='23202994',sheet_row=190,status='READY_FOR_INDEPENDENT_FACT_REVIEW',private_editorial_completion_percent=100,scientific_clearance_inherited=True,scientific_clearance_completion_percent=100,new_scientific_runs=0,root=str(OWN),root_mode=manifest['root_mode'],manifest=dict(path='MANIFEST.json',**pin(OWN/'MANIFEST.json')),actual_files=len(names),actual_child_directories=len(dirs),whole_namespace_files=names,directories=dirs,terminal_self_hash_exclusions=sorted(TERMINALS),source_files=39,source_child_directories=15,source_all_bytes_modes_hidden_empty_topology_unchanged=True,native_assets_whole_bytes_modes_equal=True,native_asset_order=['paper.pdf','source-and-verification.zip'],abstract_original_full_declared_rendering_only=True,abstract_visible_DC_model_single_ScholarlyArticle_exact=True,canonical_url=None,base_url=None,production_url=None,actual_publication_date=None,AA=None,publication_authority=False,robots='noindex, nofollow',proposed_canonical_separate=model['deployment_proposal']['proposed_canonical_url'],shared_research_css_unchanged=True,proposed_target_absent_bounded_local_check=True,builder_attempts=1,builder_exit=0,builder_stdout_stderr_bytes=[0,0],failures=[],incidental_passive_lookup_error_preserved='Optional nonexistent P/sources/AGENTS.md lookup, recorded literally in RESEARCH_LOG.md; no producer failure/retry',follow_up=None,limits=['Private static data preparation only','No browser/render/live certificate','No W/Git/index/ref/config/Sheet/network/deploy/AA/redirect/release/outreach action','Independent fact audit and root actual copy reading still required'],quiescent_stop=True))
actual = census(OWN)
assert set(actual['files']) == set(names) and actual['directories'] == extent['directories'] and actual['root_mode'] == extent['root_mode']
for name,data in extent['files'].items():
    assert actual['files'][name] == data
expected_manifest = read('FINAL.json')['manifest'].copy()
assert expected_manifest.pop('path') == 'MANIFEST.json'
assert actual['files']['MANIFEST.json'] == expected_manifest
assert all(actual['files'][name]['mode'] == '0644' for name in TERMINALS)
assert census(SOURCE) == source
print(json.dumps(dict(status='FROZEN_READY_FOR_INDEPENDENT_FACT_REVIEW',files=len(names),directories=len(dirs),article=actual['files']['article.html'],manifest=actual['files']['MANIFEST.json'],FINAL=actual['files']['FINAL.json'],source39_15_exact=True)))
