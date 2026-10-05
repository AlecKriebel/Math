#!/usr/bin/env python3
"""Writing inventory/closure driver. It never executes verification programs."""
import argparse,datetime,gzip,hashlib,json,pathlib,shutil
R=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def identity(p):
    b=p.read_bytes();r=dict(bytes=len(b),sha256=sha(b))
    if p.suffix=='.gz':
        d=gzip.decompress(b);r.update(logical_bytes=len(d),logical_sha256=sha(d))
    return r
parser=argparse.ArgumentParser();parser.add_argument('--seal',action='store_true');args=parser.parse_args()
assert not (R/'FINAL_SEAL.json').exists(),'closed namespace'
writing={'integration_driver','integration_driver_v2','repair_audit_driver','create_v2_driver','prepare_packet_driver','preserve_preseal_driver'}
commands=[]
for p in sorted((R/'private').glob('*.json')):
    c=json.loads(p.read_bytes());c['readonly']=c['name'] not in writing
    for s,row in c['streams'].items():
        # Entire raw API responses remain private. All other postmerge captures
        # contain Git/source-program bytes, recipes, or sanitized factual reports.
        if c['argv'][0]!='gh':
            dest=R/'captures'/(c['name']+'.'+s+'.gz');dest.parent.mkdir(exist_ok=True)
            shutil.copyfile(R/row['path'],dest);row['original_private_path']=row['path'];row['path']=dest.relative_to(R).as_posix()
    commands.append(c)
(R/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
public={};private={}
for p in sorted(R.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(R).as_posix()
    if rel in {'PUBLIC_MANIFEST.json','FINAL_SEAL.json'}:continue
    (private if rel.startswith('private/') else public)[rel]=identity(p)
manifest=dict(schema='postmerge exact namespace v1',files=public,private_files=private,self_exclusions=['PUBLIC_MANIFEST.json','FINAL_SEAL.json'],command_count=len(commands),readonly_commands=sum(c['readonly'] for c in commands))
payload=(json.dumps(manifest,indent=2)+'\n').encode();(R/'PUBLIC_MANIFEST.json').write_bytes(payload)
if args.seal:
    seal=dict(sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),manifest='PUBLIC_MANIFEST.json',manifest_sha256=sha(payload),verifier_sha256=sha((R/'verify_public.py').read_bytes()),public_files=len(public),private_files=len(private),self_exclusions=manifest['self_exclusions'])
    (R/'FINAL_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
print(json.dumps(dict(manifest_sha256=sha(payload),public_files=len(public),private_files=len(private),commands=len(commands),readonly_commands=manifest['readonly_commands'],sealed=args.seal)))
