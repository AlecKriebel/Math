from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile,subprocess,os
ROOT=Path('/Users/alec/Documents/Math')
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
gate=json.loads((HERE/'tmp/inputs'/AUDIT.relative_to(ROOT)/'FINAL_PUBLICATION_GATE.json').read_bytes())
original=gate['original_pr_head']
native={}
env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'}
with zipfile.ZipFile(AUDIT/'publication/gns_verification.zip') as z:
    for rel,pin in gate['reviewed_inputs'].items():
        if not rel.startswith('native/'):continue
        repo_path=rel[len('native/'):]
        result=subprocess.run(['git','cat-file','blob',original+':'+repo_path],cwd=ROOT,env=env,capture_output=True)
        candidate='candidate/'+repo_path.split('/attempts/30001184/',1)[1]
        archive_bytes=z.read(candidate)
        native[rel]={'original_blob_exists':result.returncode==0,
                     'original_sha256':hashlib.sha256(result.stdout).hexdigest() if result.returncode==0 else None,
                     'original_matches_pin':result.returncode==0 and hashlib.sha256(result.stdout).hexdigest()==pin['sha256'],
                     'archive_entry':candidate,'archive_matches_pin':hashlib.sha256(archive_bytes).hexdigest()==pin['sha256']}
    manifest=json.loads(z.read('PACKAGE_MANIFEST.json'))
    entries=[n for n in z.namelist() if n!='PACKAGE_MANIFEST.json']
    transport_in_names=any('native_transport' in n for n in z.namelist())
    transport_in_content=any(b'native_transport' in z.read(n) for n in entries)
    integrity={}
    values=manifest.get('files',manifest)
    for receipt in values:
        name=receipt['path']
        data=z.read(name)
        integrity[name]=hashlib.sha256(data).hexdigest()==receipt['sha256'] and len(data)==receipt['bytes']
pdf=AUDIT/'publication/gns_generation_counterexample.pdf'
text=subprocess.run(['pdftotext',str(pdf),'-'],capture_output=True)
pdf_check={'extracted':text.returncode==0,'text_sha256':hashlib.sha256(text.stdout).hexdigest(),
           'native_transport_in_text':b'native_transport' in text.stdout,'transport_phrase_in_text':b'native transport' in text.stdout.lower()}
result={'checked_utc':datetime.now(timezone.utc).isoformat(),'original_pr_head':original,'native29_count':len(native),
        'native29_match_original':all(v['original_matches_pin'] for v in native.values()),
        'native29_match_zip':all(v['archive_matches_pin'] for v in native.values()),'native':native,
        'archive_manifest_files':len(integrity),'archive_all_hashes_match':all(integrity.values()),
        'transport_in_zip_names':transport_in_names,'transport_in_zip_content':transport_in_content,'pdf':pdf_check}
(HERE/'ORIGINAL_ARCHIVE_BINDING.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='native'},indent=2))
if not result['native29_match_original'] or not result['native29_match_zip'] or not result['archive_all_hashes_match'] or transport_in_names or transport_in_content or not pdf_check['extracted'] or pdf_check['native_transport_in_text']:raise SystemExit(1)
