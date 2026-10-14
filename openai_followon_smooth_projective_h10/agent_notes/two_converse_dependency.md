# Pivotal pointwise 2-converse audit

Follow-up checkpoint (2026-10-06 22:27 PDT): the original Kato source was
subsequently inspected in memory, and a deeper reconstruction of
`cyclotomic.tex:315–748` is saved in
[two_converse_cyclotomic.md](two_converse_cyclotomic.md). That note closes
the initial Kato source-access concern and supports the uniform arithmetic
error calculation conditional on the preceding perfection/residual interface.
It does not certify the whole companion. The 30% figure below records the
earlier checkpoint; my later whole-companion audit estimate is 45%.

Closing assigned-slice checkpoint (22:37 PDT): the cyclotomic note now
includes an independent reconstruction of the preceding perfect/residual
complex and the exact bounded real-place duality error, plus a formal
universal convention repair. The assigned non-CM cyclotomic arithmetic
audit is complete (100%), with no unsupported step found in that scope.
Whole-companion promotion remains the root researcher's separate decision.

Checkpoint: 2026-10-06 22:16 PDT (2026-10-07 05:16 UTC).
Auditor: independent internal dependency agent. Estimated completion of a
full independent audit of this companion: **30%**. This is an audit-progress
estimate, not a probability that the claimed theorem is true.

## Status and scope

**Not certified; not falsified by this audit.** The source contains substantial
proof bodies for the new assertions. I did not find a checkable counterexample
or a demonstrably false step in the portions examined. I also did not complete
independent verification of the simultaneous arithmetic machinery needed for
its pointwise conclusion. Its release, repository presence, and theorem label
are not validation evidence.

Read-only source:
`/Users/alec/Desktop/math/preprints/A-pointwise-2-converse-for-elliptic-curves-with-rational-two-torsion-September-24-2026`.
The source checkout reported exact HEAD
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
No source edits, git mutations, downloads, or external communication were
performed. Web retrieval was read-only primary-source inspection.

The companion has approximately 7,063 section-source lines. I examined the
main statement, preliminaries, the cyclotomic interpolation proof, auxiliary
nonvanishing argument, coefficient construction and symbol interface, graph
address construction, pointwise assembly, and the pivotal local-switch,
evaluation, outer-limit, central-determinant and clearing passages in the
ring-class proof. Some of these were read as dependency interfaces rather than
fully reconstructed proofs; this distinction matters below.

## Exact consequence Family004 needs

Theorem 1.1 in `build/sections/introduction.tex:22` asserts, for every
elliptic curve E/Q with nonzero rational 2-torsion and full 2-power Selmer
corank s in {0,1}, analytic rank = algebraic rank = s and finite whole Sha.
The actual Family004 use is in `03-parity.tex`, Lemma `par:global-point`.
Its preceding descent gives

    r(E_l) + dim_F2 Sha(E_l)[2] = 1.

If t is the corank of Sha(E_l)[2∞], then t <= dim Sha[2], so the full
Selmer corank r+t <= 1. This does verify the companion theorem's stated
input. In particular it does not incorrectly substitute the dimension of
Sel_2 for full Selmer corank.

However, the downstream argument only needs **finite Sha(E_l)[2∞]**.
Whole-Sha finiteness and analytic rank are excess conclusions. For a finite
2-primary group the perfect alternating Cassels–Tate pairing forces paired
cyclic factors, hence an even dimension of Sha[2]. The displayed equation
then forces r=1 and Sha[2]=0, so the selected Selmer class (beta,1) is in
the rational Kummer image.

One can sharpen the exact unresolved alternative without using the
companion. Cofinite generation writes Sha[2∞] as
(Q_2/Z_2)^t plus a finite group F. Cassels–Tate is nondegenerate modulo
the divisible radical, and its alternating finite quotient forces
dim F[2] even. Thus the displayed equation leaves exactly:

* desired case: r=1, t=0, F=0;
* obstruction: r=0, t=1, F=0, hence Sha[2∞] is Q_2/Z_2.

The obstruction is compatible with the Selmer dimension, the full Selmer
corank bound, and the Selmer-parity theorem. It is precisely what must be
excluded. An alternating pairing on Sha[2] alone cannot do this: the
restriction of the pairing can be degenerate, and the divisible group has
a one-dimensional subgroup killed by 2.

For s_2=0 alone, r=0 and finite Sha[2∞] follow directly from the Kummer
corank identity and cofinite generation. The genuinely necessary new input
here is the **corank-one case**. A statement that low Mordell–Weil rank
implies finite Sha would not repair it.

## Dependency mechanism, rather than theorem slogans

The proof's pointwise route is:

1. A fixed-form Kato class, real-place class, and positive global determinant
   yield a scalar u in Lambda[1/2][G], with a uniform integral denominator.
   Its constant-term valuation is the normalized central L-value valuation
   minus active-prime weights and the Sha length.
2. A binary congruence lemma returns a uniformly bounded nonzero value from
   some nonzero cube vertex to a corank-zero missing vertex.
3. Half-integral weight coefficients, divided local operators, and trace
   identities yield finite binary symbols with contraction and isolation.
   Finite prime networks make every nonzero cube address a coefficient unit.
4. A ring-class determinant construction supplies a uniform lower bound for
   Heegner-point indices. This uses integral local switches and an outer DVR
   limit to handle losses at 2, rather than invoking an odd-prime theorem.
5. Bounded-factor negative companions and an explicit height comparison
   combine the even upper estimate with that ring-class lower bound to
   normalize the moving odd coefficient detector.
6. A fixed final negative companion k is chosen before cube dimension b.
   Networks make both the odd h detector and even hk detector units at all
   nonzero addresses. Ring-class missing-vertex interpolation then proves a
   simple zero at the original corank-one curve. Only afterward is the
   established forward Gross–Zagier–Kolyvagin implication invoked.

The proof expressly separates the detector's fixed genus partner h_*, the
varying bounded-factor companion k'(h), and final fixed companion k. I did
not find a circular use of the odd minimum in its stated lower-bound proof:
`pointwise.tex:474` derives that lower bound from the even construction,
ring-class bound, and height ratio before the odd normalization is used.

## Parts independently checked at the algebraic-interface level

These checks establish only the stated interfaces, subject to the arithmetic
objects having the properties required by them.

* **Integral Fourier intersection** (`cyclotomic.tex:102`): Fourier inversion
  places each group coefficient in Lambda[1/2]; intersection with the
  2-adically completed localization O is Lambda. No cube-size denominator
  is lost once the uniform O[G] integrality premise is genuinely available.
* **Binary congruence** (`cyclotomic.tex:121`): a character-value function has
  Boolean monomials divisible by 2 to at least their support size. The j-th
  binary digit has degree at most 2^j. The product indicator for r tests
  modulo 2^M has total degree at most r(2^M-1), so a cube of larger dimension
  has an even number of common zeros. Since the origin is one, another
  exists. This is a valid finite argument, not a density claim.
* **Transfer through the bounded factor** (`ring-determinants.tex:1648`): if
  f_x u_x=d_x with integral O[G] f,d, regular u_x, bounded negative support
  of f modulo 2^M, and nonzero f_0(0) of valuation c, the tested coefficients
  give v(u_x(0)-u_0(0)) >= M-2c. The proof correctly tests only the constant
  coefficient of d and handles the other convolution terms using the
  uniform denominator of u supplied by integral d/f.
* **Terminal minor estimate** (`ring-determinants.tex:709`): after a nonzero
  (n-1)-minor is available in a square two-term complex with generic kernel
  rank one, Schur elimination gives u=±alpha beta/det A. The resulting
  valuation bound is valid. Bounded matrix size alone is insufficient;
  the paper itself correctly gives [2^i] as the warning example.
* **The final Cassels–Tate deduction** in Family004 is valid if 2-primary
  finiteness is established. It uses the full finite 2-primary group, not an
  unjustified perfect pairing restricted to Sha[2].

The exact determinant-switch argument (`ring-determinants.tex:473`) is
plausible at its abstract interface: the finite and singular localization
vectors are J-related, unimodular cross pairing gives unit exterior volumes
even for nonprimitive vectors, and strict torsion is common to the two
triangles. I did not produce a counterexample to this algebraic statement.
I have not independently constructed the required arithmetic triangles and
functionals, so this is not certification of its arithmetic application.

## Primary-source checks

Read [Cai–Shu–Tian, Explicit Gross–Zagier and Waldspurger formulae,
arXiv:1408.1733v2](https://arxiv.org/pdf/1408.1733), Theorem 1.1 on pp. 1–2.
Its character-sum normalization has a height multiplier c sqrt(|D|), the
level/discriminant factor, the unit factor, and the fixed modular degree.
Under the companion's split-level and conductor-coprimality hypotheses,
the pointwise height comparison (`pointwise.tex:427`) is consistent with
this formula: dividing the conductor-|h| ring-class sum's height by the
conductor-one genus sum's height leaves sqrt(|hk|) L(E^(hk),1), up to fixed
factors and bounded projection indices. In particular, this source check
does **not** reveal a missing product over the conductor primes. It verifies
the relevant normalization, not all prior existence/local-orientation claims.

Read [Howard, The Heegner point Kolyvagin system,
arXiv:1202.6340v1](https://arxiv.org/pdf/1202.6340), introduction/Theorems A and
B. Theorems there impose odd p and strong image hypotheses; its Iwasawa
theorem additionally imposes ordinary reduction and other conditions.
Those statements cannot directly certify the companion's integral p=2
switch and limiting deformation. The companion acknowledges that and gives
its own constructions; the outstanding obligation is to verify those new
constructions, not merely to declare the Howard citation inapplicable.

Kato's primary page was retrieved from
[Numdam](https://www.numdam.org/item/AST_2004__295__117_0/), but the PDF fetch
was rejected by the web tool's size limit. I did not independently inspect
the full stated Kato section/theorem hypotheses. Consequently the fixed-form
integral projection and rational divisibility used in `cyclotomic.tex:315–595`
remain a primary-source validation gap in this audit. No local download was
attempted, respecting the project's current disk constraint.

## Central unverified obligations (not proven defects)

These are specific places where the new proof carries the central difficulty.
The obligations include compatibility among constructions, not just a list of
individually plausible abstract lemmas.

1. **Uniform fixed-form integral cyclotomic determinant**.
   `cyclotomic.tex:315–625` must furnish actual Kato classes projected to one
   fixed elliptic Tate lattice for all tame conductors, unsmooth them over
   O[G], reconcile Euler conventions integrally, and establish both rational
   height-one divisibility and a uniform O[G] denominator for the *same*
   determinant coordinate. Its central formula (`:629–748`) then must use
   full Kummer conditions so that unused Euler factors cancel exactly and
   every active prime contributes t_q. The final binary argument cannot
   replace any of these arithmetic facts.

2. **Arithmetic integral p=2 derivative switch**.
   `ring-determinants.tex:182–409` asserts one fixed integer L for arbitrarily
   many active/derivative primes, integral descent, full Kummer behavior at
   2N, and the exact limiting identities f(P_Iℓ)=0 and s(P_Iℓ)=J f(P_I).
   The proof pays attention to the division by two in ell(ell+1)/2 and to
   bounded torsion descent ambiguity. Independent verification must check
   the finite transferred cocycles, local lifts and boundary witnesses at
   one shared precision, and then their compatibility after every later
   derivative prime. A bounded error paid separately at every prime would
   destroy the asserted uniformity.

3. **All-sequence and outer-limit evaluation, including new cycles**.
   `ring-limits.tex:630–848` claims an injection of limiting H^1 into abstract
   crossed-cocycle classes on products of Galois groups, exact-kernel
   restriction, and the same injection after the outer DVR quotient.
   Outer cycles may be represented only by approximate inner cycles. The
   proof explicitly retains degree-two evaluation matrices so the cocycle
   error goes to zero. This is the key mechanism that the simple [2^i]
   bounded-size counterexample lacks. It needs a complete simultaneous
   reconstruction; mere perfectness or bounded residual dimensions do not
   imply it.

4. **Uniform outer rank reduction and paired functional**.
   `ring-determinants.tex:745–881` uses the preceding evaluation interface,
   irreducibility, finite Chebotarev realization and exact determinant
   switches to reduce emergent outer H^1 to rank one and expose a nonzero
   minor. The paired functional must have a single bounded clearing exponent
   across all fields K of bounded ramification count. The claimed bound
   2j_h >= 4w(h)+s(h)+s(hk)-C(E,A) depends on this. Replacing the argument
   by odd-prime Kolyvagin theory or by a rank bound does not establish it.

5. **Weighted theta bridge and level-prime trace support**.
   `coefficients.tex:256–531` explicitly defines local Schwartz weights and
   counts optimal-embedding/orientation multiplicities to compare a modular
   coefficient with reduced genus-character Heegner sums. Uniformity in
   the moving detecting prime and precision is crucial. The subsequent
   weight-two trace construction (`:793–1028`) needs exact level exponent
   one, primitive ramified quadratic determinant on every new constituent,
   and omission of the *whole rational prime*. Without those verified facts
   the forest/graph identities are not arithmetic identities.

6. **Binary-family bounded clearing and final common stage**.
   `ring-determinants.tex:1464–1599` must obtain bounded-size Schur elimination
   with augmentation equal to the old fixed-base complex and negative
   Laurent support bounds independent of b and #Q. The final assembly in
   `pointwise.tex:872–1058` must realize both coefficient tests in the same
   enriched graph alphabet, choose k before b, and choose an actual stage
   only after a finite network and its precision requirements are fixed.
   The finite graph result cannot by itself supply the uniform arithmetic
   valuation bound needed by interpolation.

The broad-companion 2-converse is expressly not an input to this proof.
Switching Family004's citation to that unrestricted companion would create
another pivotal dependency, not independently repair any of these items.

## Exact repair target and promotion rule

A smaller arithmetic lemma sufficient for Family004 is:

    For every positive squarefree l prime to 6 with l≡3 (mod 4),
    l≡2 (mod 3), and the matrix hypotheses of par:descent,
    Sha(E_l/Q)[2∞] has no nonzero divisible subgroup.

Equivalently in this descent setting, show r(E_l)=1 or show the selected
class (beta,1) lies in the rational Kummer image. Since the finite quotient
is forced to vanish by Cassels–Tate, this excludes exactly the corank-one
divisible obstruction above. A constructive rational point for every such
matrix instance would also suffice, and would avoid needing the full
pointwise 2-converse.

For promotion, either independently verify the six simultaneous arithmetic
obligations above or replace the companion by a proved lemma covering all
of Family004's constructed l, including both l=n and l=n theta. Validating
some numerical instances, a density-one result, or known nonvanishing twists
does not cover those prescribed instances. No unconditional H10 conclusion
should be promoted from this audit status.
