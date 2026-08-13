# Structural analysis of triangle-bearing theta factors

Status: **PROVED where marked; otherwise UNRESOLVED**

## 1. Locked inputs

This sidecar reads, but does not modify or import code from, the following
project inputs.

| Input | SHA-256 |
|---|---|
| `docs/DEFINITIONS_LOCK.md` | `3108a20e924a37b069cc4aeb53b051b03463176eafce9d590dfec378e2ad16a2` |
| `docs/GENERATOR_AND_SUPPORT_THEOREM.md` | `a6b195d158972ba842c7995ddf97898272db533d8505f5fbb4299f1a296f79e9` |
| `docs/LOCAL_ATLAS_THEOREM.md` | `34b8eccfa16100f6b25ccbca68320387d339c2264d78ba0eea61ceaa115cf217` |
| `primary/certificates/core_universe.json` | `f7ebe0b0ebc93f58cfa5bc2086f55a518b0ce8774da57667fe4c1f169ff39e10` |
| Englander et al. v4 source XML | `1323dec9322099afb9f49e11554c92d1fe78e4b29c5ee03ba8942690ae2e8c38` |

The graph convention is the locked simple, binary, LSA-rootable
semi-directed convention `sd_0`; the topology class has no omnians.  Edge
Fourier multipliers and inheritance probabilities lie in `(0,1)`.

## 2. Exact location of triangles in the four theta cores

Let the theta poles be `U,V`, and let `m_j >= 0` be the number of ordinary
port-bearing subdivisions inserted on locked core segment `j`.  A theta cycle
is triangular exactly when two of its three pole-to-pole path lengths sum to
three.  Since every path length is positive, this means that one path has
length one and another has length two.

The core JSON gives the following path lengths and strong-repair condition.

| Core | Path lengths `(L0,L1,L2)` | Strong occupancy condition |
|---|---|---|
| `theta-0` | `(2+m0+m1, 2+m2+m3, 1+m4)` | `{2,3}` or `{3,4}` occupied |
| `theta-1` | `(3+m0+m1+m2, 1+m3, 1+m4)` | `m2>0` and `m3>0 or m4>0` |
| `theta-2` | `(2+m0+m1, 2+m2+m3, 2+m4+m5)` | one recorded two-segment repair occupied |
| `theta-3` | `(3+m0+m1+m2, 2+m3+m4, 1+m5)` | `m2>0 or m4>0` |

The repair condition means that the occupied segment set contains at least
one recorded minimum repair.  It follows immediately that:

1. **PROVED — `theta-0`.**  A triangle exists exactly when
   `m0=m1=m4=0`.  Strongness then forces `m2,m3>0`.  The triangle is the
   direct path together with the two-edge path whose interior event is `S`.
2. **PROVED — `theta-1`.**  A triangle exists exactly when
   `{m3,m4}={0,1}`.  Strongness also forces `m2>0`.  Its interior triangle
   vertex is the unique ordinary port on the subdivided one-edge path.
3. **PROVED — `theta-2`.**  No triangle exists because all three path
   lengths are at least two.
4. **PROVED — `theta-3`.**  A triangle exists exactly when
   `m3=m4=m5=0`.  Strongness then forces `m2>0`.  Its interior triangle
   vertex is the path-sink reticulation `X1`.

For a minimum repair this yields exactly the following triangle-bearing
records:

```text
theta-0 repair [2,3] : path lengths (2,4,1), triangle vertex S
theta-1 repair [2,3] : path lengths (4,2,1), triangle vertex ordinary port
theta-1 repair [2,4] : path lengths (4,1,2), triangle vertex ordinary port
theta-3 repair [2]   : path lengths (4,2,1), triangle vertex X1
```

The two `theta-1` rows are exchanged by the locked path symmetry.  Added
ports preserve a triangle only when they lie on the complementary path (or
away from the two short paths as allowed by the formulas).  Therefore the
triangle side contains exactly one real boundary port in every
triangle-bearing strong expansion:

- the incoming boundary at `S` for `theta-0`;
- the ordinary repair boundary for `theta-1`; or
- the sink child boundary of `X1` for `theta-3`.

This is stronger than the assertion that a bounded support happens to have
one such port; it holds for every arbitrary port word that retains the
triangle.

## 3. The graph-theoretic obstruction

Let `Q` be the union of the direct theta path and the length-two theta path
forming the triangle, and let `R` be the third pole-to-pole path.  Then

```text
Q intersection R = {U,V}.
```

**PROVED.**  No edge of the blob separates `Q` from `R`, and no single vertex
does so.  Any separation which puts the triangle edges on one side and the
interior of the third path on the other has boundary `{U,V}`.  This is simply
the defining two-pole structure of a biconnected theta graph.

Consequences:

1. the audited one-incidence-per-side bridge peeling theorem recovers only the
   complete theta-blob port tensor;
2. it does not recover a triangle tensor and a complementary-path tensor;
3. the complementary object, with hidden states at `U,V`, is not itself a
   standard leaf-labelled triangle-free phylogenetic network to which the
   triangle-free theorem can be applied.

## 4. Exact two-terminal gauge

Let `G=Z_2 x Z_2`.  Fix any rooted realization of one of the three
triangle-bearing families.  Put the reticulation choice whose two incoming
edges lie in the triangle into the triangle factor, and the other choice into
the complementary factor.  Reticulation choices are independent.  Conditional
on the pole states `(u,v)`, all edge and switching factors partition between
the two subgraphs.  Hence the local port tensor has the form

```text
P(y,z) = sum_(u,v in G) A(y,u,v) B(z,u,v),                 (1)
```

where `y` is the unique triangle-side port state and `z` is the tuple of all
remaining port states.  Root or incoming-arm factors may be absorbed into the
side containing them; this does not change (1).

For every nowhere-zero function `c:G x G -> R`, define

```text
A_c(y,u,v) = c(u,v) A(y,u,v),
B_c(z,u,v) = c(u,v)^(-1) B(z,u,v).
```

Substitution in (1) proves `P_c=P` term by term.  The gauge remains inside the
ambient group-equivariant tensor category when `c(u,v)=kappa(u xor v)`.

Take

```text
kappa(0)=2,  kappa(g)=1 for g nonzero.                    (2)
```

This is not a separate pole-incidence scaling.  Indeed, if
`c(u,v)=f(u)g(v)`, then the matrix `C=(c(u,v))` has rank one.  On rows and
columns indexed by `0` and any nonzero `a`, (2) gives

```text
[[2,1],
 [1,2]],
```

whose determinant is `3`.  Thus the internal-pair gauge is genuinely larger
than any product of one-pole factors, and a fortiori larger than the scalar
port-arm incidence gauge in the bridge theorem.

There is also an immediate rank obstruction to unconstrained extraction.
Flatten `A` with the four values of `y` as rows and the sixteen pairs `(u,v)`
as columns.  Its rank is at most four, so it has no left inverse on the hidden
pair space.  The minimum strong topology supplies only one triangle-side
observed variable; it does not provide the three conditionally independent
views required by standard latent-state tensor uniqueness.

### Scope warning

**UNRESOLVED, and essential:** an arbitrary `c` need not map the JC triangle
factor and complementary-path factor back into their respective JC model
families.  Therefore this gauge is not an observational-equivalence move and
is not a counterexample.  It proves that uniqueness cannot follow from
contraction, positivity, group equivariance, or bridge projectivization alone.
Model-specific rigidity remains to be proved.

## 5. Why the two obvious reductions do not close the gap

### 5.1 Marginal deletion

Deleting the unique triangle-side port removes the only observation in that
factor.  Under the declared induced-subnetwork cleanup, the triangle may then
collapse through degree-two, parallel-edge, or 2-blob suppression.  This map
forgets precisely the triangle attachment that must be identified.  A
containment of full models descends to a marginal, but a marginal containment
does not lift to an extension.  Thus deletion cannot create a reversible
triangle-free reduction.

### 5.2 Virtual subdivision

Subdividing the direct triangle edge by a new labelled port makes the blob
triangle-free.  But that new leaf tensor is not determined by the original
distribution.  Source-relative containment supplies no continuous target
parameter choice and no common extension by the virtual leaf.  Applying the
triangle-free theorem to such an extension assumes an unproved lifting
statement.

### 5.3 Prior theorems

Englander et al. Theorem 3.2 applies to complete leaf-labelled networks which
are triangle-free.  Their Theorem 3.1 applies to complete level-1 networks
modulo triangle orientation.  Neither theorem asserts identifiability of a
factor with two unobserved state boundaries, nor uniqueness of the
factorization (1).  Applying the two theorems separately to `A` and `B` would
therefore be circular.

## 6. Exact missing lemma

The proof-first route would become valid after proving the following
model-specific statement.

> **Anchored two-terminal JC rigidity lemma (UNRESOLVED).**  Let `H` be a
> triangle-bearing standard-strong level-2 theta factor in one of the three
> families in Section 2, with its complete labelled boundary set and a fixed
> incoming boundary.  Let `H'` be any standard-strong cycle or theta factor
> on the same labelled boundaries.  If a source-full-dimensional regular germ
> of the projective JC tensor model of `H` is contained in that of `H'`, then
> `H'` has the same labelled pole-to-pole path words and differs from `H` only
> by ordinary redirection of the unique triangle.

Equivalently, one may formulate the lemma as a rigidity theorem for the
intersection of the hidden-pair gauge orbit in Section 4 with the finite union
of allowed JC cycle/theta factor models.  The permitted intersection should
be exactly labelled isomorphism and the three ordinary triangle orientations.

This lemma is substantially narrower than an arbitrary-size atlas: Section 2
reduces its source side to three structural families, and the already proved
support-plus-one/two theorem handles all additional word positions.  But it
is still the load-bearing local algebra.  No statement currently read in the
repository or the cited source proves it.

## 7. Sidecar verdict

**PROVED:** a canonical triangle/triangle-free decomposition does not follow
from the existing bridge and literature theorems.  The first invalid step is
the implicit replacement of a two-terminal contraction by two independently
observable projective factors.

**UNRESOLVED:** whether the JC subvarieties are rigid enough to reduce the
two-terminal gauge to ordinary `T`.  This is the precise remaining local
problem; it must be proved directly or discharged by a complete graph-derived
local certificate.

