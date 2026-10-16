from pathlib import Path
import hashlib,json,datetime
B=Path(__file__).resolve().parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def receipt(p):
 d=p.read_bytes();return {'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}
s=json.loads((B/'SOURCE.json').read_text())
s.pop('coverage_so_far',None)
s['completed_coverage']={'text_read_printed_pages':list(range(125,169)),'visually_inspected_printed_pages':list(range(125,169)),'all_article_pages_read':44,'critical_proofs_read_in_full_for_scope':['Theorems4.1–4.2(pp141–145)','Theorem4.3/Corollary4.2(pp148–150)','Variation and slit/control setup(pp150–156)','Theorem5.1(pp156–157)','Local expansion/Theorem5.4(pp162–165)'],'independently_verified_mechanisms':['Full-competitor pullback argument in extremal preservation, m=1 specialization','Explicit n=4adjoint equation, weights, Koebe saturation and bound','Rotation/phase invariant excludes exact matching to explicit Cor4.2family','SourceP/candidateQ coefficient and sign translation, commonpositivefactor noted','Local coefficient-modulus expansion'],'not_claimed':'Formal independent reproof of every source theorem and historical premise, or global novelty/publication clearance.'}
s['rendered_pages']=[{'pdf_page':i+1,'printed_page':125+i,'cache_path':str(p.relative_to(B)),**receipt(p)} for i,p in enumerate(sorted((B/'.cache').glob('fs1977-*.png')))]
assert len(s['rendered_pages'])==44
s['sealed_at_utc']=now
(B/'SOURCE.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n')
v={'sealed_at_utc':now,'source_status':'SOURCE_SCOPE_CLOSED_NO_VERIFIED_PRIOR_EXACT_NEGATIVE_RESULT','source_specific_access_gap_resolved':True,'source_specific_full_scope_audit_complete':True,'bounded_source_reopening_completion_percent':100,'all44pages_text_and_visual_read':True,'finite_checks_passed':16,'concrete_prior_method_overlap':'Classical Schiffer/power coefficient/exterior differential and Loewner/control/global-extremal transfer frameworks. Credit required.','explicit_degree4family':'Globally Koebe-maximized allS; candidate exact functional excluded from this displayedfamily/rotations by invariant.','no_prior_exact_negative_result_verified_in_source':True,'bvp_shortcut':'BLOCKED_EQUIVALENT_UNSUPPORTED_INSTANCE without explicit solvedsupport/slit/angle signs','novelty_certified':False,'publication_clearance':False,'aggregate_recommendation':'Maintain HOLD_HISTORICAL_FIRSTNESS_AND_PUBLICATION_CLEARANCE: remaining fullZemyan gaps unaffected. Update current aggregate ledger with this dated source closure; leave priority03sealed.','no_remote_or_external_action':True}
(B/'VERDICT.json').write_text(json.dumps(v,indent=2)+'\n')
files={p.name:receipt(p) for p in sorted(B.iterdir()) if p.is_file() and p.name not in ('MANIFEST.json','MANIFEST_CHECKS.json')}
(B/'MANIFEST.json').write_text(json.dumps({'sealed_at_utc':now,'scope':'All authored top-level files; ignored.cache renders excluded; source original held in root source folder and referenced by checksum','files':files},indent=2)+'\n')
print(json.dumps({'status':v['source_status'],'authored_files':len(files),'source_pdf_sha256':s['pdf']['sha256'],'visual_pages':len(s['rendered_pages'])},indent=2))
