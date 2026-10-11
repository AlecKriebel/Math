#!/usr/bin/env python3
"""Private synthetic gate/UTC/queue controls; no production source import or execution."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, os, re, sys
F=Path(__file__).absolute().parent; A=F.parent; P=A/'current_preparation_family'
assert __debug__ and not sys.flags.optimize
checks=[]
def ck(n,v):
    if not v: raise AssertionError(n)
    checks.append(n)
def need(v):
    if not v: raise ValueError('private gate rejects')
def bad(n,fn):
    try: fn()
    except (ValueError,TypeError,KeyError): ck(n,True); return
    raise AssertionError(n+' unexpectedly accepted')
def equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return set(a)==set(b) and all(equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
def clock(v):
    need(type(v) is str)
    t=dt.datetime.fromisoformat(v.replace('Z','+00:00')); need(t.tzinfo is not None and t.utcoffset()==dt.timedelta(0)); return t
prep=json.loads((P/'PREPARATION_MANIFEST.json').read_bytes()); start=clock(prep['utc']); now=dt.datetime.now(dt.timezone.utc)
def interval(v): need(start<=clock(v)<=now)
for v in [None,True,1,'2026-10-03T05:31:00','2026-10-03T05:31:00+01:00','2026-10-03T05:31:00-01:00','bad','1999-01-01T00:00:00+00:00','2099-01-01T00:00:00+00:00']: bad('invalid approvalUTC '+repr(v),lambda v=v:interval(v))
for v in [now.isoformat(),now.isoformat().replace('+00:00','Z')]: interval(v); ck('valid approval UTC '+v,True)
flags=json.loads((P/'DRAFT_ROOT_READ_LEDGER.json').read_bytes())['root_flags']; good_flags={k:True for k in flags}
read={'schema':'PR47_ROOT_READ_LEDGER_v1','operative_preparation_directory':'current_preparation_family','reading_completed':True,'root_flags':good_flags,'reading_notes':'Private synthetic test value: never an actual ROOT prerequisite.','created_utc':now.isoformat(),'original_substantive_attempts':1,'new_substantive_attempts':0,'audit_turns':0}
def reading(o):
    need(o['schema']=='PR47_ROOT_READ_LEDGER_v1' and o['operative_preparation_directory']=='current_preparation_family' and o['reading_completed'] is True and equal(o['root_flags'],good_flags) and type(o['reading_notes']) is str and len(o['reading_notes'].strip())>=40); interval(o['created_utc'])
    for k,n in [('original_substantive_attempts',1),('new_substantive_attempts',0),('audit_turns',0)]: need(type(o[k]) is int and o[k]==n)
reading(read); ck('synthetic reading baseline',True)
for k,v in [('schema','old_PASS'),('operative_preparation_directory','another_family'),('reading_completed',1),('reading_completed',False),('reading_notes','  '),('created_utc',None),('original_substantive_attempts',True),('new_substantive_attempts',False),('audit_turns',False)]: bad('reading rejects '+k+repr(v),lambda k=k,v=v:reading(dict(read,**{k:v})))
reading(dict(read,future_merge_approved=True)); ck('extra general reading key not rejected explicitly; no consumed approval',True)
head='487327b2412c436ae69e8c52bf353a9a1fb7594e'; base='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
literals=[head,base,'Status: unsolved','Original turns: 1/5; new: 0; audit: 0','Universal normal vanishing: false','Realized example instanton rank: unknown','Full problem solved: false','Novelty: false','NEW whole-current review: PENDING','Paper/new DOI/tracker: false','Sivek','Zentner','Proposition6.1']
cert='# ROOT PR47 corrected unresolved scope acceptance\nROOT_SCOPE_ACCEPTED_CORRECTED_UNRESOLVED_ONLY\n'+'\n'.join(literals)
def certificate(c):
    need(c.splitlines()[0]=='# ROOT PR47 corrected unresolved scope acceptance' and c.splitlines().count('ROOT_SCOPE_ACCEPTED_CORRECTED_UNRESOLVED_ONLY')==1 and 'DRAFT' not in c)
    for literal in literals: need(literal in c)
certificate(cert); ck('synthetic scope baseline',True)
for literal in literals: bad('scope omission '+literal,lambda literal=literal:certificate(cert.replace(literal,'',1)))
for label,c in [('duplicate sentinel',cert+'\nROOT_SCOPE_ACCEPTED_CORRECTED_UNRESOLVED_ONLY'),('no sentinel',cert.replace('ROOT_SCOPE_ACCEPTED_CORRECTED_UNRESOLVED_ONLY','')),('draft marker',cert+'\nDRAFT'),('wrong first line','wrong\n'+cert)]: bad('scope '+label,lambda c=c:certificate(c))
native={'unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}|{'draft_pr_publication_program_20260930/inventory.json'}
files=[{'path':n,'bytes':0,'sha256':'a'*64,'full_mode':0o644} for n in sorted(native)]
fresh={'schema':'PR47_ROOT_FRESH13_INPUT_PREIMAGES_v1','operative_preparation_directory':'current_preparation_family','approved_by_root':True,'created_utc':now.isoformat(),'reason':'Private synthetic thirteen-row test; does not approve any live input.','current_head':'a'*40,'files':files}
def fresh13(o):
    need(set(o)=={'schema','operative_preparation_directory','approved_by_root','created_utc','reason','current_head','files'} and o['schema']=='PR47_ROOT_FRESH13_INPUT_PREIMAGES_v1' and o['operative_preparation_directory']=='current_preparation_family' and o['approved_by_root'] is True and type(o['reason']) is str and len(o['reason'].strip())>=40 and type(o['current_head']) is str and re.fullmatch('[0-9a-f]{40}',o['current_head']) is not None and type(o['files']) is list and len(o['files'])==13); interval(o['created_utc']); seen=set()
    for r in o['files']:
        need(type(r) is dict and set(r)=={'path','bytes','sha256','full_mode'} and type(r['path']) is str and r['path'] in native and r['path'] not in seen and type(r['bytes']) is int and r['bytes']>=0 and type(r['sha256']) is str and re.fullmatch('[0-9a-f]{64}',r['sha256']) is not None and type(r['full_mode']) is int and 0<=r['full_mode']<4096); seen.add(r['path'])
    need(seen==native)
fresh13(fresh); ck('synthetic exact13 baseline',True)
for k,v in [('schema','old_PASS'),('approved_by_root',1),('approved_by_root',False),('current_head','A'*40),('current_head','a'*39),('files',files[:-1]),('files',files+[files[0]]),('files',files[:-1]+[files[0]])]: bad('fresh13 mutation '+k+repr(v)[:80],lambda k=k,v=v:fresh13(dict(fresh,**{k:v})))
bad('fresh13 extra future approval key',lambda:fresh13(dict(fresh,future_merge_approved=True)))
for k in fresh: bad('fresh13 missing key '+k,lambda k=k:fresh13({n:v for n,v in fresh.items() if n!=k}))
for k,v in [('bytes',True),('full_mode',False),('path','foreign/path'),('sha256','z'*64)]: bad('fresh13 row mutation '+k,lambda k=k,v=v:fresh13(dict(fresh,files=[dict(files[0],**{k:v})]+files[1:])))
evidencekeys={'schema','operative_preparation_directory','approved_by_root','created_utc','notes','manifest','proof_notes','summary','raw_audit','source_adversary'}
ck('evidence general exact keys design',len(evidencekeys)==10)
for k in evidencekeys: ck('evidence missing rejects '+k,(evidencekeys-{k})!=evidencekeys)
ck('evidence extra future key rejects',evidencekeys|{'future_merge_approved'}!=evidencekeys)
queue=(P/'native4_proposal/preimage/unsolved_math_prioritization__QUEUE.md').read_bytes()
prospective=(P/'native4_proposal/prospective/unsolved_math_prioritization__QUEUE.md').read_bytes()
header=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
def patch_check(before,after):
    bs=before.splitlines(keepends=True); ass=after.splitlines(keepends=True); need(len(bs)==len(ass))
    need(sum(line.startswith(b'|') and [x.strip() for x in line.decode().split('|')[1:-1]]==header for line in bs)==1)
    hits=[i for i,l in enumerate(bs) if l.startswith(b'|') and len(l.decode().split('|'))==14 and l.decode().split('|')[2].strip()=='2849 / KP-3.51']; need(len(hits)==1); i=hits[0]
    old=bs[i].decode().split('|'); new=ass[i].decode().split('|'); need(len(new)==14 and old[8].strip()=='queued' and old[9].strip()=='0/5' and new[8].strip()=='unsolved' and new[9].strip()=='1/5')
    need(all(x==y for j,(x,y) in enumerate(zip(old,new)) if j not in {8,9,11}) and all(x==y for j,(x,y) in enumerate(zip(bs,ass)) if j!=i))
    return i,old,new
i,old,new=patch_check(queue,prospective); ck('dated proposal exactly selected Status Turns Findings',True)
for j in [1,2,3,4,5,6,7,10,12]:
    changed=list(new); changed[j]=' altered '; lines=prospective.splitlines(keepends=True); lines[i]='|'.join(changed).encode(); bad('protected queue cell '+str(j),lambda lines=lines:patch_check(queue,b''.join(lines)))
bad('duplicate target row rejected',lambda:patch_check(queue+queue.splitlines(keepends=True)[i],prospective+prospective.splitlines(keepends=True)[i]))
for n in ['unsolved_math_prioritization__state.json','unsolved_math_prioritization__history.jsonl','draft_pr_publication_program_20260930__inventory.json']:
    ck('dated native body unchanged '+n,(P/'native4_proposal/preimage'/n).read_bytes()==(P/'native4_proposal/prospective'/n).read_bytes())
builder=(P/'prepare_current_packet.py').read_text(); operator=(P/'capture_root_builder_operation.py').read_text()
ck('source confirms actual mandatory null branch',"for c in caps+summary['complete_actual_Git_captures']:" in builder and "if 'source' in c: checked(c['source']); need(c['source_unchanged'] is True" in builder)
ck('truthful incremental inner chronology',"(attempt/'GIT_COMMANDS.json').write_bytes(enc(commands))" in builder and "inner_GIT_COMMANDS_written_incrementally_while_builder_alive':True" in builder and "frozen_inner_copy_is_prepublication_prefix':True" in builder)
ck('outer writes final capture after child wait',operator.index("child.wait(timeout=600)")<operator.index("write(capture/'CAPTURE.json',rec)") and 'outer_operator_does_not_write_inner_GIT_COMMANDS=True' in operator)
ck('full frozen-file mode source checks',"stat.S_IMODE(p.stat().st_mode)==0o444" in builder and "(stage/'MANIFEST.json').chmod(0o444)" in builder)
ck('no optimized guards both sources',"not sys.flags.optimize" in builder and "not sys.flags.optimize" in operator)
ck('actual stage absent-only macOS primitive',"lib.renamex_np" in builder and "str(destination))" in builder and "publish_absent(stage,dest)" in builder)
out={'schema':'pr47-source-extended-private-controls/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'pid':os.getpid(),'assertions':len(checks),'checks':checks,'status':'COMPLETE_SOURCE_CONTROLS_MANDATORY_NULL_SOURCE_REPAIR','production_import_compile_execute':False,'mathematical_helpers_run':False,'synthetic_values_not_ROOT_approvals':True,'dated_native4_not_future_main_authority':True,'exact_verified_mandatory_locator':'prepare_current_packet.py:150','earlier_control_result_estimated_locator164_corrected_here':True,'future_current_acceptance_certified':False}
(F/'EXTENDED_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
