#!/usr/bin/env python3
"""Verify included public bytes and text bindings, not missing sources or mathematics."""
import argparse,hashlib,json,pathlib
p=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
m=json.loads((p/'PUBLIC_MANIFEST.json').read_text())
for name,e in m['files'].items():
 b=(p/name).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],name
prov=json.loads((p/'PROVENANCE.json').read_text());cert=(p/'SOURCE_RESOLUTION_CERTIFICATE.md').read_bytes();review=(p/'INDEPENDENT_APPLICABILITY_REVIEW.md').read_text()
ranges={'certificate_prefix_before_administrative_section6':cert,'review_verdict':review[review.index('## Verdict'):review.index('## Public review binding')].encode(),'review_substantive_audit':review[review.index('## Substantive claim audit'):review.index('## Final disposition')].encode(),'review_final_disposition':review[review.index('## Final disposition'):].encode()}
for key,b in ranges.items():
 e=prov['unchanged_ranges'][key];assert len(b)==e['bytes'] and sha(b)==e['sha256'],key
ap=argparse.ArgumentParser();ap.add_argument('--base-queue');ap.add_argument('--queue');args=ap.parse_args();assert bool(args.base_queue)==bool(args.queue),'provide both queue paths'
patch=json.loads((p/'QUEUE_PATCH.json').read_text());assert patch['after']==patch['before'].replace('| queued | 0/5 |','| already_solved | 0/5 |')
if args.queue:
 before=pathlib.Path(args.base_queue).read_bytes();after=pathlib.Path(args.queue).read_bytes();assert sha(before)==patch['base_queue_sha256'];assert sha(after)==patch['proposed_queue_sha256'];old=(patch['before']+'\n').encode();new=(patch['after']+'\n').encode();assert before.count(old)==1 and after==before.replace(old,new,1)
print(json.dumps({'public_integrity':'PASS','included_files':len(m['files']),'unchanged_mathematical_text':'PASS','full_queue_patch':'PASS' if args.queue else 'NOT_RUN_NO_QUEUE_INPUTS','primary_source_bytes_reverified':False,'corpus_bytes_reverified':False,'mathematical_proof_verification':False,'author_turns':0},indent=2))
