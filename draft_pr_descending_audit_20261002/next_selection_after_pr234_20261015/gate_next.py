"""Native read-only descending eligibility gates; continue after PR234 qualified historical scope skip."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import base64
import hashlib
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
BASE='repos/AlecKriebel/Math/'
PRIVATE=HERE/'private_transport'
PRIVATE.mkdir(exist_ok=False)


def get(path,target):
    run=subprocess.run([GH,'api',BASE+path],capture_output=True,timeout=60)
    target.write_bytes(run.stdout)
    target.with_suffix('.stderr.txt').write_bytes(run.stderr)
    assert run.returncode==0,str(target)
    return json.loads(run.stdout)


# The prior immediate inventory found page1 ending at PR180. Authenticate a
# fresh page containing the234 boundary before selecting its highest lower PR.
inventory=get('pulls?state=open&sort=created&direction=asc&per_page=100&page=2',PRIVATE/'inventory_page2.json')
numbers=[x['number'] for x in inventory]
assert min(numbers)<234<=max(numbers)
rows=[dict(number=x['number'],title=x['title'],head=x['head']['sha'],branch=x['head']['ref'])
      for x in inventory if x['draft'] and x['number']<234 and x['number']!=8]
rows.sort(key=lambda x:-x['number'])
(HERE/'OPEN_DRAFT_BOUNDARY_INVENTORY.json').write_text(json.dumps(rows,indent=2)+'\n')
(HERE/'INVENTORY_RECEIPT.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),page=2,
    page_items=len(inventory),minimum_PR=min(numbers),maximum_PR=max(numbers),
    exact_boundary_contained=True,filtered_lower_drafts=len(rows),PR8_excluded=True),indent=2)+'\n')


def gate(item):
    n=item['number']
    out=PRIVATE/str(n);out.mkdir()
    pr=get('pulls/'+str(n),out/'PR.json')
    result=dict(utc=datetime.now(timezone.utc).isoformat(),PR=n,title=pr['title'],head=pr['head']['sha'],
                state=pr['state'],draft=pr['draft'],merged=pr['merged'],read_only_gate=True)
    if pr['state']!='open' or not pr['draft'] or pr['merged']:
        result.update(eligible=False,reason='not_current_open_draft')
    else:
        ids=re.findall(r'\d{4,}',pr['head']['ref'])
        assert len(ids)==1,(n,pr['head']['ref'])
        pid=ids[0]
        q=get('contents/unsolved_math_prioritization/QUEUE.md?ref='+pr['head']['sha'],out/'QUEUE.json')
        raw=base64.b64decode(q['content'])
        candidates=[line for line in raw.decode().splitlines() if re.match(r'\|\s*\d+\s*\|\s*'+pid+r'\s*/',line)]
        assert len(candidates)==1,(n,pid)
        row=candidates[0];status=row.split('|')[8].strip()
        result.update(problem_id=pid,Queue_path='unsolved_math_prioritization/QUEUE.md',Queue_blob=q['sha'],
                      Queue_sha256=hashlib.sha256(raw).hexdigest(),queue_row=row,status=status,
                      eligible=status=='claimed_solved',reason='exact_current_PR_head_queue_status')
    (HERE/f'PR{n}_ELIGIBILITY.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


results=[];selected=None
for start in range(0,len(rows),8):
    with ThreadPoolExecutor(max_workers=4) as pool:batch=list(pool.map(gate,rows[start:start+8]))
    results.extend(batch)
    selected=next((x for x in results if x['eligible']),None)
    if selected:break
decision=dict(utc=datetime.now(timezone.utc).isoformat(),from_cursor=233,
    prior_PR234_disposition='already_solved after verified qualified historical credit correction; exact extension novelty unresolved; open draft immediately skipped',held_PR239_uncompleted=True,
    goal_blocked=False,reason='Other authorized claimed_solved cases remain independently auditable in descending intake order',
    PR8_excluded=True,read_only_current_head_gates=results,selected=selected,
    no_science_review_or_mutation_of_non_claimed_status=True)
(HERE/'SELECTION.json').write_text(json.dumps(decision,indent=2)+'\n')
print(json.dumps(dict(gates=[dict(PR=x['PR'],status=x.get('status'),eligible=x['eligible']) for x in results],selected=selected),indent=2))
