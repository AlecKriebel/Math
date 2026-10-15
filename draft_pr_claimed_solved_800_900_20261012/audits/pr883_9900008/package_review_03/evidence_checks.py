#!/usr/bin/env python3
"""Independent checks of receipt transformations, public bytes, source editions and local Git objects.
Reads existing evidence, writes only review receipts. No candidate code import; no network or Git writes.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,io,itertools,json,re,subprocess,sys,zipfile
HERE=Path(__file__).resolve().parent
A=HERE.parent
ROOT=A/'replay/revision_r2'
PACKAGE=ROOT/'preprint/verification_package'
REPO=A.parents[2]
def need(ok,label):
 if not ok:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def js(p):return json.loads(p.read_bytes())
def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def diffs(x,y,path=''):
 if type(x)!=type(y):return [path]
 if isinstance(x,dict):
  if set(x)!=set(y):return [path+'/$keys']
  return [p for k in x for p in diffs(x[k],y[k],path+'/'+str(k))]
 if isinstance(x,list):
  if len(x)!=len(y):return [path+'/$length']
  return [p for k in range(len(x)) for p in diffs(x[k],y[k],path+'/'+str(k))]
 return [] if x==y else [path]
def repair():
 redact=js(A/'LEGACY_RECEIPT_PATH_REDACTION.json');rows=[]
 for family in redact['families']:
  name=family['family'];private=A/'private_legacy_receipt_paths'/name;public=PACKAGE/'audits'/name
  need(sha((private/'PUBLIC_MANIFEST.json').read_bytes())==family['prior_public_manifest_sha256'],'private prior manifest')
  need(sha((public/'PUBLIC_MANIFEST.json').read_bytes())==family['current_public_manifest_sha256'],'current manifest')
  amendment=js(public/'PUBLIC_PATH_AMENDMENT.json')
  need(sha((public/'PUBLIC_PATH_AMENDMENT.json').read_bytes())==family['parent_amendment_sha256'],'amendment pin')
  need(amendment['math_or_format_checks_rerun'] is False and amendment['auditor_code_or_original_source_changed'] is False,'amendment scope')
  for r in family['receipts']:
   raw=(private/r['path']).read_bytes();new=(public/r['path']).read_bytes()
   need(len(raw)==r['original_bytes'] and sha(raw)==r['original_sha256'],'raw receipt pins')
   need(len(new)==r['public_bytes'] and sha(new)==r['public_sha256'],'new receipt pins')
   x=json.loads(raw);y=json.loads(new)
   extra=set(y)-set(x);need(extra=={'publication_metadata_redaction'},'only explicit descriptor added')
   descriptor=y.pop('publication_metadata_redaction')
   need(sorted(diffs(x,y))==sorted(r['changed_json_pointers']),'only declared typed changes')
   need(descriptor['original_json_bytes']==len(raw) and descriptor['original_json_sha256']==sha(raw),'descriptor raw pins')
   rows.append({'family':name,'path':r['path'],'changed_json_pointers':r['changed_json_pointers'],'original_bytes':len(raw),'original_sha256':sha(raw),'public_bytes':len(new),'public_sha256':sha(new),'all_other_typed_fields_unchanged':True})
  before=(private/'REPORT.md').read_text();after=(public/'REPORT.md').read_text();need(after.startswith(before),'report preserves raw body')
  logbefore=(private/'RESEARCH_LOG.md').read_text();logafter=(public/'RESEARCH_LOG.md').read_text();need(logafter.startswith(logbefore),'research log preserves raw body')
  decision_before=js(private/'DECISION.json');decision_after=js(public/'DECISION.json');am=decision_after.pop('parent_publication_metadata_amendment');need(decision_before==decision_after and am['checks_rerun'] is False and am['verdict_unchanged'] is True,'decision original typed fields preserved')
  for p in private.iterdir():
   if p.name in {r['path'] for r in family['receipts']}|{'PUBLIC_MANIFEST.json','REPORT.md','RESEARCH_LOG.md','DECISION.json'}:continue
   need((public/p.name).read_bytes()==p.read_bytes(),'all other family content unchanged')
 save('RECEIPT_AMENDMENT_CHECKS.json',{'status':'PASS','count':len(rows),'receipts':rows,'amendments_are_parent_authored_presentation_only':True,'original_observations_not_rerun_or_rewritten':True})
def boundary():
 forbidden=[re.compile(rb'/(?:Users|home)/[^/\s"\\]+/'),re.compile(rb'/(?:private/var|var/folders|tmp)/[^\s"\\]+'),re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),re.compile(rb'\bsk-[A-Za-z0-9_-]{24,}\b'),re.compile(rb'\bAKIA[A-Z0-9]{16}\b')]
 matches=[];payloads=[];pdfs=[];images=[];corpora=[]
 def scan(name,raw,depth=0):
  need(depth<5,'unexpected archive nesting')
  payloads.append((name,len(raw),sha(raw)))
  for i,pattern in enumerate(forbidden):
   if pattern.search(raw):matches.append({'path':name,'pattern_index':i})
  if raw.startswith(b'%PDF-'):pdfs.append({'path':name,'bytes':len(raw),'sha256':sha(raw)})
  if raw.startswith((b'\x89PNG\r\n\x1a\n',b'\xff\xd8\xff',b'GIF87a',b'GIF89a')):images.append(name)
  if Path(name).name in {'catalog.json','problems.json','research_results.json','whole_record.json','whole_report.json'}:corpora.append(name)
  if raw.startswith(b'PK\x03\x04'):
   with zipfile.ZipFile(io.BytesIO(raw)) as z:
    for n in z.namelist():
     need(not n.startswith('/') and '..' not in Path(n).parts,'recursive zip unsafe name')
     scan(name+'!/'+n,z.read(n),depth+1)
 for p in sorted(ROOT.rglob('*')):
  if p.is_file():scan(p.relative_to(ROOT).as_posix(),p.read_bytes())
 need(not matches,'private path or credential match')
 note=sha((ROOT/'preprint/output/pdf/note.pdf').read_bytes())
 need(all(r['sha256']==note for r in pdfs),'third-party PDF bytes')
 need(not images and not corpora,'render or whole-corpus artifact')
 save('PUBLIC_BOUNDARY_CHECKS.json',{'status':'PASS','public_payload_occurrences_scanned_including_nested_archives':len(payloads),'total_bytes_scanned_with_duplicates':sum(p[1] for p in payloads),'path_or_credential_matches':matches,'pdf_occurrences':pdfs,'render_image_occurrences':images,'raw_named_corpus_occurrences':corpora,'scope':'Recursive complete-byte and filename inspection plus direct AI-agent reading of governing documents; bounded ordinary publication hygiene, not a hostile security guarantee.'})
def editions():
 paths=list((A/'private_sources').glob('*.pdf'))+list((A/'priority_classical_01/private_sources').glob('*.pdf'))+list((A/'priority_current_01/private_sources').glob('*.pdf'))
 found={};rows=[]
 for p in paths:
  raw=p.read_bytes();h=sha(raw)
  if h in found:found[h].append(p.name);continue
  found[h]=[p.name]
  t=subprocess.run(['pdftotext','-layout',str(p),'-'],capture_output=True,check=True).stdout
  txt=p.with_suffix('.txt');same=None
  if txt.exists():same=(txt.read_bytes()==t);need(same,'fresh source extraction differs '+p.name)
  rows.append({'name':p.name,'bytes':len(raw),'sha256':h,'pages':t.count(b'\f'),'fresh_layout_text_sha256':sha(t),'existing_layout_text_identical':same})
 need(len(rows)==17,'seventeen distinct editions')
 rootv1=(A/'private_sources/1405.7566v1-root.pdf').read_bytes();ownv1=(A/'priority_classical_01/private_sources/1405.7566v1.pdf').read_bytes();need(rootv1==ownv1,'root v1 duplicate')
 rootkm=(A/'private_sources/km2025-final-root.pdf').read_bytes();ownkm=(A/'priority_current_01/private_sources/khezeli_mellick_alea_2025_final.pdf').read_bytes();need(rootkm==ownkm,'root final duplicate')
 save('SOURCE_EDITION_CHECKS.json',{'status':'PASS','distinct_pdf_editions':17,'root_extra_copies_are_duplicates':True,'editions':rows,'inspection_limit':'Authentication/fresh extraction of entire editions is not exhaustive proof reading. All operative current-note credit bodies were read directly; descendants are bounded relevant-body screens. No source PDF or text redistributed.'})
def queue():
 commit='83a9565aa3588dc33abbc293e9f416d1da422bc6';pfx='unsolved_math_prioritization/attempts/9900008/'
 def git(*args):return subprocess.run(['git',*args],cwd=REPO,capture_output=True,check=True).stdout.decode()
 changed=git('diff','--name-only','d63ecaa40b535e5caa4d491dcd51a9bc3e36ff3e',commit).splitlines();need(set(changed)=={pfx+p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}|{'unsolved_math_prioritization/QUEUE.md'},'only244 and queue changed')
 old=git('show','d63ecaa40b535e5caa4d491dcd51a9bc3e36ff3e:unsolved_math_prioritization/QUEUE.md').splitlines();new=git('show',commit+':unsolved_math_prioritization/QUEUE.md').splitlines()
 oldtarget=[s for s in old if '9900008' in s];target=[s for s in new if '9900008' in s]
 need(len(target)==len(oldtarget)==1,'unique target queue')
 need([s for s in old if s not in oldtarget]==[s for s in new if s not in target],'all other queue lines unchanged')
 cells=[c.strip() for c in target[0].split('|')];need('claimed_solved' in cells and '1/5' in cells,'literal status effort')
 need(not re.search(r'10\.[0-9]{4,9}/',target[0]),'blank DOI')
 save('PREPARED_OBJECT_QUEUE_CHECK.json',{'status':'PASS','commit':commit,'changed_candidate_files':244,'one_target_queue_row_only':True,'target_queue_line':target[0],'exact_status':'claimed_solved','original_effort':'1/5','doi_blank':True,'read_only_actual_local_git_objects':True,'live_remote_gate_performed':False})
def exact_math():
 q=0;unique=[]
 for a,b in itertools.product(range(4),repeat=2):
  out=[0]*4;out[a]+=1;out[b]+=2
  if out==[1,2,0,0]:unique.append([a,b])
  q+=1
 need(unique==[[0,1]],'unequal quotient')
 equal=[]
 for a,b in itertools.product(range(4),repeat=2):
  out=[0]*4;out[a]+=1;out[b]+=1
  if out==[1,1,0,0]:equal.append([a,b])
 need(equal==[[0,1],[1,0]],'equal quotient boundary')
 windows=0
 def ceil(x):return -((-x.numerator)//x.denominator)
 for height in (1,2,3,7):
  for den in range(1,37):
   for num in range(den):
    u=F(num,den)*height
    lines=[(F(k)+offset,w) for offset,w in [(F(0),F(1)),(F(1,2),F(2))] for k in range(ceil(-u-offset),ceil(height-u-offset))]
    need(sum(w for y,w in lines)==3*height,'window total')
    need(sum(w for y,w in lines if y%1==F(1,2))==2*height,'window heavy mass');windows+=1
 intervals=0
 for den in range(1,25):
  for j in range(den):
   lo,hi=F(j,den),F(j+1,den)
   overlap=lambda a,b,c,d:max(F(0),min(b,d)-max(a,c))
   # Heavy displacement is +1/2 on U2 in [0,1/2), and -1/2 on [1/2,1).
   heavy=F(2,3)*(overlap(F(0),F(1,2),lo-F(1,2),hi-F(1,2))+overlap(F(1,2),F(1),lo+F(1,2),hi+F(1,2)))
   light=F(1,3)*(hi-lo)
   need(heavy==F(2,3)*(hi-lo) and light==F(1,3)*(hi-lo),'joint interval law');intervals+=1
 matrix=((F(0),F(1)),(F(1,2),F(1,2)))
 need([matrix[0][i]+2*matrix[1][i] for i in range(2)]==[1,2],'Markov balance')
 save('INDEPENDENT_EXACT_CHECKS.json',{'status':'PASS','quotient_label_pairs':q,'unique_unequal_preserving_labels':unique,'equal_weight_labels':equal,'endpoint_including_windows':windows,'full_joint_output_interval_pairs':intervals,'heavy_root_probability':'2/3','markov_balance':True,'limits':'Finite exact diagnostics corroborate analytic mechanisms; they cannot establish universal measurable claims. Equal-weight half-period phases are the same observed measure.'})
if __name__=='__main__':
 repair();boundary();editions();queue();exact_math();print('PASS evidence, recursive boundary, editions, prepared queue, independent exact diagnostics')
