"""External root scientific adjudication and full immutable namespace closure."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
A=Path(__file__).resolve().parent;N=A/'arithmetic'
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.now(timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b),'mode':stat.S_IMODE(p.stat().st_mode)}
def inventory():
    out={};dirs={}
    for p in sorted(N.rglob('*')):
        assert not p.is_symlink(),str(p)
        if p.is_file():out[str(p.relative_to(N))]=pin(p)
        elif p.is_dir():dirs[str(p.relative_to(N))]=stat.S_IMODE(p.stat().st_mode)
    return out,dirs
assert not (A/'ROOT_ARITHMETIC_CLOSURE.json').exists()
files,dirs=inventory();assert len(files)==111
assert files['MANIFEST.json']['sha256']=='2c5a2bd6d7f7068bbb74b550c182b6070f699340204288da73a1c897dad73532'
assert files['REPORT.md']['sha256']=='b09b75573decc88ccba5776146b39a54bfaa5758852cd5c8cb003b76fedcc3c9'
manifest=json.loads((N/'MANIFEST.json').read_bytes())
assert {k:v for k,v in files.items() if k!='MANIFEST.json'}==manifest['files']
D=A/'root_runs_private/arithmetic_full_external001'
native=json.loads((D/'execution.json').read_bytes())
assert native['exit_code']==0 and (D/'stderr.bin').read_bytes()==b''
for k in ['stdout','stderr']:
    b=(D/(k+'.bin')).read_bytes();assert len(b)==native[k+'_bytes'] and sha(b)==native[k+'_sha256']
full=json.loads((D/'stdout.bin').read_bytes())
assert full['status']=='PASS' and full['namespace_files_unchanged']==111 and full['all_namespace_bodies_modes_inventory_unchanged']
assert full['manifest_sha256']==files['MANIFEST.json']['sha256'] and full['full_replay_stderr']==''
inner=json.loads(full['full_replay_stdout']);assert inner['status']=='PASS' and inner['binding_count_before_after']==1657 and inner['all_bindings_unchanged']
assert len(inner['results'])==6 and all(x['matches_original_native_streams'] for x in inner['results'])
external=[]
for tag in ['system','bundled']:
    for suffix,receipt,wanted in [('', '019_independent_arithmetic',0),
        ('_drop_twist','020_mutant_drop_twist',1),('_wrong_radical','021_mutant_wrong_radical',1),
        ('_wrong_cyclotomic','022_mutant_wrong_cyclotomic',1),('_wrong_norm_degree','023_mutant_wrong_norm_degree',1)]:
        R=A/'root_runs_private'/('arithmetic_'+tag+suffix+'_external001')
        j=json.loads((R/'execution.json').read_bytes())
        assert j['exit_code']==wanted and (R/'stderr.bin').read_bytes()==b''
        for k in ['stdout','stderr']:
            b=(R/(k+'.bin')).read_bytes();assert len(b)==j[k+'_bytes'] and sha(b)==j[k+'_sha256']
            assert b==(N/'executions'/receipt/(k+'.txt')).read_bytes()
        assert j['programs'][0]['sha256']==files['check_arithmetic.py']['sha256']
        external.append({'interpreter_family':tag,'mutant':suffix[1:] or None,'actual_execution':j,'exact_original_stream_equality':True})
M=A/'ROOT_ARITHMETIC_NAMESPACE_MANIFEST.json'
M.write_text(json.dumps({'utc':utc(),'namespace':'arithmetic','files':files,'directories':dirs,
    'excluded_namespace_files':[],'whole_namespace_pinned':True,'raw_primary_files_private_not_public_package':True},indent=2)+'\n')
j={'utc':utc(),'status':'PASS_ROOT_EXTERNALLY_CLOSED_ARITHMETIC_FAMILY_ONLY',
    'root_one_time_external_authorization':'Root has fully read the final scientific report, source/first-assessment/test/closure gates, all current math/capture/replay/verifier/packaging programs, source/external bindings and log; checked the operative originals and generic/fiberwise proofs; native full local replay passed with complete mathematical streams and unchanged111-file/1657-binding inventories. Close this stable family only, without priority/publication approval.',
    'namespace_manifest':dict(path=str(M.relative_to(A)),**pin(M)),
    'root_full_scientific_reading':True,
    'source_reading_scope':'Original AIM complete Question17/all4remarks text/pixels; Fisher printed172,173,179-182,194,195 and selected original renders; MIT5 complete sections5.5-5.6 and MIT23 full12-14 plus original13. No exhaustive reading of unrelated rank/Selmer material, entire referenced books or every dependency source file is asserted.',
    'native_receipt_and_dependency_reading_scope':'Every28 native metadata/stream body and all runtime-file entries are integrity checked by the root-read verifier and full namespace pins; all scientific streams used in adjudication were fully read. Unrelated raw primary-page text and dependency resource bodies are bound, not claimed individually read for scientific meaning.',
    'full_native_external_execution':native,
    'full_native_verified_summary':{'namespace_files':111,'binding_count':1657,'positive_streams':2,'negative_mutants':4,'actual_child_environment':full['actual_replay_env'],'all_scientific_streams_read':True},
    'two_interpreter_portable_positive_and_mutant_replays':external,
    'arithmetic_family_percent':100,'exact_remaining_arithmetic_gap':'None within the stated normalized characteristic-zero family.',
    'Kummer_precision':'[-1/a]=[a] inverse with fixed generator; same radical field and split criterion. Explicit current-paper wording is required; historical candidate is preserved.',
    'entire_candidate_accepted':False,'priority_complete':False,'publication_ready':False,'original_author_turn_count':'1/5'}
assert inventory()==(files,dirs)
(A/'ROOT_ARITHMETIC_CLOSURE.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps({'utc':j['utc'],'status':j['status'],'files':len(files),'native_bindings':1657,'arithmetic_percent':100,'entire_candidate_accepted':False},indent=2))
