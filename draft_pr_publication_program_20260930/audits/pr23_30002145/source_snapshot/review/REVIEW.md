# Independent adversarial source review: 30002145

**Verdict: PASS for the source-status correction as explicitly scoped.**
No new theorem, novel proof, or unrestricted global-domain resolution is certified.
Review date: 2026-09-30. Reviewer execution: gpt-6-astra, xhigh.

## Frozen artifacts reviewed

- `SOURCE_STATUS.md`: SHA-256 `ff80528de521556c537c8dd67868b8cc4aaa680ba011c61ce594dfad70216ef3`
- `verify.py`: SHA-256 `be3c12b1d90ed309c6f8aeb6f4da2a3cd72d9bf878ce31e36987c6c83301f372`

The reviewer is separate from the author. The review did not alter the target artifacts.

## Source and quantifier audit

1. **Original setting.** I read Rindler's complete contribution, pp. 2247–2249 of [OWR 36/2012](https://publications.mfo.de/bitstream/handle/mfo/3307/OWR_2012_36.pdf?isAllowed=y&sequence=1), and visually checked p. 2248. The fixed-line inclusion is introduced while explaining the published lower-semicontinuity argument and its iterated blow-ups. The text explains why the overly simple two-profile guess can fail and how the requisite structure is obtained. It does not designate the extracted sentence as an open conjecture. The general variational problem starts on a Lipschitz domain; this does **not** supply a claim of one global profile representation on every nonconvex domain.
2. **All dimensions and signs.** [De Philippis–Rindler, 2020](https://www.aimspress.com/article/doi/10.3934/mine.2020018), Theorem 2.10 ([arXiv pp. 12–14](https://arxiv.org/pdf/1911.01356)), assumes `u in BD_loc(R^d)` and `Eu=P nu` with a **signed** locally finite measure. Its independent-product case includes the transverse quadratic term; its rank-one parallel case includes the transverse-linear terms with one-variable coefficient functions. Both displayed smooth formulas in the reviewed note match these cases. Theorem 3.2 separately uses positivity for tangent measures to simplify them. Confusing that positive-measure result with Theorem 2.10 would be a scope error; the note does not do so.
3. **Prior two-dimensional work.** [Rindler's 2011 paper](https://arxiv.org/pdf/1008.2089), Propositions 4.7 and 4.9, gives the corresponding two-dimensional structures. Example 4.8 is exactly the polynomial example quoted in the note. It is properly attributed as prior work.
4. **Normalization and degenerate cases.** The note correctly splits independent vectors from nonzero parallel vectors, rather than applying the printed condition `a != +/-b` to unnormalized collinear vectors. Since the target is a line, any nonzero parallel product can be replaced by a unit-vector product after scalar absorption. Zero product gives zero symmetric gradient and hence componentwise rigidity. The one-dimensional nonzero case imposes no additional restriction.

## Independent mathematical checks

All eight assertions in the author's verifier passed on rerun. They are sufficiency checks only, as the note explicitly states.

I also implemented a distinct check using the Saint-Venant compatibility tensor. If `Eu=P lambda` and `H=D^2 lambda`, its entries are

`P_jl H_ik + P_ik H_jl - P_jk H_il - P_il H_jk`.

For `P=e1 odot e2`, exact linear algebra in dimensions 2 through 6 leaves precisely the Hessian entries `H_11,H_22` free. This agrees with a sum of two one-variable terms plus an affine transverse term. For `P=e1 odot e1`, it leaves precisely `H_1j` free, including `H_11`; this agrees with a one-variable term plus transverse-linear terms with one-variable coefficients. These finite algebra checks independently test the underlying compatibility restriction; they are not substituted for the theorem's all-dimensional BD proof.

The independent script also checks a nonorthogonal, nonunit independent-vector polynomial specialization. This guards against accidentally testing only an orthonormal-coordinate identity. Direct differentiation confirms cancellation of the mixed terms in both formulas; the remaining strains are the coefficients stated in the note. The cited theorem supplies necessity, and its local smooth compatibility argument works on sufficiently small adapted boxes.

## Scope boundary and publication conditions

There is no mandatory correction to the frozen note. The PASS requires preserving its explicit whole-space/local-blow-up qualification, its arbitrary-nonconvex-domain warning, and its statement that no new mathematical discovery is claimed. It must not be promoted to a theorem about a single global pair of profiles on an unspecified domain, nor to a new solution of an open problem. The imported question lacks enough domain information to support that stronger disposition.

Source PDFs were independently retrieved and their relevant passages read. Their SHA-256 hashes are recorded in `review_summary.json`; the PDFs and page renders are reference material, not intended repository additions. `independent_checks.py`, `independent_results.json`, and `verifier_rerun.txt` record the reproducible checks.
