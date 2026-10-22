Updated 2026-10-14T03:51:52.926694+00:00

# Submission review corrections: PR906, candidate revision 2

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
Polar decomposition A=SR and circular rotation invariance give the
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

Reviewer01 optional clarity improvements were also applied: the KS coordinate
seminorm s_z is explicitly defined and this release presentation of the dated
source-access addendum is copy-edited, with the earlier wording preserved.
