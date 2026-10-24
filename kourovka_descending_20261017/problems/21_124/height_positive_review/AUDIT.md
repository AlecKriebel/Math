# Independent adversarial audit of the six-edge positive witness

UTC checkpoint: **2026-10-24T22:57:22Z**. Reviewer:
`/root/p21124_dihedral_adversary`, which did not discover, construct, or author
this positive witness. **Verdict: PASS for this particular six-edge group.**
There are no outstanding substantive objections. The estimate toward a complete
resolution of Kourovka 21.124 remains **6%**. Neither originality nor a complete
solution of the Kourovka problem is certified.

The assigned frozen proof is
`root_orbit/HEIGHT_POSITIVE_WITNESS.md`, SHA256
`5a7a2b188f55025c117d808f921ab8e15d6f703f5ace119fbd66344f8603e421`.
All nine files and byte counts in `HEIGHT_MANIFEST.json` matched. The original
example `positive_hierarchy/HEIGHT_NORM_COUNTERMODEL.md` has SHA256
`1fa8e429e858996244286761f47a90956483e249544ac800801dfcade6329db1`.
No author file or previous review file was edited. No numerical optimizer,
Flint module, or author program was imported or executed by this audit.

## Precise claim and source-group identification

This is the group built from two rank-two abelian vertex groups
`<a,t>` and `<b,s>` and six cyclic edges pairing the following slopes:

    (7,1) <-> (1,1), (7,1) <-> (-1,1),
    (8,1) <-> (4,1), (8,1) <-> (-4,1),
    (13,1) <-> (11,1), (13,1) <-> (-11,1).

Choose the first edge as maximal tree. Its equality is
`T=a^7 t=b s`. Since both vertices are abelian, `(a,T)` and `(b,T)` are also
integral bases of their vertex groups. The five remaining relations are

    u_i^-1(a^p_i T)u_i=b^q_i T,
    (p_i,q_i)=(0,-2),(1,3),(1,-5),(6,10),(6,-12).

I checked the shifts from every original edge directly: `p=x-7`, `q=y-1`.
In particular, the positive `p=1,6` values in these edge relations must not be
confused with the negative left exponents in the mapping-torus automorphism.

The claimed result is that this one group has (VRC), hence is virtually special
by the cited tubular criterion. It is a different group from the three-Pell-pair
test group, so it contradicts none of the earlier abelian or dihedral exclusions.
It also does not contradict the failure of a common Schur-complement metric on
the original graph. That metric restriction is not a necessary condition for
an embedding into a larger Euclidean-by-finite group.

As an eligibility cross-check, the original matching lengths are
`50,50,65,65,170,170` for the forms `x^2+y^2` and `x^2+49y^2`.
The primitive height-one edges have trivial stabilizer in the height kernel.
That kernel has two cyclic vertex groups and the rank-five graph contribution,
so it is `Z*Z*F5=F7`. The usual tree-of-flats argument establishes the already
reviewed CAT(0) property. These observations identify the intended eligible
example; the new positive witness does not rely on a false equality of its
original vertex height norms.

## Independent exact certificate checks

Run `python3 independent_check.py` from this review directory, or by its path.
It writes only this directory's `independent_results.json`. Its complete input
hashes and all resulting signed projection distributions are in that file.

I reconstructed the full signed atomic measure from the 82 positive-support
entries. Every multiplicity is a positive integer. Adding the prescribed
negative triples gives 164 distinct signed support points and exactly
**4,370,132** indexed coordinates. The coordinate blocks in the separate
permutation certificate cover the entire indexed set without overlap or gaps
and reproduce exactly the same signed measure.

For each of the five pairs I aggregated both **signed** projections with their
complete integer multiplicities, rather than comparing only absolute values,
moments, or approximate masses. The two distributions agreed exactly. Their
distinct value counts are `41,47,47,69,69`.

For every permutation segment `(source,destination,length,value)`, I checked
both complete interval partitions. Sorted source intervals and sorted
destination intervals each tile `[0,N)` exactly once. Hence interval translation
defines an actual bijection of all `N` integer indices. The respective segment
counts are `269,279,281,259,259`, totaling **1,347**.

I then independently swept the source and destination coordinate-block
boundaries through every segment. On each resulting constant-coordinate
subinterval, I verified

    p*A_source+H_source=q*B_destination+H_destination=value.

This verifies every coordinate of every equation. There are
**21,850,660 coordinate equalities** across the five permutations; none are
sampled, inferred from a floating-point residual, or omitted. In this particular
certificate every listed segment already lies within one block on each side,
but the independent checker also handles and splits crossings instead of
assuming that property.

The uncompressed permutations and vectors need not be stored in enormous
arrays: the interval specification defines their values at every integer index,
and the exact partition and block-sweep checks prove the stated literal finite
identities. The numerical support search and rational elimination are discovery
history, not unverified premises of the proof.

## Conjugation direction and extension to the actual group

Let a permutation `P` act by `P e_j=e_(Pj)`. Then
`(P v)_(Pj)=v_j`. The checked source-to-destination convention therefore proves
exactly

    P_i(p_i A+H)=q_i B+H.

In a translation semidirect product the multiplication rule is
`(v,S)(w,R)=(v+S w,SR)`. Thus the map

    a -> ((A,0),1),  b -> ((B,0),1),  T -> ((H,1),1),
    u_i -> ((0,0),P_i^-1)

has the required conjugation direction: `u_i^-1` acts on a translation by
`P_i`. The extra last coordinate is fixed by every permutation. Both sides of
each edge relation have last coordinate one, and the other coordinates are
the checked identity. Vertex commutators vanish because their images are
translations. This verifies all defining relations and hence gives a
homomorphism of the whole group.

This inverse convention is essential for the actual supplied permutations.
For example, in the first relation the segment sending index 2,299,087 to
1,690,404 has reverse-orientation values `-18` and `-20`. Therefore replacing
`u_i -> P_i^-1` by `u_i -> P_i` is not justified. The independent certificate
contains one exact reverse-orientation failure for each of the five relations.

Returning to original generators gives translations
`t -> (H-7A,1)` and `s -> (H-B,1)`. Hence `a^7 t=b s` maps identically to
`(H,1)`. Every original non-tree edge then uses precisely the same certified
pair, as checked by `p=x-7`, `q=y-1`. This checks the maximal-tree identification,
rather than constructing a homomorphism of a merely similar presentation.

## Vertex injections and discreteness

The vectors `A` and `B` are nonzero. The last coordinate of both is zero, while
the last coordinate of the image of `T` is one. Thus each pair `(A,0),(H,1)`
and `(B,0),(H,1)` is real linearly independent. An integer relation in either
vertex first has zero `T` coefficient by its last coordinate and then zero
remaining coefficient because `A` or `B` is nonzero. Both rank-two vertex
restrictions are injective.

For an additional exact rank certificate, the first displayed signed support
triple `(1,-3,2)` gives two-by-two minors

    (a,T): [[1,2],[0,1]],    (b,T): [[-3,2],[0,1]],
    (a,t): [[1,-5],[0,1]],   (b,s): [[-3,5],[0,1]].

Their determinants are `1,-3,1,-3`, all nonzero. Every translation coordinate
is integral, so these vertex images are discrete subgroups of the Euclidean
translation space. The generated linear group is a subgroup of the finite
symmetric group on `N` indices, fixing the last coordinate; it is finite and
orthogonal. Thus the constructed target is a legitimate
`R^(4,370,133) semidirect Q` Euclidean-by-finite group. No explicit computation
of the order or generators' orders is needed for that finiteness statement.

## External theorem application and limitations

I freshly read the primary [Merladet Urigüen–Minasyan paper, version
3](https://arxiv.org/html/2505.18054v3), specifically Theorem 1.6(ii) and
Proposition 1.10. The first criterion applies to a finite graph of finitely
generated virtually abelian vertex groups and the verified discrete injective
vertex images. It yields (VRC). The second applies to tubular groups with
(VRC), yielding a finite-index subgroup embedded in a finitely generated RAAG.
Our six-edge group satisfies both sets of hypotheses. No compact-specialness
claim or extra cocompact cubulation conclusion is inferred from these results.
The cached primary HTML used as the stable file reference has SHA256
`4917ad68415a2c0d17605f31fdb717a7b822a05ffd553a04984b0a1161434507`.

**No substantive correction is required.** This is a rigorous affirmative
result for the specific test group. The positive construction relies on its
particular exact atomic measure. No argument currently extends the construction
to every CAT(0) free-by-cyclic group, or even to every compatible tubular
presentation. A complete general mechanism or a valid negative example remains
the gap for 21.124. This audit does not establish originality, justify a solved
Kourovka publication, or verify a DOI/tracker entry.
