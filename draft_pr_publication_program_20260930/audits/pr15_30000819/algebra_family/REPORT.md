# Independent adversarial algebra review of PR15

**Independent verdict: narrow PASS.** No mandatory mathematical correction
was identified in the theorem stated at `source_snapshot/PROOF.md:60`–`67`.
For a finite set of distinct degree-one lattice generators, saturation in
their generated group, intrinsic normalized volume `V`, and finite nonempty
holes, the proof establishes

\[
h\le 2V^2(V-1)^2-2.
\]

This verdict was reached before reading an old review or another family's
conclusions. It concerns the frozen proof attributed by the parent audit to
head `e1cd2bcd1345d2d24f5610a40487b40e8a771b9c`. It does not certify
historical novelty or resolve the potentially sharp source question `h <= V`.
The exact remaining gap is an estimate strong enough to replace the quartic
function by the proposed sharp volume or Eisenbud–Goto expression.

## Claim and falsification criteria

Write `a_i=(v_i,1)`, `S=N A`, `G=Z A`, `r=rank G=d+1`, and `c=n-r`.
The lattice on the affine slice is `L=Z{v_i-v_1}`. The volume in this report
is normalized in `L`, not an arbitrary larger lattice. The normalization
semigroup is `bar S=cone(A) intersect G`. Holes are its elements absent from
`S`. No completeness assumption `A=P intersect L` is imposed.

A defect would be mandatory if, under exactly these hypotheses, it made
the no-pyramid lemma, circuit/support bounds, regularity estimate, or
normalization-to-last-hole inequality false or inapplicable. In particular,
the audit tried to falsify the proof by lattice-index changes, missing
degree-one lattice points, dimension one, a free apex, a normalization that
need not be generated in degree one, and either possible one-step error in
the final regularity shift.

## Independent reconstruction of the combinatorial inputs

### A free column propagates every hole

Suppose `a_i` is outside the real span of the other columns, which generate
`S'` and `G'`. The real decomposition along that column is unique, so

\[
S=S'\oplus\mathbb N a_i,\qquad G=G'\oplus\mathbb Z a_i.
\]

If `x+t a_i` lies in `cone(A) intersect G`, its group decomposition forces
`t` to be an integer, and its cone decomposition forces `t>=0` and
`x in cone(A')`. Consequently

\[
\bar S=\bar S'\oplus\mathbb N a_i,\qquad
H=(\bar S'\setminus S')\times\mathbb N.
\]

Thus any hole gives infinitely many distinct holes. This proves the exact
configuration statement at `PROOF.md:75`–`97`; it is not an assumption about
the shape of `P`. It also verifies the failed apex mechanism independently.

### Circuit degree is bounded by intrinsic volume

Here is a determinant derivation of the input at `PROOF.md:109`–`113`.
Let `u` be a primitive circuit relation with support `C` of size `s`.
Its columns have rank `s-1`. Adjoin columns from `A` that extend this span
to rank `r`; this needs `r-s+1` columns. The resulting configuration `B`
has `r+1` columns and exactly one rational relation, namely `u` with zero
entries on the added columns.

Take a lattice basis of `G_B=Z B`, and express `B` as an integral matrix
`M` in that basis. Its columns generate the entire basis lattice, so the
gcd of its maximal minors is one (equivalently, its Smith invariant factors
have product one). The vector of signed maximal minors spans `ker M`.
Primitivity therefore makes these minors exactly the coordinates of `u`,
up to an overall sign.

Since the height map on `G_B` takes every column to one, it is onto `Z`;
an affine lattice simplex obtained by omitting column `i` has normalized
volume `|u_i|` in the degree-zero lattice of `G_B`. The usual circuit
triangulation consists of the simplices `B minus {i}` for `u_i>0`.
For completeness, given a convex representation of a point of `conv(B)`,
move its coefficient vector along the unique relation until the first
positive-side coefficient becomes zero. This places the point in one of
those simplices. Uniqueness of this endpoint gives disjoint interiors.
Hence

\[
\operatorname{Vol}_{G_B}(\operatorname{conv} B)
=\sum_{u_i>0}u_i=\deg u.
\]

The index `e=[G:G_B]` is a positive integer. Its degree-zero slice has the
same index. Measuring `conv(B)` in the larger lattice multiplies that
volume by `e`. As `conv(B)` is full dimensional and contained in `P`,

\[
V\ge e\deg u\ge\deg u.
\]

This proves the circuit bound even when the circuit's support is lower
dimensional or generates a proper sublattice. There is no reversed index
factor hidden in the argument.

### Codimension and number of columns

A triangulation using every point of `A` as a vertex exists by successive
insertion of the finitely many points. Its full-dimensional simplex dual
graph is connected: a generic path in the convex polytope crosses facets
and avoids faces of codimension at least two. If it has `t` top simplices,
ordering them along a spanning tree shows that the first introduces `d+1`
vertices and each later simplex at most one. Thus `n<=d+t`. Every simplex
has positive integer volume in `L`, so `V>=t`, giving `c<=V-1`.

Circuits span the rational relation space. To check this directly, if a
relation is not support-minimal, choose a nonzero smaller-support relation
and subtract a multiple that cancels one coordinate. Both this relation
and the residual have smaller support; induction expresses the original
as a combination of circuits. Choose `c` independent primitive circuits
forming a basis.

Each homogeneous circuit has disjoint positive and negative supports and
equal positive and negative coefficient sums. Its support therefore has
at most `2 deg u <=2V` entries. If a coordinate were absent from every
selected basis vector, it would be absent from every relation, making
that column free. The finite nonempty hole hypothesis excludes this.
The union of basis supports covers all `n` coordinates, whence

\[
n\le 2Vc\le2V(V-1).
\]

These arguments validate `PROOF.md:114`–`155` without restricting `A` to
the complete lattice-point set.

## Independent reconstruction of the toric regularity interface

In a fixed sign orthant, the cone `K=ker_R A intersect orthant` is pointed
and has dimension at most `c`. Its primitive extremal rays are circuits:
if the relation space restricted to a ray vector's support had dimension
at least two, a sufficiently small positive and negative perturbation
inside that support would stay in the orthant, contradicting extremality.

Let `g` be a Graver relation, meaning a nonzero integer relation with no
nontrivial conformal decomposition. Conic Carathéodory expresses it as

\[
g=\sum_{j=1}^q\lambda_j u_j,\qquad q\le c,
\quad\lambda_j\ge0,
\]

where `u_j` are primitive circuit rays in its orthant. If a coefficient is
at least one, `g-u_j` is both an integer relation and in the same orthant.
It contradicts indecomposability unless `g=u_j`. Except for that case all
coefficients are less than one. Degree is linear on this sign cone, so

\[
\deg g=\sum_j\lambda_j\deg u_j\le cV.
\]

This supplies an independent proof of the Graver estimate; it does not
replace it with the false assertion that Graver degrees always equal
circuit degrees.

A binomial in a reduced toric Gröbner basis is conformally indecomposable.
Otherwise decompose its relation as `g=v+w` with compatible signs. If the
positive monomial of `g` leads, at least one of the positive monomials of
`v,w` leads in its own binomial, by multiplicativity of the term order.
It is a proper divisor of the leading monomial of `g`, contradicting its
being a minimal initial generator. A common monomial factor is excluded
by the same smaller-leading-monomial argument. Thus each minimal generator
of an initial ideal has degree at most `D=Vc`.

For the Taylor resolution of that initial monomial ideal, each variable's
exponent in any least common multiple is at most `D`. Every shift has
degree at most `nD`; subtracting its nonnegative homological index can
only decrease the regularity contribution. Gröbner degeneration of a
homogeneous ideal gives `reg I_A <= reg in(I_A)` by semicontinuity of
graded Betti numbers. Therefore

\[
\operatorname{reg} I_A\le nVc.
\]

The cited [Sturmfels paper](https://arxiv.org/pdf/alg-geom/9610018),
pp. 10–11, was independently consulted. Its regularity notation refers
to the ideal; its homogeneous toric estimates impose neither normality
nor a complete lattice-point configuration. Its degree lattice agrees
with the generated affine lattice. In the current finite-hole setting,
degree equals `V` also because `R_k` and the intrinsic Ehrhart layer agree
for all sufficiently large `k`. This confirms the citation and convention
at `PROOF.md:161`–`181`.

## Normalization, support, and the last hole

### Finiteness does not require degree-one generation

Triangulate the cone over `P` by cones on simplices with columns in `A`.
For `u in bar S`, choose such a cone and write `u=sum lambda_i a_i` with
`lambda_i>=0`. Removing the integer parts leaves a lattice point in the
bounded fundamental parallelepiped of that simplex. Only finitely many
such remainder points occur in `G`, over finitely many simplices. Thus
`bar R=C[bar S]` is a finite graded `R`-module.

Every normalized monomial has a positive power in `R`, since its cone
coefficients may be chosen rational. The saturated cone semigroup ring
is normal, giving the normalization in `Frac R`. Neither fact asserts
that its algebra generators have degree one. Accordingly that potential
hidden hypothesis is absent at `PROOF.md:188`–`195`.

The monomial basis of `bar R` contains that of `R`, so `C=bar R/R` has
exactly the hole classes as a homogeneous vector-space basis. Finite
holes imply finite dimension and, because multiplication raises degrees,
annihilation by a sufficiently high power of `m=R_+`. Thus `C` has finite
length, `H^0_m(C)=C`, higher local cohomology zero, and `end C=h`.

### The local-cohomology support is correct

For each positive-degree `u in bar S`, a positive multiple `ell u` lies
in `S`, and `t^(ell u)` belongs to `m`. Hence `t^u` belongs to the radical
of `m bar R`. Conversely `m bar R` is contained in the positive-degree
maximal ideal `bar R_+`, which has quotient `C`. It follows that

\[
\sqrt{m\bar R}=\bar R_+.
\]

This also identifies local cohomology over `R` with support in the extended
ideal; a Čech complex on the original degree-one generators computes it.
No standard grading of `bar R` is needed.

Both rings are domains, so a nonzero element is not killed by a power of
the nonzero ideal `m`; their zeroth local cohomology vanishes. If `d=0`,
distinctness makes `A` a singleton and the generated-group semigroup free
and normal, giving no holes. The nonempty case therefore has `r>=2`.

Hochster's normal monomial-ring theorem applies to `bar R`, hence its
depth at the vertex is `r` and its local cohomology below degree `r`
vanishes. The hypotheses can be checked directly against the original
[Hochster paper](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Hochster.pdf)
and its [publication record](https://annals.math.princeton.edu/1972/96-2/p05).
Allowing Laurent coordinates causes no restriction: a pointed rational
cone embeds its lattice semigroup in a nonnegative orthant by integral
linear forms. In fact, normality and Serre's `S_2` alone would suffice for
the two vanishings needed here.

The long exact sequence of `0 -> R -> bar R -> C -> 0` now reads

\[
0\longrightarrow C\longrightarrow H^1_m(R)\longrightarrow0.
\]

This proves the claimed isomorphism. Standard-graded regularity of `R`
uses `sup_i(end H^i_m(R)+i)`, so `reg R >=h+1`.

### The final indexing is correct

With `c=0`, the columns are independent and an element of the cone in
their generated group has nonnegative integer coordinates, so `H` is
empty. Hence the current theorem has nonzero `I_A`. Because the points
are distinct, it has no degree-one relations, although the usual shift
works even for a nonzero ideal with linear generators.

If `F` is the minimal graded resolution of `R=Q/I_A`, its zeroth module
is `Q`, and its positive part is the resolution of `I_A` shifted by one
homological index. Thus `reg R=max(0,reg I_A-1)`. A nonzero homogeneous
ideal in `Q_+` has `reg I_A>=1`, yielding `reg I_A=reg R+1`. Combining
the two shifts gives exactly

\[
h\le\operatorname{reg}I_A-2
\le nVc-2\le2V^2c^2-2\le2V^2(V-1)^2-2.
\]

There is no missing `+1` or unjustified assumption that `R` is
Cohen–Macaulay. Indeed a finite nonempty quotient here forces `R` to have
nonzero first local cohomology. This completes the algebraic reconstruction
of `PROOF.md:197`–`225`.

## Boundary cases and exact computational controls

- `d=0`: one distinct point, free normal semigroup, no holes.
- `c=0`: independent columns, normal in their generated group, no holes.
- `c=1`: the toric ideal is principal, so `R` is a hypersurface and
  Cohen–Macaulay. If `r>=2`, the preceding isomorphism forces finite `C`
  to be zero. Thus nonempty finite holes actually require `c>=2`, a safe
  strengthening of the proof's weaker `c>=1`.
- `V=1`: `c<=V-1` forces `c=0`, so no holes. The theorem is explicitly
  limited to nonempty holes. The optional convention `h=-1` for empty
  holes must not be used to extend its displayed formula to `V=1`, where
  that formula's right side is `-2`.
- Proper ambient index: larger-lattice volume is the intrinsic volume
  multiplied by the index. The quartic is increasing for integer `V>=2`.
  If ambient saturation is used instead, a proper index gives infinitely
  many holes: choose `b` in an absent group coset and an integral interior
  cone point `e in G`; then `b+t e` is in the cone for all sufficiently
  large integers `t`, stays outside `G`, and has unbounded height.
- Missing points: `A={0,1,3,4}` has exactly the degree-one hole `(2,1)`.
  Each of its four degree-one generators kills this class in `C`, and the
  missing monomial's square lies in `R`. This checks the finite-length
  support concretely without completing `A`.
- Free apex: adjoining an independent apex to this last configuration
  leaves `(2,k-1,k)` as a hole for every `k>=1`. The fixed-volume
  construction therefore fails the finite-hole hypothesis.

The independent [exact checker](exact_checks.py) and
[results](exact_checks.json) use integer sets and arithmetic only. They
enumerate all 4,095 endpoint-containing subsets of intervals of length at
most 12; 4,016 have generated lattice `Z`. The latter contain 1,025
finite-hole configurations, of which 1,013 have nonempty holes, and
2,991 configurations with explicit infinite-hole witnesses. The checker
also verifies 179,792 primitive three-point circuit relations. No failure
occurred. These finite tests corroborate boundary handling and are not the
proof of the general theorem.

The finite-hole certification in dimension one is exact: after intrinsic
normalization, a configuration containing endpoints `0,V` has finite holes
if and only if it contains both `1` and `V-1`. Missing either gives the
persistent hole `1` or `kV-1` in degree `k`. Having both includes
`{0,1,V-1,V}`, whose exact sumset is the displayed interval union in the
frozen proof, covering every degree at least `V-2`.

For `A_m={0,1,m-1,m}`, `m>=4`, the degree-`k` hole count is exactly
`k(m-k-2)` for `1<=k<=m-3` and zero otherwise. Thus `h=m-3`. Its
normalization is the `m`-th Veronese ring of `C[s,t]`; its top local
cohomology in degree `j` is `H^1(P^1,O(mj))`, whose last nonzero degree is
`-1`. Since `H^1_m(R)=C` and higher local cohomology agrees with the
normalization, `reg R=max(h+1,1)=m-2` and `reg I_A=m-1`. The final
subtract-two inequality is equality throughout this family. Exact sumsets
were checked for `m=4,...,30`. The cohomology derivation, not a numerical
surrogate, supplies these regularity values.

## Final scope and suggested disposition

Mandatory mathematical issues: **none identified**. Optional editorial
clarification: at `PROOF.md:65`–`67`, say explicitly that the `h=-1`
empty-hole convention does not extend formula (2.1) to `V=1`, or use
`h=-infinity`. This does not affect the stated nonempty-hole theorem.

The proof verifies a coarse classical corollary under the stated precise
semigroup hypotheses. The sharp source reading and novelty remain
unresolved. This family's recommendation is **retain partial /
source-scope hold**, with the independently verified quartic theorem and
its exact assumptions stated clearly. No release, outside communication,
or canonical edit was performed by this family.
