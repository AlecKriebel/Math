import base64,concurrent.futures,json,re,subprocess
from pathlib import Path
from datetime import datetime,timezone
P=Path(__file__).resolve().parent
rows=json.loads((P/'inventory_metadata.json').read_text())
def queue_rows(text):
    found={}
    for line in text.splitlines():
        c=[s.strip() for s in line.split('|')]
        if len(c)>9 and re.match(r'^\d+\s*/',c[2]):
            found[c[2].split('/')[0].strip()]={'status':c[8],'row':line}
    return found
main=queue_rows(Path('unsolved_math_prioritization/QUEUE.md').read_text())
def inspect(r):
    nums=set(re.findall(r'(?<!\d)\d{4,8}(?!\d)',r['headRefName']+' '+r['title']))
    ids=sorted(nums & main.keys())
    if len(ids)!=1:
        f=subprocess.run(['gh','pr','view',str(r['number']),'--repo','AlecKriebel/Math','--json','files'],capture_output=True,text=True,check=True)
        ids=sorted(set(re.findall(r'attempts/(\d+)/',f.stdout)))
    content=subprocess.run(['gh','api',f'repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref={r["headRefOid"]}','-H','Accept: application/vnd.github.raw+json'],capture_output=True,text=True,check=True).stdout
    if content.startswith('{'):
        payload=json.loads(content)
        if 'content' in payload: content=base64.b64decode(payload['content']).decode()
    q=queue_rows(content)
    entries=[{'id':i,'pr_head_status':q.get(i,{}).get('status'),'main_status_at_inventory':main.get(i,{}).get('status'),'pr_head_queue_row':q.get(i,{}).get('row')} for i in ids]
    eligible=len(entries)==1 and entries[0]['pr_head_status']=='claimed_solved'
    return {**r,'entries':entries,'eligible':eligible,'disposition':'pending_audit' if eligible else 'skipped_status_gate','inventory_utc':datetime.now(timezone.utc).isoformat()}
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    futures={pool.submit(inspect,r):r for r in rows}
    for f in concurrent.futures.as_completed(futures):
        try: result=f.result()
        except Exception as e: result={**futures[f],'inventory_error':str(e),'eligible':False,'disposition':'gate_unresolved'}
        results.append(result)
        (P/'inventory_progress.json').write_text(json.dumps(sorted(results,key=lambda x:x['number']),indent=2)+'\n')
results.sort(key=lambda x:x['number'])
(P/'inventory.json').write_text(json.dumps(results,indent=2)+'\n')
print('Inventory count:',len(results),'eligible:',sum(r['eligible'] for r in results))
for r in results:
    if r['eligible'] or 'inventory_error' in r: print(r['number'],[(e['id'],e['pr_head_status'],e['main_status_at_inventory']) for e in r.get('entries',[])],r.get('inventory_error',''))
