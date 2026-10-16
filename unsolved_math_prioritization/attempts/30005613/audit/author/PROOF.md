# A finite-rank construction of pure point Dirichlet spectrum

Problem 30005613 / OWR-14297736-021. Author candidate, 5 October 2026.
This is a complete argument submitted for independent checking, not a claim of
human peer review or historical novelty.

## 1. Precise assertion and scope

For every integer d >= 2 there is a connected open set O in R^d, formed by a
tower of expanding cubes joined through positive, shrinking windows, whose
Dirichlet Laplacian A has pure point spectral type and

    spectrum(A) = [0,infinity),
    closure(point_spectrum(A)) = [0,infinity),
    H_ac(A) = H_sc(A) = {0}.

Here A is the nonnegative self-adjoint operator associated with
q[u] = integral_O |gradient u|^2 on H_0^1(O). Pure point means that eigenvectors
span L^2(O); it does not mean that every point of [0,infinity) is an eigenvalue.
In fact 0 is not an eigenvalue. The spectrum is entirely essential, and dense
positive eigenvalues are embedded in it.

Both cube widths and window widths are chosen in the construction. Cube widths
are free inductive parameters in Section 3 of Krejcirik--Lotoreichik [KL]. We
do not assert the result for every arbitrarily preassigned sequence of cubes.
There is no Neumann claim, no bounded-domain claim, and no smooth or globally
Lipschitz boundary claim. The domain has the same zero-thickness interface
screens and open windows as the construction in [KL].

The mechanism is convergence of increasing finite-dimensional reducing spaces.
No inference from trace-class perturbations to absence of singular-continuous
spectrum is used.

## 2. Finite-window facts and the source dependency

Write Q_a(x) for the axis-parallel open cube of half-width a centered at
x e_1. Set a_1 = x_1 = 1. Once a_1,...,a_n and x_1,...,x_n have been fixed, a
new half-width a > a_n + 1 places the next center at x = x_n + a_n + a.
The cubes have disjoint interiors and successive closures meet along a face.

Let O_n be the connected first n cubes with the first n-1 windows already
opened. Put p_n = (x_n+a_n)e_1 and

    D_0 = O_n union Q_a(x),
    D_delta = D_0 union Q_delta(p_n),   0 < delta < a_n.

The added cube Q_delta(p_n), apart from its middle face, is already in D_0.
Thus D_delta and D_0 agree up to a Lebesgue-null set and have the same L^2
space, although their H_0^1 spaces differ. On this common space,

    (A_D_delta + 1)^(-1) -> (A_D_0 + 1)^(-1) in operator norm
    as delta decreases to zero.                                      (2.1)

This is exactly the finite-window convergence proved and used in [KL,
Section 3, first interconnection], from its Propositions 2.2 and 2.3. Its
hypotheses hold here: all the sets lie in a fixed bounded set; their only
persistent added boundary point is p_n; a point has H^1 capacity zero in
d >= 2. Previously opened windows stay fixed. No regularity of the slit
boundary beyond that argument is being assumed. The finite-window
norm-resolvent fact is the external analytic input to this proof.

Every bounded open set has compact Dirichlet resolvent: extend H_0^1 functions
by zero into a larger bounded box and use the compact H_0^1-to-L^2 embedding
there. This applies to O_n, D_0, and D_delta. Their eigenvalues are strictly
positive, by the Poincare inequality in a containing bounded box.

Consequently, if S is a finite collection of distinct eigenvalues of A_O_n
and none belongs to the spectrum of A_Q_a(x), then each lambda in S is an
isolated finite-multiplicity eigenvalue of A_D_0, with eigenspace precisely
its old eigenspace extended by zero. Choose pairwise disjoint intervals
I_lambda about these values, with endpoints in the resolvent set of A_D_0,
containing no other eigenvalues of A_D_0. Norm-resolvent convergence gives

    E_D_delta(I_lambda) -> E_O_n({lambda}) direct_sum 0
    in operator norm.                                               (2.2)

For completeness, (2.2) follows by passing to the bounded resolvents in (2.1):
the corresponding nonzero eigenvalues (lambda+1)^(-1) are isolated; the
resolvent identity gives uniform convergence of their resolvents along
fixed small contours; the contour integrals give norm convergence of the
Riesz projections. Projections less than distance 1 apart have equal rank,
because either projection is injective on the other's range. Thus the
ranks in (2.2) also stabilize. Multiplicity inside an interval is permitted.

## 3. Nonresonant next cubes

The eigenvalues of the Dirichlet cube of half-width a are

    pi^2 (m_1^2 + ... + m_d^2) / (4 a^2),   m_i in {1,2,...}.

For any finite positive set S and any nonempty bounded open interval of
positive candidate a's, only finitely many a's in that interval can make a
cube eigenvalue equal to a member of S. Indeed an equality with lambda in S
forces m_1^2+...+m_d^2 = 4 a^2 lambda/pi^2, which bounds every m_i uniformly
on the interval. Each allowed multi-index and lambda excludes at most one a.

We may therefore choose a_{n+1} in (a_n+1,a_n+2) to avoid any finite
protected spectral set of A_O_n. The cube multiplicities do not matter.
This choice is made before choosing the next aperture. It does not alter
any previous cube, aperture, or protected subspace.

## 4. Induction with finitely many protected projections

Set epsilon_n = 2^(-n-2) and eta_n = 2^(-n), for n >= 1. Each new cube
omega_j is equipped, when it is chosen, with a fixed countable orthonormal
Dirichlet sine basis (f_{j,l})_{l>=1} of L^2(omega_j). These vectors will
always be extended by zero. At stage n the finite test set is

    F_n = { f_{j,l} : 1 <= j <= n, 1 <= l <= n }.

We construct O_n and finite-rank orthogonal projections P_n^k, 1 <= k <= n,
with the following properties:

(a) Each P_n^k is a sum of complete eigenspace projections of A_O_n.

(b) Their ranges are nested: P_n^1 <= ... <= P_n^n.

(c) For 1 <= k <= n, the zero extensions into L^2(O_{n+1}) satisfy

    ||P_{n+1}^k - P_n^k|| < epsilon_n,
    rank(P_{n+1}^k) = rank(P_n^k).                                  (4.1)

(d) At birth, the largest projection approximates every current test:

    ||(I-P_n^n) f|| < eta_n    for every f in F_n.                    (4.2)

Base step. Take O_1 = omega_1. Since its eigenvectors are complete, a
sufficiently large finite spectral cutoff P_1^1 satisfies (4.2).

Inductive step. Let S_n be the finite set of all eigenvalues whose complete
eigenspaces occur in P_n^n. Choose a_{n+1} by Section 3 so its cube spectrum
avoids S_n. For every lambda in S_n take an isolating interval I_lambda as
in Section 2. Write S_n^k for the subset defining P_n^k. For small delta,
define

    P_delta^k = sum_{lambda in S_n^k} E_D_delta(I_lambda),  k <= n.

These are nested full spectral projections. Because there are finitely
many k, (2.2) allows one common positive delta_n, also satisfying

    delta_n < min(a_n/2, 2^(-n)),

for which all n bounds (4.1) hold. Put O_{n+1}=D_delta_n and
P_{n+1}^k=P_delta_n^k for k<=n. The ranks agree because epsilon_n<1.

Finally choose L_{n+1} above every eigenvalue in the previously protected
projections, and outside the spectrum of A_O_{n+1}, large enough that

    P_{n+1}^{n+1} = E_O_{n+1}([0,L_{n+1}])

satisfies (4.2) for the finite set F_{n+1}. Such an L_{n+1} exists by the
compact-resolvent spectral theorem. This extends the nesting in (b).
Future steps need not keep this projection a low-energy cutoff: they
transport its selected finite collection of eigenspaces instead.

This completes a countable induction in which every individual step has
only finitely many constraints. No uniform lower bound on spectral gaps,
no simple-spectrum assumption, and no choice of a basis inside a splitting
multiple eigenvalue is required.

## 5. The limiting domain and resolvent

Let O = union_{n>=1} O_n. It is open and connected. It contains omega_n,
whose inscribed ball has radius a_n -> infinity, hence O is quasi-conical.
Apart from the countable union of interface windows, which is null for
d-dimensional Lebesgue measure,

    O = disjoint_union_{j>=1} omega_j.

We may identify H=L^2(O) with the Hilbert direct sum of the cube L^2 spaces.
The collection of all f_{j,l} is therefore an orthonormal basis of H.
Every projection above now acts on H by zero extension. The inequalities,
ranks, and nesting in Section 4 remain unchanged under this identification.

Let A=A_O and let

    R_n = i_n(A_O_n+1)^(-1)r_n,   R=(A+1)^(-1),

where r_n restricts to O_n and i_n extends by zero. We need strong, not
norm, convergence R_n -> R on H. Here is a direct proof. On V=H_0^1(O)
use the Hilbert inner product

    b(u,v)= integral_O (gradient u dot conjugate(gradient v) + u conjugate(v)).

The zero-extended V_n=H_0^1(O_n) are increasing closed subspaces of V.
Their union is dense in V: a compactly supported smooth function on O has
compact support covered by the increasing open sets O_n, hence its support
lies in some O_N; such functions are dense by definition of H_0^1(O).

For f in H, u=Rf solves b(u,v)=<f,v> for v in V. The analogous solution
u_n=R_n f in V_n is the b-orthogonal projection of u onto V_n. Density and
the projection theorem give u_n -> u in V, and consequently in H. Also
||R_n||<=1 and ||R||<=1.

## 6. Fixed-rank limits commute with R

Fix k. By (4.1), for m>n>=k,

    ||P_m^k-P_n^k|| <= sum_{j=n}^{m-1} epsilon_j.

Thus P_n^k converges in norm to an orthogonal projection P^k, with

    ||P^k-P_n^k|| <= sum_{j=n}^infinity epsilon_j = 2^(-n-1).         (6.1)

The limit is a projection since multiplication and adjoints are norm
continuous. Its rank is the finite rank of P_k^k: for sufficiently large n
its norm distance to P_n^k is less than 1, and the rank comparison from
Section 2 applies. Since P_n^k<=P_n^{k+1} for n>=k+1, passage to the norm
limits shows P^k<=P^{k+1}.

Each zero-extended P_n^k commutes with R_n. For any f in H, boundedness of
R_n, strong convergence of R_n, and norm convergence of P_n^k give

    R_n P_n^k f -> R P^k f,
    P_n^k R_n f -> P^k R f.

Therefore RP^k=P^kR. In particular, range(P^k) is a finite-dimensional
reducing subspace for the bounded self-adjoint R.

The resolvent R is injective. Its restriction to this finite-dimensional
space is therefore injective, so all its eigenvalues mu on the space are
strictly positive. If Rv=mu v then v=mu^(-1)Rv belongs to dom(A), and
Av=(mu^(-1)-1)v. Diagonalizing R on this finite-dimensional space proves

    range(P^k) is contained in the pure point subspace H_pp(A).      (6.2)

This step excludes any possible escape of a protected finite-dimensional
space to infinite energy. Such an escape would create a nonzero vector in
the kernel of R; injectivity prevents it.

## 7. Completeness and exclusion of both continuous spectral types

Fix a cube-basis vector f_{j,l}. For every n>=max(j,l), it belongs to F_n.
Combining (4.2) and (6.1) with ||f_{j,l}||=1 gives

    ||(I-P^n)f_{j,l}||
       <= ||(I-P_n^n)f_{j,l}|| + ||P_n^n-P^n||
       < 2^(-n) + 2^(-n-1) -> 0.                                  (7.1)

By (6.2), P^n f_{j,l} belongs to H_pp(A). This subspace is closed, so every
f_{j,l} lies in H_pp(A). Since these vectors form a basis of H,

    H_pp(A)=H.

The mutually orthogonal absolutely continuous and singular continuous
spectral subspaces must both vanish. This is the required spectral-type
conclusion; merely producing dense eigenvalues would not suffice.

Equivalently, the increasing finite-rank projections P^k converge strongly
to I. The orthogonal differences P^{k+1}-P^k, together with P^1, reduce R
and admit finite eigenbases. Their union is a complete eigenbasis for A.

## 8. Spectrum as a set

Nonnegativity gives spectrum(A) contained in [0,infinity). For lambda>=0,
choose xi in R^d with |xi|^2=lambda, and a fixed smooth compactly supported
function chi in the unit ball with L^2 norm 1. In an inscribed ball of
omega_n use the test function

    u_n(x)=r_n^(-d/2) chi((x-c_n)/r_n) exp(i xi dot x),
    r_n=a_n/2,

where c_n is the cube center. It belongs to C_c^infinity(O) and has norm 1.
The product rule yields

    ||(A-lambda)u_n||
       <= r_n^(-2)||Delta chi|| + 2 |xi| r_n^(-1)||gradient chi|| -> 0.

Hence every lambda>=0 belongs to spectrum(A). The supports are in disjoint
cubes escaping to infinity, so the same sequence is weakly zero; alternatively,
the spectral interval has no isolated points. Thus the spectrum is entirely
essential. Since A has a complete eigenbasis, its spectrum is the closure of
its eigenvalues. They consequently form a dense subset of [0,infinity).

If Au=0, then q[u]=0; u has zero weak gradient and is constant on the
connected O. The domain has infinite measure, so an L^2 constant is zero.
Therefore all eigenvalues are positive. The proof of the assertion is complete.

## 9. Boundary of the claim

The choices are qualitative: no explicit numerical aperture sizes are
computed, and no effective modulus for (2.1) is claimed. No result for an
arbitrary fixed preexisting tower is asserted. No boundary smoothing or
passage replacement is needed for this proof. These strengthenings are
separate from the existential open-domain problem treated here.

The credit to [KL] is substantive: the geometry, cube-size freedom,
finite-window convergence, and original embedded-eigenvalue construction
come from that work. The argument here transports a growing family of
finite-rank spectral subspaces and proves completeness explicitly.

## References

[KL] D. Krejcirik and V. Lotoreichik, Quasi-conical domains with embedded
eigenvalues, Bulletin of the London Mathematical Society 56 (2024),
2969-2981. https://doi.org/10.1112/blms.13113 . Inspected author version:
https://arxiv.org/abs/2205.08172v2 ; particularly Section 2.2 and Section 3.

[OWR] V. Lotoreichik, joint work with D. Krejcirik, contribution on
quasi-conical domains in Geometric Spectral Theory, Oberwolfach Reports
36/2023, pp. 2077-2078. https://doi.org/10.4171/OWR/2023/36 .

[K26] D. Krejcirik, Spectral geometry: old questions and new answers,
arXiv:2609.28602v1, submitted 23 September 2026. Open Problem 1, PDF p. 16.
https://arxiv.org/abs/2609.28602v1 .
