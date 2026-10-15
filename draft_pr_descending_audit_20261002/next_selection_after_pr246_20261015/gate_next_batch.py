"""Read-only eligibility gates; non-claimed results receive no science review."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import base64
import json
import re
import subprocess

P=Path(__file__).resolve().parent
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
rows=json.loads((P/'OPEN_DRAFT_INVENTORY.json').read_text())
batch=sorted([x for x in rows if 239<=x['number']<=245],key=lambda x:-x['number'])
assert [x['number'] for x in batch]==list(range(245,238,-1))

def gate(item):
    number=item['number']
    T=P/'private_transport'/str(number)
    T.mkdir(parents=True,exist_ok=False)
    def get(path,name):
        run=subprocess.run([GH,'api','repos/AlecKriebel/Math/'+path],capture_output=True,timeout=90)
        (T/(name+'.json')).write_bytes(run.stdout)
        (T/(name+'.stderr.txt')).write_bytes(run.stderr)
        assert run.returncode==0,(number,name)
        return json.loads(run.stdout)
    pr=get('pulls/'+str(number),'PR')
    base={'utc':datetime.now(timezone.utc).isoformat(),'PR':number,'title':pr['title'],'head':pr['head']['sha'],
          'state':pr['state'],'draft':pr['draft'],'merged':pr['merged'],'read_only_gate':True}
    if pr['state']!='open' or not pr['draft'] or pr['merged']:
        base.update(eligible=False,reason='not_current_open_draft')
    else:
        ids=re.findall(r'\d{5,}',pr['head']['ref'])
        assert len(ids)==1,(number,pr['head']['ref'])
        pid=ids[0]
        q=get('contents/unsolved_math_prioritization/QUEUE.md?ref='+pr['head']['sha'],'QUEUE')
        candidates=[r for r in base64.b64decode(q['content']).decode().splitlines() if re.match(r'\|\s*\d+\s*\|\s*'+pid+r'\s*/',r)]
        assert len(candidates)==1,(number,pid)
        row=candidates[0]
        status=row.split('|')[8].strip()
        base.update(problem_id=pid,Queue_path='unsolved_math_prioritization/QUEUE.md',Queue_blob=q['sha'],
                    queue_row=row,status=status,eligible=status=='claimed_solved',reason='exact_current_PR_head_queue_status')
    (P/f'PR{number}_ELIGIBILITY.json').write_text(json.dumps(base,indent=2)+'\n')
    return base

with ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(gate,batch))
selected=next((r for r in results if r['eligible']),None)
decision={'utc':datetime.now(timezone.utc).isoformat(),'from_cursor':245,'PR8_excluded':True,'read_only_current_head_gates':results,
          'selected':selected,'highest_eligible_in_gated_range':selected['PR'] if selected else None,
          'no_science_review_or_mutation_of_non_claimed_status':True}
(P/'SELECTION.json').write_text(json.dumps(decision,indent=2)+'\n')
print(json.dumps({'gates':[{'PR':x['PR'],'status':x.get('status'), 'eligible':x['eligible']} for x in results],
                  'selected':selected},indent=2))
