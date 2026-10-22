# Independent adversarial review: 2919 / KP-4.43

**Verdict: PASS_KNOWN_COUNTEREXAMPLE_TO_LITERAL_ABSOLUTE_VALUE_QUESTION.** No mandatory mathematical correction. The exact printed absolute-value assertion is contradicted by the credited MMSW example. This verdict does not address a repaired one-sided question and does not assign new discovery credit.

Reviewed on 2026-09-30 by a separate gpt-6-astra agent at xhigh reasoning. This is an AI source/proof audit, not human peer review. Frozen `KNOWN_COUNTEREXAMPLE.md` SHA-256:

`f239c3a4ddf249251d04ccaa6567cc940f93a2781db49ccec1c1c043167d22fe`.

## 1. Exact original statement

I independently opened the problem page (unavailable in the reader), then the complete [K3 primary PDF](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf). I read Problem4.43 and all four remarks and visually inspected printed p.224. Both the absolute-value bars in $2g(\Sigma)\ge|s(K)|$ and the phrase “null-homotopic” are actually present. They are not extraction artifacts. The ambient manifold is negative definite and smooth; the proposed counterexample uses the standard closed oriented $\overline{\mathbb{CP}}^{\,2}$ and therefore does not rely on any missing compactness or exotic-smoothness qualification.

The source's remark1 attributes its displayed bound to MMSW in the standard connected-sum case. The cited MMSW theorem is instead one-sided. The package appropriately records that precise discrepancy without silently rewriting the question or speculating about its author's intent.

## 2. Known disk and its orientation

I read the relevant parts of the full [author-hosted MMSW manuscript](https://web.stanford.edu/~cm5/S1S2sInvt.pdf), specifically the introduction, §6.1, Theorem6.10's proof, Corollary6.11 and its following paragraph, and §9.2. I also visually checked manuscript pp.5,30,32,49. The orientation bars on the projective plane are clear in those images, although plain-text extraction drops them.

Definition6.2 requires a proper embedded union of disks with zero class in $H_2(X\setminus B^4,\partial(X\setminus B^4);\mathbb Z)$. Example6.4 identifies the left-handed trefoil $T_{2,-3}$ as such a knot in $\overline{\mathbb{CP}}^{\,2}$. Its construction is explained in Remarks6.1 and6.3: the trace of a negative crossing change gives a relative-null-homologous annulus in the doubly punctured negative projective plane; capping its unknot end with the usual smooth disk gives the desired disk. The balanced orientations in the crossing region account for the zero relative class. The paragraph after Corollary6.11 explicitly states $s(T_{2,-3})=-2$ and repeats the same negative-projective-plane sliceness claim. Thus neither the sign nor the ambient orientation is being inferred from a potentially ambiguous diagram alone.

Corollary1.9 says $s(L)\le1-\chi(\Sigma)$ for the specified null-homologous surface; for a knot this is $s(K)\le2g(\Sigma)$. The known disk obeys this inequality. This audit does not find a contradiction to the MMSW theorem.

For the negative projective plane with a ball removed, $Q=[-1]$ and the boundary is a three-sphere. Identifying that boundary with the standard oriented sphere in the other orientation mirrors the knot, possibly accompanied by reversal of its own orientation. Mirroring negates the knot Rasmussen invariant; reversing a knot's own orientation does not affect the absolute value. Consequently the invariant appearing in the literal question is $|s|=2$ in either boundary-identification convention. Reversing the orientation of the entire four-dimensional pair changes the intersection form to $[+1]$; it cannot produce a second one-sided inequality while remaining in the negative-definite class.

## 3. Null-homology really gives the required relative nullhomotopy here

This is the only additional topological implication needed beyond the published example, and it is valid.

Let $W=\overline{\mathbb{CP}}^{\,2}\setminus\mathring B^4$. Van Kampen, applied when the ball is restored along a collar of $S^3$, gives $\pi_1(W)=0$. The relevant exact sequences are

$$0=\pi_2(S^3)\longrightarrow\pi_2(W)\longrightarrow\pi_2(W,S^3)\longrightarrow\pi_1(S^3)=0$$

and

$$0=H_2(S^3)\longrightarrow H_2(W;\mathbb Z)\longrightarrow H_2(W,S^3;\mathbb Z)\longrightarrow H_1(S^3)=0.$$

The horizontal maps in the middle are isomorphisms. Since $W$ is simply connected and has the homotopy type of a CW complex, degree-two Hurewicz gives $\pi_2(W)\cong H_2(W;\mathbb Z)$. Naturality identifies the relative Hurewicz map with the composite of these isomorphisms. Thus the known disk's zero relative homology class implies that its class in $\pi_2(W,S^3)$ vanishes.

There is no hidden dependence on a homotopy that moves the specified boundary parametrization. Given its knot map $k:S^1\to S^3$, choose any continuous extension $f_0:D^2\to S^3$. Gluing the disk map to the oppositely oriented $f_0$ gives a sphere in $W$. Its absolute homology class maps to the disk's zero relative class, so it is zero; by Hurewicz the sphere is nullhomotopic. Equivalently, the two disk maps are homotopic rel $S^1$ (one can extend the resulting map on the boundary of $D^2\times I$ across that three-ball). This proves the stronger fixed-boundary formulation used in the artifact.

Neither the source statement nor the argument requires a homotopy through embeddings, or an embedded filling disk inside $S^3$. Such a requirement would be a different geometric condition. Ordinary absolute nullhomotopy of a disk map is weaker and is automatic, but the package correctly verifies the meaningful relative condition rather than relying on that vacuity. No source definition imposing a different stronger notion was found in the problem and its remarks.

## 4. Contradiction and exact scope

For the resulting smooth proper disk $\Delta$, one has

$$2g(\Delta)=0<2=|s(T_{2,-3})|.$$

Every stated hypothesis is satisfied, including relative nullhomotopy. This is a complete known counterexample to the literal displayed assertion. The same disk has $-2\le0$, so it gives no obstruction to the one-sided extension posed in MMSW Question9.7. The package neither establishes a new example nor addresses that repaired general question or a smooth-Poincaré counterexample.

Classification `already_solved`, known negative answer to the literal source formulation, with 0/5 new proof attempts, is justified. Any later reformulation must be assessed separately.

## 5. Reproducibility and source/version limits

The author supplied an explicit JSON checklist, not an executable verifier. I reproduced its numerical conclusion and retained it unchanged as `submitted_verification.json`. Run `python independent_checks.py` in this directory. All20 exact controls pass: Euler-characteristic and inequality conventions, mirror/ambient sign controls, rank-one intersection-form diagnostics, the degree-two diagram's algebra, and replay of the submitted checklist. These controls do not purport to compute Khovanov homology, certify a handle diagram, or prove Hurewicz by finite testing; the mathematical verification is given above.

The current [arXiv record](https://arxiv.org/abs/1910.08195) lists v1 from17October2019 and v2 from5January2022, described as the final version. [Manolescu's publication list](https://web.stanford.edu/~cm5/papers.html) independently confirms Duke Mathematical Journal172(2023),231–311. The full source actually inspected was the52-page author manuscript, not a newly retrieved typeset81-page journal PDF; exact locators in this report are manuscript page numbers. The DOI landing page did not load in the reader. No relevant correction was found on the author publication listing or current arXiv record. These bounded checks should not be advertised as exhaustive bibliographic certification.

Source hashes checked:

- K3 PDF: `ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f`
- MMSW author PDF: `47e7f927b0f67b77b43c57ce6b5bde28a2550cd936508531e109dd3b1842aa21`

The author's artifact and source files were not edited during this review.
