# Independent acceptance of the finite coefficient bound

12 October 2026. This is the complete substantive mathematical audit of [the finite-bound proof](FINITE_COEFFICIENT_OBSTRUCTIONS.md). It reports the accepted historical independent verification. It is independent AI-assisted review, not external human peer review, journal acceptance or proof-assistant certification. Programs and raw computational certificates are not distributed in this appendix.

## Verdict and exact scope

**ACCEPT.** The frozen finite-tail bridge proves that every member of either the ternary-digit family or the base-four-digit family has a total product coefficient outside \(\{-1,0,1\}\) in degrees \(1\) through
\[
N_*=150,994,944=36\cdot2048^2.
\]
This is an explicit, deliberately conservative coefficient-only upper bound. No sharpness is asserted. The earlier combined-search endpoints 59 and 77 retain their original meaning: exhaustion of the coefficient-and-Jensen searches under their respective necessary analytic conditions. This bridge does not identify either endpoint as the first impossible coefficient prefix.

The two families are
\[
\prod_{m\ge1}\prod_{j\ge0}
(1+u_{m,j}q^{m3^j}+v_{m,j}q^{2m3^j}),
\qquad u_{m,j},v_{m,j}\in\{-1,1\},
\]
and
\[
\prod_{m\ge1}\prod_{j\ge0}
(1+a_{m,j}q^{m4^j}+b_{m,j}q^{2m4^j}+c_{m,j}q^{3m4^j}),
\qquad a_{m,j},b_{m,j},c_{m,j}\in\{-1,1\}.
\]
Unique base expansion ensures that each original factor indexed by \(m\) has all its local coefficients in \(\{-1,1\}\). The theorem covers every indicated digit sign. It does not cover arbitrary independent signs on all original factor coefficients. The original unrestricted sign-array problem remains open.

The accepted proof is reproduced in full in the accompanying public finite-bound proof. The preceding general-zero, full-ternary and full-base-four proof-and-review appendices provide its mathematical dependencies.

This is a separate audit. The previously accepted general-zero, full-ternary, and full-base-four packets remain unchanged. The bridge uses the complete-state exhaustion and analytic zero bounds already independently established in those packets. It does not infer completeness from equal totals alone.

## 1. Universal coefficient and analytic bounds

For an arbitrary original independent-sign array, the degree-\(n\) coefficient is the sum of exactly \(p(n)\) signed terms: a partition specifies the multiplicity selected in every original factor. Hence
\[
|A_n|\le p(n).
\]
This remains true in both digit subclasses, without any assumption that the total coefficients are small.

For \(t>0\), write \(E(e^{-t})=\prod_{m\ge1}(1-e^{-mt})^{-1}\). Nonnegative-term expansion gives
\[
\log E(e^{-t})
=\sum_{k\ge1}\frac1{k(e^{kt}-1)}
\le\frac1t\sum_{k\ge1}\frac1{k^2}
\le\frac2t.
\]
The last bound follows by comparison of the tail with \(\int_1^\infty x^{-2}\,dx\). These estimates also justify finiteness of the sums and product; no asymptotic partition formula is needed. Since \(p(n)e^{-nt}\le E(e^{-t})\), putting \(t=n^{-1/2}\) proves
\[
p(n)\le e^{3\sqrt n}\qquad(n\ge1).
\]
The degree-zero coefficient is 1 and is treated separately wherever necessary.

Analyticity in the open disk does not depend on an infinite good-coefficient hypothesis. For each original factor \(f_m(q^m)\), its nonconstant part on \(|q|\le r<1\) has modulus at most \(r^m/(1-r^m)\), whose sum over \(m\) is finite. Thus the product converges locally uniformly; its tail is nonvanishing on each sufficiently small compact neighborhood after taking logarithms of factors close to 1. Block zeros therefore persist, with multiplicities adding even when their locations coincide. These were proved in the preceding audits and their hypotheses continue to hold here.

Parseval applies on each circle strictly inside the disk, and Jensen followed by the concavity of the logarithm gives the same squared-norm lower bounds from any selected finite collection of known block zeros. There is no appeal to cancellation of zeros, no use of the behavior of the product only on a radial line, and no exchange of a finite-prefix assumption with an infinite coefficient bound.

## 2. Uniform unknown-tail estimate

The 21 radii are \(r=(b-1)/b\), with
\[
b\in\{2,3,4,6,8,12,16,24,32,48,64,96,128,192,256,384,512,768,1024,1536,2048\}.
\]
Let \(t=-\log r\). Then \(t\ge1/b\). For \(n\ge36b^2\),
\[
6\sqrt n\le n/b\le nt,
\qquad |A_n|^2r^{2n}\le e^{6\sqrt n-2nt}\le r^n.
\]
As \(N_*\ge36b^2\), summing only over \(n>N_*\) yields
\[
\sum_{n>N_*}|A_n|^2r^{2n}\le b r^{N_*+1}.
\]
The elementary binomial inequality
\[
\left(\frac b{b-1}\right)^b
\ge1+\frac b{b-1}>2
\]
implies \(r^b<1/2\). For all selected denominators,
\(\lfloor(N_*+1)/b\rfloor\ge73728\), because \(N_*/2048=73728\). Consequently
\[
\sum_{n>N_*}|A_n|^2r^{2n}
<2048\,2^{-73728}=2^{-73717}<\eta,
\qquad \eta=2^{-32768}.
\]
The strict inequality comes from \(r^b<1/2\); it is not lost when \(b=2048\). The independent checker evaluates the cutoff and exact denominator bounds at every radius, rather than substituting a numerical logarithm.

## 3. What the finite good prefix actually implies

Assume \(|A_n|\le1\) only for \(0\le n\le N_*\). In the ternary case its contribution is at most the full geometric series \(U^{(3)}_r=1/(1-r^2)\). Adding the unknown tail gives
\[
\sum_{n\ge0}|A_n|^2r^{2n}<U^{(3)}_r+\eta.
\]
Using a full geometric series for the prefix and then adding a tail overcounts some terms. It is a legitimate upper bound.

All signed products have \(A_n\equiv p(n)\pmod2\). Within the assumed good prefix, integrality forces \(|A_n|^2=\pi_n\), where \(\pi_n=p(n)\bmod2\), including \(\pi_0=1\). Since \(N_*>512\), the base-four prefix is bounded by
\[
U^{(4)}_r=\sum_{n=0}^{512}\pi_n r^{2n}
+\frac{r^{1026}}{1-r^2}.
\]
The geometric term covers all degrees from 513 onward, in particular those through \(N_*\). Adding the actual unknown tail proves the strict upper bound \(U^{(4)}_r+\eta\) for the full squared norm. No assertion about the parity density or individual coefficients beyond \(N_*\) is needed.

For \(a=b-1\), the exact rational envelope has denominator dividing
\(b^{1024}(b^2-a^2)=b^{1024}(2b-1)\). This follows directly by putting the finite sum over denominator \(b^{1024}\), then adding the geometric tail. The 513 parity bits and all 21 exact envelopes were independently verified in the preceding base-four audit; the present checker reuses those accepted rational values and checks the new inflation exactly with rational arithmetic.

## 4. Strict base-four margin, including all possible tested profiles

The accepted cubic root classification gives the lower bound \(R=1839/1000<T\), with \(T\) the real root greater than 1 of \(x^3-x^2-x-1\). Explicit substitution gives \(h(R)=-1568281/10^9\), and \(h\) is increasing above 1. A defect with quadratic sign negative contributes effective weight \(n\); with quadratic sign positive its two complex inner roots jointly contribute effective weight \(2n\). The latter is one effective contribution, not an extra factor of two in the defect count.

At a chosen radius, the active lower squared-norm bound is
\[
L=R^{2K}r^{2S}.
\]
Only defects with \(Rr^w>1\) are selected. Dropping other zeros only weakens the necessary lower bound. In the source's entire truncation domain through 78, every finalized edge has exponent at most 26 and capacity \(d_n=1+v_4(n)\). Thus even unreachable profiles satisfy
\[
K\le\sum_{n=1}^{26}d_n=33,
\qquad S\le2\sum_{n=1}^{26}nd_n=902.
\]
These totals were independently recalculated, including the extra multiplicities at 4, 8, 12, 16, 20, 24 and the additional one at 16.

A positive rational difference \(L-U^{(4)}_r\) is at least the reciprocal of the common (not necessarily reduced) denominator
\[
D=1000^{2K}b^{2S+1024}(2b-1).
\]
Since \(1000<2^{10}\), \(b\le2^{11}\), and \(2b-1<2^{12}\),
\[
D<2^{660+31108+12}=2^{31780}.
\]
Therefore every old strict rejection has
\[
L-U^{(4)}_r>2^{-31780}>2^{-32768}=\eta.
\]
The calculation is uniform over all active subsets and all possible tested profiles, not merely the rejected profiles observed in a run.

## 5. Strict ternary margin by an explicit integer norm

Let \(\varphi=(1+\sqrt5)/2\). For an active ternary profile,
\[
L=\varphi^{2K}r^{2S},\quad U^{(3)}_r=\frac{b^2}{2b-1},\quad
E=A\varphi^{2K}-B,
\]
where \(A=a^{2S}(2b-1)\), \(B=b^{2S+2}\). A strict old rejection is exactly \(E>0\). Also \(0<A<B\), since \(A/B=r^{2S}(1-r^2)<1\).

The conjugate of \(\varphi\) is \(\varphi'=1-\varphi=-\varphi^{-1}\). Hence
\[
E'=A\varphi^{-2K}-B\in(-B,0).
\]
This is valid also for \(K=0\), although no strict rejection occurs there. Reducing powers with \(\varphi^2=\varphi+1\), write \(E=u\varphi+v\) for integers \(u,v\). Then
\[
EE'=v^2+uv-u^2
\]
is a nonzero integer when \(E>0\). Therefore \(|EE'|\ge1\) and \(|E'|<B\) imply \(E>1/B\). Dividing by \(b^{2S}(2b-1)\) gives
\[
L-U^{(3)}_r>\frac1{b^{4S+2}(2b-1)}.
\]
Every finalized ternary defect in the source's entire truncation domain through 60 has exponent at most 30 and multiplicity at most \(1+v_3(n)\). Consequently
\[
S\le\sum_{n=1}^{30}n(1+v_3(n))=465+165+54+27=711.
\]
Thus
\[
b^{4S+2}(2b-1)<2^{11\cdot2846+12}=2^{31318},
\qquad L-U^{(3)}_r>2^{-31318}>\eta.
\]
This argument neither approximates \(\sqrt5\) nor assumes an unproved numerical separation between distinct algebraic quantities. The independent checker verifies the even-power recurrence \((u,v)\mapsto(2u+v,u+v)\), its unit norm, and the full-domain bound \(K\le44\), though the final separation does not require a bound on \(K\).

## 6. Exhaustiveness transfer and exact replay arithmetic

Increasing an upper envelope cannot create a new rejection. Sections 4 and 5 show that every formerly strict rejection remains strict after adding \(\eta\). The coefficient tests, available stage choices, and ordering of complete histories are unchanged. Induction over the finite search tree therefore proves equality of the entire retained state sets, not only equality of frontier counts. This analytical argument already transfers the earlier independently certified exhaustions.

The two replay sources were also checked character-for-character against the accepted originals after applying only these precise substitutions and output-path changes:

* Ternary: let \(s=2^{32768}\). Replace \(A\) by \(sA\) and \(B\) by \(sB+b^{2S}(2b-1)\), then use the original exact quadratic-field comparison. This is precisely \(L>U^{(3)}_r+1/s\).
* Base four: replace the rational numerator/denominator \((U,V)\) by \((sU+V,sV)\). The numerator uses the old \(V\), before the denominator is scaled. This is exactly \(U/V+1/s\).

There were no changes to combinatorial transitions, deferred choices, pool realization, coefficient recurrences, active-zero selection, or profile caching. Integer inflation occurs in arbitrary precision. The already verified guarded coefficient arithmetic remains in effect.

If a good prefix through \(N_*\) existed, its actual successive sign choices would give a path in the complete deferred search. Its coefficients satisfy all coefficient tests, and Sections 2–3 imply the inflated necessary analytic tests. Thus the path would survive to every level considered. The empty frontiers contradict this. The argument proves a genuine finite coefficient obstruction without assuming that the unknown infinite coefficient tail remains bounded by 1.

## 7. Independent computational evidence

The independent exact-arithmetic checker verifies the following:

1. Integrity of the accepted inputs, all complete-domain maxima, all 21 denominators, the uniform tail budget, both strict-margin bounds, and exact rational inflation of each previously verified parity envelope.
2. That the only replay-source changes are the stated rational inflations and output destinations.
3. Every byte of all 60 author-inflated ternary frontiers against the previously accepted original archive, and every byte of the complete author-inflated base-four tree against the previously accepted original compressed tree.
4. Exact agreement of both replay stdout logs with the accepted original logs.
5. Four intentionally uncertified parameter choices are rejected: cutoff one below the stated sufficient threshold, inflation exponent 10000, inflation exponent 80000, and a denominator bound 4096 without increasing the cutoff. These controls test the guards of this sufficient proof; their rejection does not assert that every modified mathematical statement is false.

Independent runs under normal Python, `-O`, and `-OO` produced byte-identical reports, so required checks do not disappear when assertions are disabled.

Both frozen inflated C++ programs were independently compiled and executed afresh with `-O2 -std=c++17 -fsanitize=undefined -fno-sanitize-recover=all`. They exited successfully. Every fresh ternary frontier byte and the complete fresh base-four tree matched the source inflated outputs; both stdout logs matched exactly. Ternary stderr was empty. Base-four stderr contained only the eleven expected progress lines and no sanitizer errors. The independent audit recorded these fresh replay results.

The retained totals are 831,371 ternary states and 11,151,089 base-four states. The ternary last nonempty level is 58 and level 59 is empty. The base-four last nonempty level is 76 and level 77 is empty. Complete-state equality, the prior independent reconstruction of every state, and the mathematical margin argument together support the accepted theorem.

## Final assessment

No mathematical or certificate defect was found in the frozen bridge. The unknown-tail estimate, strict algebraic and rational separation estimates, exact inflation, and transfer of complete-state exhaustion are sound. The accepted new conclusion is the explicit nonsharp bound \(150,994,944\) for each of the two digit families. It supplies neither a solution nor an obstruction for the full independent-sign partition problem.
