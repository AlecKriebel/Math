#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--sources',type=Path);a=ap.parse_args();p=a.author.resolve();r=Path(__file__).resolve().parent
pins={'FINAL_AUTHOR_MANIFEST.json':'1c50623aa192f334537774bc34eb71f58128c34b3ca0515996ca3e59e0190d5e','ADDITIVE_MANIFEST.json':'669e634c7d0e3ddac28d34f2f23a0aa916a6793d16bb47f02bb3965cb1261878'}
for n,h in pins.items():
 b=(p/n).read_bytes();assert hashlib.sha256(b).hexdigest()==h
 for e in json.loads(b)['files']:
  x=(p/e['path']).read_bytes();assert len(x)==e['bytes'] and hashlib.sha256(x).hexdigest()==e['sha256']
for e in json.loads((r/'REMOTE_BINDING.json').read_bytes())['all_corrected_tree_files']:
 b=(p/e['path']).read_bytes();assert len(b)==e['bytes'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha']
for e in json.loads((r/'REVIEW_MANIFEST.json').read_bytes())['files']:
 b=(r/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
cmd=[sys.executable,str(p/'REPLAY_ALL.py')]
if a.sources:cmd+=['--sources',str(a.sources.resolve())]
result=json.loads(subprocess.check_output(cmd));assert result['author_assertions']==329914 and result['verified_bindings']==60 and result['all_five_receipts_exact']
b=subprocess.check_output([sys.executable,str(r/'independent_checks.py')]);assert b==(r/'INDEPENDENT_CHECKS.json').read_bytes()
print(json.dumps({'verdict':'PASS_SCOPED_WITH_ADDITIVE_CLARIFICATION','original_status':'unsolved','author_turns':5,'original_files':35,'additive_files':2,'raw_blob_bindings':37,'author_assertions':329914,'independent_assertions':91084,'source_files_checked':result['optional_source_files']},indent=2,sort_keys=True))
