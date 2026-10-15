"""MIT licensed. Prepare lean original-intake notes; no ROOT helper or math credit."""
import datetime, hashlib, json, os, pathlib, stat
R=pathlib.Path(__file__).resolve().parent
N=pathlib.Path('/Users/alec/Documents/Math')
def sha(b): return hashlib.sha256(b).hexdigest()
def put(n,body):
    p=R/n
    with p.open('x',encoding='utf-8') as f: f.write(body)
def dump(n,obj): put(n,json.dumps(obj,sort_keys=True,indent=2)+'\n')
def pin(p):
    h=hashlib.sha256(); size=0
    with p.open('rb') as f:
        while b:=f.read(1024*1024): h.update(b); size+=len(b)
    s=p.stat()
    return {'path':str(p),'bytes':size,'sha256':h.hexdigest(),
            'full_mode_07777':format(stat.S_IMODE(s.st_mode),'04o'),
            'nlink':s.st_nlink,'external_in_place':True,'not_copied':True}
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
account=json.loads((R/'SOURCE_ACCOUNTING.json').read_bytes())
auth=json.loads((R/'ORIGINAL_AUTHENTICATION.json').read_bytes())
assert account['head']==auth['head'] and account['original_substantive_attempts']==1
assert account['raw_prior']['key_present'] is False
assert account['raw_prior']['SQL_storage_type']=='text'
assert (R/'RAW_PRIOR_SQL_TEXT.txt').read_bytes()==b'{}'
inputs={n:pin(N/n) for n in [
    'AGENTS.md','unsolved_math_prioritization/AGENTS.md',
    'unsolved_math_prioritization/manifest.json',
    'unsolved_math_prioritization/cache/catalog.sqlite',
    'unsolved_math_prioritization/queue.py','unsolved_math_prioritization/state.json',
    'unsolved_math_prioritization/QUEUE.md',
    'unsolved_math_prioritization/review_v2/related_target_groups.json']}
manifest=json.loads((N/'unsolved_math_prioritization/manifest.json').read_bytes())
assert manifest['revision']==account['manifest_revision']
q=(N/'unsolved_math_prioritization/queue.py').read_text().splitlines()
assert "reports.get(p['problem_number'],{})" in q[55]
dump('EXTERNAL_INPUT_PINS.json',{'schema':'pr62-dated-external-input-pins/v1',
    'writer_pid':os.getpid(),'utc':now,'inputs':inputs,
    'raw_corpus_and_private_primary_pins':'SOURCE_ACCOUNTING.json',
    'SQL_missing_report_fallback':{'source':'unsolved_math_prioritization/queue.py',
        'LF_line_1_based':56,'operation':'json.dumps(reports.get(problem_number, {}))',
        'read_only_inspection':True,'queue_generator_executed':False},
    'scope':'Dated measured external inputs; neither copied corpus nor frozen SOURCE custody. No cache is required for ROOT packet-byte verification.'})
web=[]
def w(name,url,locators,scope,limitations):
    web.append({'name':name,'url':url,'selected_visible_read_locators':locators,
        'scope_checked':scope,'limitations':limitations})
w('Zemke, published Annals paper',
  'https://annals.math.princeton.edu/wp-content/uploads/annals-v190-n3-p05-s.pdf',
  ['web extracted text lines 0-356: selected Introduction and Section 2',
   'Section 3, web extracted lines 324-569, printed 939-943: theorem proof and Lemma 3.1 text'],
  'F2 coefficients, bigraded injection and reversed ordinary-concordance left inverse; textual proof warns the composite need not be a product annulus.',
  'PDF text supplied by web reader; no new local download/body hash or figure pixels. Underlying TQFT, grading formulas and imported sphere-map results are not independently recertified.')
w('Boninger, versioned author preprint', 'https://arxiv.org/html/2405.08103v1',
  ['Section 4, web lines 222-278: residual-nilpotence definition, Lemma 4.1, Theorem 4.2, Euler characteristic, Proposition 4.4 and concluding proof'],
  'Residual nilpotence concerns the commutator subgroup; the rigidity gate is on the successor, with equal Alexander degree. Euler characteristic transfers bigraded equality to Alexander equality.',
  'Versioned HTML selected text only; no fresh complete Gordon 1981 proof or publisher-PDF proof audit. Direction prose is interpreted through the upward movie and injection convention.')
w('Boninger bibliographic metadata', 'https://msp.org/index/ail.php?jpath=pjm&l=B',
  ['MSP author index, web line 504'], 'Pacific J. Math. 335 (2025), 81-95.',
  'Metadata access, not full publisher-PDF reading.')
w('Boninger author bibliography', 'https://sites.google.com/view/joeboninger/research',
  ['author research page, web line 23'], 'Independently agrees with page range 81-95.',
  'Public page read only; no communication with author.')
w('Wang, versioned author preprint','https://arxiv.org/html/2006.01070v1',
  ['Theorem 1.3, web lines 162-168','Theorem 1.8 and Remark 1.9, web lines 197-203'],
  'Specified nontrivial-band twist family has equal bigraded F2 hat HFK but a finite nonzero shifted Khovanov summand.',
  'Selected statements only; no full knot computation, theorem proof recertification or line-by-line comparison with journal numbering (K3 cites published Theorem 1.2).')
w('Levine-Zemke, corrected versioned preprint','https://arxiv.org/html/1903.01546v2',
  ['web lines 26-51: direction convention, coefficients, grading, Theorem 1',
   'web lines 76-117: Propositions 7-8 and main theorem proof text'],
  'Bigraded Khovanov split injection with any-ring coefficients; ordinary reversed-cobordism map supplies the left inverse up to sign.',
  'Selected HTML proof text read, without diagram pixels or independent recertification of imported dotted-cobordism/TQFT relations. No fresh journal erratum reading claimed.')
w('Agol, versioned author preprint','https://arxiv.org/html/2201.03626v1',
  ['web lines 42-55: convention and Theorems 1.1-1.2',
   'web lines 59-82: core argument','web lines 93-118: Appendix A text'],
  'Antisymmetry requires ribbon comparability in both directions. Algebraic Floer inverses do not meet that geometric hypothesis.',
  'Versioned HTML core and appendix text only; no full external group/representation/topology-dependency proof recertification, figure pixels or successful AMS DOI publication access.')
w('Baldwin-Hanselman-Sivek, versioned 2026 preprint','https://arxiv.org/html/2602.21109v1',
  ['web lines 46-60: Theorem 1.2 and Corollary 1.3',
   'web lines 140-165: Theorem 1.7, Question 1.8 and coefficient context'],
  'Fibered-predecessor finiteness and stated fibered cyclic-cover results; these statements do not supply general equal-HFK endpoint uniqueness.',
  'Selected statement/context reading; not full immersed-curve proof audit or verification that v1 is the latest version.')
w('Hom-Park, versioned 2026 preprint','https://arxiv.org/html/2608.06625v1',
  ['web lines 56-65: Theorem 1.2'],
  'Cable rigidity is for cables of one fixed companion with p>1.',
  'Selected theorem scope only; not arbitrary KP1.56 or full proof/latest-version recertification.')
w('Dunkerley, versioned 2026 preprint','https://arxiv.org/html/2606.20802v1',
  ['web lines 130-136: Theorems 1.5-1.6'],
  'Particular ribbon-minimal examples outside one classical sufficient class.',
  'Selected theorem scope only; no general equality-rigidity, complete proof or latest-version claim.')
dump('PRIMARY_READING_RECEIPT.json',{'schema':'pr62-preparer-bounded-primary-reading/v1',
    'receipt_written_utc':now,'receipt_writer_pid':os.getpid(),
    'read_operator':'/root/analytic_convex_audit',
    'web_read_timestamps':'The tool supplies no owned process timestamps for web reading; receipt time is not a claimed retrieval time.',
    'owned_web_PID_or_local_download_or_body_hash_or_visual_read_claimed':False,
    'literal_question':'Existing private K3 text in SOURCE_ACCOUNTING.json, LF2867-2893, both remarks, printed55-56, full relevant passage read; no new download or pixels.',
    'selected_primary_reads':web,
    'access_failures_or_limits':[
      {'url':'https://msp.org/pjm/2025/335-1/pjm-v335-n1-p04-p.pdf',
       'observed':'web reader returned text/html with 0 text lines; no publisher PDF reading claimed'},
      {'url':'https://doi.org/10.1090/cams/15',
       'observed':'web reader Internal Error, one-line result; no successful publication retrieval claimed'}],
    'no_full_copyrighted_primary_pdf_text_or_images_redistributed':True,
    'historical_original_primary_receipts':'Preserved verbatim in original/provenance.json and original/SOURCE_AUDIT.md; historical hashes/read assertions are not newly remeasured or transferred to this reader.',
    'literature_search_bound':'Selected cited primary statements only; no exhaustive priority or worldwide-open theorem.'})
caps={}
for step in ['retrieval','accounting','submitted_replay','historical_replay','submitted_guarded','historical_guarded']:
    p=R/'captures'/step;c=json.loads((p/'CAPTURE.json').read_bytes())
    for stream in ['stdout','stderr']:
        b=(p/c[stream]['path']).read_bytes()
        assert len(b)==c[stream]['bytes'] and sha(b)==c[stream]['sha256']
    assert c['exit_code']==0
    caps[step]={'CAPTURE':str((p/'CAPTURE.json').relative_to(R)),
      'controller_pid':c['controller_pid'],'child_pid':c['pid'],
      'started_utc':c['started_utc'],'finished_utc':c['finished_utc'],
      'exit_code':c['exit_code'],'stdout':c['stdout'],'stderr':c['stderr']}
    if step.endswith('_guarded'):
        pr=c['runtime_probe']
        assert pr['exit_code']==0
        assert json.loads((p/'probe_stdout.bin').read_bytes())=={'debug':True,'ignore_environment':1,'optimize':0}
        assert (p/'probe_stderr.bin').read_bytes()==b''
        assert c['argv'][1:3]==['-E','-B'] and '-O' not in c['argv']
        caps[step]['separate_same_flags_runtime_probe']=pr
assert (R/'captures/submitted_replay/stdout.bin').read_bytes()==(R/'original/verification.json').read_bytes()
assert (R/'captures/historical_replay/stdout.bin').read_bytes()==(R/'original/independent_review/independent_results.json').read_bytes()
assert (R/'reproduction/historical/independent_checks.py').read_bytes()==(R/'original/independent_review/independent_checks.py').read_bytes()
dump('REPRODUCTION_RECEIPT.json',{'schema':'pr62-original-finite-controls/v1',
    'receipt_written_utc':now,'writer_pid':os.getpid(),'actual_runs':caps,
    'submitted_assertions':564,'historical_independent_assertions':20223,
    'both_stdout_byte_identical_to_unchanged_original_receipts':True,
    'historical_writable_script_is_exact_original_body':True,
    'first_successful_replay_environment_qualification':'Initial capture_step.py inherited os.environ and supplied -B only. Its historical __debug__/optimization state was not measured, and environment isolation is not claimed.',
    'guarded_replay_qualification':'Separate exact-body replays use -E -B with no -O. Separate same-flags probes actually reported ignore_environment1,optimize0,debugtrue; each replay stdout is again exactly original. This checks the assertion-setting assumption, with no new mathematical credit.',
    'scope':'Exact finite F2 matrix/graded-rank, parity, shift and categorical logical controls. No knot Floer or Khovanov complex computations, geometric knot/concordance search or universal theorem by testing.',
    'original_sources_unchanged':True,'new_proof_attempts':0,'new_audit_credit':0,
    'ROOT_helpers_executed':False,'failed_owned_runs_so_far':[]})
put('SOURCE_PRECISION_QUALIFICATION.md', '''# Current source precision; originals retained

The literal KP1.56 target is isotopy of the endpoint knots under ribbon concordance and isomorphic hat HFK. The argument is presented with the usual absolutely Maslov/Alexander bigraded F2 hat-HFK conventions; the literal question does not separately print a coefficient field. Other coefficient or ungraded variants are not silently certified.

The dated triage in original/source_record.json LF6 says to make the map geometrically trivial. That wording is stronger than the needed target. Current interpretation requires endpoint isotopy, and never product isotopy of a chosen annulus. Original/OBSTRUCTION.md LF17 already states this precisely; LF38-40 correctly separates an algebraic inverse from a reversed ribbon movie and explains the composite-annulus warning. All original bytes are preserved.

Current editorial correction: original/SOURCE_AUDIT.md LF16 lists Boninger's Pacific J. Math. 335 (2025) page range as 81-93. The [MSP author index](https://msp.org/index/ail.php?jpath=pjm&l=B) and [author bibliography](https://sites.google.com/view/joeboninger/research) both list **81-95**. This is a bibliographic correction, without changing the archived claim or asserting fresh publisher-PDF access. That PDF endpoint supplied no readable PDF text to this preparer; versioned author HTML was used for selected Section4 checks.

The raw upstream report for KP-1.56 is absent. SQL stores TEXT `{}` through the missing-report default in the measured native queue.py LF56. Raw null and decoded empty object are distinct values, not contradictory classifications. Absence does not reset the authenticated historical unsolved1/5 ledger. Source readiness does not establish ROOT custody or mathematical acceptance.

The first successful finite-replay captures inherited the environment and used -B only; their historical optimization/__debug__ state was not measured. They are preserved without claiming environment isolation. Separate later exact-body replays use -E -B with no -O and retain separate same-flags probes reporting optimize0, ignore_environment1 and debugtrue. These guarded runs reproduce the original bytes and narrow that environmental assumption without new mathematical credit.
''')
put('ORIGINAL_INTAKE_REPORT.md', '''# PR62 original intake: unresolved KP1.56

PR62 is an open draft at head98cc2821e9376507caf2d2c57414f7c7e7719c1b, basec6975ca76f9f667f1250ba403d0e6da2aafe14d0. Complete read-only GitHub blob/tree authentication preserved the 17 scientific/support bodies, their Git100644 modes, SHA1 blob identities, complete byte counts and SHA256 values. All 18 diff paths are authenticated; the eighteenth is the queue presentation. No native branch, reference or index was modified. ROOT custody and scientific adjudication remain separate.

The literal target is whether ribbon-concordant knots with isomorphic hat HFK must have isotopic endpoints. The entire selected primary question and both remarks were read from the dated, pinned private K3 text LF2867-2893 (printed55-56), without new download or figure reading. SOURCE_PRECISION_QUALIFICATION.md governs the endpoint/product distinction and coefficient convention. This is original intake, not a new independent mathematical review or proof attempt; the initial uncaptured GitHub display exposed candidate excerpts before the saved initial scope, and this is disclosed.

The original partial argument imports Zemke's F2 bigraded split injection. Its nonnegative graded dimension deficits sum to zero when total ranks agree, so each vanishes. This equivalence reduces the target to strict total-rank increase for nonisotopic ribbon-comparable endpoints; it supplies no geometric inverse. An ordinary reversed concordance can contain maxima. Agol's antisymmetry needs a ribbon concordance in each direction. These requirements remain central.

The credited affirmative gate is equal Alexander degree with a successor whose knot-group commutator subgroup is residually nilpotent, imported through Boninger's restatement of Gordon. Equality of bigraded HFK gives equality of Alexander polynomials by Euler characteristic. Fibered knots lie in the sufficient class; the stronger statement that either equal-HFK endpoint being fibered forces both is conditional on the standard imported fiberedness-detection theorem. No full Gordon 1981 proof or underlying Floer-theory reconstruction was performed here.

The original Wang band-twist route concerns a specified nontrivial band on a split two-component link. Its finite nonzero Khovanov shift, together with the bigraded split injection, excludes ribbon comparability between distinct members; formal shift controls do not realize knots. The 2026 cited scopes are fibered finiteness, fixed-companion cable rigidity and particular minimal examples. They do not give arbitrary equality-case endpoint isotopy. The odd-rank chain bound remains conditional on resolving the missing equality case.

The author564 and historical independent20223 finite controls ran under genuine separate owned captures and exactly reproduced the unchanged original output bodies. Their full stdout, empty stderr, genuine child/controller PIDs, UTC, prelaunch operator/controller bodies and author proof dependency are retained. They test finite algebra/logical models, not knot Floer computations, actual concordance search or a proof of the universal target. The historical checker was an exact-body copy run in a writable reproduction directory; it did not write into the original archive.

The initial successful captures inherited environment options and used -B only; no measured historical optimization/debug state or environment isolation is claimed. A distinct guarded controller subsequently ran both unchanged bodies with -E -B and no -O, retaining actual same-flags runtime probes and complete streams. Both guarded outputs are again exact. This is an environmental reproducibility check, not new mathematics.

Typed accounting: the original source record equals the raw problem and SQL payload. The raw prior report is ABSENT and selected as null; SQL TEXT `{}` is the measured missing-report fallback, not SQL NULL. Native queue/state are dated observations only, with queued0/5 and absent state key; the authenticated original turns and PR queue preserve unsolved1/5. Neither the fallback nor absent native state resets the one substantive historical attempt. New attempts0, audit0, novelty0, no paper or DOI.

Primary access is bounded by PRIMARY_READING_RECEIPT.json: selected published Zemke text including Section3 and Lemma3.1, Boninger author-version Section4, corrected Levine-Zemke proof text and Agol core/Appendix text, plus selected Wang and 2026 statements. This is not a recertification of every imported theorem or dependency. The MSP Boninger PDF endpoint returned no readable text; the AMS Agol DOI failed. No new primary PDF/text/images are redistributed. External private cache and corpus bodies are dated in-place references, not fixed packet custody. Historical source-reader claims remain historical.

The strongest original result remains the credited sufficient rigidity class and sound algebraic reduction. Exact remaining gap: arbitrary successor cases outside that class still require a proof of endpoint isotopy or a genuine distinct ribbon-comparable equal-HFK pair. No global answer, exhaustive literature/priority claim, new topology result, native acceptance or publication is established by this packet. ROOT must independently verify custody and adjudicate the science before any later ordered action.
''')
put('README.md', '''# PR62 original source handoff

Original intake for 2715/KP1.56, proposed **unsolved1/5**, new0/audit0/novelty0. Original17 are unchanged under original/. The current interpretation and exact remaining mathematical gap are in ORIGINAL_INTAKE_REPORT.md and SOURCE_PRECISION_QUALIFICATION.md. SOURCE_ACCOUNTING.json distinguishes absent raw prior from SQL TEXT `{}`. ORIGINAL_AUTHENTICATION.json and complete API streams pin the actual head/base/scientific domain.

REPRODUCTION_RECEIPT.json points to genuine own captures for original564 and historical20223 finite controls. They are not knot Floer computations. Historical author/reviewer claims remain historical. PRIMARY_READING_RECEIPT.json records actual bounded fresh textual primary reading and access limitations; whole published papers/private corpora were not copied into this handoff. External cache pins are dated references only. PR_QUEUE_SELECTED.json's `whole_body_not_copied` means no standalone second queue-body copy: the sole complete queue-blob API response is retained within the full original retrieval stream to preserve actual evidence.

The first successful captures do not measure historical optimization or establish environment isolation. The separately retained guarded replays use -E -B/no-O and actual same-flags runtime probes, reproduce both original outputs, and receive no new mathematical credit.

The fixed SOURCE will index every prepared regular file except itself, with full07777 file0444 and directory0755 topology, no symlinks or multiple links. ROOT_verify_original.py, ROOT_close_original.py and ROOT_readback_original.py are source-only helpers, syntax-read by the preparer but never executed or imported. ROOT should run them in separate owned captures; closure receipt must be outside the fixed packet. These helpers verify custody only. No ROOT scientific decision, native acceptance, merge, Git/PR write, paper, DOI or external individual communication is created here.
''')
with (R/'RESEARCH_LOG.md').open('a',encoding='utf-8') as f:
    f.write(f'- {now} — Intake75%: complete original17/Git100644 authentication at actual15669, typed raw/SQL accounting18393, submitted564 actual18399 and historical20223 actual18401 all passed with complete streams. Fresh selected primary text reading and two access limits recorded. Current endpoint-isotopy and Boninger81-95 qualifications written; historical bytes unchanged. Source topology/admin verification and unexecuted ROOT helpers remain. New math/audit/novelty0; target remains unsolved1/5.\n')
print(json.dumps({'status':'PREPARED_NOTES_AND_DATED_RECEIPTS','pid':os.getpid(),
    'utc':now,'new_math_credit':0,'ROOT_helpers_executed':False},sort_keys=True))
