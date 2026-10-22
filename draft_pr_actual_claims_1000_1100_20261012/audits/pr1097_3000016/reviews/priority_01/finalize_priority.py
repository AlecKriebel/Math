#!/usr/bin/env python3
"""Write scoped source/custody records and terminal seals; never alter inputs."""
from pathlib import Path
import ast, datetime, hashlib, json, subprocess

ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent.parent
UTC=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()

def digest(b): return hashlib.sha256(b).hexdigest()
def pin(path,base=ROOT):
    b=path.read_bytes()
    return {'path':str(path.relative_to(base)), 'bytes':len(b), 'sha256':digest(b)}
def write(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def need(ok,msg):
    if not ok: raise RuntimeError(msg)

READ={
 'FL_v3':([2,10,11,12,13], 'Full exact source definition and complexity proof interface, including Theorem3.1 and Corollary3.2; not unrelated theorem certification.'),
 'HKT_v4':([2,3,4,8,9,10,12], 'Definitions, period deletion, complete Theorem12 membership proof, complete Theorem14 recurrence-target proof, Problem19; generalization proof not fully audited.'),
 'T_v2':([2,3,4,5,6,7], 'Full chip-firing proof chain for Claim2.4, Theorem2.3, Proposition2.8 and source interfaces; rotor algorithm elsewhere not certified.'),
 'BL_author':([1,2,11,13,16,17,18], 'Author-manuscript period deletion and full reachability §5 proof plus introduction; not a publisher-byte identity claim.'),
 'KT_latest':([1,2,6,7,10,11,12,13,14], 'Theorem statements and full bounded-reserve simulation §4; PDF12,13 actual pixels viewed. Other underlying hardness theorems credited, not re-proved.'),
 'ACE_journal':([1,2,3,4,5,39,40,41,42,43,44], 'Model definitions/overview and full Theorem21 hardness construction/proof; cyclic-case opening only. General NP-membership certificate-size theorem not audited afresh. PDF43 pixels viewed.'),
 'MD_latest':([1,2,3,4,9,25,28], 'Actual optimization target, definitions and main theorem statements/comparison; only proof portions at25 and28, not complete long technical proof. No whole-source correctness certification.'),
 'CL_latest':([7,9,10,11,12,13,14,24,25,26,50,51,53,54,55,56,57], 'Introduction, relevant state/period definitions, complete critical burning-test argument and its explicitly exponential runtime; not full97-page monograph.'),
 'AM_latest':([39], 'Original v1 printed Theorem7.2 and surrounding reduction as a bibliographic antecedent to FL; polarity/notation not silently reconciled into a new hardness claim; no independent correctness certification.'),
 'PP_v5':([1,2,8,15,16], 'Actual sink-recurrent definition and optimization theorem/proof at15, with source scope/conclusion; other feedback-set theorem dependencies not re-proved.'),
 'HT_latest':([1,2,3,11,12], 'Directed divisor/nontermination definitions and Eulerian-only structural and Riemann-Roch statements/proof interface; not complete paper.'),
 'HLM_latest':([1,2,3], 'Primary survey introduction, graph/sandpile/rotor definitions and least-action statement; not complete survey proofs.'),
 'LO_latest':([1,2], 'Self-reachable definition and simple undirected/tree scope; not complete enumeration proof.'),
 'Devil_latest':([1,2], 'Parallel-update/real-chip graphon activity definition and main stated target; not activity theorem proofs.'),
 'T_thesis':([33,34,36,38], 'Membership proof, period-dependent reachability theorem, recurrence-target scope and historical questions. Earlier thesis chapters not read wholesale.'),
 'MultiArrival2025':([1,2,3], 'Actual tree-like rotor graph and rotor-state/sink-output model plus main algorithm statements; no proof of its algorithm claimed.'),
 'Klivans_book':([244,245,246], 'Divisor/dollar-game/rank discussion and KT attribution; this is not a read of old infinite-graph universality proofs.'),
 'Petri_complexity':([13,14,23,24,25,26,27,28,66], '2008 thesis definitions and reproduced ordinary conflict-free/sinkless proof chain, source bibliography. This is a secondary account of1977/1988 theorems, whose original bodies remain uninspected.'),
 'Petri_joinfree_2021':([1,2,3], 'Primary author model definitions and actual acyclic join-free theorem scope; full SAT construction not read/certified.'),
 'Petri_single_shared':([1,2,3,8,9], 'Weighted choice-free/marked-graph restrictions, actual liveness/conditional reachability contributions; no complete proof audit.'),
 'Petri_marking_equation_correct':([8,19,20,21,22,23], 'Primary weighted-model restrictions and complete displayed live-WMG potential/reachable argument and related conditional statements; not all larger-class proofs.'),
 'Alimonti_2011':([1,2,3,4,5], 'Published primary body explicitly unit-weight/no-parallel, structural conflict-free definition and relevant potential-firing argument; not a full reproof of cited NP-completeness. PDF3 pixels viewed.'),
}

QUERIES=[
 '"chip-firing" "reachability" "coNP" complete',
 '"chip-firing" "reachability" "coNP-hard"',
 '"chip firing" "reachability" "2026" complexity',
 '"chip-firing" "reachability" "Karp"',
 '"chip-firing reachability" -site:unsolvedmath.com -site:researchgate.net',
 '"chip-firing" "simple" "NP-complete" halting',
 '"chip-firing" "nonhalting" "reachability"',
 '"chip-firing" "gate" "reachability"',
 '"chip-firing" reachability coNP 2024 2025 2026',
 '"chip firing" "co-NP-complete"',
 '"chip-firing reachability" reduction termination',
 '"chip-firing" "nontermination" "reduction"',
 '"chip-firing" "reachability" "coNP-complete" -site:unsolvedmath.com -site:github.com',
 '"chip-firing" "reachability" "co-NP-hard" -site:unsolvedmath.com -site:github.com',
 '"chip-firing" "reachability" "many-one"',
 '"chip-firing" "gate" "nonhalting"',
 '"chip-firing" "reachability" 2023 2024 Karp',
 '"chip-firing" "reachability" 2025 2026 hardness',
 '"chip-firing" "NONHALTING" reduction',
 '"chip-firing" "coNP-completeness"',
 '"chip-firing reachability" 2026 coNP',
 '"chip-firing" "reachability" "marker"',
 '"chip firing" "reachability" "polynomial reduction"',
 '"chip-firing" "halting" "simple directed" 2026',
 '"conflict-free" "Petri" "reachability" coNP',
 '"chip-firing" "conflict-free" complexity',
 '"communication-free" "Petri" "binary" "reachability"',
 '"join-free" "Petri" "reachability" complexity',
 '"conflict-free Petri nets" "binary" reachability',
 '"conflict free" "Petri" "weighted" reachability coNP',
 '"COMPLEXITY OF THE REACHABILITY PROBLEM IN" Petri Jancar',
 '"chip-firing" "persistent" "Petri"',
 '"weighted choice-free" "reachability" complexity',
 '"choice-free nets" "coNP"',
 '"choice-free" "reachability" "NP-complete"',
 '"Jones" "Landweber" "Lien" "complexity" "1977"',
 '"chip-firing" "reachability" complexity -site:unsolvedmath.com -site:researchgate.net -site:arxiv.org after:2024-01-01',
 '"chip-firing" "coNP-hardness"',
 '"chip-firing" "co-NP-hardness"',
 '"chip-firing" "strongly connected" "reduction" "reachability"',
 '"Checking marking reachability with the state equation in Petri net subclasses" arxiv',
 '"conflict-free vector replacement systems" completeness reachability',
 '"chip-firing" "halting to reachability"',
 '"chip firing" "non-halting" "marker"',
 '"chip-firing" "Karp reduction" reachability -site:github.com',
 '"chip-firing reachability" "2024"',
 '"chip-firing reachability" "2025"',
 '"chip-firing reachability" "2026" -site:unsolvedmath.com',
 '"chip-firing" reachability "complete" "2026" -site:researchgate.net -site:unsolvedmath.com',
 '"chip-firing" "nonhalting" "gate" -site:github.com',
 '"chip-firing" "NONHALTING" "REACHABLE" -site:github.com',
 '"chip-firing" "termination" "reachability" "reduction" Petri nets',
 '"chip-firing" reachability "complement"',
 '"chip-firing" "state bound" reduction',
 '"chip-firing" "bounded simulation"',
 '"chip-firing" "reachability" "2019" "2020"',
 '"chip-firing" "many-one" -site:unsolvedmath.com -site:github.com',
 '"chip-firing" "simple digraphs" hardness after:2022-01-01',
 '"reachability" "chip-firing" "co-NP-complete" -site:github.com',
 '"reachability" "chip-firing" "NONHALTING" -site:github.com',
]

def main():
    # Exact read-only actual-Git and old-stage checks, not just old labels.
    checks=[]
    inp=json.loads((ROOT/'INPUT_PINS.json').read_text())
    for row in inp['records']:
        path=AUDIT/row['path']; actual=pin(path,AUDIT)
        need(actual['bytes']==row['bytes'] and actual['sha256']==row['sha256'],'changed baseline '+row['path'])
        checks.append(actual)
    submitted=json.loads((AUDIT/'SUBMITTED_PINS.json').read_text())
    originals=[]
    for row in submitted['files']:
        b=(AUDIT/row['snapshot_path']).read_bytes()
        g=subprocess.run(['git','show',submitted['head_oid']+':'+row['repository_path']],cwd=AUDIT,capture_output=True,check=True).stdout
        need(b==g and digest(b)==row['sha256'] and len(b)==row['bytes'],'original mismatch '+row['snapshot_path'])
        originals.append({'path':row['snapshot_path'],'git_path':row['repository_path'],'bytes':len(b),'sha256':digest(b),'actual_git_body_equal':True})
    write('INPUT_PRESERVATION.json',{'utc':UTC(),'status':'ALL_PINNED_INPUTS_UNCHANGED','baseline_records':checks,'original_git_records':originals,'head_oid':submitted['head_oid']})

    urls={}
    for file in ('retrieve_sources.py','retrieve_additional.py','retrieve_resume.py'):
        tree=ast.parse((ROOT/file).read_text())
        for node in ast.walk(tree):
            if isinstance(node,ast.Assign) and isinstance(node.value,ast.List):
                try:
                    for pair in ast.literal_eval(node.value):
                        if isinstance(pair,tuple) and len(pair)==2: urls[pair[0]]=pair[1]
                except (ValueError,TypeError): pass
    urls.update({'JLL_1977':'https://core.ac.uk/download/pdf/81144441.pdf',
                 'Petri_single_shared':'https://arxiv.org/pdf/2005.04818',
                 'Petri_marking_equation':'https://arxiv.org/pdf/2006.05635',
                 'Petri_marking_equation_correct':'https://arxiv.org/pdf/2006.05600',
                 'Alimonti_2011':'https://bibliotecadigital.exactas.uba.ar/download/paper/paper_03043975_v412_n4-5_p320_Alimonti.pdf'})
    sources=[]
    for path in sorted((ROOT/'sources/raw').glob('*.pdf')):
        key=path.stem; txt=ROOT/'sources/extracted'/(key+'.txt')
        b=path.read_bytes(); need(b.startswith(b'%PDF'),'nonpdf retained')
        row={'id':key,'url':urls.get(key),'pdf_bytes':len(b),'pdf_sha256':digest(b),'private_storage':str(path.relative_to(ROOT))}
        if txt.exists():
            text=txt.read_bytes(); row.update(text_bytes=len(text),text_sha256=digest(text),pdf_pages=txt.read_text().count('\f'))
        if key in READ:
            pages,scope=READ[key]
            need(max(pages)<=row['pdf_pages'],'bad page scope '+key)
            row.update(status='RELEVANT_BODY_SCOPES_READ',read_pdf_pages_one_based=pages,scope=scope)
        elif key=='Petri_marking_equation':
            row.update(status='EXCLUDED_WRONG_IDENTIFIER_AFTER_TITLE_CHECK',scope='Actual paper concerns data augmentation for speech-recognition dialogue models; not a Petri-net source.')
        else:
            row.update(status='RETAINED_EDITION_NOT_SUBSTANTIVELY_READ_HERE',scope='Custody only; do not infer theorem numbering or byte identity with inspected editions.')
        sources.append(row)
    need(sum(r['status']=='RELEVANT_BODY_SCOPES_READ' for r in sources)==22,'read body count')
    write('SOURCE_READ_LEDGER.json',{'utc':UTC(),'scope':'Exact retained bytes and page-specific reading, not full-paper certification','body_records':sources,
        'read_scoped_bodies':22,'original_uninspected_or_unavailable':[
            {'title':'Jones, Landweber, Lien, Complexity of some problems in Petri nets (1977)','status':'ORIGINAL_BODY_UNAVAILABLE_HERE; CORE returned403','url':'https://core.ac.uk/download/pdf/81144441.pdf'},
            {'title':'Howell and Rosier, Completeness results for conflict-free vector replacement systems (1988)','status':'PUBLISHER_ABSTRACT_ONLY; exact original-body conventions/additional consequences UNKNOWN','url':'https://doi.org/10.1016/0022-0000(88)90013-X'},
            {'title':'Hoang thesis, On Two Combinatorial Reconfiguration Problems','status':'INDEXED_PRIMARY_THESIS_PASSAGE_ONLY; complete body not available here','url':'https://www.research-collection.ethz.ch/bitstream/handle/20.500.11850/572947/1/thesis-hoang.pdf'},
            {'title':'Universality of the chip-firing game; conflicting chip-firing and2012 subclass reachability paper','status':'METADATA_OR_DISCOVERY_ONLY; uninspected proofs and additional implications UNKNOWN'}],
        'web_body_reads':[
            {'url':'https://lemon.cs.elte.hu/egres/open/Chip-firing','scope':'Full returned survey body read; cached revision displays30Nov2021; current page-state not authenticated.'},
            {'url':'https://lemon.cs.elte.hu/egres/open/Complexity_of_the_chip-firing_reachability_problem_for_general_digraphs','scope':'Full returned exact problem body read by following survey link11; revision displays5Dec2016; no current-world openness inference.'},
            {'url':'https://tmlilla.web.elte.hu/talks/papers.html','scope':'Author bibliography for discovery/chronology, not absence proof.'},
            {'url':'https://arxiv.org/abs/2411.18364','scope':'Submission/version dates and abstract; mathematical comparison uses separate journal body.'},
            {'url':'https://arxiv.org/abs/2604.13949','scope':'Submission/version dates and abstract; main comparison uses retained v2 body.'},
            {'url':'https://arxiv.org/abs/1502.04690','scope':'Bibliographic metadata corroboration, distinct from full v3 body read.'},
            {'url':'https://arxiv.org/abs/1507.03209','scope':'Bibliographic metadata corroboration, distinct from full v4 body read.'},
            {'url':'https://www.sciencedirect.com/science/article/pii/S0195669821001608','scope':'Publisher abstract/bibliographic metadata for2022 barrier; not publisher-PDF byte identity.'},
            {'url':'https://egres.elte.hu/www/tr-15-10.html','scope':'Technical-report metadata and links; numbering not assumed equal across editions.'}
        ],'primary_source_distribution':'No PDF, extracted text or rendered source pixels included in public review outputs.'})
    need(len(QUERIES)==60,'query count')
    write('QUERY_LEDGER.json',{'utc':UTC(),'count':len(QUERIES),'queries':[{'sequence':i+1,'query':q} for i,q in enumerate(QUERIES)],'outcome':'Discovery across exact classifications, complements, Karp/gate mechanisms, recent literature and equivalent models. No exact earlier full theorem established among actual read interfaces; no exhaustive absence or priority certification. Repeated/overlapping queries are not independent controls.','nonprimary_policy':'Search snippets, mirrors, author bibliographies and UnsolvedMath are discovery aids; mathematical comparisons rely on listed primary bodies. No current shard work consulted as outside evidence.'})

    images=json.loads((ROOT/'SOURCE_PIXELS_TO_VIEW.json').read_text())['records']
    for row in images:
        path=Path(row['path']); b=path.read_bytes()
        need(len(b)==row['bytes'] and digest(b)==row['sha256'],'pixel changed before receipt')
    write('SOURCE_VISUAL_INSPECTION.json',{'utc':UTC(),'status':'ALL_FOUR_COMPLETE_PAGES_ACTUALLY_VIEWED','records':images,'observations':'KT exact reserve identities and drift bound, generalized-rotor variable proof, published Petri unit-weight convention visually confirmed. Read-only review; no authoring/compiler marker required.','cleanup':'After this successful receipt is written, only these own derivative PNGs are removed for disk pressure; retained hashes describe the captured inspection stage.'})
    for row in images: Path(row['path']).unlink()
    return len(checks),len(originals),len(sources)

if __name__=='__main__':
    counts=main(); print(json.dumps({'status':'CUSTODY_AND_SCOPED_LEDGERS_WRITTEN','baseline_records':counts[0],'actual_git_originals':counts[1],'retained_pdf_bodies':counts[2]}))
