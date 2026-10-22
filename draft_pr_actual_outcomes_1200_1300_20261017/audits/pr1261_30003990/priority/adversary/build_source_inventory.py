"""Inventory this family's retained source bytes and honest reading scopes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json

ROOT=Path(__file__).resolve().parent
SCOPES={
 'totik_varga_2012':['Printed pp.378-388 selected introduction, definitions, statements and relevant proofs; Theorem 2.1 complete printed proof pp.380-381; Theorems 3.1/3.2 upper-estimate construction and proof extension pp.383-386; Theorem 4.1 proof pp.387-388; Section 5 endpoint discussion and Example 5.1 statement p.389; reference list p.390. Example 5.1 proof not fully read.','Visually inspected complete PDF pp.2,6,9 (printed 379,383,386), including exact endpoint formula and singleton-center-compatible Theorem 3.2.','The symmetric fast-decrease premise cited from Ivanov-Totik 1990 was not checked in that missing full paper.'],
 'totik_survey_2013':['Undated author manuscript; retrieval ID 2013 is provisional and not a bibliographic date. Selected pp.1-7, endpoint/Christoffel statements, Section 3 shell proof and Section 4 endpoint construction. No reading of later complex-plane sections claimed.'],
 'totik_survey_2012_final':['Title-page year 2012, printed pp.241-247: selected first-page statement, Sections 2-4 definitions, relevant results, shell proof at p.246, Theorem 4.1 endpoint specialization at p.247. Later sections not read.'],
 'slot_laurent_1905_v2':['PDF p.2 normalized Eq.(3) and accompanying definitions (also visually inspected); pp.5-6 Lemma 4/proxy and proof; p.17 Theorem 11 and proof outline; p.21 Lemma 15/Proposition 3 and proofs; p.24 Lemma 20/Corollary 5 and proofs; pp.27-29 selected regularity extension and final questions. Intermediate geometric needle construction not fully proof-audited.'],
 'slot_laurent_2001_v2':['PDF pp.1-5: hierarchy Eqs.(2),(5),(6), Theorems 1-3 / Corollary 1, scope and original-objective eigenvalue discussion. Full proof of its main convergence theorem not read in this family.'],
 'deklerk_hess_laurent_1603_v2':['Title page including arXiv v2 banner and internal June 21,2021 date; pp.1-5 hierarchy definitions and Theorem 1.5; Section 2.2 (PDF pp.8-9) Jackson kernel definitions, degree/cone/measure scope. Main convergence proof not audited.'],
 'gribling_deklerk_vera_2605_v1':['Section 4.3, PDF pp.14-16, ordinary upper hierarchy Eqs.(23)-(25), Proposition 14 and full printed proof, Remark 15; Section 5 concluding discussion. Introduction/kernel sections searched for scope; no full proof-audit of coefficient/lower-hierarchy results.'],
 'laurent_slot_2026_overview':['PDF p.1 publication metadata; pp.10-11 normalized Eq.(14) and Table 1 (printed 158-159). Later proof sections not audited.'],
 'owr_2018':['Complete Laurent contribution PDF pp.23-25 / printed 2991-2993. PDF p.23 visually inspected: Eq.(2) probability convention and omitted mass value in Eqs.(3)-(4).'],
 'deklerk_laurent_2018_annealing':['Title/publication metadata; Corollaries 2-3 and complete quadratic-proxy reduction proof, publisher PDF pp.5-6. Remaining annealing proof not fully audited.'],
 'deklerk_laurent_1804_v1':['PDF pp.1-3 hierarchy and eigenvalue scope; pp.6-9 Jacobi-root theorem, Corollary 2.3 proof excerpt, Theorem 3.1 and complete Corollary 3.2 proof. Superseded for final numbering by publisher body below.'],
 'deklerk_laurent_2020_final':['Publisher cover and metadata; article pp.1-2 definitions; pp.4-7 recurrence/eigenvalue representation, Jacobi roots, Theorem 4 and complete Corollary 2 proof. No complete audit of multivariate upper-bound proof.'],
 'kirschner_deklerk_2203_v1':['PDF pp.1-3: general kernel axioms, Proposition 1 and full printed proof, contribution paragraph restricting quantitative construction to cube/product-Chebyshev. Later SDP construction not proof-audited.'],
 'eulersolve_index':['Captured index text searched for Lasserre,16633,density,Convergence,Endpoint,convex bod,quadratic proxy; all matching excerpts inspected. No Lasserre or 16633 match in this capture. Did not read every linked paper.'],
 'springer_mastroianni_totik_2010':['Official primary abstract/publication metadata/references; DOI correction verified. Subscription page is not the full paper.'],
 'springer_ivanov_totik_1990':['Official primary abstract/publication metadata; full paper not obtained.'],
 'springer_kroo_2016':['Official primary abstract/publication metadata/references; full paper not obtained.'],
 'springer_kroo_2026':['Full HTML body captured. Only introduction/Section 2 Theorems 1-2 (scope and extremal quantities), and the printed Theorem 1 proof following Lemma 6, read. Proof dependency Lemma 3 not audited; no positive full-target implication claimed.'],
}
METADATA_SCOPES={
 'arxiv_1905_metadata':'Official version history and title/authors; v1/v2 dates.',
 'arxiv_2001_metadata':'Official version history and title/authors; v1/v2 dates and journal DOI.',
 'arxiv_1804_metadata':'Official single-version history and title/authors.',
 'arxiv_2605_metadata':'Official v1 history/title/authors, 17-page scope and abstract.',
 'ems_owr_metadata':'Whole report title, publication date, DOI and page range; separate contribution checked in PDF.',
 'siam_1603_metadata':'Official abstract, journal metadata, pages347-367 and online publication date; read via web tool.',
 'springer_1905_metadata':'Official title, issue pages/year and online version-of-record date; read via web tool.',
 'springer_2001_metadata':'Official title, issue pages/year and online date; read via web search primary result.',
 'springer_overview_metadata':'Official chapter title, pp149-176, first-online date and DOI; read via web tool.',
 'cwi_worstcase_metadata':'Official link to final PDF and publication record; issue-page-range error distinguished from article page range.',
}

if __name__=='__main__':
 records=[]
 for receipt in sorted(ROOT.glob('*RECEIPT.json')):
  for rec in json.loads(receipt.read_text()):
   if not isinstance(rec,dict) or 'id' not in rec:continue
   rec=dict(rec);rec['receipt']=receipt.name
   source_id=rec['id']
   payload=rec.get('pdf_path') or rec.get('local_path')
   if not payload and (ROOT/'_local'/'primary'/(source_id+'.pdf')).exists():
    payload='_local/primary/'+source_id+'.pdf'
   if payload and (ROOT/payload).exists():
    data=(ROOT/payload).read_bytes()
    rec['retained_payload']={'path':payload,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'is_pdf':data.startswith(b'%PDF')}
   rec['read_scopes']=SCOPES.get(source_id,([METADATA_SCOPES[source_id]] if source_id in METADATA_SCOPES else ['No paper body read; failed PDF/version/route request or non-PDF payload.']))
   rec['full_work_proof_audit']=False
   records.append(rec)
 out={'generated_utc':datetime.now(timezone.utc).isoformat(),'source_records':records,'limits':['Retrieval is not reading.','Selected printed proof inspection does not verify every cited dependency.','Failed PDF requests may retain HTML payloads named .pdf; their signature is explicitly false.','No source-author code was executed.','Web tool search/open/find results are separately retained in _local/SEARCH_RAW.json and _local/WEB_BODY_RAW.json.']}
 (ROOT/'SOURCE_INVENTORY.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'records':len(records),'valid_pdfs':sum(r.get('retained_payload',{}).get('is_pdf',False) for r in records)},indent=2))
