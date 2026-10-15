from pathlib import Path
import hashlib,json,datetime,shutil,subprocess,sqlite3
D=Path(__file__).resolve().parent;ROOT=D.parents[3];S=D/'submitted/unsolved_math_prioritization/attempts/5100063';R=D/'private_reading';R.mkdir()
old=ROOT/'draft_pr_descending_audit_20261002/audits/pr254_5100020/initial_review_20261013/primary_source_reading_copies';rows=[]
for item in json.loads((S/'source_manifest.json').read_text())['sources']:
 p=old/item['file'];b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==item['sha256'];q=R/item['file'];shutil.copyfile(p,q);subprocess.run(['pdftotext','-layout',str(q),str(q.with_suffix('.txt'))],check=True)
 rows.append(dict(**item,bytes=len(b),reused_private_reading_copy=str(p),copied_into_private=str(q),hash_matches_frozen_source_pin=True,full_text_or_visual_read_by_root=False))
now=datetime.datetime.now(datetime.timezone.utc).isoformat();(D/'ROOT_PRIMARY_REUSE.json').write_text(json.dumps(dict(utc=now,sources=rows,private_copies_not_redistributed=True,arxiv_landing_page_version_history_freshly_read=True,DOI_web_reader_failed_not_fresh_publisher_download=True),indent=2)+'\n')
up=D/'private_upstream';up.mkdir();dbpath=ROOT/'unsolved_math_prioritization/cache/catalog.sqlite'
con=sqlite3.connect(dbpath.as_uri()+'?mode=ro',uri=True);p,r=con.execute('select payload,report from records where key=?',('5100063',)).fetchone();rev=con.execute('select revision from metadata').fetchone()[0];con.close();p=json.loads(p);r=json.loads(r)
assert p==json.loads((S/'source_record.json').read_text());assert r==json.loads((S/'prior_imported_report.json').read_text())
raw=json.dumps(dict(record=p,report=r,revision=rev),indent=2)+'\n';(up/'complete_record.json').write_text(raw)
receipt=dict(utc=now,record_key='5100063',revision=rev,sqlite_URI_mode_ro=True,native_record_and_prior_report_exact_matches=True,complete_record_payload_sha256=hashlib.sha256(raw.encode()).hexdigest(),statement_hash=hashlib.sha256((p.get('statement') or '').encode()).hexdigest(),review_hash=hashlib.sha256(json.dumps([p,r],sort_keys=True).encode()).hexdigest(),record_and_report_read_by_root_from_submitted_copies=True,no_cache_writes=True)
(D/'UPSTREAM_PROVENANCE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'sources_reused':len(rows),'upstream':receipt},indent=2))
