"""Passive finite private-writer closure; does not rebuild or publish anything."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
A=P/'verification/binary-gram-locus-editorial-sol-20261117'
S=P/'papers/23318851/sources'
I=P/'papers/23318851/reviews/adversarial-sol'
C=P/'papers/23318851/reviews/adversarial-continuation-20261117'
TERMINALS={'FINAL_MANIFEST.json','FINAL_SEAL.json'}
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(v):return (json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode()
def snap(root):
    rows=[]
    for p in [root,*sorted(root.rglob('*'))]:
        st=p.lstat();r={'path':'.' if p==root else str(p.relative_to(root)),
            'mode':oct(stat.S_IMODE(st.st_mode)),'hidden':any(x.startswith('.') for x in p.relative_to(root).parts)}
        if stat.S_ISDIR(st.st_mode):r.update(kind='directory',empty=not any(p.iterdir()))
        elif stat.S_ISREG(st.st_mode):
            b=p.read_bytes();r.update(kind='file',bytes=len(b),SHA256=sha(b))
        else:r.update(kind='other',target=os.readlink(p) if p.is_symlink() else None)
        rows.append(r)
    return rows
def counts(rows):return {'files':sum(r['kind']=='file' for r in rows),
    'child_directories':sum(r['kind']=='directory' for r in rows)-1,
    'hidden_paths':sum(r['hidden'] for r in rows),
    'empty_directories':[r['path'] for r in rows if r['kind']=='directory' and r['empty']],
    'empty_files':[r['path'] for r in rows if r['kind']=='file' and r['bytes']==0]}
assert not (A/'FINAL.json').exists() and not any((A/n).exists() for n in TERMINALS)
before=json.loads((A/'CUSTODY_BEFORE.json').read_text());after=json.loads((A/'CUSTODY_AFTER.json').read_text())
for key,root,nfiles,ndirs in [('source',S,95,16),('INITIAL',I,18,1),('continuation',C,98,10)]:
    assert before[key]==after[key]==snap(root),key
    assert counts(before[key])['files']==nfiles and counts(before[key])['child_directories']==ndirs
assert before['specific_inputs']==after['specific_inputs']
for r in before['specific_inputs']:
    p=Path(r['path']);b=p.read_bytes()
    assert len(b)==r['bytes'] and sha(b)==r['SHA256'] and oct(stat.S_IMODE(p.lstat().st_mode))==r['mode']
run=json.loads((A/'BUILDER_RUN.json').read_text());build=json.loads((A/'BUILD_RECEIPT.json').read_text())
model=json.loads((A/'MODEL.json').read_text())
assert run['attempts']==1 and run['exit']==0 and run['repairs_retries']==0
for stem in ['stdout','stderr']:
    b=(A/('BUILDER.'+stem+'.bin')).read_bytes()
    assert len(b)==run[stem+'_bytes'] and sha(b)==run[stem+'_SHA256']
assert run['stdout_bytes']==446 and run['stderr_bytes']==0
assert sha((A/'private-page/index.html').read_bytes())==build['page_SHA256']
assert sha((A/'MODEL.json').read_bytes())==build['model_SHA256']
assert model['private_only'] is True and model['publication_authority'] is False
null_fields=['actual_canonical','base_url','production_url','page_publication_date','AA','legacy_redirect','follow_up']
assert all(model[k] is None for k in null_fields)
assert model['robots']=='noindex, nofollow'
assets=model['native_assets_in_original_order']
assert [r['native_filename'] for r in assets]==['gram_locus_note.pdf','gram_locus_support.zip']
for r in assets:
    b=(A/'private-page'/r['local_filename']).read_bytes()
    assert len(b)==r['bytes'] and sha(b)==r['SHA256']
    assert b==(S/'zenodo-files'/r['native_filename']).read_bytes()
assert sha((A/'private-page/research.css').read_bytes())==model['stylesheet']['SHA256']
assert build['abstract_full_normalization_exact'] and build['single_ScholarlyArticle'] and build['parser_checks_passed']
assert model['native_publication_date']=='2026-10-12' and model['native_version']=='1.0.0'
now=datetime.now(timezone.utc).isoformat()
with (A/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+now+': Complete source95/16, INITIAL18/1, continuation98/10 and specific approval/review/CSS after-guards exact. Private writer100%; one builder exit0, no retries. Entire actual generated HTML/model/Bib read, native assets and shared CSS unchanged. Terminal finite manifest/seal closes this lane; publicationauthorityfalse and canonical/base/production/page-date/AA/legacy/follow-up remainnull. Stop for root copy/fact/legacy decisions.\n')
final={'UTC':now,'row':194,'record':'23318851','status':'PRIVATE_EDITORIAL_WRITER_COMPLETE',
    'completion_percent':100,'completion_scope':'Writer only; no publication or independent fact/legacy/live certificate',
    'publication_authority':False,'private_only':True,'proposed_slug':model['proposed_slug'],
    **{k:None for k in null_fields},'robots':'noindex, nofollow',
    'private_page':'private-page/index.html','model':'MODEL.json','report':'EDITORIAL_REPORT.md',
    'page_SHA256':build['page_SHA256'],'model_SHA256':build['model_SHA256'],
    'source95_16_INITIAL18_1_continuation98_10_complete_exact':True,
    'SOURCE_FINAL_SHA256':'c61fb0473f0954877ab5af49e7b6139732eb4afab7cfab3377864a91dd98b317',
    'SOURCE_MANIFEST_SHA256':'ed5c217040b7a0d72df7de7ef1d5cbce9bc516ab32c1f20ed6466ef153a6bac8',
    'root_clearance_SHA256':build['root_clearance_SHA256'],'root_review_SHA256':build['root_review_SHA256'],
    'native_assets_in_original_order':assets,'full_abstract_exact_with_declared_replacements':True,
    'normalized_abstract_SHA256':model['abstract']['normalized_SHA256'],
    'one_ScholarlyArticle_and_citation_metadata':True,'shared_CSS_unchanged':True,
    'CSS_SHA256':model['stylesheet']['SHA256'],'builder_attempts':1,'builder_exit':0,
    'builder_stdout_bytes':446,'builder_stderr_bytes':0,'builder_repairs_retries':0,
    'old_review_or_source_mutations':0,'website_mutations':0,'website_guard_scope':'Specific CSS only; no whole website guard',
    'network_Git_Sheet_redirect_deploy_release_Zenodo_operations':0,
    'scientific_source_execution':0,'external_contact_outreach':0,
    'scope_limits':['No live or browser certificate','No canonical route binding','No legacy correspondence or redirect certification','No publication authorization'],
    'stop':True}
(A/'FINAL.json').write_bytes(enc(final))
for n in TERMINALS:(A/n).write_bytes(b'')
rows=snap(A);assert not any(r['kind']=='other' for r in rows)
for r in rows:
    if r['path'] in TERMINALS:r['SHA256']='EXCLUDED_TERMINAL_RECURSIVE_HASH'
scope=counts(rows);scope['empty_files']=[n for n in scope['empty_files'] if n not in TERMINALS]
assert scope['files']==21 and scope['child_directories']==1
manifest={'UTC':now,'root':str(A),**scope,'actual_all_bytes_modes_hidden_empty_topology':True,
    'only_recursive_hash_exclusions':sorted(TERMINALS),'entries':rows}
seal={'UTC':now,'frozen':True,'root':str(A),**scope,'manifest_bytes':0,'manifest_SHA256':'0'*64,
    'FINAL_SHA256':sha((A/'FINAL.json').read_bytes()),'page_SHA256':build['page_SHA256'],'model_SHA256':build['model_SHA256'],
    'CUSTODY_BEFORE_SHA256':sha((A/'CUSTODY_BEFORE.json').read_bytes()),
    'CUSTODY_AFTER_SHA256':sha((A/'CUSTODY_AFTER.json').read_bytes()),
    'source95_16_INITIAL18_1_continuation98_10_exact':True,'builder_attempts':1,'builder_exit':0,
    'only_recursive_hash_exclusions':sorted(TERMINALS),'seal_SHA256':'EXCLUDED_TERMINAL_RECURSIVE_HASH',
    'completion_percent':100,'publication_authority':False,'follow_up':None,'stop':True}
for _ in range(20):
    mb=enc(manifest);seal['manifest_bytes']=len(mb);seal['manifest_SHA256']=sha(mb);sb=enc(seal)
    sizes={'FINAL_MANIFEST.json':len(mb),'FINAL_SEAL.json':len(sb)}
    if all(r['bytes']==sizes[r['path']] for r in rows if r['path'] in TERMINALS):break
    for r in rows:
        if r['path'] in TERMINALS:r['bytes']=sizes[r['path']]
else:raise AssertionError('Terminal byte-size fixed point failed')
(A/'FINAL_MANIFEST.json').write_bytes(mb);(A/'FINAL_SEAL.json').write_bytes(sb)
actual=snap(A)
for r in actual:
    if r['path'] in TERMINALS:r['SHA256']='EXCLUDED_TERMINAL_RECURSIVE_HASH'
assert actual==rows and counts(actual)==scope
assert before['source']==snap(S) and before['INITIAL']==snap(I) and before['continuation']==snap(C)
print(json.dumps({'UTC':now,'frozen':True,**scope,'FINAL_SHA256':seal['FINAL_SHA256'],
    'page_SHA256':build['page_SHA256'],'model_SHA256':build['model_SHA256'],
    'manifest_bytes':len(mb),'manifest_SHA256':sha(mb),'seal_bytes':len(sb),'seal_SHA256':sha(sb),
    'source_and_old_reviews_exact':True,'builder_attempts':1,'builder_exit':0,
    'completion_percent':100,'publication_authority':False}))
