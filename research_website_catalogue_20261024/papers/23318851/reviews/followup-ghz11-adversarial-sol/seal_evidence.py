"""Seal only own captured bounded-screen evidence; make the final tree read-only."""
from pathlib import Path
import datetime, hashlib, json, os, stat
if not __debug__:
    raise RuntimeError('Finite seal requires assertions')
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23318851/reviews/followup-ghz11-adversarial-sol')
def read(name):return json.loads((OWN/name).read_bytes())
def pin(path):
    z=path.lstat();assert stat.S_ISREG(z.st_mode) and not path.is_symlink()
    raw=path.read_bytes();after=path.lstat()
    assert (z.st_dev,z.st_ino,z.st_mode,z.st_size,z.st_mtime_ns,z.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_mode,after.st_size,after.st_mtime_ns,after.st_ctime_ns)
    return dict(bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),mode=format(stat.S_IMODE(z.st_mode),'04o'))
assert read('ACQUIRE_EXECUTION.json')['exit_code']==read('EXACT_EXECUTION.json')['exit_code']==0
assert all(x['exit_code']==0 for x in read('ACQUISITION_EXECUTIONS.json'))
assert all(x['exit_code']==0 for x in read('PDF_RENDER_EXECUTIONS.json'))
assert read('PROTECTED_AFTER.json')['exact_bytes_modes_topology_mtime_ctime_equal']
assert read('PROTECTED_BEFORE.json')['trees']==read('PROTECTED_AFTER.json')['trees']
certificate=read('EXACT_CERTIFICATE.json')
assert certificate['raw_sign_vector_count']==2048 and certificate['negative_factors']==certificate['positive_factors']==1024 and certificate['zero_factors']==0
assert certificate['Q2_raw_sign_product']==certificate['Q2_independent_binomial_product']
assert pin(OWN/'RAW_SIGN_FACTORS.tsv')['SHA256']==certificate['raw_trace_SHA256']
assert certificate['ratio_binary_bracket']==dict(lower_exponent=135,upper_exponent=136,strict_lower=True)
assert read('LIMITS.json')['bounded_screen_completion_percent']==100
assert read('LIMITS.json')['no_novelty_priority_claim']
for execution,source in [('ACQUIRE_EXECUTION.json','acquire_primary.py'),('EXACT_EXECUTION.json','exact_control.py')]:
    assert pin(OWN/source)['SHA256']==read(execution)['source']['SHA256']
with (OWN/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n'+datetime.datetime.now(datetime.timezone.utc).isoformat()+' — Finite terminal seal validates captured primary/reading/control exits, exact route agreement, literal factor-table hash, and before/after protected metadata equality. Only own evidence is read by this sealer. Payload/terminal files become0444 and directories0555. Bounded goal100%; catalogue69.458128% active/incomplete.\n')
manifest_path=OWN/'MANIFEST.json';final_path=OWN/'FINAL.json'
manifest_stream=manifest_path.open('x');final_stream=final_path.open('x')
manifest_stream.write('{}\n');manifest_stream.flush();final_stream.write('{}\n');final_stream.flush()
all_paths=list(OWN.rglob('*'))
for path in all_paths:
    z=path.lstat();assert not path.is_symlink()
    if stat.S_ISREG(z.st_mode):path.chmod(0o444)
    else:assert stat.S_ISDIR(z.st_mode)
for path in sorted([p for p in all_paths if p.is_dir()],key=lambda p:len(p.parts),reverse=True):path.chmod(0o555)
OWN.chmod(0o555)
files=[];directories=[]
for path in sorted(OWN.rglob('*')):
    rel=path.relative_to(OWN).as_posix();z=path.lstat();assert not path.is_symlink()
    if path.is_dir():directories.append(dict(path=rel,mode=format(stat.S_IMODE(z.st_mode),'04o')))
    elif path not in (manifest_path,final_path):files.append(dict(path=rel,**pin(path),hidden=any(x.startswith('.') for x in Path(rel).parts),empty=z.st_size==0))
manifest=dict(schema='finite-ghz11-bounded-falsification-manifest-v1',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),root=str(OWN),root_mode='0555',regular_files=len(files)+2,child_directories=len(directories),payload_files=files,directories=directories,exact_already_created_terminal_recursive_hash_exclusions=[str(manifest_path),str(final_path)],terminal_controls=[dict(path=p.name,mode=pin(p)['mode']) for p in (manifest_path,final_path)],other_exclusions=[],all_hidden_empty_files_bytes_modes_topology_included=True,no_future_subtree_or_basename_exclusions=True)
manifest_stream.seek(0);manifest_stream.write(json.dumps(manifest,indent=2)+'\n');manifest_stream.truncate();manifest_stream.flush();manifest_stream.close()
final=dict(schema='ghz11-bounded-falsification-final-v1',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='TARGET_FALSIFICATION_VERIFIED_AT_N11_UNDER_CHECKED_PRIMARY_DEFINITIONS',regular_files=manifest['regular_files'],child_directories=manifest['child_directories'],root_mode='0555',manifest=pin(manifest_path),exact_control_exit=0,exact_control_invocations=1,raw_sign_vectors=2048,independent_exact_routes_equal=True,eleven_realized_Gram_determinants='1/4',squared_Frobenius_norm='1',strict_ratio_certificate='Q2/Q1>2^52',exact_ratio_bracket='2^135<Q2/Q1<2^136',Seigal_diagonal_odd_n_assertion_falsified_at_11=True,Ferudun_Problem_3_8_universal_inclusion_falsified=True,protected_Gram194_source_95files_16dirs_and_six_original_INITIALs_140files_2dirs_exact_unchanged=True,peer_scientific_reports_opened=False,no_saved_research_support_code_executed=True,no_publication_promotion_original_paper_modification_or_outreach=True,no_novelty_priority_claim=True,bounded_screen_completion_percent=100,overall_catalogue_review_percent=141/203*100,programme_goal_active_incomplete=True,no_current_P_W_reads_by_sealer=True)
final_stream.seek(0);final_stream.write(json.dumps(final,indent=2)+'\n');final_stream.truncate();final_stream.flush();final_stream.close()
assert stat.S_IMODE(OWN.lstat().st_mode)==0o555
assert {p.relative_to(OWN).as_posix() for p in OWN.rglob('*') if p.is_file()}=={x['path'] for x in files}|{'MANIFEST.json','FINAL.json'}
assert {p.relative_to(OWN).as_posix():format(stat.S_IMODE(p.stat().st_mode),'04o') for p in OWN.rglob('*') if p.is_dir()}=={x['path']:x['mode'] for x in directories}
for item in files:assert pin(OWN/item['path'])=={key:item[key] for key in ('bytes','SHA256','mode')}
assert pin(manifest_path)==final['manifest'] and pin(final_path)['mode']=='0444'
print(json.dumps(dict(**final,FINAL_SHA256=pin(final_path)['SHA256'])))
