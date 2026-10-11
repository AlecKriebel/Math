# Proofs of the retained deductions

These proofs concern a literal formulation counterexample and methodological partial results. They do not claim a solution within the nontrivial-incidence class discussed in the primary papers.

## Proof 1. The four-line configuration and its covering

Let Q be the plane y_0+y_1+y_2+y_3=0 in P^3, and let L_i=Q intersect {y_i=0}. These are four distinct lines with no triple intersection: three zero coordinates on Q force the fourth zero as well.

Any ordered four lines with no triple intersection correspond in the dual plane to four points with every triple linearly independent. Choose representatives v_0,v_1,v_2 as a basis. Write v_3=a_0v_0+a_1v_1+a_2v_2. All a_i are nonzero by the independence condition. A change of basis followed by a diagonal transformation sends these four points to the three coordinate points and (1:1:1). The projective transformation is unique: a diagonal matrix fixing (1:1:1) is scalar. This normalization is algebraic on the open set of such frames. Thus the incidence space is isomorphic to PGL(3,C), not just set-theoretically a single orbit. The configuration is infinitesimally rigid modulo projective transformations.

For any n>=2 let F_n be the degree-n Fermat surface in P^3. Its partial derivatives are n z_i^(n-1), so it is smooth. It is irreducible: if a positive-dimensional projective hypersurface in P^3 decomposed into two positive-degree components, their intersection would be nonempty, and the product defining equation would have zero gradient there. This contradicts smoothness.

The coordinate-power morphism

q_n:F_n -> Q, [z_0:z_1:z_2:z_3] |-> [z_0^n:z_1^n:z_2^n:z_3^n]

is finite and surjective. On the open set with all y_i nonzero its degree is n^4/n=n^3, and its deck group is (mu_n)^4/diagonal(mu_n), isomorphic to (Z/n)^3. The local ramification index at each L_i is n. On y_0!=0 its function field is obtained by adjoining the three nth roots of y_i/y_0, i=1,2,3. This is exactly the maximal exponent-n abelian cover in the setup, rather than a proper quotient. Since F_n is already smooth, its minimal desingularization is F_n itself.

## Proof 2. A genuine nontrivial smooth family for all n>=4

Fix n>=4 and put M=z_0^(n-2)z_1^2 and f_t=sum z_i^n+tM.

### Smoothness on a uniform disk

At a singular point of {f_t=0}, the z_2 and z_3 derivatives force z_2=z_3=0. Neither z_0 nor z_1 can be zero: the derivative of the other pure power would then force both zero. Write r=z_1/z_0. The remaining derivative equations imply

n+(n-2)t r^2=0, and n r^(n-2)+2t=0.

Eliminating t gives r^n=2/(n-2) and hence

|t|^n = n^n / [4(n-2)^(n-2)] > 1.

The last inequality follows from n^n > n^2(n-2)^(n-2) and n^2>4. Consequently every fiber for |t|<1 is smooth. The hypersurface family is a proper holomorphic submersion over that disk: locally a nonzero derivative in a projective-space direction solves the hypersurface equation with t as a free coordinate.

### The Kodaira–Spencer class is nonzero

Write F=F_n. The tangent-normal sequence is

0 -> T_F -> T_(P^3)|F -> O_F(n) -> 0.

The connecting map sends a polynomial perturbation to its abstract Kodaira–Spencer class. Its kernel consists exactly of the image of H^0(T_(P^3)|F).

For a hypersurface of degree n>=2, H^1(O_F)=0 and H^0(O_F(1))=C^4. Indeed use 0->O_(P^3)(k-n)->O_(P^3)(k)->O_F(k)->0 and the vanishing of the intermediate cohomology of line bundles on P^3, for k=0,1. The Euler sequence restricted to F therefore shows that H^0(T_(P^3)|F) is the 15-dimensional space of ambient projective linear vector fields. In particular no extra vector fields along the embedding are being omitted.

Their normal images are the degree-n polynomials sum a_ij z_j (partial f_0/partial z_i), modulo f_0. Thus every polynomial in that image is in the monomial ideal

J=(z_0^(n-1),z_1^(n-1),z_2^(n-1),z_3^(n-1)).

The relation f_0 lies in J by Euler's identity, so passing to O_F(n) does not change this membership test. The exponents of M are (n-2,2,0,0). For n>=4 all are strictly below n-1. Hence M is not in J and its Kodaira–Spencer class is nonzero.

If F were locally rigid, the fibers of this proper smooth family would all be isomorphic near 0. The local triviality theorem for a proper holomorphic family whose compact fibers are all isomorphic (Fischer–Grauert) would force its Kodaira–Spencer map to be zero. Equivalently, one can use the reduced Kuranishi base: a map from a reduced disk to a zero-dimensional germ factors through its reduced point. Either standard formulation contradicts the computed class. Thus F_n is not locally rigid.

This proof uses the explicit family, not the generally invalid implication H^1(T_F)!=0 => nonrigid. Infinitesimal nonrigidity alone would not suffice.

As an exact dimensional control, the degree-n part J_n contains the 16 distinct monomials z_i^(n-1)z_j for n>=3. Therefore the image of embedded first-order deformations in H^1(T_F) has dimension binomial(n+3,3)-16. For n=4 this is 19, not the full unpolarized K3 deformation dimension 20. We do not identify this image dimension with h^1(T_F) in all degrees.

Dependencies: standard projective-space line-bundle cohomology, tangent-normal/Euler sequences, and the Kodaira–Spencer or Fischer–Grauert local-triviality theorem. No unpublished rigidity input is used.

## Proof 3. What branch rigidity actually controls

Let pi:S->Y be a smooth finite Galois abelian cover in characteristic zero, with normal-crossings branch divisor D and locally independent inertia groups. Then

(pi_*T_S)^G = T_Y(-log D).

This can be checked locally. Near one branch component the map is (u,v)->(x=u^e,y=v), up to an étale factor. An invariant vector field has u-component u A(u^e,v) and v-component B(u^e,v). Its image is e x A(x,y) partial_x + B(x,y) partial_y, exactly a vector field tangent to x=0. At a crossing, x=u^e and y=v^f; invariance forces divisibility by u and v respectively, giving x partial_x and y partial_y. Away from D the assertion is ordinary étale descent. These descriptions agree on overlaps.

Finite pushforward is exact on coherent sheaves and has no higher direct images. Taking G-invariants is exact over C, by averaging. Consequently

H^1(S,T_S)^G = H^1(Y,T_Y(-log D)).

Vanishing of the right-hand side therefore controls only the invariant summand. A representation can have zero invariant subspace and still be nonzero. No implication about the remaining eigenspaces follows from this equality alone.

For the quadrangle, fixed-incidence configurations are recovered from their four triple points as the six joining lines. In a neighborhood those points remain a projective frame, and their intersections and joins are algebraic functions. Normalizing the frame trivializes the incidence scheme, including its tangent space. Thus this arrangement supplies a rigid branch control. Proof 5 supplies a nontrivial surface-deformation character at n=3 for the very same arrangement.

## Proof 4. Fixed base and finite character types

Let L be any fixed nonpencil arrangement of d=r+1 distinct lines over C, and Y the blow-up of all points with at least three incident lines. Let D_1,...,D_s be the components of its reduced total branch divisor. Pic(Y) is free of finite rank with basis H,E_1,...,E_m.

Choose integral meridian vectors g_0=-sum_(i=1)^r e_i, g_i=e_i. A strict transform has its line's vector; an exceptional divisor over p has vector g_p=sum_(L_i containing p) g_i. Denote all these fixed integral vectors by v_j.

Every v_j has order n modulo n. To see this for an exceptional vector, choose a line not through p as the omitted generator; then v_j is a sum of a nonempty subset of basis vectors. At a double point two strict-transform vectors are independent modulo n, choosing any other line as omitted generator. At a crossing of an exceptional divisor with the strict transform of L_i, choose a line outside the pencil as omitted generator. A relation a g_i + b sum_(L_k containing p)g_k=0 forces b=0 by the coefficient of some k!=i, then a=0. There are no crossings of different exceptional divisors. Hence the normalized cover of Y is smooth, locally a product of coordinate root maps.

For completeness, this is the minimal desingularization of the original normal plane cover. Above a point of valency v>=3, the local deck subgroup has order n^v. Over the exceptional P^1, the ramification index is n and each local exceptional component maps with degree n^(v-1). The local projection formula gives its self-intersection -n^(v-2), which is at most -2. Thus this resolution has no exceptional (-1)-curve. The local subgroup is generated by the v independent meridians, and quotienting by their sum gives the connected cover of the exceptional P^1 branched at the v tangent directions; this justifies using the full degree n^(v-1) for each local component. Unramified copies elsewhere do not change the self-intersection.

For c=(c_1,...,c_r), 0<=c_i<n, let a_j be the least residue of v_j dot c modulo n. The standard character line bundle L_c in pi_*O_S=sum L_c^(-1) satisfies

n [L_c] = sum_j a_j [D_j].                                           (4.1)

The abelian-cover tangent-eigensheaf formula is

(pi_*T_S)^c = T_Y(-log D_(J_c)) tensor L_c^(-1),
J_c={j:a_j != n-1}, D_J=sum_(j in J)D_j.                             (4.2)

Formula (4.2), with its character convention, is Pardini's formula, reproduced as Lemma 2.8 of [BGBP-2021]. Its dual form is Proposition 5.7 of [BC-rigid]. These are explicit standard dependencies. Reversing all characters just permutes the summands and does not affect total vanishing.

Write d_jq for the coordinates of [D_j]. Since 0<=a_j/n<1, (4.1) gives

|[L_c]_q| <= B_q := sum_j |d_jq|.

Each [L_c]_q is integral. Only finitely many vectors ell=[L_c] are possible, uniformly in n. Torsion-free Pic(Y) identifies each such vector with at most one line bundle, not merely one numerical class. There are at most 2^s sets J. Therefore only finitely many sheaves

F_(ell,J)=T_Y(-log D_J) tensor O_Y(-ell)

can occur in (4.2), despite the growth in the number n^r of characters.

This also pinpoints why “make n large and apply Serre vanishing” is invalid without another argument: L_c is a normalized residue sum in a bounded region of Pic(Y), not a sequence of positive tensor powers tending to infinity.

## Proof 5. Exact quadrangle negative control at n=3

Use the source's labels on the ten (-1)-curves of Y=Bl_(p1,p2,p3,p4)P^2:

E_(i5)=E_i; E_(ij)=H-E_h-E_k if {i,j,h,k}={1,2,3,4}.

The canonical class is K=(-3,1,1,1,1) in the basis H,E_1,...,E_4. For the source basis of (Z/n)^5 use

v_13=e_5, v_14=e_1, v_23=e_4, v_24=e_2, v_34=e_3,
v_12=-(e_1+e_2+e_3+e_4+e_5), v_45=-(e_1+e_2+e_3),
v_15=e_2+e_3+e_4, v_25=e_1+e_3+e_5, v_35=-(e_3+e_4+e_5).

For c=(2,2,2,1,1) modulo 3, the residues in order

12,13,14,15,23,24,25,34,35,45

are

1,1,2,2,1,2,2,2,2,0.

Equation (4.1) gives [L_c]=(3,-1,-1,-1,-1)=-K. The selected divisor is E_12+E_13+E_23+E_45. By Serre duality and (4.2), the corresponding tangent eigenspace has the same dimension as

H^1(Y,Omega^1_Y(log(E_12+E_13+E_23+E_45))).

The residue sequence is

0 -> Omega^1_Y -> Omega^1_Y(log D_J) -> direct_sum_(j in J) O_(D_j) -> 0.

Each D_j is P^1, so H^1(O_(D_j))=0. Since Y is the blow-up of P^2 at four points, H^0(Omega^1_Y)=0 and H^1(Omega^1_Y)=C^5, with divisor classes giving its usual Hodge (1,1) basis. The connecting map C^4->C^5 sends the four residue basis vectors to the four divisor Chern classes (up to a common nonzero normalization). The rows are

(1,0,0,-1,-1), (1,0,-1,0,-1), (1,-1,0,0,-1), (0,0,0,0,1).

They are linearly independent: the E_3,E_2,E_1 coordinates successively force the first three coefficients zero, and then the E_4 coordinate forces the fourth zero. Their rank is four, hence the cokernel is one-dimensional. The long exact sequence proves the displayed H^1 has dimension exactly one. Thus H^1(S_3,T_(S_3)) has a one-dimensional nonzero character summand.

This recovers and sharpens the Euler-characteristic witness used in [BC-rigid], Proposition 8.1, without claiming an exact value for the entire H^1. It proves infinitesimal nonrigidity. For actual nonrigidity of the n=3 surface we credit the separate published quadrangle statement; the present argument alone does not prove that the tangent vector integrates.

## Proof 6. Eventual periodicity of infinitesimal-rigidity failure

Under the fixed-arrangement setup of Proof 4, the set

B={n>=2: H^1(S_n,T_(S_n)) != 0}

is eventually periodic. No assertion about eventual periodicity of *local rigidity* is made.

### Step A: occurrence of one sheaf type is an integer-linear condition

For fixed ell and J from the finite set in Proof 4, write

a_j=v_j dot c - n k_j, 0<=c_i<n, 0<=a_j<n.

The carries k_j range over a fixed finite set because

|k_j| <= 1+sum_i |v_ji|.

Fix one possible tuple k. The conditions that (ell,J) occurs are precisely

sum_j (v_j dot c - n k_j)d_jq = n ell_q for every q;
v_j dot c - n k_j = n-1 for j not in J;
0 <= v_j dot c - n k_j <= n-2 for j in J;
0 <= c_i <= n-1, n>=2.

With k,ell,J fixed, every coefficient is constant; in particular there is no product of two variables. These are affine integer-linear equations and inequalities in n,c. Add nonnegative slack variables and write n=2+u to turn them into A x=b with x a vector of nonnegative integers. Projecting the solution set to n gives the exponents realizing this carry tuple and type. Taking a finite union over k gives the full occurrence set.

### Step B: projected affine integer solution sets are semilinear

Here is an elementary proof, so no quantifier-elimination black box is required. For S_b={x in N^t:Ax=b}, let M_b be the componentwise-minimal elements. Dickson's lemma says M_b is finite. Every x in S_b dominates some m in M_b, and x-m lies in the nonnegative homogeneous solution monoid H={h:Ah=0}.

The nonzero componentwise-minimal elements P of H are also finite. They generate H: if h!=0, choose p in P with p<=h, subtract p, and induct on the sum of coordinates. Thus

S_b = union_(m in M_b) (m+sum_(p in P) N p).

This is a finite union of linear sets. Coordinate projection preserves this form. Dickson's lemma itself follows by induction on the number of coordinates: every infinite sequence of nonnegative integer vectors has an infinite subsequence with first coordinates nondecreasing (use an infinitely repeated value or successively larger values), and induction applied to the remaining coordinates supplies a comparable pair. An infinite antichain of minimal elements is therefore impossible.

### Step C: a semilinear subset of N is eventually periodic

A linear subset of N has the form a+sum_i N p_i. If all p_i=0 it is a singleton. Otherwise pick a positive p among the generators. The residues of the generated monoid modulo p form an additive subgroup of the finite cyclic group: closure under addition in a finite group provides inverses by repeated addition. For each attained residue choose one monoid element q_r in that residue. Every q_r+t p, t>=0, also lies in the monoid. Above max_r q_r, membership is therefore determined entirely by the residue modulo p. A finite union of such sets and singletons is eventually periodic, with a common period taken as a least common multiple of the positive component periods.

### Step D: pass from occurrence to cohomology vanishing

Finite pushforward and the character splitting give

H^1(S_n,T_(S_n)) = direct_sum_c H^1(Y,F_([L_c],J_c)).

For each of the finitely many types (ell,J), the dimension of H^1(Y,F_(ell,J)) is a fixed nonnegative integer independent of n. Select the types with positive dimension. Their occurrence sets are eventually periodic by Steps A–C, and their finite union is exactly B. This proves the claim.

The proof gives a reduction: once the finitely many fixed-sheaf cohomologies are known, occurrence is a problem in integer linear algebra. It does not supply those cohomology values, an effective complexity bound, or a universal vanishing theorem. In particular a nonempty periodic tail remains possible. A rigid but not infinitesimally rigid configuration may also obstruct using infinitesimal rigidity as a substitute for the original local-rigidity question.

Classical context: Steps B–C are special cases of semilinear-set theory; see Ginsburg–Spanier [GS-1966]. No originality claim is made.

## The unproved bridge in the fifth approach

A complete argument through the known equisingular theorem would need to establish, for every sufficiently large exponent and every sufficiently small abstract deformation of S_n, persistence of the exceptional curves with the required incidence data, and a compatible contraction producing an equisingular deformation of X_n. Neither the vanishing of the invariant summand nor the existence of fibrations proves this persistence. No such bridge is established here. This is the stopping point for the intended conjecture.
