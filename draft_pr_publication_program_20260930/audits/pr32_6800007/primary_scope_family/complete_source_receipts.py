#!/usr/bin/env python3
"""Primary-source variants, complete applicable proof locations and preserved retrieval failures."""
import hashlib,json,pathlib,subprocess,urllib.request
from datetime import datetime,timezone
HERE=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
receipts=[]
for label,url in [
 ('fv2020_author_pdf','https://www.researchgate.net/publication/profile/Jose-Veloso-2/publication/340658748_Flag_structures_on_real_3-manifolds/links/5e9c88ef4585150839ebc0b1/Flag-structures-on-real-3-manifolds.pdf'),
 ('fv2020_publisher_pdf','https://link.springer.com/content/pdf/10.1007/s10711-020-00528-4.pdf')]:
 r={'label':label,'url':url,'utc_started':now()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as f:
   b=f.read();r.update(http_status=f.status,content_type=f.headers.get('content-type'),final_url=f.url,bytes=len(b),sha256=sha(b),is_pdf=b.startswith(b'%PDF'))
  (HERE/'tmp'/(label+'.response')).write_bytes(b)
 except Exception as e:r.update(error_type=type(e).__name__,error=str(e))
 r['utc_finished']=now();receipts.append(r)
render=subprocess.run(['pdftoppm','-f','4','-singlefile','-scale-to','1800','-png',str(HERE/'sources/borrelli2002.pdf'),str(HERE/'tmp/borrelli_section2')],capture_output=True)
(HERE/'tmp/borrelli_render.stderr').write_bytes(render.stderr)
result={'utc':now(),'retrieval_attempts':receipts,
 'web_tool_reads':[
  {'url':'https://www.researchgate.net/publication/340658748_Flag_structures_on_real_3-manifolds','surface':'complete public author-manuscript text, uploaded by Jose Veloso 2020-04-19',
   'complete_applicable_proof_read':'Section8.1, manuscript pp26-27, Proposition8.1 and its complete proof, and definitions/introduction context',
   'local_bytes_unavailable':True,'text_not_identified_as_publisher_pdf':True,
   'direct_pdf_web_failure':'404 Not Found; ordinary urllib route is separately recorded above'},
  {'url':'https://link.springer.com/article/10.1007/s10711-020-00528-4','surface':'publisher metadata/subscription preview',
   'verified_metadata':{'authors':['E. Falbel','J. M. Veloso'],'journal':'Geometriae Dedicata','volume':209,'pages':'149-176','published':'2020-04-15','issue':'2020-12','doi':'10.1007/s10711-020-00528-4'},
   'publisher_full_proof_not_read_from_preview':True}],
 'full_proof_locations':[
  {'source':'Forstneric1986 author-hosted complete journal scan','pages':13,'read':'Full Section2 pp245-248: general smooth-bundle open ample weak equivalence, cube lemma and ample-relation proof; Theorems1.1/1.4 and complete formal-frame/Ktheory argument §5 pp251-254',
   'visual_checked':['printed p246 general bundle theorem','printed p247-248 proof via OCR/full page images','printed pp244-245 scope'],
   'bound':'Theorem1.4 is compact orientable; §2 supports local arbitrary-target application using M x F and candidate principal slices, not an unconditional existence theorem.'},
  {'source':'Koshkin2009 published journal PDF','pages':16,'read':'Full §§1-3 including all Lemmas1-5/Theorems1-3 and complete Theorem3 proof, pp331-344; checked §3 Corollary1 and references pp344-346',
   'visual_checked':['printed p343 complete Theorem3 proof'],'bound':'Theorem3 is ordinary maps into compact simply connected G/H with G compact connected simply connected and H connected, M3CW; it does not compute formal derivative data.'},
  {'source':'Borrelli2002 author PostScript, locally rendered','read':'Full §2 pp4-6 of author preprint and Euclidean formal-frame/Ktheory discussion introduction and §4 pp9-11; embedding-isotopy assumptions retained',
   'visual_checked':['author manuscript p4 full §2.1 theorem'],'bound':'Parametric embedding theorem requires an ordinary isotopy plus a specified formal homotopy. Its Euclidean Ktheory description presupposes a totally real immersion/trivial complexified tangent, not arbitrary flag-target data.'},
  {'source':'Falbel-Veloso2018 arxiv1804.11096v1','pages':28,'read':'Complete primary definitions and flagged homotopy/existence passages and final section/table of contents inspection',
   'later_proposition_absent':True,'bound':'No §8.1/Proposition8.1 in this version. Broad introduction removes compact/orientable hypotheses of cited Forstneric1.4; candidate explicitly avoids that scope leap.'}],
 'render_diagnostics':{'exit_code':render.returncode,'stderr_bytes':len(render.stderr),'stderr_sha256':sha(render.stderr),
   'warning':'Poppler Type3-glyph bad bounding-box warnings; rendered §2.1 is legible and visually inspected. Extraction artifacts are not mathematical evidence.'},
 'variant_rules':'Equal source bytes are established only by byte count plus SHA256. Converted PS PDF is a derivative with a different hash. Complete author text and published metadata do not establish equality with inaccessible publisher bytes.'}
manifest=json.loads((HERE.parent/'source_snapshot/source_manifest.json').read_text())
variants=[]
for oldname,newname in [('problems_MTDG.tex','problems_MTDG.tex'),('falbel-veloso.pdf','falbel_veloso_v1.pdf'),('forstneric1986.pdf','forstneric1986.pdf'),('borrelli2002.ps','borrelli2002.ps'),('borrelli2002.pdf','borrelli2002.pdf'),('koshkin2009.pdf','koshkin2009.pdf'),('koshkin2009.pdf','koshkin_arxiv_current.pdf')]:
 old=next(f for f in manifest['sources'] if f['file']==oldname);b=(HERE/'sources'/newname).read_bytes()
 variants.append({'original_label':oldname,'fresh_file':newname,'fresh_bytes':len(b),'fresh_sha256':sha(b),'matches_original_bytes_and_hash':len(b)==old['bytes'] and sha(b)==old['sha256']})
result['variants']=variants
result['koshkin_original_file_identified']='Original225126-byte bd1116... file equals arXiv0808.0024v2 dated21Sep2009, not the fresh199216-byte f595... journalPDF. The complete integral Theorem3/proof is present in both.'
result['nonorientable_source_guard']='Journal deRham discussion/Corollary1 p345 claims nonorientable integral H3=0, which is false for closed connected nonorientable three-manifolds (H3=Z/2). The candidate uses ordinary integral cohomology and does not transfer that corollary.'
(HERE/'SOURCE_PROOF_RECEIPTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'retrievals':receipts,'source_variants':len(variants),'complete_applicable_proofs_read':True},indent=2))
