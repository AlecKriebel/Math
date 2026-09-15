# Settings appendix: statement contract and proof boundary

**All Lean below is uncompiled source. No kernel-certified result is claimed.**
This supplements the original contract and records the narrowly selected
appendix extension, not a redefinition of any physical strategy or old theorem.

## Source and exact scope

Canonical manuscript: `cyclic_bell_exact_values_and_randomness/main.tex`, Git
blob `bbd0667c934d5a34dd9c8ced50df91515cb1308c`. The live GitHub excerpt at
`app:settings` / `eq:standard-tables` was read again. The manuscript is unchanged.
Its expected SHA-256 is retained from the repository manifest; this pass did
not independently reconstruct the full raw manuscript bytes.

Targets: the displayed four standard Fourier-phase tables, their maximum and
nonuniformity, the particular third-setting perfect anchor and its cross table,
the qubit exception, and the scalar observed joint min-entropy asymptotic.
The external self-testing theorem cited by the paper is not formalized here;
we explicitly realize the displayed tables. We do not assert a formal local
isometry identification with every source convention for that external theorem.
These claims are not universal impossibility theorems for two-input or
three-input Bell designs.

## Physical definitions, independently of the answer

Fix d>=2, labels in ZMod d, and ordinary representatives a.val,b.val,j.val when
offsets need not be integers. Write cis(t)=exp(i*t). The actual unit vectors are

    u_(alpha,a)(j) = exp(-2*pi*i*(a.val+alpha)*j.val/d) / sqrt(d),
    v_(beta,b)(j)  = exp( 2*pi*i*(b.val+beta)*j.val/d) / sqrt(d).

Each measurement consists of outer products of those vectors. PVM validity
comes from Fourier orthogonality and unit diagonal phase multipliers. Alice
has alpha=(0,-1/2); Bob has beta=(-1/4,-3/4). Thus delta=alpha-beta is exactly

    ( 1/4   3/4 )
    (-1/4   1/4 ).

The state is the existing normalized Phi_d. `phasePairProbability` is the
existing trace Born rule on its density and the actual projectors. It is not
defined by a sine ratio or by the target probability table. No bound,
maximality, uniformity, or desired probability is a validity hypothesis.
Bob's positive Fourier sign is implemented by a negative phase and outcome
inversion; outcome inversion is not silently equated with adjoint or entrywise
complex conjugation.

## Target formulas

With t=a.val-b.val+alpha-beta, the joint amplitude is d^(-3/2) times
sum_(j=0)^(d-1) exp(2*pi*i*t*j/d). A division-free geometric identity first gives

    sin(pi*t/d)^2 * |sum_j exp(2*pi*i*t*j/d)|^2 = sin(pi*t)^2.

Only after proving that the denominator is nonzero do we derive

    p(a,b) = sin(pi*t)^2 / (d^3*sin(pi*t/d)^2).

The resonant case is not evaluated by 0/0: equal offsets are separately shown
to give delta_(a,b)/d. Each full table is normalized and both marginals are 1/d.

For the four standard tables, the numerator is 1/2 and the maximum is

    1 / (2*d^3*sin(pi/(4*d))^2) > 1/d^2.

The upper bound is proved for every pair and an attaining pair is exhibited.
For delta=3/4 use a=0,b=1; for delta=+/-1/4 use a=b=0. Existence of outcome 1
uses d>=2. A floor-and-integer argument folds ANY n+r/q into [0,d), then into
[0,d/2], and proves its distance is at least 1/q. No nearest-representative
hypothesis is supplied by the caller. The original sum a-b is not confused
with the a+b target of the cyclic counterexample elsewhere in this companion.

## The actual anchor

A third Bob input `none` uses beta=alpha_c for a chosen c in Fin 2; existing
inputs are `some y`. All four previous tables are unchanged. The pair x=c,
y=none perfectly matches equal labels. The cross pair x!=c has numerator one,
maximum 1/(d^3*sin(pi/(2*d))^2), and a=b=0 attains it. This exceeds 1/d^2 for
d>=3. Every entry equals 1/4 at d=2; the strict statement excludes that case.

## Entropy

`standardJointMinEntropy` is minus the base-two logarithm of the proven attained
peak. The table-maximum theorem supplies its scalar observational meaning.
It is NOT private entropy conditioned on Eve. The exact expression is

    log(2*d^3*sin(pi/(4*d))^2) / log(2).

The o(1) assertion is stated as an actual sequential limit:

    H(d) - log(d)/log(2) -> log(pi^2/8)/log(2), as d -> infinity.

The proof script composes the punctured sin(x)/x limit with pi/(4*d), handles
its eventual nonzeroness explicitly, then applies log continuity at pi^2/8>0.
Finite numerical samples are not a verification of this limit.

## Dependencies and exclusions

The new source relies on the shared physical model, Fourier basis, and phases.
Its import closure excludes the all-dimensional scalar extremum, the Bell
upper bounds, the concrete cyclic-maximizer endpoints, and the support-rigidity
chain. The full standard build still imports all prior candidates and all new
audit files. We do not omit hard old modules to report a successful build.

No Lean has run, so formal acceptance, transitive axiom sets, and independent
statement correspondence remain pending for every new and old endpoint.
