#!/usr/bin/python3
"""Read-only family custody checks; does not import or execute math helpers."""
from pathlib import Path
from datetime import datetime
import hashlib,json,stat
ROOT=Path(__file__).resolve().parent
checks=0

def need(v,msg):
 global checks
 checks+=1
 if not v:raise AssertionError(msg)

def load(p):return json.loads(Path(p).read_text())

def row(p):
 p=Path(p);need(not p.is_symlink(),'No symlink file')
 need(stat.S_ISREG(p.stat().st_mode),'Regular file')
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return {'path':str(p),'bytes':p.stat().st_size,'sha256':h.hexdigest(),'mode':format(p.stat().st_mode&0o7777,'04o')}

def contained(p):
 p=Path(p);need(p.is_absolute(),'Absolute owned path')
 need(ROOT==p or ROOT in p.parents,'Owned path confined to this exact family')
 for a in [p]+[x for x in p.parents if x==ROOT or ROOT in x.parents]:need(not a.is_symlink(),'No symlink ancestor')
 return p

def all_files(exclude=()):
 out=[]
 for p in ROOT.rglob('*'):
  need(not p.is_symlink(),'No packet symlinks')
  if p.is_file() and p.name not in exclude:out.append(p)
 return sorted(out)

def all_dirs():return [ROOT]+sorted(p for p in ROOT.rglob('*') if p.is_dir())

def check_external():
 refs=load(ROOT/'EXTERNAL_REFERENCES.json');need(len(refs)==31,'Exact external reference count')
 need(len({r['path'] for r in refs})==len(refs),'Distinct external paths')
 for r in refs:need(row(Path(r['path']))==r,'Exact whole external body/full mode')
 return refs

def check_cap(name,script,inp,expected_pid,resultname,status):
 folder=ROOT/'captures'/name;cap=load(folder/'CAPTURE.json')
 need(cap['schema']=='actual-independent-subprocess-v1','Actual capture schema')
 need(cap['child_pid']==expected_pid and cap['operator_pid']!=cap['child_pid'],'Literal actual child/operator PIDs')
 need(cap['exit_code']==0 and cap['source_after_unchanged'] is True,'Actual success and epoch source stability')
 need(cap['acceptance_authority'] is False,'No acceptance authority')
 need(cap['argv']==['/usr/bin/python3','-B',str(ROOT/script)] and cap['cwd']==str(ROOT),'Exact genuine argv/cwd')
 need(datetime.fromisoformat(cap['ended_at_utc'])>=datetime.fromisoformat(cap['started_at_utc']),'UTC chronology')
 op=(folder/'operator_prelaunch.py').read_bytes();need(hashlib.sha256(op).hexdigest()==cap['operator_sha256'],'Actual prelaunch operator body')
 need(op==(ROOT/'capture_command.py').read_bytes(),'Own operator body preserved')
 need(len(cap['source_prelaunch'])==2,'Code and input separately captured')
 for r,name2 in zip(cap['source_prelaunch'],[script,inp]):
  need(r['path']==str(ROOT/name2),'Literal original input path')
  cp=contained(r['prelaunch_copy']);b=cp.read_bytes()
  need(len(b)==r['size'] and hashlib.sha256(b).hexdigest()==r['sha256'],'Captured prelaunch code/input full bytes')
  need(b==(ROOT/name2).read_bytes(),'Current code/input body equals genuine prelaunch copy')
  need(r['mode']=='0644','Mode at actual math/source capture epoch')
 for key in ['stdout','stderr']:
  p=folder/(key+'.bin');r=cap[key];b=p.read_bytes()
  need(r['path']==str(p) and r['size']==len(b) and r['sha256']==hashlib.sha256(b).hexdigest(),'Whole actual stream')
 need(cap['stderr']['size']==0,'Full stderr is empty')
 result=load(ROOT/resultname);need(result['status']==status,'Own result scope')
 stream=json.loads((folder/'stdout.bin').read_text())
 need(stream['status']==status and stream['require_evaluations']==result['require_evaluations'],'Result matches complete actual stdout')
 return cap

def check_science():
 v=load(ROOT/'VERDICT.json')
 need(v['status']=='PASS_SCOPED_GKZ_COMBINATORIAL_COMPARISON' and v['mandatory_issues']==[],'Scoped mathematical verdict')
 need(v['ROOT_personal_read_claimed'] is False and v['acceptance_authority'] is False,'No future ROOT or acceptance claim')
 need(v['historical_novelty']=='unestablished' and v['current_open_status_certified'] is False,'Priority qualifications')
 cap1=check_cap('independent_polynomial_controls','independent_polynomial_controls.py','independent_input.json',86845,'INDEPENDENT_POLYNOMIAL_RESULTS.json','PASS_FINITE_EXPLICIT_POLYNOMIAL_CONTROLS')
 cap2=check_cap('primary_and_scope','check_primary_and_scope.py','source_input.json',90796,'PRIMARY_AND_SCOPE_RESULTS.json','PASS_PRIMARY_ACQUISITION_AND_LITERAL_SCOPE_CONTROLS')
 p=load(ROOT/'INDEPENDENT_POLYNOMIAL_RESULTS.json');s=load(ROOT/'PRIMARY_AND_SCOPE_RESULTS.json')
 need(p['require_evaluations']==11955 and p['negative_controls']==2,'Exact finite control accounting')
 need(sum(r['generic_heights'] for r in p['univariate'])==800,'Distinct line height tests')
 need(p['cube']['general_generic_heights']==160 and p['cube']['equal_column_generic_perturbations']==64,'Cube control counts')
 need(s['require_evaluations']==78 and s['prior_report']['raw_key']=='ABSENT','Source controls separately counted')
 need(s['prior_report']['SQL_report_literal']=='{}' and s['prior_report']['SQL_is_NULL'] is False,'SQL source precision')
 need(s['original']['claimed_solved_turns']=='1/5' and s['original']['JSONL_entries']==1,'Original turn count preserved')
 need(datetime.fromisoformat(cap1['ended_at_utc'])<datetime.fromisoformat(cap2['started_at_utc']),'Independent math completed before source custody capture')
 return check_external()

def check_prepared():
 index=load(ROOT/'INDEX.json');ready=load(ROOT/'READY.json')
 need(ready['ROOT_closure_executed'] is False and ready['acceptance_authority'] is False,'Prepared only')
 need(ready['index_sha256']==hashlib.sha256((ROOT/'INDEX.json').read_bytes()).hexdigest(),'Prepared index whole-body pin')
 paths=[]
 for r in index['files']:
  p=contained(r['path']);need(row(p)==r,'Prepared whole owned body/full mode');paths.append(p)
 need(set(paths)==set(all_files(('INDEX.json','READY.json','SELF_MANIFEST.json'))),'Exact payload topology')
 need(len(paths)<=58 and sum(r['bytes'] for r in index['files'])<1000000,'Compact file/body limit')
 dirs=[{'path':str(p),'mode':format(p.stat().st_mode&0o7777,'04o')} for p in all_dirs()]
 need(dirs==index['directories'],'Exact directory topology/full modes')
 need(all(r['mode']=='0755' for r in dirs),'Prepared directory mode')
 need(index['external_references']==check_science(),'External references and scientific checks match index')
 return index,ready

def check_closed():
 m=load(ROOT/'SELF_MANIFEST.json');need(m['acceptance_authority'] is False and m['ROOT_personal_read_not_inferred_from_integrity'] is True,'Qualified genuine closure')
 paths=[]
 for r in m['files']:
  p=contained(r['path']);need(row(p)==r and r['mode']=='0444','Closed whole owned body/full mode');paths.append(p)
 need(set(paths)==set(all_files(('SELF_MANIFEST.json',))),'Closed exact topology')
 need(format((ROOT/'SELF_MANIFEST.json').stat().st_mode&0o7777,'04o')=='0444','Manifest full mode')
 dirs=[{'path':str(p),'mode':format(p.stat().st_mode&0o7777,'04o')} for p in all_dirs()]
 need(dirs==m['directories'],'Closed directory topology/modes')
 need(m['external_references']==check_science(),'Closed external references')
 return m
