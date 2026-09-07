#!/usr/bin/env python3
"""Controlled scratch-only release gate and preflight negative controls."""
import datetime,hashlib,json,os,pathlib,shutil,subprocess,sys
from audit_driver import HERE,SOURCE,SCRATCH,LOGS,ENV,run

def hash_tree(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
def fresh(name,source=SOURCE):
    dst=SCRATCH/name
    if dst.exists():shutil.rmtree(dst)
    shutil.copytree(source,dst)
    return dst
results=[]
def record(name,**kwargs):
    results.append(dict(name=name,**kwargs))

kind=sys.argv[1]
if kind=='preflight':
    d=fresh('negative_preflight')
    (d/'release/replay.log').write_text('REFEREE-ARCHIVED-SUCCESS-SENTINEL\n')
    before=hash_tree(d)
    e=ENV.copy();e['TOOLCHAIN_LOCK_FILE']=str(SCRATCH/'invalid_toolchain.lock')
    lock=(SOURCE/'environment/texlive-2022.04.lock.txt').read_text()
    (SCRATCH/'invalid_toolchain.lock').write_text(lock.replace('pdfTeX','INVALID-pdfTeX',1))
    status=run('refresh_wrong_toolchain',['bash','release/refresh_packages.sh'],d,expected=2,env=e)
    assert status!=0 and before==hash_tree(d)
    record('refresh_wrong_toolchain',status=status,tree_unchanged=True)
    e=ENV.copy();e['FROZEN_BASE']=str(SCRATCH/'absent_archives')
    status=run('historical_lineage_unavailable',['bash','release/one_command_replay.sh'],d,expected=2,env=e)
    after=hash_tree(d)
    assert status==2 and before==after
    assert (LOGS/'historical_lineage_unavailable.log').read_text().count('MISSING ')==5
    record('historical_lineage_unavailable',status=status,missing_archives=5,tree_unchanged=True)
    d=fresh('negative_manifest',SOURCE/'public/repository')
    target=d/'data/current_profile_exact.json'; target.write_text(target.read_text()+'\n')
    before=hash_tree(d)
    status=run('portable_baseline_mutation',['bash','replay.sh'],d,expected=1)
    assert status!=0 and before==hash_tree(d)
    record('portable_baseline_mutation',status=status,tree_unchanged=True)
    d=fresh('negative_self_manifest',SOURCE/'public/repository')
    target=d/'data/current_profile_exact.json';target.write_text(target.read_text()+'\n')
    manifest=d/'verification_outputs/replay_self_consistency_manifest.txt'
    manifest.write_text(hashlib.sha256(target.read_bytes()).hexdigest()+'  ./data/current_profile_exact.json\n')
    before=hash_tree(d)
    status=run('portable_forged_self_manifest',['bash','replay.sh'],d,expected=1)
    assert status!=0 and before==hash_tree(d)
    record('portable_forged_self_manifest',status=status,tree_unchanged=True)
elif kind=='canonical_warning':
    d=fresh('negative_canonical_warning')
    p=d/'manuscript/main.tex';s=p.read_text();s=s.replace(r'\begin{document}',r'\begin{document}'+'\n'+r'\noindent\hbox to 600pt{\hfil REFEREE OVERFLOW}\par',1);p.write_text(s)
    baseline=(d/'release/BUNDLE_SHA256.txt').read_bytes()
    status=run('refresh_canonical_overfull',['bash','release/refresh_packages.sh'],d,expected=1)
    assert status!=0
    assert 'document log audit failed:' in (LOGS/'refresh_canonical_overfull.log').read_text()
    assert baseline==(d/'release/BUNDLE_SHA256.txt').read_bytes()
    record('canonical_overfull',status=status,bundles_unchanged=True)
elif kind=='journal_warning':
    d=fresh('negative_journal_warning')
    p=d/'manuscript/main.tex';s=p.read_text();s=s.replace(r'\noindent\textbf{Keywords:}',r'\noindent\textbf{Keywords:}'+r'\ifsiadsreview\smash{\hbox to 0pt{\hskip 430pt REFEREE OVERFLOW}}\fi',1);p.write_text(s)
    status=run('refresh_journal_overfull',['bash','release/refresh_packages.sh'],d,expected=0)
    record('journal_overfull',status=status)
    if status==0:
        confirmation=SCRATCH/'journal_warning_rebuild'
        if confirmation.exists():shutil.rmtree(confirmation)
        shutil.copytree(d/'submission/journal/source',confirmation)
        commands=[['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],['biber','main']]+[['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex']]*2
        for i,args in enumerate(commands):assert run('journal_warning_confirmation_'+str(i),args,confirmation)==0
        final_log=(confirmation/'main.log').read_text()
        warnings=[line for line in final_log.splitlines() if 'Overfull' in line]
        assert warnings
        (LOGS/'journal_warning_main.log').write_text(final_log)
        reference=d/'submission/journal/manuscript.pdf'
        assert subprocess.check_output(['pdftotext','-layout',str(confirmation/'main.pdf'),'-'],env=ENV)==subprocess.check_output(['pdftotext','-layout',str(reference),'-'],env=ENV)
        witness=dict(warning_lines=warnings,mutation=r'After Keywords insert \ifsiadsreview\smash{\hbox to 0pt{\hskip 430pt REFEREE OVERFLOW}}\fi',refresh_status=0,journal_pdf_gate_status=0,mutant_pdf_sha256=hashlib.sha256(reference.read_bytes()).hexdigest(),reproduced_from_sealed_journal_bundle=True,classification='journal layout and warning gate gap; canonical preprint unaffected')
        (HERE/'JOURNAL_WARNING_WITNESS.json').write_text(json.dumps(witness,indent=2)+'\n')
elif kind=='fresh_evidence':
    d=fresh('negative_stale_pdf_evidence')
    for rel in ['manuscript/main.pdf','manuscript/supplement.pdf','external_audit/theorem_summary.pdf','external_audit/proof_skeleton.pdf','submission/journal/manuscript.pdf','submission/journal/supplement.pdf','submission/journal/cover_letter_SIADS.pdf']:
        (d/rel).write_bytes(b'REFEREE-STALE-INVALID-PDF')
    for f in (d/'release/pdf_preflight').glob('*.txt'):f.write_text('REFEREE-STALE-PDF-EVIDENCE\n')
    for name in ['pdf_semantic_audit.txt','journal_pdf_semantic_audit.txt']:
        (d/'release/verification_outputs'/name).write_text('REFEREE-STALE-PDF-EVIDENCE\n')
    status=run('refresh_stale_pdf_evidence',['bash','release/refresh_packages.sh'],d)
    assert status==0
    for f in (d/'release/pdf_preflight').glob('*.txt'):assert b'REFEREE-STALE' not in f.read_bytes()
    for name in ['pdf_semantic_audit.txt','journal_pdf_semantic_audit.txt']:
        assert (d/'release/verification_outputs'/name).read_bytes()==(SOURCE/'release/verification_outputs'/name).read_bytes()
    for line in (SOURCE/'release/BUNDLE_SHA256.txt').read_text().splitlines():
        digest,rel=line.split(None,1);assert hashlib.sha256((d/rel).read_bytes()).hexdigest()==digest
    record('fresh_pdf_evidence',status=status,sealed_bundles_match_release=True,stale_pdfs_replaced=7)
(HERE/(kind+'_controls.json')).write_text(json.dumps(results,indent=2)+'\n')
print(kind+'_CONTROLS_DONE')
