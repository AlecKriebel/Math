#!/usr/bin/env python3
"""Exact owned checkpoint after actual PR38 acceptance; active scopes excluded."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import subprocess

R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_publication_program_20260930';A=P/'audits'
owned=set();closures=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def run(args):return subprocess.run(args,cwd=R,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
def add(p):
    assert p.is_file() and not p.is_symlink() and not any(q.is_symlink() for q in p.parents)
    owned.add(p.relative_to(R).as_posix())
def manifest(p):
    o=json.loads(p.read_bytes());rows=next(o[k] for k in ('files','members','authored_files','first_party') if k in o)
    assert type(rows) is list;names=set()
    for row in rows:
        n=row['path'];assert n not in names and not n.startswith('/') and all(c not in ('','.','..') for c in n.split('/'));names.add(n)
        q=p.parent/n;b=q.read_bytes();size=row.get('bytes',row.get('size'));assert type(size) is int and len(b)==size and sha(b)==row['sha256'];add(q)
    add(p);closures.append({'path':p.relative_to(R).as_posix(),'members':len(rows),'sha256':sha(p.read_bytes())})

assert run(['git','branch','--show-current']).strip()==b'main'
assert not run(['git','diff','--cached','--name-only']).strip()
post=json.loads((A/'pr38_2765/ROOT_POST_ACCEPTANCE_VERIFICATION.json').read_bytes())
assert post['status']=='PASS' and post['complete_primary_prs']==28 and post['current_targets']==29 and post['consumed_original_substantive_turns']==35
manifest(R/'unsolved_math_prioritization/attempts/2765/MANIFEST.json')
for rel in ('pr39_9500008/whole_current_source_first_family/MANIFEST.json',
            'pr40_2814/whole_current_source_first_family/FIRST_PARTY_MANIFEST.json',
            'pr40_2814/reviewed_candidate/MANIFEST.json'):
    manifest(A/rel)
for n in ('ROOT_FINAL_RECONCILIATION_INSPECTION.json','ROOT_AUTOMATIC_MERGE_INSPECTION.json',
          'ROOT_MERGE_STAGING_INSPECTION.json','execute_root_integration.py','integration_preflight.json',
          'integration_queue_before.md','integration_inventory_before.json','accepted_pr_body.md',
          'integration_merge_queue_before.md','integration_check.json','integration_prepush.json',
          'remote_merge_receipt.json','acceptance.json','state_mirror_bindings.json','state_mirror_plan.json',
          'state_mirror_intent.json','state_mirror_receipt.json','ROOT_POST_ACCEPTANCE_VERIFICATION.json',
          'RESEARCH_LOG.md','ROOT_RESEARCH_LOG.md'):
    add(A/'pr38_2765'/n)
for phase in ('preflight','overlay','prepush','finalize','mirror','post'):
    for n in ('CAPTURE.json','prelaunch_source.py','prelaunch_guards.py','stdout.bin','stderr.bin'):
        add(A/'pr38_2765'/('root_integration_'+phase+'_actual_capture')/n)
add(A/'pr39_9500008/ROOT_WHOLE_CURRENT_REVIEW.json');add(A/'pr39_9500008/ROOT_RESEARCH_LOG.md')
for n in ('freeze_root_current.py','ROOT_CURRENT_INPUT_PREIMAGES.json','ROOT_SCIENCE_CARD.json',
          'ROOT_CURRENT_SOURCE_REVIEW.json','ROOT_CURRENT_PACKET_INSPECTION.json','ROOT_WHOLE_CURRENT_REVIEW.json','ROOT_RESEARCH_LOG.md'):
    add(A/'pr40_2814'/n)
for n in ('CAPTURE.json','prelaunch_source.py','stdout.bin','stderr.bin'):
    add(A/'pr40_2814/root_current_freeze_actual_capture'/n)
snap=json.loads((A/'pr41_9700035/snapshot_manifest.json').read_bytes())
for row in snap['files']:
    p=A/'pr41_9700035/source_snapshot'/row['path'];b=p.read_bytes();assert len(b)==row['size'] and sha(b)==row['sha256'];add(p)
for n in ('snapshot_manifest.json','pr_input/metadata.json','pr_input/diff.patch','ROOT_RESEARCH_LOG.md'):
    add(A/'pr41_9700035'/n)
for n in ('RESEARCH_LOG.md','inventory.json'):add(P/n)
for n in ('state.json','history.jsonl'):add(R/'unsolved_math_prioritization'/n)
add(Path(__file__).resolve())
now=dt.datetime.now(dt.timezone.utc).isoformat()
notes={
    'pr38_2765':'Acceptance100%, actual original-head two-parent merge198b8acb0 published and postPASS PID94451. Exact1514-member accepted manifest, named12-column queue only, allprior28states/fullhistory retained plusone presentacceptance; native29targets/35originalturns. Full target unsolved (resolution0%), original2/5,new0/audit0; no paper/DOI/tracker.',
    'pr39_9500008':'Acceptance approximately96%, independent whole-current45+self clean and root whole review94419a9f passed. Strongest verified bounded-piece Brownian coupling/weak diffusive limit; exact finite random origin remains unproved (discovery0%). Both failed/successful typed attempts and exact five-field administrative schema diff retained; literal original ledger uses numbers[1,2]. Future integration requires fresh post38 native rebase. Original2/5,new0/audit0, no paper/DOI.',
    'pr40_2814':'Acceptance approximately94%, actual current freeze239+self/216deps/110JSON passed PID80794; root owncurrent719b08f8 and whole review5ce4f40f passed. New independent whole25+self/21foreign clean, initialbackground exposure/standardimports qualified. Credited existing source coverage is valid conservative unsolved/sourcehold partial; originalSOURCE_STATUS unchanged, projectdiscovery0%. Original0/5,new0/audit0; fresh future integration rebase pending, no paper/DOI.',
    'pr41_9700035':'Audit approximately15%, independent two materially distinct families sealed original SIRSN target before candidate proof. Literal span is union of prescribed pair routes, correcting imported Steiner wording. Primary2012/2014 numbering and extra-assumption scope separately reconstructed. Both reviewers identified a repairable conditional-probability presentation issue in ancillary Kahn moment applicability; root reading/actual reproduction/current review stillpending. Exact unconditional discovery0%; no substantive attempt added.'}
for folder,note in notes.items():
    with (A/folder/'ROOT_RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — '+note+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — Program28/180=15.5556% accepted; earlier PR18/20 holds preserved. '+' '.join(notes.values())+'\n')
pre=P/'checkpoints/CHECKPOINT_PR38_ACCEPTANCE.json';assert not pre.exists()
records=[{'path':n,'bytes':len((R/n).read_bytes()),'sha256':sha((R/n).read_bytes())} for n in sorted(owned)]
pre.write_text(json.dumps({'utc':now,'head_before':run(['git','rev-parse','HEAD']).decode().strip(),'accepted':28,'total':180,
    'completion_percent':28/180*100,'closed_manifests':closures,'exact_owned_files':records,
    'excluded':'All active39/40integration preparation and41independent scopes; all foreign primary PDFs/text/images/caches/private fixtures; both unrelated tracked referee logs.'},indent=2)+'\n');add(pre)
names=sorted(owned)
for i in range(0,len(names),150):run(['git','add','-f','--',*names[i:i+150]])
staged={n for n in run(['git','diff','--cached','--name-only','-z']).decode().split('\0') if n};assert staged<=owned
pins={r['path']:r for r in records}
for n in staged:
    assert not n.startswith('paper_ii_simultaneous_amplification_referee_audit_2026-08-22/')
    if n in pins:b=(R/n).read_bytes();assert len(b)==pins[n]['bytes'] and sha(b)==pins[n]['sha256']
checked=0
for entry in run(['git','ls-files','--stage','-z']).split(b'\0'):
    if not entry:continue
    meta,n=entry.split(b'\t',1);name=n.decode()
    if name not in staged:continue
    mode,oid,stage=meta.split();assert mode in (b'100644',b'100755') and stage==b'0';b=(R/name).read_bytes();assert oid.decode()==hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest();checked+=1
assert checked==len(staged)
print(json.dumps({'status':'EXACT_OWNED_ACCEPTANCE_CHECKPOINT_STAGED','owned':len(owned),'staged':len(staged),'bytes':sum(len((R/n).read_bytes()) for n in staged),'accepted':28,'percent':28/180*100}))
