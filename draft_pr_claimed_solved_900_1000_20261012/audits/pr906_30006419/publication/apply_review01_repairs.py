"""Apply the two recorded review01 repairs while preserving sealed history."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

P = Path(__file__).resolve().parent
A = P.parent

def require(ok,message):
    if not ok: raise RuntimeError(message)

def change(path,old,new):
    text = path.read_text()
    require(text.count(old)==1,'Ambiguous replacement in '+str(path))
    path.write_text(text.replace(old,new))

def main():
    require((A/'reviews/full_package_01/RESULT.json').is_file(),'Reviewer01 must finish first')
    freeze = json.loads((P/'PREPUBLICATION_FREEZE.json').read_text())
    require(freeze['candidate_revision']==1,'Repair already applied or wrong revision')
    for name,r in freeze['files'].items():
        require(hashlib.sha256((P/name).read_bytes()).hexdigest()==r['sha256'],
                'Frozen candidate01 drift')
    now = datetime.now(timezone.utc).isoformat()
    family = A/'reviews/priority_family'
    old_manifest = json.loads((family/'MANIFEST.json').read_text())
    history = family/'history/initial_revision'
    require(not history.exists(),'Priority history collision')
    history.mkdir(parents=True)
    names = [r['path'] for r in old_manifest['public_files']]+['MANIFEST.json']
    for name in names: shutil.copyfile(family/name,history/name)
    correction = '''# Submission review corrections: PR906, candidate revision 2

R1 fixes one malformed Sacks–Uhlenbeck publisher link in active
`reviews/priority_family/CITATION_EVIDENCE.md`: `/p. 01` becomes `/p01`.
Reviewer01 confirmed HTTP404 for the malformed address and HTTP200 for the
correct record. The manuscript, citation graph, source manifest and earlier
source-access addendum already used the correct identifier.

R2 repairs the interpretation of the companion KS bound. After the global
stress argument establishes T(s)=0, the pointwise seminorm satisfies the
older Lytchak–Wenger SL(2)-minimality hypothesis. For J(A)=I(s composed with A),
convexity and differentiability give DJ(I)[D]=I(s)tr(D). If S is positive
symmetric with determinant one, J(S)>=J(I)+I(s)(tr(S)-2)>=J(I).
Right polar decomposition A=SR and circular rotation invariance give the
same bound for every A in SL(2). Conversely minimization there forces T=0.
The sharper classical pointwise KS bound therefore applies. The elementary
4+sqrt(17) proof is retained as a self-contained nonsharp proof; no new or
improved constant is claimed. The smooth compact Reshetnyak counterexample
and both written theorem conclusions are unchanged.

Root identified this attribution gap during the adversarial review, and
reviewer01 independently confirmed the argument. The primary source is the
author-hosted Lytchak–Wenger manuscript dated11September2015: Definition3.1,
Lemma3.1, and Section3.3 (printedpp12–14),
https://www.mi.uni-koeln.de/~alytchak/preprints/enarea.pdf . Its pointwise KS
constant is 2sqrt(2)+sqrt(6). This source and these locators were inspected
again; its body is not redistributed. No optimality or first-priority claim
is introduced by the repair.

The seven initial sealed priority artifacts are byte-preserved under
`reviews/priority_family/history/initial_revision/`. Active priority explanations,
paper, README and deposit metadata now state the derived SL(2) premise.
Earlier sealed mathematical/source reviews and root retrieval records retain
their original dated interpretations. This release correction supersedes any
suggestion in them that the older pointwise bound is inapplicable merely
because it was stated for SL(2)-minimal seminorms. It does not rewrite their
retrieved bytes, executed queries, evidence, or original independence.
Candidate01 is preserved under publication/history/candidate01, including its
PDF, archive and exact metadata. All30 original PR files and original2/5 remain
unchanged. Historical access gaps and unresolved first priority remain explicit.
'''
    (A/'PUBLICATION_REVIEW_CORRECTIONS.md').write_text('Updated '+now+'\n\n'+correction)
    change(family/'CITATION_EVIDENCE.md','https://annals.math.princeton.edu/1981/113-1/p. 01',
           'https://annals.math.princeton.edu/1981/113-1/p01')
    change(family/'CITATION_EVIDENCE.md',
           'This is a strong nearby antecedent, not an exact local fixed-trace sphere theorem.',
           'The sphere stress argument supplies its pointwise SL(2)-minimality premise by matrix convexity, so the sharper constant applies to the companion theorem; the global sphere argument is still required.')
    change(family/'CITATION_EVIDENCE.md',
           "Cite this framework for general energies and bounded-distortion minimizers; do not replace the candidate's stationarity hypothesis with it without another argument.",
           'Matrix convexity and right polar decomposition supply the stationarity-to-SL(2)-minimality argument once T(s)=0; the known sharper pointwise KS bound therefore applies. See PUBLICATION_REVIEW_CORRECTIONS.md at the package root.')
    change(family/'PRIORITY_AUDIT.md',
           'The authenticated prior literature supplies major components and stronger conclusions under different minimization or curvature hypotheses.',
           'The authenticated prior literature supplies major components. In particular, the companion stress-zero step implies SL(2)-minimality by matrix convexity, so the older sharper pointwise KS distortion bound applies; other cited conformality conclusions retain curvature hypotheses.')
    change(family/'PRIORITY_AUDIT.md',
           'The allowed reparametrizations can change the boundary trace. Local fixed-trace minimization is not that hypothesis.',
           'The map-level variational hypothesis differs, but global stress vanishing plus matrix convexity yields the pointwise SL(2)-minimality premise, so the sharper old bound applies.')
    change(family/'PRIORITY_AUDIT.md',
           'Pointwise SL(2)-minimality is not an assumption of either local theorem. It cannot simply be substituted for domain stationarity.',
           'In the KS companion it is a derived conclusion after stress vanishing: convexity of J(A)=I(s composed with A) and right polar decomposition prove it. The old pointwise bound is an applicable antecedent, not an excluded result.')
    change(family/'PRIORITY_AUDIT.md',
           'The older full-reparametrization theorem has a better constant, but it does not automatically establish B. Conversely, no claim that 4+sqrt(17) improves the existing SL(2)-minimal or Plateau constants is justified.',
           'After T(s)=0, convexity of J(A)=I(s composed with A) gives DJ(I)[D]=I(s)tr(D). For positive symmetric det-one S, J(S)>=J(I)+I(s)(tr(S)-2)>=J(I). Right polar decomposition extends this to all SL(2), so the established sharper pointwise bound does apply. The sphere stress argument supplies that premise; the elementary 4+sqrt(17) proof is retained only for a self-contained bound, not an improvement.')
    change(family/'PRIORITY_AUDIT.md',
           '| Treat a better old Q as a refutation or priority match for B | Excluded as direct implication | The better Q assumes all reparametrizations or SL(2)-minimality. A stationarity-to-minimality theorem would be an additional unsupported step unless separately proved/cited. |',
           '| Apply the sharper old pointwise Q after stress vanishing | Verified applicable antecedent | Matrix convexity and right polar decomposition prove that T(s)=0 supplies SL(2)-minimality. This sharpens the elementary bound; it does not by itself authenticate an earlier complete sphere proof or the negative Reshetnyak construction. |')
    for name in ['PRIORITY_AUDIT.md','CITATION_EVIDENCE.md']:
        with (family/name).open('a') as f:
            f.write('\nRelease revision '+now+': root repaired R1/R2 after reviewer01; the initial sealed report is in history/initial_revision. See package-root PUBLICATION_REVIEW_CORRECTIONS.md.\n')
    for name in ['SOURCE_MANIFEST.json','CITATION_GRAPH.json']:
        data = json.loads((family/name).read_text())
        data['release_interpretation_qualification'] = {'utc':now,
            'correction':'Package-root PUBLICATION_REVIEW_CORRECTIONS.md',
            'KS_pointwise_SL2_bounds':'Applicable after the stress-zero step by convexity and polar decomposition',
            'retrieval_bytes_queries_and_citation_edges_unchanged':True}
        (family/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    with (family/'RESEARCH_LOG.md').open('a') as f:
        f.write('\n'+now+' — Root release repair after reviewer01: R1 link and R2 derived SL(2) premise corrected; all initial sealed artifacts preserved. Assigned historical coverage estimate remains95%; no new query, first-priority assertion, or candidate proof change.\n')
    public = [*names[:-1],*['history/initial_revision/'+n for n in names]]
    new_manifest = {**old_manifest,'release_revision_at_utc':now,
                    'release_correction':'PUBLICATION_REVIEW_CORRECTIONS.md at package root',
                    'public_files':[{'path':n,'bytes':(family/n).stat().st_size,
                                     'sha256':hashlib.sha256((family/n).read_bytes()).hexdigest()}
                                    for n in public]}
    (family/'MANIFEST.json').write_text(json.dumps(new_manifest,indent=2)+'\n')
    change(P/'note.tex',
           'metric spaces. Classical ingredients are credited; first priority is not claimed.',
           "metric spaces; the sharper classical SL(2)-minimal bound also applies.\nClassical ingredients are credited; first priority is not claimed.")
    change(P/'note.tex',
           "The better KS bounds for SL(2)-minimal or Plateau-minimizing\nseminorms \\cite{lw} have a different variational hypothesis; our constant is\nnonsharp and no improvement or optimality is claimed.",
           r'''The older, sharper KS bound also applies here. Indeed,
$J(A)=I(s\circ A)$ is convex in the matrix $A$, and the angular identity gives
$DJ(I)[D]=T(s):D+I(s)\tr D$. Once $T(s)=0$, for any positive symmetric
$S$ with $\det S=1$ convexity and $\tr S\ge2$ imply
\[
 J(S)\ge J(I)+I(s)(\tr S-2)\ge J(I).
\]
Every $A\in SL(2)$ has right polar decomposition $A=SR$, with $R$ a rotation;
circular invariance gives $J(A)=J(S)$. Thus the balanced seminorm is
SL(2)-minimal. The pointwise Lytchak--Wenger bound
$2\sqrt2+\sqrt6$ applies \cite[Lemma~3.1 and \S3.3]{lw}.
We retain the elementary $4+\sqrt{17}$ proof for a self-contained bound;
no new, improved, or optimal distortion constant is claimed.''')
    change(P/'README.md',
           'bound `4 + sqrt(17)`. The energy and minimization class are essential.',
           'bound `4 + sqrt(17)`. Its stress-zero step implies pointwise SL(2)-minimality\nby matrix convexity, so the sharper established Lytchak–Wenger bound also\napplies. The elementary constant is retained for a self-contained proof, not\nas an improvement. The energy and minimization class are essential.')
    with (P/'README.md').open('a') as f:
        f.write('\nPUBLICATION_REVIEW_CORRECTIONS.md records reviewer01 repairs: the supporting\nSacks–Uhlenbeck link and the applicability of the older sharper KS bound.\nThe initial sealed priority review is preserved in its history/initial_revision.\nThis release correction qualifies any contrary historical interpretation in\nthe unchanged original packet or earlier sealed analytic reviews.\n')
    change(P/'build_package.py',
           "'ROOT_PRIORITY_QUERY_LOG.md']:",
           "'ROOT_PRIORITY_QUERY_LOG.md','PUBLICATION_REVIEW_CORRECTIONS.md']:")
    descriptor = json.loads((P/'zenodo-deposit.json').read_text())
    old = 'A separate angular-stress proof establishes the nonsharp distortion bound 4+sqrt(17) for locally Korevaar-Schoen-minimizing spheres into complete metric spaces.'
    require(descriptor['metadata']['description'].count(old)==1,'Metadata repair ambiguity')
    descriptor['metadata']['description'] = descriptor['metadata']['description'].replace(old,
        old+' Its stress-zero step implies pointwise SL(2)-minimality by matrix convexity, so the established sharper Lytchak-Wenger bound also applies. The elementary constant is retained for a self-contained proof; no improved bound is claimed.')
    (P/'zenodo-deposit.json').write_text(json.dumps(descriptor,indent=2)+'\n')
    print(json.dumps({'repairs':['R1 supporting link','R2 applicable classical SL2 bound'],
                      'initial_priority_artifacts_preserved':7,'original_PR_files_changed':0,
                      'next':'Compile, visually inspect, rebuild, replay, refreeze; metadata package hash must be updated.'},indent=2))

if __name__=='__main__':main()
