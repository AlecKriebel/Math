# Delta 1: abelian extraction is insufficient, even for a power word

Status: explicit obstruction to an attempted proof mechanism, not a counterexample to 21.122. Written after checkpoint 1 was frozen.

An attractive idea is to show that an infinite word image must already be infinite on a closed abelian subgroup. This is false even for the one-variable power word `w=x^p`, with `p` any odd prime, on a nilpotent profinite group of class two.

Let

`V = product_(i>=1) Z/p^2 Z`,

`C = product_(i<j) F_p`,

and put `G=V x C` as a topological space. Write `bar(a)` for coordinatewise reduction of `a in V` modulo `p`, and set

`beta(a,b)_(ij) = bar(a_i) bar(b_j)` for `i<j`.

Define the product by

`(a,c)(b,d) = (a+b, c+d+beta(a,b))`.

The map beta is additive in both arguments, so the cocycle identity follows immediately; zero is an identity, and the inverse of `(a,c)` is `(-a,-c+beta(a,a))`. All coordinate operations are continuous. Thus `G` is a profinite group, the inverse limit of the finite versions on the first `n` coordinates. The subgroup `0 x C` is central and the commutator is given, up to sign according to convention, by

`beta(a,b)-beta(b,a)`.

Consequently two elements commute exactly when all the two-by-two minors of the two rows `bar(a),bar(b)` vanish. If one row is nonzero, choose a nonzero coordinate in it; the minors show that the other row is its scalar multiple. Therefore the image modulo `p` of any abelian subgroup is a vector space of dimension at most one.

For every integer `m>=0`, induction gives

`(a,c)^m = (m a, m c + binomial(m,2) beta(a,a))`.

Because `p` is odd, multiplication by `p` and by `binomial(p,2)` vanish in `C`. Hence

`(a,c)^p = (p a,0)`.

It follows that

`G_w = pV x {0}`,

which is an infinite profinite elementary abelian group of cardinality continuum. Nevertheless, for every abelian subgroup `B<=G`, the set of p-th powers of elements of `B` has at most `p` elements, since `p a` depends only on `bar(a)` and the image of `B` modulo `p` has dimension at most one. This holds for abstract abelian subgroups too, and hence in particular for every closed abelian subgroup.

In the finite stage on `n` coordinates, the full p-th-power image has size `p^n`, while every abelian subgroup has p-th-power image of size at most `p`. Thus no bound on the full image can be inferred merely from this uniform bound on all abelian restrictions.

The genuine power map in this example avoids thin splitting because `(xy)^p=x^p y^p` for all `x,y` in `G`, even though `G` is nonabelian. Its full image is a compact subgroup. A successful argument must exploit how distinct noncommuting preimages combine, rather than relying on an abelian source subgroup carrying all variation.

This is an elementary construction; no priority or novelty claim is made. It does not suggest that the target dichotomy fails.
