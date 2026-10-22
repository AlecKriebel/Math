from pathlib import Path
import json,hashlib,zipfile,re,datetime
A=Path(__file__).resolve().parents[2];O=A/'whole_package_adversary_01';P=A/'publication_package_v1';N=A/'native_revision_preparation_01'
checks=[]
def require(c,m):
 if not c:raise RuntimeError(m)
 checks.append(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p,ent):
 require(p.is_file() and not p.is_symlink(),'file_regular:'+str(p.relative_to(A)))
 require(p.stat().st_size==ent['bytes'] and sha(p)==ent['sha256'],'pin:'+str(p.relative_to(A)))
def parse(p):
 def duplicate(pairs):
  d={}
  for k,v in pairs:
   if k in d:raise ValueError('duplicate key '+k)
   d[k]=v
  return d
 return json.loads(p.read_text(),object_pairs_hook=duplicate,parse_constant=lambda c:(_ for _ in ()).throw(ValueError(c)))
M=parse(P/'PACKAGE_MANIFEST.json')
for ent in M['files']:pin(P/ent['path'],ent)
require(len(M['files'])==M['file_count']==45,'package_file_count_45')
require(sum(ent['bytes'] for ent in M['files'])==M['total_bytes']==310204,'package_scientific_bytes_310204')
V=parse(P/'verification/MANIFEST.json')
for ent in V['files']:pin(P/'verification'/ent['path'],ent)
require(len(V['files'])==V['file_count']==37,'verification_file_count_37')
require(sum(ent['bytes'] for ent in V['files'])==V['total_bytes'],'verification_total_bytes')
seal=parse(P/'PACKAGE_SEAL.json')
for key,file in [('PDF','focal_inversion_area.pdf'),('TeX','focal_inversion_area.tex'),('ZIP','verification_package.zip'),('deposit_manifest','zenodo-deposit.json'),('metadata','METADATA.json'),('scientific_manifest','PACKAGE_MANIFEST.json')]:pin(P/file,seal[key])
expected=({ent['path'] for ent in M['files']} - {'focal_inversion_area.pdf'}) | {'PACKAGE_MANIFEST.json'}
with zipfile.ZipFile(P/'verification_package.zip') as z:
 names=z.namelist();require(len(names)==len(set(names)),'zip_no_duplicates')
 require(set(names)==expected,'zip_exact_45_body_member_selection')
 require(z.testzip() is None,'zip_crc_integrity')
 for name in names:
  require(not (name.startswith('/') or '..' in Path(name).parts),'zip_no_traversal:'+name)
  require(z.read(name)==(P/name).read_bytes(),'zip_body_match:'+name)
require(parse(P/'METADATA.json')['metadata']==parse(P/'zenodo-deposit.json')['metadata'],'exact_intended_zenodo_metadata_equality')
delivery=parse(P/'zenodo-deposit.json')['files'];require([e['path'] for e in delivery]==['focal_inversion_area.pdf','verification_package.zip','METADATA.json','VERIFICATION_REPORT.md'],'intended_four_delivery_files')
for p in P.rglob('*.json'):
 if p.stat().st_size:parse(p)
 else:require(p.name.endswith('.stdout.json') and 'validation_run_02' in p.parts,'empty_JSON_is_deliberate_failed_stdout:'+p.name)
NS=parse(N/'SEAL.json');pin(N/'PROPOSAL_MANIFEST.json',NS['manifest']);pin(N/'PREPARATION_REPORT.json',NS['preparation_report'])
NM=parse(N/'PROPOSAL_MANIFEST.json')
for name,ent in NM['files'].items():pin(N/name,ent)
require(set(NM['files'])=={str(p.relative_to(N)) for p in N.rglob('*') if p.is_file()}-{'SEAL.json','PROPOSAL_MANIFEST.json'},'native_proposal_manifest_complete')
root=N/'payload/unsolved_math_prioritization/attempts/5100044';files=[p for p in root.rglob('*') if p.is_file()]
require(len(files)==22 and sum(p.stat().st_size for p in files)==97450,'native_22_files_97450_bytes')
for p in N.rglob('*.json'):parse(p)
for n in ('MANIFEST.json','independent_review/reviewed_hashes.json'):
 d=parse(root/n)
 for name,ent in d['files'].items():pin(root/name,ent)
pin(root/'MANIFEST.json',parse(root/'PUBLICATION_MANIFEST.json')['manifest'])
I=parse(N/'INPUT_PINS.json')
for name,ent in I['archive_files'].items():pin(A/'submitted_snapshot'/name,ent)
arc=[p for p in (A/'submitted_snapshot').rglob('*') if p.is_file()]
require(len(arc)==20 and sum(p.stat().st_size for p in arc)==61131,'archive_20_files_61131_bytes')
for op in parse(N/'NATIVE_ADOPTION_MAP.json')['operations']:
 pin(N/op['staged_path'],op['after'])
 if 'before' in op:pin(A/'submitted_snapshot'/str(Path(op['native_path']).relative_to('unsolved_math_prioritization/attempts/5100044')),op['before'])
for n,same in [('verify.py','verify_exact.py'),('independent_review/independent_check.py','diagnose_geometry.py'),('requirements.txt','requirements.txt')]:require((root/n).read_bytes()==(P/'verification'/same).read_bytes(),'native_byte_copy:'+n)
for p in root.rglob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if target.startswith(('http:','https:')):continue
  virtual=Path('unsolved_math_prioritization/attempts/5100044')/p.relative_to(root)
  virtual_target=(A.parents[2]/virtual.parent/target).resolve()
  require((p.parent/target).resolve().exists() or virtual_target.exists(),'native_link_target_exists:'+str(p.relative_to(root))+':'+target)
# Every primary snapshot is hashed, not reproduced in public output.
source_checks=[]
for ent in parse(root/'source_manifest.json')['source_pdf_reading_copy_pins']:
 matches=list((A/'problem_source_contract_01/private_sources').glob(ent['file']))
 require(len(matches)==1 and sha(matches[0])==ent['sha256'],'primary_reading_pin:'+ent['file'])
 source_checks.append(ent['file'])
# Current output pins cannot substitute for execution: compare genuinely computed fresh output.
exact=parse(O/'runs/exact_fresh.json');stored=parse(P/'verification/exact_run_02.json')
require(exact==stored,'fresh_exact_output_byte_semantics_agree')
# Scan portable text files for private source content, dangerous executable import patterns and credentials.
scan=[]
for ent in M['files']:
 p=P/ent['path']
 if p.suffix in ('.json','.md','.py','.txt','.tex'):
  text=p.read_text()
  hits=[]
  for pattern in [r'BEGIN (?:RSA |OPENSSH )?PRIVATE KEY',r'ghp_[A-Za-z0-9]{20,}',r'sk-[A-Za-z0-9]{20,}',r'https?://[^\s\"<>]*token=',r'/Users/[^\s\"<>]+']:
   hits+=re.findall(pattern,text)
  if hits:scan.append({'path':ent['path'],'hits':hits})
report={'schema':'fresh-whole-package-integrity-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','check_count':len(checks),'checks':checks,'zip_members':sorted(expected),'source_pins_checked':source_checks,'privacy_scan_hits':scan,'package_total_inventory':sorted(str(p.relative_to(P)) for p in P.rglob('*') if p.is_file())}
(O/'INTEGRITY_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks),'zip_members':len(expected),'privacy_scan':scan,'package_other_files':sorted(set(report['package_total_inventory'])-{e['path'] for e in M['files']})},indent=2))
