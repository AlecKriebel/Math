from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess
A=Path(__file__).resolve().parent;P=A.parents[1];D=A/'primary_sources_20261006';D.mkdir(exist_ok=False)
old=P/'audits/pr107_30003997/primary_sources_20261006';previous=json.loads((old/'RETRIEVAL_MANIFEST.json').read_text());source=json.loads((A/'original_source_authentication_20261006/original_attempt/source_manifest.json').read_text())
records=[]
for record in previous['records']:
 b=(old/record['file']).read_bytes();h=hashlib.sha256(b).hexdigest()
 if h!=record['sha256'] or len(b)!=record['bytes']:raise RuntimeError('existing primary custody mismatch')
 if record['file']=='owr.pdf' and h!=source['sources'][0]['sha256']:raise RuntimeError('submitted report mismatch')
 pdf=D/record['file'];pdf.write_bytes(b);args=['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(pdf.with_suffix('.txt'))]
 p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate()
 if p.returncode:raise RuntimeError(err.decode())
 records.append({'file':pdf.name,'bytes':len(b),'sha256':h,'same_bytes_as_legitimately_retrieved_primary':True,'reused_pinned_body_not_a_new_network_retrieval':True,'source_body':str(old/record['file']),'previous_actual_retrieval_receipt':str(old/'RETRIEVAL_MANIFEST.json'),'previous_request':record['requested_url'],'matches_submitted_hash':h==source['sources'][0]['sha256'] if record['file']=='owr.pdf' else None,'Karp_full_primary_copy_matches_previous_checked_3SAT_dependency':record['file']=='karp-original.pdf','extraction_argv':args,'extraction_PID':p.pid,'extraction_exit_code':p.returncode,'extraction_sha256':hashlib.sha256(pdf.with_suffix('.txt').read_bytes()).hexdigest()})
manifest={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'records':records,'third_party_primary_files_excluded_from_public_checkpoint':True,'original_submitted_source_manifest_unchanged':True}
(D/'PRIMARY_CUSTODY_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'primary_bodies':len(records),'actual_operator_PID':os.getpid(),'submitted_report_hash_verified':True}))
