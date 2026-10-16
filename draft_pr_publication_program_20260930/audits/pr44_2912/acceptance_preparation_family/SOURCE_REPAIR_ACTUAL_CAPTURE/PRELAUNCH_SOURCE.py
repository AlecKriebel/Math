"""Own adjacent source repair; preserves all initially generated snippets. Never executes production."""
from pathlib import Path
import datetime as dt
import difflib
import hashlib
import json
import os
import re

H=Path(__file__).resolve().parent;A=H.parent;R=H.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def dump(p,o):p.write_text(json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
def main():
    archive=H/'INITIAL_GENERATED_SOURCE';archive.mkdir(exist_ok=False)
    names=['pr44_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','EXPECTED_ROOT_WHOLE_REVIEW.json','INPUT_BINDINGS.json']
    before={n:(H/n).read_bytes() for n in names}
    for n,b in before.items():(archive/n).write_bytes(b)
    g=(H/'pr44_guards.py').read_text()
    old="'PR44_STRICT_CURRENT_PACKET_v1':{'schema','self_excluded','files_count','files','current_gate','prior_standard_partial','full_problem_solved_by_project','novelty_claimed','original_substantive_attempts','new_substantive_attempts','audit_turns'},"
    new="'PR44_STRICT_CURRENT_PACKET_v1':{'schema','self_excluded','files_count','files','current_gate','status','full_problem_solved','novelty_claimed','original_substantive_attempts','new_substantive_attempts','audit_turns','full_permission_mode'},"
    if old not in g:raise ValueError('Initial exact known-schema literal missing')
    g=g.replace(old,new)
    g=g.replace("require(len(names)==964 and NATIVE<=names and historical_checked==historical,'Exact identities/native13/historical4')", """require(len(names)==964 and (NATIVE-historical)<=names and not historical.intersection(names),'Exact964 foreign identities and nine stable native inputs')
    for n in sorted(historical):
        z=dated_native[n]
        entries=git_bytes('ls-tree','-z',dated_head,'--',n).decode().split('\\0')
        require(len(entries)==2 and entries[-1]=='','Exactly one independent frozen Git blob')
        fields,literal=entries[0].split('\\t');mode,kind,blob=fields.split()
        require(mode=='100644' and kind=='blob' and literal==n,'Frozen native4 exact immutable Git modes')
        raw=git_bytes('show',dated_head+':'+n)
        require(len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Entire independent frozen native4 body differs')
        historical_checked.add(n)
    require(historical_checked==historical,'All four independently rechecked frozen native bodies')""")
    g=g.replace("'schema':'pr44-accepted-qualified-standard-partial-partial/v1'", "'schema':'pr44-accepted-qualified-standard-partial/v1'")
    # Clock binds the real complete ROOT record; no newly authored claim is invented.
    anchor="    ledger=load(A/'ROOT_PRIMARY_READ_LEDGER.json');card=load(A/'ROOT_SCIENCE_CARD.json');"
    g=g.replace(anchor,"    require(utc_clock(root['created_utc'],'ROOT whole inspection')<=utc_clock(approved['created_utc'],'ROOT acceptance approval'),'Completed whole inspection must precede ROOT approval')\n"+anchor)
    strict_direct="""    require(root.get('direct_four_independent_ROOT_Git_checks_completed') is True and type(root.get('actual_direct_four_operator_pid')) is int and root['actual_direct_four_operator_pid']>0,'Genuine direct ROOT native4 operation')
    commands=root['complete_dated_git_captures'];require(type(commands) is list and len(commands)==8,'Exact eight genuine direct ROOT Git captures')
    expected=[]
    for n in sorted(historical):expected.extend([['git','ls-tree',dated_head,'--',n],['git','show',dated_head+':'+n]])
    require(equal([z['argv'] for z in commands],expected),'Exact entire direct ROOT native4 argv sequence')
    for i,z in enumerate(commands):
        required(z,{'cwd':str(R),'operator_pid':root['actual_direct_four_operator_pid'],'stdin_supplied':False,'exit_code':0,'actual_execution':True,'completed':True},'Genuine complete direct Git query')
        require(type(z['pid']) is int and z['pid']>0 and utc_clock(z['started_utc'],'Git start')<=utc_clock(z['finished_utc'],'Git finish')<=utc_clock(root['created_utc'],'Root read completion'),'Actual Git PID/time')
        for channel in ['stdout','stderr']:exact_reference(z[channel]);check(R,[z[channel]])
        require(regular(R,z['stderr']['path']).read_bytes()==b'','Complete direct Git stderr')
        n=sorted(historical)[i//2];raw=regular(R,z['stdout']['path']).read_bytes()
        if i%2:
            require(len(raw)==dated_native[n]['bytes'] and sha(raw)==dated_native[n]['sha256'],'Entire direct show stdout equals frozen native body')
        else:
            require(raw.endswith(b'\\n') and raw.count(b'\\n')==1,'One literal direct ls-tree line')
            fields,literal=raw.decode().rstrip('\\n').split('\\t');mode,kind,blob=fields.split()
            require(mode=='100644' and kind=='blob' and literal==n,'Exact direct100644 path/mode')
"""
    g=g.replace("    require(utc_clock(root['created_utc'],'ROOT whole inspection')",strict_direct+"    require(utc_clock(root['created_utc'],'ROOT whole inspection')")
    g=g.replace("Actual32 prior primaries", "Actual33 prior primaries").replace("Exactly33 derived primary completions", "Exactly34 derived primary completions")
    (H/'pr44_guards.py').write_text(g)
    i=(H/'integrate_reviewed_partial.py').read_text()
    # A regex replacement interpreted escapes in generated repr literals. Rebuild
    # complete assignments by direct slicing, retaining the bad initial bodies.
    body='Accept PR44 / 2912 / Kirby4.36 as an UNSOLVED repository report of standard conditional deductions. The finite-support meridional restriction kernel, sufficient relative-degree-one pair-map criterion and conditional integral R^C/R^A for the specified abstract group-pair are valid scoped partials. Neither a degree-one meridian-compatible pair map from the unmarked full(G,pi2module,k) nor two actual smooth/locally flat PL S2-in-S4 exteriors with equal full triples and different homotopy types is realized. Both gaps remain explicit. Original18 and twelve immutable science/helper/result/source/ledger bodies are unchanged; original2/5,new0,audit0. The NEW whole-current source-first audit and genuine ROOT full reading/final reconciliation are separately bound. Global source/category/integral/history qualifications remain operative, including finite checks not proving realization/classification and absent raw prior versus SQL fallback{}. Current model/reasoning/deadline are null. No novelty, project solution, full prior-literature resolution, exhaustive priority, human peer review, paper, new DOI, tracker or release is claimed. One present acceptance event follows the exact original-head no-ff merge, preserves every prior state and the full history prefix, and consumes only the original two turns.\n'
    present='The NEW whole-current source-first audit has passed for this scoped UNSOLVED standard partial; actual completed acceptance is bound in acceptance.json. SOURCE_PRECISION_QUALIFICATIONS.md and CURRENT_OBSTRUCTION_CONTEXT.md apply globally to OBSTRUCTION.md, every presentation and metadata file. The unmarked full triple supplies no boundary/meridian marking or degree-one pair map; no actual allowed-category equal-full-triple exterior pair is realized. The integral quotient is conditional on the specified abstract group-pair, and augmentation-lattice substitution is invalid. Original18 archive and twelve immutable bodies remain exact. Earlier PENDING/source-only/PASS/runtime/search/access/model statements in the frozen current packet and original archives remain dated attributions at or before its frozen publication; later actual acceptance records alone describe the present disposition. Raw prior absence and SQL fallback{} remain distinct. Original2/5,new0,audit0; current runtime fields null; no novelty, human referee, paper/new DOI/tracker/release.\n'
    start=i.index('BODY = ');end=i.index('\ndef queue_after(')
    i=i[:start]+'BODY = '+repr(body)+'\nPRESENT_SCOPE = '+repr(present)+'\n'+i[end:]
    i=i.replace('Require postPR43 native33targets/41turns','Require postPR43 native34targets/41turns').replace('Require32 complete primaries before43','Require33 complete primaries before44')
    i=i.replace('Program33/180=18.3333%','Program34/180=18.8889%')
    (H/'integrate_reviewed_partial.py').write_text(i)
    m=(H/'state_mirror_reconciliation.py').read_text().replace('Exactly33 primary completions','Exactly34 primary completions').replace('Require33targets/41turns','Require34targets/41turns').replace('Exactly34targets/41turns/33primary','Exactly35targets/43turns/34primary').replace('Exact empty-ledger guard','Exact two-turn-ledger guard').replace('original2/5 empty ledger','original2/5 exact two-turn ledger')
    (H/'state_mirror_reconciliation.py').write_text(m)
    p=(H/'verify_post_acceptance.py').read_text().replace('original2/5 empty ledger','original2/5 exact two-turn ledger').replace('exact_original18_and_SOURCE_STATUS_unchanged','exact_original18_and_OBSTRUCTION_unchanged').replace("'full_target_resolved_in_prior_published_literature':True,'prior_publication_doi':'10.4064/sm210413-18-9'", "'full_target_resolved_in_prior_published_literature':False,'prior_publication_doi':None")
    (H/'verify_post_acceptance.py').write_text(p)
    actual=(A/'ROOT_WHOLE_CURRENT_REVIEW.json').read_bytes();actual_object=json.loads(actual)
    if not actual_object['complete_dated_git_captures'] or len(actual_object['complete_dated_git_captures'])!=8 or actual_object.get('direct_four_independent_ROOT_Git_checks_completed') is not True:raise ValueError('Genuine corrected ROOT eight complete captures required; initial [] is preserved')
    if actual_object['candidate_manifest_sha256']!='169f2825a8f730735627bdc33a43366c05e317fdf7ec4df4cd96a31e37329eb0':raise ValueError('ROOT record candidate pin changed')
    (H/'EXPECTED_ROOT_WHOLE_REVIEW.json').write_bytes(actual)
    inputs=json.loads((H/'INPUT_BINDINGS.json').read_bytes());inputs['closed_root_whole_inspection']=pin(A/'ROOT_WHOLE_CURRENT_REVIEW.json')
    for p in sorted((A/'root_complete_dated_four_actual_capture').iterdir()):inputs['pins']['root_corrected_whole_'+p.name]=pin(p)
    for p in sorted((A/'root_complete_dated_four_actual_Git').rglob('*')):
        if p.is_file():inputs['pins']['root_direct_Git_'+p.relative_to(A/'root_complete_dated_four_actual_Git').as_posix()]=pin(p)
    inputs['pins']['root_direct_four_source']=pin(A/'complete_dated_four_ROOT_Git_inspection.py')
    # Preserve original external ROOT inspection body separately in ROOT-owned
    # evidence; bind that exact archived record when supplied by the genuine ROOT.
    oldroot=A/'ROOT_WHOLE_CURRENT_REVIEW_V2_BEFORE_DIRECT_FOUR.json'
    if not oldroot.is_file():raise ValueError('ROOT original inspection must be preserved at agreed literal path')
    inputs['pins']['root_whole_initial_inspection']=pin(oldroot)
    dump(H/'INPUT_BINDINGS.json',inputs)
    delta=[]
    for n in names:
        after=(H/n).read_bytes()
        delta.extend(difflib.unified_diff(before[n].decode().splitlines(keepends=True),after.decode().splitlines(keepends=True),fromfile='INITIAL_GENERATED_SOURCE/'+n,tofile=n))
    (H/'SOURCE_REPAIR_DELTA.patch').write_text(''.join(delta))
    dump(H/'SOURCE_REPAIR_RESULT.json',{'schema':'pr44-owned-source-repair/v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_author_pid':os.getpid(),'initial_generated_members_retained':sorted(names),'initial_authoring_capture_preserved':True,'repairs':['Literal BODY/PRESENT source strings preserve escapes by slicing','Exact PR44 current-manifest schema includes status/full_problem_solved/full_permission_mode','Actual964 individual foreign inventory has stable native9; frozen native4 separately queried immutably','Remove inherited PR43 prior-resolution/DOI fields from PR44 post','Use corrected genuinely captured ROOT whole native4 record and preserve original refs','Accurate two-turn/count/percentage prose'], 'production_imported_compiled_executed':False,'candidate_changed':False,'ROOT_approval_claimed':False})
    with (H/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+dt.datetime.now(dt.timezone.utc).isoformat()+' — Source-repair checkpoint. Completion100% source/0% acceptance/0% discovery. Initially generated snippets retained; repaired lexical source literals, exact manifest schema, independent dated native4 contract and stale scientific DOI. ROOT corrected its own four-capture inspection separately; no packet, scientific or shared state changed.\n')
    print(json.dumps({'status':'SOURCE_REPAIRED','actual_author_pid':os.getpid(),'production_executed':False,'ROOT_whole_sha256':sha(actual),'initial_members_preserved':len(names)},sort_keys=True))
if __name__=='__main__':main()
