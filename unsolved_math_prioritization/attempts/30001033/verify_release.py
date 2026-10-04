#!/usr/bin/env python3
"""Check the complete safe-only release allowlist; optionally reject a byte mutation."""
import argparse,hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent

def verify(manifest,data):
 expected={f['path'] for f in manifest['files']}
 assert set(data)==expected,'payload allowlist mismatch'
 for f in manifest['files']:
  name=f['path'];b=data[name]
  assert len(b)==f['bytes'],'size mismatch: '+name
  assert hashlib.sha256(b).hexdigest()==f['sha256'],'hash mismatch: '+name

def main():
 a=argparse.ArgumentParser();a.add_argument('--negative-test',action='store_true');args=a.parse_args()
 m=json.loads((ROOT/'RELEASE-MANIFEST.json').read_bytes())
 actual={str(p.relative_to(ROOT)):p.read_bytes() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='RELEASE-MANIFEST.json'}
 assert not any(pathlib.PurePosixPath(x).suffix=='.pdf' or 'private' in pathlib.PurePosixPath(x).parts for x in actual)
 verify(m,actual)
 negative=False
 if args.negative_test:
  mutant=dict(actual);p='package/PROOF.md';b=bytearray(mutant[p]);b[0]^=1;mutant[p]=bytes(b)
  try:verify(m,mutant)
  except AssertionError:negative=True
  assert negative,'one-byte mutation was not detected'
 print(json.dumps({'payload_files_verified':len(actual),'all_hashes_match':True,'safe_allowlist_verified':True,'one_byte_negative_control_rejected':negative},indent=2))
if __name__=='__main__':main()
