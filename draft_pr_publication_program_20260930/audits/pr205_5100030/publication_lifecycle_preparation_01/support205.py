"""PR205 shared operational guards. Imports perform no backend or service action.
Root injects reviewed direct c/h modules and an exact source-adoption record.
"""
from pathlib import Path
import base64,datetime,hashlib,json,os,re,sys
if sys.flags.optimize or not sys.dont_write_bytecode:raise RuntimeError('Ordinary Python -B required')
D=Path(__file__).resolve().parent;A=D.parent;ROOT=A.parent.parent.parent
PREFIX='draft_pr_publication_program_20260930/';CASE=PREFIX+'audits/pr205_5100030/';OWN=CASE+D.name+'/'
HEAD='e8d7e925d19698edcb75822e40ca5ac820eb4388';PID='5100030';NATIVE='unsolved_math_prioritization/attempts/'+PID+'/'
Q='unsolved_math_prioritization/QUEUE.md';VIEWS=[CASE+n for n in ('CURRENT_CASE_STATUS.json','RESEARCH_LOG.md')]+[PREFIX+n for n in ('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md')]
SOURCES={'support205.py','ready205.py','lifecycle205.py','make_native205.py'}
INTAKE='custody_checkpoint_01/intake10_01';INTAKE_COMMIT='42f7c19cca7117f06139fd3ecbac6a32662072db';INTAKE_TREE='efdb04e6bb93dc80c7e16b9d3510b367ab194e09';INTAKE_DIGEST='4a391bd9f830aae85377d64cd7b552510ba5c3210491d7bb984390d02eb4456d'
INTAKE_ACCEPT={'bytes':1323,'sha256':'1b3135037f3adf80b8356417576d6140c2e211a44d424e37741c72d33cf0969d'}
INTAKE_MAP={'bytes':1241149,'sha256':'f8496b756cf9d976000afd4b6b814019598cb60ae5e103179872c612e9a19105'}
CUSTODY={'bytes':7313,'sha256':'967da7f97505e7c25b332535b1d468f23e20c0eb1204196710f074885c942f5e'}
QRECEIPT={'bytes':1785,'sha256':'4f7ff59a64cd99331711ece68a960baf52267397532cc4f48a2d3ae25ec87ec9'}
BASE_ROW={'bytes':121,'sha256':'f66cda83ff5e83157122daa3a7d24c36974172aa8c5c77161b1da43cbf1e8774'}
HEAD_ROW={'bytes':371,'sha256':'b6aa5ade7853f7513e4835adf129b8e38d2c1f3a0242354dd4e90db2f338f827'}
MATH='ROOT_MATHEMATICAL_SOURCE_GATE_01.json';MATH_PIN={'bytes':22117,'sha256':'7b7ccfc01af4e3b11c37ac8c92ce6b7fe193f841035a71e363c6221f1d0e8dd4'}
PRIORITY='ROOT_PRIORITY_EDITORIAL_GATE_01.json';PRIORITY_PIN={'bytes':11458,'sha256':'49ee3c7aa2df2167dded573bdee3336c1a7ccf85a23e2b1c9b08a499de0e8413'}
PORTABLE={'bytes':14419,'sha256':'7fbee76b89716091b84e2ec4f99f252d7cd1b0a47f517e4f605c806f762398bd'}
PORTABLE_RECEIPT='ROOT_PORTABLE_VERIFICATION_ACCEPTANCE_01.json';PORTABLE_RECEIPT_PIN={'bytes':1434,'sha256':'cc0624a96c76ae96a6b626c786546f9f8cc24b9c6ccaa67dc37d3a47911cf794'}
REPAIRS='ROOT_VERIFICATION_REPAIR_ACCEPTANCE_01.json';REPAIRS_PIN={'bytes':2193,'sha256':'e20c2d14f3d8be88b86f6d45a66c2ac9e49f013b7af2f587c31a7d23b23f4b38'}
BASE_COUNTS={'fully_completed_count':47,'published_count':31,'last_completed_PR':204,'next_numeric_intake_cursor':205,'advance_to_next_PR_authorized_now':False,'goal_complete':False}
DONE_COUNTS={'fully_completed_count':48,'published_count':32,'last_completed_PR':205,'next_numeric_intake_cursor':206,'advance_to_next_PR_authorized_now':True,'goal_complete':False}
POINTER={k:'ROOT_ACTUAL_'+k.upper()+'_CHECKPOINT.json' for k in ('ready','merge','factual','completion')}
CLAIM='Ordinary outer-focus distances to complete original supporting lines in proper nested confocal ellipses: the product of the two focal distance sums is constant on each admitted odd primitive family, including all coprime stars and reversal; odd repetitions multiply the product by r squared.'
CREDIT='The full all-odd analytic lemma is a corollary of Khare-Sukhatme generalized Landen Eqs68-70; Khare-Lakshminarayan-Sukhatme cyclic identities, Bialy-Tabachnikov Lemma4.2 focal-support geometry, Stachel Theorem4.3 canonical billiard grid, Reznik-Garcia-Koiller k601 observation and published elliptic-trace methods are credited. This is an attributed verification, with no theorem, formula or method novelty, firstness, certified independent discovery or simultaneity claim. Exact earlier explicit geometric k601 publication was not established by the bounded audit.'
EFFORT='Original submitted claimed_solved1/5 retained; author turn count and actual model/reasoning effort unverified. Later audits are not original author turns.'
_authority=None;_backend=None
def need(ok,message):
    if not ok:raise RuntimeError(message)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def bpin(raw):return {**pin(raw),'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
def enc(value):return (json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
def decode(raw):return json.loads(raw,parse_constant=lambda x:(_ for _ in ()).throw(RuntimeError('Nonfinite JSON '+x)))
def rel(value):
    need(isinstance(value,str) and value and not value.startswith('/') and '\\' not in value and all(x not in ('','.','..') for x in value.split('/')),'Unsafe relative path');return value
def bytepin(value):
    need(isinstance(value,dict) and set(value)=={'bytes','sha256'} and type(value['bytes']) is int and value['bytes']>=0 and re.fullmatch('[0-9a-f]{64}',value['sha256']) is not None,'Exact byte pin');return value
def pp(path,value):return {'path':rel(path),**bytepin(value)}
def read(path,expected=None,readonly=True):
    p=A
    for part in rel(path).split('/'):p=p/part;need(not p.is_symlink(),'Symlink artifact '+path)
    need(p.is_file() and (not readonly or p.stat().st_mode&0o777==0o444),'Regular readonly artifact '+path);raw=p.read_bytes()
    if expected is not None:need(pin(raw)==bytepin(expected),'Artifact pin drift '+path)
    return raw
def obj(path,expected=None,readonly=True):return decode(read(path,expected,readonly))
def digest(selected):
    need(all(set(v)=={'bytes','sha256','git_blob'} for v in selected.values()),'Selected pin schema');return hashlib.sha256(json.dumps(selected,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def configure_authority(path,expected):
    global _authority
    _authority=(rel(path),bytepin(expected));authority()
def authority():
    need(_authority is not None,'Missing explicit future Root source adoption; no runtime allowed');path,wanted=_authority;j=obj(path,wanted)
    need(j.get('schema')=='pr205-root-lifecycle-preparation-adoption-v1' and j.get('accepted_preparation_only') is True and j.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and j.get('PR')==205 and j.get('original_head')==HEAD,'Root source adoption not accepted')
    expected_gate=j['expected_publication_gate'];need(set(expected_gate)=={'path','bytes','sha256'} and expected_gate['path']=='ROOT_PUBLICATION_GATE_01.json','Explicit future gate binding');bytepin({k:expected_gate[k] for k in ('bytes','sha256')})
    need(set(j['sources'])=={D.name+'/'+n for n in SOURCES},'Exact four preparation source paths')
    for name,x in j['sources'].items():read(name,bytepin(x))
    need(j['native_constructor']==pp(D.name+'/make_native205.py',j['sources'][D.name+'/make_native205.py']),'Exact adopted pure constructor source')
    safe=j['safe_artifacts'];need(isinstance(safe,dict) and all(safe.get(name)==x for name,x in j['sources'].items()),'Adopted preparation safe artifacts')
    for name,x in safe.items():need(name.startswith(D.name+'/') and not any(p.startswith('private_') or p=='__pycache__' for p in rel(name).split('/')),'Preparation artifact scope');read(name,bytepin(x))
    return j
def configure_backend(c,h):
    global _backend
    mods=[h,h.m,h.m.m,h.m.m.h,h.m.m.h.m,h.m.m.h.m.m]
    need(len({id(x) for x in mods})==6 and all(x.api is h.api for x in mods),'Direct six API aliases')
    need(all(callable(getattr(c,k,None)) for k in ('byte_pin','selected_current','selected_digest')) and h.lookup.__globals__ is mods[-1].__dict__ and h.changed_leaves.__globals__ is mods[-1].__dict__ and h.m.native_tree_cache is mods[-1].TREE_CACHE,'Direct native utility graph')
    _backend=(c,h)
def runtime():authority();need(_backend is not None,'Root must inject reviewed direct c/h backend');return _backend
def validate_cache(h):
    for sha,rows in h.m.native_tree_cache.items():h.m.verify_tree_object(sha,rows)
def body(h,path,commit):
    tree=h.api('git/commits/'+commit)['tree']['sha'];x=h.lookup(tree,path)
    if x is None:return None
    need(x[:2]==('100644','blob'),'Nonregular native body '+path);j=h.api('git/blobs/'+x[2]);need(j['sha']==x[2] and j['encoding']=='base64','Native blob response');raw=base64.b64decode(j['content']);need(len(raw)==j['size'] and bpin(raw)['git_blob']==x[2],'Native blob identity');return raw
def entries(h,out):
    result=[]
    for path,raw in sorted(out.items()):
        rel(path);need(isinstance(raw,bytes),'Byte postimage required')
        try:text=raw.decode('utf-8')
        except UnicodeDecodeError:text=None
        if text is None or path.endswith(('.pdf','.zip')):
            sha=h.api('git/blobs','POST',{'encoding':'base64','content':base64.b64encode(raw).decode()})['sha'];need(sha==bpin(raw)['git_blob'],'Created binary blob identity');result.append({'path':path,'mode':'100644','type':'blob','sha':sha})
        else:result.append({'path':path,'mode':'100644','type':'blob','content':text})
    return result
def originals():
    j=obj('ORIGINAL_SUBMISSION_CUSTODY.json',CUSTODY);need(j['original_head']==HEAD and j['file_count']==len(j['files'])==17 and j['total_native_bytes']==41845 and j['original_QUEUE_effort_cell']=='1/5','Original205 extent');out={}
    for name,x in j['files'].items():raw=read('original_submitted_head/'+rel(name));need(bpin(raw)=={k:x[k] for k in ('bytes','sha256','git_blob')},'Original archive '+name);out[name]=raw
    return j,out
def queue_rows():
    q=obj('ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json',QRECEIPT);base=q['base_own_row']['text'].encode();head=q['original_QUEUE_row']['text'].encode()
    need(q['original_head']==HEAD and q['range_base']=='a7e588da5ac76913e00f979681f2dfff2d9a56be' and all(q[k] is True for k in ('foreign_QUEUE_rows_identical','own_only_changed_row','all_queue_bytes_retrievable_by_immutable_native_blob_ID')),'Original QUEUE scope')
    for raw,k,w in ((base,'base_own_row',BASE_ROW),(head,'original_QUEUE_row',HEAD_ROW)):need(pin(raw)==w and bpin(raw)=={n:q[k][n] for n in ('bytes','sha256','git_blob')},'Original QUEUE row pin')
    bc=base.decode().rstrip('\n').split('|');hc=head.decode().rstrip('\n').split('|');need(len(bc)==len(hc)==14 and bc[:8]==hc[:8] and (bc[8].strip(),bc[9].strip(),hc[8].strip(),hc[9].strip())==('queued','0/5','claimed_solved','1/5'),'Original BASE versus HEAD');return q,base,head
def published_row(doi):
    need(re.fullmatch(r'10\.5281/zenodo\.[1-9][0-9]*',doi) is not None,'Actual DOI');q,base,head=queue_rows();cells=head.decode().rstrip('\n').split('|');cells[10]=' https://github.com/AlecKriebel/Math/pull/205 ';cells[11]=' '+CLAIM+' '+CREDIT+' '+EFFORT+' Extensive AI; unrefereed; no conventional human peer review. ';cells[12]=' ['+doi+'](https://doi.org/'+doi+') ';return '|'.join(cells).encode()+b'\n'
def replace_queue(old,doi):
    q,base,head=queue_rows();rows=old.splitlines(keepends=True);ix=[i for i,x in enumerate(rows) if b'| 5100030 / AMR-050-0030 |' in x];need(len(ix)==1 and rows[ix[0]]==base,'First merge requires exact BASE121');new=list(rows);new[ix[0]]=published_row(doi);need([i for i,(x,y) in enumerate(zip(rows,new)) if x!=y]==ix,'Only own QUEUE row changed');return b''.join(new)
def reconcile(c,h,base,parent,published_doi=None):
    old=body(h,Q,base['commit']);new=body(h,Q,parent);need(c.byte_pin(old)==base['selected_files'][Q],'Accepted QUEUE preimage pin');ol,nl=old.splitlines(keepends=True),new.splitlines(keepends=True);need(len(ol)==len(nl),'Foreign QUEUE line count');protected={k.split('/')[2] for k in base['selected_files'] if k.startswith('unsolved_math_prioritization/attempts/')}|{PID};changes=[]
    def ident(row):
        cells=row.decode().split('|');need(len(cells)==14 and cells[1].strip().isdigit(),'Changed QUEUE row shape');return cells[2].strip().split(' / ')[0]
    for i,(x,y) in enumerate(zip(ol,nl)):
        if x==y:continue
        pid=ident(x);need(ident(y)==pid and pid not in protected,'Own/protected QUEUE change');changes.append({'line':i+1,'problem_id':pid,'before':bpin(x),'after':bpin(y)})
    marker=b'| 5100030 / AMR-050-0030 |';own=[x for x in ol if marker in x];current=[x for x in nl if marker in x];expected=queue_rows()[1] if published_doi is None else published_row(published_doi);need(len(own)==len(current)==1 and own==current==[expected],'Phase-specific exact own row')
    return {**base['selected_files'],Q:c.byte_pin(new)},{'UTC':now(),'baseline_actual_commit':base['commit'],'observed_MAIN':parent,'current_QUEUE':c.byte_pin(new),'foreign_changed_rows':changes,'own_and_protected_rows_unchanged':True}
def baseline_intake():
    a=obj(INTAKE+'/ACCEPTANCE.json',INTAKE_ACCEPT);x=obj(INTAKE+'/ACCEPTANCE_CURRENT_SELECTED_MAP.json',INTAKE_MAP);need(a['accepted'] is True and a['checkpoint_commit']==a['main_observed']==INTAKE_COMMIT and a['actual_tree']==INTAKE_TREE and a['case_percent']==10,'Actual custody10 required');need(len(x['selected_files'])==4124 and digest(x['selected_files'])==x['selected_map_sha256']==a['actual_current_selected_map_sha256']==INTAKE_DIGEST,'Actual4124map');need(all(a[k]==v for k,v in BASE_COUNTS.items()),'Intake counters');return {'commit':INTAKE_COMMIT,'tree':INTAKE_TREE,'selected_files':x['selected_files']}
def gate(wanted):
    adopted=authority();need(adopted['expected_publication_gate']==pp('ROOT_PUBLICATION_GATE_01.json',bytepin(wanted)),'Gate differs from exact Root source activation');g=obj('ROOT_PUBLICATION_GATE_01.json',wanted);need(g['schema']=='pr205-root-publication-ready-v1' and g['evidence_scope']=='ACTUAL_ROOT_RECEIPT' and (g['PR'],g['problem_id'],g['original_head'])==(205,5100030,HEAD),'Publication gate identity')
    for k in ('publication_ready_gate_accepted','whole_package_review_loop_complete','mathematical_clearance','source_contract_clearance','bounded_priority_audit_complete'):need(g[k] is True,'Final clearance '+k)
    for k in ('historical_priority_established','theorem_novelty_cleared','formula_novelty_cleared','proof_method_novelty_cleared','first_disclosure_certified','independent_discovery_certified','literal_simultaneity_established','actual_publication_verified','actual_tracker_row_verified','actual_original_PR_merged'):need(g.get(k,False) is False,'Forbidden readiness claim '+k)
    package=rel(g['package']);need(re.fullmatch('publication_package_[A-Za-z0-9_]+',package) is not None,'Package directory');safe=g['package_safe_files'];need(isinstance(safe,dict) and safe,'Complete package map');files={'ROOT_PUBLICATION_GATE_01.json':wanted}
    for name,x in safe.items():path=package+'/'+rel(name);read(path,bytepin(x));files[path]=x
    pd=A/package;actual=set()
    for p in pd.rglob('*'):need(not p.is_symlink(),'Package symlink');actual.add(p.relative_to(pd).as_posix()) if p.is_file() else None
    need(actual==set(safe),'Exact complete package set');seal_file=rel(g.get('package_seal_file','PACKAGE_SEAL.json'));need(safe[seal_file]==bytepin(g['package_seal']),'Package seal pin');need(safe['verification/verify.py']==PORTABLE,'Current portable source');read(package+'/verification/verify.py',PORTABLE)
    uploads=g['intended_upload_files'];need(len(uploads)==3 and {'odd_period_focal_pedal.tex','odd_period_focal_pedal.pdf'}<=set(uploads) and sum(n.endswith('.zip') for n in uploads)==1,'Exactly manuscript/source/ZIP');need(all(Path(n).name==n and safe[n]==bytepin(x) for n,x in uploads.items()),'Exact uploads');metadata_file=rel(g.get('metadata_file','zenodo-deposit.json'));md=obj(package+'/'+metadata_file,safe[metadata_file]);need(md['metadata']==g['metadata'] and {x['path'] for x in md['files']}==set(uploads) and len(md['files'])==3,'Exact metadata/manifest')
    events=g['whole_package_review_events'];need(isinstance(events,list) and len(events)>=2,'At least two NEW whole-package reviews');dirs=set();acceptances=set();repairs=False
    for index,event in enumerate(events,1):
        directory=rel(event['directory']);af=rel(event['Root_acceptance_file']);need(directory not in dirs and af not in acceptances and type(event['review_number']) is int and event['review_number']==index and event['whole_package_scope'] is True and type(event['open_findings']) is int and event['open_findings']>=0,'Distinct whole-review event');need(event['verdict']!='CLEANPASS' or event['open_findings']==0,'Clean review has open finding');dirs.add(directory);acceptances.add(af);rs=event['safe_files'];need(isinstance(rs,dict) and event['report_file'] in rs,'Review report bound')
        for name,x in rs.items():path=directory+'/'+rel(name);read(path,bytepin(x),False);files[path]=x
        a=obj(af,bytepin(event['Root_acceptance_pin']),False);files[af]=event['Root_acceptance_pin'];need(a['schema']=='pr205-root-whole-package-review-acceptance-v1' and a['evidence_scope']=='ACTUAL_ROOT_RECEIPT' and a['accepted'] is True and a['PR']==205 and a['original_head']==HEAD and a['review_accepted'] is True and type(a['NEW_whole_package_reviews_completed']) is int and a['NEW_whole_package_reviews_completed']==index,'Actual Root review acceptance');ae=a['review_event'];need({k:v for k,v in event.items() if k not in ('Root_acceptance_file','Root_acceptance_pin')}==ae and ae['safe_files']==rs,'Root accepted exact event, except nonrecursive envelope pins');need(event['report_pin']==rs[event['report_file']],'Review report pin');read(rel(event['reviewed_package'])+'/'+seal_file,event['reviewed_package_seal']);repairs=repairs or event['verdict']!='CLEANPASS' or a['review_cycle_repairs_required_now'] is not False
    last=events[-1];need(last['verdict']=='CLEANPASS' and last['open_findings']==0 and last['reviewed_package']==package and last['reviewed_package_seal']==g['package_seal'] and a['review_cycle_repairs_required_now'] is False,'Last clean final exact seal')
    if repairs:need(g.get('fresh_final_review_after_documented_editorial_repairs') is True,'Documented repair history/fresh final review')
    for path,x in g['other_safe_files'].items():rel(path);need(path!='ROOT_PUBLICATION_GATE_01.json' and not any(p.startswith('private_') or p in ('__pycache__','.venv','site-packages') for p in path.split('/')) and not path.endswith(('.pyc','.pyo')) and 'ACCEPTANCE_CURRENT_SELECTED_MAP' not in path,'Public other-file scope');read(path,bytepin(x),False);files[path]=x
    need(g['other_safe_files'].get(MATH)==MATH_PIN and g['other_safe_files'].get(PRIORITY)==PRIORITY_PIN,'Fixed Root math/priority gates');mg=obj(MATH,MATH_PIN);pg=obj(PRIORITY,PRIORITY_PIN);need(mg['mathematical_clearance'] is True and mg['source_contract_clearance'] is True and pg['bounded_priority_audit_complete'] is True and pg['novelty_clearance'] is False,'Root scientific/editorial facts')
    need(g['other_safe_files'].get(PORTABLE_RECEIPT)==PORTABLE_RECEIPT_PIN and g['other_safe_files'].get(REPAIRS)==REPAIRS_PIN,'Fixed portable/repair receipts')
    for name,x in ((PORTABLE_RECEIPT,PORTABLE_RECEIPT_PIN),(REPAIRS,REPAIRS_PIN)):
        record=obj(name,x);need(record['accepted'] is True and record['evidence_scope']=='ACTUAL_ROOT_RECEIPT' and record['PR']==205,'Root portable/repair acceptance')
    for role in ('mathematics','priority','portable','repairs'):
        x=g['preparation_receipts'][role];need(set(x)=={'path','bytes','sha256'} and files.get(rel(x['path']))=={k:x[k] for k in ('bytes','sha256')},'Explicit Root preparation role '+role)
    for name,x in authority()['safe_artifacts'].items():files[name]=x
    files[_authority[0]]=_authority[1]
    return g,files
def actual(which):
    need(which in POINTER,'Actual phase');p=obj(POINTER[which]);directory=rel(p['directory']);need(directory.startswith(D.name+'/'),'Approved205 actual directory');a=obj(directory+'/ACCEPTANCE.json',p['acceptance_pin']);r=obj(directory+'/PREPARATION.json');x=obj(directory+'/ACCEPTANCE_CURRENT_SELECTED_MAP.json',a['actual_current_map_file'])
    need(p['PR']==a['PR']==205 and p['phase']==which and a['accepted'] is True and a['original_head']==HEAD and a['checkpoint_commit']==r['commit']==p['checkpoint_commit'] and a['main_observed']==p['main_observed'] and a['case_percent']=={'ready':90,'merge':95,'factual':98,'completion':100}[which],'Actual phase identity')
    for k in ('every_selected_identity_checked_at_actual_observed_MAIN','all_overlay_body_identities_verified','full_foreign_tree_scope_preserved'):need(a[k] is True,'Actual full scope '+k)
    need(digest(x['selected_files'])==x['selected_map_sha256']==a['actual_current_selected_map_sha256'] and len(x['selected_files'])==a['selected_files'] and digest(r['selected_files'])==a['selected_map_sha256']==r['selected_map_sha256'],'Actual selected maps');return directory,a,r,x
def actual_context():
    directory,a,r,x=actual('ready');g,files=gate(a['Root_publication_gate_pin'])
    for k in ('QUEUE_native_original_PR_unchanged','mathematical_clearance','source_contract_clearance','priority_clearance','bounded_priority_audit_complete','qualified_attributed_note_editorially_cleared','publication_ready'):need(a[k] is True,'Actual ready alias '+k)
    need(a['historical_firstness_independence_established'] is False,'No firstness');need(all(x['selected_files'].get(CASE+path)==bpin(read(path,w,False)) for path,w in files.items()),'Ready map binds final files');custody,old=originals()
    for name,raw in old.items():need(x['selected_files'].get(CASE+'original_submitted_head/'+name)==bpin(raw),'Actualready original archive '+name)
    need(x['selected_files'].get(CASE+'ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json')==bpin(read('ORIGINAL_QUEUE_SINGLE_ROW_RECEIPT.json',QRECEIPT)),'Actualready original QUEUE receipt');return g,{'gate_pin':a['Root_publication_gate_pin'],'ready_pointer_pin':pin(read(POINTER['ready'])),'ready_acceptance_pin':pin(read(directory+'/ACCEPTANCE.json')),'checkpoint_commit':a['checkpoint_commit'],'package_seal':g['package_seal'],'package':g['package'],'manifest_pin':pin(read(g['package']+'/'+g.get('metadata_file','zenodo-deposit.json')))}
def tracker_row(g,doi):return ['k601: ordinary focal-pedal distance product (AMR-050-0030)','','https://doi.org/'+doi,g['metadata']['title']+'. '+CLAIM+' '+CREDIT+' '+EFFORT+' Extensive AI; unrefereed; no conventional human peer review. PR205.']
def operations():
    g,context=actual_context();raw=read('ROOT_PUBLICATION_RECEIPT.json');p=decode(raw)
    for k in ('actual_publication_verified','metadata_exact_verified','all_three_public_download_SHA256_verified'):need(p[k] is True,'Actual publication '+k)
    need(p['PR']==205 and p['state']=='published' and p['gate_sha256']==context['gate_pin']['sha256'] and p['package']==g['package'] and p['context']==context and p['metadata_normalizations']==[],'Publication context');need(type(p['id']) is int and p['id']>0 and p['doi']=='10.5281/zenodo.'+str(p['id']) and p['doi_url']=='https://doi.org/'+p['doi'] and p['record_url']=='https://zenodo.org/records/'+str(p['id']),'Actual record/DOI');need(p['doi_resolution']['http_status']==200 and p['doi_resolution']['status']=='resolved','DOI resolver');need(len(p['files'])==3 and {z['name']:{'bytes':z['size'],'sha256':z['sha256']} for z in p['files']}==g['intended_upload_files'] and set(p['verified_public_download_names'])==set(g['intended_upload_files']),'Actual exact uploads');need(len(p['public_downloads'])==3 and {z['name']:{'bytes':z['bytes'],'sha256':z['sha256']} for z in p['public_downloads']}==g['intended_upload_files'] and all(z['url'].startswith('https://') and z['final_url'].startswith('https://') for z in p['public_downloads']),'Actual public downloads')
    traw=read('ROOT_TRACKER_RECEIPT.json');t=decode(traw)
    for k in ('actual_tracker_row_verified','own_row_readback_verified','foreign_rows_retained','original_preappend_baseline_retained','two_fresh_full_prechecks','RAW_INSERT_ROWS','B_intentionally_blank_no_verified_chat_share_URL'):need(t[k] is True,'Actual tracker '+k)
    need(t['PR']==205 and t['doi']==p['doi'] and t['gate_sha256']==context['gate_pin']['sha256'] and t['publication_receipt']==pin(raw) and t['context']==context and t['row']==tracker_row(g,p['doi']),'Tracker context/row');need(t['spreadsheet_id']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and t['sheet_gid']==1254632077 and re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",t['range']) is not None,'Tracker actual own range');base=t['original_preappend_baseline'];need(set(base)=={'file','pin','row_count','counter_sha256'} and type(base['row_count']) is int and base['row_count']>0 and re.fullmatch('[0-9a-f]{64}',base['counter_sha256']) is not None,'Tracker original baseline');bytepin(base['pin']);return g,p,t,context
def fsync_dir(path):
    fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(fd)
    finally:os.close(fd)
def save(path,raw,pointer=False):
    need((path.parent==A and path.name in POINTER.values()) if pointer else path.resolve().is_relative_to(D),'Output scope')
    with path.open('xb') as f:need(f.write(raw)==len(raw),'Short record');f.flush();os.fchmod(f.fileno(),0o444);os.fsync(f.fileno())
    fsync_dir(path.parent)
def generation(name):need(re.fullmatch('[a-z][a-z0-9_]{0,48}',name) is not None,'Generation name');return D/name
def local_preimages(h,parent):
    result={}
    for path in VIEWS:
        f=ROOT/path;raw=body(h,path,parent);need(f.is_file() and not f.is_symlink() and f.read_bytes()==raw,'All-five fresh parent preimage '+path);result[path]=pin(raw)
    return result
def sync_views(h,r):
    images=[]
    for path in VIEWS:
        f=ROOT/path;post=body(h,path,r['commit']);need(bpin(post)==r['selected_files'][path] and f.is_file() and not f.is_symlink(),'Local five postimage/type');raw=f.read_bytes();need(pin(raw) in (r['local_five_expected_preimages'][path],pin(post)),'Local five preimage');images.append((path,f,raw,post))
    for path,f,raw,post in images:
        need(f.is_file() and not f.is_symlink() and f.read_bytes()==raw,'Local five type/preimage after precheck')
        if raw!=post:
            tmp=f.with_name(f.name+'.pr205_publication_sync_tmp')
            with tmp.open('xb') as stream:need(stream.write(post)==len(post),'Short local view');stream.flush();os.fchmod(stream.fileno(),0o444);os.fsync(stream.fileno())
            os.replace(tmp,f);fsync_dir(f.parent)
        need(f.is_file() and not f.is_symlink(),'Local five type before chmod');f.chmod(0o444);need(f.read_bytes()==post,'Local five readback')
    return [{'path':path,'postimage':pin(post)} for path,f,raw,post in images]
