#!/usr/bin/env python3
"""Relocatable, fail-closed integrity and exact-calculation replay; not a geometry proof."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
PINS={
 'author/AUTHOR_MANIFEST.json':'5968a1f89b3e1c738a2a9981db6005e0df401cab99a718d3b59d8617e5b6aaf5',
 'independent_audit/AUDIT_MANIFEST.json':'511eefcc9c8bed7e29b0063df45a3da55c05ea6e5c5cfd6105b3ee29b2c839c8',
 'independent_audit/INPUT_BINDING.json':'1212233f18b263f696a74129a6416fef975813650c442775b46448dd2cbd6dc6',
}
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def run(name):
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0')
 env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
 return subprocess.check_output([sys.executable,'-B',str(ROOT/name)],cwd=ROOT,env=env)
def main():
 require(sys.version_info>=(3,8),'Python 3.8 or newer required')
 manifest_raw=(ROOT/'PUBLICATION_MANIFEST.json').read_bytes();m=json.loads(manifest_raw)
 require(m['problem_id']=='30002003' and m['queue_status']=='unsolved' and m['turns']=='5/5','Incorrect publication scope')
 records={row['path']:row for row in m['files']}
 require(len(records)==len(m['files'])==21,'Wrong payload count or duplicate entry')
 for name in records:
  p=PurePosixPath(name);require(not p.is_absolute() and '..' not in p.parts and str(p)==name,'Unsafe path')
 for p in ROOT.rglob('*'):
  require(not p.is_symlink(),'Symlink forbidden');require(p.is_file() or p.is_dir(),'Special file forbidden')
 actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
 require(actual==set(records)|{'PUBLICATION_MANIFEST.json'},'Unexpected or missing file')
 require({p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_dir()}=={'author','independent_audit'},'Unexpected directory')
 before={}
 for name,row in records.items():
  raw=(ROOT/name).read_bytes();require(len(raw)==row['bytes'] and digest(raw)==row['sha256'],'Integrity mismatch: '+name);before[name]=raw
 for name,pin in PINS.items():require(digest(before[name])==pin,'Frozen binding mismatch: '+name)
 for dirname,filename in [('author','AUTHOR_MANIFEST.json'),('independent_audit','AUDIT_MANIFEST.json')]:
  inner=json.loads(before[dirname+'/'+filename]); rows=inner['files']
  require(len(rows)==8 and len({r['path'] for r in rows})==8,'Wrong frozen member count')
  require({p.name for p in (ROOT/dirname).iterdir()}=={r['path'] for r in rows}|{filename},'Frozen set differs')
  for row in rows:
   raw=before[dirname+'/'+row['path']];require(len(raw)==row['bytes'] and digest(raw)==row['sha256'],'Frozen payload differs')
 binding=json.loads(before['independent_audit/INPUT_BINDING.json']);original=binding['original_packet']
 require(original['sha256']=='d7b0488b4a95340a72e58954e521432382a69310d86b33ad598862debbd6dc47' and original['bytes']==24648,'Author archive binding differs')
 for row in original['files']:
  require(row['path'].startswith('stringy_30002003/'),'Unexpected original prefix')
  raw=before['author/'+row['path'].split('/',1)[1]]
  require(len(raw)==row['bytes'] and digest(raw)==row['sha256'],'Independent author binding differs')
 status=json.loads(before['PUBLICATION_STATUS.json']);audit=json.loads(before['independent_audit/RESULTS.json'])
 require(status['queue_status']=='unsolved' and status['turns']=='5/5','Wrong queue gate')
 require(status['literal_dataset_statement']=='refuted_by_complete_audited_counterexample','Wrong literal scope')
 require(status['qualified_conjecture']=='unresolved_by_this_work','Wrong qualified scope')
 require(audit['verdict']=='PASS_LITERAL_COUNTEREXAMPLE_WITH_EXPLICIT_SCOPE' and not audit['published_conjecture_disproved'] and not audit['required_mathematical_corrections'],'Audit scope differs')
 require(not status['novelty_certified'] and not status['global_current_openness_certified'] and not status['immutable_dataset_revision_claim'],'Unsupported promotion')
 require(not status['raw_dataset_statement_published'] and not status['computations_are_geometry_proof'],'Unsupported evidence claim')
 require(binding['statement']['decoded_statement_utf8_bytes']==126 and binding['statement']['decoded_statement_sha256']==status['decoded_statement_sha256']=='6e964d979f65113b1582de96738094b9042e96d116451d2b5a7f5c54955074c6','Statement binding differs')
 authored=run('author/verify.py');independent=run('independent_audit/independent_controls.py')
 require(authored==before['author/CHECK_RESULTS.json'],'Author result bytes differ')
 require(independent==before['independent_audit/INDEPENDENT_RESULTS.json'],'Independent result bytes differ')
 a=json.loads(authored);b=json.loads(independent)
 require(a['all_checks_passed'] and a['exact_checks']==321 and a['negative_controls_rejected']==9,'Author counts differ')
 require(b['all_checks_passed'] and b['independent_checks']==32 and b['false_shortcuts_rejected']==10 and not b['geometry_certification'],'Independent counts differ')
 require(all((ROOT/n).read_bytes()==raw for n,raw in before.items()),'Replay modified payload')
 require((ROOT/'PUBLICATION_MANIFEST.json').read_bytes()==manifest_raw,'Replay modified manifest')
 require({p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}==actual,'Replay created files')
 print(json.dumps({'result':'PASS','problem_id':'30002003','queue_status':'unsolved','turns':'5/5','literal_dataset_statement':'refuted','qualified_conjecture':'unresolved_by_this_work','packet_files':22,'frozen_files_preserved':18,'author_replay_byte_equal':True,'independent_replay_byte_equal':True,'author_checks':321,'author_false_shortcuts':9,'independent_checks':32,'independent_false_shortcuts':10,'child_assertions_enabled':True,'geometry_certification':False,'publication_manifest_sha256':digest(manifest_raw)},indent=2,sort_keys=True))
if __name__=='__main__':main()
