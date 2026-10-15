# Turn 3: exact persistence criterion and the finite cohomology behind the obstruction

This turn replaces raw approximant ranks by an exact stable-image criterion, gives a finite cochain formula for testing it, and reconstructs the rational cohomology of the Thue–Morse factor through a fully specified collared substitution. The Turn2 example has Betti numbers(1,4,4) in the limit despite its unbounded approximant ranks. The arbitrary source question remains unresolved.

## 1. An exact direct-limit criterion

Let V_1→V_2→... be finite-dimensional rational vector spaces, and write A_(j,i) for the composite map from V_i to V_j, including the identity when i=j. Then

    dim direct_limit V_i =sup_i inf_(j>=i) rank A_(j,i).   (1.1)

For fixed i, the kernels of A_(j,i) increase and hence stabilize after finitely many steps, because V_i is finite-dimensional. Their union is exactly the kernel of the canonical map from V_i to the direct limit: a representative is zero there precisely when some later image is zero. Thus the dimension of its image in the limit is the infimum in(1.1). These canonical images form an increasing family whose union is the limit, proving the formula, including the value infinity.

Consequently finite rank at most M is equivalent to

    for every i there exists j>=i with rank A_(j,i)<=M.   (1.2)

The later index may depend on i. There is no uniform bound on the delay, and observing a small rank for finitely many source stages does not verify(1.2). A two-scale uniform image bound would suffice if independently proved, but no such general bound follows here from O(n^d) complexity.

## 2. A computable cochain image formula

For a cellular map from a fine approximant K_j to K_i, let F^k be the induced cochain pullback. Choose a matrix Z_i whose columns form a basis of degree-k cocycles in K_i, and a matrix B_j whose columns span the degree-k coboundaries in K_j. Then

    rank(H^k(K_i;Q)→H^k(K_j;Q))
      =rank([B_j | F^k Z_i])−rank(B_j).                   (2.1)

Indeed, the image in cohomology is(B_j+F^k Z^k_i)/B_j. Cochain compatibility ensures that cocycles map to cocycles and source coboundaries map into B_j. This proves(2.1) without requiring an explicit choice of quotient basis or an injective bonding map.

For the rectangular complexes of Turn2, the chain maps are just central-cropping matrices, with one1 in each fine-cell column. The checker verifies their chain identities before using(2.1). The computations are exact over Q, rather than ranks modulo a prime or floating-point rank estimates.

## 3. A small stationary model for Thue–Morse

The rational cohomology result reconstructed here is classical Anderson–Putnam territory and is already consistent with the integral group quoted by the original source. No novelty or new integral classification is claimed. A direct specialized model makes the survival calculation explicit.

Use vertices00,01,10,11 and edges, in this order,

    001,010,011,100,101,110.

An edge abc represents the central tile b with one neighboring tile on each side, and joins ab to bc. The allowed four-letter words show that every gluing with a shared pair is a legal collared adjacency. There are ten such gluings, exactly the ten legal four-letter words, so this graph is the collared tile complex, rather than an identification of incompatible collars.

Substitution mu(0)=01, mu(1)=10 sends vertex ab to(1−a)b and sends the edge abc to the two-edge path

    (1−a)b(1−b), followed by b(1−b)c.                    (3.1)

The common middle vertex is b(1−b), and both endpoints agree with the vertex rule. Each edge is mapped linearly across its two image edges, with expansion factor2.

Why does its inverse limit model the hull? Every Thue–Morse tiling has a unique partition into substituted pairs: any00 or11 determines the parity, and length5 alternating words are forbidden, as proved in Turn2. Existence and consistency of the partition follow by taking limits of shifted substituted words; uniqueness follows from the double letter. Desubstitution stays in the same language because every finite aligned preimage occurs in a lower substitution iterate. Iteration gives a unique hierarchy at every level.

A collared supertile at level n specifies its central substituted block and both adjacent blocks. After expansion, it determines a neighborhood of radius at least2^n about any point in the central block. At a graph vertex the adjacent pair determines the same size neighborhood on either side of the boundary. Therefore a compatible inverse-limit point gives nested legal neighborhoods of unbounded radius and hence exactly one tiling; every tiling supplies such a point by its unique hierarchy. The local maps are continuous and respect the vertex identifications. Compactness then proves the inverse-limit homeomorphism. This is a specialized proof of the usual collaring construction, with the needed recognizability and border information stated explicitly.

## 4. The surviving two-dimensional rational space

Let e_1,...,e_6 denote the six oriented edges in the order above. A cycle basis is

    c_1=e_1+e_2+e_4,
    c_2=e_2+e_5,
    c_3=−e_2+e_3+e_6.

The graph is connected, so these three independent cycles form a basis of H_1. Under(3.1), its homology matrix in that basis is

    J = [[1,1,0],
         [1,0,1],
         [1,1,0]].                                      (4.1)

The checker verifies the full edge and vertex chain maps and the identity M C=C J, where C contains these cycle columns. Direct calculation gives

    characteristic polynomial(J)=lambda(lambda−2)(lambda+1),
    rank(J)=rank(J²)=2,
    ker(J)=span{(−1,1,1)}.

The induced cohomology map is J transpose in the dual basis. Its stable image has dimension2 and the restriction is invertible over Q, with nonzero eigenvalues2 and−1. Hence its direct limit has dimension2. We obtain

    H^0(Omega_TM;Q)=Q, H^1(Omega_TM;Q)=Q²,
    H^k(Omega_TM;Q)=0 for k>=2.                           (4.2)

This argument is deliberately over Q; an eigenvalue2 cannot be inverted over Z without changing the module, so the integral finite-generation question is not answered by the rank calculation.

The Sturmian factor from Turn1 also has rank polynomial1+2t. The shearing and recoding homeomorphisms of Turn2 therefore give the exact rank polynomial

    1+4t+4t²                                             (4.3)

for its two-dimensional hull. Its total rational rank is9.

## 5. What the persistence computations show

For the sheared rectangular complexes, the exact finite maps include:

    K_1→K_3 on cohomology: image ranks4 in degree1 and4 in degree2,
    K_2→K_4 on cohomology: image ranks4 in degree1 and6 in degree2,
    K_2→K_6 on cohomology: image ranks4 in both degrees.

Here the arrow means the pullback associated with forgetting from the larger-pattern complex to the smaller one. The degree2 rank6 in the second line exceeds the limiting rank4, and the third line certifies that two dimensions of this image have died by scale6. Formula(1.1), together with(4.3), proves that for every fixed initial scale the later image ranks eventually become at most4 in both degrees. It supplies no universal time for that stabilization. Further finite computations are controls only, not a substitute for this quantifier.

## 6. Remaining target

A route to the original problem is now precise: deduce finite uniform bounds as in(1.2), degree by degree, from low translational complexity for arbitrary repetitive aperiodic tilings, or construct persistent independent classes contradicting such bounds. The current source-compatible example shows why the raw rank at a stage is the wrong quantity. The stationary collared model solves its special survival calculation, but no comparable bounded model or image bound is established for every low-complexity tiling.
