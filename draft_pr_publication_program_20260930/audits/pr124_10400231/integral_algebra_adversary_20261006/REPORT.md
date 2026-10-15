# PR 124: independent adversarial integral-algebra audit

Verdict: **PASS_INTEGRAL_ALGEBRA**. No mandatory mathematical correction was
found within this audit's scope. The determinant multiplicity obstruction is
correct for the actual square presentation asserted in the submitted proof.
It cannot be inferred from an arbitrary gcd order alone. The exact remaining
scope boundary is independent topological validation of that presentation and
its specialization; no computation below certifies topology.

This audit concerns numeric problem 10400231, original PR head
`d110ad761291aa6ac1d66d2a49e8b8212c18bed6`, and submitted artifact
`COUNTEREXAMPLE.md`, SHA-256
`483bc7e3dccd4d6d262d36341becdf05bfa22f7d52e721eae4f51ecdc0fb95e5`.
The original submitted effort remains 2/5; this is validation of that candidate,
not a new central-proof search turn. No novelty, priority, human-peer-review,
or current-literature-status conclusion is made.

## 1. Independent starting point and exact claim

`INDEPENDENT_ALGEBRA.md` was written at 2026-10-06 19:42:43 UTC before reading
the submitted proof, prior imported report, old independent review, or source
conventions. After that reasoning was recorded, the full source record,
nonempty imported prior report, and submitted proof were read. The old review
was compared only after the fresh exact checker and core argument existed.

Let `R = Z[t,t^-1]`, let `A` be an `n x n` matrix over `R`, and let
`D = det A`. For every prime `p`,

\[
\operatorname{ord}_{t=1}(D\bmod p)
\geq \dim_{\mathbb F_p}\operatorname{coker}(A(1)\bmod p).
\]

The zero polynomial has order infinity. The determinant of the empty matrix
is one, and the cokernel of the corresponding map between zero modules is
zero. If `coker A(1) = T` is finite, the right-hand side is
`dim_Fp(T tensor Fp)`. If instead `coker A(1)=Z^b direct-sum T`, it is
`b+dim_Fp(T tensor Fp)`. These are different interfaces.

**Proof.** Reduce coefficients modulo `p`. Constant invertible row and column
matrices over `Fp` bring `A(1)` to `diag(I_(n-r),0)` with
`r=dim_Fp coker(A(1) mod p)`. Apply those same matrices to `A(t)` over the
Laurent ring. Every entry in each of the final `r` rows evaluates to zero at
one. The kernel of evaluation `Fp[t,t^-1] -> Fp` is `(t-1)`, so one factor
`t-1` can be taken from each such row in the determinant. Constant invertible
operations multiply the determinant only by a nonzero field constant. This
proves the claim, also when the reduced determinant is zero. Alternatively,
the same argument takes place in the DVR `Fp[t]_(t-1)`, where `t` is a unit.
No derivative argument is needed in characteristic two or any characteristic.

Tensoring a presentation with `Z=R/(t-1)` and then with `Fp` is right exact.
Thus `coker(A(1) mod p) = (coker A(1)) tensor Fp`; there is no need to assert
flatness or to preserve injectivity at the left of another exact sequence.

## 2. Why the nonprincipal Fitting and finite-module attacks matter

`R` is a UFD, but is not a PID. For

\[
N=R/(p,t-1),
\]

the rectangular presentation is the one-row matrix `[p, t-1]`.
Its zeroth Fitting ideal is `(p,t-1)` and its gcd order is `1`.
The ideal is proper: evaluation at one modulo `p` kills both generators but
does not kill `1`. It is nonprincipal: any common divisor of `p` and `t-1`
is a unit, so a principal ideal with those same generators would be all of
`R`. Yet `N tensor_R Z = Z/p`, of `Fp` dimension one. It follows that

\[
\operatorname{ord}_1(\operatorname{ord}(N)\bmod p)=0<1.
\]

This is an actual pseudonull finite module: it has `p` elements and support
at the height-two maximal ideal `(p,t-1)`. Replacing its Fitting ideal by a
gcd loses precisely the information relevant to specialization. In
particular, specialization of a gcd order is not the same operation as
specialization of the Fitting ideal.

For a genuine square presentation, there is a sole maximal minor, so
`Fitt_0(coker A)=(det A)` and its gcd order is the same determinant up to
an `R` unit. The above rectangular module cannot secretly replace the
module presented by that square matrix: its nonprincipal Fitting ideal
already rules out such an identification. Nor may one use a rationalized
or pseudo-isomorphic module in place of the full integral cokernel.

The submitted proof expressly presents the full cyclic-cover first homology,
retaining all constant torsion relation columns. Therefore this attack
identifies a real necessary hypothesis, but finds no violation of it in the
submitted algebraic construction.

## 3. Actual torsion-block construction and lift ambiguity

Suppose the cut group has the full decomposition
`G=Z^m direct-sum direct-sum_j Z/d_j`, and the surface contributes `m`
relations. Present `G tensor R` with `m+r` generators and the `r` diagonal
torsion relation columns. Lift the surface relation images to those
generators. The quotient has the genuine square presentation

\[
A(t)=\begin{pmatrix}B(t)&0\\C(t)&D\end{pmatrix},
\qquad D=\operatorname{diag}(d_1,\ldots,d_r).
\]

Here `C(t)` is not generally zero. The determinant is
`det A=(product_j d_j) det B`, independently of `C`, but the specialization
group can depend on `C`. Every coefficient retains the integer factor
`product_j d_j`. In particular, a primitive submitted polynomial cannot
hide nontrivial cut-group torsion in this construction.

A legal change of lift adds a multiple of a torsion relation column to a
surface column. This is an elementary column operation with determinant
one; it preserves the presented module and its specialization. Choosing a
different torsion class in `C` is a change of the map itself, not merely a
change of lift.

An explicit distinction is the family

\[
A_c=\begin{pmatrix}1&0&0\\0&p^2&0\\0&c&p\end{pmatrix}.
\]

All have determinant `p^3`. At `c=0` the cokernel is
`Z/p direct-sum Z/p^2`; at `c=1` it is `Z/p^3`, because the relation
`p^2 e_2+e_3=0` gives `p^3 e_2=0`. The case `c=1+3p` is a legal lift
change from `c=1`, with the same cokernel. Exact Smith-minor calculations
check these three cases for six primes.

The cited [Alcaraz v1 preprint](https://arxiv.org/pdf/1406.2042v1), p. 15,
displays a block-diagonal simplification. This is not a justification for
discarding arbitrary torsion coordinates. The submitted proof constructs
the lifted columns directly and therefore does not rely on that
simplification. Its rational rank input and integral module interface are
kept distinct.

## 4. Candidate, normalization, and boundary cases

The submitted pair is

\[
H_p=\mathbb Z\oplus(\mathbb Z/p)^3,
\qquad \Delta_p=t+(p^3-2)+t^{-1}.
\]

It is reciprocal with exponent zero, has integer content one, and evaluates
to `p^3`. The exact identity

\[
t\Delta_p=(t-1)^2+p^3t
\]

shows that its nonzero mod-`p` reduction has order exactly two. For `p=2`,
this is `t^-1(t+1)^2`; the order is still exactly two. The target finite
group has `Fp` dimension three. Accordingly, no genuine square
presentation with determinant `Delta_p` can specialize to `(Z/p)^3`.

The relevant submitted interface is `coker A(1)=T`, with the free `Z` in
`H_1(M)` arising externally from the re-gluing sequence. Setting
`coker A(1)=H_p` instead would make `det A(1)=0`, contradicting
`Delta_p(1)=p^3`; that is not the claim submitted.

Matching the number `p^3` alone is insufficient. There are actual square
presentations for the same polynomial with different groups:

\[
[\Delta_p],\qquad
\begin{pmatrix}p&t-1\\-(t-1)/t&p^2\end{pmatrix}.
\]

Their specializations are respectively `Z/p^3` and
`Z/p direct-sum Z/p^2`. Their mod-`p` nullities are one and two, both
consistent with order two. These are algebraic examples, without any
claim to topological realization.

Multiplication by `+/-t^k` preserves order at one. Inversion does too,
since `t^-1-1=-(t-1)/t`. Removing a factor `t-1` changes the order and is
not a unit operation. The submitted integral determinant has nonzero
evaluation at one, so it has no such factor over `Z`. Removing integer
content divisible by `p` can turn a zero mod-`p` determinant into a nonzero
polynomial; it is also not an `R` unit operation. For example
`diag(p,p)` has determinant `p^2`, order infinity modulo `p`, and
specialization `(Z/p)^2`; its primitive part `1` would wrongly have order
zero. The source convention retains that content.

The edge cases cause no contradiction: an empty matrix gives determinant
one and torsion rank zero; a matrix whose reduction has zero determinant
has infinite order; a constant torsion determinant divisible by `p` also
has zero reduction, not order zero. A positive free rank in the actual
specialization adds that free rank to the nullity bound.

## 5. Source pins and exact reproducibility

The [published conjecture](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf),
printed p. 542 / PDF p. 170, prescribes the full rank-one abelian group,
not just its torsion cardinality, and uses the free-abelian quotient ring.
The [Massuyeau author preprint](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/massu.pdf),
Definitions 3.1 and 3.5 and equation (3.2), defines the integral module order
by the gcd of maximal minors up to Laurent units. This agrees with a full
square determinant and introduces neither content removal nor `t-1`
cancellation. Complete relevant pages were read as text; the conjecture,
order definitions, and Alcaraz presentation were also visually inspected.

The downloaded PDF hashes match the originals' source manifest:

| Source | SHA-256 |
|---|---|
| Ohtsuki | `33d9c18c9ab8403a4d88b978b366451383edd12dd24760a77b9e25b666d9a8fd` |
| Massuyeau | `38e28f1b1c5c7dc14c487aa010da6925ba53b615722ff40e36883440de0cfa6a` |
| Alcaraz v1 | `39e79189a153b22b10ef26bbf36821226a161b6085f334175fdd98a1287de734` |

PDFs, full extracted text, and rendered pages remain in the ignored
`private/` directory. `SOURCE_ACQUISITION.json` retains file hashes and
actual extraction/render process PIDs, exits, and output hashes.

`audit_exact.py` uses sparse integer Laurent polynomials, exact determinant
expansion, exact binomial expansion at one, finite-field rank, and Smith
invariants from integer minors. The fresh suite executes 3,360 explicit
exception-based checks across 673 matrix cases, including all 256 two-by-two
matrices in a small Laurent family over `F2`, 384 seeded integral matrices,
candidate/group fixtures, and boundary cases. Both normal and `-O` runs
pass with identical stdout SHA-256
`e5a2c13470fa75f6dd934ce92f0b6ee43c8d0bf8ecbefe8160cb6ccbbdb815b8`.

Eight mutations each fail in both modes: wrong finite multiplicity, assigning
order zero to the zero polynomial, wrong empty determinant, dividing integer
content, dropping a torsion relation column, subtracting an unauthorized
`t-1` factor, using cardinality valuation as nullity, and applying the square
bound to a rectangular gcd order. In all, `RUNS.json` records 22 actual
subprocesses, their PIDs, exact arguments, UTC times, exits, complete stdout
and stderr, and output hashes. Its SHA-256 is
`1d9de06bb8df962d9771e5aaeaffbee305bc9116769845d506345f82fa429bad`.

The original author verifier was copied into isolated private replay folders;
authenticated original input hashes stayed unchanged. Its normal replay
reports 8,967 assertions and 5,312 cases. A forced-false assertion fails
normally but passes under `-O`, with the same reported count. Thus optimized
execution of that assertion-based checker is not predicate validation. This
is a diagnostic robustness limitation; it does not invalidate the proof or
the fresh explicit-exception checks.

## 6. Strongest verified result and exact remaining obligation

The independently proved algebraic result is the square determinant/nullity
inequality. The exact source conventions and candidate arithmetic satisfy
its hypotheses once the submitted topological presentation interface is
established. Nonprincipal Fitting ideals, pseudonull finite modules, torsion
lift choices, content, Laurent units, generator inversion, characteristic
two, empty matrices, and zero reductions supply no algebraic escape.

The remaining topological obligation for a complete nonrealizability verdict
is to verify, independently of these computations: the connected primitive
cut surface, the free rank `2g` of the cut group, the full integral
cyclic-cover cokernel, and the integral re-gluing identification
`coker A(1)=T`. This audit checks the algebra when those facts hold, rather
than computationally asserting them. The old independent review agrees with
this algebraic conclusion, but its verdict is not used as proof. No other
current review was consulted.

No branch, index, native research service, GitHub, Sheets, Zenodo, release,
push, or outreach operation was performed by this audit. All new work is
contained in its dedicated folder.

The public members are sealed in `SHA256SUMS.json`; that manifest excludes
itself and the ignored private material. `verify_seal.py` checks the seal
without writing files. To repeat the author/source-acquisition runners,
first copy this audit directory, because those runners write their ledgers.
Sealed originals must not be overwritten by a replay.
