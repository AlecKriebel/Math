#!/usr/bin/env python3
"""Authenticate this file externally before use; supply a separately trusted manifest pin."""
import argparse, hashlib, io, json, math, os, re, stat, subprocess, sys, tempfile, zipfile
from pathlib import Path, PurePosixPath

AUTHOR = ('AUTHOR_FREEZE.zip','EXTERNAL_TRUST.json','REPLAY_RECEIPT.json','freeze/bootstrap.py','freeze/AUTHOR_MANIFEST.json','freeze/packet/CLAIMS.json','freeze/packet/EXPECTED.json','freeze/packet/GATE.json','freeze/packet/README.md','freeze/packet/REPORT.md','freeze/packet/SOURCES.json','freeze/packet/run_controls.py','freeze/packet/verify_math.py')
AUDIT = ('AUDIT_MANIFEST.json','AUDIT_FREEZE.zip','EXTERNAL_AUDIT_TRUST.json','public/ACCEPTANCE.json','public/AUDIT.md','public/AUTHOR_CONTROLS_REPLAY.json','public/AUTHOR_PIN_VERIFICATION.json','public/INDEPENDENT_DIAGNOSTICS.json','public/INDEPENDENT_REPLAY.json','public/PUBLIC_ALLOWLIST.json','public/SOURCE_INSPECTION.json','public/independent_checks.py','public/replay_independent.py')
EXTRAS = {'README.md','RESEARCH_LOG.md','PUBLICATION_ACCEPTANCE.json','verify_publication.py','test_publication.py'}
FILES = {'original/'+p for p in AUTHOR} | {'independent_audit/'+p for p in AUDIT} | EXTRAS
PINS = {
 'original/AUTHOR_FREEZE.zip':(19310,'d69db2bf1a7cf84b8c366e7c4a4dc31b1049acafd3840b70222308da801161dd'),
 'original/freeze/bootstrap.py':(3606,'811328f9f6635891f369a850602d191ae3a48ecec95ac2f2db85cab7556d6a9b'),
 'original/freeze/AUTHOR_MANIFEST.json':(1339,'40ab15f865b6965782024a310c3b1dd17fe9b53a2343b1f41980e376d61aa438'),
 'independent_audit/AUDIT_FREEZE.zip':(17263,'be8c0d8e449df0533f7308c2974fb65ed11a152ba96f3c579819e4f9104802e1'),
 'independent_audit/AUDIT_MANIFEST.json':(1694,'43008cc8589fa844811ef9e396dac469947adf21710173f8d2742a3183c5bb1d'),
 'independent_audit/public/AUDIT.md':(12912,'45ae2209244980f5cf58c3360187ade2176019c0b9039dc371044d3ac718fd41')}
HEX = re.compile(r'[0-9a-f]{64}')
class Rejected(Exception): pass
def need(ok,message):
 if not ok: raise Rejected(message)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def unique(pairs):
 out={}
 for k,v in pairs:
  need(k not in out,'duplicate JSON key');out[k]=v
 return out
def bad(value): raise Rejected('nonfinite JSON: '+value)
def finite(value):
 n=float(value);need(math.isfinite(n),'nonfinite numeric overflow');return n
def load(raw): return json.loads(raw,object_pairs_hook=unique,parse_constant=bad,parse_float=finite)
def regular(path):
 need(stat.S_ISREG(path.lstat().st_mode),'nonregular or symlink: '+str(path));return path.read_bytes()
def integer(value,want=None): return type(value) is int and value >= 0 and (want is None or value == want)
def safe(name):
 return type(name) is str and bool(name) and all(re.fullmatch(r'[A-Za-z0-9_.-]+',p) and p not in ('.','..') for p in name.split('/'))
def entries(records):
 need(type(records) is list and bool(records),'inventory list required');out={}
 for e in records:
  need(type(e) is dict and set(e)=={'path','bytes','sha256'},'file record keys')
  need(safe(e['path']) and e['path'] not in out,'unsafe or duplicate path')
  need(integer(e['bytes']),'exact integer byte count required')
  need(type(e['sha256']) is str and HEX.fullmatch(e['sha256']) is not None,'digest syntax')
  out[e['path']]=(e['bytes'],e['sha256'])
 return out
def check_bytes(root,records):
 for name,(size,digest) in records.items():
  b=regular(root/name);need(len(b)==size and sha(b)==digest,'byte mismatch: '+name)
def inventory(root,names):
 need(stat.S_ISDIR(root.lstat().st_mode),'real packet directory required')
 expected_dirs={str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'}
 files=set();dirs=set()
 for here,subdirs,children in os.walk(root,followlinks=False):
  for n in subdirs+children:
   p=Path(here)/n;mode=p.lstat().st_mode;name=p.relative_to(root).as_posix()
   if stat.S_ISDIR(mode):dirs.add(name)
   else:need(stat.S_ISREG(mode),'symlink/special file rejected: '+name);files.add(name)
 need(files==names and dirs==expected_dirs,'exact file/directory inventory mismatch')
def archive(root,archive_name,names):
 with zipfile.ZipFile(io.BytesIO(regular(root/archive_name))) as z:
  infos=z.infolist();need(len(infos)==len(names) and {i.filename for i in infos}==set(names),'archive inventory mismatch')
  for i in infos:
   need(safe(i.filename) and not i.is_dir() and i.flag_bits & 1 == 0,'unsafe archive entry')
   mode=i.external_attr >> 16;need(stat.S_IFMT(mode) in (0,stat.S_IFREG),'archive symlink/special entry')
   b=regular(root/i.filename);need(i.file_size==len(b) and z.read(i)==b,'archive/extracted equality: '+i.filename)
def verify(root,pin):
 need(type(pin) is str and HEX.fullmatch(pin) is not None,'external SHA-256 required')
 inventory(root,FILES|{'PUBLICATION_MANIFEST.json'})
 raw=regular(root/'PUBLICATION_MANIFEST.json');need(sha(raw)==pin,'external publication manifest pin mismatch')
 m=load(raw)
 need(type(m) is dict and set(m)=={'schema','problem_id','rank','status','turns','new_mathematical_approaches','zero_outputs_allowed','formal_proof_claimed','source_files_redistributed','files'},'publication schema keys')
 need(m['schema']=='mesh-preserver-publication-v1','schema identity')
 need(integer(m['problem_id'],2200009) and integer(m['rank'],1030),'target exact integers')
 need(type(m['status']) is str and m['status']=='already_solved' and type(m['turns']) is str and m['turns']=='0/5','disposition')
 need(integer(m['new_mathematical_approaches'],0),'approach exact integer')
 need(m['zero_outputs_allowed'] is True and m['formal_proof_claimed'] is False and m['source_files_redistributed'] is False,'scope booleans')
 records=entries(m['files']);need(set(records)==FILES,'allowlisted manifest paths');check_bytes(root,records);check_bytes(root,PINS)
 al=load(regular(root/'independent_audit/public/PUBLIC_ALLOWLIST.json'))
 need(set(al['allowed_original_author_artifacts'])==set(AUTHOR),'author allowlist mismatch')
 need(set(al['allowed_audit_envelopes'])|{'public/'+p for p in al['allowed_audit_payloads']}==set(AUDIT),'audit allowlist mismatch')
 for folder,manifest,payload,keys,schema,count in [
  ('original','freeze/AUTHOR_MANIFEST.json','freeze/packet',{'schema','problem_id','disposition','new_mathematical_approaches','files'},'mesh-preserver-author-manifest-v1',8),
  ('independent_audit','AUDIT_MANIFEST.json','public',{'audit_status','files','problem_id','schema'},'mesh-preserver-independent-audit-manifest-v1',10)]:
  inner=load(regular(root/folder/manifest));need(type(inner) is dict and set(inner)==keys,'frozen schema keys')
  need(inner['schema']==schema and integer(inner['problem_id'],2200009),'frozen identity')
  if folder=='original':need(inner['disposition']=='previously_solved' and integer(inner['new_mathematical_approaches'],0),'frozen author disposition')
  else:need(inner['audit_status']=='PASS','frozen audit disposition')
  e=entries(inner['files']);need(len(e)==count and all('/' not in n for n in e),'frozen inventory schema');check_bytes(root/folder/payload,e);inventory(root/folder/payload,set(e))
 archive(root/'original','AUTHOR_FREEZE.zip',set(AUTHOR)-{'AUTHOR_FREEZE.zip','EXTERNAL_TRUST.json'})
 archive(root/'independent_audit','AUDIT_FREEZE.zip',set(AUDIT)-{'AUDIT_FREEZE.zip','EXTERNAL_AUDIT_TRUST.json'})
 for p in root.rglob('*.json'):load(regular(p))
 acceptance=load(regular(root/'PUBLICATION_ACCEPTANCE.json'))
 need(acceptance=={'schema':'mesh-preserver-current-acceptance-v1','problem_id':2200009,'rank':1030,'status':'already_solved','turns':'0/5','independent_audit':'PASS','historical_flags_preserved':True,'new_mathematical_approaches':0,'zero_outputs_allowed':True,'nonzero_only_condition':'degree(T(F_m)) = m','universal_theorem':'Leake-Ryder arXiv:1712.02499v1 Theorem 1.4','formal_proof_claimed':False,'novelty_claimed':False,'source_pdf_verification':'NOT_RUN','corpus_verification':'NOT_RUN','hosted_ci':'NOT_RUN'},'current acceptance scope')
 for k in ['problem_id','rank','new_mathematical_approaches']:need(type(acceptance[k]) is int,'acceptance exact integer')
 for k in ['historical_flags_preserved','zero_outputs_allowed','formal_proof_claimed','novelty_claimed']:need(type(acceptance[k]) is bool,'acceptance exact boolean')
 return len(records)
def replay(root):
 need(os.getuid()!=0 and os.geteuid()!=0,'genuinely nonroot execution required')
 results=[]
 with tempfile.TemporaryDirectory(prefix='mesh-publication-replay-') as td:
  for mode in ('normal','-O','-OO'):
   flags=[] if mode=='normal' else [mode]
   def run(script,args=()):
    p=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/script),*args],cwd=td,capture_output=True,timeout=600)
    need(p.returncode==0 and not p.stderr,'diagnostic failure '+script+': '+p.stderr.decode(errors='replace'));return load(p.stdout),p.stdout
   a,raw=run('original/freeze/bootstrap.py')
   need(a['status']=='PASS' and a['independent_review']=='pending' and integer(a['payload_files'],8),'author bootstrap output')
   x,out=run('independent_audit/public/independent_checks.py')
   need(out==regular(root/'independent_audit/public/INDEPENDENT_DIAGNOSTICS.json') and integer(x['total_checks'],12339) and integer(x['sturm_nontrivial_cases'],35),'independent output mismatch')
   results.append({'mode':mode,'author_checks':8829,'independent_checks':12339,'nontrivial_sturm_cases':35,'author_bootstrap_sha256':sha(raw),'independent_output_sha256':sha(out)})
  controls,out=run('original/freeze/packet/run_controls.py')
  recorded=load(regular(root/'original/REPLAY_RECEIPT.json'))
  for k in ('uid','euid'):recorded[k]=controls[k];need(integer(controls[k]) and controls[k]!=0,'nonroot receipt')
  need(controls==recorded,'author hostile/read-only controls mismatch')
  independent,out=run('independent_audit/public/replay_independent.py')
  recorded=load(regular(root/'independent_audit/public/INDEPENDENT_REPLAY.json'))
  for k in ('uid','euid'):recorded[k]=independent[k];need(integer(independent[k]) and independent[k]!=0,'nonroot independent receipt')
  need(independent==recorded,'independent read-only replay mismatch')
 return results
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--packet',type=Path,default=Path(__file__).absolute().parent);p.add_argument('--manifest-sha256',required=True);p.add_argument('--check-only',action='store_true');a=p.parse_args()
 try:
  root=a.packet.absolute();count=verify(root,a.manifest_sha256);results=[] if a.check_only else replay(root);verify(root,a.manifest_sha256)
  print(json.dumps({'schema':'mesh-preserver-publication-replay-v1','status':'PASS','files_verified':count+1,'uid':os.getuid(),'euid':os.geteuid(),'check_only':a.check_only,'replays':results,'source_pdf_verification':'NOT_RUN','corpus_verification':'NOT_RUN','hosted_ci':'NOT_RUN'},sort_keys=True,indent=2));return 0
 except (Rejected,OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError,zipfile.BadZipFile) as e:
  print('REJECT: '+str(e),file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
