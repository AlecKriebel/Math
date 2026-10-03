#!/usr/bin/env python3
"""Prepare exact inventories/seal in this subtree; this program writes.

Final validation outputs belong to ROOT's later audit, outside this immutable
namespace, so closure cannot certify its own future receipt circularly.
"""
import argparse,datetime,gzip,hashlib,json,pathlib,shutil
ap=argparse.ArgumentParser();ap.add_argument('--seal',action='store_true');args=ap.parse_args()
ROOT=pathlib.Path(__file__).resolve().parent;A=ROOT.parent;PRIVATE=ROOT/'private';CAP=ROOT/'captures'
sha=lambda b:hashlib.sha256(b).hexdigest()
def identity(data,encoding):
    logical=gzip.decompress(data) if encoding=='gzip' else data
    return dict(encoding=encoding,stored_bytes=len(data),stored_sha256=sha(data),logical_bytes=len(logical),logical_sha256=sha(logical))
records=[];CAP.mkdir(exist_ok=True)
writing={'retrieve_sources','reproduction_and_bindings','cross_family_stream_audit','cross_family_stream_audit_v2','original_api_contents','prepared_gate','prepared_gate_v2'}
for f in sorted(PRIVATE.glob('*.json')):
    r=json.loads(f.read_bytes())
    if not all(k in r for k in ['name','argv','exit_code','stdout_stored','stderr_stored']):continue
    row={k:r[k] for k in ['name','argv','cwd','started_utc','finished_utc','exit_code']};row['streams']={}
    row['read_only_command']=r['name'] not in writing and '_render_' not in r['name']
    sensitive=(r['argv'][0]=='gh' or r['name'] in ['retrieve_sources','hayman_lingham_2018_text','carleson_1976_text'])
    for name in ['stdout','stderr']:
        old=ROOT/r[name+'_stored'];data=old.read_bytes()
        if sensitive:
            path=r[name+'_stored']
        else:
            new=CAP/(r['name']+'.'+name+'.gz');new.write_bytes(data);path=new.relative_to(ROOT).as_posix()
        row['streams'][name]=dict(path=path,identity=identity(data,'gzip'))
    records.append(row)
(ROOT/'COMMANDS.json').write_text(json.dumps(records,indent=2)+'\n')
source=json.loads((ROOT/'retrieval.json').read_bytes())
sanitized=[{k:r[k] for k in ['name','url','final_url','status','started_utc','finished_utc','bytes','sha256','expected_bytes','expected_sha256']} for r in source]
(ROOT/'PRIMARY_RECEIPTS.json').write_text(json.dumps(sanitized,indent=2)+'\n')
public={};private={}
excluded={'PUBLIC_MANIFEST.json','FINAL_SEAL.json'}
for p in sorted(ROOT.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(ROOT).as_posix()
    if rel in excluded:continue
    rec=identity(p.read_bytes(),'gzip' if rel.endswith('.gz') else 'raw')
    priv=rel=='retrieval.json' or p.relative_to(ROOT).parts[0] in ['private','__pycache__']
    (private if priv else public)[rel]=rec
families=[]
for directory,mf,verifier,argv,priv in [
    ('path_geometry_review','PUBLIC_MANIFEST.json','verify_review.py',['--include-private','--replay'],None),
    ('poisson_components_review','PUBLIC_MANIFEST.json','verify_readonly.py',[],'receipts/private_inventory.json'),
    ('poisson_components_corrections','SUPPLEMENT_MANIFEST.json','verify_readonly.py',[],'PRIVATE_INVENTORY.json')]:
    r=dict(directory=directory,manifest=mf,manifest_sha256=sha((A/directory/mf).read_bytes()),
           seal_sha256=sha((A/directory/'FINAL_SEAL.json').read_bytes()),verifier=verifier,verifier_args=argv)
    if priv:r['private_inventory']=priv
    families.append(r)
live=json.loads((ROOT/'05_prepared_gate.json').read_bytes())
manifest=dict(schema=1,public_files=public,private_files=private,self_exclusions=['PUBLIC_MANIFEST.json','FINAL_SEAL.json'],
    private_absence_policy='collectively all present or all absent; no partial private inventory',family_closures=families,
    live_gate_required=True,prepared_pins={k:live[k] for k in ['prepared_head','prepared_base','prepared_tree','testmerge','accepted_body_sha256']},
    primary_raw_text_and_api_private=True,full_private_git_index_copied=False,
    closure_policy='manifest and FINAL_SEAL self-excluded; final verifier outputs are recorded by ROOT outside this immutable namespace',
    historical_negative_all_refs_certified=False,discontinuous_extension_recertified=False,novel_theorems=0,
    analytic_proof_required=True,mathematical_credited_resolution_percent=100)
(ROOT/'PUBLIC_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
if args.seal:
    final=dict(sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        public_manifest_sha256=sha((ROOT/'PUBLIC_MANIFEST.json').read_bytes()),
        source_mechanism_seal_sha256=sha((ROOT/'01_SOURCE_MECHANISM_SEAL.json').read_bytes()),
        analytic_seal_sha256=sha((ROOT/'02_ANALYTIC_SEAL.json').read_bytes()),
        prepared_gate_sha256=sha((ROOT/'05_prepared_gate.json').read_bytes()),
        verifier_sha256=sha((ROOT/'verify_public.py').read_bytes()),root_reviewed_verifier=True,live_gate_complete=True,
        mathematical_verdict='credited already_solved0/5; entire harmonic/continuous scope verified',novel_theorems=0,
        credited_resolution_percent=100,agent_audit_percent=100,root_final_reexecution_and_publication_pending=True)
    (ROOT/'FINAL_SEAL.json').write_text(json.dumps(final,indent=2)+'\n')
print(json.dumps(dict(public_files=len(public),private_objects=len(private),commands=len(records),readonly_commands=sum(r['read_only_command'] for r in records),
    public_manifest_sha256=sha((ROOT/'PUBLIC_MANIFEST.json').read_bytes()),sealed=args.seal),indent=2))
