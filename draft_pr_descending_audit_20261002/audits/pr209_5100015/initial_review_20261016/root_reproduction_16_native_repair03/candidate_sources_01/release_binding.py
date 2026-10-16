"""Pure local bindings for PR209's separately authorized release stages.

No network, Git or CLI calls. Re-reading these records grants no new authority;
actual caller stages must retain their once-only intent and readback guards.
"""
from pathlib import Path
import hashlib
import json
import sys
import os
import fcntl
from urllib.parse import urlsplit
from datetime import datetime, timezone
import re

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Release stages refuse optimized Python: all guards must remain enabled')

ORIGINAL_HEAD='fd09a95b479f376234835a4494693bb1316c85ec'
EXPECTED_DEPOSIT_FILES=[
    {'path':'manuscript.pdf','name':'k303b-outer-center-pedal-areas.pdf'},
    {'path':'k303b-source-verification.zip','name':'k303b-source-verification.zip'},
]
BINDING_KEYS=['clearance_sha256','package_manifest_sha256','deposit_manifest_sha256','metadata_sha256']
HELPERS=['append_verified_tracker.py','integrate_reviewed_pr.py','publish_preprint.py','release_binding.py','verify_and_merge.py','verify_published_readonly.py']
CORE=['SOURCE_MANIFEST.json','PACKAGE_MANIFEST.json','manuscript.tex','manuscript.pdf','metadata.json','deposit.json','k303b-source-verification.zip']
SHEET='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
SHEET_ID=1254632077
FULL_RANGE="'Math Puzzles'!A:D"
HEADER=['Original Problem','Solution Chat URL','DOI','Notes']
CLEAN_VERDICTS={'PASS','CLEAN','NO_FINDINGS','PASS_NO_FINDINGS','PASS_WITH_NO_FINDINGS','CLEAN_NO_FINDINGS'}


def require(value,message):
    if not value:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def save_process_streams(stdout_path,stderr_path,result):
    """Save captured binary streams before any UTF-8 or JSON decoding can fail."""
    stdout=getattr(result,'stdout',None)
    if stdout is None:stdout=getattr(result,'output',None)
    raw=[]
    for path,value in zip([stdout_path,stderr_path],[stdout,getattr(result,'stderr',None)]):
        require(value is None or isinstance(value,(bytes,str)),'Unexpected subprocess stream type')
        body=value if isinstance(value,bytes) else (value or '').encode('utf-8')
        Path(path).write_bytes(body);raw.append(body)
    return raw[0],raw[1]


def file_pin(base,row):
    require(type(row) is dict and set(row)=={'path','bytes','sha256'},'Invalid cleared file pin schema')
    require(type(row['path']) is str and Path(row['path']).name==row['path'],'Cleared paths must be exact local basenames')
    p=base/row['path']
    require(p.is_file() and not p.is_symlink(),'Missing or symlinked cleared file: '+row['path'])
    require(type(row['bytes']) is int and p.stat().st_size==row['bytes'] and digest(p)==row['sha256'],'Cleared file bytes changed: '+row['path'])


def pin(path,base):
    path=Path(path)
    return {'path':path.relative_to(base).as_posix(),'bytes':path.stat().st_size,'sha256':digest(path)}


def checked_path(base,name):
    require(type(name) is str and name and '\\' not in name,'Invalid relative path')
    parts=name.split('/')
    require(all(x not in {'','.','..'} for x in parts) and not Path(name).is_absolute(),'Unsafe relative path')
    p=Path(base)
    for part in parts:
        p=p/part
        require(not p.is_symlink(),'Symlink in retained evidence path: '+name)
    require(p.is_file(),'Missing retained evidence: '+name)
    return p


def pinned(base,row):
    require(type(row) is dict and set(row)=={'path','bytes','sha256'},'Invalid retained pin schema')
    p=checked_path(base,row['path'])
    require(type(row['bytes']) is int and row['bytes']>=0 and p.stat().st_size==row['bytes'] and digest(p)==row['sha256'],'Retained evidence bytes changed: '+row['path'])
    return p


def normalized(row):
    require(type(row) is dict and {'path','bytes','sha256'}<=set(row),'Incomplete payload pin')
    return {k:row[k] for k in ('path','bytes','sha256')}


def utc(value):
    require(type(value) is str,'Missing machine UTC timestamp')
    try:t=datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError as e:raise RuntimeError('Invalid machine UTC timestamp') from e
    require(t.tzinfo is not None and t.utcoffset().total_seconds()==0,'Timestamp must be UTC')
    require(t<=datetime.now(timezone.utc),'Future evidence cannot grant release authority')
    return t


def current_core(root):
    return {name:{k:v for k,v in pin(root/name,root).items() if k!='path'} for name in CORE}


def review_chain(case,entries,kind,expected):
    """Authenticate retained seals, chronology and all dispositions; never infer reviews from counts."""
    require(type(entries) is list and len(entries)>=2,'Two sequential sealed '+kind+' reviews required')
    ids=set();previous_end=None;previous_resolution=None;clean_current=0
    for entry in entries:
        require(type(entry) is dict and {'assessment','authored_manifest','supplements'}<=set(entry),'Incomplete structured review entry')
        ap=pinned(case,entry['assessment']);mp=pinned(case,entry['authored_manifest'])
        require(ap.name=='ASSESSMENT.json' and mp.name=='AUTHORED_MANIFEST.json' and ap.parent==mp.parent,'Assessment/manifest must share a sealed reviewer folder')
        a=load(ap);m=load(mp);folder=ap.parent
        require(a.get('schema')=='pr209-'+('whole-package' if kind=='whole-package' else 'release-helper')+'-assessment-v1','Wrong review assessment schema')
        ident=a.get('review_id') if kind=='whole-package' else a.get('reviewer')
        require(type(ident) is str and ident and ident not in ids,'Review identities must be nonempty and unique')
        ids.add(ident)
        rows=m.get('files');require(type(rows) is list and rows,'Sealed review manifest is empty')
        byname={}
        for row in rows:
            row=normalized(row);require(row['path'] not in byname,'Duplicate review payload')
            pinned(folder,row);byname[row['path']]=row
        require(byname.get('ASSESSMENT.json')==pin(ap,folder) and 'REPORT.md' in byname,'Actual assessment and report must be manifest payloads')
        require(type(entry['supplements']) is list,'Supplements must be explicit pins')
        supplement_hashes=[]
        for supplement_pin in entry['supplements']:
            sp=pinned(case,supplement_pin);require(sp.parent==folder,'Supplement must belong to same review')
            s=load(sp);require(s.get('original_manifest')==pin(mp,folder),'Supplement refers to another original manifest')
            old=s.get('original_payloads_unchanged')
            require(type(old) is list and {r['path']:normalized(r) for r in old}==byname and len(old)==len(byname),'Supplement does not preserve the complete original seal')
            for row in old:pinned(folder,normalized(row))
            extra=s.get('supplemental_payloads');require(type(extra) is list,'Supplement payload list missing')
            for row in extra:
                require(row['path'] not in byname,'Supplement cannot replace an original payload');pinned(folder,normalized(row))
            supplement_hashes.append(supplement_pin['sha256'])
        completed=utc(a.get('completed_utc'))
        if kind=='whole-package':
            require(a.get('review_completed') is True,'Whole-package review incomplete')
            freeze=a.get('evidence',{}).get('freeze');report=a.get('evidence',{}).get('report')
            require(freeze==byname.get(freeze.get('path') if type(freeze) is dict else None),'Actual freeze must be sealed')
            require(report==byname.get('REPORT.md'),'Actual report pin must be sealed')
            f=load(pinned(folder,freeze));frozen=utc(a.get('frozen_utc'))
            require(f.get('frozen_utc')==a['frozen_utc'],'Assessment/freeze UTC differs')
            core=f.get('core')
            require(type(core) in (list,dict),'Frozen core evidence missing')
            if type(core) is list:
                reviewed={r['path']:{k:r[k] for k in ('bytes','sha256')} for r in core}
            else:
                require(all(type(r) is dict and set(r)=={'bytes','sha256'} for r in core.values()),'Invalid keyed frozen core schema')
                reviewed=core
            require(len(core)==len(CORE) and set(reviewed)==set(CORE) and a.get('frozen_bindings')==reviewed,'Assessment/frozen core bindings differ')
        else:
            fp=pinned(case,entry.get('source_freeze'));require(fp.parent==folder and byname.get(fp.name)==pin(fp,folder),'Actual helper source freeze must be sealed')
            f=load(fp);frozen=utc(f.get('frozen_utc'))
            rows=f.get('rows');require(type(rows) is list,'Helper freeze rows missing')
            reviewed=[normalized(r) for r in rows]
            require([r['path'] for r in reviewed]==HELPERS and a.get('frozen_sources')==reviewed,'Helper assessment/freeze source set differs')
            for row in reviewed:require(byname.get(row['path'])==row,'Exact reviewed helper copy is not sealed')
        require(frozen<completed,'Review completion must follow actual freeze')
        if previous_end is not None:
            require(frozen>previous_end,'Next review must freeze after prior completion/resolution')
            if previous_resolution is not None:
                field='package_bindings' if kind=='whole-package' else 'source_bindings'
                require(previous_resolution.get(field)==reviewed,'Next review does not bind the resolved repair snapshot')
        mandatory=a.get('mandatory_findings');optional=a.get('optional_findings')
        require(type(mandatory) is list and type(optional) is list,'Actual finding lists required')
        findings=mandatory+optional
        finding_ids=[r.get('id') for r in findings]
        require(all(type(i) is str and i for i in finding_ids) and len(set(finding_ids))==len(finding_ids),'Invalid finding identities')
        previous_resolution=None;previous_end=completed
        if findings:
            rp=pinned(case,entry.get('resolution'));r=load(rp)
            require(r.get('review_id',r.get('reviewer'))==ident and r.get('review_assessment_sha256')==entry['assessment']['sha256'] and r.get('review_manifest_sha256')==entry['authored_manifest']['sha256'],'Resolution belongs to another review seal')
            resolved=r.get('resolved_findings');require(type(resolved) is list and len(resolved)==len(findings),'Every actual finding requires resolution')
            require({x.get('id') for x in resolved}==set(finding_ids) and all(x.get('status')=='resolved' for x in resolved),'Resolution does not close exactly all actual findings')
            require(r.get('unresolved_mandatory_findings')==[] and r.get('unresolved_optional_findings')==[],'Root resolution retains findings')
            if supplement_hashes:require(r.get('review_report_reference_supplement_sha256') in supplement_hashes or r.get('review_supplement_sha256s')==supplement_hashes,'Resolution omits applicable additive correction seal')
            previous_end=utc(r.get('utc'));require(previous_end>=completed,'Resolution predates actual review completion')
            previous_resolution=r
        else:
            require(a.get('verdict') in CLEAN_VERDICTS,'Final no-finding review needs an explicit clean verdict')
            if reviewed==expected:clean_current+=1
    require(not findings and reviewed==expected,'Final clean review must freeze exact current inputs')
    return len(entries),clean_current


def context(root):
    root=Path(root)
    c=load(root/'FINAL_CLEARANCE.json');p=load(root/'PACKAGE_MANIFEST.json')
    require(c.get('release_cleared') is True,'Final release not cleared')
    require(c.get('unresolved_mandatory_findings')==[] and c.get('unresolved_optional_findings')==[],'Unresolved findings prohibit release')
    require(c.get('original_native_head')==ORIGINAL_HEAD,'Wrong original PR head')
    require(c.get('package_manifest_sha256')==digest(root/'PACKAGE_MANIFEST.json'),'Final package-manifest binding changed')
    require(c.get('deposit_manifest_sha256')==digest(root/'deposit.json'),'Final deposit-manifest binding changed')
    require(c.get('publication_metadata_sha256')==digest(root/'metadata.json'),'Final metadata bytes changed')
    helpers=c.get('release_helpers')
    require(type(helpers) is list and [x.get('path') for x in helpers]==HELPERS,'Exact reviewed release-helper set required')
    for row in helpers:file_pin(root.parent/'publication',row)
    rows=c.get('submission_files')
    require(type(rows) is list and [r.get('path') for r in rows]==[x['path'] for x in EXPECTED_DEPOSIT_FILES],'Wrong cleared file set/order')
    require(rows==p.get('submission_files'),'Package and clearance disagree on submission files')
    for row in rows:file_pin(root,row)
    require(c.get('source_manifest')==p.get('source_manifest'),'Cleared source manifest differs from package')
    require(c.get('manuscript_source')==p.get('manuscript_source'),'Cleared TeX differs from package')
    for key in ['source_manifest','manuscript_source','metadata']:file_pin(root,p[key])
    source=load(root/'SOURCE_MANIFEST.json').get('files')
    require(type(source) is list and source and len({r.get('path') for r in source})==len(source),'Complete unique source manifest required')
    for row in source:pinned(root,row)
    m=load(root/'metadata.json');d=load(root/'deposit.json')
    require(type(d) is dict and set(d)=={'metadata','files'},'Unexpected deposit manifest fields')
    require(d['files']==EXPECTED_DEPOSIT_FILES,'Deposit paths/names differ from the reviewed exact pair')
    require(d['metadata']==m==c.get('publication_metadata'),'Deposit/clearance/current metadata mismatch')
    total,clean=review_chain(root.parent,c.get('whole_package_reviews'),'whole-package',current_core(root))
    review_chain(root.parent,c.get('release_helper_reviews'),'release-helper',helpers)
    require(type(c.get('fresh_manuscript_reviews')) is int and c['fresh_manuscript_reviews']==total,'Manuscript review counter differs from actual sealed chain')
    require(type(c.get('final_frozen_clean_reviews')) is int and c['final_frozen_clean_reviews']==clean and clean>=1,'Clean review counter differs from exact-current sealed evidence')
    expected=[{'name':mapping['name'],'size':row['bytes'],'sha256':row['sha256']} for mapping,row in zip(EXPECTED_DEPOSIT_FILES,rows)]
    result={'clear':c,'metadata':m,'expected_files':expected,'clearance_sha256':digest(root/'FINAL_CLEARANCE.json'),
            'package_manifest_sha256':digest(root/'PACKAGE_MANIFEST.json'),
            'deposit_manifest_sha256':digest(root/'deposit.json'),'metadata_sha256':digest(root/'metadata.json')}
    public_exports(root,root.parent/'publication',result)
    return result


ADMIN_NAMES={
    'PUBLIC_EXPORT_MANIFEST.json','PROGRESS_BASELINE.json','PUBLICATION_PREFLIGHT.json',
    'STAGE_ATTEMPT.json','ZENODO_STAGED_VERIFIED.json','ZENODO_PREPUBLICATION_INSPECT.json',
    'PUBLISH_ATTEMPT.json','ZENODO_TOOL_PUBLICATION_RECEIPT.json','ZENODO_PROVIDER_CONFIRMED_PUBLICATION.json',
    'ZENODO_VERIFIED_PUBLICATION.json','PUBLICATION_VERIFICATION_PENDING.json','TRACKER_VERIFIED_APPEND.json',
    'TRACKER_VERIFICATION_PENDING.json','NATIVE_PREPARE_ATTEMPT.json','NATIVE_REF_UPDATE_ATTEMPT.json',
    'NATIVE_READY_ATTEMPT.json','NATIVE_MERGE_REQUEST.json','NATIVE_MERGE_PENDING.json',
    'NATIVE_COMPLETION_PENDING.json','PR_PREPARED.json','PR_MERGED.json',
    'NATIVE_OBJECT_BUILD_INTENT.json','NATIVE_OBJECTS_BUILT.json','NATIVE_METADATA_ATTEMPT.json',
    'NATIVE_SCIENTIFIC_READBACK.json','NATIVE_MERGE_OBJECT_INTENT.json','NATIVE_MERGE_OBJECTS_BUILT.json',
}


def public_exports(root,pub,ctx):
    """Exact authorized payload only; no broad enumeration can add a public file."""
    root=Path(root);pub=Path(pub);case=root.parent
    manifest_pin=ctx['clear'].get('public_export_manifest')
    require(type(manifest_pin) is dict and manifest_pin.get('path')=='publication/PUBLIC_EXPORT_MANIFEST.json','Explicit public export manifest pin required')
    manifest=load(pinned(case,manifest_pin))
    require(manifest.get('schema')=='pr209-public-export-manifest-v1','Wrong public export schema')
    rows=manifest.get('files');require(type(rows) is list and rows,'Public export set cannot be empty')
    result={}
    forbidden={'__pycache__','node_modules','.git','.venv','venv','env','environment','environments','secrets','credentials','cache','caches','private_transport','private_skill_context'}
    excluded={'preprint/FINAL_CLEARANCE.json','publication/PUBLIC_EXPORT_MANIFEST.json'}|{'publication/'+n for n in ADMIN_NAMES if n!='PROGRESS_BASELINE.json'}
    for row in rows:
        name=row.get('path','');parts=name.split('/')
        require(name not in excluded and all(part and (not part.startswith('.') or part=='.gitignore') and not part.lower().startswith(('private','secret','credential')) and part.lower().split('.')[0] not in forbidden and not part.lower().endswith('.env') for part in parts),'Private, mutable or self-referential public export rejected: '+name)
        require(name not in result,'Duplicate public export')
        result[name]=pinned(case,row).read_bytes()
    source_names={r['path'].split('/')[0] for r in load(root/'SOURCE_MANIFEST.json')['files']}
    allowed_root=source_names|set(CORE)|{'FINAL_CLEARANCE.json'}
    # The separately frozen compiler log is outside SOURCE_MANIFEST. Its exact
    # cleared public-export pin is required; no other unsealed top file is added.
    if 'preprint/manuscript.log' in result:allowed_root.add('manuscript.log')
    allowed_pub=set(HELPERS)|{'adapt_release_helpers.py','HELPER_SOURCE_ADAPTATION.json'}|ADMIN_NAMES
    for folder,allowed in [(root,allowed_root),(pub,allowed_pub)]:
        for p in folder.iterdir():
            if p.is_file() or p.is_symlink():require(p.name in allowed and not p.is_symlink(),'Unexpected top-level release file: '+str(p))
    return result


def binding(ctx):
    return {key:ctx[key] for key in BINDING_KEYS}


def unchanged(root,previous):
    current=context(root)
    require(binding(current)==binding(previous) and current['expected_files']==previous['expected_files'],'Release inputs changed during stage; reconcile read-only')
    return current


def publication(root,pub,ctx=None):
    ctx=context(root) if ctx is None else unchanged(root,ctx)
    lineage=publication_lineage(root,pub,ctx,complete=True)
    z=load(Path(pub)/'ZENODO_VERIFIED_PUBLICATION.json')
    require(z.get('lineage')==lineage,'Verified publication lacks complete exact durable ancestry')
    require(z.get('submitted') is True and z.get('metadata_and_files_verified') is True,'Published files not fully verified')
    require(z.get('exact_reviewed_frozen_files_published') is True,'Exact cleared publication not verified')
    require(z.get('release_binding')==binding(ctx),'Published receipt belongs to different clearance/inputs')
    provider=load(Path(pub)/'ZENODO_PROVIDER_CONFIRMED_PUBLICATION.json')
    require(z.get('id')==provider.get('id') and z.get('tool_postpublication_readback')==provider.get('tool_readback'),'Verified publication differs from retained provider readback')
    for key in ['doi','doi_url','record_url','doi_resolution']:
        require(z.get(key)==provider['tool_readback'].get(key),'Verified publication identity/DOI readback differs')
    require(z.get('metadata')==ctx['metadata'] and z.get('files')==ctx['expected_files'],'Published file/metadata set differs from current clearance')
    require(z.get('additional_public_readback_error') is None,'Public SHA256 readback remains unresolved')
    downloads=z.get('additional_actual_public_file_downloads')
    require(type(downloads) is list and len(downloads)==2,'Both actual public file downloads required')
    require(len({r.get('file') for r in downloads})==2,'Duplicate public file readback')
    byname={r['file']:r for r in downloads}
    for expected in ctx['expected_files']:
        r=byname.get(expected['name'],{})
        require(r.get('actual_public_download_byte_hash_match') is True and r.get('bytes')==expected['size'] and r.get('sha256')==expected['sha256'],'Actual public SHA256 binding failed')
        raw=pinned(Path(root).parent,r.get('payload')).read_bytes()
        require(len(raw)==expected['size'] and hashlib.sha256(raw).hexdigest()==expected['sha256'] and r.get('url')==z['record_url']+'/files/'+expected['name']+'?download=1','Actual retained public-byte readback differs')
    require(type(z.get('id')) is int and z['id']>0,'Invalid Zenodo record identity')
    require(z.get('doi')=='10.5281/zenodo.'+str(z['id']),'DOI/version identity mismatch')
    require(z.get('doi_url')=='https://doi.org/'+z['doi'] and z.get('record_url')=='https://zenodo.org/records/'+str(z['id']),'DOI or record URL mismatch')
    verify_doi(z)
    return z


def tool_publication(v,ctx,record_id,state='published'):
    require(type(v) is dict and v.get('environment')=='production' and v.get('title')==ctx['metadata']['title'],'Provider metadata/environment differs from cleared manifest')
    require(v.get('id')==record_id and type(v.get('id')) is int and v['id']>0 and v.get('state')==state,'Provider record/state identity differs')
    require(v.get('files')==ctx['expected_files'],'Provider file set differs from clearance')


def publication_lineage(root,pub,ctx,complete=False):
    """Acyclic intent -> stage -> inspect -> publish -> tool -> provider -> verified chain."""
    pub=Path(pub)
    names=['STAGE_ATTEMPT.json','ZENODO_STAGED_VERIFIED.json','ZENODO_PREPUBLICATION_INSPECT.json','PUBLISH_ATTEMPT.json']
    records={n:load(checked_path(pub,n)) for n in names}
    s=records[names[0]];st=records[names[1]];before=records[names[2]];a=records[names[3]]
    for n,r in records.items():
        require(r.get('release_binding')==binding(ctx) and r.get('metadata')==ctx['metadata'] and r.get('files')==ctx['expected_files'],'Publication ancestry differs from current clearance: '+n)
        utc(r.get('utc'))
    require(s.get('operation')=='single stage about to be attempted','Wrong stage intent operation')
    preflight=load(pinned(Path(root).parent,s.get('preflight')))
    require(preflight.get('release_binding')==binding(ctx) and preflight.get('head')==ORIGINAL_HEAD and preflight.get('QUEUE_status')=='claimed_solved' and preflight.get('existing_problem_tracker_rows')==[],'Publication preflight ancestry differs')
    preflight_meta=load(pinned(Path(root).parent,preflight.get('tracker_properties')))
    preflight_scan=load(pinned(Path(root).parent,preflight.get('tracker_scan')))
    preflight_values=tracker_readback(preflight_scan,FULL_RANGE,preflight_meta)
    require(preflight_values and preflight_values[0]==HEADER and not any('AMR-050-0015' in str(v) or '5100015' in str(v) for row in preflight_values for v in row),'Retained publication tracker preflight is incomplete/conflicting')
    require(st.get('stage_attempt_sha256')==digest(pub/names[0]),'Staged receipt omits exact stage intent')
    record_id=st.get('id');require(type(record_id) is int and record_id>0,'Invalid staged identity')
    tool_publication(st.get('tool_readback'),ctx,record_id,'ready_to_publish')
    require(st.get('state')=='ready_to_publish' and before.get('id')==record_id and type(before.get('id')) is int and a.get('id')==record_id and type(a.get('id')) is int,'Stage/publish identity lineage differs')
    require(before.get('staged_receipt_sha256')==digest(pub/names[1]),'Prepublication readback lacks exact staged ancestor')
    tool_publication(before.get('tool_readback'),ctx,record_id,'ready_to_publish')
    require(a.get('operation')=='single publish about to be attempted' and a.get('staged_receipt_sha256')==digest(pub/names[1]) and a.get('prepublication_inspect_sha256')==digest(pub/names[2]),'Publish intent lacks exact verified stage/readback lineage')
    require(utc(s['utc'])<=utc(st['utc'])<=utc(before['utc'])<=utc(a['utc']),'Publication ancestry chronology differs')
    if complete:
        names+=['ZENODO_TOOL_PUBLICATION_RECEIPT.json','ZENODO_PROVIDER_CONFIRMED_PUBLICATION.json']
        tr=load(checked_path(pub,names[-2]));provider=load(checked_path(pub,names[-1]))
        for r in [tr,provider]:
            require(r.get('release_binding')==binding(ctx) and r.get('id')==record_id and type(r.get('id')) is int and r.get('metadata')==ctx['metadata'] and r.get('files')==ctx['expected_files'],'Publication readback ancestry differs')
            require(r.get('publish_attempt_sha256')==digest(pub/'PUBLISH_ATTEMPT.json'),'Publication readback lacks publish intent pin')
            tool_publication(r.get('tool_readback'),ctx,record_id)
        require(tr.get('source') in {'publish-tool','read-only-recovery'} and provider.get('submitted') is True,'Publication tool/provider receipt incomplete')
        require(provider.get('tool_publication_receipt_sha256')==digest(pub/names[-2]),'Provider receipt lacks tool publication ancestor')
        require(utc(a['utc'])<=utc(tr.get('utc'))<=utc(provider.get('utc')),'Published receipt chronology differs')
    return {n:digest(pub/n) for n in names}


def verify_doi(z):
    d=z.get('doi_resolution',{})
    u=urlsplit(d.get('resolved_url',''))
    require(d.get('status')=='resolved' and type(d.get('http_status')) is int and 200<=d['http_status']<300,'DOI resolution is still pending')
    require(d.get('url')==z.get('doi_url') and u.scheme=='https' and u.netloc=='zenodo.org' and not u.query and not u.fragment and u.path.rstrip('/')=='/records/'+str(z.get('id')),'DOI did not resolve to the verified version record')


def tracker(root,pub,ctx=None,z=None):
    ctx=context(root) if ctx is None else unchanged(root,ctx)
    actual=publication(root,pub,ctx)
    if z is not None:require(actual==z,'Publication receipt changed since preceding check')
    t=load(Path(pub)/'TRACKER_VERIFIED_APPEND.json')
    require(t.get('verified') is True and t.get('exact_all_four_cells_readback') is True,'Four-cell tracker readback missing')
    require(t.get('release_binding')==binding(ctx),'Tracker receipt belongs to another clearance')
    require(t.get('publication_receipt_sha256')==digest(Path(pub)/'ZENODO_VERIFIED_PUBLICATION.json'),'Tracker belongs to another publication receipt')
    require(t.get('doi_url')==actual['doi_url'],'Tracker DOI differs from verified publication')
    require(t.get('spreadsheet_id')=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and t.get('sheet_id')==1254632077,'Wrong tracker destination')
    values=expected_tracker_row(ctx,actual)
    require(t.get('values')==values,'Tracker payload differs from exact cleared metadata and publication')
    target=t.get('updated_range');target_row=tracker_row_number(target)
    require(type(t.get('append_count')) is int and t['append_count'] in (0,1),'Append invocation count must be exactly zero or one')
    require(t.get('reconciled_existing_attempt') is (t['append_count']==0),'Tracker reconciliation mode/count differs')
    attempt=Path(pub)/'private_transport/tracker/APPEND_ATTEMPT.json'
    validate_append_attempt(load(checked_path(Path(pub),'private_transport/tracker/APPEND_ATTEMPT.json')),ctx,actual,Path(pub))
    require(t.get('append_attempt_sha256')==digest(attempt),'Tracker receipt lacks exact append intent')
    evidence=t.get('evidence');require(type(evidence) is dict,'Retained tracker readbacks required')
    case=Path(root).parent
    properties=load(pinned(case,evidence.get('properties')));tracker_properties(properties)
    properties_before=load(pinned(case,evidence.get('properties_before')));tracker_properties(properties_before)
    before=load(pinned(case,evidence.get('before_scan')))
    before_values=tracker_readback(before,FULL_RANGE,properties_before)
    readback=load(pinned(case,evidence.get('target_readback')))
    require(tracker_readback(readback,target,properties)==[values],'Retained exact target four-cell readback differs')
    after=load(pinned(case,evidence.get('after_scan')))
    require_unique_tracker(tracker_readback(after,FULL_RANGE,properties),values,actual,target_row)
    if t['append_count']==1:
        require(tracker_matches(before_values,values,actual)==([],[]),'Append preflight already contained this problem/DOI')
        response=load(pinned(case,evidence.get('append_result')));validate_append_result(response,values,target)
    else:
        require(evidence.get('reconciliation_before')==evidence.get('before_scan'),'Reconciliation does not pin original complete preflight')
        before=load(pinned(case,evidence.get('reconciliation_before')))
        require_unique_tracker(tracker_readback(before,FULL_RANGE,properties_before),values,actual,target_row)
    require(utc(t.get('utc'))>=utc(load(attempt).get('utc')),'Tracker completion predates its attempt')
    return t


def expected_tracker_row(ctx,z):
    m=ctx['metadata']
    require(all(type(m.get(k)) is str and m[k] for k in ['title','version','publication_date']),'Cleared title/version/date required for tracker')
    notes=m['title']+' — Alec Kriebel, v'+m['version']+','+m['publication_date']+'. AMR-050-0015 /5100015 /k303,b. Signed product of outer tangent-polygon area and actual perpendicular-center-foot area on its boundary tangent side LINES; strict nondegenerate confocal elliptical caustic, periods not divisible by four, admitted coprime stars, reversal and fixed repeats(d²); circle separate. Explicit fixed-linear edge-vector map and classical odd cyclic Jacobi identity give a full all-phase proof and constant. KLS2002, KS2003/2004, AST/BT2020, Stachel/Jacobi/conic and established pole methods credited. A.Ferudun2026v1.1 Theorem2/Section6 DOI10.5281/zenodo.23088516 is the exact full contemporary theorem; v1.0 centered primitive even subset distinguished. Historical ordering, independent non-derivation and novelty undetermined; no first-proof/exclusive/new-identity/current-worldwide-open claim. Required fresh sequential whole-package reviews/global fixes completed before deposit; portable eight-suite exact/uncertified numerical controls, originals and correction evidence retained. Extensive AI use; unrefereed, no independent human peer review/formal proof verification. PR:https://github.com/AlecKriebel/Math/pull/209'
    return ['https://arxiv.org/abs/2004.12497v11','',z['doi_url'],notes]


def tracker_row_number(target):
    require(type(target) is str,'Tracker target range missing')
    match=re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D\1",target)
    require(match is not None and int(match.group(1))>=2,'Tracker range must be canonical one-row Math Puzzles A:D')
    return int(match.group(1))


def tracker_properties(meta):
    require(type(meta) is dict and type(meta.get('sheets')) is list,'Tracker tab metadata missing')
    tabs=[s.get('properties',{}) for s in meta['sheets'] if s.get('properties',{}).get('sheetId')==SHEET_ID]
    require(len(tabs)==1 and tabs[0].get('title')=='Math Puzzles','Wrong tracker tab identity')
    require(meta.get('spreadsheetId')==SHEET,'Wrong spreadsheet readback identity')
    tab=tabs[0];grid=tab.get('gridProperties',{})
    require(tab.get('sheetType','GRID')=='GRID','Tracker tab is not a grid')
    require(type(grid.get('rowCount')) is int and grid['rowCount']>=2 and type(grid.get('columnCount')) is int and grid['columnCount']>=4,'Authenticated tracker grid dimensions missing')
    return grid['rowCount']


def tracker_readback(record,target,properties):
    require(type(record) is dict and record.get('request')=={'spreadsheetId':SHEET,'range':target} and type(record.get('response')) is dict,'Retained tracker request/readback identity differs')
    grid_rows=tracker_properties(properties);response=record['response']
    require(response.get('majorDimension')=='ROWS','Tracker response must explicitly use ROWS')
    require(type(response.get('range')) is str,'Tracker response range identity missing')
    match=re.fullmatch(r"'Math Puzzles'!A([1-9][0-9]*):D([1-9][0-9]*)",response.get('range',''))
    require(match is not None,'Tracker response tab/column/range identity differs')
    first,last=map(int,match.groups())
    if target==FULL_RANGE:
        require(first==1 and last==grid_rows,'Tracker full response does not cover complete authenticated A:D grid')
    else:
        row=tracker_row_number(target)
        require(first==last==row and row<=grid_rows,'Tracker response target row differs from exact grid target')
    values=response.get('values',[])
    require(type(values) is list and len(values)<=last-first+1 and all(type(row) is list and len(row)<=4 for row in values),'Invalid tracker values response coverage')
    return values


def tracker_matches(values,row,z):
    require(type(values) is list and values and values[0]==HEADER,'Tracker headers or full scan missing')
    problem=re.compile(r'(?<![0-9])5100015(?![0-9])|AMR-050-0015',re.I)
    problems=[(i,r) for i,r in enumerate(values,1) if any(problem.search(str(c)) for c in r)]
    dois=[(i,r) for i,r in enumerate(values,1) if any(z['doi'] in str(c) for c in r)]
    return problems,dois


def require_unique_tracker(values,row,z,target_row):
    problems,dois=tracker_matches(values,row,z)
    require(problems==dois==[(target_row,row)],'Tracker uniqueness conflict; retain pending evidence and reconcile read-only')


def validate_append_attempt(a,ctx,z,pub):
    require(a.get('release_binding')==binding(ctx) and a.get('publication_receipt_sha256')==digest(Path(pub)/'ZENODO_VERIFIED_PUBLICATION.json'),'Append intent belongs to another cleared publication')
    require(a.get('spreadsheet_id')==SHEET and a.get('sheet_id')==SHEET_ID and a.get('range')==FULL_RANGE and a.get('doi_url')==z['doi_url'],'Append intent destination/DOI differs')
    require(a.get('payload')=={'majorDimension':'ROWS','values':[expected_tracker_row(ctx,z)]} and a.get('status')=='single append about to be attempted','Append intent exact payload/status differs')
    utc(a.get('utc'))


def validate_append_result(result,row,target):
    update=result.get('updates',{})
    require(update.get('updatedRows')==1 and type(update.get('updatedRows')) is int and update.get('updatedCells')==4 and type(update.get('updatedCells')) is int and update.get('updatedData',{}).get('values')==[row] and update.get('updatedRange')==target,'Append response differs from exact one-row four-cell payload')
    if 'spreadsheetId' in result:require(result['spreadsheetId']==SHEET,'Append response spreadsheet differs')
    if 'range' in update.get('updatedData',{}):require(update['updatedData']['range']==target,'Append response cell range differs')
    tracker_row_number(target)


def acquire(pub):
    """Caller retains this handle for the whole workflow; all stages share the lock."""
    path=Path(pub)/'private_transport/release.lock';durable_mkdir(path.parent)
    handle=path.open('a+')
    try:fcntl.flock(handle.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close();raise RuntimeError('Another release stage is active; no parallel action allowed')
    return handle


def exclusive_json(path,data):
    """Atomic first-writer intent, flushed before the associated provider mutation."""
    with Path(path).open('x') as f:
        f.write(json.dumps(data,indent=2)+'\n');f.flush();os.fsync(f.fileno())
    sync_directory(Path(path).parent)


def pr_identity(pr,head,draft=None,state='open'):
    require(pr.get('number')==209 and pr.get('state')==state,'Wrong PR/state')
    require(pr.get('head',{}).get('sha')==head and pr['head'].get('ref')=='dot/math-5100015','Wrong expected native head/branch')
    require(pr['head'].get('repo',{}).get('full_name')=='AlecKriebel/Math','Wrong head repository')
    require(pr.get('base',{}).get('ref')=='main' and pr['base'].get('repo',{}).get('full_name')=='AlecKriebel/Math','Wrong base repository/branch')
    if draft is not None:require(pr.get('draft') is draft,'Wrong draft state')


def sync_directory(path):
    """Fail closed when the supported OS cannot sync a directory entry."""
    fd=os.open(str(path),os.O_RDONLY|getattr(os,'O_DIRECTORY',0))
    try:os.fsync(fd)
    finally:os.close(fd)


def durable_mkdir(path,exist_ok=True):
    """Sync every newly created ancestor linkage, including a retry anchor."""
    path=Path(path);missing=[];anchor=path
    while not anchor.exists():missing.append(anchor);anchor=anchor.parent
    require(anchor.is_dir(),'Directory anchor is not a directory')
    if not missing and not exist_ok:raise FileExistsError(str(path))
    # An earlier failed sync can leave the anchor visible but not confirmed durable.
    sync_directory(anchor.parent)
    for new in reversed(missing):
        new.mkdir(exist_ok=exist_ok if new==path else True)
        sync_directory(new.parent)
    require(path.is_dir(),'Required durable directory is missing')
