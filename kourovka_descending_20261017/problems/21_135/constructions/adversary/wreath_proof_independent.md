# Independent theoretical adversarial audit: wreath mechanisms

Checkpoint: 2026-10-24 18:04 UTC. Assigned audit completion estimate: 100%.
This percentage concerns the present audit, not discovery of a solution to
Kourovka 21.135. The target problem remains unresolved by these arguments.

Reviewed source:
`constructions/approach_constructions.md`, Sections 2–3, SHA-256
`e3512f4f76144e3b8641720cde509280f5e44fce331ca0d936b1360d02fda6bd`.

I independently reconstructed the representation-theoretic arguments and tried
to invalidate the prime, faithfulness, nontransitivity, trivial-base, and
projective-extension steps. I found no substantive error in the stated
mechanism exclusions. Strict class-number monotonicity uses the nonempty
coordinate-set assumption from Section 2; it should remain explicit if
Section 3 is quoted separately. No external priority claim was audited here.

## 1. Tensor permutations give genuine extensions

Write the action of a finite permutation group P on a finite set Omega as
`(p.b)_i = b_(p^{-1}i)`. Fix one concrete complex irreducible representation
`rho_chi : X -> GL(V_chi)` for every character chi of X. A labeling
`f : Omega -> Irr(X)` defines the irreducible representation

    rho_f(b) = tensor_i rho_(f(i))(b_i)

of the base B = X^Omega. This representation is irreducible by the usual
classification of irreducible representations of a finite direct product.
Its inertia subgroup in B semidirect P is exactly B semidirect P_f, where
P_f fixes f as a labeling.

For p in P_f define T_p on a pure tensor by putting v_(p^{-1}i) in slot i.
This is a map from the tensor space to itself because
`V_(f(p^{-1}i)) = V_(f(i))` as the same chosen representation space, not
merely as an unspecified isomorphic space. Direct substitution gives

    T_p T_q = T_(pq),
    T_p rho_f(b) T_p^{-1} = rho_f(p.b).

Thus `(b,p) -> rho_f(b) T_p` is an actual representation of B semidirect
P_f extending rho_f. There is no projective cocycle: no separately chosen
intertwiner enters the construction, and ordinary vector-space permutation
has no sign. The extension remains irreducible since its restriction to B
is irreducible.

For completeness, every irreducible representation of the inertia subgroup
whose restriction to B contains rho_f has form

    (extension of rho_f) tensor (inflation of tau),
    tau in Irr(P_f).

One can see this without assuming away a cocycle. Such a representation has
B-isotypic space `V_f tensor M`. Comparing its action with the fixed genuine
extension leaves an action on M commuting with B; Schur's lemma identifies
this commuting algebra with End(M). The remaining action is therefore an
ordinary representation of P_f, and irreducibility is equivalent to that
of M. Clifford induction from the inertia subgroup then gives one
irreducible of the whole wreath product for each tau. Different labeling
orbits have disjoint base constituents, so there is no duplication.

This verifies both the extension premise and exhaustiveness needed in
Sections 2 and 3, including when P is nonabelian.

## 2. Prime cyclic formula and injectivity

If P = C_p acts as a p-cycle, a tuple fixed by a nonidentity permutation is
constant: a nonidentity power of a p-cycle is still a p-cycle. Thus every
nonconstant tuple has a free orbit of size p. Constant tuples have the p
one-dimensional characters of C_p above their tensor extension, giving
p irreducibles of degree chi(1)^p. Each free orbit gives one induced
irreducible of degree p times the product of its tuple degrees.

Writing D_X(s) = sum_chi chi(1)^(-s), the contribution of constant tuples
to the uninduced tuple product is D_X(ps). Subtract it from D_X(s)^p,
divide by p for orbit size, and multiply by p^(-s) for induced degree.
This gives exactly

    D_(X wr C_p)(s)
      = p D_X(ps) + (p^(-s)/p) (D_X(s)^p - D_X(ps)).

Let F = D_X - D_Y be nonzero, and choose the least positive integer d
whose degree multiplicities differ, with difference c != 0. Since these
are finite Dirichlet polynomials,

    d^s F(s) -> c,
    d^(ps) F(ps) -> c       as s -> +infinity.

Both F(s) and F(ps) consequently have the same nonzero sign for all
sufficiently large positive s. Equality of the two wreath spectra would
give, with z = p^(-s),

    0 = z Q(s) F(s) + (p^2-z) F(ps),
    Q(s) = sum_(i=0)^(p-1) D_X(s)^(p-1-i) D_Y(s)^i.

Both coefficients are positive for s > 0, because all D values are
positive and 0 < z < 1. This contradicts the common sign. No comparison
of individual degree contributions, and therefore no uniqueness of a
degree's origin, is required.

Exact boundary checks:

- X = 1 gives p irreducibles of degree 1, as required for C_p.
- For p = 2 and X = C_2, the spectrum is four 1s and one 2; its square
  sum is 8, as for C_2 wr C_2.
- For p = 2 and X = S_3, whose degrees are 1,1,2, the spectrum is
  four 1s, one 2, and four 4s. The two extensions from the degree-2
  constant tuple and the two mixed 1,2 orbits both contribute at degree
  4. The total square sum is 4 + 4 + 64 = 72 = 2*6^2.

In general the formula at s = -2 yields p|X|^p, independently checking
the required square sum. The injectivity proof uses positive s and does
not require its coefficient signs at negative s.

Verdict: the degree formula and its injectivity hold for every finite
base, including the trivial group, and for p = 2.

## 3. Radical preservation, with nontransitive actions

Assume X != 1 and Omega is finite and nonempty. If R(X) != 1 then
R(X)^Omega is a nontrivial solvable normal subgroup of the wreath
product, independently of transitivity.

Conversely let R(X) = 1. Every minimal normal subgroup of the finite
group X is a direct product of isomorphic simple groups. It cannot be
abelian because it would then lie in R(X). Hence S = Soc(X) is a
nontrivial direct product of nonabelian simple groups, so Z(S) = 1.

The centralizer C_X(S) is normal in X. If it were nontrivial, it would
contain a minimal normal subgroup M of X. Then M <= S and
M <= C_X(S), whence M <= Z(S) = 1, a contradiction. Therefore
C_X(S) = 1.

Put T = S^Omega. It is normal in W = X^Omega semidirect P. A solvable
normal subgroup A of W has A intersect T = 1: this intersection is a
solvable normal subgroup of T, whose projection on each nonabelian
simple direct factor must be trivial. Since A and T are normal,
[A,T] <= A intersect T = 1, so A centralizes T.

If (b,p) centralizes T, conjugating an element supported on coordinate i
shows that p(i) = i: otherwise its nontrivial support moves to a
different coordinate. This holds for every i and uses only S != 1,
not transitivity. Faithfulness of the permutation action now gives
p = 1. Each b_i centralizes S, and hence b_i = 1. Thus C_W(T) = 1
and A = 1.

Verdict: radical preservation is correct for arbitrary faithful actions,
including those having several orbits or fixed coordinates. The stated
qualifications matter. For X = 1 the wreath product is P; for empty
Omega it cannot detect R(X); for a nonfaithful action the top kernel
can introduce a solvable radical.

## 4. Class-number formula and strict monotonicity

The extension and Clifford argument in Section 1 above gives precisely

    k(X wr_Omega P) = sum_(f modulo P) k(P_f).

The orbit and stabilizer on the right depend only on the finite color
set Irr(X), not on its degrees, group structure, or any choices of
representations. This proves the asserted dependence only on k(X)
and on the fixed permutation action.

If m < n, choose an injection from a color set of size m into one of
size n. The resulting inclusion of labeling sets is P-equivariant.
Its image is a union of complete P-orbits, and every old labeling has
exactly its former stabilizer. Thus all old summands persist. When
Omega != empty, a constant labeling with a new color is a new orbit
with stabilizer P and contributes k(P) >= 1. Strict increase follows.
For Omega empty there is only the empty labeling and no strict
increase; the inherited nonempty assumption must be retained.

If X is nonabelian and A is abelian with |A| = |X|, then
k(A) = |X| > k(X), so the two wreath products have different numbers
of irreducibles. Their orders are equal because their base orders and
top are equal. Consequently their degree multisets differ.

The indicated partial-coordinate version is also valid with its stated
qualification: the coordinates to be changed must form a nonempty
P-invariant collection and the action must be ordinary permutation of
the respective character labels. Use the same label injection on each
coordinate in that collection. Old orbits persist and a labeling
using a new color on the changed collection yields a new orbit. This
does not address arbitrary automorphisms of the base, nonpermutation
actions on character labels, or general nonsplit extensions.

## Outcome

No substantive objections remain to Sections 2–3 within their specified
scope. In particular, the tensor-permutation extension does not conceal
a projective obstruction. These results exclude common prime cyclic
wreath enlargement and equal-order abelian replacement mechanisms;
they neither construct a counterexample nor prove Kourovka 21.135.
No novelty or publication conclusion follows from this audit.
