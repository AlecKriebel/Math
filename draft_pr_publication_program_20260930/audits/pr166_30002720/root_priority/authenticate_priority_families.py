from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat
A=Path(__file__).resolve().parents[1]
def require(x,msg):
    if not x: raise RuntimeError(msg)
def pin(p):
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=format(stat.S_IMODE(p.stat().st_mode),'04o'))
def check(p,r):
    x=pin(p); require(x['sha256']==r['sha256'],str(p)+' digest')
    size=r.get('bytes',r.get('size',r.get('size_bytes')))
    if size is not None: require(x['bytes']==size,str(p)+' size')
    mode=r.get('mode',r.get('mode_octal'))
    if mode is not None: require(int(x['mode'],8)==int(mode,8),str(p)+' mode')
    return x
families=[('priority_current_literature','MANIFEST.json','cb9d49007440f46c0588dd8e0a5a9fa162ef3402f75147f1e2e769c150e85687'),('priority_irregular_quantiles','RETAINED_FILE_INVENTORY.json','3fc67cad454178c694dfa7a34588eecd8ca480cab33582b4b6b1fc82d7ee8245'),('priority_source_history','RETAINED_FILE_MANIFEST.json','f67c25b3fe165e2257cf69f7edb616f089748f3959e7eb18076cbd66ef1dc2db')]
out=dict(UTC=datetime.now(timezone.utc).isoformat(),status='COMPLETED_PRIORITY_FAMILY_MANIFEST_AUTHENTICATED',families=[],publication_clearance=False)
for fam,name,digest in families:
    f=A/fam; p=f/name; j=json.loads(p.read_text())
    require(pin(p)['sha256']==digest,fam+' externally delivered manifest digest')
    rows=j.get('files',j.get('entries')); rels=[r['path'] for r in rows]
    require(len(set(rels))==len(rels),fam+' duplicate inventory')
    require(all(not Path(rel).is_absolute() and '..' not in Path(rel).parts for rel in rels),fam+' unsafe inventory path')
    artifacts=[check(f/rel,r) for rel,r in zip(rels,rows)]
    actual=set()
    for leaf in f.rglob('*'):
        require(not leaf.is_symlink(),fam+' unexpected symlink')
        if leaf.is_file(): actual.add(leaf.relative_to(f).as_posix())
    require(actual==set(rels)|{name},fam+' incomplete inventory')
    require(j.get('file_count',j.get('regular_file_count'))==len(rows),fam+' inventory count')
    total=j.get('total_size',j.get('total_bytes'))
    if total is not None: require(total==sum(x['bytes'] for x in artifacts),fam+' inventory total bytes')
    if fam=='priority_source_history':
        first=json.loads((f/'FIRST_ASSESSMENT_SEAL.json').read_text())
        sealed_inputs=[check(Path(r['path']),r) for r in first['sealed_files']]
        require(pin(f/'FIRST_ASSESSMENT_SEAL.json')['mode']=='0444',fam+' first seal unfrozen')
        neutral=json.loads((f/'INPUT_IDENTITIES.json').read_text())
        inputs=[check(Path(r['path']),r) for r in neutral['candidate_inputs']]
        first_inputs=json.loads((f/'FIRST_INPUT_IDENTITIES.json').read_text())
        instruction_inputs=[check(Path(r['path']),r) for r in first_inputs['local_instructions']]
        first_retained=[]
        for r in first_inputs['retained_primary_bodies_and_derivatives']:
            rec=dict(r);prior_mode=rec.pop('mode',None)
            x=check(Path(rec['path']),rec);x['mode_at_first_seal']=prior_mode;first_retained.append(x)
        ledger=json.loads((f/'SOURCE_REGISTER.json').read_text())
        acquired=[check(f/r['local_path'],r) for r in ledger['sources'] if r['body_retained']]
        final=json.loads((f/'FINAL_SEAL.json').read_text())
        final_pins=[check(f/r['path'],r) for r in final['public_own_output_identities']]
        check(f/final['first_private_input_record']['path'],final['first_private_input_record'])
        erratum=json.loads((f/'FIRST_ASSESSMENT_ERRATUM_SEAL.json').read_text());check(f/erratum['file'],erratum)
        wl=json.loads((f/'PUBLIC_OUTPUT_WHITELIST.json').read_text());public=wl['allowed_public_own_outputs']
        require(len(set(public))==len(public) and set(public)<=actual,fam+' public allowlist')
        require(all(not rel.startswith(('private_primary/','scratch/')) and rel not in wl['excluded_patterns'] for rel in public),fam+' private output allowed')
        require(all(x['mode']=='0444' for x in artifacts),fam+' final files unfrozen')
        out['families'].append(dict(family=fam,manifest_identity=pin(p),all_preserved_artifact_identities=artifacts,external_original_input_identities=inputs,acquired_retained_inputs=acquired,instruction_inputs=instruction_inputs,first_sealed_identities=sealed_inputs,first_retained_inputs=first_retained,first_seal=pin(f/'FIRST_ASSESSMENT_SEAL.json'),final_seal=pin(f/'FINAL_SEAL.json'),final_output_identities=final_pins,complete_inventory_verified=True,public_allowlist=public,private_source_bodies_excluded=True))
        continue
    if fam=='priority_irregular_quantiles':
        seal=json.loads((f/'FIRST_PRIORITY_SEAL.json').read_text())
        assessment=check(f/seal['path'],seal)
        require(pin(f/'FIRST_PRIORITY_SEAL.json')['mode']=='0444',fam+' first seal unfrozen')
        ledger=json.loads((f/'EXTERNAL_INPUTS.json').read_text())
        inputs=[check(Path(r['path']),r) for r in ledger['allowed_submission_inputs']]
        acquired=[]
        for r in ledger['primary_downloads']:
            rec=dict(r['actual_retained_file']); prior_mode=rec.pop('mode',None)
            x=check(Path(rec['path']),rec); x['mode_at_acquisition']=prior_mode
            acquired.append(x)
        instruction_inputs=[check(Path(ledger['workflow_skill']['path']),ledger['workflow_skill'])]
        wl=json.loads((f/'PUBLIC_OUTPUT_ALLOWLIST.json').read_text()); public=wl['allowlist']
        require(len(set(public))==len(public) and set(public)<=actual,fam+' public allowlist')
        require(all(not rel.startswith(('private/','scratch/')) for rel in public),fam+' private output allowed')
        require(all(x['mode']=='0444' for x in artifacts),fam+' final files unfrozen')
        out['families'].append(dict(family=fam,manifest_identity=pin(p),all_preserved_artifact_identities=artifacts,external_original_input_identities=inputs,acquired_retained_inputs=acquired,instruction_inputs=instruction_inputs,first_assessment=assessment,first_seal=pin(f/'FIRST_PRIORITY_SEAL.json'),complete_inventory_verified=True,public_allowlist=public,private_source_bodies_excluded=True))
        continue
    seal=json.loads((f/'FIRST_ASSESSMENT_SEAL.json').read_text())
    assessment=check(f/seal['assessment']['path'],seal['assessment'])
    require(assessment['mode']=='0444',fam+' assessment unfrozen')
    inputs=[]
    for r in seal['inputs']:
        inputs.append(check(Path(r['source_path']),r))
        if r.get('retained_path'): check(f/r['retained_path'],r)
    ledger=json.loads((f/'EXTERNAL_INPUTS.json').read_text())
    retrieved=[check(f/r['retention_path'],r) for r in ledger['retrievals'] if r.get('retention_path')]
    instruction_inputs=[check(Path(r['path']),r) for r in ledger['applicable_instruction_identities']]
    final=json.loads((f/'FINAL_ASSESSMENT_SEAL.json').read_text())
    require(final['independent_first_seal_sha256']==pin(f/'FIRST_ASSESSMENT_SEAL.json')['sha256'],fam+' first seal continuity')
    final_pins=[check(f/r['path'],r) for r in final['public_output_hashes']]
    require(all(x['mode']=='0444' for x in final_pins),fam+' final science unfrozen')
    wl=json.loads((f/'PUBLIC_OUTPUT_WHITELIST.json').read_text())
    public=wl['public_own_output_paths']
    require(wl['deny_by_default'] and len(set(public))==len(public) and set(public)<=actual,fam+' public allowlist')
    require(all(not rel.startswith(('private/','scratch/')) for rel in public),fam+' private output allowed')
    out['families'].append(dict(family=fam,manifest_identity=pin(p),all_preserved_artifact_identities=artifacts,external_original_input_identities=inputs,acquired_retained_inputs=retrieved,instruction_inputs=instruction_inputs,first_assessment=assessment,first_seal=pin(f/'FIRST_ASSESSMENT_SEAL.json'),final_seal=pin(f/'FINAL_ASSESSMENT_SEAL.json'),final_output_identities=final_pins,complete_inventory_verified=True,public_allowlist=public,private_source_bodies_excluded=True))
target=A/'root_priority/PRIORITY_FAMILY_MANIFEST_AUTHENTICATION.json'
target.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(receipt=pin(target),families=len(out['families']),artifacts=sum(len(x['all_preserved_artifact_identities']) for x in out['families']),status=out['status']),indent=2))
