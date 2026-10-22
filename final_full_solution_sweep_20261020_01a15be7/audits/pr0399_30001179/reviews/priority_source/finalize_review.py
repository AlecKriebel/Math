from pathlib import Path
import datetime as dt,hashlib,json,subprocess
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parents[1]
EFFORT=HERE.parents[3]
PRIVATE=EFFORT/'private/pr0399_priority'
now=dt.datetime.now(dt.timezone.utc).isoformat()
def write(name,x): (HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
snapshot=json.loads((AUDIT/'SOURCE_SNAPSHOT.json').read_text())
inputs=[]
for entry in snapshot['files']:
 p=AUDIT/entry['snapshot'];b=p.read_bytes()
 assert len(b)==entry['bytes'] and hashlib.sha256(b).hexdigest()==entry['sha256']
 inputs.append({'path':entry['snapshot'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
write('BINDING.json',{'checked_utc':now,'pr':399,'problem_id':'30001179','source_alias':'OWR-3392-005','head':snapshot['head'],'original_files_verified':len(inputs),'original_files':inputs,'actual_read_before_previous_audit_opinions':['original/CANDIDATE_PROOF.md','original/README.md','original/EXPOSITION_NOTE.md'],'prior_audit_reports_not_used_as_premises':True})
r=json.loads((HERE/'SOURCE_DOWNLOADS.json').read_text())
scopes={
 'skeide_index2006':'Actual complete section10.2, printed33–34; introduction/context about Section9/10. Visually inspected PDF34. Search all extracted text is a screen, not whole-paper reading.',
 'skeide_sigma2022':'Actual theorem2.9 and context of units/spatiality; complete section4 printed6–7 and all references7–8, especially ref30. Visually inspected6. No claim of whole-paper proof reproduction.',
 'fowler1995':'Actual complete section2 printed752–756 including intertwiner spaces, Borel structure and multiplication; following Section3 introduction and full-Fock finite-word setup. Not a complete41-page audit.',
 'tsirelson2004':'Actual introduction; section5a definition5a1 and surrounding measurable-family discussion printed39–41; section5c opening tensor/homogeneous definition; section6a classical-part statements/proofs printed50–52; section10a opening/theorem10a1/measure-class definition10a2 printed111–112. Visually inspected39. Remaining complete-body searches explicitly only screens.',
 'liebscher_randomsets':'Actual introduction on random-set stationary factorizing measure types; square-root-of-measure construction(2.1)–(2.2), definition2.1 measurable families; definition3.1 and notes3.1–3.2/Example3.2 for tensor product systems. Visually inspected PDF10. Remaining body keyword screen only; a separately rendered57 was not used as the definition-page evidence.',
 'shalit_skeide2020':'Actual abstract, definition4.1/remark4.2 tensor-product category, definition4.3 units, definitions5.1–5.2 and surrounding subsystem discussion, appendix summary of isometric product maps, bibliography entries Ske09b/Ske22b. Only two exact free-product-system phrase occurrences in full-body screen; neither screen nor selected reading is a complete233-page audit.',
 'skeide_classification2016':'Actual bibliography entries Ske09c and Ske14b, plus complete-body exact-phrase screen (two occurrences). No complete memoir reading or reproduction claimed.',
 'skeide_abstract2013':'Actual complete institutional abstract and type/file availability notice; no files associated. Forward construction and cocycle questions only.',
 'skeide_abstract2016':'HTTPS certificate verification failed; recovered by separately recorded actual HTTP PDF. Do not treat this failed request as a reading.',
 'skeide_roland65':'Actual complete Skeide abstract on PDF8, including relationship to conditional freeness and monotone independence; no talk body/video was obtained.',
 'skeide_seminar2026':'Actual corresponding2Feb2026 entry and its actual linked abstract URL in HTML. Remaining seminar list not a mathematical literature audit.',
 'skeide_seminar2026_abstract':'Complete actual one-page abstract, also visually inspected. Both forward constructions are explicit; no converse-generation result or counterexample announced.',
 'attal_nechita2008':'Actual introduction, section3 reduced free Hilbert product, definitions of toy/Fock subspaces and Theorem1(1) with its finite-rectangle density proof on8; Theorem2 higher multiplicity statement. Visually inspected8. No entire operator-convergence proof audit claimed.',
 'margetts_srinivasan2012':'Actual introduction, definition4.1/remarks4.2 and unit definitions4.4–4.7; remark8.17 and succeeding free-flow finite-Fock setup. Visually inspected11. No complete E0-invariants paper audit.',
 'skeide_abstract2011':'Actual complete institutional abstract and no-associated-files notice; forward tensor-to-free construction and adapted-cocycle problem, no negative generation result.',
 'tsirelson_linearizable1998':'Actual abstract/introduction, theorem1.6/note1.7 and theorem1.8/conjecture1.11, section2 opening classical-noise tensor identities. Not a full proof audit of linearizability. Applies to classical stochastic group representations, not an arbitrary pointed free system.',
 'skeide_independence2003':'Actual abstract/introduction, conditional-independence theorem2.5, section3 dilation discussion through theorem3.1/remarks3.2–3.5. Concerns monotone filtration; not a converse reconstruction of arbitrary free systems.',
 'arici_ge2025':'Actual arXiv2504.12843v1 introduction and section2 definition, definition4.1/lemma4.2, definition4.7 and proposition4.8 complete proof/corollary4.9. Publisher HTML definition4.1/lemma4.2 and date/volume metadata independently inspected through web. arXiv and journal bodies are not asserted byte-identical.',
 'skeide_author_homepage':'HTTPS timed out; actual HTTP frames and publication list recovered separately. Not a missing-body inference.',
 'skeide_author_homepage_http':'Actual complete HTTP frame wrapper with its actual relative frame target. No mathematics in wrapper.',
 'skeide_abstract2016_http':'Actual complete Skeide entry46 on printed9. Forward lifting of spatial dynamics to free dynamics; no universal converse or negative result announced.',
 'skeide_author_frame':'Actual complete nested frames wrapper; followed observed relative links only.',
 'skeide_author_links':'Actual complete navigation links; followed observed publications-page link.',
 'skeide_author_main':'Actual author front page examined for public navigation/context; not used as mathematical evidence and no contact action taken.',
 'skeide_author_publications':'Complete displayed title list read, published entries through2023 plus preprints; no exact target negative or downloadable in-preparation forward manuscript listed. Date-limited website coverage, not a complete author-work census.',
 'skeide_publication_list_pdf':'The observed PUB.pdf link actually contains the1994 SUq(2) PhD thesis, not a publication-list PDF. Actual title/contents checked to correct filename-based misclassification; no whole-thesis reading or absence inference. Unrelated to target.'
}
for x in r['sources']:
 x['reading_scope']=scopes[x['name']]
 if x.get('private_path'):
  p=EFFORT/x['private_path'];assert len(p.read_bytes())==x['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
 if x['name']=='skeide_publication_list_pdf':x['actual_document']='1994 PhD thesis on Levy–Khintchine formula for SUq(2); misleading local alias corrected from actual title'
write('SOURCE_DOWNLOADS.json',r)
source=EFFORT/'private/pr0399_sources/OWR_2009_09.pdf';data=source.read_bytes();assert hashlib.sha256(data).hexdigest()=='5121d8ec30d2c1346cbbdd68164915d5a24fb31e5a94a3a3215ba576954ee64d'
write('ORIGINAL_SOURCE_SCOPE.json',{'timestamp':now,'url':'https://publications.mfo.de/bitstream/handle/mfo/3111/OWR_2009_09.pdf?isAllowed=y&sequence=1','retrieval':'Parent-provided actual official PDF, independently hashed and read; not claimed as my own new download.','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'read':'Complete Skeide printed528–530, definition529 and generation assertion530;529/530 visually inspected at PDF37/38.','universal_category':'Pointed Hilbert B–B bimodules with central unit, associative pointed B-bilinear free-product unitaries; canonical zero-time fibre.','regularity':'Source leaves additional continuity/measurability bundle hypotheses to formulations analogous to tensor case and specifically mentions embedded tensor multiplication. Explicit candidate continuous separable scalar Hilbert field is within that category.','question':'Does the maximal embedded tensor subsystem generate the given entire free product system?','separate_questions':['adapted free cocycles','characterizing associated E0 semigroups','recovering an arbitrary input spatial tensor system after forward construction'],'historical_open_status':'Stated as an open problem in actual2009 source; related universal generated-free-system question occurs in actual2006§10.2. No inference that it remained open everywhere in2026.'})
private=[]
for p in sorted(PRIVATE.rglob('*')):
 if p.is_file():
  b=p.read_bytes();rel=p.relative_to(EFFORT.parent).as_posix();c=subprocess.run(['git','check-ignore',rel],cwd=EFFORT.parent,capture_output=True,text=True);assert c.returncode==0,p
  private.append({'path':p.relative_to(EFFORT).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_ignored':True})
write('PRIVATE_CUSTODY_MANIFEST.json',{'timestamp':now,'all_bodies_text_and_renders_ignored':True,'files':private,'scope':'Custody hashes only. Full third-party source bodies, HTML and page pixels are not in the public review tree.'})
write('VISUAL_SOURCE_SCOPE.json',{'timestamp':now,'actually_viewed_source_pages':[{'source':'original2009','pdf_pages':[37,38],'printed_pages':[529,530]},{'source':'skeide_index2006','pdf_pages':[34]},{'source':'skeide_sigma2022','pdf_pages':[6]},{'source':'skeide_seminar2026_abstract','pdf_pages':[1]},{'source':'tsirelson2004','pdf_pages':[39]},{'source':'liebscher_randomsets','pdf_pages':[10]},{'source':'margetts_srinivasan2012','pdf_pages':[11]},{'source':'attal_nechita2008','pdf_pages':[8]}],'scope':'Definition, operator-symbol, exact-quantifier and theorem-hypothesis readings checked against actual pages. No new manuscript or layout authored.'})
print(json.dumps({'bound_original_files':len(inputs),'source_requests':len(r['sources']),'successful_body_requests':sum('sha256' in x for x in r['sources']),'private_ignored_files':len(private)}))
