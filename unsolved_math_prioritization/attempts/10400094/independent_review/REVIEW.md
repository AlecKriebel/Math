# Independent review: Fox 7-colorings and the (4,∞) skein module

**Verdict: PASS_SCOPED_DIAGNOSTICS.** Both restricted mathematical claims in the submitted artifact are correct. No mandatory correction is requested. Ohtsuki Problem 4.16 remains **unsolved, 2/5** in this package: neither a globally normalized auxiliary link invariant nor an all-link recovery formula has been established.

Reviewed on 2026-09-30 by a separate adversarial AI reviewer (gpt-6-astra, xhigh). This is an AI review, not human peer review, a novelty determination, or a certification that no relevant result exists in the literature.

## Frozen material

- `PARTIAL_RESULT.md`: `9383a795ca5ae12422b18b717cf24725a1e9004646c955d6abfcd62f178d6d39`
- Submitted `verify.py`: `4cbf08c6a7930cec36516bc7653a1a0bab1af2d3528293b2336faadabeab6a2a`
- The submitted verifier reproduced all **5,878 exact assertions**, with a byte-identical receipt, in an isolated copy. The author directory was not edited.
- A separately written standard-library verifier passed **3,264 exact assertions**, using crossing-equation elimination rather than matrix powers to count the braid and cap/cup closures, and a direct cyclotomic-ring implementation rather than SymPy for the Gaussian identity.

## 1. Primary-source and scope audit

I read the full relevant discussion in [Ohtsuki's collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), printed pp.450–453, and visually inspected Figure 15 on p.450. The source uses unoriented framed links, including the empty link, over a commutative unital ring, with `a`, `b₀`, and `b₃` invertible. Its four local twist diagrams are successive half-twists; the fifth diagram is the other smoothing. Problem 4.16 is the coloring-recovery question on p.452. The squared-norm examples on p.453 are decisive: the source permits more than a scalar linear relation for the raw integer count.

The author's [Trieste notes](https://indico.ictp.it/event/a08157/session/33/contribution/18/material/0/0.pdf), printed p.28, repeat the recovery motivation and suggest Gaussian sums. They report Jaeger's observation without supplying a proof. The submitted artifact accurately treats this as context, not a verified theorem. I have not independently matched the normalization of the later metaplectic-invariant lead to Figure 15, and this review grants no coefficient classification on that basis.

The use of all Fox colorings, including constant colorings, is explicit and consistent throughout the submitted proof. No identification with branched-cover homology is required. All five testing closures are nonempty; allowing the empty link in the source module cannot invalidate a necessary relation already forced by these closures.

## 2. Raw-count scalar obstruction

The proposed exterior tangles are legitimate. Rotating Figure 15 and closing an external two-strand braid with `−j` twists gives exponent `k−j` for the `k`th local twist. Reversing the sign convention changes all these exponents by sign, leaving divisibility by seven unchanged.

The other smoothing joins the two top endpoints and the two bottom endpoints. After closure against the external braid, it has one component. It is a two-strand plat with possible framing curls. More importantly, its coloring count follows directly without relying on an isotopy claim: the cap imposes equal colors, every positive or negative crossing preserves equal colors, and the cup imposes no further restriction. There are exactly seven assignments.

At every signed crossing the next color pair is determined invertibly by the previous one. The submitted matrix is `A=I+N` with `N²=0`. This gives `A^r=I+rN` for every integer, including negative integers. The closure condition is therefore precisely `r(a−b)=0` over `F₇`: there are 49 solutions when `7` divides `r` and seven otherwise.

For `j=0,1,2,3`, the unique count 49 among the four twist fillings occurs in column `j`. At `j=4`, none of the four exponents is divisible by seven. The cap/cup column is seven in all five rows. Dividing by seven yields exactly the displayed matrix. Subtracting its fifth row from its first four rows leaves a diagonal `6I₄` above a final row of ones, so its determinant is `6⁴`. Consequently the only coefficient vector annihilating all five closures over a characteristic-zero field is zero. This proves the proposition, including incompatibility with invertible end coefficients.

The stated extension to fields of characteristic other than 2, 3, or 7 is correct. The unnormalized determinant is `7⁵6⁴`. In characteristics 2 and 3, a nonempty link's count is a power of seven and reduces to one. In characteristic 7 it reduces to zero; the artifact appropriately makes no general coefficient classification there. Normalizing counts by seven over characteristic zero merely rescales the tests. Framing independence forces `a=1` for a count-valued evaluation because the unknot has nonzero value seven.

This is a rigorous obstruction to the **raw-count linear evaluation only**. An auxiliary invariant followed by a nonlinear operation, such as a squared norm, is not excluded.

## 3. Gaussian diagonal operator and coefficient conventions

The period sums use the three nonzero quadratic residues and the three nonresidues modulo seven. Direct reduction modulo `Φ₇` confirms `s+s̄=−1`, `ss̄=2`, and `(s−s̄)²=−7`. For the three nontrivial eigenvalues, the monic cubic is exactly

`P(t)=t³−s t²+s̄ t−1`.

Its constant term is negative because the product of the three roots is `ζ⁷=1`. Its linear coefficient is `ζ³+ζ⁵+ζ⁶=s̄`. At the remaining eigenvalue, `P(1)=s̄−s`; hence `P(D)+(s−s̄)Π₀=0`, with the sign in the submitted formula correct. Since all four eigenvalues `1,ζ,ζ²,ζ⁴` occur and are distinct, the minimal polynomial has degree four. There is no nonzero scalar cubic annihilating `D` alone.

The coefficient tuple is consequently correct for the specified five operators. It is not automatically a tuple for the source skein module. A cap/cup endomorphism may be a nontrivial scalar multiple of the normalized projection, changing the fifth coefficient; crossing and framing normalization also matter. No Yang–Baxter, duality, framed isotopy, Markov, or coloring-recovery theorem follows merely from this diagonal identity. The submitted artifact states these limitations clearly and does not promote the local calculation into a global invariant.

## 4. Reproduction and disposition

From this review directory, run:

```sh
python independent_checks.py
python author_replay/verify.py
```

The first command requires Python's standard library. The submitted verifier also requires SymPy. Both receipts are deterministic and record the reviewed mathematical hash. Finite checks support, rather than replace, the elementary general arguments above. They do not certify an invariant on arbitrary links.

Retain the original **unsolved, 2/5** status, the distinction between the direct obstruction and auxiliary-invariant recovery, and the explicit absence of a novelty claim. No revision to the frozen mathematical text is required.
