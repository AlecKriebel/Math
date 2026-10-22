"""Fresh primary retrievals and immutable source pins; no service mutations."""
from pathlib import Path
import base64
import concurrent.futures
import datetime as dt
import hashlib
import json
import subprocess
import urllib.request
import urllib.error

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT/'audits/prior_full_solution_doi_coverage_01'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def gh(endpoint):
    p = subprocess.run(['gh','api','repos/AlecKriebel/Math/'+endpoint], capture_output=True)
    need(p.returncode == 0, p.stderr.decode(errors='replace')[:1000])
    return json.loads(p.stdout)

def retrieve(item):
    at = dt.datetime.now(dt.timezone.utc).isoformat()
    request = urllib.request.Request(item['url'], headers={'User-Agent':'Independent-publication-identity-audit/1.0'})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            raw = response.read(); status = response.status; final = response.url
            content_type = response.headers.get('Content-Type')
    except urllib.error.HTTPError as error:
        raw = error.read();status=error.code;final=error.url;content_type=error.headers.get('Content-Type')
    suffix = '.pdf' if 'application/pdf' in (content_type or '') or item['name'].endswith('_result') else '.json' if item['name'].endswith('_registry') else '.html'
    path = HERE/'private_sources'/(item['name']+suffix)
    path.write_bytes(raw)
    result={'name':item['name'],'url':item['url'],'at':at,'status':status,'final_url':final,
            'bytes':len(raw),'sha256':sha(raw),'content_type':content_type,'path':str(path.relative_to(HERE)),
            'preparer_sha256':item.get('sha256'),'matches_preparer_bytes':sha(raw)==item.get('sha256')}
    if suffix == '.pdf' and raw.startswith(b'%PDF'):
        p = subprocess.run(['pdftotext','-layout',str(path),str(path.with_suffix('.txt'))],capture_output=True)
        result['text_extraction_exit']=p.returncode
        if p.returncode == 0: result['text_sha256']=sha(path.with_suffix('.txt').read_bytes())
    return result

def bind(pr):
    disposition=json.loads((ROOT/f'PR{pr:04d}_DISPOSITION.json').read_text())
    evidence=json.loads((ROOT/f'eligibility/pr{pr:04d}.json').read_text())
    live=gh('pulls/'+str(pr));head=live['head']['sha'];base=live['base']['sha']
    need(head==disposition['inventory_head_sha']==evidence['inventory_head_sha'],'Live head changed '+str(pr))
    need(base==disposition['inventory_base_sha']==evidence['inventory_base_sha'],'Live base changed '+str(pr))
    body=(live['body'] or '').encode();need(sha(body)==disposition['inventory_body_sha256'],'Live body changed '+str(pr))
    c=gh('compare/'+base+'...'+head);files=c['files']
    need(len(files)<300 and c['base_commit']['sha']==base and c['commits'][-1]['sha']==head,'Comparison binding')
    actual_by_name={f['filename']:f for f in files}
    expected={(f['filename'],f['sha'] if f['sha'] is not None else actual_by_name.get(f['filename'],{}).get('sha'),f['status']) for f in evidence['files']}
    actual={(f['filename'],f['sha'],f['status']) for f in files}
    if actual!=expected or len(files)!=evidence['file_count']:
        failure={'pr':pr,'base':base,'head':head,'actual_count':len(files),'expected_count':evidence['file_count'],
                 'actual_only':sorted(actual-expected),'cached_only':sorted(expected-actual)}
        (HERE/f'BINDING_DIFFERENCE_PR{pr}.json').write_text(json.dumps(failure,indent=2)+'\n')
        raise RuntimeError('Complete paths changed PR'+str(pr)+'; see BINDING_DIFFERENCE receipt')
    need(not any(Path(f['filename']).name=='QUEUE.md' for f in files),'Unexpected QUEUE change')
    selected=[]
    directory=HERE/'private_sources'/f'pr{pr:04d}_authored';directory.mkdir(exist_ok=True)
    (directory/'BODY.md').write_bytes(body)
    for f in files:
        name=Path(f['filename']).name
        p=subprocess.run(['git','show',head+':'+f['filename']],capture_output=True)
        need(p.returncode==0,'Missing immutable object '+f['filename'])
        raw=p.stdout;blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        need(blob==f['sha'],'Git blob mismatch')
        if name.endswith(('.md','.json')):
            (directory/name).write_bytes(raw)
            selected.append({'file':f['filename'],'bytes':len(raw),'sha256':sha(raw),'git_blob':blob})
    return {'pr':pr,'head':head,'base':base,'body_sha256':sha(body),'state':live['state'],'draft':live['draft'],
            'merged':live['merged'],'complete_changed_paths':[(f['filename'],f['sha'],f['status']) for f in files],
            'no_QUEUE_change':True,'cached_missing_blobs_rebound_from_immutable_comparison':sum(f['sha'] is None for f in evidence['files']),'selected_texts':selected}

def main():
    items=json.loads((HERE/'INPUT_CANDIDATES.json').read_text())['items'];prs={x['pr'] for x in items}
    retrievals=json.loads((SOURCE/'BATCH_B_PRIMARY_RETRIEVALS.json').read_text())
    selected=[x for x in retrievals if int(x['name'].split('_')[0][2:]) in prs]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results=list(pool.map(retrieve,selected))
    (HERE/'PRIMARY_RETRIEVALS.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        bindings=list(pool.map(bind,sorted(prs|{1176})))
    (HERE/'PR_BINDINGS.json').write_text(json.dumps(bindings,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'sources':len(results),'all_status_200':all(x['status']==200 for x in results),
      'fresh_pdfs':sum(x['path'].endswith('.pdf') for x in results),'pdf_mismatches':[x['name'] for x in results if x['path'].endswith('.pdf') and not x['matches_preparer_bytes']],
      'prs':len(bindings),'complete_paths':sum(len(x['complete_changed_paths']) for x in bindings)},indent=2))

if __name__=='__main__':
    main()
