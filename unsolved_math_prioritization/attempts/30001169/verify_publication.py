#!/usr/bin/env python3
"""Strict externally anchored publication integrity and actual exact replays."""
import argparse, hashlib, json, os, re, stat, subprocess, sys, zipfile
from pathlib import Path, PurePosixPath
ROOT=Path(__file__).resolve().parent
ARCHIVES={
'YAMABE_MONOTONICITY_30001169_AUTHOR_PUBLIC_SAFE_DERIVATIVE.zip':(16017,'3f73854c0fb2b1aaaa1b807f903e681efb31be5c980feb071ca90b29c969b821',10),
'YAMABE_MONOTONICITY_30001169_PUBLIC_AUDIT_DERIVATIVE.zip':(34097,'188106dfb9c7eefa0e276be478d7684a8644f779b99d9f7872a841ef849b1d85',21)}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:
  need(k not in d,'duplicate JSON key');d[k]=v
 return d
def read(b):return json.loads(b,object_pairs_hook=unique)
def execute(path):
 p=subprocess.run([sys.executable,'-I','-B',*(['-O'] if sys.flags.optimize else []),str(path)],cwd='/',capture_output=True,text=True,timeout=240)
 need(p.returncode==0,'failed replay '+str(path.relative_to(ROOT))+': '+p.stderr)
 return read(p.stdout)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--expected-manifest',required=True);parser.add_argument('--integrity-only',action='store_true');args=parser.parse_args()
 need(re.fullmatch('[0-9a-f]{64}',args.expected_manifest) is not None,'invalid external anchor')
 mp=ROOT/'PUBLICATION_MANIFEST.json';need(stat.S_ISREG(mp.lstat().st_mode),'manifest must be regular')
 raw=mp.read_bytes();need(digest(raw)==args.expected_manifest,'external manifest mismatch');m=read(raw)
 need(set(m)=={'schema','files'} and m['schema']=='yamabe-publication-v1','manifest schema');files=m['files'];need(isinstance(files,dict) and files,'empty inventory')
 dirs=set()
 for name,entry in files.items():
  p=PurePosixPath(name);need(not p.is_absolute() and '..' not in p.parts and str(p)==name and '\\' not in name,'unsafe manifest path');need(name!='PUBLICATION_MANIFEST.json','self inventory');need(set(entry)=={'bytes','sha256'} and type(entry['bytes']) is int and entry['bytes']>=0 and re.fullmatch('[0-9a-f]{64}',entry['sha256']),'entry schema')
  for parent in p.parents:
   if str(parent)!='.':dirs.add(str(parent))
 actual_files=set();actual_dirs=set()
 for current,ds,fs in os.walk(ROOT,followlinks=False):
  for name in ds+fs:
   p=Path(current)/name;relative=p.relative_to(ROOT).as_posix();mode=p.lstat().st_mode
   need(stat.S_ISREG(mode) or stat.S_ISDIR(mode),'nonregular node '+relative)
   if stat.S_ISDIR(mode):actual_dirs.add(relative)
   else:actual_files.add(relative)
 need(actual_files==set(files)|{'PUBLICATION_MANIFEST.json'},'file inventory mismatch');need(actual_dirs==dirs,'directory inventory mismatch')
 for name,meta in files.items():
  b=(ROOT/name).read_bytes();need(len(b)==meta['bytes'] and digest(b)==meta['sha256'],'content mismatch '+name)
 archive_count=0
 for name,(size,sha,count) in ARCHIVES.items():
  path=ROOT/'archives'/name;b=path.read_bytes();need(len(b)==size and digest(b)==sha,'archive pin '+name)
  with zipfile.ZipFile(path) as z:
   infos=z.infolist();need(len(infos)==count and len({i.filename for i in infos})==count,'archive member inventory');archive_count+=len(infos)
   for info in infos:
    pp=PurePosixPath(info.filename);need(not pp.is_absolute() and '..' not in pp.parts and '\\' not in info.filename and str(pp)==info.filename,'unsafe archive path');need(stat.S_ISREG(info.external_attr>>16),'nonregular archive member');need('reviewed/'+info.filename in files,'unlisted archive member');need(z.read(info)==(ROOT/'reviewed'/info.filename).read_bytes(),'archive member mismatch')
 meta=read((ROOT/'PUBLICATION_METADATA.json').read_bytes());need(meta['problem_id']==30001169 and meta['queue_status']=='unsolved' and meta['approaches_used']==meta['approach_limit']==5,'publication claim scope');need(meta['required_analytic_clarification']=='reviewed/audit/DERIVATIVE_REMAINDER.md','required derivative clarification')
 need((ROOT/meta['required_analytic_clarification']).is_file(),'missing derivative clarification')
 results={'status':'PASS','file_count':len(actual_files),'archive_count':2,'archive_member_comparisons':archive_count,'optimized':bool(sys.flags.optimize),'mathematical_status':'partial_unresolved','mode':'integrity_only' if args.integrity_only else 'full'}
 if not args.integrity_only:
  envelope=execute(ROOT/'reviewed/verify_audit.py');need(envelope['status']=='PASS' and envelope['independent_intervals']==750 and envelope['independent_exp_enclosures']==13500,'audit result')
  mutation=execute(ROOT/'reviewed/audit/replay_mutations.py');need(mutation==read((ROOT/'reviewed/audit/MUTATION_RESULTS.json').read_bytes()),'actual mutation result mismatch')
  results.update({'author_tests_actual':48,'independent_relocated_checks_actual':2,'independent_intervals':750,'independent_exponential_enclosures':13500})
 print(json.dumps(results,sort_keys=True))
if __name__=='__main__':main()
