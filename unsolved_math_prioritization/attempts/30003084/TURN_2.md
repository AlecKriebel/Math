# Author turn2: an affirmative theorem for at most nine complex points

**Partial theorem.** Every finite P in P²(C) with |P|<=9 that is not contained in a conic has an ordinary conic in the exact source sense, including reducible conics and unique determination by five distinct points. The argument is elementary quadratic interpolation and Gale duality. It does not settle arbitrary cardinality or claim priority for this small-cardinality consequence.

## 1. Quadratic evaluation and two elementary facts

Choose nonzero homogeneous representatives p_i=(x_i,y_i,z_i) for n distinct projective points, and form the6 by n matrix V with columns

    v_i=(x_i²,y_i²,z_i²,x_i y_i,x_i z_i,y_i z_i)^T.

P is not on a conic exactly when rank(V)=6. Any homogeneous quadratic through a subset is a coefficient vector in the annihilator of the corresponding columns. Thus five points determine an ordinary conic exactly when their columns span a rank5 hyperplane containing none of the other columns. Rescaling point representatives does not change any relevant rank or closure.

We use these facts about distinct point evaluations:

(a) Any set of at most3 columns is linearly independent. For a chosen point p among such a set, the other at most2 points can be killed by a product of at most2 lines that avoid p. This quadratic separates p from the others.

(b) Four distinct columns are dependent if and only if the four original points are collinear. On a line, the space of restricted quadratics has dimension3, so four columns are dependent. Conversely, for four points not all collinear and any chosen p, some pair q,r of the other points has its line avoiding p; otherwise all the points would be collinear. Take that line times any line through the remaining point and avoiding p. This quadratic separates p, proving independence of all four columns.

In particular, five distinct points whose quadratic columns have rank3 must all be collinear: every four-subset is dependent by rank, hence collinear by(b), and these four-point lines must agree. These observations use elementary line restriction, not the real Sylvester–Gallai theorem.

## 2. Gale duality in the precise form needed

Let G be an(n−6) by n matrix whose rows form a basis of ker(V). Regard its columns as vectors g_i in C^(n−6). They may be zero or proportional; no generic-position assumption is made.

For a subset C of the n indices, let I be its complement. Projection of ker(V) onto the coordinates C has dimension rank(G_C), and its kernel is the relation space among V_I. Consequently

    rank(G_C)=|C|−6+rank(V_I).                 (1)

A circuit of G means a minimally dependent nonempty set of its columns; a zero column is a one-element circuit and a proportional nonzero pair is a two-element circuit. If C is a circuit with k elements, then rank(G_C)=k−1, and every C minus one element is independent. Formula(1) gives rank(V_I)=5, and for every j in C it gives rank(V_(I union{j}))=6. Therefore V_I spans a hyperplane containing exactly the columns indexed by I.

In particular, a circuit of G of size n−5 produces exactly five independent V columns and hence an ordinary conic. We will show that absence of such a circuit for n<=9 forces P onto a conic, a contradiction.

## 3. Six and seven points

For n<=5, P is necessarily on a conic, so there is no hypothesis-satisfying case. For n=6 with rank(V)=6, any five columns give an ordinary conic.

For n=7, G has rank1. Its nonzero row is a relation among the nonzero V columns, so it has at least2 nonzero entries (in fact at least4 by Section1(a)). Any two nonzero columns of G form a circuit of size2=n−5. Hence an ordinary conic exists.

## 4. Eight points

Suppose n=8, rank(V)=6 and there is no ordinary conic. Then the rank2 Gale configuration G has no three-element circuit. Any three nonzero columns in three distinct projective directions would be such a circuit. Therefore its nonzero columns have exactly two projective directions, since G has rank2.

Let A and B be the nonempty index classes in these two directions, and C the zero-column indices. After an invertible row change of G, its two rows have disjoint supports A and B, with every entry on the corresponding support nonzero. Therefore the relation space ker(V) is the direct sum of one relation supported on A and one supported on B. Each of A and B is a circuit of V: any relation supported within one class is a scalar multiple of its full-support row.

By Section1(a), |A|>=4 and |B|>=4. Since there are only8 indices, both classes have size4 and C is empty. By Section1(b), each class consists of4 collinear original points. Their union is contained in the union of the two lines, a conic, contradicting rank(V)=6. Thus every admissible8-point set has an ordinary conic.

## 5. Nine points

Suppose n=9 and no ordinary conic exists. The rank3 Gale configuration has no circuit of size4. Delete its zero columns and identify proportional nonzero columns for a moment, obtaining a finite set S of projective directions spanning P²(C).

A four-element circuit in rank3 is precisely four distinct projective directions with no three collinear. Hence S contains no projective quadrangle. We need the following elementary geometry lemma:

**Lemma.** A rank3 projective point set without a quadrangle is contained in the union of one line and one point outside that line.

**Proof.** Choose a noncollinear triangle a,b,c from S. Every other point must lie on one of its three sides, since otherwise it and a,b,c form a quadrangle. If there is an extra point d on ab, different from a,b, then there cannot also be an extra point e on ac, different from a,c: the four points d,e,b,c would have no collinear triple. The same argument excludes an extra point on bc. Thus all additional points are on ab. If there are no additional points, choose any triangle side. This proves the lemma.

Apply the lemma to S, and restore multiplicities. Let A index the columns on the line, B the columns in the outside direction, and C the zero columns. The columns in A have rank2, and those in B rank1. A row-coordinate change puts the line in the first two coordinates and the outside direction on the third axis. Thus ker(V) is a direct sum of a two-dimensional relation space supported on A and a one-dimensional full-support relation on B; all coordinates C are zero in every relation.

The class B is a circuit of V, so |B|>=4. Also |A|>=5: on at most4 distinct original points, Section1(a) gives rank at least min(3,|A|), allowing at most one relation when |A|<=4, whereas A carries a two-dimensional relation space. Since n=9, it follows that |A|=5, |B|=4 and C is empty.

Now rank(V_A)=5−2=3, so Section1 implies that its5 original points are collinear. The4 points in B are also collinear by their circuit property and Section1(b). Again P lies on the union of two lines, contradicting rank(V)=6. Therefore an ordinary conic exists for n=9.

## 6. Scope and next step

The proof handles arbitrary distinct complex projective points, including collinear subcollections and rank-deficient Gale columns. It retains reducible conics, which are essential in the contradiction and may be the ordinary conics obtained. It proves uniqueness because the five-point evaluation rank is exactly5, not merely existence of some conic through five points.

This excludes all counterexamples with at most9 points and gives a structural reason beyond testing a few configurations. The argument stops at n=10, where the Gale configuration has rank4 and the absence of five-element circuits has more complicated possibilities. Finite-dimensional interpolation does not make an unbounded-cardinality theorem automatic.

Two substantive author turns complete; the original general question remains unresolved. Completion estimate30%. The next route will examine the ten-point Gale obstruction and whether its special Veronese origin eliminates the additional bounded-circuit configurations. Three author turns remain unless a full result is obtained earlier.
