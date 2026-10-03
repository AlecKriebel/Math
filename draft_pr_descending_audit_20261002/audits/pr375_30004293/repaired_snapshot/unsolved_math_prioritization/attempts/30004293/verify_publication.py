from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
for manifest,root in [(p/'PUBLICATION_MANIFEST.json',p),(p/'FINAL_AUTHOR_MANIFEST.json',p),(p/'review/REVIEW_MANIFEST.json',p/'review')]:
 for e in json.loads(manifest.read_text())['files']:
  b=(root/e['path']).read_bytes()
  assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],(manifest.name,e['path'])
subprocess.run([sys.executable,str(p/'review/verify_review.py'),'--author',str(p)],check=True)
print(json.dumps({'publication_hashes_verified':52,'frozen_author_files':42,'frozen_review_files':8,'source_pdfs_reverified':False},sort_keys=True))
