from pathlib import Path
import hashlib,json,datetime,stat,argparse
ROOT=Path(__file__).resolve().parent
FIRST_HASH='423b8197bec75210edf712ab6c06ea8bad117ade78c3b3a1a3dbb82f522f9ae4'
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def validate_first():
 p=ROOT/'FIRST_MANIFEST.json'
 if digest(p)!=FIRST_HASH: raise ValueError('Immutable first manifest hash changed')
 if stat.S_IMODE(p.stat().st_mode)!=0o444: raise ValueError('First manifest mode changed')
 data=json.loads(p.read_text())
 for row in data['files']:
  q=ROOT/row['path']
  if q.is_symlink() or not q.is_file(): raise ValueError(f'First-seal file missing/unsafe: {q}')
  if digest(q)!=row['sha256'] or q.stat().st_size!=row['bytes'] or format(stat.S_IMODE(q.stat().st_mode),'04o')!=row['mode']:
   raise ValueError(f'Immutable first-seal file changed: {q}')
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--validate-only',action='store_true');args=parser.parse_args()
 validate_first()
 if args.validate_only:
  p=ROOT/'FINAL_INVENTORY.json'; data=json.loads(p.read_text())
  known={r['path'] for r in data['files']}
  actual={str(q.relative_to(ROOT)) for q in ROOT.rglob('*') if q.is_file()}-{'FINAL_INVENTORY.json'}
  if known!=actual: raise ValueError('Final inventory file set mismatch')
  for row in data['files']:
   q=ROOT/row['path']
   if q.is_symlink() or digest(q)!=row['sha256'] or q.stat().st_size!=row['bytes'] or format(stat.S_IMODE(q.stat().st_mode),'04o')!=row['mode']:
    raise ValueError(f'Final inventory mismatch: {q}')
  if stat.S_IMODE(p.stat().st_mode)!=0o444: raise ValueError('Final inventory not sealed 0444')
  print(json.dumps({'status':'PASS','first_seal_unchanged':True,'retained_files_including_inventory':len(data['files'])+1,'final_inventory_sha256':digest(p),'final_inventory_bytes':p.stat().st_size,'final_inventory_mode':'0444'}))
  return
 rows=[]
 for p in sorted(ROOT.rglob('*')):
  if not p.is_file(): continue
  if p.is_symlink(): raise ValueError(f'Symlink is forbidden in retained artifacts: {p}')
  rel=str(p.relative_to(ROOT))
  if rel=='FINAL_INVENTORY.json': raise ValueError('Refuse to replace an existing final inventory')
  p.chmod(0o444)
  private=rel.startswith('private/')
  rows.append({'path':rel,'sha256':digest(p),'bytes':p.stat().st_size,'mode':format(stat.S_IMODE(p.stat().st_mode),'04o'),'public_allowlist':not private,'public_availability':{'audit_artifact':'private retained source body/extract/render/raw header, do not redistribute' if private else 'eligible original derivation/report/diagnostic/safe acquisition or identity ledger','external_primary_source':('https://par.nsf.gov/servlets/purl/10582270' if 'published' in rel else 'https://arxiv.org/pdf/2205.01587v3' if 'arxiv_v3' in rel else 'https://arxiv.org/pdf/2205.01587v1') if private else None}})
 data={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'first_manifest_sha256_unchanged':FIRST_HASH,'files':rows,'self_pin':'This inventory is the only self-excluded control file; its SHA256/size/mode are pinned in the tool validation receipt and final parent delivery. No finite file can include its own cryptographic hash without a self-reference convention.','public_allowlist_policy':'Only entries with public_allowlist=true are eligible; full primary bodies, text extracts, source page renders and raw headers remain private. Eligibility is not a publication authorization.'}
 p=ROOT/'FINAL_INVENTORY.json';p.write_text(json.dumps(data,indent=2)+'\n');p.chmod(0o444)
 print(json.dumps({'created':str(p),'sha256':digest(p),'bytes':p.stat().st_size,'mode':'0444','retained_files_including_inventory':len(rows)+1}))
if __name__=='__main__': main()
