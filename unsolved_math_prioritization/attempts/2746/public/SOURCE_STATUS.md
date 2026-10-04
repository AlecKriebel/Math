# Source, version, literature, and duplicate checks

Checked 2026-10-04 UTC. Searches establish what was found, not the absence of
all possible later or unindexed work. No full resolution was verified.

## Exact statement

The initial catalogue URL was https://www.unsolvedmath.com/problems/2746 .
The web reader could not access it; an ordinary GET returned HTTP 403 and a
59-byte response. This is disclosed rather than treated as a successful live
catalogue read.

The pinned imported record has ID 2746, code KP-1.87, title “Kirby Problem
1.87”, and asks whether every fibered link in S³ is realized as the link of
an isolated singular point of a polynomial R⁴→R² map. Its generated
2026-08-17 literature triage is only background. The source statement was
checked directly against K3 and its cited original paper.

K3 is the **new 2026 list**, not an attribution of this problem number to
Kirby's 1995 list. In the accessible author's preliminary version, Problem
1.87 occupies printed/PDF pages 78–79 and is proposed/scribed by O. Saeki.
The exact question appears on page 78; remarks separate weak from genuine
isolation. The PDF has 436 pages, metadata creation 2026-04-01 and last
modification 2026-04-15. No assertion that this pagination equals the final
published book's pagination is made. Page 78 was inspected visually as well
as through text extraction.

- R. İ. Baykur, R. C. Kirby, D. Ruberman, *K3: A New Problem List in
  Low-Dimensional Topology*, Problem 1.87:
  https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- R. Benedetti and M. Shiota, *On real algebraic links in S³*, Bollettino UMI
  (8) 1-B (1998), 585–609. Original Conjecture 1.6, p. 588; definitions on
  p. 585; Theorems 1.7–1.8 and the blow-down gap on pp. 588–589:
  https://people.dm.unipi.it/benedett/BUMI_Shiota.pdf
  Bibliographic record: https://www.bdim.eu/item?id=BUMI_1998_8_1B_3_585_0

The original distinguishes maps analytic at 0 from tame maps and analyticity
after blow-up. This matters: finite-sufficiency does not apply merely because
a pullback to the resolved space is analytic.

## Current primary developments inspected

1. B. Bode, *Closures of T-homogeneous braids are real algebraic*, Algebraic &
   Geometric Topology 25 (2025), 1075–1115; published 2025-05-16. Theorem 1.2
   realizes T-homogeneous closures; Corollary 1.3 covers homogeneous closures.
   Theorem 1.1 uses an odd, pure Rampichini diagram and inserted inner loops.
   It is not a theorem for every fibered link. The introduction still labels
   the universal statement a conjecture.
   https://doi.org/10.2140/agt.2025.25.1075
   https://msp.org/agt/2025/25-2/agt-v25-n2-p11-p.pdf

2. B. Bode, *Links of Inner Non-degenerate Mixed Functions, Part II*, Bulletin
   of the Brazilian Mathematical Society 56, article 55 (2025), published
   2025-10-08. The **published** Example 4.11 and text following Lemma 6.3
   exclude 8₁₆ from the stated convenient nondegenerate Γ-nice class. The
   preprint arXiv:2307.15340v2, dated 2023-10-18, numbers the corresponding
   example 3.10 and lemma 5.4. Our final citations use published numbering.
   The paper distinguishes weak from strong inner nondegeneracy; its
   classification is not a classification of all isolated polynomial germs.
   https://doi.org/10.1007/s00574-025-00477-0
   https://link.springer.com/content/pdf/10.1007/s00574-025-00477-0.pdf

3. B. Bode and C.-S. Hsueh, *Mutual arc presentations and braided open books*,
   arXiv:2511.21837v1, 2025-11-26. Theorem 1.3 gives the relevant property for
   canonically fibered links. Conjecture B is the assertion that every fibered
   link has a P-fibered braid representative. Theorem 1.1 recalls universal
   Hopf plumbing **and deplumbing**. None gives a universal real-polynomial
   realization. https://arxiv.org/abs/2511.21837v1

4. B. Bode and P. Truöl, *On T-positive links*, arXiv:2605.10502v1,
   2026-05-11. Theorem 1.1 identifies T-positive links with the strongly
   quasipositive T-homogeneous links. This refines an already known positive
   class, rather than proving all fibered links are T-homogeneous or real
   algebraic. https://arxiv.org/abs/2605.10502v1

5. R. N. Araújo dos Santos, B. Bode, T. de Paiva and E. L. Sanchez Quiceno,
   *Essential tori associated with links of mixed singularities*,
   arXiv:2604.25517v2, revised 2026-07-29. It studies topological consequences
   of **weakly isolated**, convenient, nondegenerate, Γ-nice mixed
   singularities. Its essential-torus criteria do not supply the missing
   universal isolated realization. https://arxiv.org/abs/2604.25517v2

The author's current publication list was also inspected to find newer
versions: https://sites.google.com/view/benjaminbode/research . Targeted
searches used the problem number, “every fibered link real algebraic”,
“Benedetti Shiota conjecture solved”, and 2025/2026 variants. No announcement
claiming a full resolution was located in the primary works inspected.
This limited negative finding is not a proof of openness.

## Credited dependencies versus independent calculations

- Source inputs: Milnor's link/cone facts; analytic Łojasiewicz lower bounds;
  the knot 8₁₆'s Alexander polynomial and fibering; the Murasugi and Hartley
  periodicity conditions as stated by Bode; Bode's Newton-class theorem.
- Reconstructed proofs: flat smooth cone rank calculation; an explicit
  finite-jet transfer under analytic and transverse hypotheses; symbolic
  same-unknot weak/isolated controls; a Fourier parity sufficient criterion;
  exact mod-2 and mod-4 arithmetic of the symmetry obstruction.
- The published source used a computer irreducibility test for Δ(t²). This
  packet instead proves that the required q(t)q(−t) factorization is impossible
  by its middle coefficient modulo 4. It does not silently claim to have
  reverified that stronger irreducibility assertion.

## Live repository gate

Repository: https://github.com/AlecKriebel/Math . The read-only gate used main
commit `25aaa7146e257ef5276e80aae60429cf3f4765f9` observed 2026-10-04.
Repository AGENTS.md and queue AGENTS.md/README.md were read at that commit.

- Queue row: rank 592, ID 2746 / KP-1.87, queued, 0/5.
- No state entry keyed 2746.
- `unsolved_math_prioritization/attempts/2746` and `problems/2746` returned 404.
- Exact numeric-ID code, PR, and branch searches returned no matches.
- A code search for “real algebraic” with “fibered” returned no matches.
- A broader Benedetti/Shiota/Kirby PR search returned unrelated PRs 54 and
  267; their problem IDs and subjects are different.
- The related-target groups file did not contain 2746.
- The historical individual review in `review_v2/reviews_5.json` suggested
  polynomial approximation of open books but identified isolated criticality
  as the obstacle. It is a heuristic, not a certificate. No readiness hold was
  stated in that review. No matching prior mathematical report was found in
  the pinned research-results corpus under ID/code or the distinctive phrase.

These checks cannot exclude differently named/unindexed branches, private
work, or all semantically related efforts. They provide no evidence of a
duplicate exact attempt, so the five-family investigation proceeded. No
repository mutation occurred in this worker.

## Pinned bytes (SHA-256)

The full imported corpora and source PDFs are private reading material and
are not included in the publication packet. Hashes permit checking exact
versions without republishing them.

- imported problems.json:
  04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf
- imported research_results.json:
  8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b
- K3 preliminary PDF:
  ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f
- Benedetti–Shiota 1998 PDF:
  01218f44e287e58dd764389f2693b79b8a14f1f1d2a1fe9b06f3785fe9287d27
- Bode T-homogeneous published PDF:
  e1ad14c76bb5650e99ed857905e94e6ddbdc4a5f211ab55bd1d52e755c73c5d9
- Bode Part II published PDF:
  08fae907e331cff185a8449ecb369a9b3cc8c0f1eb89f70d8e8358af16eca63e
- Bode Part II arXiv v2 PDF (2023 numbering):
  a1ca4dbffab19ebc4979300f9ca07d29bd470b4b016fabc86114d73acf07e1a4
- Bode–Hsueh v1 PDF:
  af054ea7d37a0839126e2083cf9686ebda418e7a6ae5e71ba7c15f7ff94d1b06
- Bode–Truöl v1 PDF:
  fdccae6124c88871fb600ee9f4d92d70d170d269ef91e95c7fe55a7ce3473971
- Essential-tori v2 PDF:
  36f98a58beee66677f2c747faa29c78d02e60b3cde1da484ecb1ccd03acccbbc

The K3 notice expressly prohibits reposting the preliminary version without
permission. It was used for private scholarly verification only.
