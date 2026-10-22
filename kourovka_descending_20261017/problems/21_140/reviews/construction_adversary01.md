# Fresh adversarial review of the noncentral approaches to 21.140

Opened **2026-10-17 21:29 UTC**; first review checkpoint **21:33 UTC**.
Discovery estimate toward the full problem: **10%**. This is a validation
checkpoint, not a probability of truth, a solution, or a novelty claim.

## Scope and verdict

Independently reviewed `approach_constructive.md`, `approach_structure.md`,
`structure_tree_closure.md`, and `approach_residual_action.md`, including the
specified primary sources and the exact rational certificate calculation.
The central-extension route and its dependent extension corollary are outside
this review because a separate fresh reviewer was assigned to them.

**Verdict: the core noncentral deductions pass, subject to the scope and
exposition corrections below.** No reviewed construction satisfies all the
hypotheses of 21.140, and no reviewed argument proves the universal assertion.
In particular no group has been promoted merely from `FP_n` to `F_infinity`,
from unbounded finite finiteness lengths to one `F_infinity` group, or from a
single failed embedding to absence of every abstract copy of Thompson `F`.

## Correction requests and resolved scope issues

1. **Uniform graph-wreath hypotheses must be explicit.** The coarse maps and
   finite-label argument concern identical vertex groups, with the head acting
   by vertex permutations preserving their labels. They are not proved here
   for arbitrary twisting automorphisms or arbitrary varying vertex groups.
   The constructive author was notified and added this scope restriction.
2. **Establish finite generation before choosing word metrics.** From finite
   generation of `W=A_Gamma semidirect H`, choose finite reduced words for its
   generators. Their finitely many vertex supports and labels generate a
   subgroup `(A_0)_Y semidirect H`. Equality with `W`, together with the canonical
   vertex projections, forces `A_0=A` and `Y=V(Gamma)`; the quotient also gives
   finite generation of `H`. Hence there are finitely many vertex orbits and
   `A,H` are finitely generated before applying Alonso. The companion action
   note supplies this argument, and the constructive author added it.
3. **Only countable directed-union closure of `HF` is needed.** An `F_infinity`
   group is finitely generated and countable. For nontrivial `A`, distinct
   vertices give distinct nonidentity vertex-labelled elements of `W`, so the
   vertex set is countable. Its finite subsets can be exhausted by a countable
   chain. This supplies exactly the countability required in the hierarchy
   proof. No closure under arbitrary uncountable directed unions is asserted.
4. **Keep ordinary and proper classifying spaces distinct.** The general
   Kropholler–Mislin conclusion is a finite-dimensional model for proper
   actions. Torsion-freeness is what turns it into a free contractible model.
   Similarly, any summary saying elementary amenable `FP_infinity` groups have
   an ordinary finite-dimensional classifying space needs the torsion-free
   qualification; without it, a nontrivial finite group is a counterexample to
   that wording. The source theorem itself and its use for the target are
   correct.
5. **Do not strengthen the graph-wreath primary theorem to `FP_infinity`.**
   Theorem 1.5 of arXiv:2506.02319v2 concerns geometric `F_infinity`, assumes an
   infinite vertex group and a head in `HF`, and assumes an infinite-dimensional
   flag complex. It does not assume cocompactness separately, and does not give
   the proposed general homological analogue. In the present torsion-free,
   nontrivial-input application the vertex group is automatically infinite.
6. **Use precise simplex indexing for finite finiteness lengths.** Original
   Kropholler–Martino Theorems A/C use the module condition `FP_{n-1-p}` for
   `p`-simplices, `0 <= p <= n-1`; equivalently, a clique of cardinality `k`
   contributes stabilizer condition `FP_{n-k}`. The wording of Appendix A.8 in
   arXiv:2506.02319v2 appears shifted if its `i`-simplex is read in the usual
   dimension convention. No present all-dimensional claim depends on that
   wording. Preserve the original indexing in any finite-`n` application.

These are precision requests, not counterexamples to the supported conclusions.

## Hierarchy obstruction: checked without a hidden converse

[Kropholler–Mislin Theorem A, printed p.123](https://ems.press/content/serial-article-files/42793)
has exactly the required form: an `HF` group of type `FP_infinity` has a
finite-dimensional proper classifying space. A torsion-free such group has
finite integral cohomological dimension. Geometric `F_infinity` implies
`FP_infinity` and finite generation. A finitely generated locally-`HF` group
is itself in `HF`, so every target group lies outside `LHF`.

Finite-cd groups lie in `H_1 F`: their finite-dimensional `K(G,1)` gives a free
contractible model. This uses only existence in some finite dimension, not an
unproved equality between geometric and cohomological dimension in dimension
two. Subgroup closure follows by restricting actions and induction. The graph
of groups closures follow from the Bass–Serre tree. For an increasing countable
union, the ray of vertex groups and their inclusions has that union as its
fundamental group, proving the needed closure by the same tree construction.
Extension closure is the standard hierarchy theorem explicitly used with its
source reference in the inspected current primary paper.

Consequently an extension of two `HF` groups, with torsion-free total group
and an infinite-cd kernel, cannot have type `FP_infinity`. This conclusion
does not require a split extension. It does not imply that every group outside
`HF` contains `F`; that unsupported converse remains a central gap.

## Universal exclusion of all abstract copies of F

The primary inputs from Cannon–Floyd–Parry are that every nontrivial normal
subgroup of `F` contains `F'`, that `F'` is simple, and that a dyadic interval
copy of `F` lies inside `F'`. The arguments in the reviewed files use these
facts correctly. They give subgroup, arbitrary product, extension, and directed
union closure for the class containing no `F`. Residual separation by any such
class also excludes `F`: every target homomorphism kills the same nonidentity
element of an embedded `F'`. No residual property of the explicit HNN group is
assumed.

The graph-of-groups strengthening also passes. Brin–Squier's
[Theorem 3.1, printed p.494](https://pi.math.cornell.edu/~justin/Limited2Cornell/PLoI.pdf)
excludes a nonabelian free subgroup in `F`.
[Culler–Morgan, definition on p.573 and Theorem 2.7 on pp.582–583](https://marc-culler.info/static/home/papers/RTrees.pdf)
then give the elliptic/invariant-line/fixed-end alternatives for a simplicial
tree action. In the fixed-end case the integral translation character kills
`F'`; each element in its kernel fixes a tail of a fixed ray. Taking two
generators of an interval copy `F_0 <= F'` gives a common tail and a fixed
vertex. This correctly avoids assuming that `F'` is finitely generated or that
the whole `F'` has a fixed vertex. In the line case perfection kills the
soluble isometry image. In the elliptic case the finite generating pair has
intersecting fixed subtrees. Barycentric subdivision handles inversions.

Thus every tree action of `F` puts an abstract subcopy in a vertex stabilizer.
This is sufficient for closure under arbitrary injective graphs of groups;
it is not the false assertion that `F` has property `FA`.

## Explicit three-generator HNN group: every claimed property checked

With `P=direct_sum Z g_n`, `K=P*Free(a,b)`, `l_n=a^{-n}ba^n`, and
`m_n=g_n l_n`, the `l_n` are a subset of a Schreier basis. Projection to
`Free(a,b)` proves independence of the `m_n`. Thus the indicated HNN edge
maps are injective, and Britton's lemma embeds the entire base.

Every `g_n=t^{-1}l_n t l_n^{-1}`, so the total group `E` is generated by
`a,b,t`. The HNN torsion theorem and the torsion-free base prove
torsion-freeness. Embedded `P` supplies `Z^r` for every `r`, hence infinite
integral cd. Either the hierarchy argument or the independently reviewed
tree-closure argument excludes every abstract `F` in `E`.

The homology computation has no degree-two gap. The edge map on `H_1` is

`[l_n] -> [l_n]-[m_n] = -g_n`,

an injective map of free abelian groups. The edge group is free and has zero
homology in degree at least two. Therefore Mayer–Vietoris gives

`H_j(E;Z) = H_j(K;Z) = exterior_power^j(P)` for all `j>=2`.

At degree one its cokernel is `Z^2`, and the edge map on `H_0` is zero, so
`H_1(E;Z)=Z^3`. Thus the generating rank is exactly three. In particular
`H_2(E;Z)` has the independent basis `{g_i wedge g_j : i<j}` and is not
finitely generated. A resolution finitely generated through degree two would
give finitely generated ordinary second homology after tensoring with `Z`.
Hence `E` is not `FP_2`, and cannot be finitely presented or `F_infinity`.
This is a verified three-of-four boundary construction, not a counterexample.

## Graph-wreath and coloring deductions

The honest retraction to a chosen vertex group is the coarse map
`beta(b,h)=p_u(b)`, where `p_u` is the canonical graph-product homomorphism
killing other vertex groups. It is not generally a group homomorphism on `W`.
Its finite-generator increments and its section are bounded exactly as claimed,
so Alonso's theorem supplies the geometric finiteness inheritance. Treating
arbitrary graph-product elements as coordinate functions would be invalid;
the reviewed proof instead uses the genuine canonical projection.

The no-first-counterexample proposition follows. If both `A,H` had finite cd,
every finite graph product of copies of `A` would have finite cd by the stated
amalgam/direct-product induction. The countable graph-product base and then
`W` belong to `HF`, contradicting torsion-free `FP_infinity` and infinite cd.
Since embedded inputs inherit torsion-freeness and absence of `F`, and their
retractions give `F_infinity`, one input must already satisfy all four target
conditions. This is an inheritance obstruction, not a construction.

The residual finite-coloring proof also passes independently of the quoted
residual-finiteness theorem. The edge difference is nontrivial by a vertex
retraction. Intersecting the finitely many finite-index kernels gives a normal
subgroup `K <= H` that cannot move endpoints of any edge into the same orbit.
Normality is the essential step allowing translation from chosen edge-orbit
representatives to all edges. Its number of vertex orbits is at most
`r[H:K]`. The separate finite-presentation argument correctly supplies finite
vertex and edge orbit sets: omitted edge commutators remain nontrivial in the
induced free product on their endpoints. Empty graph and edgeless graph cases
are addressed. For cyclic vertex groups, this bounds clique dimension and
gives finite cd when the head has finite cd.

The syllablewise coarse reduction to cyclic vertex groups is sound with the
honest geodesic section and `rho(1)=0`: reduced words differ by commuting
syllable swaps, and a generator modifies the final accessible syllable at its
vertex. The suffix commutes with that vertex, so the displayed bounded
increment is valid. The proof is a direct normal-form check rather than an
assumption that a general graph product is a direct sum.

## Finite-length matrix benchmark and computation reproduction

The exact matrix family in `approach_structure.md`, for `n>=2`, agrees with
the primary abstract and §2 of
[Kropholler–Mullaney](https://arxiv.org/pdf/1208.1083): finite presentation,
`FP_{n+1}`, and failure of `FP_{n+2}`. Its diagonal factors generate a
torsion-free multiplicative subgroup; an element of finite order therefore
has diagonal one and then zero additive entry. Its metabelian structure
excludes `F`; conjugates of `U(1)` supply the independent unipotents
`U(1),U(x),...,U(x^{r-1})`. Finite presentation plus `FP_{n+1}` supplies
geometric `F_{n+1}`; the next homological failure prevents `F_infinity`.
Changing `n` does not solve the single-group target.

Reran and inspected `structure_artifacts/verify_f_certificate.py`. Its exact
fraction arithmetic composes PL maps using all breakpoints and inverse images
of breakpoints; equality is equality of reduced piecewise-linear maps. Both
relators evaluate to the identity and the commutator sends `3/4` to `5/8`.
The source presentation plus the proper-quotient theorem proves the embedding
certificate; the computation verifies an existing explicit witness only.
Its rerun is saved beside this review in `construction_adversary01_check.json`.

## Strongest conclusion and exact remaining gap

The verified output is a collection of universal exclusion closures, a
hierarchy obstruction, explicit torsion-free infinite-cd `F`-free groups with
specified failed finiteness properties, and no-go statements for graph-wreath
constructions from simpler inputs. The matrix family even reaches every fixed
finite geometric finiteness length, but never all lengths in one group.

There is still no derivation of the two-relator/noncommutation certificate
from the hypotheses of an arbitrary target group, and no construction of a
single torsion-free `F_infinity` group of infinite cd excluding every `F`.
Postulating an `F`-free envelope that supplies the missing finiteness, or
asserting that nonmembership in `LHF` forces `F`, transfers the unresolved
problem to an unsupported assertion. Those routes stay blocked pending a new
mechanism or evidence. This review does not establish novelty or solve 21.140.

No external outreach, Git operation, pull request, queue mutation, publication,
or release was performed in this review.

## Added checkpoint: the classical Baumslag benchmark

**2026-10-17 21:34 UTC — discovery estimate 10%.** Independently reviewed the
subsequently supplied `constructive_baumslag_benchmark.md`. **PASS** for its
direct derivation, with the residual-specialization precision below. This is
an additional reviewed partial result, not a new candidate solution.

The three-relator presentation really identifies the full group, rather than
only a metabelian quotient. Inductively, conjugating `[a_0,a_n]=1` by `s`
gives `[a_0 a_1,a_n a_{n+1}]=1`; the previously established commutations allow
cancellation and force `[a_0,a_{n+1}]=1`. This is valid also at the base step
`n=1`, where the repeated `a_1` causes no difficulty. The equivalent infinite
presentation is the ascending HNN extension of `Z wr Z` by multiplication of
its normal Laurent-polynomial base by `1+x`. That endomorphism is injective.
Britton's lemma and the ascending localization give exactly

`B = Z[x,x^{-1},(1+x)^{-1}]_add semidirect Z^2`.

Its torsion-freeness, solvability, absence of abstract `F`, and infinite cd
follow as stated. For residual finiteness, specialize a matrix generating
ring, not the entire rational-function field: here the ring is the displayed
localization over `Z`. For a fixed nonidentity matrix, choose a prime
preserving a nonzero numerator and a sufficiently large finite field, then
avoid the roots of that numerator as well as `0,-1`. This defines a
homomorphism on the entire matrix group and separates the chosen element.

The rational calculation is also correct. In `q` variables the tensor-power
ring is localized at the symmetric products
`u=product x_i` and `v=product(1+x_i)`. In characteristic zero the alternating
part is `Delta_q` times its symmetric subring. For `q>=2`, eliminate
`e_{q-1}=v-1-u-sum_{j=1}^{q-2}e_j`; the resulting module is free over
`Q[u^{+/-1},v^{+/-1}]`, with basis `Delta_q` times the monomials in
`e_1,...,e_{q-2}`. For `q=1`, one Koszul operator is multiplication by the
unit `x` (or `-x/(1+x)`), so all head homology vanishes. These facts leave
only the trivial-coefficient `q=0` row and the `p=0,q>=2` column of the LHS
spectral sequence. The candidate differential `(2,0)->(0,1)` has zero target;
there are no other possible nonzero sources or targets. Thus

`H_1(B;Q)=Q^2`, `H_2(B;Q)=Q^2`, and

`H_n(B;Q) = Q[z_1,...,z_{n-2}]` as vector spaces for `n>=3`.

The multiplication-by-Vandermonde identification and free-module argument
are crucial; coinvariants alone would not justify discarding positive-column
terms. They are supplied correctly. The vector-space splitting does not make
a claim about a homology ring. Infinite-dimensional `H_3(B;Q)` prevents
`FP_3` and therefore geometric `F_infinity`, precisely as asserted.

The underlying classical presentation independently matches §2 of the already
inspected Kropholler–Mullaney primary paper. A literature search also located
the [author's thesis, §1 discussion](https://theses.gla.ac.uk/4452/1/2013mullaneyphd.pdf),
which attributes infinite-rank integral higher homology of this example to
Baumslag–Dyer (1982). This attribution reinforces the instruction to make no
novelty claim; the 1982 original has not been fully inspected by this reviewer.
The independent rational calculation above does not rely on that attribution.
