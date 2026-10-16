"""One-time edition preparation; not a public kit command."""
from pathlib import Path
import hashlib,json,shutil,datetime
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent
def save(name,obj):
    p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
freeze=json.loads((ROOT/'INPUT_FREEZE.json').read_text())
selection=[]
for r in freeze['entries']:
    p=AUDIT/r['path']
    if sha(p)!=r['sha256'] or p.stat().st_size!=r['bytes']:
        raise ValueError('prior input changed: '+r['path'])
    include=('/sources/' not in r['path'] and not r['path'].endswith('.py') and p.name!='.gitignore')
    row=dict(r)
    if include:
        destination=ROOT/'history'/r['path'];destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(p,destination)
        row.update(disposition='EXACT_AUTHORED_COPY',destination=str(destination.relative_to(ROOT)))
    else:
        row.update(disposition='OMITTED',reason=('Third-party source body, converted extract or source cache; exact hash/read scope retained, no redistribution.'
                   if '/sources/' in r['path'] else 'Historical executable or cache configuration not needed by the self-contained proof or fresh edition controls; not replayed.'))
    selection.append(row)
save('CUSTODY_SELECTION.json',{'schema_version':1,'frozen_count':len(selection),'entries':selection,
     'all_prior_bytes_unchanged':True,'history_meaning':'Exact dated snapshots; acceptance labels and earlier pending flags do not override current STATUS.json.'})
old=json.loads((AUDIT/'reviews/priority_01/SOURCE_READ_LEDGER.json').read_text())
sources=[]
for s in old['retained_primary_bodies']:
    row={k:v for k,v in s.items() if k not in ('path','text_path','id')}
    if s['id']=='Gramlich_Schnitger':row['citation_id']='Gramlich_2003'
    elif s['id']=='Hujsa_single_shared':row['citation_id']='Best_Devillers_Erofeev_Wimmel_target_synthesis'
    else:row['citation_id']=s['id']
    if s['id']=='Farrell_thesis':row['authors']='Matthew Farrell (author); Lionel Levine (thesis advisor)'
    sources.append(row)
sources.append({'citation_id':'Dusart_2010','title':'Estimates of Some Functions Over Primes without R.H.',
 'authors':'Pierre Dusart','url':'https://arxiv.org/pdf/1002.0442v1','bytes':233779,
 'sha256':'3f11eca84613ad00e6a447f99b318d5c3d76e360283efcc6d3eebdda25ff3923',
 'read':'Equation (4.2) and proof, PDF4, directly read and actually viewed in the mathematical review and ROOT; identity recorded in the preserved modular SOURCE_REVIEW.md.',
 'edition':'arXiv:1002.0442v1','preparation_new_body_read':False})
save('SOURCE_LEDGER.json',{'schema_version':1,'date_utc':'2026-10-16','sources':sources,
    'read_scope_provenance':'Selective read scopes recorded by the named prior independent reviews and adopted by ROOT. Edition preparation read their complete reports and comparisons; it does not claim to have reread all 27 bodies.',
    'limits':old['global_limits'],'additional_source':'Dusart arXiv:1002.0442v1 Eq.(4.2), PDF4, as directly read in the two mathematical reviews and ROOT; exact source identity remains in history/reviews/modular_encoding_01/SOURCE_REVIEW.md and its preserved receipts.',
    'no_third_party_bodies_distributed':True,'full_result_priority':'UNKNOWN',
    'mandatory_attribution_conditions_discharged_in_current_paper_and_metadata':['HLW literal bank and priming','Stockmeyer-Meyer and sole-author Gramlich literal CRT/SAT complement with nonBoolean redundancy']})
title='A modular-storage proof of NP-completeness for chip-firing halting on simple digraphs'
description=('<p>A complete attributed proof that ordinary conservative chip-firing HALTING is NP-complete under deterministic polynomial-time many-one reductions on finite loopless simple strongly connected digraphs with nonnegative binary configurations. Hardness holds with polynomial numerical total initial chips and a specified root whose deletion leaves an acyclic graph with no path of two arcs. The main construction permits antiparallel arcs; a separately proved oriented construction forbids them. The proof includes actual legal checkpoints, conservation, schedule-independent least action, polynomial output bounds, all preprocessing cases and a polynomial-bit NP certificate.</p>'
 '<p>The literal modular-bank formula and parallel primed-toppler mechanism are credited to Holroyd, Levine and Winkler, Abelian logic gates, arXiv:1511.00422v2, Lemma 4.1. The prime Boolean and local clause-product encoding is credited to Stockmeyer and Meyer, STOC 1973, Theorem 6.1, and its reconstruction by Gregor Gramlich alone, MFCS 2003, Fact 3. The allowed-predicate intersection is the complement of the classical invalid-variable or failed-clause union; extra local nonBoolean clause-complement residues are already variable-invalid. Neither ingredient nor avoiding global-period expansion is claimed as new. NP membership, capacity and the root-last viewpoint are prior Farrell-Levine/Farrell methods, and long simple-graph clocks are prior Eriksson. Full-result, conservative simple/oriented realization and remaining method priority, and preexisting worldwide openness, remain UNKNOWN after a bounded audit.</p>'
 '<p>AI tools were used extensively in solving, verification, source comparison, programming and writing. This is an unrefereed preprint, without external human peer review, journal acceptance or formal proof-assistant certification. No firstness is claimed. The support ZIP contains the complete TeX source, exact authored historical snapshots, bibliographic hashes/read scopes and fresh standard-library finite diagnostics with meaningful faults. No third-party source bodies are redistributed, no omitted historical program is claimed replayed, and finite tests do not certify the unbounded proof or the literature.</p>')
metadata={'title':title,'upload_type':'publication','publication_type':'preprint',
 'creators':[{'name':'Kriebel, Alec','orcid':'0009-0001-9320-500X','affiliation':'Independent researcher'}],
 'description':description,'publication_date':'2026-10-16','version':'1.0','language':'eng',
 'access_right':'open','license':'cc-by-4.0',
 'keywords':['chip-firing','halting problem','NP-completeness','simple digraphs','oriented graphs','conservative dynamics','Chinese remainder theorem','modular storage'],
 'notes':'Preparation checkpoint dated 16 October 2026 UTC: the exact mathematical scope had passed two independent mathematics families and ROOT adoption; the bounded priority audit required the two exact antecedent credits reflected in this edition. At that checkpoint zero new complete whole-package reviews had been completed, at least two were required, readiness and publication were false, and ordered external actions were held behind PR #1032. These statements describe that past checkpoint, not future publication state. Full-result and realization priority and preexisting worldwide openness remained unknown.',
 'related_identifiers':[{'identifier':'https://arxiv.org/abs/1502.04690v3','relation':'isSupplementTo','scheme':'url'},
    {'identifier':'https://github.com/AlecKriebel/Math/pull/1098','relation':'isSupplementTo','scheme':'url'}],
 'references':['Farrell and Levine, CoEulerian graphs, arXiv:1502.04690v3, Sections 2-3.1; DOI 10.1090/proc/12952.',
 'Holroyd, Levine and Winkler, Abelian logic gates, arXiv:1511.00422v2, Lemma 4.1 and Section 8.3.',
 'Stockmeyer and Meyer, Word Problems Requiring Exponential Time: Preliminary Report, STOC 1973, Theorem 6.1, retained PDF pages 7-8.',
 'Gregor Gramlich, Probabilistic and Nondeterministic Unary Automata, MFCS 2003, LNCS 2747, 460-469, Fact 3.',
 'Matthew Farrell, The halting problem for chip-firing on finite directed graphs, Cornell senior thesis, 2 December 2014, Sections 1.1 and 4.1.',
 'Kimmo Eriksson, No Polynomial Bound for the Chip Firing Game on Directed Graphs, Proceedings AMS 112(4) (1991), 1203-1205.']}
save('metadata.json',metadata);save('zenodo-api.json',{'metadata':metadata})
save('publication/zenodo-deposit.json',{'metadata':metadata,'files':[
 {'path':'../paper.pdf','name':'paper.pdf'},
 {'path':'../pr1098_support_v1_0.zip','name':'pr1098_support_v1_0.zip'}]})
(ROOT/'code/metadata_constants.py').write_text('"""Exact reviewed native metadata object; no mutable input alias."""\nEXPECTED_METADATA = '+repr(metadata)+'\n')
scope={'problem_id':3000018,'alias':'AMR-029-0018','pr':1098,'head':'f37a3ff66595fcf75bb18bf859be8594c3662242',
 'theorem':'NP-completeness of ordinary conservative HALTING for finite loopless simple strongly connected digraphs, N>=2, nonnegative binary configurations; main permits antiparallel arcs and separately proved oriented version forbids them.',
 'hardness_restrictions':['Specified root deletion leaves an acyclic graph with no directed path of two arcs.','Numerical total chips polynomial in explicit SAT input size; unary encoding also retains hardness.'],
 'prior_ingredients':['HLW Lemma4.1 exact bank multiplicities and parallel priming','Stockmeyer-Meyer Theorem6.1 and sole-author Gramlich Fact3 exact prime Boolean and clause-product complement encoding','Farrell-Levine NP membership/capacity/tree-period method and classical least action','Farrell thesis/FL Section2 root-last and mass comparison','Eriksson long simple games'],
 'unasserted':['Eulerian restriction','polynomial simulation time','bounded degree','firstness','worldwide current openness','priority certification','formal or external human peer review'],
 'full_result_and_realization_priority':'UNKNOWN','remaining_method_priority':'UNKNOWN'}
save('CLAIM_SCOPE.json',scope)
save('STATUS.json',{'checkpoint_date_utc':'2026-10-16','stage':'PREPARATION_PENDING_TWO_NEW_COMPLETE_WHOLE_REVIEWS',
 'new_complete_whole_reviews_completed':0,'minimum_new_complete_whole_reviews_required':2,
 'publication_ready':False,'published':False,'services_held_after_pr':1032,
 'exact_scope_math_adopted':True,'priority':'QUALIFIED_ATTRIBUTED_PROOF; FULL_RESULT_AND_REALIZATION_UNKNOWN',
 'attribution_conditions':'Discharged in current authored materials; to be independently checked in new whole reviews.'})
(ROOT/'LICENSE.txt').write_text('Authored paper and new verification materials: Copyright 2026 Alec Kriebel.\nCreative Commons Attribution 4.0 International (CC BY 4.0).\nhttps://creativecommons.org/licenses/by/4.0/\nHistorical authored snapshots retain their dated statements. No third-party source bodies are distributed.\n')
(ROOT/'CITATION.txt').write_text('Alec Kriebel. '+title+'. Version 1.0, 16 October 2026. Unrefereed preprint.\nORCID: https://orcid.org/0009-0001-9320-500X\nLicense: CC BY 4.0. DOI not assigned at the dated preparation checkpoint.\n')
print(json.dumps({'prior_inputs':len(selection),'exact_copies':sum(r['disposition']=='EXACT_AUTHORED_COPY' for r in selection),
 'exclusions':sum(r['disposition']=='OMITTED' for r in selection),'native_metadata_objects':3}))
