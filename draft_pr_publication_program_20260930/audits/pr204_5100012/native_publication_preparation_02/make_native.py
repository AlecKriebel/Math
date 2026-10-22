"""Pure PR204 canonical-gate postimage constructor, revision02. No writes, subprocesses, network or publication.

Actual production construction requires authenticated future Root receipts. See CONTRACT.md.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime
import hashlib
import json
import re

PREP = Path(__file__).resolve().parent
A = PREP.parent
HEAD = '551a524e2db65fec90684485ef676d0b4179378d'
CUSTODY_PIN = {'path': 'ORIGINAL_SUBMISSION_CUSTODY.json', 'bytes': 7837, 'sha256': '5011318581db86668f4a6d27939808957875c55b70c1cc71b61ed63bb1f18a93'}
CASE = 'draft_pr_publication_program_20260930/audits/pr204_5100012/'
NATIVE = 'unsolved_math_prioritization/attempts/5100012/'
CHANGED = frozenset({'README.md', 'SOURCES.md', 'MANIFEST.json', 'PUBLICATION_MANIFEST.json', 'PUBLICATION_STATUS.md'})
ADDED = frozenset({'CURRENT_STATUS.json', 'CURRENT_PROOF.md', 'CURRENT_SOURCE_AND_PRIORITY.json', 'QUALIFIED_PRIORITY.md', 'CURRENT_RESEARCH_LOG.md', 'NATIVE_PRESENTATION_RECEIPT.json', 'SHA256SUMS'})
STAGES = ('published_pending_merge', 'actual_merge_accepted', 'factual_checkpoint_accepted')
FACT_KEYS = {'schema','original_head','UTC','package_seal','publication_ready_gate','publication_receipt','tracker_receipt','merge_receipt','factual_receipt'}

class Refused(ValueError):
    """Required evidence missing, inconsistent, stale or synthetic in production."""

def need(test, message):
    if not test:
        raise Refused(message)

def enc(obj):
    return (json.dumps(obj, indent=2, sort_keys=True, allow_nan=False)+'\n').encode()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def same_pin(left, right):
    return isinstance(left,dict) and isinstance(right,dict) and all(left.get(k)==right.get(k) for k in ('path','bytes','sha256'))

def moment(value):
    need(isinstance(value,str), 'UTC must be a string')
    try:
        dt=datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError as exc:
        raise Refused('Invalid UTC') from exc
    need(dt.tzinfo is not None and dt.utcoffset().total_seconds()==0, 'UTC offset must be zero')
    return dt

def safe_file(root, rel):
    need(isinstance(rel,str) and rel and '\\' not in rel, 'Unsafe relative path')
    pure=PurePosixPath(rel)
    need(not pure.is_absolute() and all(c not in ('','..','.') for c in pure.parts), 'Unsafe relative path')
    need(str(pure)==rel, 'Noncanonical relative path')
    p=root
    for component in pure.parts:
        p=p/component
        need(not p.is_symlink(), 'Symlinks are not accepted: '+rel)
    need(p.is_file(), 'Required file missing: '+rel)
    return p

def read_pin(root, pin):
    need(isinstance(pin,dict) and set(pin)=={'path','bytes','sha256'}, 'Pin must contain path,bytes,sha256 only')
    need(type(pin['bytes']) is int and pin['bytes']>=0 and re.fullmatch(r'[0-9a-f]{64}',str(pin['sha256'])), 'Invalid byte/hash pin')
    data=safe_file(root,pin['path']).read_bytes()
    need(len(data)==pin['bytes'] and digest(data)==pin['sha256'], 'Pinned bytes differ: '+pin['path'])
    return data

def json_bytes(data, name):
    try:
        value=json.loads(data,parse_constant=lambda unused: (_ for _ in ()).throw(Refused('Nonfinite JSON forbidden')))
    except (ValueError, UnicodeError) as exc:
        raise Refused('Invalid JSON: '+name) from exc
    need(isinstance(value,dict), 'Receipt must be an object: '+name)
    return value

def originals(root=A):
    root=Path(root)
    custody=json_bytes(read_pin(root,CUSTODY_PIN),'custody')
    need(custody.get('original_head')==HEAD and custody.get('original_QUEUE_status')=='claimed_solved','Wrong original HEAD/status')
    need(custody.get('file_count')==20 and custody.get('total_native_bytes')==59343 and len(custody.get('files',{}))==20,'Wrong original archive extent')
    out={}
    for name,pin in custody['files'].items():
        data=safe_file(root,'original_submitted_head/'+name).read_bytes()
        need(len(data)==pin['bytes'] and digest(data)==pin['sha256'],'Modified original: '+name)
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        need(blob==pin['git_blob'],'Original native blob identity differs: '+name)
        out[name]=data
    need(CHANGED<=set(out) and len(set(out)-CHANGED)==15,'Original preservation set differs')
    return out

def read_role(root, pin, schema, scope, facts_utc):
    obj=json_bytes(read_pin(root,pin),schema)
    need(obj.get('schema')==schema and obj.get('evidence_scope')==scope,'Wrong receipt schema/evidence scope: '+schema)
    need(obj.get('original_head')==HEAD,'Wrong receipt HEAD: '+schema)
    need(moment(obj.get('UTC'))<=facts_utc,'Receipt is later than facts: '+schema)
    return obj

def verify_preparation(root, gate):
    baseline=json_bytes((PREP/'PREPARATION_INPUT_PINS.json').read_bytes(),'preparation pins')['receipts']
    need(gate.get('preparation_receipts')==baseline,'Accepted math/priority/repair/portable pins differ')
    objects={name:json_bytes(read_pin(root,pin),name) for name,pin in baseline.items()}
    need(objects['mathematics'].get('original_head')==HEAD and objects['mathematics'].get('verdict','').startswith('MATHEMATICAL PASS'),'Math acceptance missing')
    priority=objects['priority']
    need(priority.get('original_head')==HEAD and priority.get('bounded_priority_audit_complete') is True and priority.get('editorial_manuscript_preparation_authorized') is True,'Qualified priority/editorial gate missing')
    for key in ('novel_theorem_verified','novel_formula_verified','novel_method_verified','independent_discovery_established','historical_firstness_established','literal_simultaneity_established'):
        need(priority.get(key) is False,'Uncleared novelty/chronology flag changed: '+key)
    need(objects['repairs'].get('verification_integrity_required_repairs_complete') is True,'Repair acceptance missing')
    need(objects['portable'].get('status')=='PASS' and objects['portable'].get('finite_noninterval_controls_only') is True,'Portable acceptance missing')
    return baseline


GATE_NAME='ROOT_PUBLICATION_GATE_01.json'
FIRST_REVIEW_FILE='ROOT_WHOLE_PACKAGE_REVIEW_ACCEPTANCE_01.json'
FIRST_REVIEW_PLAIN={'bytes':4290,'sha256':'3014eae5a1bf70938c43556fad732235b7c08359971b775bb8f0ee36f6fdbbc7'}
UPLOAD_NAMES={'centered_pedal_dn.pdf','centered_pedal_dn.tex','verification-package.zip'}
READY_FIELDS=('accepted','every_selected_identity_checked_at_actual_observed_MAIN','all_overlay_body_identities_verified','full_foreign_tree_scope_preserved','QUEUE_native_original_PR_unchanged','mathematical_clearance','source_contract_clearance','priority_clearance','bounded_priority_audit_complete','qualified_attributed_note_editorially_cleared','publication_ready')

def plain(pin):
    need(isinstance(pin,dict) and set(pin)=={'bytes','sha256'},'Exact plain byte/SHA256 pin required')
    need(type(pin['bytes']) is int and pin['bytes']>=0 and re.fullmatch('[0-9a-f]{64}',str(pin['sha256'])),'Invalid plain byte/SHA256 pin')
    return pin

def with_path(path, pin):
    return {'path':path,**plain(pin)}

def byte_pin(data):
    return {'bytes':len(data),'sha256':digest(data)}

def package_name(value):
    need(isinstance(value,str) and re.fullmatch('publication_package_[a-zA-Z0-9_]+',value),'Unsafe explicit package directory')
    return value

def scope_check(obj, fixture, label):
    if fixture:
        need(obj.get('evidence_scope')=='SYNTHETIC_OFFLINE_FIXTURE','Synthetic marker missing: '+label)
    else:
        need(not str(obj.get('evidence_scope','')).startswith('SYNTHETIC'),'Synthetic evidence refused in production: '+label)

def read_package_seal(root, seal_pin, fixture):
    need(isinstance(seal_pin,dict),'Package seal pin missing')
    rel=seal_pin.get('path')
    need(isinstance(rel,str) and '/' in rel,'Explicit package seal path missing')
    package,unused=rel.split('/',1);package_name(package)
    need(unused.endswith('.json'),'Package seal filename is not JSON')
    seal=json_bytes(read_pin(root,seal_pin),'package seal')
    need(isinstance(seal.get('schema'),str) and re.fullmatch(r'pr204-publication-package-seal-v[1-9][0-9]*',seal['schema']) and seal.get('package_prepared') is True,'Not a prepared PR204 package seal')
    scope_check(seal,fixture,'package seal');moment(seal.get('UTC'))
    return package,seal

def verify_package(root, seal_pin, gate, fixture):
    package=package_name(gate.get('package'))
    sealfile=gate.get('package_seal_file','PACKAGE_SEAL.json')
    need(isinstance(sealfile,str),'Explicit seal filename missing')
    wanted=with_path(package+'/'+sealfile,gate.get('package_seal'))
    need(seal_pin==wanted,'Native path-bearing seal does not equal canonical package/plain seal')
    got,seal=read_package_seal(root,seal_pin,fixture);need(got==package,'Package name drift')
    files=gate.get('package_safe_files')
    need(isinstance(files,dict) and files and files.get(sealfile)==gate['package_seal'],'Complete canonical package safe map missing exact seal')
    for name,pin in files.items():
        need(not any(c in {'__pycache__','runtime_packages','primary_source_private','.git','site-packages','.venv','private_tree_cache'} for c in PurePosixPath(name).parts) and not name.endswith(('.pyc','.pyo')) and 'ACCEPTANCE_CURRENT_SELECTED_MAP.json' not in name,'Private/runtime/cache file in public package')
        read_pin(root,with_path(package+'/'+name,pin))
    actual=set()
    for path in (root/package).rglob('*'):
        need(not path.is_symlink(),'Symlink in package')
        if path.is_file():actual.add(path.relative_to(root/package).as_posix())
    need(actual==set(files),'Complete actual package differs from canonical safe map')
    sealed_files=seal.get('files')
    need(isinstance(sealed_files,dict) and len(sealed_files)==seal.get('file_count_excluding_seal'),'Prepared seal file extent differs')
    need(set(sealed_files)|{sealfile}==set(files) and all(files.get(n)==p for n,p in sealed_files.items()),'Gate safe map differs from prepared seal')
    paper=gate.get('paper');driver=gate.get('portable_entrypoint')
    need(isinstance(paper,str) and paper.endswith('.tex') and paper in files,'Final paper not pinned')
    need(isinstance(driver,str) and driver.endswith('.py') and driver in files,'Portable driver not pinned')
    uploads=gate.get('intended_upload_files')
    need(isinstance(uploads,dict) and set(uploads)==UPLOAD_NAMES and uploads==seal.get('intended_uploads'),'Canonical exact intended upload set differs')
    need(all('/' not in n and files.get(n)==plain(p) for n,p in uploads.items()) and paper in uploads,'Upload pins differ from final package')
    metadatafile=gate.get('metadata_file','zenodo-deposit.json')
    need(metadatafile in files,'Final metadata not pinned')
    md=json_bytes(read_pin(root,with_path(package+'/'+metadatafile,files[metadatafile])),'final metadata')
    need(md.get('metadata',md)==gate.get('metadata'),'Gate and exact final metadata differ')
    need(set(md)=={'metadata','files'} and isinstance(md['files'],list) and len(md['files'])==3 and all(isinstance(x,dict) and set(x)=={'path'} for x in md['files']) and {x['path'] for x in md['files']}==UPLOAD_NAMES,'Canonical operations metadata/upload manifest differs')
    need(any(isinstance(x,dict) and x.get('name')=='Kriebel, Alec' and x.get('orcid')=='0009-0001-9320-500X' for x in gate['metadata'].get('creators',[])),'Author ORCID missing')
    return package,seal,files,paper,driver

def canonical_reviews(root, gate, seal_pin, fixture):
    reviews=gate.get('whole_package_review_events')
    need(isinstance(reviews,list) and len(reviews)>=2,'At least two NEW actual Root-accepted whole-package reviews required')
    directories=set();acceptances=set();acceptance_hashes=set();report_hashes=set();report_paths=set();previous=None;repairs=False;last_acceptance=None
    for index,event in enumerate(reviews,1):
        need(isinstance(event,dict) and type(event.get('review_number')) is int and event['review_number']==index,'Canonical review numbers must be sequential')
        need(event.get('whole_package_scope') is True,'Explicit whole-package scope missing')
        need(isinstance(event.get('verdict'),str) and event['verdict'] and type(event.get('open_findings')) is int and event['open_findings']>=0,'Malformed canonical verdict/open findings')
        need(event['verdict']!='CLEANPASS' or event['open_findings']==0,'CLEANPASS still has open findings')
        directory=event.get('directory');safe=event.get('safe_files');reportfile=event.get('report_file')
        need(isinstance(directory,str) and directory not in directories and isinstance(safe,dict) and safe,'Review directory/safe artifacts missing or reused')
        directories.add(directory)
        for name,pin in safe.items():read_pin(root,with_path(directory+'/'+name,pin))
        need(isinstance(reportfile,str) and reportfile in safe,'Review report not in exact safe files')
        report=with_path(directory+'/'+reportfile,safe[reportfile])
        need(event.get('report')==report,'Explicit report alias does not bind canonical report_file/safe_files')
        if 'report_pin' in event:need(event['report_pin']==safe[reportfile],'Review report_pin differs')
        need(report['path'] not in report_paths and report['sha256'] not in report_hashes,'Review report path or bytes reused')
        report_paths.add(report['path']);report_hashes.add(report['sha256'])
        af=event.get('Root_acceptance_file');ap=plain(event.get('Root_acceptance_pin'))
        need(isinstance(af,str) and af not in acceptances and ap['sha256'] not in acceptance_hashes,'Root acceptance reused/missing')
        acceptances.add(af);acceptance_hashes.add(ap['sha256'])
        accepted=json_bytes(read_pin(root,with_path(af,ap)),'Root whole-review acceptance')
        scope_check(accepted,fixture,'Root review acceptance')
        need(accepted.get('schema')=='pr204-root-entire-package-review-acceptance-v1' and accepted.get('PR')==204 and accepted.get('original_head')==HEAD and accepted.get('review_accepted') is True and type(accepted.get('NEW_whole_package_reviews_completed')) is int and accepted['NEW_whole_package_reviews_completed']==index,'Root acceptance identity/authority/count differs')
        need(type(accepted.get('review_cycle_repairs_required_now')) is bool,'Root review repair disposition missing')
        ae=accepted.get('review_event')
        need(isinstance(ae,dict) and all(event.get(k)==v for k,v in ae.items()),'Canonical event changed an exact Root-accepted review_event field')
        need(ae.get('safe_files')==safe and ae.get('reviewed_package')==event.get('reviewed_package') and ae.get('reviewed_package_seal')==event.get('reviewed_package_seal'),'Root acceptance does not bind exact reviewed package/artifacts')
        if index==1 and not fixture:need(af==FIRST_REVIEW_FILE and ap==FIRST_REVIEW_PLAIN,'Exact already accepted first review was replaced')
        reviewed=package_name(event.get('reviewed_package'));sf=event.get('reviewed_package_seal_file','PACKAGE_SEAL.json')
        if reviewed==gate['package']:sf=event.get('reviewed_package_seal_file',gate.get('package_seal_file','PACKAGE_SEAL.json'))
        _,reviewed_seal=read_package_seal(root,with_path(reviewed+'/'+sf,event.get('reviewed_package_seal')),fixture)
        when=moment(event.get('UTC'));accepted_when=moment(accepted.get('UTC'))
        need(previous is None or previous<when,'Review UTC order is not strict');previous=when
        need(moment(reviewed_seal['UTC'])<=when<=accepted_when<=moment(gate['UTC']),'Review/seal/Root acceptance/gate chronology differs')
        repairs=repairs or event['verdict']!='CLEANPASS' or accepted['review_cycle_repairs_required_now']
        last_acceptance=accepted
    last=reviews[-1]
    need(last['verdict']=='CLEANPASS' and last['open_findings']==0 and last_acceptance['review_cycle_repairs_required_now'] is False and last['reviewed_package']==gate['package'] and last['reviewed_package_seal']==gate['package_seal'],'Final actual Root-accepted review not clean/exact/fresh')
    if repairs:need(gate.get('fresh_final_review_after_documented_editorial_repairs') is True,'Earlier repair history requires explicit documented repairs and fresh final review')
    return reviews

def check_canonical_gate(root, gate, facts, fixture):
    need(facts['publication_ready_gate']['path']==GATE_NAME,'Only canonical ROOT_PUBLICATION_GATE_01.json accepted')
    need(gate.get('PR')==204 and gate.get('problem_id')==5100012,'Canonical gate case mismatch')
    for key in ('accepted','publication_ready','release_authorized','publication_ready_gate_accepted','whole_package_review_loop_complete','mathematical_clearance','source_contract_clearance','bounded_priority_audit_complete'):
        need(gate.get(key) is True,'Canonical/native Root gate authority missing: '+key)
    need(gate.get('historical_priority_established') is False,'Historical priority cannot be promoted')
    for key in ('theorem_novelty_cleared','formula_novelty_cleared','proof_method_novelty_cleared','first_disclosure_certified','independent_discovery_certified','literal_simultaneity_established','actual_publication_verified','actual_tracker_row_verified','actual_original_PR_merged'):
        need(gate.get(key,False) is False,'Readiness gate cannot claim novelty/actual publication: '+key)
    need(gate.get('proof_kind')=='origin_only_Jacobi_direct_foot_two_pole','Wrong proof presentation')
    baseline=verify_preparation(root,gate)
    other=gate.get('other_safe_files')
    need(isinstance(other,dict),'Canonical other-safe-files map missing')
    required={p['path'] for p in baseline.values()}|{'ROOT_SOURCE_FIRST_CONTRACT_01.md','ROOT_PACKAGE_PREPARATION_ACCEPTANCE_01.json'}
    need(required<=set(other) and any('PDF' in n and 'VISUAL' in n for n in other),'Canonical scientific/preparation/PDF history incomplete')
    for name,pin in other.items():
        need(name!=GATE_NAME and 'ACCEPTANCE_CURRENT_SELECTED_MAP.json' not in name and not any(c in {'private_operations','private_tree_cache','__pycache__','primary_source_private','.venv','site-packages','runtime_packages'} for c in PurePosixPath(name).parts) and not name.endswith(('.pyc','.pyo')),'Private/recursive/map artifact in canonical public history')
        read_pin(root,with_path(name,pin))
    for pin in baseline.values():need(other.get(pin['path'])==plain({k:pin[k] for k in ('bytes','sha256')}),'Canonical history does not retain accepted preparation pin')
    return baseline

def canonical_ready_context(root, context, gate, gate_pin, fixture, cutoff):
    need(isinstance(context,dict) and set(context)=={'gate_pin','ready_pointer_pin','ready_acceptance_pin','checkpoint_commit','package_seal','package','manifest_pin'},'Authentic canonical operations context required')
    need(context['gate_pin']==byte_pin(read_pin(root,gate_pin)) and context['package']==gate['package'] and context['package_seal']==gate['package_seal'],'Operations gate/package context differs')
    metadatafile=gate.get('metadata_file','zenodo-deposit.json')
    need(context['manifest_pin']==gate['package_safe_files'][metadatafile],'Operations metadata pin differs')
    pointer=json_bytes(read_pin(root,with_path('ROOT_ACTUAL_READY_CHECKPOINT.json',context['ready_pointer_pin'])),'actual ready pointer')
    scope_check(pointer,fixture,'actual ready pointer')
    need(pointer.get('PR')==204 and pointer.get('phase')=='ready' and pointer.get('Root_recorded_only_after_actual_full_scope_acceptance') is True,'Actual ready pointer not accepted')
    directory=pointer.get('directory');need(isinstance(directory,str),'Ready acceptance directory missing')
    accepted=json_bytes(read_pin(root,with_path(directory+'/ACCEPTANCE.json',context['ready_acceptance_pin'])),'actual ready acceptance')
    scope_check(accepted,fixture,'actual ready acceptance')
    need(pointer.get('acceptance_pin')==context['ready_acceptance_pin'] and accepted.get('PR')==204 and accepted.get('original_head')==HEAD and accepted.get('case_percent')==90,'Actual ready acceptance identity differs')
    need(all(accepted.get(k) is True for k in READY_FIELDS),'Actual ready full-scope acceptance flags missing')
    need(accepted.get('historical_firstness_independence_established') is False,'Ready acceptance priority qualification differs')
    commit=context.get('checkpoint_commit')
    need(re.fullmatch('[0-9a-f]{40}',str(commit)) and accepted.get('checkpoint_commit')==pointer.get('checkpoint_commit')==commit and accepted.get('main_observed')==pointer.get('main_observed'),'Ready commit/accepted MAIN binding differs')
    observed=accepted.get('main_observed')
    need(isinstance(observed,str) and re.fullmatch('[0-9a-f]{40}',observed) and pointer.get('main_observed')==observed,'Exact accepted observed MAIN/pointer hash required')
    need(moment(accepted.get('UTC'))<=moment(pointer.get('UTC'))<=cutoff,'Ready acceptance/pointer chronology differs')
    mapped=json_bytes(read_pin(root,with_path(directory+'/ACCEPTANCE_CURRENT_SELECTED_MAP.json',accepted.get('actual_current_map_file'))),'actual selected map')
    scope_check(mapped,fixture,'actual selected map')
    selected=mapped.get('selected_files')
    need(isinstance(selected,dict) and type(accepted.get('selected_files')) is int and len(selected)==accepted['selected_files'],'Accepted selected-map extent differs')
    ds=hashlib.sha256(json.dumps(selected,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    need(ds==mapped.get('selected_map_sha256')==accepted.get('actual_current_selected_map_sha256'),'Actual selected-map digest differs')
    required={GATE_NAME:gate_pin,**{gate['package']+'/'+n:with_path(gate['package']+'/'+n,p) for n,p in gate['package_safe_files'].items()}}
    for name,raw in originals(root).items():
        rel='original_submitted_head/'+name
        required[rel]={'path':rel,**byte_pin(raw)}
    for name,pin in required.items():
        raw=read_pin(root,pin)
        identity={**byte_pin(raw),'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
        need(selected.get(CASE+name)==identity,'Accepted actual ready map does not bind gate/package: '+name)
    return context

def canonical_publication(root, facts, gate, fixture, clock):
    ref=facts.get('publication_receipt')
    need(isinstance(ref,dict) and ref.get('path')=='ROOT_PUBLICATION_RECEIPT.json','Authentic canonical publication receipt path required')
    raw=json_bytes(read_pin(root,ref),'canonical publication receipt');scope_check(raw,fixture,'publication')
    need(raw.get('PR')==204 and raw.get('state')=='published','Canonical publication identity/state differs')
    need(moment(gate['UTC'])<=moment(raw.get('UTC'))<=clock,'Actual publication chronology differs')
    for key in ('actual_publication_verified','metadata_exact_verified','all_three_public_download_SHA256_verified'):need(raw.get(key) is True,'Actual publication verification missing: '+key)
    gp=facts['publication_ready_gate']
    need(raw.get('gate_sha256')==gp['sha256'] and raw.get('publication_gate')==GATE_NAME and raw.get('package')==gate['package'],'Publication not bound to canonical gate/package')
    need(raw.get('metadata_normalizations')==[] and raw.get('metadata_sha256')==hashlib.sha256((json.dumps(gate['metadata'],sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()).hexdigest(),'Exact metadata evidence differs')
    rid=raw.get('id');doi=raw.get('doi')
    need(type(rid) is int and rid>0 and rid not in (23085904,23400541) and doi=='10.5281/zenodo.'+str(rid),'Own DOI/record mismatch or credited prior DOI reused')
    need(raw.get('doi_url')=='https://doi.org/'+doi and raw.get('record_url')=='https://zenodo.org/records/'+str(rid),'Canonical DOI/record URL differs')
    resolution=raw.get('doi_resolution')
    need(isinstance(resolution,dict) and resolution.get('status')=='resolved' and type(resolution.get('http_status')) is int and resolution['http_status']==200 and resolution.get('final_url') in ('https://zenodo.org/records/'+str(rid),'https://zenodo.org/records/'+str(rid)+'/','https://zenodo.org/record/'+str(rid),'https://zenodo.org/record/'+str(rid)+'/'),'Actual resolver target differs')
    wanted=gate['intended_upload_files'];names=raw.get('verified_public_download_names');files=raw.get('files')
    need(isinstance(names,list) and len(names)==3 and set(names)==UPLOAD_NAMES,'Three actual verified public download names required')
    need(isinstance(files,list) and len(files)==3 and all(isinstance(x,dict) and type(x.get('size')) is int for x in files) and {x.get('name'):{'bytes':x['size'],'sha256':x.get('sha256')} for x in files}==wanted,'Canonical actual publication file pins differ')
    downloads=raw.get('public_downloads')
    need(isinstance(downloads,list) and len(downloads)==3 and all(isinstance(x,dict) for x in downloads) and len({x.get('name') for x in downloads})==3,'Canonical independent public downloads missing/duplicate')
    for entry in downloads:
        name=entry.get('name');need(name in wanted and {k:entry.get(k) for k in ('bytes','sha256')}==wanted[name],'Independent actual public download bytes differ')
        expected='https://zenodo.org/api/records/'+str(rid)+'/files/'+name+'/content'
        need(entry.get('url')==expected and isinstance(entry.get('final_url'),str) and entry['final_url'].startswith('https://'),'Actual download source/HTTPS result differs')
    need(raw.get('historical_firstness_independence_established') is False,'Publication receipt priority limits differ')
    plain(raw.get('inspect_doi_receipt'))
    context=canonical_ready_context(root,raw.get('context'),gate,gp,fixture,moment(raw['UTC']))
    return {**raw,'record_id':rid,'DOI':doi,'resolver_url':raw['doi_url'],'package_seal':facts['package_seal']},context

def canonical_tracker(root, facts, gate, pub, context, fixture, clock):
    ref=facts.get('tracker_receipt')
    need(isinstance(ref,dict) and ref.get('path')=='ROOT_TRACKER_RECEIPT.json','Authentic canonical tracker receipt path required')
    raw=json_bytes(read_pin(root,ref),'canonical tracker receipt');scope_check(raw,fixture,'tracker')
    need(raw.get('PR')==204 and raw.get('doi')==pub['doi'],'Tracker PR/DOI differs')
    for key in ('actual_tracker_row_verified','own_row_readback_verified','foreign_rows_retained','original_preappend_baseline_retained','two_fresh_full_prechecks','RAW_INSERT_ROWS','B_intentionally_blank_no_verified_chat_share_URL'):
        need(raw.get(key) is True,'Canonical tracker verification missing: '+key)
    need(moment(pub['UTC'])<=moment(raw.get('UTC'))<=clock,'Tracker chronology differs')
    need(raw.get('gate_sha256')==facts['publication_ready_gate']['sha256'] and raw.get('publication_receipt')=={k:facts['publication_receipt'][k] for k in ('bytes','sha256')} and raw.get('context')==context,'Tracker gate/publication/ready context differs')
    need(raw.get('spreadsheet_id')=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and type(raw.get('sheet_gid')) is int and raw['sheet_gid']==1254632077,'Tracker target differs')
    row=raw.get('row')
    need(isinstance(row,list) and len(row)==4 and all(isinstance(x,str) for x in row) and row[0]=='k203b: centered original-side pedal-area product (AMR-050-0012)' and row[1]=='' and row[2]==pub['doi_url'] and gate['metadata']['title'] in row[3] and 'PR204' in row[3],'Actual tracker row differs or B populated')
    need(isinstance(raw.get('range'),str) and re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",raw['range']),'Tracker exact one-row range differs')
    baseline=raw.get('original_preappend_baseline')
    need(isinstance(baseline,dict) and isinstance(baseline.get('file'),str) and '/' not in baseline['file'] and baseline['file'].startswith('before2_') and type(baseline.get('row_count')) is int and baseline['row_count']>=1 and re.fullmatch('[0-9a-f]{64}',str(baseline.get('counter_sha256'))),'Original tracker baseline pin/count/Counter missing')
    plain(baseline.get('pin'))
    need(type(raw.get('recovered_unknown_outcome')) is bool,'Tracker recovery disposition missing')
    return raw

def check_binding(receipt, seal_pin, label):
    need(same_pin(receipt.get('package_seal'),seal_pin),'Stale/different package binding: '+label)

def _construct(stage, facts, root, fixture):
    root=Path(root).resolve()
    if fixture:
        need(root.is_relative_to(PREP/'fixtures'),'Synthetic roots must stay under preparation/fixtures')
    else:
        need(root==A.resolve(),'Production root differs from this A204 case')
    need(stage in STAGES,'Unsupported lifecycle stage')
    need(isinstance(facts,dict) and set(facts)<=FACT_KEYS and facts.get('schema')=='pr204-native-facts-v1','Unknown/missing fact fields')
    need(facts.get('original_head')==HEAD,'Wrong facts original HEAD')
    clock=moment(facts.get('UTC'))
    expected={'published_pending_merge':set(),'actual_merge_accepted':{'merge_receipt'},'factual_checkpoint_accepted':{'merge_receipt','factual_receipt'}}[stage]
    need(({k for k in ('merge_receipt','factual_receipt') if k in facts})==expected,'Receipt set contradicts requested stage')
    old=originals(root)
    scope='SYNTHETIC_OFFLINE_FIXTURE' if fixture else 'ACTUAL_ROOT_RECEIPT'
    need('publication_ready_gate' in facts,'Actual publication-ready gate missing')
    need(isinstance(facts['publication_ready_gate'],dict) and facts['publication_ready_gate'].get('path')==GATE_NAME,'Only canonical final gate path may be read')
    gate=read_role(root,facts['publication_ready_gate'],'pr204-root-publication-ready-v1',scope,clock)
    baseline=check_canonical_gate(root,gate,facts,fixture)
    seal_pin=facts.get('package_seal')
    need(isinstance(seal_pin,dict),'Final package pin missing')
    package,seal,files,paper,driver=verify_package(root,seal_pin,gate,fixture)
    reviews=canonical_reviews(root,gate,seal_pin,fixture)
    pub,context=canonical_publication(root,facts,gate,fixture,clock)
    rid=pub['record_id'];doi=pub['DOI']
    tracker=canonical_tracker(root,facts,gate,pub,context,fixture,clock)
    merge=None;factual=None
    if 'merge_receipt' in facts:
        merge=read_role(root,facts['merge_receipt'],'pr204-root-merge-receipt-v1',scope,clock)
        check_binding(merge,seal_pin,'merge')
        need(all(merge.get(k) is True for k in ('accepted','merged','original_HEAD_safe','full_scope_verified')) and merge.get('PR')==204,'Actual full-scope original-HEAD-safe merge missing')
        need(re.fullmatch('[0-9a-f]{40}',str(merge.get('merge_commit'))),'Actual merge commit missing')
        need(moment(tracker['UTC'])<=moment(merge['UTC']),'Merge predates tracker')
    if 'factual_receipt' in facts:
        factual=read_role(root,facts['factual_receipt'],'pr204-root-factual-receipt-v1',scope,clock)
        check_binding(factual,seal_pin,'factual')
        need(all(factual.get(k) is True for k in ('accepted','full_scope_MAIN_accepted','actual_factual_accepted')) and factual.get('case_percent')==98 and factual.get('completed') is False,'Actual factual98 acceptance required; no circular100 completion claim')
        for role in ('publication_receipt','tracker_receipt','merge_receipt'):
            need(factual.get(role+'_sha256')==facts[role]['sha256'],'Factual receipt does not bind '+role)
        cf=factual.get('completion_facts')
        wanted98={'case_completed':False,'goal_complete':False,'fully_completed_count':46,'published_count':30,'last_completed_PR':203,'next_numeric_intake_cursor':204,'advance_to_next_PR_authorized_now':False}
        need(isinstance(cf,dict) and cf==wanted98 and all(type(cf[k]) is type(v) for k,v in wanted98.items()),'Actual98 completion facts must remain46/30,last203,cursor204,no advance')
        need(moment(merge['UTC'])<=moment(factual['UTC']),'Factual acceptance predates merge')
    marker='SYNTHETIC_OFFLINE_FIXTURE — no actual publication, tracker update, merge or completion.\n\n' if fixture else ''
    states={'published_pending_merge':'Published and tracked; actual original-HEAD-safe merge and factual acceptance pending.','actual_merge_accepted':'Published, tracked and actual original-HEAD-safe merge accepted; factual acceptance pending.','factual_checkpoint_accepted':'Published, tracked, merged and actual factual98 checkpoint accepted; program completion is governed separately.'}
    state=('Synthetic simulated stage: '+stage+'.') if fixture else states[stage]
    theorem='For a>b>0 and 0<lambda<b², fix the outer ellipse and its proper confocal elliptical caustic. For physical orbits of least N>=3, N odd or divisible by four, the signed original-trajectory area times signed shoelace area of perpendicular feet from the fixed center O to the original complete supporting side lines is phase independent. Every admitted coprime primitive star winding and both directions are included.'
    scope_text='RGK arxiv2004.12497v11 Table3p6 and journal DOI10.1007/s40598-021-00174-y Table3p346 report k203,b. Their table does not literally print least/primitive; least physical period is a necessary explicit interpretation. An exact physical-six family duplicated to listed12 disproves unrestricted list-length wording. No moving-M, hyperbolic, nonconfocal, collapsed, clipped-segment or unweighted filled-star extension is asserted. Absolute values of the signed shoelace areas also have constant product.'
    credit='Alper Ferudun, Center-Pedal Area Products in Elliptic Billiards, DOI10.5281/zenodo.23085904, proves the same full qualified theorem. Its trace telescope and standard Jacobi identities imply the shifted-trace normalization and explicit C_T coefficient here. His later DOI10.5281/zenodo.23400541 also uses adjacent-foot pole cancellation. Stachel canonical coordinates, standard Jacobi facts, and established meromorphic cancellation/compactness methods (including Akopyan–Schwartz–Tabachnikov and Chavez-Caliz) are credited. No theorem, formula or method novelty, firstness, certified independent discovery or literal simultaneity is claimed.'
    chronology='PR204 server creation is 2026-10-01T05:28:14Z. Ferudun centered-record creation is 2026-10-01T15:39:54.821511Z (registration15:39:55Z). These are object-record timestamps, not discovery times, earliest historical visibility or proof of independence. Shared203/204 checkpoint work was author input, not independent review. Current manuscript/audits are dated16October2026, not backdated.'
    effort='Original metadata/log reports one substantive author turn and original QUEUE1/5; actual model/reasoning effort and historical runtime flags are unknown. Two audit families verified the universal Jacobi mechanism after exposure. Independent direct geometry proves all N3/N4 but its general route remains partial; independent physical evidence covers63 shape/winding configurations and378 phase/direction orbits. Root’s pre-candidate flag route is uncompleted and supplies no additional proof.'
    verification='Ordinary assertion-enabled historical replays reproduce37393 exact and4092 numeric author checks, and13712 exact plus348 reviewer diagnostics. Under optimization the original scripts enforce zero correctness assertions and accept false identities. They remain historical provenance, not supported live entrypoints. Use the sealed portable explicit-exception runner and repaired controls; its finite exact/noninterval results do not prove the universal theorem. The original PROOF.md hash binding is legacy provenance only.'
    disclosure='Alec Kriebel, ORCID0009-0001-9320-500X. Extensive AI use; unrefereed; no conventional human peer review or proof-assistant certification. No outside person was contacted on behalf of this research.'
    refs={k:facts[k] for k in ('publication_ready_gate','publication_receipt','tracker_receipt','merge_receipt','factual_receipt') if k in facts}
    common={'evidence_scope':scope,'UTC':facts['UTC'],'problem_id':5100012,'PR':204,'original_head':HEAD,'publication_lifecycle_stage':stage,'state':state,'mathematical_result_valid':True,'exact_theorem':theorem,'scope_qualification':scope_text,'source_and_priority':credit,'chronology_limits':chronology,'effort_and_independence_limits':effort,'verification_limits':verification,'author_disclosure':disclosure,'DOI':doi,'record_id':rid,'resolver_url':pub['resolver_url'],'record_url':pub['record_url'],'tracker_range':tracker['range'],'package':CASE+package+'/','package_seal':seal_pin,'paper':{'path':CASE+package+'/'+paper,**files[paper]},'portable_entrypoint':{'path':CASE+package+'/'+driver,**files[driver]},'actual_root_receipt_pins':refs,'accepted_preparation_receipts':baseline,'whole_package_review_events':reviews,'actual_publication_verified':not fixture,'actual_tracker_row_verified':not fixture,'actual_merge_accepted':not fixture and merge is not None,'actual_factual_MAIN_accepted':not fixture and factual is not None,'goal_complete':False,'program_completion_authority':{'progress_path':'draft_pr_publication_program_20260930/CURRENT_PROGRESS.json','actual_completion_acceptance':'Separate actual full-scope100 acceptance; not supplied or claimed by this native presentation'},'theorem_novelty_cleared':False,'formula_novelty_cleared':False,'proof_method_novelty_cleared':False,'historical_priority_established':False,'independent_discovery_certified':False,'literal_simultaneity_established':False,'extensive_AI_use':True,'conventional_human_peer_review':False,'unrefereed':True,'formal_proof_assistant_certification':False}
    url=pub['resolver_url'];pkg='../../../'+CASE+package+'/'
    out=dict(old)
    out['CURRENT_STATUS.json']=enc(common)
    out['README.md']=(marker+'# 5100012 / k203,b: attributed centered-pedal research note\n\n'+state+'\n\nResearch note: ['+doi+']('+url+'). '+disclosure+'\n\n'+theorem+'\n\n'+scope_text+'\n\n'+credit+'\n\nThe complete current Jacobi/direct-foot/two-pole proof is indexed in CURRENT_PROOF.md. Original PROOF.md, metadata, source manifests, raw verifiers, all original independent_review records, checkpoint and original log remain byte-exact historical provenance. CURRENT_STATUS.json and CURRENT_SOURCE_AND_PRIORITY.json govern current attribution and lifecycle. All20 originals, including the five replaced presentation files, remain byte-exact in [the custody archive](../../../'+CASE+'original_submitted_head/). Manifest wrappers explicitly direct historical hashes there. SHA256SUMS authenticates this current native presentation.\n\n'+verification+'\n\nSupported entrypoint: [portable driver]('+pkg+driver+'); see its packaged README. From the final package root use `python3 -B '+driver+' --materials materials --work-dir verification-work --output verification-receipt.json`. No dependency installation is performed.\n\n'+effort+'\n\n'+chronology+'\n\n[Reviewed final package]('+pkg+'). Proposed constructor byte postimages themselves perform no publication, merge or factual acceptance.\n').encode()
    out['CURRENT_PROOF.md']=(marker+'# Current verified centered-origin proof\n\n'+theorem+'\n\nPublished research note: '+url+'. Final source ['+paper+']('+pkg+paper+'), SHA256 '+files[paper]['sha256']+'. This indexes the final origin-only Jacobi/direct-foot proof: physical canonical step and contact line, direct Euclidean center projection, cyclic dn area trace, exact reduced two-pole divisor, adjacent-term double-to-simple pole cancellation including N3/N4, explicit positive C_T, and half-period parity for all coprime stars. No area division is required. The exact physical-six doubled12 counterexample fixes the source-period qualification. This is not a claim that Root’s unfinished flag route supplies another proof.\n\n'+credit+'\n\n'+verification+'\n\nOriginal PROOF.md remains the byte-exact submitted proof, with legacy hash/source history; the current final manuscript and qualified priority records govern present claims.\n').encode()
    out['CURRENT_SOURCE_AND_PRIORITY.json']=enc({**common,'original20_archive':CASE+'original_submitted_head/','historical_source_record_and_manifests_unchanged':True,'bounded_priority_complete':True,'current_worldwide_openness_certified':False})
    out['SOURCES.md']=(marker+'# Current source, credit and bounded priority\n\n'+scope_text+'\n\n'+credit+'\n\n'+chronology+'\n\n'+effort+'\n\nCurrent final note: '+url+'. '+state+'\n\nOriginal SOURCES.md is preserved in the custody archive. Its earlier negative search is historical and did not locate the exact Ferudun result now credited. The accepted Root priority record is '+baseline['priority']['path']+' (SHA256 '+baseline['priority']['sha256']+'). No current-openness or exhaustive-priority certificate is inferred.\n').encode()
    out['QUALIFIED_PRIORITY.md']=(marker+'# Qualified attribution and chronology\n\n'+credit+'\n\n'+chronology+'\n\n'+scope_text+'\n\n'+effort+'\n\n'+disclosure+'\n\nRoot priority receipt: '+json.dumps(baseline['priority'],sort_keys=True)+'. Actual publication/integration facts are separately bound in CURRENT_STATUS.json; no preparation gate is treated as actual release acceptance.\n').encode()
    for name in ('MANIFEST.json','PUBLICATION_MANIFEST.json'):
        out[name]=enc({'evidence_scope':scope,'scope':'Historical manifest data targets immutable original archive, not changed native presentation','historical_files_root':CASE+'original_submitted_head/','historical_original_manifest':json.loads(old[name]),'historical_manifest_bytes':len(old[name]),'historical_manifest_sha256':digest(old[name]),'current_native_hashes':'SHA256SUMS','current_status':'CURRENT_STATUS.json'})
    out['PUBLICATION_STATUS.md']=(marker+'# Current publication lifecycle\n\n'+state+'\n\n'+theorem+'\n\n'+credit+'\n\nPublication: '+url+'. Tracker range: '+tracker['range']+'. Actual facts and exact Root receipt pins: CURRENT_STATUS.json. Overall research-goal completion is not claimed. Original1/5 effort remains historical metadata. Proposed postimages do not themselves perform an external action.\n').encode()
    out['CURRENT_RESEARCH_LOG.md']=(marker+'# Current native publication record\n\n'+facts['UTC']+' — '+state+' DOI '+doi+'; tracker '+tracker['range']+'. Final package '+package+', seal SHA256 '+seal_pin['sha256']+'. All20 archival originals preserved;15 native scientific/historical files unchanged, five presentation wrappers replaced. Historical RESEARCH_LOG.md remains byte-exact. Theorem valid in the explicit least-period scope; exact theorem/formula/method overlap credited, no novelty or firstness claim. Lifecycle acceptance comes only from the actual Root receipt pins in CURRENT_STATUS.json. This entry states no invented completion percentage, counter or next intake.\n').encode()
    table={n:{'before_bytes':len(b),'before_sha256':digest(b),'after_bytes':len(out[n]),'after_sha256':digest(out[n]),'native_byte_preserved':out[n]==b,'classification':'presentation_wrapper' if n in CHANGED else 'historical_scientific_provenance'} for n,b in sorted(old.items())}
    need({n for n in old if out[n]!=old[n]}==CHANGED,'Unexpected changed native original set')
    out['NATIVE_PRESENTATION_RECEIPT.json']=enc({'evidence_scope':scope,'original_head':HEAD,'all20_original_archive_unchanged':True,'changed_originals':sorted(CHANGED),'preserved_originals':sorted(set(old)-CHANGED),'added_files':sorted(ADDED),'per_original_file_before_after':table,'actual_root_receipt_pins':refs,'side_effects_performed':False})
    out['SHA256SUMS']=''.join(digest(b)+'  '+n+'\n' for n,b in sorted(out.items()) if n!='SHA256SUMS').encode()
    need(set(out)==set(old)|ADDED and len(out)==27,'Unexpected native payload extent')
    need(all(out[n]==old[n] for n in set(old)-CHANGED),'Scientific/historical original changed')
    prefix=('SYNTHETIC_ONLY/' if fixture else '')+NATIVE
    return {prefix+n:b for n,b in out.items()}

def construct(stage, facts):
    """Return real native byte postimages only after all ACTUAL Root receipts pass."""
    return _construct(stage,facts,A,False)

def construct_fixture(stage, facts, fixture_root):
    """Offline tests only. Forced synthetic evidence and output namespace."""
    return _construct(stage,facts,fixture_root,True)
