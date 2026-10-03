#!/usr/bin/env python3
"""Read-only exact full-namespace/content verifier. No writes or subprocesses."""
from pathlib import Path
import hashlib,json,stat,zipfile
R=Path(__file__).resolve().parent;A=R.parent;P=A/'preprint/verification';S=R/'private/execution_package'
h=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def require(x,msg):
 if not x:raise AssertionError(msg)
exclusions={'MANIFEST.json','FINAL_SEAL.json','private/closure_001/verify.stdout','private/closure_001/verify.stderr','private/closure_001/verify.receipt.json'}
m=load(R/'MANIFEST.json');require(set(m['exclusions'])==exclusions,'literal exclusions')
for p in R.rglob('*'):
 require(stat.S_ISREG(p.lstat().st_mode) or stat.S_ISDIR(p.lstat().st_mode),'special file forbidden '+p.relative_to(R).as_posix())
actual={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file()};dirs={p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_dir()}
require(not any(p.is_symlink() for p in R.rglob('*')),'symlink forbidden');require(dirs==set(m['directories']),'directory set')
sealed=(R/'FINAL_SEAL.json').exists()
expected=set(m['files'])|{'MANIFEST.json'}
if sealed:expected|=exclusions
require(set(actual)==expected,'exact file set')
for name,e in m['files'].items():
 p=actual[name];data=p.read_bytes();require(stat.S_ISREG(p.lstat().st_mode),'regular file '+name);require(len(data)==e['bytes'] and h(data)==e['sha256'],'content '+name)
if sealed:
 seal=load(R/'FINAL_SEAL.json');require(seal['manifest_sha256']==h((R/'MANIFEST.json').read_bytes()),'manifest seal')
 require(set(seal['excluded_bindings'])==exclusions-{'FINAL_SEAL.json'},'excluded bindings set')
 for name,e in seal['excluded_bindings'].items():
  data=(R/name).read_bytes();require(len(data)==e['bytes'] and h(data)==e['sha256'],'excluded binding '+name)
 require(seal['mandatory_submission_defects']==0 and seal['no_further_namespace_writes'] is True,'final verdict')
# Fixed immutable submission pins, not self-described success strings.
for name,size,sha in [('biconstrained_asymmetry.tex',10991,'d225e6447a766f14713b418e7868679bfb38d82fbaa25823f9d500b8bd0783fc'),('biconstrained_asymmetry.pdf',67359,'35ddcd2a64bf0906fadcf762b913dfd9369941784ca0da87d97a3e9080ea80e4'),('biconstrained-asymmetry-verification.zip',198015,'5415f48f702ab2e234376b73c4853043b1b7601316392ff4750123eb66339d81'),('zenodo-deposit.json',1950,'e8da15076c07ef2942f4aaae5cc569423c90b3fce698783e755ffbe99f872562')]:
 data=(A/'preprint'/name).read_bytes();require(len(data)==size and h(data)==sha,'submission '+name)
anal=load(R/'ANALYTIC_SEAL.json');require(h((R/anal['path']).read_bytes())==anal['sha256'],'own analytic seal')
require(anal['before_modern_verdicts'] and anal['before_candidate_code_execution'],'analytic ordering')
receipt=load(R/'ALL_FILE_READ_RECEIPT.json');require(len(receipt['all_file_reads'])==87 and len(receipt['manifest_bindings'])==253,'full file/manifest count')
require((receipt['original_nested_instances'],receipt['family_public_instances'],receipt['outer_instances'])==(135,32,86),'253 split')
files={p.relative_to(P).as_posix():p for p in P.rglob('*') if p.is_file()};require(len(files)==87,'distributed87');require(not any(p.is_symlink() for p in P.rglob('*')),'package symlinks')
require(set(files)=={e['path'] for e in receipt['all_file_reads']},'all87 recorded reads')
for e in receipt['all_file_reads']:
 data=files[e['path']].read_bytes();require(len(data)==e['bytes'] and h(data)==e['sha256'],'distributed read '+e['path'])
 require(data==(S/e['path']).read_bytes(),'execution package '+e['path'])
for e in receipt['manifest_bindings']:
 base=(P/e['manifest']).parent;data=(base/e['path']).read_bytes();require(len(data)==e['bytes'] and h(data)==e['sha256'],'manifest '+e['manifest']+':'+e['path'])
reference=A/'snapshot/unsolved_math_prioritization/attempts/30004048'
require({p.relative_to(reference).as_posix() for p in reference.rglob('*') if p.is_file()}=={name[len('reference/'):] for name in files if name.startswith('reference/')},'original41 scope')
for name,p in files.items():
 if name.startswith('reference/'):require(p.read_bytes()==(reference/name[len('reference/'):]).read_bytes(),'original reference '+name)
with zipfile.ZipFile(A/'preprint/biconstrained-asymmetry-verification.zip') as z:
 require(len(z.infolist())==87 and set(z.namelist())=={'biconstrained-asymmetry-verification/'+n for n in files},'zip literal inventory')
 for item in z.infolist():
  require(not stat.S_ISLNK(item.external_attr>>16) and not item.is_dir(),'zip member type');name=item.filename.split('/',1)[1];require(z.read(item)==files[name].read_bytes(),'zip bytes '+name)
specs=[('reference/verify_turn1.py','reference/TURN_1_CHECKS.json',29175),('reference/verify_turn2.py','reference/TURN_2_CHECKS.json',12749),('reference/verify_turn3.py','reference/TURN_3_CHECKS.json',1831),('reference/review/check_independent.py','reference/review/INDEPENDENT_CHECKS.json',2552),('controls/graph_boundary_controls.py','controls/graph_boundary_expected.json',122568),('controls/polytope_controls.py','controls/polytope_expected.json',357),('verify_package.py',None,None)]
replays=load(R/'REPLAY_RECEIPT.json');require([e['program'] for e in replays['entries']]==[s[0] for s in specs],'seven order/count');require(replays['capture_driver_sha256']==h((R/'private/replay_portable.py').read_bytes()),'portable driver')
whole=[]
for (program,expected,count),e in zip(specs,replays['entries']):
 stem=R/'private/replays_001'/e['capture_stem'];out=stem.with_suffix('.stdout').read_bytes();err=stem.with_suffix('.stderr').read_bytes();stored=load(stem.with_suffix('.receipt.json'))
 require(stored==e,'stored replay receipt');require(e['exit_code']==0 and not err,'replay zero/empty '+program)
 require(e['argv']==[replays['python'],'-B',str(S/program)],'literal replay argv')
 cwd=S/'reference' if program.startswith('reference/') else (S/program).parent;require(e['cwd']==str(cwd),'literal replay cwd')
 require(e['start_utc']<=e['end_utc'],'replay chronology');require(e['program_sha256']==h((S/program).read_bytes()),'program '+program)
 require((len(out),h(out),len(err),h(err),h(b'STDOUT\0'+out+b'STDERR\0'+err))==(e['stdout_bytes'],e['stdout_sha256'],e['stderr_bytes'],e['stderr_sha256'],e['logical_stream_sha256']),'whole native streams '+program)
 exp=S/expected if expected else R/'private/package_expected.json';require(e['expected_file']==str(exp),'expected path');require(out==exp.read_bytes() and e['expected_sha256']==h(exp.read_bytes()),'whole expected bytes '+program)
 if count:
  o=json.loads(out);require(o.get('assertions',o.get('exact_assertions'))==count,'exact check count');whole.append(dict(program=program,whole_stdout_bytes=len(out),whole_stdout_sha256=h(out),exact_checks=count,exit_code=0,stderr_bytes=0))
package_expected=json.dumps(dict(status='PASS',original_files=41,nested_manifest_instances=135,whole_program_replays=whole,writes=0,scope='Exact finite controls, original proof-record custody and whole receipt reproduction. The universal proof is in the manuscript. The exact invariant minima, values, ordering and global priority are not certified by these computations. Raw primary sources and API evidence are omitted; source identities and retrieval recipes are supplied.'),sort_keys=True,indent=2)+'\n'
require((R/'private/package_expected.json').read_bytes()==package_expected.encode(),'independently reconstructed package expected whole stream')
# Latest corrected own source plus both forensic earlier versions and failures.
c=load(R/'CONTROLS_RECEIPT.json');stem=R/c['capture_stem'];out=stem.with_suffix('.stdout').read_bytes();err=stem.with_suffix('.stderr').read_bytes();require(out==(R/'CONTROLS.json').read_bytes() and not err and c['exit_code']==0,'own whole controls')
require(c['program_sha256']==h((R/'independent_controls.py').read_bytes()),'latest own source');require(c['stdout_sha256']==h(out) and c['logical_stream_sha256']==h(b'STDOUT\0'+out+b'STDERR\0'+err),'own logical stream');o=json.loads(out);require(o['assertions']==919==sum(o['categories'].values()),'own919')
for folder,source,code in [('fresh_controls_001','controls.failed_source.py',1),('fresh_controls_002','controls.executed_source.py',0)]:
 d=R/'private'/folder;e=load(d/'controls.receipt.json');stdout=(d/'controls.stdout').read_bytes();stderr=(d/'controls.stderr').read_bytes();require(h((d/source).read_bytes())==e['program_sha256'],'forensic source '+folder);require(e['exit_code']==code,'forensic exit');require((len(stdout),h(stdout),len(stderr),h(stderr),h(b'STDOUT\0'+stdout+b'STDERR\0'+stderr))==(e['stdout_bytes'],e['stdout_sha256'],e['stderr_bytes'],e['stderr_sha256'],e['logical_stream_sha256']),'forensic streams');require((code==1 and len(stderr)==351 and not stdout) or (code==0 and not stderr and stdout==out),'forensic semantics')
for e in load(R/'SOURCE_RECEIPTS.json'):
 data=(R/'private/sources'/f"{e['name']}.pdf").read_bytes();require(e['exit']==0 and len(data)==e['size'] and h(data)==e['sha256']==e['expected_sha256'],'fresh primary source '+e['name'])
priority=load(P/'audits/priority/SEARCH_COVERAGE.json');qs=[dict(record=c['record'],utc=c['utc'],q=q['q']) for c in priority['web_call_arguments'] for q in c['arguments'].get('search_query',[])];require(qs==priority['exact_queries'] and len(qs)==64,'complete priority query semantics')
meta=load(A/'preprint/zenodo-deposit.json');require([e['path'] for e in meta['files']]==['biconstrained_asymmetry.pdf','biconstrained-asymmetry-verification.zip'],'selected files');require(meta['metadata']['publication_type']=='preprint' and meta['metadata']['creators'][0]['orcid']=='0009-0001-9320-500X','metadata')
print(json.dumps(dict(status='PASS_SEALED' if sealed else 'PASS_PRESEAL',manifest_entries=len(m['files']),public_files=sum(not n.startswith('private/') for n in m['files']),private_files=sum(n.startswith('private/') for n in m['files']),distributed_files=87,manifest_instances=253,portable_complete_replays=7,independent_controls=919,mandatory_submission_defects=0,scope='Read-only whole namespace and saved native evidence verification. Universal mathematics and bounded priority are in sealed analytic assessment and final report; no exact minima, values, sign, or global novelty certification.'),indent=2,sort_keys=True))
