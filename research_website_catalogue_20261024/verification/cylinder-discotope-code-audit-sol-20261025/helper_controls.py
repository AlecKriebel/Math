"""Distinct missing-input and semantic-object attacks on the actual helper."""
from pathlib import Path
from copy import deepcopy
import hashlib,json,sys
A=Path(__file__).resolve().parent;R=A.parents[1];S=R/'verification/local-cylinder-discotope-stage-sol-20261025'
sys.path[:0]=[str(S),str(R/'scripts')]
from cylinder_discotope_source import cylinder_discotope_source_view
rb,rt,symlink=Path.read_bytes,Path.read_text,Path.is_symlink
checks=[]
def reject(rid,case,call):
    try:call()
    except (ValueError,FileNotFoundError) as e:checks.append({'record_id':rid,'case':case,'rejected':True,'type':type(e).__name__,'reason':str(e)})
    else:raise RuntimeError('false_accept:'+rid+':'+case)
for rid in ['23387774','23074543']:
    p=R/'papers'/rid;c=json.loads(rb(p/'publication.json'));g=json.loads(rb(p/'promotion.json'));original=deepcopy([c,g])
    raw,view,assets=cylinder_discotope_source_view(p,c,g)
    if len(view['files'])!=2 or raw!=c['source_binding']['source_receipt_original']:raise RuntimeError('pristine_identity')
    checks.append({'record_id':rid,'case':'pristine','accepted':True})
    for case,mutate in [
      ('omit_original_scope_verdict',lambda x:x['reviews']['scope'].pop('verdict')),
      ('promote_browser_gate',lambda x:x.update(browser_verified=True)),
      ('replace_root_authority_by_status_only',lambda x:x.update(root_clearance_record={'status':'PASS'})),
    ]:
        bad=deepcopy(g);mutate(bad);reject(rid,case,lambda:cylinder_discotope_source_view(p,c,bad))
    missing=[c['source_binding']['source_tex_path'],'sources/'+c['pdf_filename'],g['reviews']['analytic']['report'],g['reviews']['adversarial']['verdict_file']]
    for rel in missing:
        path=(p/rel).resolve()
        def read(q):
            if q.resolve()==path:raise FileNotFoundError('independent missing-read control: '+str(path))
            return rb(q)
        Path.read_bytes=read;Path.read_text=lambda q,*a,**k:read(q).decode(k.get('encoding') or 'utf-8')
        try:reject(rid,'missing_actual_read:'+rel,lambda:cylinder_discotope_source_view(p,c,g))
        finally:Path.read_bytes=rb;Path.read_text=rt
    path=(p/'sources'/c['pdf_filename']).resolve()
    Path.is_symlink=lambda q:True if q==path else symlink(q)
    try:reject(rid,'selected_reader_symlink',lambda:cylinder_discotope_source_view(p,c,g))
    finally:Path.is_symlink=symlink
    path=(p/'sources/zenodo-record.raw.json').resolve();api=json.loads(rb(path));api['files'][0]['links']['self']='https://example.invalid/substitution'
    data=json.dumps(api).encode();Path.read_bytes=lambda q:data if q.resolve()==path else rb(q)
    try:reject(rid,'altered_actual_API_URL',lambda:cylinder_discotope_source_view(p,c,g))
    finally:Path.read_bytes=rb
    if [c,g]!=original:raise RuntimeError('original_arguments_mutated')
result={'status':'ALL_DISTINCT_HELPER_CONTROLS_REJECT_AS_EXPECTED','optimization':sys.flags.optimize,'checks':checks,'in_memory_only':True,'source_or_fixture_writes':0}
print(json.dumps(result,indent=2))
