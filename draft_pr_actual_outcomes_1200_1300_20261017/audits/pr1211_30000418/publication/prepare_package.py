#!/usr/bin/env python3
"""Prepare the current corrected edition and portable verification contents."""
from pathlib import Path
import hashlib, json, shutil

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent
REPAIR = AUDIT / 'repairs'
PACKAGE = ROOT / 'verification'

def binding(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def save(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n')

def refresh_edition():
    names = ['ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCES.json','VERIFICATION.json']
    p=REPAIR/'PROOF.md'
    s=p.read_text().replace('Priority and publication review are pending; no current-openness or first-priority certificate is asserted.', 'The bounded priority audit supports a historical-counterexample note with explicit earlier general-graph attribution; historical priority and present openness remain unestablished. Preprint review/publication receipts are separate from this mathematical edition.')
    if '## Current priority context' not in s:
        s += '\n## Current priority context\n\nFiala and Škrekovski’s institutional 2001 preprint, *List Distance Labelings of Graphs* (KAM2001-530 / ITI2001-28), already gives an ordinary-five/list-greater-than-five cyclic graph in Fig.4 on printed14. That is earlier general-graph overlap, not a verified earlier tree resolution. The final2005 journal version has a different title and its full body was unavailable; content identity is not assumed. The known tree list upper bound is credited through Kohl to Voigt/Kohl–Schreyer–Tuza–Voigt (2005). Broad independent and skeptical source audits did not verify an earlier tree counterexample, but relevant inaccessible/unlocated sources remain. This is no certificate of novelty, first resolution or current openness. Detailed source and gap records accompany the preprint verification package.\n'
    p.write_text(s)
    p=REPAIR/'AUDIT.md';s=p.read_text()
    s=s.replace('This document does not claim a new mathematical execution or scholarly-source inspection during editorial preparation.', 'Historical checks described above retain their historical identity. Fresh17October2026 executions and primary-source inspections are separately recorded in VERIFICATION.json and SOURCES.json; they are not retroactive claims about the original audits.')
    if '## 12. Current bounded priority reconciliation' not in s:
        s += '\n## 12. Current bounded priority reconciliation\n\nThe independent and skeptical priority families froze before cross-comparison. Both verified the earlier Fiala–Škrekovski2001 Fig.4 cyclic five-list obstruction and independently checked all66 displayed-list spanning trees as feasible. This only excludes the immediate deletion transfer, not all historical transformations or other prior countertrees. They found no verified earlier tree resolution in inspected source portions, and expressly left historical priority and present openness unestablished. The final2005 Fiala paper, TCS2005 full body, Chen/Jonas theses and later planar sharpness sources remain material access/content gaps. The current publication scope is the exact counterexample to the printed historical equality, with known bounds and general-graph predecessors credited. No firstness, minimality, new-method or current-open-status claim follows. The separate supporting priority audit records the full bounded coverage and gaps.\n'
    p.write_text(s)
    p=REPAIR/'ACCEPTANCE.md';s=p.read_text()
    s=s.replace('Priority and publication gates are pending.', 'The bounded priority review accepts publication of the explicit historical counterexample with attribution and limits; historical priority and present openness remain unresolved. Publication and whole-package review receipts are maintained separately.')
    s=s.replace('later preprint/verification materials require\nseparate exact artifact bindings and fresh whole-package reviews.', 'the accompanying preprint and verification materials have separate exact artifact bindings and fresh whole-package review receipts.')
    p.write_text(s)
    p=REPAIR/'README.md';s=p.read_text().replace('Publication and\npriority acceptance remain pending;', 'The bounded priority review supports the attributed historical-counterexample framing;')
    s=s.replace('A new reproducible submission\npackage is a separate pending step;', 'The separate reproducible preprint verification package supplies executable checks;')
    p.write_text(s)
    p=REPAIR/'SOURCES.json';d=json.loads(p.read_text())
    d['priority_status']='Bounded independent and skeptical audits completed; explicit historical-counterexample framing with earlier general-graph attribution. Historical priority and present openness unestablished; relevant source-body access gaps remain.'
    d['priority_audits']={'independent':'priority/independent/REPORT.md','skeptical':'priority/adversary/REPORT.md','prior_general_graph':'Fiala–Škrekovski2001 KAM2001-530 / ITI2001-28, p14 Fig4; cyclic graph, not a tree','journal_version_identity':'2005 final title Generalized list T-colorings of cycles, DOI10.1016/j.dam.2004.11.005; full content not inspected, not equated with preprint','scope':'Supporting verification archive includes authored reports and code, not downloaded third-party source bodies.'}
    save(p,d)
    p=REPAIR/'VERIFICATION.json';d=json.loads(p.read_text())
    d['current_primary_replay']=json.loads((AUDIT/'verification_research/REPLAY_AND_CONTROLS.json').read_text())
    d['publication_review_status']='The mathematical edition has separate preprint/verification artifact bindings; publication and fresh whole-package review receipts are outside this immutable edition.'
    save(p,d)
    p=REPAIR/'ACCEPTANCE.json';d=json.loads(p.read_text())
    d['status']='MATHEMATICALLY_ACCEPTED_HISTORICAL_COUNTEREXAMPLE_WITH_PRIORITY_LIMITS'
    d['priority_gate']='bounded audit completed; earlier general-graph overlap credited; no historical priority/current-openness claim'
    d['publication_gate']='separate frozen preprint, verification, whole-package review and publication receipts'
    d['current_document_bindings']={n:binding(REPAIR/n) for n in ['PROOF.md','AUDIT.md','ACCEPTANCE.md']}
    save(p,d)
    save(REPAIR/'MANIFEST.json',{'schema':'tree-list-labeling-corrected-manifest-v1','problem_id':30000418,'members':names,'entries':[{'file':n,**binding(REPAIR/n)} for n in names if n!='MANIFEST.json'],'self_hash_excluded':'MANIFEST.json'})
    save(REPAIR/'CURRENT_EDITION_BINDINGS.json',{'schema':'tree-list-labeling-current-edition-bindings-v1','files':{n:binding(REPAIR/n) for n in names},'original_submission':'../SUBMITTED_SNAPSHOT.json','scope':'Current corrected mathematical edition; original submitted bytes preserved separately.'})
    return names

def main():
    names=refresh_edition()
    PACKAGE.mkdir(exist_ok=True)
    def copy(src,rel):
        dst=PACKAGE/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
    for n in names:copy(REPAIR/n,'corrected_edition/'+n)
    for n in ['specimen.json','verify.py','REPLAY_AND_CONTROLS.json']:
        copy(AUDIT/'verification_research'/n,n)
    copy(ROOT/'manuscript/main.tex','manuscript/main.tex')
    family=AUDIT/'reviews/input_reconstruction'
    for p in family.iterdir():
        if p.is_file():copy(p,'independent_family/'+p.name)
    for sub in ['independent','adversary']:
        folder=AUDIT/'priority'/sub
        for p in folder.iterdir():
            if p.is_file() and (p.suffix in {'.md','.json','.py','.jsonl'} or p.name in {'.gitignore','kstv2005_elsevier.xml'}):
                copy(p,'priority/'+sub+'/'+p.name)
    for n in ['REPORT.md','VERDICT.json','SOURCE_RECEIPTS.json','SOURCE_SCOPE_CHECK.json','BOUNDARY_CHECKS.json','INDEPENDENT_CHECKS.json']:
        copy(AUDIT/'reviews/proof_source_adversary'/n,'source_math_review/'+n)
    copy(AUDIT/'SUBMITTED_SNAPSHOT.json','provenance/SUBMITTED_SNAPSHOT.json')
    copy(AUDIT/'ROOT_INPUT_FAMILY_COMPARISON.json','provenance/ROOT_INPUT_FAMILY_COMPARISON.json')
    if (AUDIT/'PRIORITY_ADJUDICATION.json').exists():copy(AUDIT/'PRIORITY_ADJUDICATION.json','priority/PRIORITY_ADJUDICATION.json')
    print(json.dumps({'corrected_files':names,'package_files':sum(p.is_file() for p in PACKAGE.rglob('*'))}))

if __name__=='__main__':main()
