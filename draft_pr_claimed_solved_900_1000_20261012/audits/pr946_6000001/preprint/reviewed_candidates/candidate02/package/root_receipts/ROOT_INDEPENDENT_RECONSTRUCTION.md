# Independent reconstruction of the global realization argument

Verification of PR946/6000001, immutable head
7d3adb0e500b0414a49a449e7981d34ade329427. The complete source/prior
report and proof were read before this reconstruction. This checks the saved
mechanism; it supplies no new proof-search response. Five independent family
verdicts and deep priority remain separate obligations.

## Exact target and conventions

The scanned FMU1998 printed p125 item1(a) begins with a Riemannian metric
and mutually dual affine connections. It asks for realization as a higher
dimensional submanifold of a dually flat manifold, and, if needed, an additional
condition. Its cited Amari1997 printed p84 explicitly requires both torsion
and curvature to vanish, and uses local dual affine coordinates. Thus a general
dual pair must first have both torsions zero. This is necessary under induced
orthogonal projection from torsion-free ambient connections. It is sufficient
if the present construction is correct. A fixed probability model, convex
domain, complete metric or globally injective gradient is absent from this
target. No answer to those stronger variants follows here.

The hypotheses are smooth, Hausdorff, second-countable finite-dimensional
manifolds without boundary and a positive metric. These ensure paracompactness
and smooth bundle metrics. No orientability, connectedness or completeness
assumption is used. The claimed ambient dimension for n>=1 is
N=binomial(2n+4,3)>n. A countable discrete zero-manifold has a separate
proper embedding in a line and no nonzero tangent data.

## Scalar jets, including their inhomogeneous transition

Let L be the Levi-Civita connection. Duality and both torsion conditions make
A=∇−L a symmetric tensor whose lowered version is symmetric in all slots.
Consequently C=∇g=−2g(A,.) and Γ_ijk=L_ijk−C_ijk/2. Hence

    Q_ijk=∂_k g_ij+Γ_ijk
         =(∂_i g_jk+∂_j g_ik+∂_k g_ij−C_ijk)/2

is symmetric. It is not a covariant3tensor. At each p prescribe a scalar3jet
by q_p(exp_p(v))=g_p(v,v)/2−C_p(v,v,v)/12. The exponential is needed only
as a germ near the zero section; local smooth dependence makes this a smooth
section without a uniform injectivity radius. Normal-coordinate third
derivatives are −C/2. In arbitrary coordinates the three Christoffel
correction terms sum to (∂_i g_jk+∂_j g_ik+∂_k g_ij)/2. Thus the ordinary
third derivative is exactly Q. The zero first derivative removes third
coordinate-change derivatives, while the nonzero metric supplies precisely
the three second-coordinate-change terms. Treating Q as a tensor would fail.

Take a proper smooth Whitney embedding e into R^(2n+1), and all ambient
monomials of degree<=3, including the constant, as f's coordinates. Linear
projection recovers e. Injectivity, differential injectivity and topology
follow from that projection. For a compact ambient B, f^−1(B) is closed in
the compact e^−1(π(B)), giving properness and a closed embedded image S.

For each p choose n ambient linear functions whose restricted differentials
are independent. They are local coordinates. Every scalar3jet in them is
represented by a degree<=3 polynomial in these restricted functions centered
at p; this remains an ambient polynomial of that degree. Therefore one common
finite polynomial space surjects onto every fiber of J^3(M,R). The coordinates
chosen to prove surjectivity may vary; the ambient feature space does not.

For the resulting smooth bundle map E, choose smooth positive bundle metrics.
The right inverse E†(EE†)^−1 exists smoothly because EE† is positive definite
at every point. No bounded inverse or finite chart cover is required. Applying
it to the prescribed jet gives a smooth coefficient covector a with

    a·f=0, a·f_i=0, a·f_ij=g_ij, a·f_ijk=Q_ijk.

The evaluation derivatives hold a fixed at the point; subsequent
differentiation along M differentiates a as well. For φ=−a this gives

    φ·df=0, f_i·φ_j=g_ij, f_ij·φ_k=Γ_ijk.

The first identity makes potential compatibility exactly zero, rather than
assuming away a period obstruction. The last identity verifies the specified
connection, including its sign; knowing only the middle one would be insufficient.

## One global positive Hessian neighborhood

The smooth tubular-neighborhood theorem for a closed Euclidean embedded
submanifold gives an open T, normal projection r and ν=z−r(z). The tube may
have a variable radius; completeness and a trivial normal bundle are unnecessary.
The covector φ annihilates TS. Thus Ψ0(z)=φ_r(z)(ν(z)) is smooth, vanishes
on S and has ambient differential φ there. Differentiating that equality
along S fixes every Hessian column on tangent vectors: H0(f_i,.)=φ_i.
In particular its tangent block is g, positive relative to the Euclidean
tangent metric. Along a fixed straight normal fiber the function is linear,
so the normal-normal block is zero. In orthonormal blocks this is

    H0=[A B; B^t 0], A>0.

Both t=tr(A^−1)||B||_HS² and λ=1+t are globally smooth scalar functions on S;
their frame independence follows from the Euclidean bundle metrics. Adding
λ(r(z))|ν(z)|² changes neither the value nor gradient on S, and changes only
the normal-normal Hessian there to 2λI. For every normal w,

    w^t B^t A^−1 B w <= tr(A^−1)||B||_HS² |w|²=t|w|².

The Schur complement is at least (2+t)I, so the full Hessian is positive on
every point of S. Its positive-definite locus inside T is open and contains
all of S. Taking this locus as U proves one global realization, without
inventing a uniform radius or spectral lower bound. Properness into U follows
since a compact subset of U is compact in the original Euclidean space.

## Flatness and the ordered induced connections

On U, G=Hess Ψ and the standard D is flat and torsion-free. Its dual has
coefficient matrices G^−1∂_A G. The symmetry of Ψ's third derivative gives
torsion-freeness. The functions η_E=∂_E Ψ have invertible Jacobian G and
zero D*-covariant Hessian, so give local D*-affine charts. This proves
flatness locally everywhere; it does not require η globally injective.

The preserved gradient equality gives G(f_i,.)=φ_i. Thus f*G=g and

    G(f_ij,f_k)=f_ij·φ_k=Γ_ijk.

Orthogonal projection of D induces ∇, with the original ordering. Ambient
duality restricted to tangent fields and uniqueness of the g-dual connection
then induce exactly ∇*. Projection of either ambient torsion identity proves
the necessary condition on a general dual pair. There is no assumption of a
flat Levi-Civita metric or trivial intrinsic holonomy.

## Evidence limits and current assessment

No mathematical gap in this mechanism was found by this reconstruction.
Proper Whitney embedding and the smooth tubular theorem are declared
external differential-topology inputs; finite scripts do not prove them.
The current original wrapper rejects platform-level floating differences in
the author numerical samples even though all actual author assertions pass;
that failure is preserved and its transport repair is pending. Exact algebraic
identities, numerical corroboration, universal proof, original4/5 declaration
and historical priority must remain distinct. No novelty, exhaustive search,
human peer review, formal certification or completed publication is asserted.
