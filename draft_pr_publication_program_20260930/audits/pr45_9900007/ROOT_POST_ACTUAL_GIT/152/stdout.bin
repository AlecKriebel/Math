"""Author a PR45 SOURCE-only builder by fully disclosed exact adaptations of PR44."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat
F=Path(__file__).resolve().parent; A=F.parent; R=A.parents[2]
T=R/'draft_pr_publication_program_20260930/audits/pr44_2912/current_preparation_family'
HEAD='d9b4acf5d070d1f04ffac86a4f08916a5629ff16'
BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
MERGE='01358d66fc67d1c462bddf31c0d4ee5b120e6737'
FLAGS=['original18_science_helpers_results_metadata_and_complete19_path_diff_fully_read',
 'operative_primary_target_and_scoped_prior_work_comparisons_fully_read',
 'arbitrary_fixed_coupling_metric_and_tight_offset_proof_accepted',
 'whole_raw_SQL_and_prior_presence_actual_evidence_fully_read',
 'unchanged_author885_and_independent3044_actual_reproductions_fully_read',
 'both_closed_independent_families_fully_read',
 'first_party_closures_and_individual_foreign_exclusions_mechanically_checked',
 'unsolved_illustrative_obstruction_only_no_novelty_scope_accepted',
 'new_source_adversary_closed_clean_complete_report_personally_read']
def sha(b): return hashlib.sha256(b).hexdigest()
def write(name,b):
    if isinstance(b,str): b=b.encode()
    assert len(b)<100*1024*1024
    with (F/name).open('xb') as f: f.write(b); f.flush(); os.fsync(f.fileno())
def js(name,o): write(name,json.dumps(o,indent=2,sort_keys=True,allow_nan=False)+'\n')
def pin(p):
    b=p.read_bytes(); return {'path':p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b)}
def replace(s,old,new):
    assert s.count(old)==1, (old[:120],s.count(old)); return s.replace(old,new)
def block(s,start,end,new):
    assert s.count(start)==s.count(end)==1
    i=s.index(start); j=s.index(end,i); return s[:i]+new+s[j:]

def main():
    write('AUTHOR_PRELAUNCH_SOURCE.py',Path(__file__).read_bytes())
    old=(T/'prepare_current_packet.py').read_text(); oldop=(T/'capture_root_builder_operation.py').read_text()
    write('READ_PR44_ADMINISTRATIVE_BUILDER_BASIS.py',old); write('READ_PR44_ADMINISTRATIVE_OPERATOR_BASIS.py',oldop)
    s=old.replace('PR44','PR45').replace('pr44','pr45').replace('pr45_2912','pr45_9900007')
    s=replace(s,"HEAD = 'c772dc5b851ec91da9d46d534577609e5d3ca389'","HEAD = '"+HEAD+"'")
    s=replace(s,"BASE = '01358d66fc67d1c462bddf31c0d4ee5b120e6737'","BASE = '"+BASE+"'\nMERGE_BASE = '"+MERGE+"'")
    s=replace(s,"SCIENCE = '69a3ffb7b6c2ba3bf1a4df8d7d83960d66095db9d175d78cfe49e2324aac1a71'","SCIENCE = '7123c345d3ecdf4fecb8941596687da54c44e169831eb23177ea485fa8386722'")
    s=block(s,'FLAGS = [','HEADER = ', 'FLAGS = '+repr(FLAGS)+'\n')
    s=block(s,'IMMUTABLE = [','\ndef require(',"IMMUTABLE = ['PARTIAL.md','SOURCES.md','binary_verification.json','source_manifest.json','source_record.json','turns.jsonl','verify_binary_process.py','review/verify_binary_process.py','review/submitted_results.json','review/PARTIAL.md','review/independent_checks.py','review/independent_results.json']\n")
    s=block(s,"    snapshot_raw = checked(pins['snapshot_manifest']", "    for row in pins['auxiliary']:", '''    snapshot_raw = checked(pins['snapshot_manifest'], 'original18_snapshot')
    snapshot = load(snapshot_raw)
    require(snapshot['schema'] == 'pr45-original-source-snapshot/v1' and
            snapshot['head'] == HEAD and snapshot['github_base'] == BASE and
            snapshot['merge_base'] == MERGE_BASE and snapshot['original_files'] == 18 and
            len(snapshot['files']) == 18, 'Exact original18 and distinct bases required')
    original = {}
    for row in snapshot['files']:
        name = relative(row['relative_path'])
        require(name not in original and type(row['bytes']) is int and row['bytes'] >= 0 and
                hex64(row['sha256']) and row['git_mode'] == '100644' and row['snapshot_mode'] == '0444' and
                type(row['git_object']) is str and re.fullmatch('[0-9a-f]{40}', row['git_object']),
                'Typed unique original Git body required')
        raw = bind('source_snapshot/' + name, 'immutable_original18', row['sha256'])
        require(len(raw) == row['bytes'] and stat.S_IMODE((audit/'source_snapshot'/name).stat().st_mode) == 0o444,
                'Original full bytes/mode changed')
        native = 'unsolved_math_prioritization/attempts/9900007/' + name
        require(row['path'] == native and git('show', HEAD + ':' + native) == raw,
                'Original Git/path body differs')
        require(git('ls-tree', HEAD, '--', native).decode().strip() ==
                '100644 blob ' + row['git_object'] + '\\t' + native, 'Original mode/blob differs')
        original[name] = raw
    require(inventory(audit/'source_snapshot') == set(original) and sha(original['PARTIAL.md']) == SCIENCE,
            'Complete original science required')
    tree = git('ls-tree', '-r', '-z', HEAD, '--', 'unsolved_math_prioritization/attempts/9900007/').decode().split('\\0')
    require({entry.split('\\t',1)[1] for entry in tree if entry} ==
            {'unsolved_math_prioritization/attempts/9900007/'+name for name in original}, 'Complete original Git tree required')
    metadata = load(checked(pins['original_metadata'], 'original_distinct_base_and_diff_metadata'))
    require(metadata['head'] == HEAD and metadata['github_base'] == BASE and metadata['merge_base'] == MERGE_BASE and
            metadata['changed_files'] == 19 and git('rev-parse', BASE) == (BASE+'\\n').encode(), 'Actual distinct original bases required')
    diff = checked(metadata['full_diff'], 'whole_original19_path_diff')
    require(len(diff) == 183402 and sha(diff) == 'e35d109f694c8abb0a83c3b5604ede674a14d33025ae124340d4102829c3e6ba' and
            git('diff','--no-ext-diff','--no-textconv','--binary',MERGE_BASE,HEAD,'--') == diff and
            git('diff','--name-only',MERGE_BASE,HEAD).decode().splitlines() == [r['path'] for r in metadata['all_changed_paths']],
            'Whole original19-path diff and merge-base binding required')
    ledger = [load(line) for line in original['turns.jsonl'].splitlines()]
    require(len(ledger) == 1 and type(ledger[0]['turn']) is int and ledger[0]['turn'] == 1 and
            ledger[0]['outcome'] == 'partial', 'Exact original one-turn partial ledger required')
    require(original['verify_binary_process.py'] == original['review/verify_binary_process.py'] and
            original['binary_verification.json'] == original['review/submitted_results.json'] and
            original['PARTIAL.md'] == original['review/PARTIAL.md'], 'Original duplicate bindings differ')
    saved, independent = load(original['binary_verification.json']), load(original['review/independent_results.json'])
    require(saved['status'] == 'PASS' and type(saved['exact_assertions']) is int and saved['exact_assertions'] == 885 and
            type(independent['passed']) is int and independent['passed'] == 3044 and independent['failed'] == 0 and
            type(independent['checks']) is dict and len(independent['checks']) == 3044 and
            all(value == 'PASS' for value in independent['checks'].values()) and independent['reviewed_sha256'] == SCIENCE,
            'Whole saved receipts only; fresh ROOT reproduction still required')
''')
    s=s.replace("{'duality_algebra_family', 'literal_realization_family'}","{'probability_metric_family', 'literal_priority_family'}")
    s=replace(s,"        require(directories == set(info['directories']), 'Independent family directory topology changed')", "        require(directories == set(info['directories']) and all(stat.S_IMODE((audit/family/name).stat().st_mode) == mode for name,mode in info['directory_modes'].items()), 'Independent family directory topology/modes changed')")
    s=block(s,"    dual = load(bind(","    future = {}",'''    probability = load(bind('probability_metric_family/VERDICT.json','scoped_probability_verdict'))
    literal = load(bind('literal_priority_family/VERDICT.json','scoped_literal_verdict'))
    require(probability['mathematical_determination'] == 'original_partial_claim_valid_with_stated_boundaries' and
            probability['mandatory_mathematical_corrections'] == [] and probability['full_target_characterization_resolved'] is False and
            probability['historical_novelty_certified'] is False and literal['verdict'] == 'PASS_SCOPED_PARTIAL_OBSTRUCTION' and
            literal['mandatory_mathematical_corrections'] == [] and literal['full_source_solved'] is False and
            literal['historical_novelty'] == 'unestablished', 'Scoped UNSOLVED reports only; no full solution or novelty')

''')
    s=s.replace("('original_substantive_attempts', 2)","('original_substantive_attempts', 1)")
    s=s.replace('finite_checks_do_not_prove_geometric_realization_or_full_problem','finite_checks_do_not_prove_universal_coupling_or_full_problem')
    s=s.replace('# ROOT PR45 scoped standard-partial acceptance','# ROOT PR45 scoped synchronous-obstruction acceptance')
    s=s.replace('ROOT_SCOPE_ACCEPTED_STANDARD_PARTIAL_ONLY','ROOT_SCOPE_ACCEPTED_SYNCHRONOUS_OBSTRUCTION_ONLY')
    s=s.replace('PR45 / 2912 / KP-4.36','PR45 / 9900007 / AMR-098-0007')
    s=s.replace('Original turns: 2/5; new: 0; audit: 0','Original turns: 1/5; new: 0; audit: 0')
    s=replace(s,"for literal in ['PR45 / 9900007 / AMR-098-0007', HEAD, BASE, 'Status: unsolved',", "for literal in ['PR45 / 9900007 / AMR-098-0007', HEAD, BASE, MERGE_BASE, 'Status: unsolved',")
    s=s.replace("'2912 / KP-4.36'","'9900007 / AMR-098-0007'")
    s=block(s,"    finding = (","    for name, value in [('Status'",'''    finding = ('Verified original synchronous-coupling obstruction: weak shifted laws but mismatch tends to1/2 under every fixed joining; '
               'stated metric law and tight nonnegative-offset scope retained. Broader two-process characterization unresolved. '
               'UNSOLVED original1/5,new0,audit0; no novelty/paper/new DOI/tracker. Current Asmussen primary access qualified; NEW whole-current review PENDING.')
''')
    s=s.replace("('Turns', '2/5')","('Turns', '1/5')")
    s=s.replace("original['OBSTRUCTION.md']","original['PARTIAL.md']").replace('CURRENT_OBSTRUCTION_CONTEXT.md','CURRENT_PARTIAL_CONTEXT.md')
    s=s.replace("'id': 2912, 'problem_number': 'KP-4.36'","'id': 9900007, 'problem_number': 'AMR-098-0007'")
    s=s.replace("'original_substantive_attempts': 2","'original_substantive_attempts': 1")
    s=block(s,"        'exact_remaining_scientific_gaps': [","        'exact_remaining_publication_gap':",'''        'exact_remaining_scientific_gaps': ['No alternative general two-process characterization has been given or excluded',
            'Exhaustive historical priority and full published-original source comparison remain unestablished'],
''')
    s=s.replace('actual_now_author507_and_old_independent29933_entire_results_byte_exact','actual_now_author885_and_old_independent3044_entire_results_byte_exact')
    s=s.replace('finite_checks_are_not_duality_group_cohomology_geometric_realization_or_full_problem_proof','finite_checks_do_not_prove_arbitrary_infinite_couplings_or_full_problem')
    s=s.replace("'original_V1_failed_filename_guess_retained_V2_operative': True,","'genuine_original_export_queue_selector_failure_retained_separate_repair': True,\n        'current_Asmussen_primary_access_comparison_retained_historical_access_bytes_unchanged': True,")
    s=s.replace('all_source_proof_and_geometric_qualifications_apply_globally','all_source_proof_metric_offset_and_access_qualifications_apply_globally')
    s=s.replace("'id': 2912,","'id': 9900007,")
    s=s.replace('Scoped standard partial deductions accepted by genuine ROOT reading','Scoped original synchronous obstruction accepted by genuine ROOT reading')
    s=s.replace('Original2/5,new0,audit0.','Original1/5,new0,audit0.').replace("'original_attempts': '2/5'","'original_attempts': '1/5'")
    s=s.replace('Only scoped unsolved standard-partial acceptance','Only scoped unsolved synchronous-obstruction acceptance')
    for bad in ['2912','c772dc5','KP-4.36','OBSTRUCTION.md','group_block','duality_algebra','literal_realization','29933','507','original2/5','Original2/5']:
        assert bad not in s, bad
    op=oldop.replace('PR44','PR45').replace('pr44','pr45').replace('pr45_2912','pr45_9900007')
    write('prepare_current_packet.py',s); write('capture_root_builder_operation.py',op)
    write('BUILDER_SOURCE_ADAPTATION.patch',__import__('difflib').unified_diff(old.splitlines(True),s.splitlines(True),fromfile='PR44 reviewed administrative basis',tofile='PR45 source-only builder').__iter__().__str__() if False else ''.join(__import__('difflib').unified_diff(old.splitlines(True),s.splitlines(True),fromfile='PR44 reviewed administrative basis',tofile='PR45 source-only builder')))
    original=json.loads((A/'ORIGINAL_PREPARATION_MANIFEST.json').read_bytes())
    assert original['files_count']==181 and original['head']==HEAD
    auxiliary=[pin(A/r['path']) for r in original['files']]+[pin(A/'ORIGINAL_PREPARATION_MANIFEST.json')]
    auxiliary += [pin(p) for p in sorted((A/'original_preparation_closure_actual_capture').iterdir())]
    families={}
    for family,manifest in [('probability_metric_family','OWN_CLOSURE.json'),('literal_priority_family','FINAL_CLOSURE_MANIFEST.json')]:
        d=A/family; mf=json.loads((d/manifest).read_bytes()); own=[]; foreign=[]
        if family=='probability_metric_family':
            own=[{k:r[k] for k in ('path','bytes','sha256')} for r in mf['files']]
            own.append({k:v for k,v in pin(d/'OWN_CLOSURE.sha256').items() if k!='path'} | {'path':'OWN_CLOSURE.sha256'})
            assert (d/'OWN_CLOSURE.sha256').read_text().split()[0]==sha((d/manifest).read_bytes())
        else:
            for row in mf['files']:
                if row['path']==manifest: continue
                r={k:row[k] for k in ('path','bytes','sha256')}
                (own if row['publication_allowed'] is True else foreign).append(r)
            assert len(own)==49 and len(foreign)==64
        dirs=[p for p in sorted(d.rglob('*')) if p.is_dir()]
        families[family]={'manifest':{'path':manifest,'bytes':len((d/manifest).read_bytes()),'sha256':sha((d/manifest).read_bytes())},
            'copied_members':own,'foreign_members':foreign,'external_inputs':[],
            'directories':[p.relative_to(d).as_posix() for p in dirs],
            'directory_modes':{p.relative_to(d).as_posix():stat.S_IMODE(p.stat().st_mode) for p in dirs}}
    js('STATIC_INPUT_BINDINGS.json',{'schema':'PR45_FIXED_CURRENT_SOURCE_INPUTS_v1','status':'SOURCE_ONLY_ROOT_PREREQUISITES_PENDING',
      'snapshot_manifest':pin(A/'snapshot_manifest.json'),'original_metadata':pin(A/'original_pr_metadata.json'),
      'auxiliary':auxiliary,'families':families,'ROOT_prerequisites':None,'current_candidate':None})
    quals='''# PR45 current science, source and provenance qualifications

PR45 /9900007 /AMR-098-0007 remains UNSOLVED. The original9439-byte partial proof rejects only the illustrative synchronous metric condition for a single fixed joint construction. The broader general two-process characterization is neither supplied nor ruled out. Novelty remains unestablished. The original fair binary process has independent flip probabilities1/(k+2); its shifted laws converge weakly to the stationary nonergodic constant-path mixture. The all-fixed-couplings mismatch tends to1/2 by full-path conditional projection and finite-history L1 approximation, not a finite diagnostic count. The stated metric law is tied to the stated product metric. Other compatible metrics retain the failure of convergence to zero, without a claimed identical numerical limit. Offsets are nonnegative and finite or uniformly tight, possibly dependent; arbitrary escaping offsets are excluded and can repair this example. Each-n different couplings are not one fixed coupling. Setwise convergence fails, so distinct9900005 is not revised.

Both newly closed independent families validate this original scoped claim and retain its exact gap. The probability family's separate iid duplicate-block mechanism and growing first-hit-offset construction are audit-only boundary evidence; they are not an expanded original submission, new accepted theorem or new author attempt. Its early approximation imprecision and later correction stay preserved. Neither family re-executed the original helper. Future ROOT must independently reproduce unchanged helpers in private copies and inspect all actual outputs. The historical independent helper writes its receipt beside itself; a private copied review/PARTIAL is required. Saved885/3044 labels are historical observations and finite checks never establish the arbitrary-infinite-coupling quantifier, source scope or full problem.

Historical SOURCES, source_manifest and all18 originals stay byte exact. Their September30 Asmussen access failure is a dated fact. NEW access on October3 obtained Asmussen1992's complete scanned primary PDF1177292B/SHAf97b11902da4a2a980dbf114d8dca546448ab0155c479a839e4adb398c938191; the literal family rendered all13 article pages and read OCR, visually checking pp739–741. OCR contains errors and this is a bounded scoped comparison, not an independent proof audit of the whole article. Lemma2.1 gives a sufficient continuous-time one-time-marginal condition with potentially different construction for each epsilon, small finite offset, finite eventual time and strictly stationary right-continuous comparison process; Remark2.1 allows an epsilon discrepancy. It is not necessity for arbitrary weak path-shift convergence or a single synchronous joining, and no novelty follows. NEW current presentations must not repeat the old failure as present access state.

The original Thorisson author preprint's relevant Section3 pp3–4 is available only as independently recovered indexed text here, without full original PDF or pixels. The published2011 source remains metadata/subscription preview, so no full published/preprint comparison is certified. The six-page density/Skorohod preprint was freshly retrieved and read by the literal family; it builds a sequence of copies and does not enforce their being shifts of one path. Bounded search and comparisons do not prove exhaustive literature absence or universal present openness.

Original head d9b4acf5d070d1f04ffac86a4f08916a5629ff16, dated GitHub base c6975ca76f9f667f1250ba403d0e6da2aafe14d0 and actual merge base01358d66fc67d1c462bddf31c0d4ee5b120e6737 are distinct and separately checked. Original turns remain1/5,new0,audit0. Original export's queue-prefix error and separate successful repair remain preserved as genuine administrative histories; no retrospective successful execution is fabricated. Historical model, reasoning, deadline, PASS and access claims remain dated attributions. Current model/reasoning/deadline/verdict are explicitly null. NEW whole-current review remainsPENDING after future freeze.

AI tools were used extensively. This is unrefereed work with no claimed human peer review or formal certification. Future scoped repository acceptance would publish a partial report, with no paper, new DOI or tracker row. All64 literal foreign primary/access/OCR artifacts are individually hash-bound and excluded from authored packet bodies, including PDF bytes, indexed source text, OCR, pixels and their access captures. Full raw caches/SQL are likewise dependencies only, never copied as publication bodies. Dated native bindings are historical records, not current authority; separate fresh13/current-main approval is required before and after staging. These qualifications apply globally to every current presentation and metadata wrapper while original bodies remain literal archives.
'''
    write('SOURCE_PRECISION_QUALIFICATIONS.md',quals)
    write('CURRENT_OVERVIEW.md','''# PR45: scoped synchronous weak-shift coupling obstruction

The original binary process approaches a stationary constant-path law weakly while every fixed joining has coordinate mismatch tending to1/2. The original metric-error law and uniformly tight nonnegative-offset boundary are preserved. The broad two-process characterization remains UNSOLVED; novelty is unestablished. Original1/5,new0,audit0. Current Asmussen access is recorded separately from immutable historical failure. No paper/new DOI/tracker; NEW whole-current reviewPENDING.

Read PARTIAL.md with SOURCE_PRECISION_QUALIFICATIONS.md and CURRENT_PARTIAL_CONTEXT.md; original_archive preserves all18 originals. Family reports, true future ROOT evidence and actual execution references remain inspectable. Finite diagnostics support identities and do not replace the full proof. AI tools were used extensively; unrefereed, no claimed human peer review. This is a prospective current presentation; source preparation does not authorize execution or acceptance.
''')
    common={'reading_completed':False,'created_utc':None,'reading_notes':None,'root_flags':{x:False for x in FLAGS},
      'scope_certificate_sha256':None,'preparation_manifest_sha256':None,'source_qualification_sha256':None,
      'evidence_bindings_sha256':None,'family_manifest_sha256':{k:None for k in families},
      'original_substantive_attempts':1,'new_substantive_attempts':0,'audit_turns':0}
    js('DRAFT_ROOT_READ_LEDGER.json',dict(common,schema='PR45_ROOT_PRIMARY_READ_LEDGER_v1'))
    js('DRAFT_ROOT_SCIENCE_CARD.json',dict(common,schema='PR45_ROOT_SCIENCE_CARD_v1',status='unsolved',partial_valid=False,
      full_problem_solved=False,novelty_claimed=False,turn_limit=5,paper_created=False,new_DOI_created=False,
      tracker_row_created=False,read_ledger_sha256=None,current_input_manifest_sha256=None,new_whole_current_gate='PENDING',
      current_model=None,current_reasoning_effort=None,current_deadline_utc=None,current_verdict=None))
    js('DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json',{'schema':'PR45_ROOT_FRESH13_INPUT_PREIMAGES_v1',
      'approved_by_root':False,'created_utc':None,'reason':None,'current_head':None,'files':[]})
    js('DRAFT_ROOT_EVIDENCE_BINDINGS.json',{'schema':'PR45_ROOT_EVIDENCE_BINDINGS_v1',
      'approved_by_root':False,'created_utc':None,'notes':None,'manifest':None,'proof_notes':None,'summary':None})
    write('DRAFT_ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md','# DRAFT PR45 future ROOT scoped synchronous-obstruction certificate\n\nROOT reading/approval not performed by this source-preparation family. No acceptance sentinel. True ROOT certificate must be separately authored after completed reading.\n')
    js('SOURCE_STATUS.json',{'schema':'PR45_CURRENT_SOURCE_ONLY_STATUS_v1','status':'SOURCE_ONLY_ROOT_PREREQUISITES_PENDING',
      'builder_executed':False,'ROOT_operator_executed':False,'current_packet_exists_from_this_family':False,
      'ROOT_approval':None,'current_whole_verdict':None,'original1_new0_audit0':True,'created_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    write('SOURCE_PREPARATION_RESEARCH_LOG.md', '# PR45 source-only current preparation\n\n'+dt.datetime.now(dt.timezone.utc).isoformat()+
      ' — source authoring; source package50%, actual current freeze0%, discovery0%. Original closed181+manifest+four outer evidence preserved. No production import/compile/execution or ROOT gate.\n')
    print(json.dumps({'status':'SOURCE_ONLY_AUTHORED','builder_sha256':sha(s.encode()),'operator_sha256':sha(op.encode()),
      'original_auxiliary':len(auxiliary),'probability_copied':len(families['probability_metric_family']['copied_members']),
      'literal_copied':len(families['literal_priority_family']['copied_members']),'literal_foreign_individually_excluded':64,
      'ROOT_prerequisites':None,'production_executed':False},sort_keys=True))
if __name__=='__main__': main()
