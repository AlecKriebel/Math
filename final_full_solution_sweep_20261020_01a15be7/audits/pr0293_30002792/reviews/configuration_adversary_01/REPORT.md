# PR293 independent configuration adversary report

**Verdict: PASS for the configuration, symbolic-power, and ACM reductions, conditional only on the separately audited surface Lemma B. No counterexample or blocking configuration-side gap was found.**

Scope: target 30002792 / OWR-13494-011, frozen input head `6e717193f93c8a321cce1ce35a00eed1ecfb56e7`. This audit concerns the full arbitrary-characteristic line-configuration statement, but independently certifies its configuration-side implications rather than re-auditing resolution, duality, or adjoint nonvanishing on surfaces. The parent reports that a separate surface-family audit has passed. That information did not enter the initial derivation or the controls below.

## Claim and primary-source quantifiers

For every algebraically closed field k, let L be a nonempty finite reduced union of distinct projective lines in `P3_k`, with homogeneous saturated radical ideal I. The candidate asserts:

`alpha(I^(2))=alpha(I)+1 => L is coplanar or a complete plane-pair pseudostar => L is ACM`.

The original question is the existential negation of the ACM conclusion. Janssen arXiv:1306.4387v2, PDF page 1, establishes arbitrary characteristic; type `(d-1,d)` is defined by the two initial degrees; Question 3.1 on PDF page 8 asks whether a configuration of that type can fail to be ACM. Theorem 2.13 classifies the ACM case. Definition 2.1 allows arbitrarily many defining planes to meet at a point and excludes only three sharing a line. The same existence question and plane-pair definition appear in OWR 9/2015, printed page 514, which is PDF page 26. The OWR contribution does not itself repeat the field convention. See [Janssen](https://arxiv.org/pdf/1306.4387), [OWR](https://ems.press/content/serial-article-files/46557), and `SOURCE_VALIDATION.md` for precise scope and preserved primary PDFs.

The sought counterexample has no ACM assumption, general-position requirement at points, degree bound, or connectedness requirement. The broader reduced-curve question is a separate question, not this target.

## Independence and order of work

`DERIVATION_INITIAL.md` was preserved before examining the original control code or results. It records a complete independent conditional derivation of C1–C4 and the intended falsification plan. I never read the original final adversarial review or another fresh auditor's derivation. After preserving the derivation, I read the original control script, reproduced its output, and wrote a separate engine using primal point bases and truncated substitution. `DERIVATION_SUPPLEMENT.md` gives a further independent direct proof of radicality, saturation, and ACM.

All files and computations are confined to this assigned directory. No individual was contacted; no remote mutation, commit, branch change, or publication was performed.

## Analytic audit

### Symbolic square and repeated factors: verified

For a reduced union, `I=intersection p_l` over distinct line primes, and localization at each minimal prime isolates that line. A line prime has coordinates `(u,v)`; its square is primary. One elementary proof uses the quotient's free `k[s,t]` basis `1,u,v`: multiplication by a polynomial outside `(u,v)` is injective by the normal-degree filtration. Therefore `I^(2)=intersection p_l^2`, including characteristic two.

For a nonzero degree-d member F, every target line lies in its squarefree radical. Initial degree `a=d-1` bounds the total repeated-factor excess by one. Thus any repetition has the unique form `F=P^2 G` with P linear and G squarefree, coprime to P. If G is constant, all lines lie in P. Otherwise some partial of G is nonzero: over a perfect field, the simultaneous derivative kernel consists of p-th powers. Every target line outside P has `G in p_l^2` by primary contraction, so that partial belongs to `p_l`. Multiplying it by P gives a nonzero degree-(d-2) form through all target lines, a contradiction. The proof does not differentiate `P^2`, so its zero derivative in characteristic two is harmless.

### Nonlinear factors: verified conditional implication

The exact independent input needed is:

> For every integral degree-e surface in `P3_k`, with `e>=2`, a nonzero form of degree e-2 vanishes on every reduced singular-curve component.

Isolated singular points need not be covered. The statement must hold in every characteristic without an ACM, separability, or general-position assumption.

For an irreducible nonlinear factor Q of squarefree F, any target line contained in Q alone has `Q in p_l^2`. All its first partials vanish along that line. Over the algebraically closed, hence perfect, field, Q is generically smooth and its singular locus is proper of dimension at most one; the line is a reduced singular-curve component. Multiplying the input's form A by `F/Q` therefore covers all target lines in degree d-2. There is no additional configuration-side hypothesis hidden here. Establishing the displayed input itself is the exact separate surface-audit dependency.

### Complete plane pairs and triple-line exclusion: verified

Once F is a product of d distinct planes, each target line lies in at least two factors. If the pair line `V(Pi,Pj)` is missing, each target line is covered by a factor remaining in `F/(Pi Pj)`. If that pair line lies in a third plane, the same quotient also covers it. In either case the quotient has forbidden degree d-2. Thus all pair lines occur and no triple contains a line. Concurrency at a point does not affect this argument.

### Radicality, saturation, ACM: independently verified

The proposed Hilbert-Burch argument is correct: maximal minors are `F/Pi`, their ideal has height two, and no triple line makes every minimal-prime localization reduced. Its Cohen-Macaulay quotient has no embedded primes, so it is reduced. Saturation follows from equality with the line-prime intersection.

There is also a direct verification. Under the no-triple-line hypothesis,

`(F/P1,...,F/Pd)=intersection_{i<j}(Pi,Pj)`.

Induct on d. Reducing a member of the right side modulo Pd places it in the intersection of distinct principal linear ideals in `R/(Pd)`, hence in their product. Subtract that product multiple and divide the remaining term by Pd. Since Pd lies in none of the older pair primes, its quotient belongs to the smaller intersection and induction applies. This proves radicality and saturation directly.

For any distinct planes, a relation `sum hi(F/Pi)=0` reduces modulo each Pi to show `hi=Pi ai`. Cancellation then gives `sum ai=0`. Hence all syzygies are freely generated by `Pi e_i-Pd e_d`, giving the explicit resolution

`0 -> R(-d)^(d-1) -> R(-(d-1))^d -> J -> 0`.

Height two and this resolution make `R/J` Cohen-Macaulay of dimension two. Combining with the ideal identity proves the actual reduced line union ACM in every characteristic. For coplanar unions, `(P,G)` is a complete intersection. The boundary `d=2` is covered; nonemptiness ensures `a>=1`.

## Exact computational evidence

The retained independent suite passes **125,930 assertions**, with all assertions distinguished by type in `INDEPENDENT_CONTROLS.json`. Assertion totals include bookkeeping and repeated checks and are not counts of independent mathematical results.

The independent engine substitutes each polynomial into a line's point basis and two complementary vectors, then retains all coefficients below the required total normal degree. These are exact coefficient conditions for membership in the line ideal or its square. It uses no floating-point computation and no evaluation on finitely many rational points. Coefficient ranks over a finite field are preserved by extending to its algebraic closure.

**Exhaustive retained search:** all **59,535** nonempty subsets of up to four of the 35 lines in `PG(3,2)`. Cubic dimension counting bounds alpha by three, and squaring bounds the symbolic initial degree by six, so the search cutoff is proved sufficient. Every gap-one case is classified:

| Number of lines | Coplanar gap-one cases | Pseudostar gap-one cases |
| --- | ---: | ---: |
| 1 | 35 | 0 |
| 2 | 315 | 0 |
| 3 | 525 | 420 |
| 4 | 525 | 0 |

The remaining 57,715 configurations have larger gaps. Four-line states include `(alpha,alpha_square)=(2,4),(3,5),(3,6)`; skew and disconnected cases are present. There are no classification exceptions. A deterministic record-stream digest is `0f7a69ad8b6507feaf4108c7ad5b8eba50d8850ac1a6f1c285657a7bc04e7c52`.

**Additional completed controls:**

- All 63 nonempty subsets of the six coordinate tetrahedron lines in each characteristic 2,3,5,7: 252 configurations, including all missing-edge states. Gap one agrees exactly with the classification.
- All 219 subcaps of sizes 3 through 8 of the eight characteristic-two planes `(1,a,b,c)`, with `a,b,c in {0,1}`. These test large pseudostars and many point concurrencies. The largest has 28 distinct lines and initial degrees `(7,8)`.
- 120 comparisons of the actual radical line-ideal dimensions, spans of multiples of `F/Pi`, and the explicit resolution's Hilbert-series numerator `1-d*t^(d-1)+(d-1)*t^d`, for d=3 through 8 and characteristics 2,3,5,7.
- Four-plane point cones, four/five-plane triple-line degenerations, repeated-factor double forms, and maximal same-ruling line families on smooth quadrics. Triple-line four-plane support has `(2,4)`, five-plane support `(3,5)`, repeated-factor support `(2,4)`, and every tested same-ruling family `(2,4)`.
- An exact nonradical-minor negative control: for `F=x*y*(x+y)*z`, `xz` belongs to the radical but not to the degree-three generator ideal, while `(xz)^2` belongs to it by an explicit identity. This confirms that the proof's triple-line exclusion is essential.
- Engine negative controls reject the characteristic-two polynomial `x0^2*x1+x0*x1^2`, which vanishes at every F2-rational point of a line but not identically on it, and reject `x0^2` as a squared-line member despite all its derivatives being zero.

**Original reproduction:** all **3,888** frozen assertions reproduced with exact JSON equality to the frozen archived result. The 24 original line examples were also recomputed by the independent engine and agree. The retained frozen script hash is `08744c44e2a0c057ac8d25b315c5a0c282ce60a32ce5c9bdd7546fc0b3668b4d`; the public proof hash is `56d7aee2dbb567f1574952bfe905b5407c0f0b06ec60e4b53b72acda48c245e1`.

An optional extended run through six lines completed before an attempted stop reached it: its tool completion reported PASS for **2,007,327 configurations**, **4,027,195 assertions**, in **221.864 seconds**. Its aggregate JSON was subsequently overwritten by the final size-four replay before being copied. `EXTENDED_SEARCH_EXECUTION_RECORD.txt` and `OPTIONAL_EXTENDED_SEARCH_STATUS.json` record this accurately. This supplementary execution trace is not substituted for the fully retained primary JSON. No further extension was run.

## Remaining gap and disposition

There is **no remaining configuration-side gap or requested correction**. The strongest independently established universal result is the target theorem conditional on the exact surface input above. This audit does not independently certify that surface input, nor claim that finite controls prove it. Integration must combine this report with the separate surface-family verification before calling the full proof validated.

No novelty, literature-completeness, priority, or publication claim is made. Reproduction instructions are in `REPRODUCE.md`; the final `MANIFEST.json` hashes every retained file other than itself.
