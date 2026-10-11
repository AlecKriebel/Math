# Source and priority audit

Checked 2026-09-30. Source triage is distinct from the proof attempt below.

## Exact original target

The pinned source record is UnsolvedMath 30001696, OWR-4798-013, with a unique
join by that problem code in the supplied dataset. The full Oberwolfach
contribution by Steven Klee (joint work with Isabella Novik), pp. 370–372
of Report 08/2011, was read. Its Question 4 on p. 372 asks whether B(i,d)
is a combinatorial triangulation of the sphere–ball product. The facets
are precisely the sign words with at most i switches. A boundary sphere
product or the homology/homotopy type alone would not answer the question.

The proof gives a semialgebraic homeomorphism of the entire realization
with the product and then applies the compact semialgebraic
Hauptvermutung. This supplies the PL conclusion in all dimensions in the
question, including i=0 and the codimension-one ball factor. The whole
cross-polytope boundary i=d-1 is a separate immediate endpoint.

Original source: https://doi.org/10.4171/owr/2011/08
Full PDF: https://publications.mfo.de/bitstream/handle/mfo/3223/OWR_2011_08.pdf?isAllowed=y&sequence=1

## Previously known ingredients and related work

1. Klee–Novik, *Centrally symmetric manifolds with few vertices*,
   arXiv:1102.0542, Indiana Univ. Math. J. 61 (2012), already establish the
   manifold, homology, boundary-product assertions and the ball-product
   cases i=0,1. The full paper and the author's final-version link were
   checked: https://sites.math.washington.edu/~novik/publications/sphere-products.pdf
2. Schwarz, *Totally positive differential systems*, Pacific J. Math.
   32 (1970), 203–229, Theorems 3–4, is the classical tridiagonal-flow
   source. The proof also derives strict positivity of the exponential
   through connected additive compounds rather than asserting it.
   https://msp.org/pjm/1970/32-1/pjm-v32-n1-p20-s.pdf
3. Margaliot–Sontag, *Revisiting totally positive differential systems*,
   Automatica 101 (2019), 1–14, Theorem 3, explicitly states the needed
   strong inequality `s^+(Ax) ≤ s^-(x)` for strictly totally positive A
   and every nonzero x. The plus/minus convention at zeros is essential.
   https://www.sontaglab.org/FTPDIR/margaliot_sontag_totally_positive_automatica2019.pdf
4. Hardt–Lambrechts–Turchin–Volić, *Real homotopy theory of semi-algebraic
   sets*, AGT 11 (2011), 2477–2545, Theorem 2.6, states the compact
   semialgebraic Hauptvermutung and cites Shiota–Yokoi (1984), Corollary
   4.3. The theorem as stated in the former paper was checked; the latter
   original corollary was not independently rederived.
   https://arxiv.org/abs/0806.0476
5. Galashin–Karp–Lam, *The totally nonnegative Grassmannian is a ball*,
   arXiv:1707.02010, Lemma 2.3, uses a contractive-flow method in positive
   geometry. No originality claim is made for the general flow idea.
   https://arxiv.org/abs/1707.02010
6. Machacek, *Boundary measurement and sign variation in real projective
   space*, Ann. Inst. H. Poincaré D 9 (2022), 543–565. The final journal
   text was checked, particularly Theorem 3.4 (manifold) and Theorem 3.6
   (homotopy type of the projective quotient). These do not themselves
   state the full sphere–ball homeomorphism of the double cover.
   https://ems.press/journals/aihpd/articles/8736466
   https://ems.press/content/serial-article-files/39446

## Prior-attempt gate

Before proof work, repository searches by numeric ID, OWR code, and
ball-product/B(i,d) wording found no earlier attempt or pull request.
The branch search found no existing problem branch. The queued source row
was rank 36 with 0/5 attempts. The pinned prior-report dataset has no
report for this problem code; the related-target groups contained no
entry for this numeric ID. Readiness notes, not proof certificates, were
read from the repository shortlist. The all-state PR search was repeated
on 2026-09-30 at 04:36 UTC and was empty.

The source datasets are pinned at repository revision
`37e53eabe540fb458758e198be61634bd02ee008`. The parent verified their
full hashes against the repository manifest. This attempt preserves its
individual source record and does not edit the shared datasets.

## Priority limit

Bounded searches for the exact question, B(i,d), bounded sign variation,
ball products, and the Klee–Novik construction located the works above,
but no earlier proof of the entire ball-product conclusion. Such searches
do not establish historical priority. The candidate's specific additional
construction is the spectral hitting graph with an algebraic flow
parameter and an identity-near-core reparametrization. It remains
AI-assisted, independently AI-reviewed, and unrefereed.
