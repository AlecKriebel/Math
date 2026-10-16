from pathlib import Path
import json,hashlib,datetime,zipfile,io,collections
H=Path(__file__).resolve().parent;B=H.parents[1];P=B/'preprint_v1_0';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
sources=[
('Wajnryb/Farb, author-hosted 2006 volume','reviews/positive_words_01/sources/W.pdf','https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf',[131,132,133,134],'Full surrounding positive-relations passage; chain relation (3); preceding unrestricted question; separately printed restricted arbitrary-length and maximum clauses; repetitions and separate A5/Hurwitz suggestion.'),
('Honda-Kazez-Matic math/0510639v1','reviews/positive_words_01/sources/HKM.pdf','https://arxiv.org/abs/math/0510639v1',[2,3,4],'Definition2.1, universal-cover arc order and monoid closure; complete handle-extension Lemma2.3 and Lemma2.5 including homotopically nontrivial peripheral/separating convention.'),
('Cossu-Tringali 2208.05869v3','reviews/positive_words_01/sources/CT.pdf','https://arxiv.org/abs/2208.05869v3',[4,5,6,9,10,13,14,19,20,21],'Definitions2.3/3.1/3.2/4.1, Remark3.3(2), complete local-finiteness Lemma4.2 and Proposition4.3, Higman Theorem4.10 and full Cor4.13/adjacent proof. Source uses arbitrary matching; BF length plus nonerasing expansions establishes raw ordered-word finiteness.'),
('Ivan Smith math/0011223v1','reviews/positive_words_01/sources/S.pdf','https://arxiv.org/abs/math/0011223v1',[1,2,3,4,5,6,9,10,11,12],'Symplectic LF context, genus>=2 convention, Theorem1.3; complete fixed-lift monotonicity discussion and Prop4.2 singleton proof with Cor4.3. Incorrect countable-fixed-points wording is not adopted. Neither journal-body equality nor every theorem in the source is certified.'),
('Baykur-Monden-Van Horn-Morris 1412.0352v2','reviews/positive_words_01/sources/BMVHM.pdf','https://arxiv.org/abs/1412.0352v2',[1,2,3,4,5,6,7,8,9,10],'Boundary-fixed/nonseparating convention, TheoremA, Prop1 abelianization, complete Prop3/5 and Theorem6 including exceptional-section correspondence and genus2 one-boundary40; gauge dependencies credited, not independently reproved.'),
('Juvan-Malnic-Mohar 1996 author-hosted publisher PDF','reviews/priority_01/private/raw/jmm_1996.pdf','https://users.fmf.uni-lj.si/mohar/Reprints/1996/BM96_JCT68_Juvan_SystemsofCurves.pdf',[6,7],'Complete Theorem3.3 and proof: compact bordered k-system cardinality, not repeated-word length.'),
('Malestein-Rivin-Theran 1008.3710v5','reviews/priority_01/private/raw/mrt_v5.pdf','https://arxiv.org/abs/1008.3710v5',[2,8,9,12,13],'Literal boundary convention, Prop4.1 parity/disjointness mechanism and Section6.1 boundary adaptation. Candidate coarse pants bound avoids importing the closed-surface sharp bound literally.'),
('Cahn-Fanoni-Petri 1603.00846v2','reviews/priority_01/private/raw/cfp_v2.pdf','https://arxiv.org/abs/1603.00846v2',[8,9,10],'Full Lemma10 proof, separate Lemma11 no-disk hypothesis, Section3.2 partition/signature classification. Literal single-curve punctured setting does not itself state the candidate disconnected bordered result.')]
rows=[]
for name,path,url,pages,scope in sources:
    rows.append(dict(source=name,url=url,full_relevant_text_pages_read=pages,read_scope=scope,acquisition='Existing retained primary body rehashed and read directly; no fresh full-body download or duplicate extraction retained',**pin(B/path)))
images=['reviews/surface_orbits_01/sources/rendered/wajnryb_p133.png','reviews/priority_01/private/rendered/ct_v3_p21.png','reviews/positive_words_01/sources/S-p10.png']
ledger={'utc':now,'sources':rows,'primary_source_pixels_actually_viewed':[dict(actually_viewed_this_review=True,**pin(B/p)) for p in images],'fresh_web_metadata_reads':['https://arxiv.org/abs/2208.05869v3','https://arxiv.org/abs/math/0011223v1','https://arxiv.org/abs/1412.0352v2'],'web_scope':'Version/bibliographic metadata only. Essential theorem bodies read locally above. No abstract/title exclusion or unavailability-to-absence inference.','limits':['Original Higman article body not read; needed lemma checked self-contained','No Smith journal-body read or preprint/journal byte equality certificate','No independent reproof of external gauge-theory hierarchy','No exhaustive priority search or current worldwide-open inference; novelty/application priority UNKNOWN']}
(H/'SOURCE_READ_LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n')
skill=Path('/Users/alec/.codex/plugins/cache/openai-primary-runtime/pdf/26.1013.11914/skills/pdf/SKILL.md')
external=[Path('/Users/alec/Documents/Math/AGENTS.md'),skill,Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')]
(H/'EXTERNAL_INPUT_PINS.json').write_text(json.dumps({'utc':now,'files':[pin(p) for p in external]},indent=2)+'\n')
(H/'BUILTIN_COMPILE_RECEIPT.json').write_text(json.dumps({'utc_observation':'2026-10-16T04:43Z','tool':'mcp__codex_app__compile_latex_document','arguments':{'path':str(P/'preprint.tex')},'actual_result':{'kind':'success','message':"The current source compiled successfully with the desktop editor's compiler."},'source':pin(P/'preprint.tex'),'read_only_no_authoring_marker':True},indent=2)+'\n')
pages=[dict(page=i,actually_viewed_this_review=True,**pin(H/f'scratch/page-{i}.png')) for i in range(1,8)]
(H/'VISUAL_QA.json').write_text(json.dumps({'utc':now,'delivered_pdf':pin(P/'preprint.pdf'),'pages':pages,'all_seven_new_pixel_views':True,'render_command_receipt':'RESUME02_COMMAND_RECEIPTS.jsonl','result':'PASS: no clipped/overlapping text, missing glyph, unreadable equation, broken reference or page-number defect; bibliography spacing acceptable.','compiled_source_pdf':pin(H/'scratch/compiled/preprint.pdf'),'cross_runtime_byte_identity_claimed':False,'read_only_no_authoring_marker':True},indent=2)+'\n')
archive_rows=[];recursive=[]
def inspect_zip(body,label,depth=0):
    with zipfile.ZipFile(io.BytesIO(body)) as z:
        for info in z.infolist():
            name=info.filename
            if name.endswith('.zip'):
                data=z.read(info);r={'path':label+'!/'+name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'depth':depth};recursive.append(r)
                if depth==0:archive_rows.append(r)
                inspect_zip(data,r['path'],depth+1)
            if name.lower().endswith(('.pdf','.png','.jpg','.jpeg')):
                raise RuntimeError('Unexpected source-body/image-like member '+name)
inspect_zip((P/'verification_kit.zip').read_bytes(),'verification_kit.zip')
(H/'HISTORICAL_ZIP_DISTRIBUTION_EVIDENCE.json').write_text(json.dumps({'utc':now,'current_archive':pin(P/'verification_kit.zip'),'top_level_nested_zip_members':archive_rows,'all_recursive_nested_zip_members':recursive,'duplicate_top_level_payload_sha256':'d1c03ef097938934641907c3552f05a0687347ea7945b399fff1a365322a1a1b','same_duplicate_bytes':607553,'scope':'Historical ZIPs are legitimate exact custody artifacts; the actionable issue is current blanket exclusion prose. Recursive PDF/image scan found none.'},indent=2)+'\n')
with (H/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — Whole mathematical/source/PDF/native/custody review completed. Independent custody validates all 677 frozen inputs, 623 baseline, 10 exact changes, 613 protected, 157 copies/4641 references and 75 old-pin resolutions. Actual current math/fault/output-guard and 42 independent CLI checks pass; initial two guard ENOSPC interruptions retained separately; earlier repair erasing wrapper cause still unknown. One P3 current archive-exclusion prose inconsistency confirmed. Delegated review completion estimate: 90%; underlying full mathematical research goal remains approximately 60%.\n')
print('metadata, source ledger, actual seven-page QA pins and finding evidence saved')
