# Independent algebraic decomposition and complete path falsification

Source-first: native manuscript, full TeX and own fresh rasters only. No support, code/results, archived/current opinions or foreign body has been consulted.

## 1. A filtration-adapted integral basis gives the barcode directly

The nonempty simplices have birth indices a=1,b=2,c=3,d=4,cd=5,bd=6,ac=7. All endpoints precede their edges, so this is a valid simplex-wise simplicial filtration. The underlying graph a-c-d-b is connected with four vertices and three edges and is a tree, hence an interval. No 2-simplices or higher boundary maps exist.

Work first over the integers. In C0 use the basis

u1=a, u2=b-a, u3=c-b, u4=d-c.

Its matrix relative to a,b,c,d is unit triangular, determinant1, and its initial i generators span exactly the first i vertex chains. It is therefore filtration adapted, with births1,2,3,4, over EVERY field, without division. Alphabetical edge orientations give

partial(cd)=u4,
partial(bd)=u4+u3,
partial(ac)=u3+u2.

At stage5 the boundary span is <u4>; at stage6 it is <u4,u3>; at stage7 it is <u4,u3,u2>. Before these stages the corresponding u's are independent modulo the previous boundary span. The H0 persistence module is therefore the direct sum of intervals [1,infinity), [2,7), [3,6), [4,5). These are explicit compatible bases of the quotients, not just a list of dimensions. Pairings are (b,ac),(c,bd),(d,cd). All determinant/pivot coefficients used are +/-1, so characteristic2 and every other characteristic give the same result. There is no reduced-H0 versus ordinary-H0 ambiguity for the THREE FINITE pairs; only the eternal a class changes on augmentation.

The explicit integral killing cycles are u4=partial(cd), u3=partial(bd-cd), u2=partial(ac-bd+cd). Thus ac-bd+cd is the underlying oriented path from a to b as a 1-chain, but this algebraic combination is not a directed gradient path in the fixed matching. The difference is structural, not numerical cancellation error.

## 2. Full incidence graph and a strict potential

There are exactly six vertex-edge incidences: a<ac,c<ac,b<bd,d<bd,c<cd,d<cd. In the persistence pairs only d<cd is incident. Thus V={(d,cd)}; b,ac,a,c,bd are critical. Orient the matched incidence d->cd upward and all five other incidences downward. The entire edge list is

ac->a, ac->c, bd->b, bd->d, d->cd, cd->c.

The potential values ac:6, bd:5, d:4, cd:3, c:2, b:1, a:0 strictly decrease along EVERY arrow, proving the field acyclic. From ac the only first choices are a,c; both have outdegree0. Therefore all maximal paths from ac are exactly (ac,a) and (ac,c). Its reachable set including the starting cell is {ac,a,c}, so b is absent, and the number of ac-to-b paths is exactly0. No path-length convention can create a missing reachable endpoint. The earlier nonincident pair (c,bd) has exactly one directed path bd,d,cd,c; the other maximal path bd,b does not reach c.

Both endpoints of the targeted pair are critical in V and differ in dimension by one. This rules out a possible escape through endpoint eligibility, conditional on the manuscript's precise foreign conjecture interpretation. Incidence of c with ac does not put c into V: c is paired by persistence with NONincident bd, so it remains unmatched.

## 3. Updated-field control, kept distinct

Reverse the unique bd,d,cd,c path. The new matching is V'={(d,bd),(c,cd)}. Its complete arrows are ac->a, ac->c, c->cd, cd->d, d->bd, bd->b. Potential values ac:6,c:5,cd:4,d:3,bd:2,b:1,a:0 decrease strictly, so it too is a discrete gradient. Now exactly one ac-to-b path exists: ac,c,cd,d,bd,b. This is a change of field; it cannot repair the zero count in V. Treating the nonincident pair (c,bd) itself as an upward incidence would invent a nonexistent face relation, so that alternative graph is inadmissible.

## 4. Independent H0 rank-invariant calculation

For each stage j, components are: stage1 {a}; stage2 {a},{b}; stage3 {a},{b},{c}; stage4 four singletons; stage5 {a},{b},{c,d}; stage6 {a},{b,c,d}; stage7 {a,b,c,d}. For i<=j, the rank of H0(K_i)->H0(K_j) is the number of components at j that meet the vertices born by i. Distinct such components give independent basis images over every field. The triangular rows (j=i through7) are

i1: 1,1,1,1,1,1,1
i2: 2,2,2,2,2,1
i3: 3,3,3,2,1
i4: 4,3,2,1
i5: 3,2,1
i6: 2,1
i7: 1.

The barcode above gives exactly the same ranks by counting intervals with birth<=i and death>j. This is an independent finite check on endpoint indexing. In particular a death at stage7 is absent at stage7, not stage8. The boundary basis argument already proves all fields, while the component calculation supplies a different topological mechanism.

## 5. Current strongest result and exact remaining gate

The fixed finite filtration's complete barcode, incident matching, acyclic path graph, zero targeted path count and distinct cancellation outcome have actual elementary proofs above. Own machine controls independently calculate the finite objects with ordinary assertions and integer sets. This confirms the example under the stated definitions. Whether those definitions exactly match the original 2008 conjecture—including any ambient-dimensional/filtration/function restrictions and path convention—is an essential foreign-primary obligation still CLOSED here. No narrower replacement claim, minimality assertion, first-priority certification or final disposition is promoted. Follow-up null.
