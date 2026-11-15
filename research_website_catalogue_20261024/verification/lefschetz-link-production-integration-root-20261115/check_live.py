from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import json,subprocess,hashlib
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S=P/'verification/lefschetz-link-private-stage-sol-20261115'
O=Path(__file__).resolve().parent
D=O/'live-http';D.mkdir(exist_ok=False)
rows=json.loads((S/'OVERLAY_MANIFEST.json').read_text())['files']
def request(item):
 i,row=item
 relative=row['path']
 uri=relative[:-10] if relative.endswith('index.html') else relative
 url='https://aleckriebel.com/'+uri
 stem=D/('response-%02d'%i)
 command=['curl','-q','--connect-timeout','10','--max-time','40','--dump-header',str(stem)+'.headers','--output',str(stem)+'.body','--write-out','%{json}',url]
 r=subprocess.run(command,capture_output=True)
 (Path(str(stem)+'.curl-metadata.json')).write_bytes(r.stdout)
 (Path(str(stem)+'.stderr')).write_bytes(r.stderr)
 metadata=json.loads(r.stdout) if r.stdout else None
 body=Path(str(stem)+'.body').read_bytes() if Path(str(stem)+'.body').exists() else None
 result={'requested_URL':url,'public_path':relative,'curl_exit_code':r.returncode,'HTTP_status':metadata['http_code'] if metadata else None,'effective_URL':metadata['url_effective']if metadata else None,'actual_redirects':metadata['num_redirects']if metadata else None,'body_bytes':len(body)if body is not None else None,'body_SHA256':hashlib.sha256(body).hexdigest()if body is not None else None,'headers_path':str(stem)+'.headers','body_path':str(stem)+'.body','whole_curl_metadata_path':str(stem)+'.curl-metadata.json','stderr_path':str(stem)+'.stderr'}
 result['whole_body_matches_sealed_original']=body is not None and len(body)==row['bytes'] and result['body_SHA256']==row['SHA256'] and body==(S/'candidate-a/public'/relative).read_bytes()
 return result
with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(request,enumerate(rows)))
receipt={'UTC':datetime.now(timezone.utc).isoformat(),'website_commit':'46773fd3d0e7289f5ab79bfc9f8ddf382fa508fc','actual_ordinary_GETs':11,'cache_busters_custom_bypass_or_retries':False,'results':results,'all11_HTTP200_and_whole_bytes_identical':all(r['curl_exit_code']==0 and r['HTTP_status']==200 and r['whole_body_matches_sealed_original']for r in results),'browser_native_Sheet_canonical_verification_claimed':False}
(O/'live-http.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'PASS':receipt['all11_HTTP200_and_whole_bytes_identical'],'responses':len(results),'status_sequence':[r['HTTP_status']for r in results],'body_bytes':[r['body_bytes']for r in results]},indent=2))
if not receipt['all11_HTTP200_and_whole_bytes_identical']:raise SystemExit(1)

