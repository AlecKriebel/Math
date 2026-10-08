# Calegari Question 4.2: scoped reductions and five routes

Problem 10300008 / AMR-102-0008. Author investigation, 8 October 2026.
No general solution, novelty, or independent-review claim is made.

## Scope and notation

The source asks for obstructions to making a collection of taut foliations on a
three-manifold minimal for one Riemannian metric, with isotopy permitted. It does
not fix the metric to be hyperbolic. Here all proved differential statements use
a smooth oriented three-manifold and smooth cooriented codimension-one
foliations. Compact-leaf conclusions additionally use closed oriented leaves.
The general source question is not restricted to this setting, or explicitly to
a finite collection. Our finite-triple reductions do not remove those issues.
Isotopies below are allowed separately for the different foliations; a common
ambient isotopy is a more restrictive variant and cannot remove relative
tangencies. Every statement below distinguishes fixed representatives from
this independent-isotopy interpretation.

For a unit normal n to a foliation, let h = div_g(n), the trace convention for
scalar mean curvature. Reversing n changes its sign but not its vanishing. The
characteristic two-form is chi = i_n vol_g. Cartan's formula gives

    d chi = h vol_g.                                           (1)

Indeed, for an orthonormal frame e1,e2,n, divergence is the sum of
g(nabla_ej n,ej); the n term vanishes because n has length one. Thus h is
the tangential trace of the normal derivative, and its vanishing is minimality.
Equation (1) follows from L_n vol_g = (div_g n) vol_g. Consequently a minimal
cooriented foliation has a closed characteristic TWO-form. Its comass is one,
by Cauchy--Schwarz after identifying an oriented unit two-plane with its unit
normal. This is the codimension-one instance of the classical Rummler--Sullivan
calibration calculation; it is not a new theorem.

## Route 1. Attempt to combine individual calibrations

The attempted strategy is to apply the individual tautness criterion and then
combine its closed forms into a metric. It fails without a genuinely common
metric-compatibility condition. A single common calibration is not a necessary
condition: on the flat three-torus the foliations x = constant and y = constant
are both totally geodesic. In a Euclidean oriented three-space any two-form is
i_v vol. Its comass is |v|, and equality on an oriented unit two-plane with
normal n is v dot n = 1. If |v| <= 1 this forces v=n. It cannot calibrate two
different oriented planes. Thus even a successful simultaneous minimal metric
generally supplies different closed forms, one per foliation.

There is an exact, but still differential, compatibility reduction for three
foliations. Suppose positive smooth tangent bivectors xi1,xi2,xi3 form a frame
of Lambda^2 TM everywhere. They need not be unit. There is a common minimal
metric for these fixed representatives if and only if there are smooth closed
two-forms omega1,omega2,omega3 such that ai=omegai(xii)>0 and the matrix

    Sij = ai omegai(xij)                                      (2)

is symmetric positive definite at every point.

Proof, necessity. Let B be the inner product on Lambda^2 TM induced by g.
The characteristic form for the plane represented by xii is

    omegai(eta) = B(xii,eta)/sqrt(B(xii,xii)).                  (3)

It is closed by (1), ai=sqrt(B(xii,xii)), and Sij=B(xii,xij).
Thus (2) is the Gram matrix of a positive definite inner product.

Proof, sufficiency. Use (2) to define a smooth inner product B on Lambda^2 TM
by B(xii,xij)=Sij. In any oriented frame e1,e2,e3 of TM, express B in the
cofactor bivector frame (e2 wedge e3,e3 wedge e1,e1 wedge e2). The induced
metric of a positive matrix G on TM has matrix cof(G)=(det G)G^{-1} on this
bivector frame. Conversely, for every positive matrix B the positive matrix

    G = sqrt(det B) B^{-1}                                    (4)

satisfies cof(G)=B. In fact det G=sqrt(det B), which proves the identity.
The operation is unique and therefore agrees under changes of local frames;
it constructs a smooth metric globally. Now B(xii,xii)=ai^2 and, on the
bivector basis, B(xii,.)=ai omegai(.). Equation (3) gives precisely omegai.
Since these forms are closed, (1) proves simultaneous minimality. QED.

The strategy therefore reaches a real algebraic compatibility test for CHOSEN
closed forms, but not a criterion for choosing them. Individual positivity
omegai(xii)>0 does not imply (2): in a three-dimensional bivector basis take
omega1=(1,2,0), omega2=(0,1,0), omega3=(0,0,1). All diagonal evaluations are
positive, and constant forms are closed, but S12=2 and S21=0. No inner product
can have these three forms as its characteristic forms. This does not obstruct
the plane fields themselves, since alternate forms may work.

Remaining gap: existence of closed compatible forms after the allowed
isotopies, as well as variable-rank, arbitrary-size and non-cooriented cases.
The reduction is not an elimination of the original unknown metric problem.

## Route 2. A local second-jet obstruction, and why isotopy matters

We next try to obstruct a common metric through a forced tangency. The
following obstruction is independent of which smooth ambient metric is chosen.

Let two embedded surface patches be z=0 and z=f(x,y), where f(0)=0 and
df(0)=0. If D^2 f(0) is positive semidefinite and nonzero, the two patches
cannot both be minimal at 0 for any ambient Riemannian metric.

Proof. Their tangent bases at 0 agree, namely partial_x, partial_y. Fix a
common unit normal n with g(n,partial_z)>0. In their second fundamental forms
b_ab=g(n,nabla_{Xa}Xb), the connection terms coincide at 0; their difference
is f_ab g(n,partial_z). The first fundamental forms at 0 also coincide. The
difference of the traces of the two second fundamental forms is therefore
g(n,partial_z) tr(C D^2f), where C is the positive definite inverse induced
metric on the common tangent plane. If D^2f is positive semidefinite nonzero,
then C^(1/2) D^2f C^(1/2) is positive semidefinite nonzero and has positive
trace. Both traces cannot vanish. QED.

Here is a global example with both foliations taut. On T^3=(R/Z)^3 put

    f(x,y)=epsilon(2-cos(2 pi x)-cos(2 pi y)),  0<epsilon<1/8.
    F0: z=constant;     F1: z-f(x,y)=constant mod 1.

These are smooth circle fibrations. A vertical circle at fixed x,y is
transverse and meets every leaf, so both are taut. At (0,0,0) the displayed
zero leaves are tangent and D^2f=4 pi^2 epsilon I. The preceding proof
excludes a common minimal metric for these FIXED representatives.

But the maps phi_t(x,y,z)=(x,y,z-t f(x,y)), 0<=t<=1, are smooth
diffeomorphisms, with inverse (x,y,z+t f(x,y)). They are well-defined on T^3
and start at the identity. The final map sends F1 to F0. Apply this isotopy
only to F1 and leave F0 fixed. The resulting collection is minimal in the
flat metric. The pair is therefore NOT a counterexample to the independent-
isotopy version of Question 4.2. If one insists instead on applying one common
ambient isotopy to both foliations, pulling back a proposed metric shows that
this pair remains obstructed. Those two interpretations must not be conflated.

The same example has tangent plane fields arbitrarily close in every fixed
C^k norm as epsilon tends to zero. Thus closeness alone does not imply a
common smooth minimal metric for the original representatives. In particular,
the printed PL observation cannot simply be promoted to that stronger claim.

Remaining gap: produce an obstruction to tangency removal by independent
isotopies, or construct isotopies that arrange all local compatibility
conditions. The example proves neither general assertion.

## Route 3. Compact-leaf homology and an isotopy-invariant necessary condition

The local obstruction above disappears under independent isotopy. This route
instead uses a compact-leaf invariant that independent isotopies preserve.

Suppose F and G are cooriented foliations minimal for the same metric on a
closed oriented three-manifold. Let S be a closed connected oriented leaf of F
and T a closed connected oriented leaf of G. Use their induced orientations.
If [T]=c[S] in H_2(M;R), with c>0, then T is also a leaf of F and S is also a
leaf of G. In particular S and T are disjoint or are the same leaf, as sets.

Proof. Let omega and eta be the respective closed characteristic forms from
(1). Their comasses are one, and their restrictions to the appropriate leaves
are the area forms. Write a=Area(S)>0 and b=Area(T)>0. Homology and Stokes
give

    b >= integral_T omega = c integral_S omega = ca,
    a >= integral_S eta = (1/c) integral_T eta = b/c.

Both inequalities must be equalities. On T the continuous nonnegative density
dA_T-omega|_T has integral zero. It vanishes pointwise. At every point of T,
the equality case in Cauchy--Schwarz identifies its oriented tangent plane
with TF. Thus T is tangent everywhere to F. In a foliation chart the
transverse coordinate is constant on each connected piece of T, so T lies in
a single connected leaf L of F. The inclusion T -> L is a local
diffeomorphism, hence has open image. Its image is compact and therefore
closed in the Hausdorff leaf manifold L. Consequently T=L. Interchanging
the foliations proves the assertion about S. Distinct leaves of F cannot
intersect. QED.

The homology classes in this argument are necessarily nonzero: if [S]=0,
closedness would imply integral_S omega=0, contradicting a>0. Likewise for T.
Negative proportionality can be handled by reversing the chosen coorientation
of one foliation, but the displayed theorem uses the positive convention.

It follows that the following is an obstruction which survives the permitted
independent isotopies. Suppose the original F has a compact oriented leaf S,
the original G has a compact oriented leaf T, and [T]=c[S], c>0. If the
oriented ambient isotopy class of T is not represented by any compact leaf of
F, then no separately isotoped F and G can be simultaneously minimal.

For if phi(F),psi(G) were simultaneously minimal, the proved assertion makes
psi(T) a leaf of phi(F). Thus phi^{-1}psi(T) is a leaf of F. Since phi and
psi are each isotopic to the identity, phi^{-1}psi is also isotopic to the
identity and preserves homology and the transported orientation. This
contradicts the assumed absence of that leaf isotopy class. The symmetric
condition with F,G interchanged is necessary as well. A weaker consequence
is that two non-isotopic compact leaves on the same positive homology ray
must have disjoint representatives.

Attempted extension. One might use two homologous, non-isotopic
norm-minimizing surfaces and arrange taut foliations containing them, hoping
that one foliation excludes the other's isotopy class. This investigation has
not supplied such an explicit verified closed-manifold pair. Homology alone
does not imply that two surfaces are non-isotopic or cannot be disjoint, and
an existence theorem for a taut foliation containing S does not identify ALL
its compact leaves. Furthermore, genus minimization and area minimization
are different notions. Those are actual missing construction steps, not
conclusions justified by the inequalities above.

Remaining gap: realize and classify this obstruction for arbitrary prescribed
foliations; and treat pairs without suitable compact leaves. No sufficiency
claim, example violating the criterion, or full resolution follows.

## Route 4. Solve the simultaneous equations in a fixed conformal class

Fix a smooth metric g0 and coorientations. Let ni be its unit normals and
hi=div_g0(ni). Under g=e^(2u)g0 the unit normal becomes e^(-u)ni and the
volume form becomes e^(3u)vol_g0. The defining equation for divergence gives

    hi(g) = e^(-u)(hi + 2 ni(u)).                            (5)

For completeness, L_X(f vol) = (X(f)+f div X)vol. Substitute
X=e^(-u)ni and f=e^(3u); the derivative terms are 3ni(u)-ni(u),
which proves (5). Thus simultaneous minimality in this conformal class is
equivalent to the system ni(u)=-hi/2 for all i.

If n1,n2,n3 form a smooth frame of TM, there is a unique smooth one-form
beta with beta(ni)=-hi/2 for i=1,2,3. A simultaneous minimal metric in the
conformal class exists if and only if beta is exact and
beta(nj)=-hj/2 for every additional foliation j. Necessity follows by taking
beta=du. Conversely an exact beta=du satisfying the extra equations gives
minimality by (5). On a connected manifold the potential is unique up to an
additive constant, because its differential is specified on a frame.

The exactness test is equivalent to d beta=0 and zero integral around every
closed piecewise smooth loop. Necessity is immediate. For sufficiency choose
a base point and define u(p) as the beta integral along any path from the
base point to p. The zero-period condition makes it path-independent; in a
coordinate ball, closedness supplies the local potential and proves smoothness
and du=beta. This proves the criterion without replacing global exactness by
local closedness. It is an exact criterion only for the CHOSEN conformal class.

There are taut collections which pass the unrestricted problem while failing
this conformal test. On T^3 let

    b(x,y)=sin(2 pi x)sin(2 pi y),
    g0=dx^2+e^(2b)dy^2+dz^2,

and take the three coordinate foliations. Their g0 unit normals are
n1=partial_x, n2=e^(-b)partial_y, n3=partial_z. Since vol_g0=e^b dx dy dz,
their mean-curvature traces are h1=b_x, h2=0, h3=0. The resulting beta is
-(b_x/2)dx, with

    d beta = (b_xy/2) dx wedge dy.

At x=y=0 this equals 2 pi^2 dx wedge dy and is nonzero. No conformal
multiple of this g0 makes the three coordinate foliations simultaneously
minimal. They are nevertheless all minimal for the flat metric. Each is
taut, with a transverse coordinate circle meeting every leaf.

Remaining gap: choose a conformal class (and isotopies) for which these
compatibility and period conditions hold. Formula (5) gives no reason that
failure in one conformal class survives changing the class. It therefore
cannot be promoted to an obstruction for the unrestricted source question.

## Route 5. Constructive positive families and the smooth gluing gap

We finally try to construct a common metric by local product models and
gluing. There is an immediate class of positive examples. Let a(z)>0 be a
smooth periodic function and put, on T^3,

    g_a=a(z)^2 dx^2+a(z)^(-2)dy^2+dz^2.                       (6)

Its volume form is dx dy dz. The coordinate foliations have unit normals
a^(-1)partial_x, a partial_y, and partial_z, each with zero divergence.
More generally, every foliation ker(p dx+q dy), where (p,q) is a nonzero
integer pair, has unit normal

    n=(p a^(-2)partial_x+q a^2 partial_y)
          /sqrt(p^2 a^(-2)+q^2 a^2).

Its coefficients depend only on z and its z component is zero. Its divergence
is therefore zero. These foliations and the horizontal foliation are all
simultaneously minimal. They are taut: after dividing p,q by their greatest
common divisor the foliation is a fibration over S^1, and a closed integral
linear transversal with nonzero evaluation meets every fiber. For the
horizontal foliation use a vertical circle. Thus there are infinite
collections for which the simultaneous condition is entirely compatible.

These elementary models do not capture the limit of current positive
literature. Nguyen, arXiv:2608.18428v2, Theorem 1.2, constructs calibrated
torus foliations in every primitive codimension-one homology class for a
broader one-variable family of metrics. Marques--Neves--Sun,
arXiv:2608.15376v1, Theorem 5.1, gives an overlapping cofactor formulation.
Their results and the nonflat torus examples are credited prior work. The
present calculation is only a transparent special case, not a new solution.
Existence of suitable foliations in each class does not establish existence
for arbitrary prescribed taut foliations on an arbitrary three-manifold.

There is also a precise failure in the naive gluing method. Both (6) and the
flat metric make the horizontal foliation minimal. Their arithmetic average
is block diagonal with z coefficient one and horizontal area density

    A(z)=sqrt((a(z)^2+1)(a(z)^(-2)+1))/2
        =(a(z)+a(z)^(-1))/2.                                 (7)

For this average metric the horizontal unit normal is partial_z, so its
mean-curvature trace is A'(z)/A(z). Take a(z)=2+sin(2 pi z). At z=0,
a=2 and a'=2 pi, whence A'=3 pi/4 and A'/A=3 pi/5, which is nonzero.
Thus even averaging two metrics which solve the SAME single-foliation
minimality condition can destroy that condition. A partition-of-unity
argument on arbitrary metric solutions is invalid without extra structure.

One might instead glue closed characteristic forms, but a partition of unity
also introduces d rho wedge omega terms. Gluing closed forms by a procedure
that repairs those errors must additionally preserve the common positive-
matrix compatibility of Route 1. No such construction has been proved here.
The printed PL recurrent-weight observation is not already this smoothing
and compatibility theorem. The arbitrarily close fixed-representative
counterexample in Route 2 further excludes the simplest unjustified version.

Remaining gap: a global smooth construction preserving closedness, algebraic
metric compatibility and the allowed foliation isotopy classes. The special
torus families and the PL remark supply neither a necessary-and-sufficient
classification nor a universal construction.

## Final mathematical disposition

Five distinct strategies were investigated: common closed-form compatibility;
local second jets; compact-leaf homology; conformal integrability; and
constructive models/gluing. The propositions above are proved under their
explicit hypotheses. The general Question 4.2 is UNRESOLVED BY THIS WORK.
The bounded literature check did not establish its complete current global
status. In particular, this packet does not prove a universal existence
theorem, a complete obstruction classification, or an explicit counterexample
to the independent-isotopy problem. It must be recorded as unsolved, 5/5,
subject to separate mathematical review.
