#!/usr/bin/env python3
import json,hashlib,datetime,collections
from pathlib import Path
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1];P=BASE/'preprint_v1_0';K=P/'verification_kit';R=BASE/'repairs/case_alias01'
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def read(p):return json.loads(p.read_text())
def pin(p):return {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def match(p,row):need(pin(p)=={k:row[k] for k in ['bytes','sha256']},str(p))
frozen=read(HERE/'INPUT_FREEZE.json')['files']
for r in frozen:match(BASE/r['path'],r)
baseline=read(R/'IMMEDIATE_INPUT_PINS.json')['files'];changes=read(R/'CHANGE_ACCOUNTING.json')['changes'];changed={r['path']:r for r in changes}
need(len(baseline)==623 and len(changed)==10,'623/10 accounting')
for r in baseline:
    path=r['path']
    if path in changed:
        match(BASE/changed[path]['source_snapshot'],r);match(BASE/path,changed[path]['after'])
    else:match(BASE/path,r)
protected=read(R/'PROTECTED_INPUT_PINS.json')['files']
need(len(protected)==613,'protected 613')
for r in protected:match(BASE/r['path'],r)
for r in read(R/'OUTPUT_PINS.json')['files']:match(R/r['path'],r)
stage=read(K/'REPAIR01_STAGE_COPIES.json')['files'];oldstage=read(R/'before/preprint_v1_0/verification_kit/REPAIR01_STAGE_COPIES.json')['files']
need(len(stage)==157 and len(oldstage)==145 and stage[:145]==oldstage,'copy exact prefix')
for r in stage:match(K/r['destination'],r)
history=read(K/'REPAIR01_HISTORY_RESOLUTION.json')['references'];oldhistory=read(R/'before/preprint_v1_0/verification_kit/REPAIR01_HISTORY_RESOLUTION.json')['references']
need(len(history)==4641 and len(oldhistory)==4628 and history[:4628]==oldhistory,'history exact prefix')
rel=[]
for name,n in [('TERMINAL_HISTORY_RELOCATIONS.json',2),('CASE_ALIAS_HISTORY_RELOCATIONS.json',7)]:
    rows=read(K/name)['rows'];need(len(rows)==n,'relocation count');rel+=rows
relmap={r['reference_index']:r for r in rel};need(len(relmap)==9,'unique relocations')
for index,row in relmap.items():need(history[index]==row['historical_reference'],'exact relocated old row')
dispositions=collections.Counter()
for i,r in enumerate(history):
    dispositions[r['disposition']]+=1
    if r['disposition']=='omitted':need(bool(r['reason']),'individual omission')
    else:
        need(r['disposition']=='exact_captured_stage_or_canonical_copy','history disposition')
        match(K/(relmap[i]['current_exact_destination'] if i in relmap else r['destination']),r)
need(dispositions=={'omitted':1434,'exact_captured_stage_or_canonical_copy':3207},'history totals')
for row in read(R/'INDIVIDUAL_CHANGED_OLD_PIN_RESOLUTIONS.json')['references']:
    source=BASE/(changed[row['source_inventory']]['source_snapshot'] if row['source_inventory'] in changed else row['source_inventory'])
    obj=read(source)
    for token in row['json_pointer'].strip('/').split('/'):
        token=token.replace('~1','/').replace('~0','~')
        obj=obj[int(token)] if isinstance(obj,list) else obj[token]
    need(obj==row['original_pin'],'structured old pin JSON pointer')
    match(BASE/row['exact_local_before'],obj)
    if row['delivered_before']:match(K/row['delivered_before'],obj)
    else:need(row['disposition']=='old_archive_local_only_not_newly_packed','local only omission')
ledger=read(K/'COPY_EXCLUSION_LEDGER.json')
for r in ledger['files']:
    if r['disposition']=='byte_identical_copy':match(K/r['destination'],r)
    else:need(r['disposition']=='omitted' and r['reason'],'copy omission')
for r in ledger['historical_pin_references']:
    if r['disposition']=='hash_identical_canonical_copy':need(pin(K/r['destination'])['sha256']==r['sha256'],'canonical hash')
    else:need(r['disposition']=='omitted' and r['reason'],'old reference omission')
submitted=sorted(p for p in (BASE/'submitted').iterdir() if p.is_file())
need(len(submitted)==6,'six original submitted')
for p in submitted:need(p.read_bytes()==(K/'originals/submitted'/p.name).read_bytes(),'six original copy')
native=read(P/'metadata.json');upload=read(P/'deposit_metadata.json')
need(upload['metadata']==native==read(K/'metadata.json'),'native schema equality')
need((P/'metadata.json').read_bytes()==(K/'metadata.json').read_bytes(),'native byte equality')
need((P/'research_metadata.json').read_bytes()==(K/'research_metadata.json').read_bytes(),'custom historical research')
need(upload['files']==[{'path':'preprint.pdf','name':'preprint.pdf'},{'path':'verification_kit.zip','name':'verification_kit.zip'}],'two attachment names')
need(set(upload)=={'metadata','files'},'native uploader descriptor')
current=read(P/'CURRENT_CASE_ALIAS_REPAIR01.json')
need(all(current[k] is False for k in ['publication_ready','issues_resolved','published']),'hold flags')
need(current['services_held_at']==1032,'1032 hold')
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_frozen_regular_inputs_unchanged':len(frozen),'baseline':623,'changed_exact_before_and_after':10,'protected_unchanged':613,'repair_outputs':36,'stage_copies':157,'old_copy_exact_prefix':145,'new_copies':12,'history_references':4641,'old_history_exact_prefix':4628,'new_history':13,'history_dispositions':dict(dispositions),'terminal_relocations':2,'case_relocations':7,'changed_old_structured_pin_resolutions':75,'original_six_exact':True,'native_metadata_bytes_and_descriptor':True,'services_held_at':1032,'publication_ready':False}
(HERE/'INDEPENDENT_CUSTODY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
