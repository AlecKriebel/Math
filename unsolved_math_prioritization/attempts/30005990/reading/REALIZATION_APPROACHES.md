# Four attempts to realize the sharp cone in the global spectral problem

Together with the dimensional-lift theorem in PROOF.md, these are the five substantive author approaches. The aim of the four approaches below is the remaining assertion: a frequency-5/2 point belonging to a globally minimizing sum-of-first-Dirichlet-eigenvalues partition of a bounded domain satisfying the source regularity assumptions. None of the constructions below is claimed to establish that assertion.

Throughout, the variational sum energy on an open bounded domain G is

    E_N(G) = inf sum_i integral_G |grad f_i|^2,

where each f_i is nonnegative, belongs to H^1_0(G), has L^2 norm one, and f_i f_j=0 almost everywhere for i!=j. This is the normalized segregated formulation of the spectral sum problem. For the bounded Lipschitz domains below, the direct method gives a minimizer: a bounded-energy sequence has weak H^1 and strong L^2 convergence, preserving the normalization and segregation, and energy is weakly lower semicontinuous. The value is finite by using disjoint interior balls.

## Approach 2. Cartesian-product realization and the tensorization obstruction

### 2.1 Exact restricted result

Let Omega be a bounded connected Lipschitz domain in R^m, m>=1, let N>=2, and let I_L=(0,L). Restrict partitions of Omega x I_L to Cartesian cells A_i x I_L, where (A_i) is an admissible N-partition of Omega. Separation of the Dirichlet Laplacian gives

    lambda_1(A_i x I_L) = lambda_1(A_i) + pi^2/L^2.

For the equivalent functional statement, write f_i(x,s)=g_i(x)a_i(s), with the g_i nonnegative, normalized and mutually segregated in Omega, and a_i nonnegative normalized elements of H^1_0(I_L). Then

    integral |grad f_i|^2
      = integral_Omega |grad g_i|^2 + integral_I |a_i'|^2.

Minimizing the latter term gives a_i(s)=sqrt(2/L)sin(pi s/L), and minimizing over the g_i gives the exact restricted infimum

    E_N(Omega) + N pi^2/L^2.                              (2.1)

Thus if a planar spectral optimizer with a 3/2 triple point could be safely tensorized with an interval, its product eigenfunctions would have 5/2 order where that triple spine meets an end face. But (2.1) is a restricted minimization and does not license that tensorization globally.

### 2.2 A genuine obstruction to unrestricted tensorization

The N functions in the definition of E_N(Omega) are L^2-orthonormal. The Rayleigh-Ritz/Ky Fan variational inequality therefore gives

    E_N(Omega) >= sum_(k=1)^N lambda_k(Omega) > N lambda_1(Omega).                 (2.2)

The strict inequality uses connectedness of Omega, hence simplicity of the first Dirichlet eigenvalue and lambda_2>lambda_1. Denote the positive difference E_N(Omega)-N lambda_1(Omega) by Delta.

Now partition the product domain into N transverse slabs

    Omega x ((i-1)L/N,iL/N),  i=1,...,N.

Their total energy is

    N lambda_1(Omega) + N^3 pi^2/L^2.                    (2.3)

For

    L^2 > N(N^2-1) pi^2 / Delta,                         (2.4)

(2.3) is strictly less than (2.1). Consequently the Cartesian product of a minimizing N-partition of Omega with I_L is not a globally minimizing spectral sum partition for all sufficiently large L. This disproves the unqualified tensorization step that would otherwise have supplied attainment.

The same example identifies the failure of a tempting slice inequality. At a height in one of these slabs only one phase is active, and its tangential Rayleigh quotient is lambda_1(Omega). A putative estimate

    sum_i integral_Omega |grad_x f_i(x,s)|^2
       >= (E_N(Omega)/N) sum_i integral_Omega |f_i(x,s)|^2

is false, since E_N(Omega)/N>lambda_1(Omega). The original L^2 normalization is global for each phase, not a separate equal-mass constraint on every slice.

### 2.3 Outcome and remaining gap

This route yields an exact restricted minimization theorem and an explicit family showing why it cannot be promoted to global optimality. A sufficiently thin product might still be useful, but no finite-thickness tensorization theorem is proved here. The thin limit is treated separately in Approach 4. Products also have boundary edges; the original smooth-domain hypotheses cannot be silently imported at those edges.

## Approach 3. Angular optimization and the sum-versus-max obstruction

### 3.1 A spectral shift between a hemisphere and a higher-dimensional sphere

Let S_+^(d-1) be the unit hemisphere in coordinates (x,t), x in R^(d-1), t>0. Given an open nonempty subset omega of that hemisphere, define its rotational lift

    omega_tilde = {(x,y) in S^(d+1) : y!=0 and (x,|y|) in omega}.

The omitted axis A={y=0} has codimension three in S^(d+1); omitting it does not affect H^1 by the cutoff argument used in PROOF.md. Define, initially for smooth compactly supported phi in omega,

    T phi(x,y)=phi(x,|y|)/|y|.

Then the following exact identities hold:

    integral_(omega_tilde) |T phi|^2 = 4 pi integral_omega phi^2,

    integral_(omega_tilde) |grad_S(T phi)|^2
       = 4 pi [integral_omega |grad_S phi|^2
                         - (d-1) integral_omega phi^2].                         (3.1)

To prove them, first note that orbit integration on S^(d+1) is 4 pi t^2 times integration on S_+^(d-1) for functions depending only on (x,t). This follows by the parametrization y=sqrt(1-|x|^2) omega': the hemisphere area element is dx/t, whereas the lifted sphere element is t dx d omega'. The induced metric on rotationally invariant functions is the hemisphere metric. The positive function h=t satisfies -Delta_S h=(d-1)h on the hemisphere. Integrating by parts in

    |grad_S(phi)|^2 = h^2 |grad_S(phi/h)|^2
                       + grad_S h dot grad_S(phi^2/h)

proves the second identity in (3.1). Compact support makes every boundary term zero. Density then extends T to H^1_0(omega).

This gives an isomorphism, up to the factor sqrt(4 pi), between H^1_0(omega) and the SO(3)-invariant subspace of H^1_0(omega_tilde), with the quadratic-form shift in (3.1). For the inverse density assertion, approximate an invariant lifted function by smooth compactly supported functions on omega_tilde and average these approximations over SO(3). Group averaging is bounded in H^1, preserves the open lifted domain, and preserves compactness of support because SO(3) is compact. The resulting invariant smooth functions descend, after multiplication by t, to smooth compactly supported functions on omega. This proves the claimed onto statement without an unproved boundary regularity assumption on omega.

The bottom Dirichlet eigenvalue of omega_tilde can be computed within the invariant subspace. Indeed choose a nonnegative first eigenfunction, average it over SO(3), and use rotational invariance of the domain and Laplacian. The average remains an eigenfunction at the same eigenvalue and is not zero, since its integral is positive. Existence follows from compactness of the Sobolev embedding on the sphere. Therefore

    lambda_1(omega_tilde) = lambda_1(omega) - (d-1).       (3.2)

This assertion also covers nonregular open cells, with H^1_0 understood by completion. An axis of zero capacity is not an extra Dirichlet barrier.

### 3.2 Sharp three-cell min-max theorem on the hemisphere

The credited full-sphere theorem [OV-triple, Corollary 3.6] gives the minimal possible maximum of the first eigenvalues of three disjoint cells in S^(n-1) as

    (3/2)(3/2+n-2),

attained by the planar Y partition extended in the other coordinates. If needed, disconnected cells can be replaced by connected components supporting a first eigenfunction, so the same lower bound applies to the unrestricted open-cell infimum.

Lift any three disjoint hemispherical cells to S^(d+1), so n=d+2. By (3.2),

    max_i lambda_1(omega_i)
       >= (3/2)(3/2+d) + (d-1)
       = (5/2)(5/2+d-2).                                (3.3)

The three hemispherical sectors determined by U=tY attain equality: their positive angular functions U|_(S_+^(d-1)) are eigenfunctions with the displayed eigenvalue. Positivity identifies each as its cell's ground state. Thus (3.3) is the exact three-cell min-max value for d>=3.

This is a complete angular min-max result, but the source problem optimizes a sum. From a bound on max_i lambda_i one cannot infer a lower bound of three times that value for sum_i lambda_i. No such inference is used here.

### 3.3 Conditional sum route

Equation (3.2) also gives

    sum_i lambda_1(omega_i)
       = sum_i lambda_1(omega_i_tilde) + 3(d-1).          (3.4)

If the three-sector Y partition minimizes the sum on the full sphere S^(d+1), then (3.4) proves that tY's three cells minimize the sum on the hemisphere. The relevant full-sphere sum assertion is the p=1 Bishop-type partition conjecture discussed separately from the proven p=infinity theorem in [OV-triple, Section 1.2]. It is not an imported theorem here.

Even proving the hemispherical sum claim would concern a spherical angular functional. It would not, on its own, prove that the corresponding conical cells globally minimize the Euclidean bounded-domain spectral sum, whose competitors need not be conical. Those are two separate missing steps in this route.

## Approach 4. A thin-cylinder Gamma-limit for the original spectral sum

### 4.1 Statement

Let Omega be any bounded Lipschitz domain in R^m, and let N>=1 be fixed. Put D_epsilon=Omega x (0,epsilon). Then

    lim_(epsilon->0) [E_N(D_epsilon)-N pi^2/epsilon^2]
        = E_N(Omega).                                   (4.1)

After rescaling the thin coordinate to (0,1), every sequence of minimizing normalized segregated eigenfunctions has a subsequence converging strongly in L^2 to f_i(x)e(s), where e(s)=sqrt(2)sin(pi s) and (f_i) minimizes E_N(Omega). The proof below establishes the corresponding liminf and recovery statements, not only an upper bound.

### 4.2 Rescaling and recovery

For normalized u_i on D_epsilon define

    w_i(x,s)=sqrt(epsilon) u_i(x,epsilon s),   0<s<1.

Each w_i has L^2 norm one, and the rescaled functional after the transverse subtraction is

    F_epsilon(w)=sum_i integral |grad_x w_i|^2
       + epsilon^(-2) sum_i [integral |partial_s w_i|^2-pi^2].                    (4.2)

The one-dimensional Poincare inequality shows each bracket is nonnegative. For every admissible normalized segregated (f_i) on Omega, the maps w_i=f_i e are admissible and give

    F_epsilon(f e)=sum_i integral_Omega |grad f_i|^2.      (4.3)

This proves the recovery/limsup inequality, including the upper bound in (4.1).

### 4.3 Compactness and liminf

Suppose epsilon tends to zero and F_epsilon(w_epsilon)<=C. Expand in the first transverse mode by setting

    f_i,epsilon(x)=integral_0^1 w_i,epsilon(x,s)e(s) ds,
    q_i,epsilon=w_i,epsilon-f_i,epsilon e.

For almost every x the remainder q_i,epsilon is L^2(0,1)-orthogonal to e. The second Dirichlet eigenvalue of (0,1) is 4 pi^2, so

    integral |partial_s w_i,epsilon|^2-pi^2 integral |w_i,epsilon|^2
      = integral |partial_s q_i,epsilon|^2-pi^2 integral |q_i,epsilon|^2
      >= 3 pi^2 ||q_i,epsilon||_2^2.                    (4.4)

Thus sum_i ||q_i,epsilon||_2^2 <= C epsilon^2/(3 pi^2). Also f_i,epsilon>=0, belongs to H^1_0(Omega), and

    ||f_i,epsilon||_2^2=1-||q_i,epsilon||_2^2,
    integral |grad f_i,epsilon|^2 <= integral |grad_x w_i,epsilon|^2.              (4.5)

Consequently the f_i,epsilon are uniformly H^1-bounded. Passing to a subsequence, they converge weakly in H^1 and strongly in L^2 to f_i, with f_i>=0 and ||f_i||_2=1. Equation (4.4) gives w_i,epsilon -> f_i e strongly in L^2 on Omega x (0,1).

The original components have disjoint support, so w_i,epsilon w_j,epsilon=0. Strong L^2 convergence of both factors implies L^1 convergence of their product, giving f_i(x)f_j(x)e(s)^2=0 almost everywhere. Since e>0 on (0,1), f_i f_j=0 almost everywhere in Omega. The limiting tuple is therefore admissible for E_N(Omega), even though the projected tuples f_i,epsilon need not be segregated before taking the limit.

Dropping the nonnegative transverse excess in (4.2) and using (4.5) plus weak lower semicontinuity proves

    liminf F_epsilon(w_epsilon)
       >= sum_i integral_Omega |grad f_i|^2 >= E_N(Omega).                       (4.6)

Together with (4.3), this proves (4.1) and the stated compactness for minimizing sequences. More formally, on the fixed L^2 space of tuples on Omega x (0,1), the extended functionals F_epsilon, equal to infinity outside the normalized segregated H^1_0 class, Gamma-converge to the functional which is sum_i integral|grad f_i|^2 on w_i=f_i e with admissible f, and infinity otherwise. The preceding compactness, liminf, and recovery arguments prove all parts of this assertion.

### 4.4 Why this does not finish realization

The theorem gives an asymptotic link between actual global spectral minimizers, rather than only stationary candidates. It does not identify a planar minimizing tuple as Y, force a boundary triple point for every small positive epsilon, or control its exact frequency. Strong L^2 (even ordinary energy compactness) alone is insufficient for a boundary-stratum persistence argument. Uniform boundary regularity on the degenerating domains and a topology/frequency persistence theorem would be needed. The cylinder has edges; replacing it by a globally smooth domain is an additional step, not an invariance of (4.1) that has been proved here.

## Approach 5. Explicit separated spectral stationary profiles

### 5.1 An actual eigenfunction construction with the desired local asymptotic

Fix d>=3, set gamma=5/2, and let C_i be the three half-space sectors of U=tY from PROOF.md. In the Euclidean half-ball D=B_R intersect {t>0}, take cells

    Omega_i=C_i intersect B_R,   i=1,2,3.

Let phi_i be the restriction of U_i to the unit hemisphere. It is positive inside its angular cell, vanishes on its boundary, and satisfies

    -Delta_S phi_i=gamma(gamma+d-2)phi_i.

Write nu=gamma+(d-2)/2=(d+3)/2, and let j_(nu,1) denote the first positive zero of the Bessel function J_nu. Define on Omega_i

    u_i(r,theta)=a r^(-(d-2)/2) J_nu(j_(nu,1) r/R) phi_i(theta),                  (5.1)

with zero extension outside the cell and with the same positive normalizing factor a for all three components. Rotational congruence makes their L^2 norms equal, so choose a to make each norm one.

The Bessel equation and the angular equation give

    -Delta u_i=(j_(nu,1)/R)^2 u_i.

The radial factor is positive for 0<r<R and vanishes at r=R. Positivity and the Dirichlet boundary condition identify u_i as the first eigenfunction of Omega_i. For example, if a smaller eigenvalue existed, its nonnegative ground state would be L^2-orthogonal to this positive eigenfunction, which is impossible. Thus all three cell eigenvalues equal (j_(nu,1)/R)^2.

The standard convergent power series for J_nu near zero gives

    r^(-(d-2)/2)J_nu(j_(nu,1)r/R)
        = c_0 r^gamma (1+O(r^2)),   c_0>0.

Therefore the vector of normalized eigenfunctions has the asymptotic

    u(x,t)=c_1 tY(x_1,x_2)+O(|(x,t)|^(9/2)),             (5.2)

with the corresponding first-derivative remainder of order 7/2 almost everywhere, and classically within each open cell. Across a pairwise interface the zero-extended components need not be classically differentiable. Its boundary frequency at the flat center is 5/2. This is an actual spectral eigenfunction partition, not merely a formal harmonic cone.

### 5.2 Pairwise first variation vanishes

On each smooth pairwise interface away from the spine and external boundary, the magnitudes of the normal derivatives of the two adjacent angular profiles phi_i and phi_j are equal. They are multiplied in (5.1) by the same radial factor and normalization. Hence

    |partial_(nu_i) u_i|^2=|partial_(nu_j) u_j|^2         (5.3)

there. The Hadamard formula for a simple Dirichlet eigenvalue under smooth interface perturbations supported in such a patch is

    delta lambda_1(Omega_i)
        = -integral_interface |partial_(nu_i)u_i|^2 X dot nu_i.

The adjacent outward normals are opposite, so (5.3) cancels the two contributions to the spectral sum. Thus this construction passes all pairwise first-order shape variations supported away from the junction and outer boundary. This statement does not assert a full second variation theorem at the nonsmooth spine.

### 5.3 The remaining obstruction

Neither exact eigenfunctions nor pairwise flux balance implies global minimality of the spectral sum. The candidate could lose to a nonconical, topology-changing partition. Its conical/angular symmetry is an imposed ansatz, and Approach 3 establishes a min-max angular theorem rather than the necessary sum theorem. In addition, the half-ball's rim is not globally C^1, although the flat center where (5.2) is computed is smooth. Smoothing the rim destroys the exact separated eigenfunctions and requires a stability argument.

Accordingly, this approach produces a concrete spectral stationary candidate with the desired boundary behavior, but it does not produce the global optimizer required to close the original attainment claim.

## Final remaining obligation

To settle the source target in its strict spectral reading, one must prove the existence of a bounded domain satisfying the source boundary hypotheses and a globally sum-minimizing partition with a boundary free-interface point of frequency 5/2. One possible route is a robust realization/persistence theorem for the sharp tY cone. Another would certify a concrete spectral partition globally and preserve the relevant flat-boundary singularity under any required boundary smoothing.

The universal lower bound, the equality classification for all admissible blow-ups, and exact cone-class sharpness have a candidate proof in PROOF.md. The five approaches above do not resolve the remaining global-realization assertion, and no sixth author approach is claimed.

## Public references for imported inputs

- R. Ognibene and B. Velichkov, *Structure of the free interfaces near triple junction singularities in harmonic maps and optimal partition problems*, arXiv:2412.00781v5, Sections 1.2 and 2, Proposition 3.5 and Corollary 3.6. https://arxiv.org/abs/2412.00781v5
- R. Ognibene and B. Velichkov, *Boundary regularity of the free interface in spectral optimal partition problems*, arXiv:2404.05698v1. https://arxiv.org/abs/2404.05698v1
- NIST Digital Library of Mathematical Functions, Sections 10.2 and 10.21, for the Bessel equation, its power series and positive zeros. https://dlmf.nist.gov/10.2 ; https://dlmf.nist.gov/10.21

Rayleigh-Ritz/Ky Fan, the one-dimensional Dirichlet spectrum, Sobolev compactness, and the localized Hadamard formula are standard analytic inputs. The new derivations in this file do not establish historical novelty of any of these reductions.
