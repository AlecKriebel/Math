# Independent complex-dynamical adversarial audit of PR 46

Audit checkpoint: 2026-10-03 03:26 UTC. Mathematical-audit completion estimate: 100%. New-discovery credit: 0%.

**Exact mathematical claim verified. No mandatory correction to the original 13 scientific files was found.** This is a mathematical audit of a credited known-result correction, not an acceptance decision or external peer review. No Git, index, branch, remote, native status, or acceptance operation was performed.

## Scope, independence, and identity

Target: for each integer d>=2, the (2d+1)-dimensional real rational-map space Rat_d(R) contains a nonempty Euclidean-open subset whose complex projective periodic points, of every positive period, all lie in RP^1. The space consists of coprime homogeneous degree-d pairs modulo common nonzero scalar, before quotienting by conjugacy. The claim concerns all points fixed by every positive iterate, including infinity, without requiring any multiplicity convention.

Original PR head: `a39d178b10f75fb127058b08e0d0002b3ae97f8a`. The 318-file original-preparation manifest has SHA-256 `da37655e9b3bab420862a0c17c761e67fa9a4bc2028a328d033547249c54ad2e`. `ORIGINAL_INPUT_BINDINGS.json` binds all 13 scientific source files by exact size, SHA-256, and full mode 0444 to that manifest. The 13-file set was completely byte-read; JSON receipts were parsed, while the mathematical text and programs were inspected substantively. Repeated PASS entries are receipt data, not independent proof.

The mechanism in `INDEPENDENT_PRE_SOURCE_DERIVATION.md` was obtained and saved before candidate or earlier-review access. Its initial UTC minute label was rounded; the original file was created at approximately 03:19:30 UTC, preceding the candidate reads in the tool sequence. This family remained independent of the parallel algebraic proof family. Operator: Codex agent `/root/pr46_complex_dynamics_adversary`.

## Independent full-dimensional family

Let p_1<...<p_d be real, c_j>0, and B real. Define

f(z)=B+sum_{j=1}^d c_j/(p_j-z).

Its finite poles are simple and real. Its numerator and denominator have no common factor because the residue at every denominator zero is nonzero. Thus its degree is d. For y>0,

Im f(x+iy)=y sum_j c_j/((x-p_j)^2+y^2)>0.

It maps the upper half-plane H into itself, and maps the lower half-plane into itself by conjugation. Choose p_j=j, r=d+1, c_j=1/(10d), and B=r+sum_j c_j/(r-p_j). Then f(r)=r and

0<mu=f'(r)=sum_j c_j/(r-p_j)^2<=1/10<1.

This gives a strictly attracting real fixed point to the right of every pole, with B>r. There is no even/odd distinction and no failure at d=2.

In the denominator-monic chart, q has degree d with d free lower coefficients and p has d+1 free coefficients. The chart has 2d+1 real coordinates. The above partial fractions are a local parametrization: the d pole positions, d nonzero residues, and B recover p and q uniquely after ordering the poles. Under all sufficiently small real coefficient perturbations, the d simple real poles remain real and simple, their order persists, and the residues retain their strictly negative ordinary sign. A simple real root remains real because its unique continued root must equal its conjugate. The nonzero resultant and denominator degree also persist.

The fixed-point equation has derivative mu-1!=0 at r, so the real implicit-function theorem gives a nearby real fixed point r_f. Its multiplier remains in a compact interval (0,kappa) with kappa<1 after shrinking one neighborhood. We can also keep r_f>max_j p_j and B>r_f. These are strict open conditions in the full coefficient chart, not in a subspace fixing infinity. The construction therefore gives a single full-dimensional neighborhood for all periods.

## Uniform all-period proof, with every pole accounted for

For any map in that neighborhood, write r=r_f and mu=f'(r) in (0,1). The real orientation-preserving Möbius map M(z)=-1/(z-r) maps H to H. Let g=M f M^(-1), where M^(-1)(z)=r-1/z. Expanding at r gives

f(r-1/z)-r=-mu/z+O(1/z^2),

so g(z)=az+b+O(1/z), where a=1/mu>1. In particular infinity is a fixed point of g, attracting with local multiplier mu.

Every equation f(t)=r has one solution in each of the d-1 bounded intervals between poles, since f is strictly increasing there from minus infinity to plus infinity. There is also exactly one solution on the right exterior interval, namely r, since f rises from minus infinity to B>r. There is no solution on the left exterior interval, where f>B>r. These d real simple solutions exhaust the degree-d fiber. Infinity is not in this fiber because f(infinity)=B!=r.

The d-1 solutions t!=r become the finite poles P=M(t) of g. They are simple. At such a pole, (M^(-1))'(P)=1/P^2>0, hence the ordinary residue is

A=-P^2/f'(t)<0.

Conjugation preserves degree d. With d-1 finite simple poles, g has the exact partial-fraction form

g(z)=az+b+sum_{k=1}^{d-1} C_k/(P_k-z),  C_k>0, a=1/mu>1.

Consequently for every z in H,

Im g(z)=a Im z+(Im z)sum_k C_k/|P_k-z|^2 >= a Im z.

Iteration gives Im g^n(z)>=a^n Im z>Im z for every n>=1. Thus no point of H is fixed by any positive iterate. Conjugation rules out the lower half-plane identically. The only remaining sphere points are RP^1, so every complex projective periodic point is real.

The same inequality also shows g^n(z) tends to infinity for every z in H or the lower half-plane. Therefore f^n(z) tends to r there. Nonreal points in the attracting basin are included in the proof: they cannot form other attracting or indifferent periodic cycles. Poles and infinity are real; no nonreal orbit can hit a real pole because H and the lower half-plane remain invariant. In the original equal-degree chart, infinity maps to a finite point. In the conjugated chart, infinity is the attracting real fixed point. Both normalizations are explicitly covered.

No Julia-set classification, Denjoy-Wolff theorem, hyperbolic structural stability theorem, or claim about critical orbits is assumed here. The central difficulty is resolved by an explicit inequality rather than transferred to another unsupported assertion.

## Direct audit of the candidate construction

The original construction is

f_d(z)=prod_{j=1}^d (z+2j-1)/(z+2j).

All poles are negative, simple, and real. Their ordinary residues are negative, as follows by counting the signs of factors at z=-2j. For x>=0,

0<f_d(x)<1,

f'_d(x)=f_d(x) sum_{j=1}^d 1/((x+2j-1)(x+2j))

<sum_{j=1}^d 1/(j(j+1))=d/(d+1)<1.

Since f_d(0)>0 and f_d(1)<1, it has a fixed point r in (0,1), with 0<f'_d(r)<1. Therefore the same complex-dynamical mechanism verifies a full rational coefficient neighborhood of the candidate itself, for every d>=2.

There is an even stronger local check for the entire candidate neighborhood with the same residue sign. Write f=B-sum_j c_j/(x-b_j), b_j<0, c_j>0. On x>=0, f'>0 and f''<0. Positivity of the candidate coefficients implies f(0)>0 and finite positive B=f(infinity). Thus F(x)=f(x)-x is strictly concave, F(0)>0, and F(x) tends to minus infinity. Its unique positive root r satisfies F'(r)<=-F(0)/r<0 by the tangent inequality for a concave function. Hence 0<f'(r)<1. This verifies the real-attraction condition throughout a sufficiently small residue-preserving candidate neighborhood, without a period-dependent root continuation argument.

The candidate's separate algebraic proof is also internally consistent: homogeneous composition preserves coefficient positivity, real fibers and projective nonramification persist under composition, exact iterate degree is d^n, and the root-count parity argument needs at least d^n distinct real roots of a degree d^n+1 fixed-point polynomial. Its count is sufficient. It does not assume simplicity of every periodic point or confuse fixed points of f with fixed points of f^n. No common factor is introduced under projective composition. The full chart retains a free numerator leading coefficient.

## Falsification attempts and boundary cases

| Attempted stronger claim | Exact attack | Outcome |
|---|---|---|
| A real-fibered H-selfmap alone has only real periodic points | h(z)=(z^2-1)/(2z) has h(i)=i, h(-i)=-i, and h'(i)=0 | False; nonreal superattracting fixed points exist. |
| Swapping half-planes alone suffices | k=-h has k(i)=-i, k(-i)=i, and zero cycle multiplier | False; a nonreal superattracting two-cycle exists. |
| Every verified all-period map is interior | z-c/z, c>0, has strict imaginary growth but neutral infinity; az-c/z for any a<1 has nonreal fixed points +/-i sqrt(c/(1-a)) | False; bad maps approach the neutral boundary. Strict attraction is essential for the openness proof. |
| Perturbation checks in finitely many chart directions prove openness | Finite samples cannot control every direction or all periods | Rejected as a proof method; coefficient-root continuity and the single strict multiplier bound prove openness. |
| Reality of repelling periodic points suffices | Possible nonreal attracting cycles must still be excluded | Excluded directly by the half-plane growth inequality, including attracting basins. |
| Fixed infinity gives ambient openness | Fixing infinity removes a coordinate | Avoided: original family has denominator degree d and a movable finite attracting point. |

Degree d=2, odd d>=3, even d>=4, poles, infinity, cancellation, multiplicities, strictness boundaries, and the unbounded-period quantifier are covered by the general derivation. No counterexample to the exact target or original sufficient open family was found.

## Computations and reproducibility

`complex_checks.py` runs under `/usr/bin/python3 -B`, SymPy 1.14.0. The repaired run passes **101 exact controls**, including independent-family degrees 2 through 7, degree-two and degree-three periods dividing 1 through 3, conjugated pole reality and simplicity, the reciprocal multiplier/linear-part identity, candidate degrees 2 through 8, and the negative controls above. They are finite diagnostic controls, not the foundation of the all-degree/all-period proof.

The first run failed at a comparison of structurally different but algebraically identical symbolic expressions for the neutral-boundary fixed equation. It is preserved in `complex_checks_actual_capture`, including its exact source and stderr. The repair replaces structural equality by cancellation of the difference. The successful run is `complex_checks_repaired_actual_capture`. No input or mathematical assertion changed. Every actual proof-control computation and input-binding computation records the exact prelaunch source, operator, actual child PID, aware UTC start/end, exit code, and complete stdout/stderr bytes with hashes. The interpreter-version probe before these runs was a lightweight unrecorded probe; it is not used as computational evidence. The captured successful run independently records the version.

The candidate's submitted 51 checks and earlier 848-check receipt were inspected, but were not rerun by this family. Their success is a claim of the original files; this report's own fresh computational evidence is the 101-control capture. The parent audit may independently reproduce the original programs.

## Existing priority and scope limits

Fresh official arXiv browsing confirmed that [Kozhasov–Kummer v1](https://arxiv.org/pdf/2004.10003v1), submitted 21 April 2020, explicitly asserts an open subset of the full real rational-map space in Theorem 2, printed page 2, and proves the positive-coefficient/interlacing construction in Section 2.2, printed page 6. [The current v2](https://arxiv.org/pdf/2004.10003v2), revised 27 October 2020, retains the attracting-real-fixed-point interior example in Example 1, printed page 3; Lemma 9, printed page 5, gives the all-period statement from a nonrepelling real cycle of length at most two. The proof of Theorem 3, printed page 6, explicitly treats every positive iterate. The direct independent inequality above removes reliance on its cited classical theorem for the strictly attracting case.

The [official arXiv record](https://arxiv.org/abs/2004.10003) displays those version dates and no journal-reference field. Therefore retain existing-author credit to **Khazhgali Kozhasov and Mario Kummer**, and describe the checked source as a 2020 preprint result. This limited observation does not establish exhaustive publication history. The original report and exact PDF hash/source-specific audit belong to the parent audit; this family has not copied or independently redownload-hashed any foreign PDF/OCR/pixel body into its owned topology. The failed arXiv HTML fetch returned HTTP 406; PDF primary-source reading succeeded, so it leaves no mathematical gap.

Strongest independently verified result: the exact all-degree, ambient-open, all-period affirmative construction is valid. Remaining mathematical gap for that target: **none identified**. Remaining scope limits: no classification of the whole locus, no assertion that the whole locus is open, no Hermite result, no higher-dimensional-projective result, no novel discovery, no exhaustive journal history, and no acceptance approval. Recommended mathematical disposition is consistent with a known-result source correction. No paper or DOI package is prepared.
