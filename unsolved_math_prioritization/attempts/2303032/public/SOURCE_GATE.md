# Source, identity, status, and duplication gate

Checked 2026-10-04 UTC.

## Exact identity

The starting catalogue URL was
https://www.unsolvedmath.com/problems/2303032 . The web fetch was unavailable;
a direct header check returned HTTP 403 (Vercel mitigation). No attempt was
made to defeat it. Identity was recovered from the pinned upstream dataset
revision 372682f27c1b0d3d39e75fa63ad7932c7a2e1bde, numeric ID 2303032, code
AMR-022-3032, and verified against Hayman--Lingham, arXiv:1809.07200v2,
printed p.70 (PDF page 71). The complete target was read.

The imported report called the sharp threshold open and stated that no
resolution was located. It supplied no proof or obstruction. That report is
not authoritative: the cited collection's own Update 3.32 points to Aikawa,
and Aikawa's 1994 Section 4 expressly connects Corollary 6 to this problem.
The paper's bibliographic identity is independently confirmed by the author's
publication list. The 2019 article restates the bound and its proof.

## Parameter and transcription corrections

- Use theta for the geometric half-angle and a=a_n(theta) for the cone's
  positive harmonic degree. The collection's update overloads alpha.
- The correct second entry is 1/(a-1), positive for a>1. The 1994 author
  manuscript's piecewise explanatory display prints 1/(1-alpha) in its
  alpha>2 branch. This contradicts the preceding theorem and is a sign typo;
  the 2019 Theorem 1.7 gives the correct expression.
- The dimensionally correct Whitney exponent is n/p-n, not the anomalous
  exponent printed in the 1994 manuscript's abbreviated Lemma 3 argument.
  The 2019 proof and the derivation in PROOF.md establish the correct scaling.
- The angle for barrier order two satisfies cos(theta)=1/sqrt(n), hence
  k=cot(theta)=1/sqrt(n-1). This follows from an explicit harmonic quadratic.

The problematic displays and theorem statements were checked visually in
rendered source pages, rather than trusting extraction alone.

## Later literature and verification limit

Author-hosted 1994, 1998, 2000 and 2019 papers were retrieved. The 1998 and
2000 introductions and the 2019 exposition attribute a sharp Lipschitz
integrability exponent to the 1994 work. The relevant modern source is
2019 Theorem 1.7 and its proof; the 1998 Lemma 15 also checks the general
interior-cone Green lower bound.

The proof reconstructed here establishes the entire displayed sufficient
range. Cone harmonic functions give matching nonintegrability for a<=2.
For a>2, the published sharpness assertion is a cited historical conclusion,
not an independently reconstructed counterexample in this dossier. The
1996 monograph, DOI 10.1007/BFb0093410, has a pertinent Section II.9.5;
the publisher route returned a subscription-preview HTML page rather than
the PDF. It was not treated as retrieved full text. The checked AMS PDF route
for the 1994 version of record was unavailable; the author manuscript and
later author exposition were used instead. No access restriction was bypassed.

Recommendation: **already_solved**, explicitly at theorem-level historical
provenance. This recommendation is not a claim that every sharpness detail
has been independently reconstructed. If a policy requires full independent
reconstruction before that label, the outstanding review condition is
precisely the a>2 optimality/endpoint construction; the sufficient theorem
is not the outstanding condition. No new-solution claim is justified.

## Repository duplicate check

Live main was inspected at commit
bd5c59ad2b9f2c57c82aa1fe7b0466fe3ea92e1b. Its queue row was rank 573,
queued, 0/5. No 2303032 key occurred in the fetched state; the attempts
directory listing contained no 2303032 directory (direct request: 404).
The related-target grouping contained no entry for this numeric ID.
GitHub PR searches for the numeric ID, AMR-022-3032, the Function Theory
3.32 title, Aikawa, and superharmonic returned no matches. Default-branch
connector code search for the ID returned no results; direct queue inspection
was therefore also used and is the authoritative positive identity check.
These are scoped checks, not an assertion that no unindexed branch could
contain related material.

Aikawa also names Problem 3.34, which is a genuinely related formulation
about interior cones. That row is not changed by this dossier. Its more
general geometric assumptions must be separately checked before any update.

No remote repository writes were performed during this investigation.
Only this target's Status and Turns are proposed for queue changes. Public
files exclude source PDFs, imported corpora, access-page HTML, and private
coordination material. Source digests and bibliographic citations are public.
