"""Bounded dated terminal accounting; no Git, services, compiler or math edits."""
from pathlib import Path
import datetime, difflib, hashlib, io, json, os, zipfile

R = Path(__file__).resolve().parent
A = R.parent.parent
P = A / 'preprint_v1_0'
K = P / 'kit'
PREFIX = 'historical/terminal_admin_20261016/'
SELECTED = [
    'reviews/package_02/REPORT.md',
    'reviews/package_02/INDEPENDENT_DERIVATION.md',
    'reviews/package_02/SOURCE_READ_LEDGER.json',
    'reviews/package_02/VERDICT.json',
    'reviews/package_02/OUTPUT_PINS.json',
    'reviews/package_02/SEAL.json',
    'ROOT_WHOLE_PACKAGE_REVIEW_02.json',
]
BEFORE_COPIES = ['preprint_v1_0/README.md', 'preprint_v1_0/kit/README.md',
                 'preprint_v1_0/kit/scripts/verify_kit.py']

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def need(ok, message):
    if not ok: raise ValueError(message)
def record(p, n):
    b=p.read_bytes(); return {'path':n,'bytes':len(b),'sha256':sha(b)}
def atomic(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    q=p.with_name(p.name+'.terminal-tmp')
    need(not q.exists(), 'temporary path exists')
    with q.open('xb') as f: f.write(b)
    os.replace(q,p)
def writej(p,d): atomic(p,(json.dumps(d,indent=2,sort_keys=True)+'\n').encode())

VERIFIER = '''import argparse
import json
import sys
sys.dont_write_bytecode=True
from safety import verify_payload, binding_check, require, load_json, member, record

def terminal_accounting():
    # Additive stage semantics only. Existing payload, binding, mathematical
    # and filesystem guards remain the unchanged safety.py contracts.
    t=load_json(member('TERMINAL_ACCOUNTING_20261016.json'))
    require(t['schema']==1 and t['pr']==1094 and
            t['head_oid']=='954dd70b49458026e29b8dae63243391249008d8' and
            t['original_submitted_files']==8, 'terminal identity')
    require(type(t['completed_new_whole_package_reviews']) is int and
            type(t['minimum_new_whole_package_reviews']) is int and
            t['completed_new_whole_package_reviews']==t['minimum_new_whole_package_reviews']==2
            and t['new_complete_whole_review_required'] is False,
            'terminal whole-review counts')
    for key in ('publication_ready','issues_resolved','published',
                'root_terminal_integrity_adopted','external_human_peer_review',
                'formal_proof_assistant_certification','final_readiness_seal_issued'):
        require(t[key] is False, 'terminal false flag: '+key)
    for key in ('root_terminal_integrity_required','root_whole02_adopted',
                'extensive_AI_assistance','unrefereed'):
        require(t[key] is True, 'terminal true flag: '+key)
    require(t['ordered_services_hold_pr']==1032 and t['service_actions_permitted'] is False,
            'terminal service hold')
    for key in ('full_result_priority','construction_method_priority','novelty',
                'worldwide_preexisting_openness'):
        require(t[key]=='UNKNOWN', 'terminal priority: '+key)
    require(t['mathematical_scope']==
            'All n>=1; globally smooth compactly supported real Nijenhuis tensor; prescribed numerical real Jordan matrix in a commuting smooth local frame on a nonempty open domain iff all spectrum is real; type, rank and eigenvalues may change outside; no fixed Cartesian matrix, global regularity or analytic compact support.',
            'terminal mathematical scope')
    require(t['stage']=='TERMINAL_ACCOUNTING_PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY' and
            t['not_another_whole_review'] is True, 'terminal pending stage')
    require(all(type(t['latest_whole_review'][k]) is int for k in ('number','P0','P1','P2','P3')) and
            t['latest_whole_review']=={'number':2,'complete':True,'repair_only':False,
                                    'P0':0,'P1':0,'P2':0,'P3':0},
            'terminal latest whole review')
    ledger=load_json(member('TERMINAL_SOURCE_COPY_LEDGER.json'))
    origins=[r['original_path'] for r in ledger['copies']]
    require(len(origins)==len(set(origins))==10, 'terminal copy ledger count')
    for r in ledger['copies']:
        require(record(member(r['copy_path']),r['original_path'])==
                {'path':r['original_path'],'bytes':r['bytes'],'sha256':r['sha256']},
                'terminal authored copy hash')
    by_origin={r['original_path']:r for r in ledger['copies']}
    require(set(t['evidence'])=={'report','derivation','source_ledger','verdict',
                               'output_pins','seal','root_adoption'},
            'terminal evidence roles')
    expected={'report':'reviews/package_02/REPORT.md',
              'derivation':'reviews/package_02/INDEPENDENT_DERIVATION.md',
              'source_ledger':'reviews/package_02/SOURCE_READ_LEDGER.json',
              'verdict':'reviews/package_02/VERDICT.json',
              'output_pins':'reviews/package_02/OUTPUT_PINS.json',
              'seal':'reviews/package_02/SEAL.json',
              'root_adoption':'ROOT_WHOLE_PACKAGE_REVIEW_02.json'}
    require(set(by_origin)==set(expected.values())|{'preprint_v1_0/README.md',
            'preprint_v1_0/kit/README.md','preprint_v1_0/kit/scripts/verify_kit.py'},
            'terminal exact selection origins')
    for role,origin in expected.items():
        require(t['evidence'][role]==by_origin[origin], 'terminal evidence locator: '+role)
    def evidence(role): return load_json(member(t['evidence'][role]['copy_path']))
    v=evidence('verdict'); s=evidence('seal'); root=evidence('root_adoption')
    pins=evidence('output_pins')
    for e in (v,s):
        require(e['pr']==1094 and e['head_oid']==t['head_oid'] and
                e['original_submitted_files']==8, 'terminal evidence identity')
    for key in ('full_result_priority','construction_method_priority','novelty',
                'worldwide_preexisting_openness'):
        require(v[key]=='UNKNOWN', 'terminal verdict priority')
    require(v['complete_whole_review'] is True and v['repair_only_review'] is False and
            v['actionable_findings']==[] and
            all(type(v[k]) is int and v[k]==0 for k in ('P0','P1','P2','P3')),
            'terminal verdict semantics')
    require(s['full_review'] is True and s['input_count']==388 and s['output_count']==27 and
            s['actionable_findings']==0 and all(s[k]==0 for k in ('P0','P1','P2','P3')),
            'terminal seal semantics')
    actual=record(member(t['evidence']['output_pins']['copy_path']),'OUTPUT_PINS.json')
    require(s['output_pins']==actual and root['output_pins_sha256']==actual['sha256'] and
            len(pins['records'])==27, 'terminal review seal hash binding')
    pinmap={r['path']:r for r in pins['records']}
    for role in ('report','derivation','source_ledger','verdict'):
        e=t['evidence'][role]; name=e['original_path'].split('/')[-1]
        require(pinmap[name]=={'path':name,'bytes':e['bytes'],'sha256':e['sha256']},
                'terminal selected review-output binding')
    require(root['status']=='ADOPT_COMPLETE_WHOLE02_ZERO_ACTIONABLE_PENDING_TERMINAL_ADMIN'
            and root['whole_reviews_completed']==root['minimum_whole_reviews']==2
            and root['actionable_P0_P1_P2_P3']==0
            and root['terminal_administrative_reconciliation_and_root_final_integrity_required'] is True,
            'terminal root adoption semantics')
    for e in (v,s,root):
        require(e['publication_ready'] is False and e['published'] is False,
                'terminal evidence readiness')
    require(v['ordered_services_hold_pr']==s['ordered_services_hold_pr']==root['services_held_after_pr']==1032,
            'terminal evidence service hold')
    require(root['full_result_and_method_priority_novelty_worldwide_openness']=='UNKNOWN',
            'terminal root priority')
    old=t['preserved_repair_status']
    require(record(member('CURRENT_STATUS.json'),'CURRENT_STATUS.json')==old,
            'terminal captured repair status binding')
    dated=load_json(member('CURRENT_STATUS.json'))
    require(dated['completed_new_whole_package_reviews']==1 and
            dated['new_complete_whole_review_required'] is True,
            'terminal dated repair status')
    require(ledger['prior_partitions_unchanged']==[171,309] and
            ledger['no_omitted_code_replay_claim'] is True,
            'terminal historical partition semantics')
    return {'status':'PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY',
            'completed_whole_reviews':2,'minimum_whole_reviews':2,
            'publication_ready':False,'issues_resolved':False,'published':False,
            'ordered_services_hold_pr':1032}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--binding');parser.add_argument('--require-binding',action='store_true');args=parser.parse_args()
    data=verify_payload()
    terminal=terminal_accounting()
    print(json.dumps({'status':'PASS','payload_files':len(data['records']),
                      'terminal_accounting':terminal,
                      'binding':binding_check(args.binding,args.require_binding)},sort_keys=True))
if __name__=='__main__': main()
'''

def main():
    frozen=json.loads((R/'FROZEN_INPUT_PINS.json').read_text())['records']
    allowed=[r['path'] for r in json.loads((R/'ALLOWED_CHANGES.json').read_text())['existing_edits']]
    for row in frozen:
        need(record(A/row['path'],row['path'])==row,'input changed before mutation: '+row['path'])
    copies=[]
    for n in SELECTED+BEFORE_COPIES:
        before=n in BEFORE_COPIES
        src=R/'before'/n if before else A/n
        dst=PREFIX+('before/' if before else '')+n
        atomic(K/dst,src.read_bytes())
        q=record(src,n)
        copies.append({'original_path':n,'copy_path':dst,'bytes':q['bytes'],'sha256':q['sha256'],
                       'meaning':'Exact before-terminal interface bytes' if before else 'Exact authored whole02/root evidence; dated history'})
    ledger={'schema':1,'utc':now(),'scope':'Append-only terminal selection; neither the 171-input preparation partition nor the 309-input repair partition is modified or recounted.',
            'prior_partitions_unchanged':[171,309],'copies':copies,
            'no_omitted_code_replay_claim':True,
            'excluded_categories':['raw compiler/command streams','third-party bodies/text/pixels','compiler/runtime/cache','old ZIP','current delivery bindings'],
            'changed_interfaces_retained_locally_only':[{'original_path':n, 'before_locator':'finalization/terminal_admin_20261016/before/'+n, **{k:record(R/'before'/n,n)[k] for k in ('bytes','sha256')}, 'reason':'Archive/binding/manifest dependency; exact local before bytes retained, not redistributed or treated as current inventory.'} for n in allowed if n not in BEFORE_COPIES]}
    writej(K/'TERMINAL_SOURCE_COPY_LEDGER.json',ledger)
    evidence=dict(zip(('report','derivation','source_ledger','verdict','output_pins','seal','root_adoption'),copies[:7]))
    terminal={'schema':1,'utc':now(),'pr':1094,'head_oid':'954dd70b49458026e29b8dae63243391249008d8','original_submitted_files':8,
              'stage':'TERMINAL_ACCOUNTING_PENDING_EXTERNAL_ROOT_FINAL_INTEGRITY',
              'completed_new_whole_package_reviews':2,'minimum_new_whole_package_reviews':2,
              'new_complete_whole_review_required':False,'root_whole02_adopted':True,
              'latest_whole_review':{'number':2,'complete':True,'repair_only':False,'P0':0,'P1':0,'P2':0,'P3':0},
              'root_terminal_integrity_required':True,'root_terminal_integrity_adopted':False,
              'publication_ready':False,'issues_resolved':False,'published':False,
              'final_readiness_seal_issued':False,'ordered_services_hold_pr':1032,
              'service_actions_permitted':False,'full_result_priority':'UNKNOWN',
              'construction_method_priority':'UNKNOWN','novelty':'UNKNOWN',
              'worldwide_preexisting_openness':'UNKNOWN','external_human_peer_review':False,
              'formal_proof_assistant_certification':False,'extensive_AI_assistance':True,
              'unrefereed':True,'not_another_whole_review':True,
              'mathematical_scope':'All n>=1; globally smooth compactly supported real Nijenhuis tensor; prescribed numerical real Jordan matrix in a commuting smooth local frame on a nonempty open domain iff all spectrum is real; type, rank and eigenvalues may change outside; no fixed Cartesian matrix, global regularity or analytic compact support.',
              'evidence':evidence,'preserved_repair_status':record(K/'CURRENT_STATUS.json','CURRENT_STATUS.json'),
              'history_rule':'CURRENT_STATUS.json and every previous report, pin, seal, root adoption and native 15 October observation remain exact dated captured-stage evidence. This separate later record supplies current pending-root accounting.'}
    writej(P/'TERMINAL_ACCOUNTING_20261016.json',terminal)
    atomic(K/'TERMINAL_ACCOUNTING_20261016.json',(P/'TERMINAL_ACCOUNTING_20261016.json').read_bytes())
    atomic(K/'scripts/verify_kit.py',VERIFIER.encode())
    outer=(R/'before/preprint_v1_0/README.md').read_text()
    start=outer.index('This candidate is **not publication-ready yet**.')
    end=outer.index('\nThe bounded repair report',start)
    outer=outer[:start]+'''Current accounting is dated 16 October 2026 UTC in
`TERMINAL_ACCOUNTING_20261016.json` and the identical kit record. Two new
complete independent whole-package reviews have finished, meeting the
minimum of two. Review01's P3 was repaired and root-adopted; the NEW complete
review02 has zero actionable P0–P3 findings and root adopted it. No further
whole review is currently required. External ROOT terminal integrity
adoption remains required and has not occurred; publication_ready,
issues_resolved and published remain false. This administrative checkpoint
is not another review or a final readiness grant. All external services
remain held after #1032.

The original preparation's zero-review state and the bounded repair's
one-review/new-review-required state remain exact dated history in all old
pins, reports, seals and `kit/CURRENT_STATUS.json`. They do not describe the
later terminal count. `kit/TERMINAL_SOURCE_COPY_LEDGER.json` adds only selected
exact authored whole02/root evidence and before-interface copies; both
previous custody partitions remain exact. The portable verifier now checks
the separate terminal count, evidence hashes, conservative scope and pending
ROOT/false-publication semantics. Historical reviewer programs are omitted
and no portable replay of their environments is claimed.
''' + outer[end:]
    atomic(P/'README.md',outer.encode())
    text=(R/'before/preprint_v1_0/kit/README.md').read_text()
    text=text.replace('They do not override `CURRENT_STATUS.json` or claim that new whole-package reviews are complete.',
       'They retain their own dated meaning. The unchanged `CURRENT_STATUS.json` is the captured repair-stage status; the later `TERMINAL_ACCOUNTING_20261016.json` supplies current pending-ROOT accounting.')
    text=text.replace('## Current repair checkpoint (16 October 2026 UTC)','## Captured repair checkpoint (16 October 2026 UTC; superseded accounting)')
    text=text.replace('A NEW complete independent whole-package review is\nstill required, with a minimum of two total new complete reviews and all\nactionable findings resolved.',
       'At that captured checkpoint a NEW complete independent whole-package\nreview was still required, with a minimum of two total new complete reviews\nand all actionable findings resolved.')
    text += '''
## Terminal accounting (16 October 2026 UTC; pending external ROOT integrity)

Two new complete independent whole-package reviews have finished, meeting
the minimum of two. The first review's P3 was repaired and root-adopted.
The NEW complete review02 found zero actionable P0–P3 issues, and root adopted
that whole review. No further whole review is currently required. The
separate `TERMINAL_ACCOUNTING_20261016.json` binds the exact selected report,
derivation, source-read ledger, verdict, output pins, seal and root adoption.
`TERMINAL_SOURCE_COPY_LEDGER.json` appends their individual exact locators
and the changed prose/verifier's before bytes without changing either old
171/309-input custody partition. Old ZIP/bindings and raw streams are omitted
from this new selection. `scripts/verify_kit.py` adds explicit checks of this
terminal accounting and its evidence; all old payload/path/math guards remain
unchanged. Reviewer programs are dated external evidence, omitted here and
not promised as portable replay environments.

External ROOT terminal integrity adoption is required and has not occurred.
publication_ready, issues_resolved and published remain false. This dated
administrative reconciliation supplies neither another whole review nor a
final readiness grant. Priority, novelty and worldwide prior openness remain
UNKNOWN; extensive AI assistance, unrefereed status and absence of external
human peer review or proof-assistant certification remain in force. All
external services remain held after PR #1032.
'''
    atomic(K/'README.md',text.encode())
    manifest={'schema':1,'hash_scope':'Every regular kit file except this root manifest; historical manifests retain captured-stage meaning.',
              'records':[record(p,p.relative_to(K).as_posix()) for p in sorted(K.rglob('*')) if p.is_file() and p!=K/'MANIFEST.json']}
    writej(K/'MANIFEST.json',manifest)
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as archive:
        for n in sorted(['MANIFEST.json']+[r['path'] for r in manifest['records']]):
            info=zipfile.ZipInfo(n,(1980,1,1,0,0,0));info.create_system=3
            info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_STORED
            archive.writestr(info,(K/n).read_bytes())
    atomic(P/'pr1094_supportkit_v1.0.zip',buf.getvalue())
    binding=json.loads((R/'before/preprint_v1_0/DEPOSIT_BINDING.json').read_text())
    binding['files']=[record(P/n,n) for n in ('paper.pdf','pr1094_supportkit_v1.0.zip')]
    writej(P/'DEPOSIT_BINDING.json',binding)
    edits=[]
    for row in frozen:
        n=row['path'];current=record(A/n,n)
        if current!=row:
            need(n in allowed,'unauthorized old input mutation: '+n)
            need(record(R/'before'/n,n)==row,'before bytes differ')
            edits.append({'path':n,'before':row,'current':current,'exact_before_locator':'before/'+n})
    need(len(edits)==6,'incorrect allowed edit count')
    writej(R/'INPUT_PRESERVATION.json',{'utc':now(),'baseline_count':len(frozen),'allowed_existing_edits':edits,'protected_unchanged_count':len(frozen)-6,'all_protected_inputs_rehashed':True,'old_CURRENT_STATUS_all_guards_math_TeX_PDF_native_metadata_unchanged':True})
    parts=[]
    for n in allowed+['preprint_v1_0/TERMINAL_ACCOUNTING_20261016.json','preprint_v1_0/kit/TERMINAL_ACCOUNTING_20261016.json','preprint_v1_0/kit/TERMINAL_SOURCE_COPY_LEDGER.json']:
        if n.endswith('.zip'):continue
        before=(R/'before'/n).read_text().splitlines(keepends=True) if n in allowed else []
        after=(A/n).read_text().splitlines(keepends=True)
        parts.extend(difflib.unified_diff(before,after,fromfile='before/'+n if n in allowed else '/dev/null',tofile='current/'+n))
    atomic(R/'COMPLETE_CODE_PROSE_DIFF.patch',''.join(parts).encode())
    writej(R/'SOURCE_COPY_SELECTION.json',ledger)
    print(json.dumps({'status':'TERMINAL_ACCOUNTING_BUILT_PENDING_VALIDATION','baseline':len(frozen),'edits':len(edits),'selected_authored_copies':len(copies),'kit_members':len(manifest['records'])+1,'zip':record(P/'pr1094_supportkit_v1.0.zip','pr1094_supportkit_v1.0.zip')},indent=2))

if __name__=='__main__':main()
