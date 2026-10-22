# Root review of the original gamma-filtration target

PR1271, problem30003042 / OWR-14213-008. The current root mathematical
assessment supports the full negative answer at n=8. All four mathematical families have now sealed; root authenticated their
explicit members and input receipts and reproduced their actual executable
checks in normal, -O and -OO modes. MATH_GATE.json binds the final mathematical
assessment. Priority and publication gates remain separate requirements. This
document supplies no publication clearance.

## Exact hypotheses and success condition

The complete contribution in OWR5/2016, printed226–227, fixes a nondegenerate
odd quadratic form phi of dimension2n+1 over F, its maximal orthogonal
Grassmannian X, division even Clifford algebra A of index2^n, and
K=F(SB(A)). Conjecture3 prohibits the distinguished K-theoretic special class
e_n from gamma^(n+1-floor((n+1)/2))K(X_K), for n>=8. A single permitted
instance at n=8 with e8 in gamma5 refutes that universally quantified claim.
No assertion about all n, an optimal replacement, or a different
Chow-to-associated-graded conjecture is needed.

The 2016 final preprint a16i5, pp3–5 and9–12, has exactly this setup and the
pointwise implication. I read those parts, the relevant definitions, and the
complete printed proof of Theorem4.3 and the p12 implication. The target and
critical pages were freshly viewed as images; precise scopes and input hashes
are in ROOT_PRIMARY_VISUAL_READING.json. In particular, extension to a splitting
field preserves the gamma filtration, while it can change the topological
filtration. These filtrations must be identified over the required K itself.

## Existence and field matching

The primary paper explicitly supplies maximal-half-Clifford-index models over
extensions of any base field. Independently, the candidate adversary proposed
the following concrete characteristic-zero existence argument, which root
checked algebraically after its checkpoint. Take
F=C((t1))...((t16)) and phi=<1,-t1,...,-t16>. The generators ui=e0*ei of its
even Clifford algebra satisfy ui^2=ti and ui*uj=-uj*ui for i!=j. The usual
Clifford basis consists of 2^16 ordered monomials u_I. Assign u_I the valuation
half the sum of the distinct basis values v(ti) for i in I. These values occupy
distinct cosets modulo the rank16 valuation group of F. A nonzero linear
combination therefore has a unique lowest-valued term. Multiplication of
ordered monomials has nonzero leading coefficient, so the product of two
nonzero elements has a unique nonzero leading term. The finite central simple
even Clifford algebra has no zero divisors and is division. Its dimension is
2^16 and degree is256, giving the exact original index assumption.

Set psi=phi orthogonal-sum <-t1*...*t16>. Its dimension is18 and its signed
discriminant is the square (t1*...*t16)^2. The standard Clifford/subform
identities, also recorded on a16i5 pp3–4, identify either half algebra with
C0(phi) and either maximal even Grassmannian component with X. After passing
to K=F(SB(A)), the discriminant and Clifford invariant of q=psi_K vanish.
This extension does not assert that q or phi_K is hyperbolic. Standard Clifford
structure, rank valuations and the Severi–Brauer splitting theorem remain
explicit mathematical background; no finite experiment proves those theorems.

## The needed index bound, with two validation mechanisms

The submitted route is valid at the scope of its cited theorems. Karpenko's
published 2023 odd-spin paper, final preprint §§5–6, gives the fourth
Spin18 Grassmannian index8. DKM Proposition2.1 places the generic Chow image
inside the image for an arbitrary torsor. In top degree, I_generic Z is
contained in I_arbitrary Z, so I_arbitrary divides I_generic. This gives
ind OG4(q) dividing8 without identifying two different generic constructions.
The relevant source bodies freshly retrieved at root exactly match the
submitted historical source hashes; that authenticates versions, not proofs.

A materially different later input is Karpenko's author preprint
spind18-04.pdf, dated28Aug2023, listed as the 2024/2025 article
On isotropy fields of Spin(18)-torsors. Its Theorem4.1 and Corollary4.4 give a
noncomputer proof of the same needed bound. The paper explicitly states the
consequence for every18-dimensional form with trivial discriminant and
Clifford invariant. It produces a finite isotropy extension of degree not
divisible by16. Since the Grassmannian index is a power of2 (a multiquadratic
splitting extension supplies such a zero-cycle degree), its fourth, and even
fifth, index divides8. The precise published-version metadata and priority
still require the separate audit; root read the entire seven-page primary
text and visually checked its pages4–6.

I independently reproduced the finite polynomial step of that later proof
with root_mod2_check.py, using both a product of all16 subset factors and the
linearized recursion. Both exact F2 expansions have150 terms and agree in
normal, -O and -OO execution. The coefficient of x^8 contains
x7^4*x8^4 with coefficient1. There are35 coefficient monomials; the four pure
eighth powers vanish by the flag relations, leaving31 distinct already
reduced flag-basis monomials. All surviving exponents satisfy a_i<i for
i=5,6,7,8. The e8 component is therefore nonzero, using the cited free
flag/Schubert basis. The source's shorthand about power-of-two exponents is
read as zero or a power of two when a variable is absent, as its own displayed
witness requires. No mathematical inference depends on excluding exponent0.

This finite check reproduces a published step. It does not reprove the
Chow presentation, torsion exponent4, or critical-index criterion connecting
that step to geometry. Those are stated theorems, not experimental
assumptions. Separately, the two candidate-aware families independently constructed exact
intersection pairings detecting the original computation's obstruction. Their
sealed artifacts have been authenticated and independently executed by root.
A further fresh adversary obtained the same witness by root-monomial and
Vandermonde extraction, with an independently generated quotient-root check.
It also verified both lower-divisibility identities. This closes the original
finite computational gap within the stated standard geometric framework.

## Pointwise transfer and the exact forbidden term

Let Y be the16-dimensional projective quadric of psi. Each closed point of
OG4(q), with residue field L, supplies a projective3-space on Y_L. Its
structure-sheaf class lies in T13K(Y_L). Finite pushforward preserves
codimension and, after the injective split K-theory identification used in
the primary proof, acts on this distinguished class by [L:K]. The index is a
gcd, so integral combinations of transfers give 8*l3 in T13K(Y_K).
An extension of degree exactly8 is neither assumed nor needed.

The integral quadric relation is

    8*l3 = l0 + h^15 + 2*h^14 + 4*h^13.

It follows by iterating 2*l_j=l_(j-1)+h^(16-j) for j=1,2,3.
The hyperplane contributions all lie in T13, hence so does l0. There is no
division in an integral group and no cancellation of an unsupported factor8.

For the incidence variety Z of a line inside a maximal9-dimensional
isotropic subspace of psi, f:Z->X has projective8-space fibers. The other
projection g:Z->Y is smooth; in this case its relative dimension is28.
The dimensions36 of X,44 of Z, and16 of Y are consistent. Thus
f_*g^*(l0)=e8 lies in T^(13-8)=T5K(X_K). Using the odd rank8 tautological
bundle for this incidence would give the wrong shift; the even component
and its rank9 bundle are essential before identifying the component with X.

Theorem4.3 of a16i5 applies because C0(phi) was division of degree256 over F
and K is the function field of its ordinary Severi–Brauer variety. Its proof
uses the projective-bundle description of X times SB(A), the generation of
the associated graded by Chern classes, and the preceding maximal-index
Proposition4.2. Consequently T5=gamma5 over this K. Finally
8+1-floor(9/2)=5, exactly the prohibited term. This is a complete
counterexample to the original universal statement, rather than only a
formal contraposition of two universal conjectures.

## Root limits and remaining gates

No mathematical repair to the submitted inference has been identified.
The later analytic proof can strengthen its current exposition by removing
dependence on an unreplayed Maple calculation; original historical claims
about what was not run on11October must remain historical. The independent
finite pairings may provide additional supporting verification, with their
actual scopes. Standard published background theorems remain dependencies.
Root does not claim a proof-assistant formalization, external human review,
novelty, firstness, current worldwide openness, or a complete literature
audit at this point. Four family seals/replays are complete and no unresolved
mathematical finding remains. The extensive priority audit is still pending. Original eight output files, their joint bindings,
editorial output partitions and protected regions authenticate; old input
bodies are not contained in this snapshot and no old transformation replay
has been certified.

## Source normalization precision

ROOT_NORMALIZATION_PRECISION.json records a genuine prose typo in both AppendixA versions: the eight-factor product is labelled2^3*z-tilde there. Each of eight orbit factors is doubled, so the correct identity is a=2^8*z-tilde, consistently with sections4/5 and the explicit product code. Root freshly viewed journalPDF11/printed753 as well as preprintPDF9. The current arithmetic uses factor256; no official erratum or first-identification claim is inferred.
