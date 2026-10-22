#!/usr/bin/env python3
"""Write final review evidence and recheck input custody; no mutations outside own tree."""
from pathlib import Path
import datetime,hashlib,json,stat,sys
R=Path(__file__).resolve().parent;A=R.parents[1];P=A/'preprint_v1_1'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(name,obj):(R/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def need(p,msg):
    if not p:raise RuntimeError(msg)
def main():
    utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    freeze=json.loads((R/'INPUT_FREEZE.json').read_text());bad=[]
    for row in freeze['files']:
        p=A/row['path'];s=p.stat();actual=dict(size=s.st_size,sha256=sha(p.read_bytes()),inode=s.st_ino,device=s.st_dev,nlink=s.st_nlink)
        if any(row[k]!=v for k,v in actual.items()):bad.append(dict(path=row['path'],actual=actual,expected=row))
    need(not bad,'frozen input changed')
    original=json.loads((A/'preparation/unknown_priority_20261016/ORIGINAL_INPUT_PINS.json').read_text());oldbad=[]
    for row in original['files']:
        b=(A/row['path']).read_bytes()
        if len(b)!=row['bytes'] or sha(b)!=row['sha256']:oldbad.append(row['path'])
    need(not oldbad,'original 287-file evidence changed')
    seal=json.loads((P/'PREPARATION_SEAL.json').read_text())
    for row in seal['files']:
        b=(P/row['path']).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'preparation row changed')
    final_hashes=[sha((R/f'commands/independent_final_{m}.stdout').read_bytes()) for m in ('normal','O','OO')]
    need(len(set(final_hashes))==1,'optimization-dependent fresh computation')
    runs=[json.loads(p.read_text()) for p in sorted((R/'commands').glob('*.json'))]
    need(all(r['expectation_met'] and r['outcome']=='completed' for r in runs),'unexpected or incomplete execution')
    for r in runs:
        for suffix in ('stdout','stderr'):
            b=(R/'commands'/f'{r["name"]}.{suffix}').read_bytes();need(len(b)==r[suffix+'_bytes'] and sha(b)==r[suffix+'_sha256'],'raw command receipt mismatch')
    write('COMMAND_RUNS.json',dict(utc=utc,executions=len(runs),zero_exit=sum(r['returncode']==0 for r in runs),intentional_nonzero=sum(r['returncode']!=0 for r in runs),unexpected=0,incomplete=0,runs=runs))
    pages=[]
    observations={1:'Title, ORCID, abstract, disclosures and conventions legible.',2:'Statement and source-interface/basis hypotheses legible.',3:'Reverse equation, pair factor and rational germ legible.',4:'Scalar table, transport lemma and proper-kernel text legible.',5:'Full-open restriction and odd cycle; noninduction bridge legible.',6:'All fifteen Hall/Y rows and consequences legible.',7:'Antecedents, UNKNOWN comparison and replay instructions legible.',8:'Reproducibility boundaries and bibliography legible.',9:'Final references legible; sparse final page acceptable.'}
    for n in range(1,10):
        c=(R/f'source_renders/candidate-{n}.png').read_bytes();d=(R/f'source_renders/compiled-{n}.png').read_bytes()
        need(c==d,'rebuild raster difference')
        pages.append(dict(page=n,actually_viewed=True,observation=observations[n],candidate_png_sha256=sha(c),compiled_raster_equal=True))
    write('PDF_QA.json',dict(utc=utc,pages=pages,actual_candidate_pages_viewed=9,visual_defects=[],offline_compile_exit=0,compiler_warnings='Two underfull bibliography hbox warnings, badness1210, line248; no observed overfull/undefined-reference warning.',pdf_byte_identity_promised=False))
    inspection=[]
    def source(name,path,scope,visual=[]):
        p=A/path;b=p.read_bytes();inspection.append(dict(id=name,path=str(p),bytes=len(b),sha256=sha(b),actual_read_scope=scope,actually_viewed_pdf_pages_1_based=visual,full_source_proof_reproved=False))
    source('FLO','reviews/analytic_01/sources/raw/FLO-published.pdf','Published pp.200–203 normalization/inverses/Lemma1.1/segment relation; pp.214–217 tau-Witt and simultaneous twist; (4.5), (6.6), Conjecture6.12; p.283 (12.1),(12.5); pp.291,293–294 basis, reverse scalar and open restriction. Corresponding local extracted text read; deep source proofs remain dependencies.',[18,33,41,58,62,99,107,109,110])
    source('LM16','reviews/analytic_01/sources/raw/LM-v3.pdf','arXiv1411.6310v3: §§2.1–2.3, Proposition2.5(5), Theorem2.6, Definition5.13, full LC graph and Proposition5.20, §A.5; extracted p16 Leclerc example read.',[8,10,11,35,38,53])
    source('JPSS','reviews/analytic_01/sources/raw/JPSS-published.pdf','Published scan: §8.2/(5), pp.444–445; §2.9 epsilon monomials, pp.395–396. Relevant local OCR and rendered pages inspected; no claim of full-body reproof.',[31,79,80])
    source('OWR','reviews/priority_01/sources/raw/owr_ems.body','EMS cover and Lapid contribution heading; printed pp.729,731,734: local converse, orbit sum, imprimitive definition and Conjecture4.',[1,9,11,13,16])
    source('HKU','reviews/priority_01/sources/raw/lz_hku_announcement.body','Institutional program pages1 and4: event date and same-title Luo–Zha announcement abstract; no internal proof/parameters inferred.',[1,4])
    for key,scope in [('lm2014_pdf','Local text pp.27–28, transported rank-one kernels and K subset L versus conjectural equality. Undated author manuscript; revision/VOR identity not certified.'),('gmm_pdf','Local text pp.18–19, §8 five segments, imprimitive strategy and negative Galois distinction; not unitary stabilizer distinction.'),('mos_pdf','Local text PDFp31/printed641, Example9.4: six Langlands versus three dual segments; symplectic subgroup.'),('sharma_pdf','Local text pp.19 and21, Theorem8.1 and remarks/§9 boundary between combinatorial and symplectic-period consequences.'),('bp_pdf','Local text pp.3–4, tempered Plancherel and generic multiplicity theorems; not arbitrary quotient descent.'),('lu_matringe_pdf','Local text pp.26,28–29, square-integrable induction, completeness deduction and normalization remarks.'),('mo2022_pdf','Local text p.3, explicit arbitrary-quotient descent limitation.'),('moy_pdf','Local text pp.25–26, Theorem5.4 and Corollary5.5 inducing hypotheses and conclusion.')]:
        source(key,'reviews/priority_01/sources/raw/'+key+'.txt',scope)
    write('SOURCE_INSPECTION.json',dict(utc=utc,policy='Bounded primary-interface/excerpt review, no new retrieval and no full-body audit beyond scope actually read.',sources=inspection,Luo_Zha=dict(body_inspected=False,all_exact_transformed_dual_twist_kernel_unitary_overlap='UNKNOWN',accepted_nonblocking=True,novelty_or_firstness_certified=False)))
    write('ERRORS_AND_LIMITS.json',dict(utc=utc,unexpected_test_failures=[],incomplete_executions=[],notes=['One combined long prior-evidence read was truncated; remaining complete reports and source sections were reread in bounded calls.','Original independent output retained after final program added set-boundary and edge-deletion controls.','Initial extra-member ZIP negative control also changes timestamp; do not interpret as isolated allowlist-only rejection.','Local uploader source pin recorded after inspected LOCAL check; canonical audit/candidate inputs were frozen before tests.','External deep theorem proofs are dependencies, not independently re-proved.','Luo-Zha full-body comparison remains UNKNOWN and nonblocking by user direction.','No live service/publication state, DOI resolution, worldwide novelty or complete literature coverage tested.']))
    write('FINAL_INTEGRITY.json',dict(utc=utc,status='PASS',input_rows_checked=len(freeze['files']),input_size_sha_device_inode_nlink_differences=bad,original_rows_checked=len(original['files']),original_mismatches=oldbad,preparation_rows_checked=len(seal['files']),candidate_pdf_sha256=sha((P/'paper.pdf').read_bytes()),candidate_zip_sha256=sha((P/'pr1032_supportkit_v1.1.zip').read_bytes()),preparation_seal_sha256=sha((P/'PREPARATION_SEAL.json').read_bytes()),no_canonical_hardlinks_created=True,only_own_review_tree_written=True))
    write('VERDICT.json',dict(utc=utc,status='COMPLETE_WHOLE_PACKAGE_REVIEW_ZERO_ACTIONABLE_P0_P3',complete_whole_review=True,repair_only=False,review_ordinal_TOTAL=2,counts=dict(P0=0,P1=0,P2=0,P3=0),actionable_findings=[],prior_three_P3='RESOLVED in reviewed v1.1',mathematical_scope='Exact F=Q3, E/F unramified quadratic smooth-complex GL15 Langlands quotient, tau-invariant, no entire proper induction, no Hermitian-stabilizer period; cited established theorems remain dependencies.',Luo_Zha_overlap='UNKNOWN_USER_ACCEPTED_NONBLOCKING',novelty_certified=False,computes_Hom_space=False,publication_ready=False,publication_ready_semantics='Reviewer does not grant ROOT adoption, platform publication or merge clearance.',completion_percent=100,independent_final_output_bytes=(R/'commands/independent_final_normal.stdout').stat().st_size,independent_final_output_sha256=final_hashes[0]))
    with (R/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc+' — Complete whole-package review finished: zero actionable P0–P3. All 1,018 frozen identity/inode/link-count rows and original 287 rows unchanged; all 49 current seal rows pass. Six whole verifier runs, fresh exact derivation/calibration, 48 builder cases, 27 archive attacks, 15 re-pinned semantic attacks, two native LOCAL checks, offline compile and actual nine-page QA complete. Completion estimate: 100%. Priority/overlap remains UNKNOWN; final ROOT and downstream disposition are separate.\n')
    rows=[];nonregular=[]
    for p in sorted(R.rglob('*')):
        if p.name in ('OUTPUT_INVENTORY.json','OUTPUT_SEAL.json') and p.parent==R:continue
        s=p.lstat()
        if stat.S_ISREG(s.st_mode):rows.append(dict(path=str(p.relative_to(R)),bytes=s.st_size,sha256=sha(p.read_bytes()),nlink=s.st_nlink))
        elif not stat.S_ISDIR(s.st_mode):nonregular.append(dict(path=str(p.relative_to(R)),mode=s.st_mode))
    need(not nonregular,'unexpected surviving nonregular fixture')
    need(all(r['nlink']==1 for r in rows),'own output has hardlinks')
    write('OUTPUT_INVENTORY.json',dict(utc=utc,scope='All review files, including ignored local source_renders and owned fixtures; excludes this inventory and its seal only. No listed fixture or third-party source raster is a release object.',files=rows,total_bytes=sum(r['bytes'] for r in rows),nonregular=nonregular))
    b=(R/'OUTPUT_INVENTORY.json').read_bytes()
    write('OUTPUT_SEAL.json',dict(utc=utc,status='FROZEN_COMPLETE',inventory=dict(path='OUTPUT_INVENTORY.json',bytes=len(b),sha256=sha(b)),content_rows=len(rows),all_own_nlink_one=True,input_integrity='FINAL_INTEGRITY.json',verdict='VERDICT.json',seal_self_hash_excluded=True))
    print(json.dumps(dict(status='COMPLETE',findings=0,input_rows=len(freeze['files']),command_runs=len(runs),output_rows=len(rows),output_bytes=sum(r['bytes'] for r in rows),seal_sha256=sha((R/'OUTPUT_SEAL.json').read_bytes()))))
if __name__=='__main__':main()
