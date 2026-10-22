# Brauer projector proof and parameter audit

This AI-assisted, unrefereed edition records an internal AI mathematical audit. Acceptance is limited to the expressly stated projector component and parameter criterion; it is not external human peer review or formal proof-assistant certification. The full original recoupling problem remains PARTIAL. This is a written proof/correction/audit edition, not a computational reproduction package. Source inspection and exact mathematical checks described below occurred in the preceding audit on 11 October 2026. Editorial preparation authenticates the retained records without claiming a fresh scholarly-source inspection or a new mathematical-program run.

Rank 1592, problem 10600014, AMR-105-0014. This is an independently authored proof of the symmetric annihilating projector component. It verifies the recurrence, uniqueness characterization, and coefficient formula attributed to Deng, Jin, and Kauffman. It does not provide the recoupling theory requested in the original problem, and the full problem remains PARTIAL.

## 1. Result and precise scope

Let B_n(d) be the diagrammatic Brauer algebra: its basis consists of the perfect matchings of n upper and n lower vertices, multiplication is vertical stacking, and each closed middle component contributes d. This is the diagrammatic virtual Temperley-Lieb algebra used in the primary source. Throughout, n >= 1. The generic base field is C(d); all coefficients below actually lie in Q(d). Specializations are to C, with no positive-characteristic assertion.

Let m = floor(n/2), and let S_{n,l} be the sum of all basis diagrams having l upper pairs, l lower pairs, and n-2l through strands. The source writes this sum as [n-2l]_n. Define

    a_{n,l}(d) = (-2)^l l! / (n! product_{j=1}^l (d+2n-2-2j)),
    F_n(d) = sum_{l=0}^m a_{n,l}(d) S_{n,l}.

The empty product is 1. Then F_n is the unique nonzero element satisfying all three conditions

    F_n^2 = F_n,
    e_i F_n = F_n e_i = 0,
    v_i F_n = F_n v_i = F_n        (1 <= i < n).

Here v_i interchanges neighboring strands and e_i is the neighboring cup-cap diagram. Both left and right conditions are part of the assertion.

With the standard embedding B_{n-1}(d) -> B_n(d) obtained by adjoining a last vertical strand, the recurrence is

    F_1 = 1,
    F_n = (1/n) F_{n-1}
          - 2(n-1)/(n(d+2n-4)) F_{n-1} e_{n-1} F_{n-1}
          + (n-1)/n F_{n-1} v_{n-1} F_{n-1}.                 (R)

For construction of the entire tower F_1,...,F_n by this literal recurrence, the source's sufficient parameter restriction is

    d not in E_n = {-2j : 0 <= j <= n-2}.

E_1 is empty. The finite upper bound is essential: the displayed set is not a restriction against every nonpositive even number independently of n.

There is a sharper fixed-n statement, proved here rather than inferred by substituting into an undefined recurrence. Put

    P_n = {-2n+2l+2 : 1 <= l <= floor(n/2)}.

The particular idempotent characterized above exists in B_n(d_0), for d_0 in C, if and only if d_0 is not in P_n. At d_0 in P_n, no nonzero idempotent with these simultaneous annihilation and invariance properties exists. This does not say there are no other idempotents in that algebra. At E_n minus P_n the literal tower is blocked, but the fixed-n formula is regular and the direct diagram proof still applies. No evaluation is made at a genuine pole.

## 2. Diagram foundations and dependency boundary

The proof works directly in the free diagram algebra. Thus distinct matchings remain linearly independent at every complex parameter, even if the algebra is not semisimple or a chosen tensor representation is nonfaithful. A pairing is not replaced by its image in an orthogonal-group representation. This distinction matters at exceptional integer parameters.

Associativity follows by stacking three diagrams at once: the external pairing and total number of internal closed components are independent of which two layers are composed first. The identity pairs each upper vertex with the corresponding lower vertex. Reflection in a horizontal line is an anti-involution fixing e_i and v_i.

Stacking the displayed elementary diagrams gives

    e_i^2 = d e_i,                    v_i^2 = 1,
    e_i v_i = v_i e_i = e_i,
    e_i e_j = e_j e_i,                v_i v_j = v_j v_i       (|i-j| >= 2),
    e_i v_j = v_j e_i                                        (|i-j| >= 2),
    e_i e_{i+1} e_i = e_i,            e_i v_{i+1} e_i = e_i,
    e_i e_{i-1} e_i = e_i,            e_i v_{i-1} e_i = e_i,
    v_i v_{i+1} v_i = v_{i+1} v_i v_{i+1},
    v_i e_{i+1} v_i = v_{i+1} e_i v_{i+1}.

Indices are used only when the generators exist. The v_i generate the permutation diagrams, a copy of the symmetric group S_n. Every diagram with l upper pairs can be written as

    sigma (e_1 e_3 ... e_{2l-1}) tau,

where sigma and tau are permutation diagrams. To see this, first relabel upper vertices so that the upper pairs become consecutive prescribed pairs, do the same for the lower pairs, and use the remaining permutation freedom to match the through strands. This factorization creates no loops.

Consequently the permutation diagrams and e_i generate the diagram algebra, and every non-permutation basis diagram has a factor e_i between permutation diagrams and further cup-cap factors. The proof does not import a completeness theorem for a separately presented abstract algebra. Its algebra is exactly the free pairing model specified in the source and original problem. No semisimplicity theorem, classification of simple modules, tensor-category equivalence, or recoupling theorem is assumed.

## 3. The augmentation and uniqueness

Define epsilon on a basis diagram to be 1 for a permutation diagram and 0 for every diagram with fewer than n through strands. Extend it linearly. A product cannot have more through strands than either factor. The product of two permutation diagrams is a permutation and produces no loop. Therefore epsilon is a unital algebra homomorphism B_n(d) -> the base field.

Suppose p is fixed on both sides by all v_i and killed on both sides by all e_i. The factorization just established gives, for every basis diagram b,

    p b = epsilon(b) p,       b p = epsilon(b) p.             (A)

By linearity this holds for every algebra element b. In particular,

    p^2 = epsilon(p) p.

If p is a nonzero idempotent over C(d) or C, then epsilon(p)=1. If p and q are two such nonzero idempotents, (A) gives

    p q = epsilon(q) p = p,
    p q = epsilon(p) q = q.

Thus p=q. This proves uniqueness whenever existence holds, with no semisimplicity restriction.

The left and right S_n actions independently relabel the upper and lower vertices. Their orbits on basis diagrams are exactly the levels l. Hence an element invariant under all v_i on both sides has a unique expression

    p = sum_{l=0}^m a_l S_{n,l}.

There are n! permutation diagrams, so epsilon(p)=n! a_0. Any nonzero idempotent with the required properties must therefore have

    a_0 = 1/n!.

Conversely, once the simultaneous annihilation and invariance conditions and this normalization have been established, (A) proves idempotence automatically. There is no circular use of idempotence to prove existence below.

## 4. Complete contraction count

Fix e=e_{n-1}, and fix an output diagram T whose upper vertices n-1,n are paired. Let T have l upper pairs, hence l lower pairs and n-2l through strands. Such a T has 1 <= l <= m. We count every input basis diagram D for which stacking e above D produces T, recording loops and the level of D.

Only the two upper vertices of D beneath the lower pair of e are affected. The following cases are disjoint and exhaustive.

1. They are paired to each other in D. The input is T, one middle loop is created, and the contribution is d a_l.

2. They are paired to two other upper vertices in D. In T those two other vertices constitute one of the l-1 upper pairs other than the forced pair. Choose that pair and one of the two assignments of its ends to the affected vertices. This gives exactly 2(l-1) inputs at level l, with no loop.

3. One is paired to another upper vertex and the other to a lower vertex in D. In T the selected upper and lower vertices make a through strand. Choose one of the n-2l through strands and choose which affected vertex was attached to its upper end. This gives exactly 2(n-2l) inputs at level l, with no loop.

4. Both are paired to lower vertices in D. In T those lower vertices form one of its l lower pairs. Choose that pair and one of the two assignments of its ends to the affected upper vertices. These are exactly 2l inputs at level l-1, with no loop.

The constructions also recover D uniquely from the stated choices, so there are no uncounted multiplicities. Every output of e has the forced upper pair; outputs without it have coefficient zero. It follows that the coefficient of T in e p is

    (d + 2(l-1) + 2(n-2l)) a_l + 2l a_{l-1}
      = (d+2n-2l-2) a_l + 2l a_{l-1}.                      (C_l)

Thus e p=0 if and only if (C_l)=0 for all 1 <= l <= m. Conjugating by permutation diagrams gives the same conclusion for each e_i. Alternatively the same count applies to any specified upper pair. Reflecting the calculation proves right annihilation as well. Each orbit sum is reflection invariant, so left annihilation already implies right annihilation for this candidate.

This is the central general proof. Its validity is combinatorial for every n; finite enumeration is only an independent check of the count.

## 5. Formula, existence, and exact exceptional set

Over C(d), every factor d+2n-2l-2 is invertible. Starting from a_0=1/n!, equations (C_l)=0 uniquely give

    a_l = -2l a_{l-1}/(d+2n-2l-2)
        = (-2)^l l!/(n! product_{j=1}^l(d+2n-2-2j)).        (F)

The resulting element is invariant under both permutation actions by its orbit-sum definition. Section 4 proves both annihilation conditions. Section 3, with epsilon(F_n)=1, proves F_n^2=F_n and nonzeroness. Section 3 also proves uniqueness. This establishes the generic version of Proposition 2.8 and Corollary 5.5 independently of the source's inductive proof.

All these identities in fact hold in the free diagram algebra over

    R_n = Q[d, (product_{j=1}^{floor(n/2)}
                         (d+2n-2-2j))^(-1)].

R_n is an integral domain. The uniqueness argument works there too because the free diagram module is torsion-free and epsilon(p)=1 follows from (epsilon(p)-1)p=0 for nonzero p. This claim is not extended to arbitrary rings with zero divisors.

For d_0 not in P_n, evaluation R_n -> C at d=d_0 is a well-defined ring homomorphism. It carries the diagram identities, coefficients, and epsilon(F_n)=1 to B_n(d_0). This proves every source-admissible specialization, including d=2, negative odd integers, and negative even integers below the source's finite excluded range. It also proves the additional fixed-n specializations in E_n minus P_n. Their justification is the direct proof and a defined ring homomorphism, not an attempt to evaluate a singular intermediate tower element.

For d_0 in P_n, choose the unique l_0 with d_0+2n-2l_0-2=0. The factors for 1 <= l < l_0 are nonzero and a_0=1/n!. Successively applying (C_l)=0 forces all a_l for l<l_0 to be nonzero. But (C_{l_0})=0 reduces to

    2l_0 a_{l_0-1} = 0,

which is impossible in C. Thus there is no nonzero idempotent satisfying all target properties at a genuine pole. This obstruction does not depend merely on a displayed rational formula having a pole: it rules out any alternative coefficients, including a hypothetical differently normalized or limiting candidate. Nonzero idempotence itself forces the normalization.

## 6. Independent derivation of the recurrence

Work generically and put n=i+1, i>=1. Let F be F_i embedded in B_{i+1}(d), with last strand vertical, and write

    A = F e_i F,       B = F v_i F.

We prove that the corner F B_{i+1}(d) F is spanned by F,A,B, then determine the coordinates of F_{i+1} in this corner.

If a basis diagram D has an upper pair entirely among the first i vertices, then F D=0. For a direct justification, use a permutation of the first i vertices to move that pair to an adjacent pair. A diagram with that upper pair factors as e_j X without division by d: select any lower pair of D, remove the selected upper and lower pairs, and connect their ends by two through strands to obtain X. Left multiplication by e_j restores D with no loop. Invariance of F under first-i permutations and F e_j=0 give the assertion. The corresponding statement for a lower pair gives D F=0.

Any remaining D has no upper or lower pair wholly within the first i vertices. It can therefore have at most one upper pair and at most one lower pair, and any such pair contains the last vertex.

- If it has no pairs, D is a permutation diagram. Under left and right multiplication by S_i, fixing the last vertex is the only invariant distinguishing the two double cosets. These have representatives 1 and v_i. Thus F D F is F or B.
- If it has a pair, it has exactly one upper and one lower pair, each containing the last vertex. Permuting the first i upper and lower vertices independently puts it in the form sigma e_i tau with sigma,tau in S_i. Thus F D F=A.

This proves the span claim for all basis diagrams, including the i=1 boundary where the first case of annihilation is empty.

The augmentation of the embedded F is 1. Applying (A) for F_{i+1} shows

    F F_{i+1} = F_{i+1} F = F_{i+1}.

Hence F_{i+1}=x F+y A+z B for some scalars. Three individual diagram coefficients determine them.

First, the coefficient of the identity in F is 1/i!, whereas its coefficient in A and B is zero. For A, through rank drops. For B, a product of permutations of the first i vertices, then v_i, then another such permutation cannot fix the last vertex. A non-permutation term cannot produce a permutation. Therefore

    x/i! = 1/(i+1)!,       x=1/(i+1).

Second, v_i has coefficient zero in F and A. Its coefficient in B is

    (i-1)!/(i!)^2 = 1/(i i!).

Indeed only permutation terms of the two F factors can contribute. The equation sigma v_i tau=v_i, with sigma,tau in S_i, allows precisely (i-1)! choices: sigma must belong to the intersection S_i intersect v_i S_i v_i, the permutations of the other i-1 vertices, after which tau is determined. Hence

    z/(i i!) = 1/(i+1)!,       z=i/(i+1).

Third, e_i has coefficient zero in F and B. Every non-permutation term in the left F factor has an upper pair among the first i vertices which survives multiplication, incompatible with the upper pair of e_i; the same argument applies to a non-permutation right factor and the lower pair. Thus B cannot contribute e_i, since its remaining permutation terms yield only permutations. The same observation shows that only permutation terms of the two F factors contribute e_i in A. The equation sigma e_i tau=e_i requires sigma and tau to fix vertex i and to be inverse on the other i-1 vertices, giving exactly (i-1)! possibilities. So its coefficient in A is again 1/(i i!). By (F), the coefficient of e_i in F_{i+1} is

    -2/((i+1)!(d+2i-2)).

Consequently

    y = -2i/((i+1)(d+2i-2)).

The three coefficient functionals also prove that F,A,B are linearly independent. Substituting x,y,z gives (R), with precisely the source's coefficients. This is an independent general proof of the recurrence; no appeal to the source's auxiliary identities is needed.

For every n, the complete recurrence tower is defined over

    T_n = Q[d, (product_{j=0}^{n-2}(d+2j))^(-1)]

with T_1=Q[d]. Every coefficient denominator at each earlier stage is invertible there. The generic identity therefore holds in T_n and specializes at every d_0 outside E_n. The pointwise recurrence also holds whenever both relevant fixed-rank elements and its scalar denominator are defined. No claim is made that one can run the literal tower through an undefined step.

## 7. Small ranks and parameter examples

For n=1 there are no e_i or v_i conditions and, after complex specialization, B_1(d_0)=C; the unique nonzero idempotent is 1 for every d. The source's base case needs no division. With S_{n,l} as above,

    F_2 = (1/2) S_{2,0} - (1/d) S_{2,1},
    F_3 = (1/6) S_{3,0} - (1/(3(d+2))) S_{3,1},
    F_4 = (1/24) S_{4,0} - (1/(12(d+4))) S_{4,1}
                                  + (1/(3(d+2)(d+4))) S_{4,2}.

The actual forbidden sets for n=1,2,3,4,5,6 are, respectively,

    empty; {0}; {-2}; {-4,-2}; {-6,-4}; {-8,-6,-4}.

The source's full-tower forbidden sets at these ranks are

    empty; {0}; {0,-2}; {0,-2,-4}; {0,-2,-4,-6}; {0,-2,-4,-6,-8}.

For example, F_3(0)=(S_{3,0}-S_{3,1})/6 is a well-defined projector in the free diagram algebra B_3(0), although F_2(0) does not exist with the target properties and the displayed recursive construction cannot pass through rank 2. This is a proved fixed-rank extension, not an assertion that the recurrence is defined at d=0. At n=3,d=-2, the contraction equation demands 0*a_1+2*(1/6)=0, proving nonexistence of the target projector. At n=2,d=0 it demands 0*a_1+2*(1/2)=0.

The value d=2 is admissible at every rank. Some auxiliary expressions in the printed proof have a removable d-2 denominator when i=1; the source separately specifies x_0=1,y_0=z_0=0 and alpha_0=d. Our proof never introduces that apparent singularity.

The optional zero-strand convention B_0=C and F_0=1 is compatible with the empty diagram. It is not needed for any target statement and is not asserted as a separately stated source theorem.

## 8. Why the virtual invariance hypothesis must stay

For n=2 the sign idempotent H=(1-v_1)/2 satisfies H^2=H and e_1 H=H e_1=0 at every parameter, but v_1 H=H v_1=-H. Thus the annihilation conditions alone do not characterize F_n. Already where F_2 exists there are different nonzero annihilating idempotents unless the virtual-generator condition is retained.

Equation (A) says the verified F_n spans a one-dimensional two-sided ideal and is central. This identifies the symmetric augmentation component. It is not a classification of all primitive idempotents, all exceptional-parameter blocks, or all projectors one might employ in a recoupling category. In particular the nonexistence assertion at P_n concerns only the three simultaneous target conditions.

## 9. Original problem boundary

The original Virtual Knot Theory problem 14, on page 27 of arXiv:1409.2823, asks about projector structure in the Brauer setting and also asks for a useful generalization of classical recoupling theory. The audited family answers a definite projector construction and characterization question. Neither this proof nor the audited source's projector theorem supplies a specified family of fusion objects, fusion multiplicities and bases, admissibility rules, recoupling isomorphisms, coherence identities, and a demonstrated intended virtual-knot application.

The projector component is accepted. The original bundle remains PARTIAL. Recoupling is an explicit residual task, not a consequence of idempotence or coefficient computations, and not silently discharged by this audit.

## References

1. Qingying Deng, Xian'an Jin, and Louis H. Kauffman, Projectors in the Virtual Temperley-Lieb Algebra, arXiv:2103.11355v1, submitted 21 March 2021, 24 pages. https://arxiv.org/abs/2103.11355v1 . The inspected PDF has a 23 March 2021 typesetting footer; that is not a different arXiv submission date.
2. Roger Fenn, Denis P. Ilyutko, Louis H. Kauffman, and Vassily O. Manturov, Unsolved Problems in Virtual Knot Theory and Combinatorial Knot Theory, arXiv:1409.2823v1, retained PDF page 27, problem 14. https://arxiv.org/abs/1409.2823v1 .

The exact retained PDF identities, source inspection record, source-proof corrections, and numerical-check boundaries are recorded in the companion audit. Journal-version comparison remains unverified because the preceding source retrieval encountered a publisher HTTP 403. This proof does not represent the journal text as inspected.
