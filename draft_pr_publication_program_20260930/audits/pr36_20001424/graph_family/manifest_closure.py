#!/usr/bin/env python3
"""Strict self-excluding authored audit closure; --verify checks exact inventory/bytes.
Private foreign downloads, derivative source text, caches, tmp are excluded explicitly.
"""
from pathlib import Path
import json,hashlib,datetime,sys
ROOT=Path(__file__).resolve().parent
MANIFEST=ROOT/'authored_manifest.json'
EXCLUDED_DIRS={'private_sources','private_tmp','__pycache__'}
def excluded(p):
 rel=p.relative_to(ROOT)
 return p==MANIFEST or any(x in EXCLUDED_DIRS for x in rel.parts) or p.suffix=='.pyc' or p.name.endswith('.tmp')
def inventory():
 rows=[]
 for p in sorted(ROOT.rglob('*')):
  if not p.is_file() or excluded(p):continue
  b=p.read_bytes();rows.append({'path':p.relative_to(ROOT).as_posix(),'size':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 return rows
def main():
 files=inventory()
 if '--verify' in sys.argv:
  m=json.loads(MANIFEST.read_text())
  assert m['files']==files,'Strict authored inventory or a file hash changed'
  assert len(files)==m['file_count']
  assert all(row['path']!='authored_manifest.json' for row in files)
  assert not any(any(part in EXCLUDED_DIRS for part in Path(row['path']).parts) for row in files)
  print(json.dumps({'strict_manifest_verifies':True,'files':len(files),'self_excluded':True,'foreign_sources_and_tmp_excluded':True},indent=2));return
 m={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Authored graph-family verification closure, including actual private original-code replays and controlled mutant packets. No new candidate science. Original16 audit; original research attempts added0.','self_excluding':True,'excluded':['authored_manifest.json','private_sources/** (foreign downloaded PDFs/HTML/text, including source mutant)','private_tmp/**','__pycache__/**','*.pyc','*.tmp'],'file_count':len(files),'files':files}
 MANIFEST.write_text(json.dumps(m,indent=2)+'\n')
 print(json.dumps({'manifest_created':True,'files':len(files),'self_excluded':True},indent=2))
if __name__=='__main__':main()
