"""Ascending literal-status intake; do not retain science for skipped PRs."""
import importlib.util, json, os, base64
from pathlib import Path
F=Path(__file__).resolve().parent
P=F.parents[1]
D=P/'audits/pr134_2306064/scoped_completion_transaction_20261007'
sp=importlib.util.spec_from_file_location('bounded_reads',D/'scoped_publish_v6.py')
s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
j={'children':[]};a=json.loads((D/'ROOT_FINAL_METADATA_ACCEPTANCE_RECEIPT.json').read_bytes())
s.require(a['status']=='ACCEPTED_COMPLETE' and not(D/'private/OPERATION_LOCK.json').exists(),'previous acceptance required')
registry=json.loads(s.git(['show',a['metadata_commit']+':draft_pr_publication_program_20260930/claimed_solved_scope_20261003/LIVE_DRAFT_ELIGIBILITY_REGISTRY.json'],j))
known={x['pr']:x for x in registry['rows']}
live=json.loads(s.run([s.GH,'pr','list','--repo','AlecKriebel/Math','--state','open','--limit','1000','--json','number,title,isDraft,headRefOid'],j))
ordered=sorted([x for x in live if x['isDraft'] and x['number']>134],key=lambda x:x['number'])
s.dump(F/'OPEN_DRAFT_METADATA_SNAPSHOT.json',{'UTC':s.utc(),'actual_PID':os.getpid(),'rows':ordered,'scope':'metadata inventory only; no mathematics reviewed'})
records=[]
with (F/'RESEARCH_LOG.md').open('a') as log:
    log.write('\n'+s.utc()+' — Ascending status-only intake after actual PR134 acceptance '+a['metadata_commit']+'. Program 23/99 = 23.23%; goal active and incomplete. A prior row-format assertion failed safely before any audit or PR action.\n')
for item in ordered:
    n=item['number'];p=json.loads(s.run([s.GH,'api','repos/AlecKriebel/Math/pulls/'+str(n)],j))
    s.require(p['state']=='open' and p['draft'] is True,'live draft changed')
    head=p['head']['sha'];s.require(head==item['headRefOid'],'head changed since inventory')
    s.require(n in known and known[n]['headRefOid']==head,'new/changed target requires separate unambiguous identification')
    targets=known[n]['status_projection']['targets'];s.require(len(targets)==1,'one exact problem required');pid=targets[0]['problem_id']
    c=json.loads(s.run([s.GH,'api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+head],j))
    b=base64.b64decode(c['content']);rows=[]
    for row in b.decode().splitlines():
        cells=[x.strip() for x in row.split('|')]
        if len(cells)>9 and cells[2].split(' / ',1)[0]==pid:rows.append((row,cells))
    s.require(len(rows)==1,'unique target status row required');row,cells=rows[0];status=cells[8]
    record={'PR':n,'original_head':head,'problem_id':pid,'code':cells[2],'literal_status':status,'effort':cells[9],
            'selected_row_sha256':s.digest(row.encode()),'whole_QUEUE_sha256':s.digest(b),'QUEUE_Git_blob':c['sha'],
            'UTC':s.utc(),'actual_reader_PID':os.getpid(),'reviewed':False,'original_substantive_findings_retained':False,
            'action':'ELIGIBLE_NEXT_CLAIMED_SOLVED' if status=='claimed_solved' else 'SKIP_UNTOUCHED_NONCLAIMED'}
    records.append(record);s.dump(F/('PR'+str(n)+'_STATUS_ONLY.json'),record)
    with (F/'RESEARCH_LOG.md').open('a') as log:log.write(record['UTC']+' — PR'+str(n)+': literal '+status+', submitted effort '+cells[9]+'. '+record['action']+'; no science review, repair or PR action performed.\n')
    print(json.dumps(record),flush=True)
    if status=='claimed_solved':break
s.dump(F/'INTAKE_AFTER_PR134.json',{'UTC':s.utc(),'actual_PID':os.getpid(),'prior_acceptance_commit':a['metadata_commit'],
                                  'records':records,'next_eligible':records[-1]['PR'] if records and records[-1]['literal_status']=='claimed_solved' else None,
                                  'program_workflow_percent':23/99*100,'goal_complete':False,'children':j['children']})
