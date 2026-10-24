# Independent audit addendum: injectivity for an arbitrary fixed permutation top

Checkpoint: 2026-10-24 18:07 UTC. Assigned addendum audit completion estimate:
100%. This is an audit of a mechanism exclusion, not a solution of 21.135.
The earlier audit and author files have not been edited.

Fresh exact-file review: I read the complete coordinator file
`problems/21_135/root_wreath_injectivity.md`, SHA-256
`3ecf14984d7e31253c97a2f848aed3cc89850d2b895bab7d4fe165d3a6515ccb`.
Its canonical extension, completeness argument, support bound, first-degree
comparison, boundary qualifications, and final radical paragraph are all
covered by this addendum. The proof below was independently reconstructed
from the assigned claim before reading that exact file.

## Claim audited

Let P be a fixed finite group acting on a fixed nonempty finite set Omega.
The action need not be faithful or transitive. For finite groups X and Y,
equality of the multisets of irreducible complex character degrees of

    X^Omega semidirect P  and  Y^Omega semidirect P

implies equality of the degree multisets of X and Y. The action here is
ordinary permutation of the coordinates.

**Verdict:** the strengthened claim is correct. I found no substantive
gap in the proposed support argument. A full reconstruction follows,
including the cases omitted by an informal first-differing-degree argument.

## Representation-theoretic input

For a labeling f:Omega -> Irr(X), let P_f be its stabilizer, put
t_f = [P:P_f], and put B_f = product_(i in Omega) f(i)(1).
The irreducibles above this labeling orbit have degrees

    t_f B_f eta(1),                 eta in Irr(P_f).        (A)

The genuine tensor-permutation extension proving (A) is constructed in
the earlier independent audit. It remains valid for a nonfaithful
action: an element in the action kernel acts as the identity tensor
permutation, and all its possible additional actions are supplied by
ordinary representations eta of P_f. There is no need to divide P by
its action kernel, and no projective correction is missing in (A).

## Linear characters determine the base linear multiplicity

Let r be the number of P-orbits on Omega, and let l(X) be the number of
linear characters of X. Since Omega is nonempty, r >= 1.

An output degree in (A) is 1 precisely when t_f = 1, B_f = 1, and
eta(1) = 1. Thus all labels must be linear, f must be P-invariant,
and eta must be a linear character of P. A P-invariant labeling is
independently constant on each of the r coordinate orbits, so

    l(X^Omega semidirect P) = l(X)^r l(P).                  (B)

Consequently equality of output spectra implies l(X) = l(Y): l(P)
is a fixed positive integer and the map n -> n^r is strictly
increasing on positive integers. This deals with a first difference
at degree 1, which cannot be ignored in the subsequent argument.

## Support bound

Let m0 be the least size of a coordinate orbit of P on Omega. It is a
positive integer. Suppose f contains a label of degree e >= 2 on a
coordinate orbit O. Define

    S = {i in O : f(i)(1) >= e},     a = |S| >= 1,
    t = [P:P_f].

Every element of P_f fixes the entire labeling and hence preserves S.
The t left cosets of P_f determine t translated labelings and their
supports gS. Some of these supports may repeat, which causes no
problem. Because S is nonempty and P acts transitively on O, their
union is all of O. Counting with repetitions gives

    t a >= |O| >= m0.                                      (C)

The product B_f includes at least a factors each at least e, so every
degree in (A) satisfies

    t B_f eta(1) >= t e^a >= t a e >= m0 e.                 (D)

The middle inequality uses e^(a-1) >= 2^(a-1) >= a for
integers e >= 2 and a >= 1. It includes a = 1 and the equality
case e = a = 2. No assumption about the other coordinate orbits,
faithfulness, or transitivity of the whole action enters this bound.

In particular, a label of any degree e > d >= 2 cannot contribute
to any output degree at most m0*d.

## First different degree gives a strict coefficient difference

Suppose the base degree multisets differ. After (B), there is a least
integer d >= 2 where their multiplicities differ. Interchange X and
Y if necessary so that X has fewer degree-d labels than Y. Choose
a degree-preserving injection

    Irr(X)_(degree <= d) -> Irr(Y)_(degree <= d).

For degrees below d it is a bijection, and at degree d it misses at
least one label. The principal character of X can be mapped to the
principal character of Y, since their linear multiplicities agree.

Apply this injection in each coordinate. The resulting map on
labelings is P-equivariant, preserves the exact stabilizer P_f, and
preserves B_f. It therefore embeds the old labeling orbits and all
their degree contributions (A), with multiplicities unchanged.
These are full P-orbits: relabeling cannot take a tuple outside the
image back inside it.

By (D), every output contribution at degree at most m0*d, on either
side, uses only labels of degree at most d. Hence the preceding
injection compares all contributions at the degree m0*d, rather than
only a selected subset that might conceal a compensating contribution
from an unexamined larger base degree.

Now choose a missed degree-d label of Y. Place it at a single point
of a coordinate orbit of size m0, and place the principal character
of Y at every other coordinate. Since d >= 2, that exceptional label
differs from every other label in the tuple. Its stabilizer is exactly
the point stabilizer, so its orbit has size m0. Its product B_f is d.
Taking the trivial character eta of P_f in (A) gives an output degree
m0*d. This labeling orbit cannot be in the embedded old image because
it uses the missed label. It supplies at least one extra occurrence
of m0*d, while no old occurrence is lost. Thus the multiplicity at
m0*d is strictly greater for the Y wreath product, contrary to
equality of the output multisets.

This proves injectivity for every fixed finite permutation action on
a nonempty finite coordinate set.

## Boundary and scope checks

- **Empty Omega:** r = 0 and there is no m0. Both wreath products
  equal P, so the injectivity conclusion fails in general. The
  nonempty qualification is essential.
- **Trivial base:** l(1) = 1. If the other base has additional linear
  characters, (B) detects them. If it has the same single linear
  character but is nontrivial, its least nonlinear degree is detected
  by the first-difference proof. Thus no exception is needed.
- **Trivial P or a trivial action:** formula (A) and the support
  argument still work. In a trivial action every coordinate orbit has
  size 1, so m0 = 1. The result agrees with direct-product
  cancellation and injectivity of the fixed positive power of a
  finite Dirichlet polynomial.
- **Nonfaithful P:** the kernel is retained in P_f and in eta; no
  argument assumes it is trivial.
- **Nontransitive P:** taking the smallest coordinate orbit is valid
  in (C) for every orbit and supplies the required new tuple.
- **Coincident output degrees:** the proof embeds complete orbits
  with their multiplicities and adds one new orbit. It never assigns
  a unique source to an output degree, so coincidences do not create
  cancellation.
- **Generality:** arbitrary automorphisms of the base, nonsplit
  extensions, and degree-preserving but nonpermutation actions on
  character labels are outside the claim. No such generalization is
  implied by this audit.

The result broadens the wreath-mechanism exclusion but does not resolve
the unrestricted comparison of finite groups in Kourovka 21.135.
Originality has not been established or claimed.

## Exact-file radical paragraph

The coordinator file also asserts radical preservation when the action is
faithful and the base X is nontrivial and radical-free. Its direct proof
is valid and is simpler than using the socle. Put B = X^Omega and let A
be a solvable normal subgroup of W. The intersection A intersect B is
solvable normal in B and hence lies in

    R(B) = R(X)^Omega = 1.

Both A and B are normal in W, so [A,B] <= A intersect B = 1.
Since R(X) = 1 implies Z(X) = 1, the only base element centralizing B
is 1. A top permutation centralizing every base element must fix every
coordinate, since X != 1 and an element supported at one coordinate
would otherwise have its support moved. Faithfulness then forces the
top element to be 1 as well. Thus C_W(B) = 1 and A = 1.

In the converse direction a nontrivial R(X) gives the nontrivial solvable
normal subgroup R(X)^Omega because Omega is nonempty. Therefore the
radical assertion is correct under exactly its stated extra hypotheses;
these extra hypotheses are not needed for the degree-injectivity result.
The file's optional reference to the socle is not required for this proof
and does not introduce an additional inference or assumption.
