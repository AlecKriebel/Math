# Turn 4: exact three-qubit mixed-state detection regions

**4/5 substantive author turns.** This turn upgrades the odd-party estimates to exact complex projective norms for a two-parameter three-qubit family, including noisy and dephased GHZ states. It proves the complete relative detection regions within that family. The source's general mixed-state classification remains separate.

## 1. A binary cubic norm with matching primal and dual certificates

Let e_0,e_1 be an orthonormal basis of C². For A>0 and 0<=B<=A define the symmetric three-tensor

    T(A,B)=A e_0^tensor3
       +B(e_0 tensor e_1 tensor e_1
           +e_1 tensor e_0 tensor e_1
           +e_1 tensor e_1 tensor e_0).

Its complex projective norm is exactly

    ||T(A,B)||_pi=(A+B)^(3/2)/sqrt(A).                   (1)

Put u=sqrt(A/(A+B)), so 1/sqrt(2)<=u<=1, and W=(A+B)^(3/2)/sqrt(A). Define the real unit vectors

    q_+=u e_0+sqrt(1−u²)e_1,
    q_-=u e_0−sqrt(1−u²)e_1.

Direct expansion gives

    T(A,B)=(W/2)(q_+^tensor3+q_-^tensor3),               (2)

because Wu³=A and Wu(1−u²)=B. Hence the norm is at mostW. The explicit norm-one complex trilinear form T_u of turn3 evaluates both repeated unit vectors in (2) to1. Its value on T(A,B) isW, giving the opposite inequality. This proves (1) without assuming equality of real and complex nuclear norms or using a numerical tensor optimization. The boundary B=0 is included by u=1.

## 2. The density-matrix family and physical region

For 0<=p<=1 and z in C set

    rho_(p,z)= (p/2)(|000><000|+|111><111|)
              +(1−p)I_8/8
              +(z/2)|000><111|+(conjugate(z)/2)|111><000|. (3)

Write t=|z|. This is a positive trace-one matrix precisely when

    0<=t<=(1+3p)/4.                                    (4)

Indeed the six other diagonal eigenvalues are(1−p)/8, while the 000/111 block has eigenvalues(1+3p)/8 plus/minus t/2. In particular z=p gives the usual noisy GHZ state. The phase of z has no effect on the fixed-tester norms below; the two off-diagonal tensor blocks have absolute coefficients t/2.

Using the exact normalizations from turn2, let r_3 and s_3 denote the full complex three-factor projective norms of the realignment and SIC outputs. Qubit SIC existence and unitary equivalence with the canonical Gram tester were explicitly established there.

**Theorem.** Throughout (4),

    r_3(rho_(p,z))=t+(1+p)^(3/2)/(2sqrt(2)),             (5)
    s_3(rho_(p,z))=t/(2sqrt(2))+(3+p)^(3/2)/8.           (6)

## 3. Exact diagonal and off-diagonal blocks

For realignment, write

    e_0=(E_00+E_11)/sqrt(2),
    e_1=(E_00−E_11)/sqrt(2).

The two diagonal pure-projector images are (e_0 plus/minus e_1)/sqrt(2), and R(I/2)=e_0/sqrt(2). Therefore the diagonal tensor of (3) is

    T(A_R,B_R),  A_R=1/(2sqrt(2)),  B_R=p/(2sqrt(2)).

Its norm is (1+p)^(3/2)/(2sqrt(2)) by (1). The two off-diagonal directions E_01,E_10 are orthogonal to this diagonal block and each other, with unit norm. The orthogonal-block lemma of turn2 adds their combined norm t, proving (5).

For SIC, the two diagonal projector images have norm1 and inner product1/2. After a local output unitary they are

    a_+=(sqrt(3)/2)e_0+(1/2)e_1,
    a_-=(sqrt(3)/2)e_0−(1/2)e_1.

Their average, the image of I/2, is(sqrt(3)/2)e_0. Expanding the diagonal tensor gives

    T(A_S,B_S),  A_S=3sqrt(3)/8,  B_S=p sqrt(3)/8.

Here B_S/A_S=p/3<=1, so (1) gives diagonal norm(3+p)^(3/2)/8. Each off-diagonal image has norm1/sqrt(2), still in an orthogonal block. Their combined three-factor norm is t/(2sqrt(2)). This proves (6).

These calculations do not flatten the three-factor tensor. Both diagonal lower bounds use the explicit complex trilinear certificate, and the block lemma combines them with the other directions without loss.

## 4. Exact detection regions and their ordering in this family

Define

    theta_R(p)=1−(1+p)^(3/2)/(2sqrt(2)),
    theta_S(p)=2sqrt(2)(1−(3+p)^(3/2)/8).                (7)

Both are nonnegative on[0,1] and vanish at1. Within the physical region (4), realignment detects exactly when t>theta_R(p), while SIC detects exactly when t>theta_S(p). Thus this is a full detection classification for both fixed testers on the family (3), including the equality boundaries, where the corresponding test does not detect.

Moreover,

    theta_S(p)>theta_R(p) for 0<=p<1.                   (8)

To see this, their difference vanishes atp=1 and has derivative

    (3sqrt(2)/8)(sqrt(1+p)−sqrt(3+p))<0.

It is therefore positive before1. Consequently SIC never detects a state of (3) that realignment misses, while the reverse difference is nonempty. This ordering is a family-specific statement; it coexists with the global multipartite incomparability proved in turn2.

For the one-parameter noisy-GHZ line z=p, the unique realignment detection threshold alpha_R in(0,1) is the root

    alpha_R³−5alpha_R²+19alpha_R−7=0.                   (9)

The unique SIC threshold alpha_S is the root

    alpha_S³+alpha_S²+(27+32sqrt(2))alpha_S−37=0.        (10)

Both follow by squaring the positive sides of (5)=1 or (6)=1. No spurious root is introduced on[0,1]: 1−p>=0 in (9), and 8−2sqrt(2)p>0 in (10). The left sides of the original norm equations are strictly increasing, so the roots are unique.

For a simple strict separation take p=z=1/2. Then

    r_3=1/2+3sqrt(3)/8>1,
    s_3=(7sqrt(14)+4sqrt(2))/32<383/384<1.              (11)

The lower comparison uses27/64>1/4. For the upper comparison use sqrt(14)<15/4 and sqrt(2)<17/12. In particular alpha_R<1/2<alpha_S. These are exact bounds, with no decimal root approximation used as a certificate.

## 5. Relation to earlier turns and remaining questions

At p=1, the family reduces to Schmidt-correlated states and formulas(5)-(6) agree with turn3: r_3=1+t and s_3=1+t/(2sqrt(2)). For z=p, the former one-sided three-qubit bounds in turn2 remain valid but are now sharpened to exact values. The old frozen proof is not rewritten.

The map normalization, GHZ state family, and fixed-tester framework are credited to the primary sources already bound. The explicit binary cubic norm supplies the needed odd-party calculation. We make no priority claim. Finite controls verify the algebraic identities, density eigenvalues, threshold equations and exact radical comparisons. They supplement the complex multilinear proofs.

The positive/negative detection regions in (7) describe these two tests, not separability itself. A state missed by both tests may still be entangled. The fifth turn will examine that remaining gap within the broader mixed-family scope, without extending the five-turn budget.
