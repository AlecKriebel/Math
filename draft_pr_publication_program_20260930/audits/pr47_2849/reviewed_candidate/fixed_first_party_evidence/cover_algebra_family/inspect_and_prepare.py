#!/usr/bin/env python3
"""Full first-party input read and private unchanged helper preparation."""
import hashlib,json,re
from pathlib import Path
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parent;PARENT=BASE.parent;SRC=PARENT/'source_snapshot'
def entry(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'full_mode':p.stat().st_mode&0o7777}
files=sorted(p for p in SRC.rglob('*') if p.is_file());assert len(files)==16
jsons={p.relative_to(SRC).as_posix():json.loads(p.read_bytes()) for p in files if p.suffix=='.json'}
texts={p.relative_to(SRC).as_posix():p.read_text() for p in files if p.suffix!='.json'}
diff=(PARENT/'original_diff.patch').read_bytes();chunks=diff.split(b'diff --git ')[1:];assert len(chunks)==17
rebuilt=[]
for part in chunks:
 lines=part.splitlines(keepends=True);plus=next(x for x in lines if x.startswith(b'+++ ')).decode().strip()[6:]
 if '/attempts/2849/' not in plus:continue
 rel=plus.split('/attempts/2849/',1)[1]
 in_hunk=False;out=b''
 for line in lines:
  if line.startswith(b'@@ '):in_hunk=True;continue
  if in_hunk and line.startswith(b'+'):out+=line[1:]
 assert out==(SRC/rel).read_bytes(),rel
 rebuilt.append(rel)
assert len(rebuilt)==16
turn=jsons['turns.json'];assert turn['count']==1 and len(turn['attempts'])==1
assert (SRC/'prior_report.json').read_bytes()==b'null\n' and jsons['prior_report.json'] is None
selected=json.loads((PARENT/'ORIGINAL_SELECTED_NATIVE_SOURCE_READ.json').read_bytes())
assert selected['upstream_report_key_presence']=='ABSENT'
assert selected['complete_selected_prior_report']=={} and selected['original_prior_report_file_value'] is None
assert selected['original_vs_native_prior_JSON_equal'] is False
assert selected['complete_selected_problem']==jsons['source_record.json']
preparation=json.loads((PARENT/'ORIGINAL_PREPARATION_MANIFEST.json').read_bytes())
complete=json.loads((PARENT/'ORIGINAL_COMPLETE_READ_RECEIPT.json').read_bytes())
native=json.loads((PARENT/'ORIGINAL_CURRENT_NATIVE_SELECTED_READ.json').read_bytes())
binding=json.loads((PARENT/'original_native_input_bindings.json').read_bytes())
metadata=json.loads((PARENT/'original_pr_metadata.json').read_bytes())
assert metadata['head']=='487327b2412c436ae69e8c52bf353a9a1fb7594e'
assert metadata['changed_files']==17 and metadata['original_declared_turns']=='1/5'
assert jsons['verification.json']['assertions']==len(jsons['verification.json']['checks'])==114
assert len(jsons['review/independent_results.json']['checks'])==jsons['review/independent_results.json']['passed']==100
replay=BASE/'private_replays';replay.mkdir()
for label,path in [('author',SRC/'verify.py'),('submitted',SRC/'review/submitted_verify.py'),('old_independent',SRC/'review/independent_checks.py')]:
 d=replay/label;d.mkdir();(d/path.name).write_bytes(path.read_bytes())
 assert (d/path.name).read_bytes()==path.read_bytes()
report={'read_utc':datetime.now(timezone.utc).isoformat(),'all_science_files': [entry(p) for p in files],'complete_science_json_values':jsons,'whole_diff':entry(PARENT/'original_diff.patch'),'whole17_diff_hunks_read':17,'all16_added_hunks_reconstructed':rebuilt,'all_texts_read_character_counts':{n:len(v) for n,v in texts.items()},'turn_count':turn,'prior_report_literal':'null\n','upstream_key':'ABSENT','raw_fallback':{},'not_equal':True,'native_current_selected_read':native,'original_read_receipt_sha256':entry(PARENT/'ORIGINAL_COMPLETE_READ_RECEIPT.json')['sha256'],'original_preparation_manifest_sha256':entry(PARENT/'ORIGINAL_PREPARATION_MANIFEST.json')['sha256'],'native_bindings_sha256':entry(PARENT/'original_native_input_bindings.json')['sha256'],'acceptance_verdict':None,'old_PASS_not_transferred':True}
(BASE/'FULL_READ_AND_PREPARATION_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'science_files':len(files),'whole_diff_bytes':len(diff),'whole_diff_sha256':hashlib.sha256(diff).hexdigest(),'changed_files':len(chunks),'turns':turn['count'],'prior_literal_null':True,'raw_report_key_ABSENT':True,'raw_fallback':{},'native_selected':native},indent=2))
