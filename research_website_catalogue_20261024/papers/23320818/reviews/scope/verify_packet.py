#!/usr/bin/env python3
"""Read-only source, reproducibility and final packet verification; stdlib only.
For fresh universal symbolic checks run verify_symbolic_geometry.py separately.
"""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,stat
P=Path(__file__).resolve().parent;S=P.parents[1]/'sources'
checks=0

def require(test,label):
 global checks
 checks+=1
 if not test:raise RuntimeError(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def md5(p):return hashlib.md5(p.read_bytes()).hexdigest()
require(sha(S/'SOURCE_READY.json')=='aeb11ade749cbe2c6147374642fc3fed6c5d88d323dbae59340b3fb8dfbe4535','ready object')
r=json.loads((S/'SOURCE_READY.json').read_text());native=json.loads((S/'record.raw.json').read_text())
require(r['record_id']==23320818 and r['version']=='1.0' and r['publication_date']=='2026-10-12','native version and declared date')
require(r['created']=='2026-10-12T15:30:52.462194+00:00' and r['updated']=='2026-10-12T15:30:54.410145+00:00','native create/update times')
require(r['latest_record_id']==23320818 and r['versions_total_original']==1,'exact latest/version scope')
for a,b in zip(native['files'],r['all_assets_in_original_order']):
 f=Path(b['path']);require(a==b['original_api_file_object'],'entire native asset object and order');require(f.stat().st_size==a['size']==b['bytes'],'asset size');require(a['checksum']=='md5:'+md5(f),'native MD5');require(sha(f)==b['sha256'],'asset SHA256')
seal=json.loads((S/'SOURCE_READY_SEAL.json').read_text());require(sha(S/'SOURCE_READY_MANIFEST.json')==seal['manifest_sha256'],'source manifest seal')
for row in json.loads((S/'SOURCE_READY_MANIFEST.json').read_text())['files']:
 f=S/row['path'];require(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],'original source unchanged '+row['path'])
rows=json.loads((S/'archive-members.json').read_text())['full_original_ordered_regular_occurrences']
require(len(rows)==181 and sum(r['bytes'] for r in rows)==660530,'complete extracted occurrence scope')
with zipfile.ZipFile(S/'regular_zas_bianchi_verification_v1.zip') as z:
 seen=set()
 for row in rows:
  info=z.infolist()[row['ordinal']];name=PurePosixPath(info.filename);canonical='/'.join(name.parts)
  require(not name.is_absolute() and '..' not in name.parts and '\\' not in info.filename and canonical not in seen,'safe canonical member');seen.add(canonical)
  require(not(info.flag_bits&1) and stat.S_IFMT(info.external_attr>>16) in (0,stat.S_IFREG),'regular unencrypted member')
  b=z.read(info);require(hashlib.sha256(b).hexdigest()==row['sha256'] and len(b)==row['bytes'],'native CRC-read member matches extracted binding')
for receipt in json.loads((P/'CURRENT_NATIVE_REPLAY_RECEIPTS.json').read_text()):
 source=S/'published-source/verification/controls'/receipt['name'];output=Path(receipt['stdout_path']);stderr=Path(receipt['stderr_path'])
 require(sha(source)==receipt['source_sha256'],'current replay source');require(sha(output)==receipt['stdout_sha256'],'current replay stdout');require(sha(stderr)==receipt['stderr_sha256'] and not stderr.read_bytes(),'current replay clean stderr');require(receipt['returncode']==0,'current replay exit')
 require(json.loads(output.read_text())==receipt['parsed_output'],'entire current parsed result')
replays=json.loads((P/'CURRENT_NATIVE_REPLAY_RECEIPTS.json').read_text())
for name in ['check_curvature.py','check_geometry.py']:
 a=[r['parsed_output'] for r in replays if r['name']==name];require(len(a)==2 and a[0]==a[1],'normal and optimized exact outputs agree')
own=json.loads((P/'OWN_SYMBOLIC_RECEIPT.json').read_text());require(sha(P/'verify_symbolic_geometry.py')==own['source_sha256'],'own symbolic code binding');require(sha(Path(own['stdout_path']))==own['stdout_sha256'],'own symbolic output binding');require(json.loads(Path(own['stdout_path']).read_text())['symbolic_identities']==56,'all56symbolic identities completed')
for row in json.loads((P/'HISTORICAL_SOURCE_RECONCILIATION.json').read_text())['exact_historical_files']:
 f=Path(row['frozen_path']);require(sha(f)==row['sha256'] and f.stat().st_size==row['bytes'],'historical payload unchanged')
for bundle in ['PRIMARY_FETCH_RECEIPTS.json']:
 for row in json.loads((P/bundle).read_text())['requests_in_declared_order']:
  f=Path(row['path']);require(sha(f)==row['sha256'] and f.stat().st_size==row['bytes'],'primary body custody')
owr=json.loads((P/'OWR_FETCH_RECEIPT.json').read_text());require(sha(Path(owr['path']))==owr['sha256'],'official OWR custody')
if (P/'MANIFEST.json').exists():
 seal=json.loads((P/'SEAL.json').read_text());require(sha(P/'MANIFEST.json')==seal['manifest_sha256'],'review manifest seal')
 for row in json.loads((P/'MANIFEST.json').read_text())['files']:
  f=P/row['path'];require(sha(f)==row['sha256'] and f.stat().st_size==row['bytes'],'review artifact '+row['path'])
 require(sha(P/'REPORT.md')==seal['report_sha256'],'final report binding');require(sha(P/'VERDICT.json')==seal['verdict_sha256'],'final verdict binding')
print(json.dumps({'status':'PASS','packet_checks':checks,'all181original_members_verified':True,'current_symbolic_identities':56,'mathematical_sampling_is_not_universal_proof':True,'source_originals_unchanged':True},indent=2))
