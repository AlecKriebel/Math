#!/usr/bin/env python3
"""PR1280 actual context/metadata assembler. No writes without an explicit phase.

Only literal registered manifest schemas are followed. Input receipt paths,
private inventories and external deployed-artifact fields are never membership.
"""
from pathlib import Path
import argparse,hashlib,html,json,runpy,subprocess,sys
HERE=Path(__file__).resolve()
if HERE.parent.name=='_local':A=HERE.parents[1]
elif HERE.parent.name in {'context_assembly','document_scope_revision1'} and HERE.parent.parent.name=='reviews':A=HERE.parents[2]
else:raise RuntimeError('Assembler must live in the named audit _local or context_assembly folder')
P=A/'publication'
TITLE='Strong approximate innerness of finite abelian diagonal actions on Cuntz-Krieger algebras'
PDF='Diagonal_Actions_Strong_Approximate_Innerness_Note_v1.0.pdf'
ZIP='Diagonal_Actions_Strong_Approximate_Innerness_Verification_v1.0.zip'
EPOCH='1792195200'
SID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';GID=1254632077
TRACKER_URL='https://docs.google.com/spreadsheets/d/'+SID+'/edit#gid='+str(GID)
CLAIM=('Every finite abelian diagonal quasi-free action on a simple purely infinite Cuntz-Krieger algebra associated with a finite essential 0-1 matrix is strongly approximately inner, with implementing unitaries in the fixed algebra of the whole action. '
       'This gives an affirmative deduction for the historical Question 1 in OWR2017/42, including periodic matrices, nonouter actions and nonfaithful actions. No approximate representation law is asserted.')
CREDIT=('This note is attributed exposition and complete explicit verification of known consequences of prior theorems, not a claim of a new solution or mechanism. '
        'The main deduction uses Gabe-Szabo, arXiv:2205.04933v1 (10 May 2022), Theorem 5.8, together with the established diagonal-coboundary mechanism, an explicitly normalized vertex inner kernel, an honest cocycle, and finite-group averaging with polar correction. '
        'The separate verification material also retains the original Barlak-Szabo 2019 route with explicit reductions removing its outerness and aperiodicity restrictions. '
        'Prior credit includes Izumi for the standard finite Cuntz case (inspected 2002 preprint, Proposition 5.6(2)), Matsumoto 2000 for diagonal coboundaries and periodic-point constraints, and Crisp-Gow for the periodic return corner (inspected 2004 v1, Theorem 3.1). '
        'The source audit also credits Christensen-Neagu-Szabo, arXiv:2504.12730v1/v2, for the prior strong-approximate-innerness duality framework, without attributing the combined full-target deduction as their printed statement. '
        'The inspected preprints and the final publication metadata are distinguished. No first solution, independent discovery, new mechanism, first explicit combined theorem or current worldwide openness is claimed. '
        'Priority for an older explicit complete combined statement remains unestablished; the full Zacharias chapter and final Izumi 2004 body were unavailable in the current source audit. Bounded search failures do not certify priority.')
SCOPE=('The verification material preserves nine immutable original submitted files and a separately bound, explicitly documented current nine-file edition. Historical acceptance, source-access and aggregate-check records are not treated as current approval or reconstructed missing inputs. '
       'Written arguments cover the full fixed algebra, normalized inner kernel, honest cocycle correction, periodic return corners and nonfaithful actions. '
       'Finite graph, character, corner and cocycle programs are diagnostic consistency checks rather than proofs of operator-algebra limits; durable current programs use explicit checks in normal and both optimized Python modes. '
       'Earlier assertion-based programs remain historical evidence. Omitted older proof/program/input bytes and omitted third-party source bodies are not retroactively authenticated or replayed. '
       'AI tools were used extensively in research, mathematical reasoning, verification, literature review, internal adversarial review and writing. '
       'This work is unrefereed; no external human peer review, journal acceptance or formal proof-assistant certification is claimed.')

def need(value,message):
    if not value:raise RuntimeError(message)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def binding(path):data=path.read_bytes();return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def save(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def checker():return runpy.run_path(str(P/'verification/verify.py'))
def metadata():
    dois=['10.4171/OWR/2017/42','10.4310/ACTA.2024.v232.n1.a1','10.7146/math.scand.a-114823',
          '10.1215/S0012-7094-04-12221-3','10.1090/S0002-9939-06-08216-5','10.2140/pjm.1998.184.161',
          '10.1016/j.jfa.2012.08.024','10.4171/JNCG/648']
    urls=['https://arxiv.org/abs/2205.04933v1','https://arxiv.org/abs/1708.08258v3',
          'https://arxiv.org/abs/math/0404542v1','https://www.math.kyoto-u.ac.jp/preprint/2002/4.ps',
          'https://jot.theta.ro/jot/archive/2000-044-001/2000-044-001-005.pdf',
          'https://nyjm.albany.edu/j/2005/11-18.html']
    return {'title':TITLE,'upload_type':'publication','publication_type':'preprint',
       'description':''.join('<p>'+html.escape(text,quote=False)+'</p>' for text in [CLAIM,CREDIT,SCOPE]),
       'creators':[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],
       'access_right':'open','license':'cc-by-4.0','version':'1.0','publication_date':'2026-10-17',
       'keywords':['Cuntz-Krieger algebras','finite abelian actions','diagonal quasi-free automorphisms','strong approximate innerness','equivariant uniqueness','cocycle correction','reproducible mathematics','AI-assisted mathematics'],
       'related_identifiers':[{'identifier':d.lower(),'relation':'references','scheme':'doi'} for d in dois]
          +[{'identifier':u,'relation':'references','scheme':'url'} for u in urls]
          +[{'identifier':'https://github.com/AlecKriebel/Math/pull/1280','relation':'isDerivedFrom','scheme':'url'}]}

# These exact manifest names/schemas were inspected. No glob or key inference.
REG=[
 ('reviews/alternate_reconstruction_adversary/OUTPUT_MANIFEST.json','files','relative_path','bytes','math'),
 ('reviews/blind_reconstruction_adversary/MANIFEST.json','members','path','bytes','math'),
 ('reviews/blind_source_reconstruction/MANIFEST.json','members','path','bytes','math'),
 ('reviews/blind_validation_revision1/MANIFEST.json','files','relative_path','bytes','math'),
 ('reviews/candidate_adversary/MANIFEST.json','files','relative_path','bytes','math'),
 ('reviews/corner_cohomology_adversary/OUTPUT_MANIFEST.json','files','relative_path','bytes','math'),
 ('reviews/corner_cohomology_revision1/OUTPUT_MANIFEST.json','files','relative_path','bytes','math'),
 ('reviews/new_adversary_validation_revision1/MANIFEST.json','files','relative_path','bytes','math'),
 ('reviews/workflow_tooling/MANIFEST.json','authored_files','path','bytes','workflow'),
 ('reviews/context_assembly/MANIFEST.json','authored_files','path','bytes','workflow'),
 ('reviews/note_author/OUTPUT_MANIFEST.json','files','relative_path','bytes','documentary'),
 ('priority/direct_lineage/OUTPUT_MANIFEST.json','files','relative_path','bytes','priority'),
 ('priority/lineage_cross_structural/OUTPUT_MANIFEST.json','files','relative_path','bytes','priority'),
 ('priority/structural_cross_lineage/OUTPUT_MANIFEST.json','files','relative_path','bytes','priority'),
 ('priority/structural_followup_general_lemmas/OUTPUT_MANIFEST.json','files','relative_path','bytes','priority'),
 ('priority/structural_reductions/OUTPUT_MANIFEST.json','files','relative_path','bytes','priority'),
 ('priority/root_extension/MANIFEST.json','files','path','bytes','priority'),
 ('reviews/document_scope_revision1/MANIFEST.json','files','relative_path','bytes','documentary'),
 ('reviews/workflow_revision1/MANIFEST.json','authored_files','path','bytes','workflow')]
ROOTFILES=['ELIGIBILITY_REVALIDATION.json','LIVE_PR_PREFLIGHT.json',
 'ROOT_BLIND_VALIDATION_REVISION_AUTHENTICATION.json','ROOT_CANDIDATE_DIAGNOSTIC_REPLAY.json',
 'ROOT_CORNER_REVISION_REPLAY.json','ROOT_EXTENDED_MATH_AUTHENTICATION.json',
 'ROOT_FINAL_FAMILY_AUTHENTICATION.json','ROOT_GRAPH_GROUP_REPLAY.json','ROOT_GRAPH_GROUP_RESULTS.json',
 'ROOT_INITIAL_MATH_FAMILY_AUTHENTICATION.json','ROOT_MATHEMATICAL_REVIEW.md',
 'ROOT_PRIMARY_SOURCE_INSPECTION.json','ROOT_PRIORITY_QUERY_LEDGER.json','ROOT_WORKFLOW_AUTHENTICATION.json',
 'root_graph_group_check.py','PACKAGE_GUIDE.md','ROOT_CURRENT_EDITION_AUTHENTICATION.json',
 'ROOT_DOCUMENT_SCOPE_REVISION1_AUTHENTICATION.json','ROOT_WORKFLOW_REVISION1_AUTHENTICATION.json']
# Explicitly known optional, stable documentary outputs; never searched by glob.
OPTIONAL_FILES=['ROOT_CURRENT_METADATA_WORKFLOW_REPLAY.json',
 'reviews/blind_source_reconstruction/SEAL.json','reviews/blind_reconstruction_adversary/SEAL.json',
 'reviews/note_author/OUTPUT_SEAL.json','reviews/workflow_tooling/SEAL.json',
 'reviews/context_assembly/SEAL.json','priority/lineage_cross_structural/SEAL.json']
SOURCE_RECEIPTS={'SOURCE_REGISTER.json','SOURCE_LEDGER.json','SOURCE_PROVENANCE.json','SOURCE_CHECKS.json',
 'ROOT_PRIMARY_SOURCE_INSPECTION.json','ROOT_PRIORITY_QUERY_LEDGER.json'}
HISTORICAL_RECEIPTS={'LIVE_PR_PREFLIGHT.json','INITIAL_INPUT_BINDING.json','INPUT_AUTHENTICATION.json',
 'INPUT_BINDING.json','INPUT_BINDINGS.json','VALIDATION_RUNS.json','RUNS.json','REPRODUCIBILITY.json'}
REPLAYS=[
 ('root_graph_group_check.py','ROOT_GRAPH_GROUP_RESULTS.json','Finite exact graph periods/return paths, abelian characters, normalized vertex potentials and a Pauli boundary diagnostic; not an operator-algebra proof.'),
 ('reviews/candidate_adversary/checks.py','reviews/candidate_adversary/CHECK_RESULTS.json','Independent finite graph, phase and corner-word diagnostics; explicit validation remains active under optimization.'),
 ('reviews/blind_validation_revision1/check_reductions_durable.py','reviews/blind_validation_revision1/DETERMINISTIC_RESULTS.json','Detached explicit-check reproduction of the original source-only finite graph/character results; historical live timestamps are not replayed.'),
 ('reviews/corner_cohomology_revision1/CHECKS.py','reviews/corner_cohomology_revision1/DETERMINISTIC_RESULTS.json','Detached deterministic orbit-frame, exhaustive finite graph and Pauli tests; no sealed output is overwritten.'),
 ('reviews/new_adversary_validation_revision1/boundary_checks_durable.py','reviews/new_adversary_validation_revision1/boundary_checks_durable_RESULTS.json','Detached explicit boundary-case graph/phase/potential and nonsplit-kernel diagnostics.'),
 ('reviews/new_adversary_validation_revision1/alternate_checks_durable.py','reviews/new_adversary_validation_revision1/alternate_checks_durable_RESULTS.json','Detached exact matrix, honest noncommutative cocycle, phase and return-corner consistency diagnostics.')]

def role(raw):
    name=Path(raw).name
    if name in SOURCE_RECEIPTS:return 'source_receipt'
    if name in HISTORICAL_RECEIPTS:return 'historical_receipt'
    return 'authored_evidence'

def curated_inventory(v):
    registry=[];files={}
    def add(raw,assigned=None):
        path=v['member'](A,raw);need(path.is_file(),'Missing explicitly curated authored artifact '+raw)
        item={'path':raw,**binding(path),'role':role(raw) if assigned is None else assigned}
        if raw in files:need(files[raw]['bytes']==item['bytes'] and files[raw]['sha256']==item['sha256'],'Conflicting curated binding '+raw)
        files[raw]=item
    for raw,ek,pk,sk,family_role in REG:
        path=v['member'](A,raw);need(path.is_file(),'Missing exact registered manifest '+raw)
        base=path.parent.relative_to(A).as_posix();reg={'path':raw,'base':base,'entries_key':ek,'path_key':pk,'size_key':sk,'sha256':sha(path),'role':family_role}
        v['registry_schema'](reg);registry.append(reg);add(raw,'authored_evidence')
        obj=json.loads(path.read_text());entries=obj.get(ek);need(isinstance(entries,list) and bool(entries),'Empty declared authored manifest '+raw)
        for entry in entries:
            name=v['manifest_member_name'](reg,entry,obj);member_raw=base+'/'+name
            v['check_binding'](v['member'](A,member_raw),entry,sk);add(member_raw)
    for raw in ROOTFILES:add(raw)
    for raw in OPTIONAL_FILES:
        if (A/raw).is_file():add(raw)
    # All relative membership selections above are checked again by the sealed
    # actual checker. Source/input/output receipt fields are never traversed.
    v['authenticate_nested_manifests'](A,registry)
    names={item['path'] for item in registry}
    for raw,item in files.items():
        name=Path(raw).name.lower()
        if item['role']=='authored_evidence' and (name=='manifest.json' or name.endswith(('_manifest.json','_freeze.json'))):need(raw in names,'Manifest-like authored output needs an explicit registration '+raw)
    return registry,[files[raw] for raw in sorted(files)]

def actual_inputs(v):
    snapshot=json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text());v['authenticate_snapshot'](A/'submitted',snapshot)
    correction=json.loads((A/'CURRENT_EDITION_CORRECTION.json').read_text())
    source={'submitted_snapshot_sha256':sha(A/'SUBMITTED_SNAPSHOT.json'),
      'current_edition_correction_sha256':sha(A/'CURRENT_EDITION_CORRECTION.json'),
      'current_edition':{name:binding(A/'current_edition'/name) for name in sorted(v['NAMES'])}}
    v['authenticate_source_bindings'](A,A,{'edition_mode':'documented_correction','source_bindings':source})
    gates={name:json.loads((A/name).read_text()) for name in ['MATH_GATE.json','PRIORITY_ADJUDICATION.json']}
    for name,gate in gates.items():
        need(gate.get('pr')==1280 and gate.get('problem_id')==30003587 and gate.get('original_head')==snapshot['head'] and gate.get('status')=='PASS','Actual exact-target PASS gate required '+name)
    priority=gates['PRIORITY_ADJUDICATION.json']
    need(priority.get('firstness_claim') is False and priority.get('current_openness_claim') is False and priority.get('novelty_clearance') is False,'Actual no-firstness/current-openness priority framing required')
    need(priority['mathematical_gate_sha256']==sha(A/'MATH_GATE.json') and priority['current_edition_correction_sha256']==source['current_edition_correction_sha256'],'Priority/math/current correction anchors differ')
    registered={r[0] for r in REG};allowed=set(ROOTFILES)|registered|{'SUBMITTED_SNAPSHOT.json','CURRENT_EDITION_CORRECTION.json'}
    for item in gates['MATH_GATE.json'].get('root_inputs',[])+gates['MATH_GATE.json'].get('independent_review_anchors',[])+priority.get('priority_families',[]):
        need(item.get('path') in allowed,'Gate input requires explicit curated registration '+str(item.get('path')))
        v['check_binding'](v['member'](A,item['path']),item)
    need({x['path'] for x in priority['priority_families']}=={r[0] for r in REG if r[4]=='priority'},'Actual priority gate must bind exactly all six registered priority families')
    author=json.loads((A/'reviews/note_author/OUTPUT_MANIFEST.json').read_text())
    need(author.get('schema')=='pr1280-note-author-output-manifest-v1' and author.get('stage')=='final_authored_deployed_and_bound','Actual final author manifest required; no alternate filename inference')
    need((A/'reviews/document_scope_revision1/main.tex').read_bytes()==(P/'manuscript/main.tex').read_bytes(),'Current deployed source differs from the explicitly registered F4 revision')
    # The original author source remains authenticated as immutable history by
    # its own unchanged manifest; the current revision is a separate family.
    need(author.get('external_deployed_artifact',{}).get('sha256')==hashlib.sha256((A/'reviews/note_author/main.tex').read_bytes()).hexdigest(),'Original author source history differs')
    tracker=runpy.run_path(str(P/'append_tracker.py'));need(tracker['SID']==SID and tracker['GID']==GID,'Actual deployed tracker identity differs')
    proposal=json.loads((A/'reviews/context_assembly/METADATA_PROPOSAL.json').read_text());need(proposal==metadata(),'Canonical exact metadata proposal differs from assembler source')
    v['metadata_contract'](proposal)
    return snapshot,source,gates

def document_bindings(expected_pages):
    need(type(expected_pages) is int and expected_pages>0,'--expected-pages must be an actual positive page count')
    compiled=json.loads((P/'COMPILE_RECEIPT.json').read_text());layout=json.loads((P/'LAYOUT_VERIFICATION.json').read_text())
    source=sha(P/'manuscript/main.tex');pdf=sha(P/'output/pdf/main.pdf')
    need(compiled.get('returncode')==0 and compiled.get('source_sha256')==source and compiled.get('pdf_sha256')==pdf and compiled.get('source_date_epoch')==EPOCH and bool(compiled.get('at_utc')),'Actual current compilation receipt required')
    lines=subprocess.check_output(['pdfinfo',str(P/'output/pdf/main.pdf')],text=True).splitlines();pages=[int(line.split(':',1)[1]) for line in lines if line.startswith('Pages:')]
    need(pages==[expected_pages],'Requested pages differ from actual independent pdfinfo')
    need(layout.get('status')=='pass' and layout.get('source_sha256')==source and layout.get('pdf_sha256')==pdf and layout.get('all_pages_visually_inspected') is True and layout.get('page_indices_inspected')==list(range(1,expected_pages+1)) and layout.get('pages')==expected_pages and bool(layout.get('at_utc')),'Actual current all-page layout receipt required')
    return {'source_sha256':source,'pdf_sha256':pdf,'compile_receipt_sha256':sha(P/'COMPILE_RECEIPT.json'),'layout_receipt_sha256':sha(P/'LAYOUT_VERIFICATION.json')}

def assemble(expected_pages,bootstrap=False):
    v=checker();snapshot,source,gates=actual_inputs(v);registry,portable=curated_inventory(v)
    names={entry['path'] for entry in portable};replays=[]
    for program,result,scope in REPLAYS:
        need(program in names and result in names,'Durable replay program and exact stdout reference must both be retained '+program)
        replays.append({'program':program,'mode':'normal_O_OO','result':result,'output_mode':'stdout','scope':scope,'layout':'isolated','arguments':[],'comparison':'bytes_exact'})
    context={'schema':'math-pr1280-current-context-v1','pr':1280,'problem_id':30003587,
      'original_head':snapshot['head'],'original_branch':snapshot['branch'],'original_body_sha256':snapshot['body_sha256'],
      'title':TITLE,'expected_pdf_pages':expected_pages,'source_date_epoch':EPOCH,
      'edition_mode':'documented_correction','edition_text':{},'structured_records':{},'source_bindings':source,
      'disclosures':{'firstness_claim':False,'current_openness_claim':False,'ai_assisted':True,'unrefereed':True},
      'metadata':metadata(),'publication_text':{'summary':CLAIM,'priority_statement':CREDIT,'verification_scope':SCOPE},
      'tracker':{'original_problem':'30003587 (OWR-15585-006): OWR2017/42 p.2621 Question1, finite abelian diagonal quasi-free actions; https://doi.org/10.4171/OWR/2017/42 ; https://github.com/AlecKriebel/Math/pull/1280',
        'notes':'Full historical target answered affirmatively as an attributed deduction from Gabe-Szabo2022v1 Theorem5.8 and explicit normalized inner-kernel/honest-cocycle arguments; original Barlak-Szabo2019 route independently verified with its reductions. Known-consequence exposition; no first solution/new mechanism/current-openness claim. Preprint and scoped verification archive.'},
      'authored_freezes':registry,'portable_files':portable,'diagnostic_replays':replays,
      'gate_bindings':{key:sha(A/name) for key,name in [('math_gate_sha256','MATH_GATE.json'),('priority_adjudication_sha256','PRIORITY_ADJUDICATION.json'),('submitted_snapshot_sha256','SUBMITTED_SNAPSHOT.json')]}}
    if not bootstrap:context['document_bindings']=document_bindings(expected_pages)
    return context

def no_external_stage_state():
    need(not any((P/name).exists() for name in ['STAGE_INTENT.json','STAGE_RECEIPT.json','PUBLISH_INTENT.json','PUBLICATION_RECEIPT.json','FINAL_REVIEW_GATE.json']),'Assembly after staging/review/publication state requires a separate explicit reconciliation')

def main():
    parser=argparse.ArgumentParser(description=__doc__);group=parser.add_mutually_exclusive_group()
    group.add_argument('--inspect',action='store_true',help='read-only actual input and complete-context construction; default')
    group.add_argument('--bootstrap',action='store_true',help='explicitly write compilation context only, omitting future document_bindings')
    group.add_argument('--finalize',action='store_true',help='explicitly write exact full actual context and two-file deposit manifest')
    group.add_argument('--metadata-only',action='store_true',help='explicitly write the proposed exact two-file deposit manifest')
    parser.add_argument('--expected-pages',type=int,help='required for finalize/inspect; bootstrap alone may use tentative6 before compilation')
    parser.add_argument('--replay-diagnostics',action='store_true',help='read-only temporary-copy replay of all six exact stdout references in normal/-O/-OO')
    args=parser.parse_args();pages=args.expected_pages
    if args.bootstrap:
        if pages is None:pages=6
    elif args.metadata_only:
        no_external_stage_state();actual_inputs(checker());save(P/'zenodo-deposit.json',{'metadata':metadata(),'files':[{'path':PDF},{'path':ZIP}]});print(json.dumps({'metadata_sha256':sha(P/'zenodo-deposit.json'),'scope':'Actual proposed metadata only; no publication clearance.'},indent=2));return
    else:need(pages is not None,'--expected-pages is required and independently checked against the actual PDF')
    need(type(pages) is int and pages>0,'Positive --expected-pages required');context=assemble(pages,bootstrap=args.bootstrap)
    replay=[]
    if args.replay_diagnostics:
        import tempfile
        scratch=A/'reviews/context_assembly/_local';scratch.mkdir(exist_ok=True);tempfile.tempdir=str(scratch)
        replay=checker()['replay_diagnostics'](A,context)
    if args.bootstrap or args.finalize:
        no_external_stage_state();path=A/'CURRENT_PR1280_CONTEXT.json'
        if args.bootstrap and path.exists():need('document_bindings' not in json.loads(path.read_text()),'Bootstrap cannot overwrite an accepted complete context')
        previous=path.read_bytes() if path.exists() else None;temporary=A/'_local/ASSEMBLED_CONTEXT_CANDIDATE.json';save(temporary,context);temporary.replace(path)
        try:
            if args.finalize:checker()['load_context'](A,P)
        except BaseException:
            if previous is None:path.unlink()
            else:temporary.write_bytes(previous);temporary.replace(path)
            raise
        if args.finalize:save(P/'zenodo-deposit.json',{'metadata':metadata(),'files':[{'path':PDF},{'path':ZIP}]})
    print(json.dumps({'phase':'bootstrap_written' if args.bootstrap else 'actual_context_and_metadata_written' if args.finalize else 'read_only_actual_context_inspection',
       'pages':pages,'pages_meaning':'Tentative compilation bootstrap only; not an actual page-count certification.' if args.bootstrap else 'Actual independent pdfinfo and all-page layout receipt checked.',
       'families':len(context['authored_freezes']),'portable_files':len(context['portable_files']),'durable_replays':len(context['diagnostic_replays']),
       'all_six_replayed_normal_O_OO':len(replay)==6,'replayed_programs':[entry['program'] for entry in replay],
       'source_bindings':context['source_bindings'],'gate_bindings':context['gate_bindings'],
       'document_bindings':context.get('document_bindings'),'metadata_fields':sorted(context['metadata']),
       'metadata_proposal_sha256':sha(A/'reviews/context_assembly/METADATA_PROPOSAL.json'),
       'tracker':{'spreadsheetId':SID,'gid':GID,'title':'Math Puzzles','url':TRACKER_URL,'headers':['Original Problem','Solution Chat URL','DOI','Notes']},
       'scope':'Actual local source/gate/manifest/document authentication and, only if requested, scoped diagnostic replay. No service call or publication approval. Context/metadata writes occur only in explicitly selected write phases.'},indent=2))
if __name__=='__main__':main()
