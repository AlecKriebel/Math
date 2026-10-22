#!/usr/bin/env python3
"""Prepare the current mathematical edition and portable authored evidence."""
from pathlib import Path
import hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent
EDITION=AUDIT/'current_edition'
PACKAGE=ROOT/'verification'
NAMES=['ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCES.json','VERIFICATION.json']
def binding(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def copy(src,rel):
    dst=PACKAGE/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
def authored(folder):
    candidates=[p for p in folder.rglob('*') if p.is_file()]
    run=subprocess.run(['git','check-ignore','--no-index','-z','--stdin'],input=b'\0'.join(str(p).encode() for p in candidates)+b'\0',capture_output=True)
    if run.returncode not in (0,1):raise RuntimeError(run.stderr.decode())
    ignored=set(run.stdout.decode().split('\0'))
    return [p for p in candidates if str(p) not in ignored and (p.suffix in {'.md','.json','.jsonl','.py','.sha256'} or p.name in {'.gitignore','SHA256SUMS'})]
def main():
    priority=json.loads((AUDIT/'PRIORITY_ADJUDICATION.json').read_text())
    if priority['novelty_clearance'] or priority['firstness_claim'] or priority['current_openness_claim']:raise RuntimeError('Unexpected priority framing')
    EDITION.mkdir(exist_ok=True);PACKAGE.mkdir(exist_ok=True)
    (EDITION/'PROOF.md').write_text('''# Current accepted real-complement modulus theorem

For compact E contained in [0,1], F=R\\E within the real line and S2={|z|=2}, positive planar 2-modulus of the E-to-S2 family implies infinite 2-modulus of the E-to-F family. The full implication, including zero-length positive-capacity sets, passes fresh root and independent adversarial checks without mathematical repair. Curves are whole-plane endpoint connectors, with no extra interior-avoidance condition, and either globally rectifiable or locally rectifiable off endpoints with actual endpoint limits. Densities are extended nonnegative Borel functions admissible on every curve.

The original proof is retained verbatim below as a historical argument. Its original status, source-inspection and execution statements describe its own earlier preparation only; the current priority conclusion supersedes its historical priority language. The present note makes no firstness, new-mechanism or current-openness claim. Complete new source-question Riesz and classical compact-exhaustion deductions, their distinct adversarial checks, and the scoped energy argument are supplied separately in the verification archive. The paper gives the complete direct proof.

## Immutable original argument, reproduced verbatim

'''+(AUDIT/'submitted/PROOF.md').read_text())
    (EDITION/'AUDIT.md').write_text('''# Current mathematical and priority audit

The original proof and exact historical source question were reviewed in full. The weighted metric uses a pointwise lower-semicontinuous L2 majorant, actual all-point endpoint values and actual ACL slices. Critical H1/2 trace rigidity forces zero real length; it does not by itself force capacity zero. For every hypothetical finite augmented-cost outer connector, first exit followed by small circular arcs contradicts all-curves admissibility. The resulting infinite-cost density scaled to arbitrarily small energy is admissible for the entire outer family. No pointwise-to-almost-everywhere substitution, touching-condenser identity, or unsupported quasicontinuous boundary restriction occurs.

A source-question-only family supplied a materially distinct complete Riesz-potential/polygon-averaging reconstruction. A new adversary checked every estimate and both endpoint conventions. Initial input independence and its limits are recorded in preserved freezes. Two initially separate priority families then investigated direct historical sources and indirect classical implications, froze before comparison, and performed reverse challenges. A fresh additional verifier independently checked the full compact-exhaustion/Sobolev-capacity deduction. The logarithmic-energy deduction is independently validated for the zero-length branch and outer finite-energy bridge; its positive-length reduction is imported from a separately validated trace argument. No mathematical repair was required to the submitted theorem.

Classical general-theory foundations overlap substantially with the result. A complete deduction assembled during this2026 audit is not evidence of an earlier explicitly printed resolution. Firstness, a new mechanism and worldwide current openness are unestablished and not claimed. The2018 target is authenticated; the full2019 page, a Goldstein–Jackson1982 abstract/body, and final2011 body matching for an internally dated2010 draft remain unresolved source limits. Partial primary preview wording is not completed. Detailed receipts and adjudication govern the exact scope.

All old submission files and original Git identities remain separately frozen. New analytic reviews and source inspections are new acts; unavailable historical execution/source bodies are not retroactively authenticated. There is no numerical or formal-proof certificate of the analytic theorem. The portable executable verifies byte bindings, original Git objects and authored nested freezes; external third-party bodies are omitted and their inventories are receipt-only.

AI tools were used extensively. This is an internal adversarial audit, unrefereed and without external human peer review or formal proof-assistant certification. Sequential whole-package reviews and publication receipts are separate later gates.
''')
    (EDITION/'README.md').write_text('''# Problem2307058 / Hayman–Lingham7.58

Accepted: the full real-complement modulus implication in the authenticated2018 formulation, for all compact E contained in [0,1]. The original proof requires no mathematical repair. The current paper gives a complete direct proof; supplementary written derivations supply distinct Riesz-potential and classical compact-exhaustion routes, with independent scoped adversarial checks.

The original PR explicitly claimed a full solution and was eligible under the actual-outcome gate because QUEUE.md may be stale. Current acceptance does not assert firstness, a new mechanism or current worldwide openness. Two bounded initially independent priority searches and reverse challenges credit classical foundations and distinguish newly assembled deductions from authenticated earlier printed resolutions. Source-access limits remain explicit.

PROOF.md retains the original argument with a current framing prefix. AUDIT.md, SOURCES.json, VERIFICATION.json and ACCEPTANCE records describe the fresh audit. MANIFEST.json binds the other seven current files. Original submitted files and Git identities are separately preserved, not silently rewritten. The preprint/archive and publication receipts accompany this edition in publication_20261017 after the separate publication gates pass.

AI tools were used extensively in research, proof development, literature review, internal independent/adversarial verification and writing. Unrefereed; no external human peer review, journal acceptance or formal proof-assistant certification is claimed.
''')
    (EDITION/'ACCEPTANCE.md').write_text('''# Current acceptance

ACCEPT full historical implication: M2(E,S2)>0 implies M2(E,R\\E)=infinity for every compact E contained in [0,1]. Densities are pointwise extended Borel and admissible for every connector in either stated whole-plane curve convention. Zero-length positive-capacity cases are covered. No mathematical repair to the original proof was necessary.

Substantial classical foundations and new2026 deductions from older general theory are credited. No earlier explicitly printed resolution was authenticated; this is not a certificate that none exists. No firstness, new mechanism, new existence priority or current-openness claim is made. Full2019 wording and an1982 talk body remain unavailable. Draft numbering is distinguished from unmatched final-book numbering.

Original argument, source-question-only reconstruction, distinct Riesz adversary, two initially independent priority families, reverse challenges and an additional fresh full classical-corollary verifier pass within their documented scopes. This is internal extensively AI-assisted research, unrefereed; no external human peer review or formal proof-assistant certification. Exact preprint whole-package reviews, upload and merge are separate gates.
''')
    save(EDITION/'SOURCES.json',{'schema':'real-complement-current-sources-v1','problem_id':2307058,'historical_submitted_source_record':json.loads((AUDIT/'submitted/SOURCES.json').read_text()),'current_original_question_source':json.loads((AUDIT/'ROOT_SOURCE_RECEIPT.json').read_text()),'current_priority_source_scope':json.loads((AUDIT/'ROOT_PRIORITY_SOURCE_SCOPE.json').read_text()),'priority_adjudication':priority,'distribution':'Authored receipts only; third-party source bodies are not included. Historical source records retain their historical scope.'})
    save(EDITION/'VERIFICATION.json',{'schema':'real-complement-current-verification-v1','problem_id':2307058,'historical_submitted_record':json.loads((AUDIT/'submitted/VERIFICATION.json').read_text()),'current_math_gate':json.loads((AUDIT/'MATH_GATE.json').read_text()),'current_classical_cross_gate':json.loads((AUDIT/'CLASSICAL_CROSS_GATE_PROGRESS.json').read_text()),'current_analytic_checks':'Written derivations and adversarial proofs, not numerical experiments. Independent Riesz and classical capacity routes are included in the archive.','portable_replay':'Byte integrity, exact original Git blob identities and all authored nested freeze members. No numerical certification of analytic conclusions or reauthentication of omitted external source bodies.','historical_limit':'No claim to replay unavailable original execution bodies or authenticate every historical inspection.'})
    save(EDITION/'ACCEPTANCE.json',{'schema':'real-complement-current-acceptance-v1','problem_id':2307058,'status':'ACCEPT_FULL_HISTORICAL_IMPLICATION','original_head':'dc7ea7f23e7887a70e689f7f9280c9cb0819702e','mathematical_repairs':[],'all_compact_E':True,'zero_length_positive_capacity_cases':True,'all_curves_both_stated_conventions':True,'priority_clearance':False,'firstness_or_current_openness_claim':False,'AI_use':'extensive; unrefereed, no external human peer review/formal certification','current_document_bindings':{n:binding(EDITION/n) for n in ['PROOF.md','AUDIT.md','ACCEPTANCE.md']},'publication_gate':'Separate exact PDF/archive and sequential fresh whole-package review/publication receipts'})
    save(EDITION/'MANIFEST.json',{'schema':'real-complement-current-edition-manifest-v1','members':NAMES,'entries':[{'file':n,**binding(EDITION/n)} for n in NAMES if n!='MANIFEST.json'],'self_hash_excluded':'MANIFEST.json'})
    for n in NAMES:copy(EDITION/n,'current_edition/'+n);copy(AUDIT/'submitted'/n,'original_submitted/'+n)
    for p in sorted(AUDIT.iterdir()):
        if p.is_file() and p.suffix in {'.md','.json'} and p.name!='RESEARCH_LOG.md':copy(p,'provenance/'+p.name)
    for family in ['analytic_adversary','source_question_family','riesz_route_adversary']:
        for p in authored(AUDIT/'reviews'/family):copy(p,'reviews/'+family+'/'+p.relative_to(AUDIT/'reviews'/family).as_posix())
    for p in authored(AUDIT/'priority'):copy(p,'priority/'+p.relative_to(AUDIT/'priority').as_posix())
    copy(ROOT/'manuscript/main.tex','manuscript/main.tex')
    copy(ROOT/'BIBLIOGRAPHY_QA.json','provenance/BIBLIOGRAPHY_QA.json')
    print(json.dumps({'current_edition_files':8,'portable_files':sum(p.is_file() for p in PACKAGE.rglob('*')),'scope':'Authored research files only; external source bodies omitted.'}))
if __name__=='__main__':main()
