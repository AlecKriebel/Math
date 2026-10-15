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
    x=pin(p)
    require(x['sha256']==r['sha256'],str(p)+' digest')
    size=r.get('bytes',r.get('size',r.get('size_bytes')))
    if size is not None: require(x['bytes']==size,str(p)+' size')
    mode=r.get('mode',r.get('mode_octal'))
    if mode is not None: require(int(x['mode'],8)==int(mode,8),str(p)+' mode')
    return x
families=[
 ('cylinder_geometry_adversary','FINAL_MANIFEST.json','bae213937e7fcf3c165588c25c9871e7c491d05f447f4bb09b8cb4c4c1041f47'),
 ('literal_source_scope_adversary','MANIFEST.json','832ae33e9e27c90f33b3bc69b5d75f0d4d38359bb8a0e05f30594faf592056d2'),
 ('probabilistic_asymptotics_adversary','FILE_MANIFEST.json','a8eadd6e9da11c55e1bc9dd1f8217c922a07cd567a3e63d3fdc83f6ee5e96ac3')]
out=dict(UTC=datetime.now(timezone.utc).isoformat(),status='ALL_THREE_MATH_FAMILY_EXACT_MANIFESTS_AUTHENTICATED',families=[],publication_clearance=False)
for fam,name,digest in families:
    f=A/fam;p=f/name;j=json.loads(p.read_text())
    require(pin(p)['sha256']==digest,fam+' externally delivered manifest digest')
    rows=j.get('entries',j.get('retained_files'))
    rels=[r.get('relative_path',r.get('path')) for r in rows]
    require(len(set(rels))==len(rels),fam+' duplicate inventory')
    require(all(not Path(rel).is_absolute() and '..' not in Path(rel).parts for rel in rels),fam+' unsafe inventory path')
    artifacts=[check(f/rel,r) for rel,r in zip(rels,rows)]
    actual=set()
    for leaf in f.rglob('*'):
        require(not leaf.is_symlink(),fam+' unexpected symlink')
        if leaf.is_file(): actual.add(leaf.relative_to(f).as_posix())
    require(actual==set(rels)|{name},fam+' incomplete inventory')
    if fam=='cylinder_geometry_adversary':
        inputs=json.loads((f/'INPUT_RECEIPTS.json').read_text())['receipts']
        inputs=[check(Path(r['original_path']),r) for r in inputs]
        wl=json.loads((f/'PUBLIC_OUTPUT_WHITELIST.json').read_text())
        public=wl['paths']
        require(set(public)-{name}=={r['path'] for r in rows if r['publication_eligible_own_output']},fam+' public classification disagreement')
    elif fam=='literal_source_scope_adversary':
        inputs=[check(Path(r['path']),r) for r in j['actual_original_inputs']]
        inputs.append(check(Path(j['instruction_file_read']['path']),j['instruction_file_read']))
        public=j['public_own_output_whitelist']
        require(set(public)-{name}=={r['relative_path'] for r in rows if r['public_own_output']},fam+' public classification disagreement')
    else:
        inputs=[check(Path(r['path']),r) for r in j['external_actual_input_identities']]
        public=j['public_own_output_allowlist']
        require(set(public)-{name}=={r['relative_path'] for r in rows if r['public_output_allowed']},fam+' public classification disagreement')
    require(all(not rel.startswith(('private/','scratch/')) for rel in public),fam+' private output allowed')
    require(set(public)<=actual,fam+' missing public file')
    seals=[]
    for ns in ['FIRST_ASSESSMENT.md','FIRST_ASSESSMENT_SEAL.json']:
        x=pin(f/ns);require(x['mode']=='0444',fam+' first seal is not frozen');seals.append(x)
    out['families'].append(dict(family=fam,manifest_identity=pin(p),all_preserved_artifact_identities=artifacts,external_input_identities=inputs,complete_inventory_verified=True,first_seals=seals,first_seals_frozen=True,public_allowlist=public,private_source_bodies_excluded=True))
target=A/'root_math/MATH_FAMILY_MANIFEST_AUTHENTICATION.json'
target.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(receipt=pin(target),families=3,artifacts=sum(len(x['all_preserved_artifact_identities']) for x in out['families']),inputs=sum(len(x['external_input_identities']) for x in out['families']),status=out['status']),indent=2))
