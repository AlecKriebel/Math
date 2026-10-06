"""Independent bounded static bindings and receipt validation, no frozen writes."""
from pathlib import Path, PurePosixPath
import collections, datetime, hashlib, json, os, re, stat, zipfile
from record_exec import ROOT, digest
A=ROOT.parent; D=A/'contingent_credited_note_v2';P=D/'publicfiles'
checks=[]
def ck(condition,name):
    if not condition:raise RuntimeError(name)
    checks.append(name)
def sha(p):return digest(p.read_bytes())
def load(p):return json.loads(p.read_bytes())
def safe(name):
    return isinstance(name,str) and bool(name) and '\\' not in name and '\x00' not in name and not name.startswith('/') and not re.match(r'^[a-zA-Z]:',name) and all(x not in ('','.','..') for x in name.split('/')) and PurePosixPath(name).as_posix()==name

# Original closures are independently tested against their preserved manifests.
closures=[]
for folder,filename,key in [('contingent_credited_note_v2','CLOSED_MANIFEST.json','files'),
    ('contingent_credited_note_v1','CLOSED_MANIFEST.json','files'),
    ('whole_package_round1_20261006','CLOSED_EVIDENCE_MANIFEST.json','own_files')]:
    root=A/folder; m=load(root/filename)
    for e in m[key]:
        p=root/e['path'];ck(safe(e['path']) and p.is_file() and not p.is_symlink() and sha(p)==e['sha256'] and p.stat().st_size==e['bytes'],folder+' file '+e['path'])
    for e in m.get('controlled_symlinks',[]):
        p=root/e['path'];ck(p.is_symlink() and os.readlink(p)==e['target'] and p.resolve().is_relative_to(root.resolve()),folder+' link '+e['path'])
        if e.get('target_sha256'):ck(sha(p)==e['target_sha256'],folder+' link target '+e['path'])
    groups={}
    for e in m[key]:
        p=root/e['path'];s=p.stat()
        if s.st_nlink>1:groups.setdefault((s.st_dev,s.st_ino),[]).append(e['path'])
    ck(sorted(sorted(g) for g in groups.values())==sorted(sorted(g) for g in m.get('hardlink_groups',[])),folder+' hardlink closure')
    ck(all(len(g)==(root/g[0]).stat().st_nlink for g in groups.values()),folder+' no external hardlink member')
    expected={e['path'] for e in m[key]}|{e['path'] for e in m.get('controlled_symlinks',[])}|{filename}
    actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() or p.is_symlink()}
    ck(actual==expected,folder+' exact inventory')
    closures.append({'folder':folder,'manifest_sha256':sha(root/filename),'regular_files':len(m[key]),'symlinks':len(m.get('controlled_symlinks',[])),'hardlink_groups':len(groups)})

manifest=load(P/'MANIFEST.json'); entries={e['path']:e for e in manifest['files']}
ck(len(entries)==len(manifest['files'])==92,'92 distinct payload files')
ck({str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}==set(entries)|{'MANIFEST.json'},'payload closure')
ck(not any(p.is_symlink() for p in P.rglob('*')),'payload has no symlinks')
with zipfile.ZipFile(D/'pr97_support.zip') as z:
    names=z.namelist();ck(len(names)==len(set(names))==93,'93 distinct ZIP members')
    ck(set(names)==set(entries)|{'MANIFEST.json'},'ZIP exact manifest closure')
    for i in z.infolist():
        ck(safe(i.filename) and not i.is_dir() and stat.S_ISREG(i.external_attr>>16) and i.compress_type in (0,8) and not i.flag_bits&1,'safe regular ZIP '+i.filename)
        ck(z.read(i)==(P/i.filename).read_bytes(),'ZIP byte equality '+i.filename)
    ck(sum(i.file_size for i in z.infolist())<16*1024*1024,'bounded ZIP')
for n,e in entries.items():ck(sha(P/n)==e['sha256'] and (P/n).stat().st_size==e['bytes'],'payload digest '+n)
sumlines=(D/'SHA256SUMS.txt').read_text().splitlines();summed={}
for line in sumlines:
    h,name=line.split('  ',1);ck(safe(name) and h==sha(D/name),'SHA256SUMS '+name);summed[name]=h
ck(len(sumlines)==len(summed)==95,'95 sums without duplicates')
ck(set(summed)=={'publicfiles/'+x for x in entries}|{'publicfiles/MANIFEST.json','pr97_support.zip','zenodo-deposit.proposed.json'},'sum inventory matches proposal')
identity=load(D/'BYTE_IDENTITY.json')
for e in identity['files']:ck((P/e['path']).read_bytes()==(A/e['original_reference']).read_bytes() and sha(P/e['path'])==e['sha256'],'static identity '+e['path'])
for local,borrowed in [('support/CANDIDATE.md','CANDIDATE.md'),('support/verify.py','verify.py'),('support/review/independent_checks.py','review/independent_checks.py')]:
    ck((P/local).read_bytes()==(A/'credited_verification_candidate_v2'/borrowed).read_bytes(),'adopted exact input '+local)
ck((P/'support/CANDIDATE.md').read_bytes()==(P/'support/review/author_replay/CANDIDATE.md').read_bytes(),'candidate duplicate')

# Proposed metadata is a static JSON recipe; no upload or account access is performed.
meta=load(P/'zenodo_metadata.proposed.json');proposal=load(D/'zenodo-deposit.proposed.json');plan=load(D/'DEPOSIT_PLAN.json')
ck(proposal['metadata']==meta,'deposit metadata semantic identity')
ck(proposal['files']==plan['relative_file_list_exactly'] and len(proposal['files'])==9,'nine proposal files')
for e in proposal['files']:ck(safe(e['path']) and (D/e['path']).is_file() and not (D/e['path']).is_symlink(),'deposit relative file '+e['path'])
ck(sha(D/'zenodo-deposit.proposed.json')==plan['proposal_sha256'] and sha(P/'zenodo_metadata.proposed.json')==plan['metadata_sha256'],'plan recipe hashes')
provenance=load(D/'private/METADATA_PROVENANCE.json')['original']
extra_pins=[]
for kind in ['preset','pr95_pattern']:
    p=Path(provenance[kind+'_path']);ck(sha(p)==provenance[kind+'_sha256'],'metadata source '+kind)
    extra_pins.append({'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size})
preset=load(Path(provenance['preset_path']))['metadata']
for k in provenance['fields_preserved_from_preset']:ck(meta[k]==preset[k],'preset field '+k)
ck(meta['creators'][0]['orcid']=='0009-0001-9320-500X' and meta['license']=='cc-by-4.0' and meta['publication_type']=='preprint','creator/license/preprint')
ck(not any(k in meta for k in ['doi','prereserve_doi','id','record_id']),'no reserved DOI/service state')

ledger=load(P/'PRIMARY_SOURCE_READ_SCOPE.json')
for e in ledger['sources']:ck(sha(A/e['research_source_reference'])==e['source_sha256'],'primary-source exact version pin '+e['id'])
ck(not ledger['priority_clearance'] and not ledger['publication_authorized'] and not ledger['third_party_redistribution'],'bounded source-read gates')
reuse=load(P/'support/receipts/REUSED_BASELINE_PROVENANCE.json')
for e in reuse['reused_files']:ck((P/'support/receipts'/e['path']).read_bytes()==(A/e['original_reference']).read_bytes() and sha(A/e['original_reference'])==e['sha256'],'reused receipt '+e['path'])
ck(reuse['new_compile_or_render_performed'] is False and reuse['new_visual_inspection_claimed'] is False,'honest baseline reuse')
compile=load(P/'support/receipts/FINAL_COMPILE_RENDER.json')
ck(compile['source_sha256']==sha(P/'pr97_note.tex') and compile['pdf_sha256']==sha(P/'pr97_note.pdf'),'paper provenance hashes')
for e in compile['rendered_page_files']:ck(sha(A/'contingent_credited_note_v1'/e['path'])==e['sha256'],'frozen four-page render '+e['path'])
for r,label in zip(compile['processes'],['final_terminal_compile','final_pdfinfo','final_note_render']):
    ck(r['exit_code']==0 and r['pid']>0 and r['started_utc']<=r['finished_utc'],'historical compile actual fields '+label)
    for stream in ['stdout','stderr']:ck(sha(P/'support/receipts'/(label+'.'+stream+'.txt'))==r[stream+'_sha256'],'historical stream '+label+' '+stream)

def field_check(r,label):
    for key in ['command','cwd','pid','started_utc','finished_utc','exit_code','stdout_sha256','stderr_sha256']:ck(key in r,label+' field '+key)
    ck(isinstance(r['pid'],int) and r['pid']>0 and r['command'] and r['cwd'] and r['started_utc']<=r['finished_utc'],label+' actual invocation/time')
    if 'stdout' in r:
        for stream in ['stdout','stderr']:ck(digest(r[stream].encode())==r[stream+'_sha256'],label+' embedded '+stream)

index=load(D/'PROCESS_INDEX.json');counts=collections.Counter()
ck(index['process_records']==len(index['records'])==111,'111 pre-index records')
seen=[]
for row in index['records']:
    rp=D/row['receipt_path'];ck(sha(rp)==row['receipt_sha256'],'index receipt digest '+row['receipt_path'])
    raw=load(rp);record=(raw if isinstance(raw,list) else [raw])[row['record_index']]
    field_check(record,'indexed '+str(record['pid']))
    for k,v in row.items():
        if k not in ['scope','receipt_path','receipt_sha256','record_index']:ck(record[k]==v,'index field '+k+' '+str(record['pid']))
    counts[row['scope']]+=1;seen.append(record['pid'])
ck(len(seen)==len(set(seen)),'111 distinct actual child PIDs')
outer=[]
for rp in (D/'private/actual_runs').glob('*.json'):
    r=load(rp);field_check(r,'outer '+rp.stem);outer.append(r)
    for stream in ['stdout','stderr']:ck(sha(rp.with_suffix('.'+stream+'.txt'))==r[stream+'_sha256'],'outer stream '+rp.stem+' '+stream)
    for name,h in r.get('input_source_hashes',{}).items():ck(sha(D/name)==h,'outer input source '+name)
ck(len(outer)==8,'eight outer receipts incl post-index aggregation')

diags=load(D/'private/diagnostics_current/PROCESS_RECEIPTS.json')
own=load(ROOT/'diagnostics_reproduction/PROCESS_RECEIPTS.json')
ck(len(diags)==len(own)==6,'six actual diagnostics')
for r,q in zip(diags,own):
    label=r['family']+'_'+r['mode'];field_check(r,'diag '+label)
    for stream,ext in [('stdout','.json'),('stderr','.txt')]:
        ck(sha(D/'private/diagnostics_current'/(label+'.'+stream+ext))==r[stream+'_sha256'],'diagnostic raw '+label+' '+stream)
    ck(r['accepted'] and r['candidate_sha256']==sha(P/'support/CANDIDATE.md'),'diag acceptance/input '+label)
    ck(r['stdout_sha256']==q['stdout_sha256'],'independent replay exact stdout '+label)
    if r['mode']=='false_check_optimized':ck(r['exit_code']==1 and q['exit_code']==1,'active false guard '+label)
    else:ck(r['exit_code']==0 and r['diagnostic_assertions']==(87 if r['family']=='author' else 89),'finite count '+label)

custody=load(D/'private/custody_current/PROCESS_RECEIPTS.json');ck(len(custody)==50,'50 synthetic custody children')
for r in custody:
    field_check(r,'custody '+r['label']);ck(r['synthetic_control'] and r['accepted'],'synthetic role '+r['label'])
    if 'child_launched' in r:
        ck(r['exit_code']!=0 and not r['child_launched'] and r['input_inventory_before']==r['input_inventory_after'] and r['victim_sha256_before']==r['victim_sha256_after'],'pre-child preservation '+r['label'])
        if 'output_inventory_before' in r:ck(r['output_inventory_before']==r['output_inventory_after'],'output preservation '+r['label'])
    if 'failed_child_receipt' in r:
        child=r['failed_child_receipt'];field_check(child,'failed '+r['label']);ck(child['accepted'] is False and child.get('rejection_reason'),'saved failure interpretation '+r['label'])
integrity=load(D/'private/integrity_current/PROCESS_RECEIPTS.json');ck(len(integrity)==28,'28 integrity children')
for r in integrity:
    field_check(r,'integrity '+r['label']);ck(r['accepted'],'integrity control acceptance '+r['label'])
    ck((r['exit_code']==0 and 'PASS' in r['stdout']) if r['expected_reason'] is None else (r['exit_code']!=0 and r['expected_reason'] in r['stderr']),'integrity reason '+r['label'])
actualreuse=load(D/'private/actual_reuse_controls/PROCESS_RECEIPTS.json');ck(len(actualreuse)==6,'six actual output reuses')
for r in actualreuse:
    field_check(r,'reuse '+r['label']);ck(r['exit_code']!=0 and not r['child_launched'] and r['prior_inventory_before']==r['prior_inventory_after'],'actual reuse preservation '+r['label'])

# Pin authoritative original full-data sources without copying their bodies.
sourcepair=load(A/'original_source_authentication_20261005/SOURCEPAIR_AUTHENTICATION.json')
for e in sourcepair['full_data_pins']:
    p=Path(e['path']);h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    ck(h.hexdigest()==e['sha256'] and p.stat().st_size==e['bytes'],'original full-data pin '+p.name)
    extra_pins.append({'path':str(p),'sha256':e['sha256'],'bytes':e['bytes']})
for e in load(D/'CLOSED_MANIFEST.json')['borrowed_input_bindings']['original_and_round1']+load(D/'CLOSED_MANIFEST.json')['borrowed_input_bindings']['inherited_math_and_priority']:
    p=A/e['reference'];extra_pins.append({'path':str(p),'sha256':e['sha256'],'bytes':e['bytes']})
existing=load(ROOT/'BORROWED_INPUT_PINS.json');pins={e['path']:e for e in existing['files']}
for e in extra_pins:pins[e['path']]=e
existing['files']=list(pins.values());(ROOT/'BORROWED_INPUT_PINS.json').write_text(json.dumps(existing,indent=2)+'\n')
result={'status':'PASS','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':len(checks),'check_names':checks,
    'closures':closures,'historical_index_scope_counts':dict(counts),'recorded_processes_before_index':111,
    'post_index_outer_receipt':1,'package_math_children':6,'package_integrity_children':28,'package_custody_children':50,
    'package_completed_reuse_children':6,'borrowed_input_pins':len(pins),
    'historical_evidence_limit':'Receipts and source/stream hashes independently cross-checked; historic PID provenance is not reobserved kernel process state.',
    'publication_authorized':False,'priority_clearance':False}
(ROOT/'STATIC_AND_RECEIPT_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='check_names'},indent=2))
