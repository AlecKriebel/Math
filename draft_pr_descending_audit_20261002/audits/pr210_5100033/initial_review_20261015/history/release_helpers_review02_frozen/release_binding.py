"""Pure local bindings for PR210's separately authorized release stages.

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

if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Release stages refuse optimized Python: all guards must remain enabled')

ORIGINAL_HEAD='2180d64b648b81ac660a792f7823d0b715f9cf12'
EXPECTED_DEPOSIT_FILES=[
    {'path':'manuscript.pdf','name':'k605a-outer-focal-pedal-areas.pdf'},
    {'path':'k605a-source-verification.zip','name':'k605a-source-verification.zip'},
]
BINDING_KEYS=['clearance_sha256','package_manifest_sha256','deposit_manifest_sha256','metadata_sha256']


def require(value,message):
    if not value:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def file_pin(base,row):
    require(type(row) is dict and set(row)=={'path','bytes','sha256'},'Invalid cleared file pin schema')
    require(type(row['path']) is str and Path(row['path']).name==row['path'],'Cleared paths must be exact local basenames')
    p=base/row['path']
    require(p.is_file() and not p.is_symlink(),'Missing or symlinked cleared file: '+row['path'])
    require(type(row['bytes']) is int and p.stat().st_size==row['bytes'] and digest(p)==row['sha256'],'Cleared file bytes changed: '+row['path'])


def context(root):
    root=Path(root)
    c=load(root/'FINAL_CLEARANCE.json');p=load(root/'PACKAGE_MANIFEST.json')
    require(c.get('release_cleared') is True,'Final release not cleared')
    require(type(c.get('fresh_manuscript_reviews')) is int and c['fresh_manuscript_reviews']>=2,'Two NEW sequential manuscript reviews required')
    require(type(c.get('final_frozen_clean_reviews')) is int and c['final_frozen_clean_reviews']>=1,'Final frozen clean review required')
    require(c.get('unresolved_mandatory_findings')==[] and c.get('unresolved_optional_findings')==[],'Unresolved findings prohibit release')
    require(c.get('original_native_head')==ORIGINAL_HEAD,'Wrong original PR head')
    require(c.get('package_manifest_sha256')==digest(root/'PACKAGE_MANIFEST.json'),'Final package-manifest binding changed')
    require(c.get('deposit_manifest_sha256')==digest(root/'deposit.json'),'Final deposit-manifest binding changed')
    require(c.get('publication_metadata_sha256')==digest(root/'metadata.json'),'Final metadata bytes changed')
    helper_names=['append_verified_tracker.py','integrate_reviewed_pr.py','publish_preprint.py','release_binding.py','verify_and_merge.py','verify_published_readonly.py']
    helpers=c.get('release_helpers')
    require(type(helpers) is list and [x.get('path') for x in helpers]==helper_names,'Exact reviewed release-helper set required')
    for row in helpers:file_pin(root.parent/'publication',row)
    rows=c.get('submission_files')
    require(type(rows) is list and [r.get('path') for r in rows]==[x['path'] for x in EXPECTED_DEPOSIT_FILES],'Wrong cleared file set/order')
    require(rows==p.get('submission_files'),'Package and clearance disagree on submission files')
    for row in rows:file_pin(root,row)
    require(c.get('source_manifest')==p.get('source_manifest'),'Cleared source manifest differs from package')
    require(c.get('manuscript_source')==p.get('manuscript_source'),'Cleared TeX differs from package')
    for key in ['source_manifest','manuscript_source','metadata']:file_pin(root,p[key])
    m=load(root/'metadata.json');d=load(root/'deposit.json')
    require(type(d) is dict and set(d)=={'metadata','files'},'Unexpected deposit manifest fields')
    require(d['files']==EXPECTED_DEPOSIT_FILES,'Deposit paths/names differ from the reviewed exact pair')
    require(d['metadata']==m==c.get('publication_metadata'),'Deposit/clearance/current metadata mismatch')
    expected=[{'name':mapping['name'],'size':row['bytes'],'sha256':row['sha256']} for mapping,row in zip(EXPECTED_DEPOSIT_FILES,rows)]
    return {'clear':c,'metadata':m,'expected_files':expected,'clearance_sha256':digest(root/'FINAL_CLEARANCE.json'),
            'package_manifest_sha256':digest(root/'PACKAGE_MANIFEST.json'),
            'deposit_manifest_sha256':digest(root/'deposit.json'),'metadata_sha256':digest(root/'metadata.json')}


def binding(ctx):
    return {key:ctx[key] for key in BINDING_KEYS}


def unchanged(root,previous):
    current=context(root)
    require(binding(current)==binding(previous) and current['expected_files']==previous['expected_files'],'Release inputs changed during stage; reconcile read-only')
    return current


def publication(root,pub,ctx=None):
    ctx=context(root) if ctx is None else unchanged(root,ctx)
    z=load(Path(pub)/'ZENODO_VERIFIED_PUBLICATION.json')
    require(z.get('submitted') is True and z.get('metadata_and_files_verified') is True,'Published files not fully verified')
    require(z.get('exact_reviewed_frozen_files_published') is True,'Exact cleared publication not verified')
    require(z.get('release_binding')==binding(ctx),'Published receipt belongs to different clearance/inputs')
    require(z.get('metadata')==ctx['metadata'] and z.get('files')==ctx['expected_files'],'Published file/metadata set differs from current clearance')
    require(z.get('additional_public_readback_error') is None,'Public SHA256 readback remains unresolved')
    downloads=z.get('additional_actual_public_file_downloads')
    require(type(downloads) is list and len(downloads)==2,'Both actual public file downloads required')
    require(len({r.get('file') for r in downloads})==2,'Duplicate public file readback')
    byname={r['file']:r for r in downloads}
    for expected in ctx['expected_files']:
        r=byname.get(expected['name'],{})
        require(r.get('actual_public_download_byte_hash_match') is True and r.get('bytes')==expected['size'] and r.get('sha256')==expected['sha256'],'Actual public SHA256 binding failed')
    require(type(z.get('id')) is int and z['id']>0,'Invalid Zenodo record identity')
    require(z.get('doi')=='10.5281/zenodo.'+str(z['id']),'DOI/version identity mismatch')
    require(z.get('doi_url')=='https://doi.org/'+z['doi'] and z.get('record_url')=='https://zenodo.org/records/'+str(z['id']),'DOI or record URL mismatch')
    verify_doi(z)
    return z


def verify_doi(z):
    d=z.get('doi_resolution',{})
    u=urlsplit(d.get('resolved_url',''))
    require(d.get('status')=='resolved' and type(d.get('http_status')) is int and 200<=d['http_status']<300,'DOI resolution is still pending')
    require(d.get('url')==z.get('doi_url') and u.scheme=='https' and u.hostname=='zenodo.org' and u.path.rstrip('/')=='/records/'+str(z.get('id')),'DOI did not resolve to the verified version record')


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
    values=t.get('values')
    require(type(values) is list and len(values)==4 and all(type(x) is str for x in values),'Invalid tracker cells')
    require(values[0]=='https://arxiv.org/abs/2004.12497v11' and values[1]=='' and values[2]==actual['doi_url'],'Wrong tracker source/solution/DOI values')
    require('5100033' in values[3] and ctx['metadata']['title'] in values[3],'Wrong tracked problem/title')
    return t


def acquire(pub):
    """Caller retains this handle for the whole workflow; all stages share the lock."""
    path=Path(pub)/'private_transport/release.lock';path.parent.mkdir(parents=True,exist_ok=True)
    handle=path.open('a+')
    try:fcntl.flock(handle.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close();raise RuntimeError('Another release stage is active; no parallel action allowed')
    return handle


def exclusive_json(path,data):
    """Atomic first-writer intent, flushed before the associated provider mutation."""
    with Path(path).open('x') as f:
        f.write(json.dumps(data,indent=2)+'\n');f.flush();os.fsync(f.fileno())


def pr_identity(pr,head,draft=None,state='open'):
    require(pr.get('number')==210 and pr.get('state')==state,'Wrong PR/state')
    require(pr.get('head',{}).get('sha')==head and pr['head'].get('ref')=='dot/math-5100033','Wrong expected native head/branch')
    require(pr['head'].get('repo',{}).get('full_name')=='AlecKriebel/Math','Wrong head repository')
    require(pr.get('base',{}).get('ref')=='main' and pr['base'].get('repo',{}).get('full_name')=='AlecKriebel/Math','Wrong base repository/branch')
    if draft is not None:require(pr.get('draft') is draft,'Wrong draft state')
