# Quantitative dimension-growth priority chain

Date: 2026-10-14 UTC. Expanded audit of frozen commit `5bee5139501a399da653f634147eab9433774ac7`. The completed first checkpoint `REPORT.md` is preserved unchanged.

**Verdict: UNSUPPORTED as an immediate implication from the inspected literature.** Even granting a lossless ordinary-colored-cover → generic-continuous-cover → Borel-cover transfer, the available controlled bound for W = Z wr Z has exponents `(a,b)=(3,1)`, whereas GMRS's proved sufficient polynomial condition is `ab <= 1/4`. Here `ab=3`. This does not prove that better bounds, different metrics, or some other application of the general criterion are impossible.

## Exact quantities must stay distinct

For a metric space X, GMRS defines `dim^X(s,d)` by the minimum number of colors minus one in a cover by s-separated families, with every set having diameter at most d. Equivalently, same-color s-walk components have diameter at most d. `dim_B^X(s,d)` adds Borelness of the families; `sdim_B^X(s)=lim_(d→∞) dim_B^X(s,d)` forgets diameter control. Definition 2.2 and the preceding discussion are on pp. 7–8. The analogous continuous witness uses continuous finite coloring; it supplies a Borel coloring, but any claimed diameter estimate must actually be retained. [GMRS v1](https://arxiv.org/pdf/2608.22565v1).

Dranishnikov's older `ad_X(lambda)` uses multiplicity and a Lebesgue number for uniformly bounded covers; Theorem 4.6 gives polynomial growth for the appropriate wreath products, including W, without a stated polynomial diameter control for the resulting cover. This is an **uncolored** quantity. Dranishnikov–Sapir v4, Definition 1.2 and Question 1.5, explicitly distinguish it from the colored two-parameter dimension and leave equality of the single-variable growth functions as a question. GMRS p. 8 repeats this distinction. Thus “W has polynomial asymptotic-dimension growth” cannot silently be substituted for a quantitative colored-cover estimate. [Dranishnikov v1, pp. 2, 14–15](https://arxiv.org/pdf/math/0405239v1), [DS v4, pp. 3–4](https://arxiv.org/pdf/1008.3868v4).

Iyer–Shinko's Proposition 7 transfers a **specified locally checkable labeling problem** admitting a group coloring to a dense open set of Cantor actions admitting a continuous coloring. Countably many such constraints can be imposed simultaneously. Its `asdim_c` in Definition 17, however, records a uniform finite bound on monochromatic components and then takes the number of colors; it does not state a two-parameter diameter-control theorem. An appropriate bounded-diameter rule must be encoded to retain quantitative control. For the strongest adversarial check below, that routine transfer is **granted without loss**; rejecting the advertised chain does not rely on an unproved obstruction to such encoding. [Iyer–Shinko v1, pp. 3–6, Definitions 4–5/17 and Propositions 7/16](https://arxiv.org/pdf/2409.03078v1).

## Controlled W source and threshold comparison

DS v4, Definition 6.1/Lemma 6.3 (p. 16) and Theorem 6.12/Corollary 6.13 (pp. 19–20), state a Kolmogorov–Ostrand bound for iterated wreath products B_0=Z, B_(k+1)=B_k wr Z:

`(lambda,D_k)-KOdim(B_k) <= a_k lambda^k`,

`D_k(m,lambda)=b_k(m+lambda^k)lambda^(k+1)`.

Setting k=1 and m=0 gives O(lambda) colors with O(lambda^3) diameter. This is the correct specialization; a polynomial color-count theorem does not make the exponent b arbitrarily small. Question 6.14 asks for the exact growth even for W. [DS v4](https://arxiv.org/pdf/1008.3868v4).

The source requires a qualification: Davila's 2020 University of Florida dissertation explicitly identifies the use of incorrect DS Lemma 6.7 in the proof of Theorem 6.12 and supplies a replacement extension argument. Theorem 4.0.2, pp. 28–29, has color count `n_H(lambda) n_K(lambda+2D_H(0,lambda))` and control `D_K(m,lambda+2D_H(0,lambda))+2D_H(0,lambda)`. Lemmas 4.0.3–4.0.4 and Theorem 4.0.5, pp. 29–30, give a polynomial KO color-count bound for B_k. For W, the displayed formulas specialize to O(lambda) colors and O(lambda^3) diameter at m=0: the quotient scale is `5lambda+4`, and the kernel control is O(m lambda^2+lambda^3). This is an algebraic reading of the author's formulas, not independent validation of the repair. Either the original advertised pair or this repaired pair still fails the GMRS threshold. [Davila dissertation, Chapter 4](https://ufdcimages.uflib.ufl.edu/UF/E0/05/64/17/00001/Davila_T.pdf).

GMRS Theorem C and Theorem 4.7 require decreasing locally finite Borel extended metrics rho_m and, for each m, constants C_m with

`dim_B^(rho_m)(s,C_m s^a)=O(s^b)`, with `a>=1`, `b>=0`, `ab<=1/4`.

For a single orbit metric one may take a constant sequence of metrics. The more general alternative requires positive sequences s_n→∞ and d_n satisfying, for every m and all sufficiently large n,

`24 dim_B^(rho_m)(s_(n+1),d_(n+1)) d_(n-1) <= s_n <= d_n`.

The supplied W bound does not verify either condition. Failure of its exponents to meet the polynomial sufficient condition is **not** a lower bound on the actual dimension function. One cannot use GMRS's optimality discussion for this construction to deduce nonexistence of a sharper W estimate. A different estimate could conceivably verify the general sequence condition. [GMRS v1, p. 3 and pp. 15–17](https://arxiv.org/pdf/2608.22565v1).

## Chain status

| Arrow | Status | Reason |
|---|---|---|
| Older polynomial `ad_W` growth → a diameter-controlled colored bound fitting GMRS | **Unsupported** | Uncolored multiplicity/Lebesgue quantity differs from colored dimension; diameter control and its rate are missing. |
| A valid ordinary controlled colored bound → generic continuous witnesses | **Possible in principle; granted for this audit** | Iyer–Shinko Proposition 7 transfers specified finite local rules. Encoding must retain diameter bounds. |
| Continuous finite coloring with the claimed component diameter → Borel witness | **Immediate once the witness exists** | Continuous coloring is Borel; finite word balls make bounded components finite. |
| The advertised/repaired O(s) colors with O(s^3) diameter → GMRS polynomial corollary | **Insufficient** | The displayed upper bound supplies `(a,b)=(3,1)`, with product 3 rather than at most 1/4. |
| Polynomial or subexponential single-variable `sdim_B` growth → hyperfiniteness | **Not a proved GMRS implication** | GMRS Conjecture F(2), p. 5, is precisely the missing general assertion; single-variable growth has forgotten control. |
| Entire resulting chain → exact generic whole-space W claim | **Unsupported by inspected results** | No threshold-fitting controlled colored estimate or direct general-sequence verification was identified. |

No assertion is made that every ordinary geometric route is impossible, that the target is currently open worldwide, or that the candidate is novel. This addendum only excludes an immediate implication from the exact inspected sources and their displayed bounds. No candidate proof search occurred. **Expanded audit completion: 100%.**

## New-source provenance

- Alexander Dranishnikov and Mark Sapir, *On the dimension growth of groups*, arXiv:1008.3868v4, revised July 24, 2012; inspected pp. 3–4, 16, 19–20, plus the complete relevant displayed formula chain. Retrieved October 14, 2026 at 03:31:53 UTC. PDF SHA-256: `76d364d19ca95a8e1d61026544b91dd2a96bd4688116941c210a27632dc45547`.
- Alexander Dranishnikov, *Groups with a polynomial dimension growth*, arXiv:math/0405239v1, May 13, 2004; published Geometriae Dedicata 119 (2006), 1–15, DOI 10.1007/s10711-005-9026-z. Inspected pp. 2–4 and the complete Theorem 4.6 proof on pp. 14–15. Retrieved October 14, 2026 at 03:31:53 UTC. PDF SHA-256: `57700963083288b6c1e19ef41bd335f7225c6e5742eb87d440c66a8cdcfffab7`.
- Trevor Davila, *Infinite Dimensional Coarse Geometry of Groups and Spaces*, Ph.D. dissertation, University of Florida, May 2020; chair Alexander Dranishnikov. Inspected complete Chapter 4, printed/PDF pp. 28–30, including the correction notice, Theorem 4.0.2, Lemmas 4.0.3–4.0.4 and Theorem 4.0.5. Retrieved October 14, 2026 at 03:31:54 UTC. PDF SHA-256: `95fd37f72a3ebe57df23aaeda5bf58573a44186395ef97d0eef6c290e18bf4e1`.

GMRS and Iyer–Shinko source hashes, version metadata and retrieval times remain in `inspection_ledger.md` and `download_manifest.json`. The quantitative scope reread covered GMRS pp. 3, 5, 7–8, 13–18 and Iyer–Shinko pp. 3–6. A DOI link to the published DS corrigendum could not be opened, so no claim about its text is made; the later error notice is attributed specifically to Davila's thesis. The indexed Southampton characterization-paper link returned HTTP 403 on raw retrieval and was not used as content authority.
