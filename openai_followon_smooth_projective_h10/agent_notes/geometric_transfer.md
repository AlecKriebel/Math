# Independent reconstruction: geometric transfer and height obstruction

Checked: 2026-10-06 PDT / 2026-10-07 UTC. Agent: geometric_transfer.

**Status.** The geometric implication is established mathematics. The negative
solution of H10(Q) is an **unverified dependency** here. Consequently this note
establishes conditional implications, not the requested unconditional core
theorem. Estimated completion of this assigned geometric audit: 95%; completion
of the unconditional research target cannot be certified from this audit.
No external individuals were contacted; no Git mutations were performed.

## Sources and attribution

Poonen, *Existence of rational points on smooth projective varieties*, J. Eur.
Math. Soc. **11** (2009), 529–543, DOI
[10.4171/JEMS/159](https://doi.org/10.4171/JEMS/159).
[Author PDF](https://math.mit.edu/~poonen/papers/chatelet.pdf),
[publication page](https://ems.press/journals/jems/articles/1924), and
[published PDF](https://ems.press/content/serial-article-files/31670?nt=1)
were checked independently. The author PDF has 14 pages; the published PDF has
15. The relevant published locations are Theorems 1.1 and 1.3 (pp. 529–530),
Sections 8–9 (pp. 537–540), and Lemma 10.1 and Theorem 1.1 proof (pp. 540–541).
Source hashes and retrieval records are in ../sources/Poonen2009.metadata.json.
Downloaded third-party PDFs are dependency evidence, not proposed deposit files.

### Compact account of the cited transfer

Poonen's Theorem 1.3 effectively assigns to a projective number-field variety X
and open U a regular projective Y and morphism pi:Y→X satisfying
pi(Y(k))=U(k). Its construction is allowed to be disconnected. A Châtelet
surface family prevents rational points over excluded boundary points. Resolution
preserves the smooth fibers used to lift points of U. Section 9 repairs an
ineffective parameter choice: an effective cardinality bound, rather than a
list of rational points, supplies finitely many parameters, and their disjoint
union suffices. Lemma 10.1 excludes rational points on connected regular
components that are not geometrically integral. Theorem 1.1(i) then uses
computable connected components and geometric-integrality tests before invoking
the stipulated oracle. Remark 1.2(a) identifies regular and smooth over
characteristic zero. Remark 1.2(f) covers curves using threefold queries;
Section 12 asks about a general dimension-plus-two refinement. These are
Poonen's results and machinery, not a new geometric reduction.

## Exact presented decision problems

Let H10(Q) mean the following problem, with **arbitrary input variable count**:

    input: m≥0 and f∈Z[x_1,...,x_m], finitely encoded;
    output: whether ∃a∈Q^m such that f(a)=0.

Coefficient clearing gives the equivalent rational-coefficient formulation.
No fixed m or fixed degree is implicit. A constant-zero polynomial is a YES
instance and a nonzero constant is a NO instance, including m=0. This audit
does not prove undecidability of this problem.

Let SPGI(Q) be the following promised-input problem:

    input: N≥0 and homogeneous integer polynomials F_1,...,F_r
           in x_0,...,x_N;
    scheme: X=Proj(Q[x_0,...,x_N]/(F_1,...,F_r));
    promise: X is smooth over Q and geometrically integral;
    output: whether X(Q) is nonempty.

Here geometrically integral entails nonempty, reduced and irreducible after
base extension to an algebraic closure. The presentation includes its
projective embedding. Dimensions, degrees, equation counts, coefficient sizes
and ambient dimensions may all vary. r=0 is allowed. The equations need not
define a complete intersection. No behavior on inputs violating the promise
is required of a hypothetical decision procedure D.

One can instead use finite affine charts and effective gluing, as in the
paper. Effective projective constructions supply embeddings, and elimination
converts their outputs to the displayed homogeneous-equation convention.
Thus no oracle query needs an unspecified, noncomputable presentation conversion.

The input promise alone suffices. Recognition of the promise is also available:
projective emptiness and smoothness can be checked by effective algebra
(affine charts, ideal operations and the characteristic-zero Jacobian
criterion). For a nonempty smooth projective scheme, compute H^0(X,O_X),
using effective coherent sheaf cohomology. It is a finite étale Q-algebra;
X is geometrically integral exactly when its Q-dimension is 1. Indeed, scalar
extension commutes with H^0, and for a smooth proper scheme over an algebraically
closed field the dimension of H^0 is the number of connected components.
Every connected smooth component there is integral. This is a recognition
explanation, not an extra requirement imposed on D.

For a primary computational reference, Gregory G. Smith,
[*Computing Global Extension Modules for Coherent Sheaves on a Projective
Scheme*, Theorem 1](https://arxiv.org/pdf/math/9807170), gives an effective
syzygy-based truncation bound. Applied with homogeneous coordinate ring R,
both modules equal to R, and cohomological degree 0, it gives

    H^0(X,O_X) ≅ Hom_R(R_{≥r},R)_0

for an effectively computed r. The right side is computable by finite graded
module linear algebra. For the geometric criterion see
[Stacks Project, Lemma 33.10.7](https://stacks.math.columbia.edu/tag/038L):
proper geometrically normal schemes have geometric integrality exactly when
H^0(O)=k. Smooth schemes meet the geometric-normality hypothesis. These sources
were checked on 2026-10-06 PDT; no cohomology program was executed.

## Independent promise check lemma over Q

**Lemma.** A connected smooth Q-variety with a Q-point is geometrically integral.

**Proof.** Smoothness implies regularity and geometric reducedness. On a
Noetherian regular scheme distinct irreducible components do not intersect:
a local ring at an intersection would have more than one minimal prime and
could not be a regular local domain. Thus the components are open and closed,
and connectedness makes the original variety integral. Its geometric
irreducible components are disjoint, and the absolute Galois group acts
transitively on them. A Q-point yields a Galois-fixed geometric point lying
on exactly one component. Every conjugate of that component contains this
same point, so that component is fixed. Transitivity therefore forces a single
geometric component. Together with geometric reducedness this proves geometric
integrality. □

For a connected smooth **projective** C there is also a short algebraic check.
L=H^0(C,O_C) is a finite field extension of Q. A Q-point induces a Q-algebra
homomorphism L→Q, hence L=Q. Over an algebraic closure, the global-functions
algebra has dimension [L:Q] and records the disjoint smooth components. Thus
C is geometrically integral exactly when [L:Q]=1. This provides a concrete
way to implement the geometric-integrality filter on oracle candidates.

Regular=smooth is valid here because Q is perfect and has characteristic zero.
No positive-characteristic or nonperfect-field generalization is being used.

## Exact contradiction algorithm

Suppose D terminates correctly on every SPGI(Q) presentation. Define A_D on an
arbitrary H10(Q) input f as follows.

1. Form U=Spec(Q[x_1,...,x_m]/(f)); replace by its reduction if desired,
   because rational points are unchanged. Deal directly with the empty case.
2. Embed U as a closed affine scheme and compute its scheme-theoretic projective
   closure X. Record U as an **open subvariety of X**. For arbitrary finite-type
   input, first take its finite affine open cover and apply the following steps
   to each chart.
3. Apply the effective Theorem 1.3 construction to (X,U), yielding (Y,pi).
4. Compute the finitely many connected components C_1,...,C_s of Y and
   projective presentations for each. Each component is open and closed, hence
   projective; each is smooth because Y is regular over Q.
5. Test geometric integrality of each C_i. Discard those failing it. By the
   preceding lemma, every discarded component has empty rational-point set.
6. Query D only on the remaining components. Return YES exactly when at least
   one answer is YES; if there are no remaining components, return NO.

Concretely, the finite étale algebra H^0(Y,O_Y) splits effectively as a product
of number fields. Its idempotents specify the connected components; local
representatives of these global sections give their closed equations. The
dimension of the corresponding field over Q implements step 5. A field of
degree greater than 1 has no Q-algebra map to Q, so its component has no Q-point;
degree 1 implies geometric integrality by the cited global-functions criterion.

Every non-oracle step is effective. There are finitely many queries and each
satisfies D's valid-input promise, so A_D terminates. Its correctness is the
following chain, valid also when either side is empty:

    ∃a∈Q^m:f(a)=0
    ⇔ U(Q)≠∅
    ⇔ pi(Y(Q))≠∅
    ⇔ Y(Q)≠∅
    ⇔ ∃i:C_i(Q)≠∅
    ⇔ ∃i satisfying the SPGI promise:D(C_i)=YES.

Consequently **if H10(Q) is undecidable, SPGI(Q) has no decision algorithm**.
All of the arithmetic force of this conclusion is in the displayed antecedent.
Neither a projective closure alone nor an ordinary birational resolution alone
establishes the second equivalence.

For each ordinary variety input the same preprocessing yields a finite list
of promised queries before any answers are received. The proof therefore gives
a finite **nonadaptive disjunctive oracle reduction**, in particular a Turing
reduction. It does not establish a single-output many-one reduction into SPGI(Q).
Theorem 1.3 itself yields a single smooth projective Y with point-existence
equivalence if geometric integrality and connectedness are dropped. No claim
that a stronger reduction is impossible is intended.

## Effectivity audit and exact potential traps

The finite parameter union is essential. Cardinality of a finite set and
effective enumeration of that set are distinct requirements. For the
construction, an upper bound on the number of obstructing square classes lets
one choose more distinct permissible square classes than that bound. At least
one parameter is good, while every parameter excludes boundary rational
points. Hence a disjoint union has the required image without identifying the
good parameter or solving the rational-point problem on its auxiliary curves.
This combinatorial inference is independent of the oracle D. The underlying
effective cardinality theorem is inherited as part of the cited Theorem 1.3,
not reproved or numerically implemented in this audit.

The smoothness needed when resolving is pointwise over rational base points:
if t∈U(Q), the relevant fiber lies in the smooth locus, so the resolution is
an isomorphism there and preserves a rational lift. If t∈X(Q)\U(Q), a rational
lift would map to the boundary-excluding auxiliary variety, which is
impossible. Merely saying that resolution preserves a birational function
field omits both arguments.

Examples checking the promise and point-equivalence boundaries:

* Spec(Q(i)) is connected, regular and projective over Q, but not geometrically
  integral and has no Q-point. It must be filtered rather than sent to D.
* Spec(Q[x,y]/(x^2+1)) has no Q-point, but its projective closure
  V(X^2+Z^2)⊂P^2 has the rational boundary point [0:1:0]. This disproves a
  closure-only replacement.
* The affine scheme V(x^2+y^2) has the rational singular point (0,0), while
  its normalization is A^1 over Q(i), with no Q-point. This disproves a
  resolution-only point-equivalence claim. A morphism from a resolution cannot
  create a Q-point when its target has none; the actual risk is losing singular
  points or retaining newly added boundary points after compactification.
* A zero-dimensional smooth projective geometrically integral Q-variety is
  Spec(Q), so it has a Q-point. The unrestricted-dimensional statement does
  not imply any zero-dimensional or other fixed-dimensional undecidability.

No dimension-preservation claim is used. The auxiliary W has surface fibers,
and the product construction grows with the affine ambient dimension. This
audit deliberately does not claim a universal d+2 output dimension, a fixed
dimension, or a quantitative bound for the reduction. The curve-to-threefold
refinement does not prove undecidability for curves or threefolds from the
unrestricted H10(Q) antecedent. No curve, surface, Fano, general-type,
hypersurface, or finite-rational-point assertion follows here.

## Explicit size encoding and the conditional height theorem

The following is an original elementary computability deduction from the
conditional decision obstruction; it is not a new geometric reduction.

For a≥0, put b(a)=the ordinary binary representation of a, with b(0)=0, and
ell(a)=|b(a)|. Define the self-delimiting code

    c(a)=1^{ell(a)} 0 b(a).

For a signed coefficient z≠0 encode a sign bit (0 for positive, 1 for negative)
followed by c(|z|). An encoded presentation e consists, in this order, of:

    c(N), c(r), and for each i=1,...,r:
      c(t_i), and for each of its t_i monomials:
        sign(a_ij), c(|a_ij|), c(alpha_ij,0),...,c(alpha_ij,N).

Require nonzero coefficients, strictly increasing lexicographic exponent
vectors in each polynomial, and a common total degree within each polynomial.
The zero polynomial has t_i=0. Zero polynomials and redundant equations do not
affect the scheme and need not be suppressed. Parsing is unique because every
integer code specifies the length of its binary tail; the monomial and equation
counts specify exactly how many tails to read. Reject trailing bits and malformed
codes. The size parameter is precisely s(e)=the number of bits in this code.
This is computable and explicitly records N, r, coefficients and all exponents.
It does not measure an intrinsic isomorphism invariant of X.

For P∈P^N(Q), take the unique primitive integer representative
(z_0,...,z_N) with its first nonzero coordinate positive, and define

    H(P)=max_j |z_j|.

H(P) is a positive integer and is invariant under the projective scaling of
the input point. The embedding, however, is the specified one in e.

**Conditional height theorem.** If H10(Q) is undecidable, there is no total
computable B:N→N such that every valid presentation e with X_e(Q)≠∅ has some
P∈X_e(Q) with H(P)≤B(s(e)).

**Proof.** On a valid e compute M=B(s(e)). Enumerate all integer vectors
z∈[-M,M]^{N+1}; retain nonzero primitive vectors whose first nonzero entry is
positive. Evaluate every F_i(z) using exact integer arithmetic. Return YES
if one vector satisfies all equations and NO otherwise. This is a finite
computation. A witness gives a rational point; conversely the hypothesized
bound places a representative of some rational point in the enumeration.
It would therefore decide SPGI(Q), contradicting the conditional decision
theorem. For M=0 the enumeration retains no vectors, consistently with H≥1.
There is no complexity assertion. □

The same proof rules out a presentation-dependent computable bound B(e) that
terminates on every valid input and bounds the height of one point when points
exist. Its behavior off the promise is immaterial. The theorem does **not**
ask for bounds on all rational points, finite rational-point sets, degrees of
extensions, or heights under an unspecified embedding.

Conversely, a decision procedure on valid inputs would give a
presentation-dependent bound: return 0 after a NO answer, and after a YES answer
enumerate heights until a point is found and return that height. This terminates
on valid inputs. A size-only bound follows too when using the decidable input
recognition described above: inspect the finitely many strings of length at
most n, decide existence on each valid one, find one point for each YES instance,
and take the maximum of their heights (or 0 if there are none). Thus in this
convention the height obstruction and decision obstruction are equivalent
computability statements; no independent arithmetic progress is hidden in the
height corollary.

## Optional certificate consequence, precisely scoped

If used in the paper, define a scheme of no-point certificates as a decidable
predicate V(e,c) on finite binary strings, satisfying, for **valid** e:

    soundness: V(e,c)=true ⇒ X_e(Q)=∅;
    completeness: X_e(Q)=∅ ⇒ ∃c:V(e,c)=true.

Enumerate certificates and rational point candidates in alternating finite
stages. A verified point returns YES; an accepted certificate returns NO.
Soundness prevents incorrect answers and completeness ensures termination on
empty inputs; nonempty inputs terminate by point enumeration. Hence, under
the H10(Q) antecedent, no such sound and complete uniformly decidable scheme
exists. This says nothing about any particular empty variety having a proof
or a certificate, and it does not rule out sound incomplete systems. No
certificate consequence is needed to complete the requested geometric and
height argument.

## Remaining verification limits

* The exact published Theorem 1.3, its parameter-union repair, and its oracle
  use were checked in both supplied primary versions.
* The elementary connected-component promise argument, contradiction algorithm,
  height enumeration and optional certificate dovetail were reconstructed here.
* No implementation of resolution, effective cohomology or the Parshin/Faltings
  cardinality algorithm was executed. These are established dependencies of the
  cited effective geometric theorem, not computational experiments.
* No unconditional H10(Q) theorem was accepted or verified by this audit.
  An upstream gap leaves the unconditional core and production publication
  blocked; the conditional implications survive.
* This audit does not establish novelty, priority, or publication readiness.
  The root researcher must incorporate the separate arithmetic and priority
  audits before promoting any claim.
