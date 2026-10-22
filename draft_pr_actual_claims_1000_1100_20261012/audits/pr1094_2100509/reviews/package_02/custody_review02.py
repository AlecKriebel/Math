"""Independent before/current resolution and immutable-history check."""
from pathlib import Path
import hashlib,json,subprocess,sys,datetime
OUT=Path(__file__).absolute().parent;B=OUT.parent.parent;P=B/'preprint_v1_0';R=B/'repairs/package01'
def need(x,m):
    if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def pin(p):
    d=p.read_bytes();return {'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}
def equal(p,row):return p.is_file() and pin(p)=={k:row[k] for k in ['bytes','sha256']}
def save(n,x):(OUT/n).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def records(x):
    for key in ['records','entries','files']:
        if key in x:return x[key]
    raise ValueError('unknown inventory schema')
def run():
    baseline=records(load(R/'FROZEN_INPUT_PINS.json'))
    changed={r['path']:r for r in records(load(R/'ALLOWED_CHANGES.json'))}
    resolution={};rows=[]
    for r in baseline:
        live=B/r['path'];before=R/'before'/r['path']
        if r['path'] in changed:
            need(r==changed[r['path']],'allowed change must identify old exact bytes')
            need(equal(before,r),'before bytes not exact')
            need(not equal(live,r),'claimed change is not changed')
            resolution[r['path']]=before
            rows.append({'path':r['path'],'resolution':str(before.relative_to(B)),**pin(before),'successor':pin(live)})
        else:
            need(equal(live,r),'protected baseline changed '+r['path'])
            resolution[r['path']]=live
            rows.append({'path':r['path'],'resolution':r['path'],**pin(live)})
    need(len(baseline)==309 and len(changed)==8,'baseline accounting')
    c=load(P/'kit/CUSTODY_MAP.json');names=[r['original_path'] for r in c['copies']]+[r['path'] for r in c['exclusions']]
    need(len(names)==len(set(names))==c['exact_partition_count']==309,'custody exact partition')
    need(set(names)==set(resolution),'custody missing/extra baseline path')
    copy_rows=[];exclusions=[]
    for r in c['copies']:
        a=resolution[r['original_path']];p=P/'kit'/r['copy_path']
        need(equal(p,r) and equal(a,r),'selected copy changed')
        copy_rows.append({**r,'resolved_original':str(a.relative_to(B)),'verified':True})
    for r in c['exclusions']:
        a=resolution[r['path']];need(equal(a,r),'excluded path changed')
        need(bool(r['reason']),'unreasoned exclusion')
        exclusions.append({**r,'resolved_original':str(a.relative_to(B)),'verified':True})
    # Recompute all four dated stages from their actual inventories, independently
    # of the earlier repair's resolution report; then compare exact rows.
    spec=[('preprint_v1_0/FROZEN_INPUT_PINS.json',B,171),('preprint_v1_0/OUTPUT_PINS.json',P,101),
          ('reviews/package_01/INPUT_PINS.json',B,281),('reviews/package_01/OUTPUT_PINS.json',B/'reviews/package_01',24)]
    stage_rows=[];previous=load(R/'PRIOR_STAGE_RESOLUTION.json')['stages']
    for name,base,count in spec:
        raw=load(B/name); rr=records(raw);need(len(rr)==count,'stage row count')
        prev=next(s for s in previous if s['inventory']==name)
        need(prev['inventory_sha256']==pin(B/name)['sha256'],'old inventory digest')
        got=[]
        for r in rr:
            auditpath=(base/r['path']).relative_to(B).as_posix()
            selected=resolution.get(auditpath,B/auditpath)
            need(equal(selected,r),'historical row unresolved '+auditpath)
            pr=next(x for x in prev['records'] if x['path']==r['path'])
            need(B/pr['resolution']==selected,'independent resolution disagrees')
            got.append({'path':r['path'],'audit_path':auditpath,'resolution':str(selected.relative_to(B)),
                        **{k:r[k] for k in ['bytes','sha256']}})
        stage_rows.append({'inventory':name,'count':len(got),'inventory_pin':pin(B/name),'rows':got})
    # All current preparation/kit artifacts in the repair's final inventory.
    current=records(load(R/'CURRENT_ARTIFACT_PINS.json'))
    for r in current:need(equal(B/r['path'],r),'current artifact pin mismatch '+r['path'])
    # Authenticate every primary output inventory with its separately retained seal.
    seals=[]
    for folder,sname in [(P,'PREPARATION_SEAL.json'),(B/'reviews/package_01','SEALED.json'),(R,'SEAL.json')]:
        seal=load(folder/sname);inv=folder/'OUTPUT_PINS.json'
        need(seal['output_pins_sha256']==pin(inv)['sha256'],'separate seal inventory hash')
        rr=records(load(inv));need(seal['output_count']==len(rr),'separate seal output count')
        for r in rr:
            auditpath=(folder/r['path']).relative_to(B).as_posix()
            selected=resolution.get(auditpath,B/auditpath)
            need(equal(selected,r),'sealed dated output unresolved')
        seals.append({'seal':str((folder/sname).relative_to(B)),**pin(folder/sname),'inventory':str(inv.relative_to(B)),
                      'inventory_pin':pin(inv),'output_count':len(rr),'all_rows_verified':True,'semantics':'dated stage, not current readiness'})
    # Family freezes and seals have all remained untouched. Validate their own
    # nested path/hash references by their recorded stage roots, with fallback
    # only to physically identical captured bytes, explicitly enumerated.
    extra=[]
    for name in ['collar_algebra_01','geometry_rigidity_01','priority_01']:
        folder=B/'reviews'/name
        for f in sorted(folder.glob('*.json')):
            if not any(k in f.name for k in ['CUSTODY','PINS','SEALED','PRESERVATION']):continue
            x=load(f);nested=[]
            def walk(v,prefix='$'):
                if isinstance(v,dict):
                    if set(['path','bytes','sha256'])<=set(v):
                        candidates=[B/v['path'],folder/v['path'],folder/'frozen'/v['path']]
                        matches=[str(p.relative_to(B)) for p in candidates if p.is_relative_to(B) and equal(p,v)]
                        nested.append({'json_location':prefix,**{k:v[k] for k in ['path','bytes','sha256']},'verified_path_matches':list(dict.fromkeys(matches))})
                    for k,w in v.items():walk(w,prefix+'.'+k)
                elif isinstance(v,list):
                    for i,w in enumerate(v):walk(w,prefix+'['+str(i)+']')
            walk(x)
            # Some records deliberately describe immutable Git/source captures
            # at formerly external paths. Their containing freeze is authenticated
            # by the current baseline; do not invent live resolution for them.
            extra.append({'artifact':str(f.relative_to(B)),**pin(f),'history_rows':nested,'artifact_preserved_in_309_baseline':str(f.relative_to(B)) in resolution,
                          'semantics':'captured historical input; unmatched old source paths are not asserted live'})
    manifest=load(P/'kit/MANIFEST.json');allnames={str(p.relative_to(P/'kit')) for p in (P/'kit').rglob('*') if p.is_file()}
    need({r['path'] for r in manifest['records']}==allnames-{'MANIFEST.json'},'current manifest exact inventory')
    for r in manifest['records']:need(equal(P/'kit'/r['path'],r),'current manifest mismatch')
    public=load(B/'SUBMITTED_PINS.json');need(len(public['files'])==8,'actual submitted count is eight')
    gitrows=[]
    for r in public['files']:
        need(equal(B/r['snapshot_path'],r),'submitted snapshot mismatch')
        x=subprocess.run(['git','show',public['head_oid']+':'+r['repository_path']],cwd='/Users/alec/Documents/Math',capture_output=True)
        need(x.returncode==0,'Git object not available')
        need(len(x.stdout)==r['bytes'] and hashlib.sha256(x.stdout).hexdigest()==r['sha256'],'Git original differs')
        gitrows.append({**r,'git_blob_rehashed':True})
    branch=subprocess.check_output(['git','branch','--show-current'],cwd='/Users/alec/Documents/Math',text=True).strip();need(branch=='main','shared branch must remain main')
    # Dependency pins are supplemental reading/execution custody, never falsely
    # described as having been frozen before first inspection.
    dependencies=[]
    for f in ['/Users/alec/.codex/plugins/cache/openai-primary-runtime/pdf/26.1013.11914/skills/pdf/SKILL.md',
              '/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','/opt/homebrew/bin/tectonic',sys.executable,
              '/opt/homebrew/bin/pdftoppm','/opt/homebrew/bin/pdftotext','/opt/homebrew/bin/pdfinfo']:
        dependencies.append({'path':str(f),'resolved_path':str(Path(f).resolve()),**pin(Path(f))})
    save('CUSTODY_REVIEW.json',{'status':'PASS','baseline':rows,'changed_count':8,'protected_count':301,
         'selected_copies':copy_rows,'exclusions':exclusions,'copies_count':len(copy_rows),'exclusions_count':len(exclusions),
         'four_historical_stages':stage_rows,'historical_stage_rows':sum(x['count'] for x in stage_rows),
         'separate_seals':seals,'other_captured_family_freezes':extra,'current_artifact_rows':current,
         'current_artifact_count':len(current),'current_manifest_records':len(manifest['records']),
         'current_manifest_pin':pin(P/'kit/MANIFEST.json'),'submitted_actual_count':8,'submitted_git_recheck':gitrows,
         'branch':branch,'git_read_only_commands':9,'mutations':False})
    save('SUPPLEMENTAL_DEPENDENCY_PINS.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'supplemental late pins of external skills/runtime/checker dependencies; no byte copies','records':dependencies})
if __name__=='__main__':run()
