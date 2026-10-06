#!/usr/bin/env python3
from pathlib import Path
import shutil,subprocess,sys,hashlib,json,datetime,concurrent.futures
p=Path(__file__).resolve().parent;b=p.parent;s=b/'repaired_snapshot/unsolved_math_prioritization/attempts/30004047';d=p/'private_replay';d.mkdir(exist_ok=True);dst=d/'candidate';shutil.copytree(s,dst,dirs_exist_ok=True)
sources=d/'sources';sources.mkdir(exist_ok=True)
for old,new in [('owr.pdf','OWR_2019_1.pdf'),('ejc.pdf','Concatenating_published_2022.pdf')]:shutil.copyfile(p/'raw_primary'/old,sources/new)
tasks=[('packet_source',[sys.executable,str(dst/'verify_packet.py'),'--source-dir',str(sources)]),('publication_source',[sys.executable,str(dst/'verify_publication.py'),'--source-dir',str(sources)]),('publication_sourcefree',[sys.executable,str(dst/'verify_publication.py')]),('historical_independent',[sys.executable,str(dst/'review/independent_check.py')])]+[(f'turn{i}',[sys.executable,str(dst/f'check_turn_{i}.py')]) for i in range(1,6)]
def run(t):
 name,cmd=t;start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(cmd,cwd=dst,capture_output=True);(p/(name+'.stdout')).write_bytes(r.stdout);(p/(name+'.stderr')).write_bytes(r.stderr)
 v={'name':name,'command':cmd,'exit_code':r.returncode,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout_bytes':len(r.stdout),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_bytes':len(r.stderr),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()};assert r.returncode==0,(name,r.stderr)
 return v
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,tasks))
for i in range(1,6):assert (p/f'turn{i}.stdout').read_bytes()==(dst/f'TURN_{i}_CHECKS.json').read_bytes()
assert (p/'historical_independent.stdout').read_bytes()==(dst/'review/INDEPENDENT_CHECKS.json').read_bytes()
current=json.loads((p/'packet_source.stdout').read_text());hist=json.loads((dst/'FINAL_REPLAY.json').read_text());old=json.loads((dst/'review/AUTHOR_REPLAY.json').read_text());assert current==old and current['replays']==hist['replays'];assert current['all_file_bindings']==67 and hist['all_file_bindings']==29
sourcebytes=(p/'publication_source.stdout').read_bytes();assert sourcebytes.startswith((p/'packet_source.stdout').read_bytes());assert sourcebytes.endswith(b'PASS: preserved author/review bytes, 12967236 author and 30053 independent assertions; original unsolved 5/5\n')
free=(p/'publication_sourcefree.stdout').read_text();freej=json.JSONDecoder().raw_decode(free)[0];assert freej['source_pdfs_checked']==0 and freej['all_file_bindings']==65 and freej['replays']==hist['replays']
print(json.dumps({'runs':results,'all_per_turn_receipts_byte_equal':True,'historical_independent_byte_equal':True,'current_source_packet_equals_frozen_review_author_replay':True,'historical_aggregate_equality_not_asserted':True,'historical_binding_count':29,'current_source_binding_count':67,'current_sourcefree_binding_count':65,'sourcefree_is_not_raw_source_certification':True},indent=2))
