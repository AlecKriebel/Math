# Independent review: alternating-link signature and polynomial degrees

**Verdict: PASS_CREDITED_KNOWN_RESOLUTION.** The complete pair of inequalities in Ohtsuki Problem 1.16 follows from the existing results identified in the artifact, with the stated variable and signature conventions. Recommended classification: **already_solved, 0/5**. No mandatory correction is requested; no new campaign theorem or priority claim is justified.

Reviewed independently on 2026-09-30 by a separate adversarial AI reviewer (gpt-6-astra, xhigh). This is a source, scope, normalization, and deduction audit; it does not reconstruct every classical geometric theorem on which the cited papers rely.

## Snapshot and controls

- `KNOWN_RESULT.md`: `242c13dd122ada89047171656b98b004e5e59b7f60a7fa189693abdedd2e45dc`
- Submitted `verify.py`: `bddde0a556414a3efbe89e86d062eb364e1c550d5eccec63f8101c5d1b0cb246`
- Submitted receipt: `9cf7e9c1a34d2b8a0a08a0e675dd7144d14ba8262d7a68f459c9a0cf629fb17f`

All **1,566 submitted assertions** replayed byte-identically in an isolated copy. A separate standard-library verifier passed **734 exact controls**, including signed spanning trees of an actual block graph, split Laurent factors, the sharp-bound implication, and two-strand skein normalization examples. No author files were edited.

## 1. Exact original bundle

I read [Ohtsuki's collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), printed pp.390–392, and visually inspected p.392. The target is the full chain

`σ(L) ≥ min deg_l P_L(l,m) ≥ min deg_a F_L(a⁻¹,z)`

for alternating links. The HOMFLY skein relation is `l⁻¹P₊−lP₋=mP₀`, with the unknot equal to one. The Kauffman polynomial is the usual writhe-normalized version. These are separate-variable Laurent degrees, not spans. The nearby Whitehead-double question has a different target and is not being settled here.

Write h for the middle term and k for the right-hand term. Inverting a Laurent variable reverses all its exponents, so `k=−max deg_a F_L(a,z)`. Both polynomials of the unknot are one, hence h=k=0; its signature is zero. This checks the crossing-free endpoint without applying a nontrivial-block argument to an empty Seifert graph.

## 2. Signature half: exact theorem coverage

The complete short [Ito primary preprint](https://arxiv.org/abs/2504.13491), including Theorems 5 and 7 and the proof on printed p.7, was read. Theorem 5 states the stronger inequality `h(L)+q(L)−1≤σ(L)`, where q counts non-split factors, not link components. Its footnotes explicitly identify Ohtsuki Problem 1.16 and fix positive-trefoil signature +2. The published [Cambridge article metadata](https://doi.org/10.1017/S0004972726101002) confirms online publication on 2 March 2026, volume 114(1), pp.182–190, and its abstract confirms the signature conclusion.

The relevant proof uses a surviving homogeneous-graph monomial and the alternating signature formula. The common upper bound `1−χ(L)` alone would not compare h and σ. In Ito's proof, the signed block ranks give a monomial exponent A, while the signature equals that same A. Noncancellation is an explicit credited Cromwell dependency; the elementary signed spanning-tree subtraction is valid. The corrected signature formula has no extra factor of one-half. This audit does not independently reprove Cromwell's whole skein construction or Traczyk's signature theorem.

The signature convention is essential. With the opposite convention the displayed source inequality would change. The independently generated positive two-strand trefoil polynomial is `2v²−v⁴+v²z²`, with minimum degree two, agreeing with the declared +2 signature. This is a convention control, not an argument replacing the general theorem.

## 3. Split factors and orientation

A split union has

`P_(L₁⊔…⊔L_q)=((v⁻¹−v)/z)^(q−1) ∏P_(L_j)`.

The coefficient ring is an integral domain, so the product's lowest nonzero v-coefficient cannot cancel. Therefore `h(L)=Σh(L_j)−(q−1)`. Signature is additive under split union, giving the claimed strengthened inequality from the non-split cases. For the q-component unlink, h=1−q and σ=0, so the strengthened inequality is equality. No prime-knot or non-split-only restriction is introduced into the final result.

The polynomials and signatures use the orientations in the source. The cited alternating-link theorems are statements for links, not just knots. The split reduction is also available independently of any connected-diagram convention in a front-construction theorem.

## 4. Kauffman half: sharpness, not unrelated bounds

I read the definitions, bounds, and the exact proof of Corollary 5.4 in the complete [Rutherford primary preprint](https://arxiv.org/abs/math/0511097), and visually inspected its printed p.15. The corollary states `max deg_a P_R≤max deg_a F_R` for alternating links. Its proof invokes Ng's front with a ruling and Rutherford's sharpness theorem. On that same Legendrian representative,

`tb=−max deg_a F_R−1` and `tb≤−max deg_a P_R−1`.

This implies the degree ordering. It would not follow just by comparing two upper bounds with no attained bound. Rotation or transverse self-linking refinements are unnecessary: the weaker HOMFLY Thurston–Bennequin bound stated in the paper already suffices. The constant minus one is included on both sides and cancels correctly.

Rutherford normalizes his regular-isotopy HOMFLY polynomial by a⁻ʷ. Its resulting skein relation uses the inverse framing variable relative to Ohtsuki's l. Thus `−max deg_a P_R=min deg_l P_L=h`. Rutherford uses Dubrovnik Kauffman; [Kálmán's primary preprint](https://arxiv.org/abs/math/0610659), p.2 footnote 2, explicitly records the matching framing-degree distribution. The conversion changes coefficient units, not the framing exponents. Hence negating the corollary gives k≤h. Ito's p.3 footnote also states this directly in Ohtsuki's `F(a⁻¹,z)` convention, providing a separate normalization cross-check.

For split unions the normalized Kauffman factor has maximum a-degree one, so `k(L)=Σk(L_j)−(q−1)`, the same shift as h. Both inequalities therefore cover split alternating links and arbitrary unknot factors.

## 5. Bibliographic limits

The [Oxford publisher record](https://academic.oup.com/imrn/article-abstract/doi/10.1155/IMRN/2006/78591/679664) confirms Rutherford's publication in IMRN 2006, article 78591. The theorem numbering audited here is the inspected preprint numbering. Ito's current arXiv record has its 18 April 2025 v1 and is not marked withdrawn; the Rutherford and Kálmán records likewise show no withdrawal notice in the inspected records. PDF-generation dates do not replace submission-version dates.

The file named `ito-published.pdf` in the research cache is actually HTML, which I verified directly. It is not a final journal PDF. Neither final journal text was compared line by line with its primary preprint in this audit. Publication metadata, explicit theorem scope, and the relevant primary-preprint arguments are separate pieces of evidence; the package describes that distinction honestly. The retained geometric dependencies are existing theorems, not claimed to have been independently rederived in full.

## Reproduction and disposition

From this review directory:

```sh
python independent_checks.py
python author_replay/verify.py > author_replay/replayed_verification.json
cmp author_replay/verification.json author_replay/replayed_verification.json
```

Both verifiers use only Python's standard library. Their finite checks do not establish a theorem for arbitrary knots by sampling. They check the convention translations, split factors, graph identities, and logical implications used in the source audit.

The exact bundled question is a credited known result, including the split and unknot cases. Retain **already_solved, 0/5**, all source-access qualifications, and no campaign novelty or human-peer-review claim. No mandatory correction remains.
