# A candidate counterexample to the minimal-surface Seshadri bound

Status: complete candidate proof, not yet independently audited. No claim of historical priority or peer review. Prepared 2026-10-04 UTC for problem 30001232 / OWR-3471-006.

## Exact target and result

The primary source is Tomasz Szemberg's contribution, *Seshadri constants and geometry of surfaces*, Oberwolfach Report 21/2009, printed page 1124, Conjecture 2 (report DOI 10.4171/OWR/2009/21). Its denominator is **2 + the fourth root of |K_S^2|**, not the fourth root of **2 + |K_S^2|**. We work over the complex numbers, on smooth projective surfaces, with an ample integral line bundle and an arbitrary closed point.

**Candidate theorem.** For every integer d >= 7, there exist a smooth projective surface S with ample canonical bundle, an ample line bundle L on S, and a point x in S such that

    K_S^2 = 6(d-1)(d-3),    L^2 = 6,
    epsilon(S,L;x) <= 1/(d-1) < 1/(2 + (K_S^2)^(1/4)).

In particular d=7 gives K_S^2=144 and epsilon <=1/6 <1/(2+144^(1/4)). This is a counterexample to the primary conjecture if the proof below survives independent verification. Only the displayed upper bound for epsilon is claimed; no exact value is needed.

The construction starts with the classical Miranda pencil mechanism, as analyzed by Bauer [B99, Proposition 3.3 and its proof]. The added step is a double base change branched over four smooth fibres. We make no novelty claim for that operation or for the resulting example.

## 1. A pencil with a high-multiplicity integral member

Use coordinates [X:Y:Z] on P^2 and put

    f_d = Z(X^(d-1)-Y^(d-1)) + X^d,
    C_0 = V(f_d),    p=[0:0:1].

The polynomials X^(d-1)-Y^(d-1) and X^d are coprime in C[X,Y]. The polynomial f_d, regarded as a polynomial of degree one in Z over C[X,Y], is primitive and irreducible over C(X,Y). Gauss's lemma proves that C_0 is integral. In the chart Z=1 the lowest-degree part is x^(d-1)-y^(d-1), which has d-1 distinct linear factors. Thus p is an ordinary point of multiplicity d-1. In particular it is not a component or a nonreduced fibre. The partial derivatives also show that p is the only singular point: f_Z=0 forces X^(d-1)=Y^(d-1); if X,Y are nonzero, f_Y=0 forces Z=0 and then f_X=d X^(d-1) is nonzero. If either X or Y is zero, both are zero, giving p.

Here is a dimension argument ensuring the necessary pencil exists; it is not an assumption about a random sample. Let N_e=e(e+3)/2 be the dimension of the space of degree-e plane curves. The closed locus R of reducible degree-d forms is a finite union of images of multiplication maps

    P(H^0(O(a))) x P(H^0(O(d-a))) -> P(H^0(O(d))),
    1 <= a <= d-1.

Its dimension is at most max_a(N_a+N_(d-a))=N_d-(d-1). The union of projective lines joining [f_d] to points of R has dimension at most N_d-(d-2), strictly smaller than N_d for d>=3. Choose a form g outside its closure. The projective pencil spanned by f_d and g then has no reducible member. Over C a nonreduced degree-d plane curve is also reducible as a polynomial, so every member is integral.

At the same time choose g smooth, with g(p) nonzero, and meeting the smooth locus of C_0 transversely. These are nonempty Zariski-open requirements: smoothness and transversality follow from Bertini applied to the full degree-d linear system, and avoiding p is one open linear condition. Intersecting these open conditions with the complement of the preceding proper closed locus is nonempty. Bezout gives precisely d^2 distinct basepoints p_1,...,p_(d^2), all away from p. No explicit numerical choice of g is asserted or needed; the nonempty-open existence argument is part of the construction.

Blow up these d^2 points:

    b:Y -> P^2,    H=b^*(line),    E_i=b^(-1)(p_i),
    F=dH-sum_i E_i.

Transversality means one blowup at each point resolves the pencil. It induces a morphism f:Y->P^1. Its fibres are the strict transforms of the pencil members, and hence are integral and reduced. Every E_i is a section. A general fibre is smooth by Bertini. The strict transform C of C_0 is a fibre, and its point y above p still has multiplicity d-1 because b is an isomorphism near p.

## 2. An ample polarization on Y

Set A=2F+E_1. Standard blowup intersections give

    F^2=0,    F.E_i=1,    E_i^2=-1,
    A^2=3,    A.E_1=1,    A.F=1.

We check all integral curves, not only the displayed ones. The fibre class F=f^*O_P1(1) is nef. For an integral curve D different from E_1, intersection E_1.D is nonnegative. If F.D>0, then A.D=2F.D+E_1.D>0. If F.D=0, D is vertical for f and, because every fibre is integral and reduced, D is an entire fibre. In this case A.D=1. Together with A.E_1=1 and A^2=3, the Nakai-Moishezon criterion proves that A is ample.

This is the classical low-Seshadri pencil polarization. On Y it has A.C=1, but Y is not minimal. The following step addresses exactly that obstruction.

## 3. The smooth double base change

Choose four distinct values t_1,...,t_4 of P^1 over which f is smooth; exclude the value of C. Such values exist because the nonsmooth-fibre values form a proper closed, hence finite, subset of the base. Let h:B->P^1 be the connected double cover branched simply at these four points. This is a smooth projective genus-one curve, by Riemann-Hurwitz. Form

    S = Y x_(P^1) B,    pi:S->Y.

The map pi is finite flat of degree two, branched along the disjoint union f^*(t_1+...+t_4), a smooth divisor linearly equivalent to 4F. The fibre product is already smooth; no resolution or subsequent contraction is hidden in the notation. Away from the branch fibres, pi is etale over the smooth surface Y. At a point over a branch fibre, f is smooth, so local coordinates on Y are (t,u) and the base change has equation t=v^2; (v,u) are smooth local coordinates on S. Since the original fibres are geometrically connected and B is connected, S is connected, and therefore, being smooth, is integral. It is projective, for example because it is finite over projective Y.

The double-cover canonical formula gives

    K_S = pi^*(K_Y+2F).

This is also the direct Hurwitz formula, since the ramification divisor has line bundle pi^*O_Y(2F). Put N=K_Y+2F. Then

    K_Y=-3H+sum_i E_i,
    N=(2d-3)H-sum_i E_i,
    N^2=(2d-3)^2-d^2=3(d-1)(d-3).

## 4. Ample canonical bundle and minimality

For every exceptional curve E_i, N.E_i=1. Every other integral curve D on Y is the strict transform of an integral plane curve of degree e>=1, with multiplicities r_i>=0 at the basepoints. Choose a smooth pencil member different from its plane image. Bezout, with the local multiplicity inequality at each basepoint, gives

    sum_i r_i <= d e.

Consequently

    N.D=(2d-3)e-sum_i r_i >= (d-3)e >0

for d>=4. Along with N^2>0, Nakai-Moishezon proves that N is ample. A finite pullback of an ample line bundle is ample, so K_S=pi^*N is ample. In particular S is a minimal surface of general type: a smooth rational (-1)-curve would have canonical intersection -1 by adjunction, contrary to ampleness.

By the degree-two projection formula,

    K_S^2=2N^2=6(d-1)(d-3).

This proves the exact minimality hypothesis required by the source; the nonminimality of Y is immaterial after the base change.

## 5. Preserving the small Seshadri quotient

Let L=pi^*A, an ample integral line bundle with L^2=2A^2=6. The chosen singular fibre C lies over an unbranched value. Its inverse image is the disjoint union of two fibres C' and C'', and each maps isomorphically to C. Choose x on C' above y. Etaleness preserves the multiplicity d-1. The projection formula on C' gives

    L.C'=A.C=1,    mult_x C'=d-1.

The defining infimum of the Seshadri constant, taken over integral curves through x, therefore implies epsilon(S,L;x)<=1/(d-1).

For d>=7 the desired strict numerical inequality is equivalent to

    (d-3)^4 > 6(d-1)(d-3),

or (d-3)^3>6(d-1). At d=7 this reads 64>36. The difference

    [(d-2)^3-6d] - [(d-3)^3-6(d-1)]
      = 3(d-3)^2+3(d-3)-5

is positive for d>=7, proving the inequality for the whole asserted family. For the single smallest example, one can simply use 144<4^4=256, so 2+144^(1/4)<6.

## Verification boundaries

The accompanying programs check intersection calculations in the 1+d^2 dimensional blowup lattice, separate closed-form surface/cover identities, finite-dimensional pencil counts, polynomial tangency data, and exact strict inequalities. They do not certify Bertini, Nakai-Moishezon, the general cover construction, or historical novelty. Those inputs and their application must be assessed in a fresh mathematical audit. No source PDFs or text are included in this author packet.

## References

- [OWR] T. Szemberg, *Seshadri constants and geometry of surfaces*, in Oberwolfach Report 21/2009, pp.1124-1126, Conjecture 2 on p.1124. https://ems.press/journals/owr/articles/3471 ; https://doi.org/10.4171/OWR/2009/21
- [B99] T. Bauer, *Seshadri constants on algebraic surfaces*, Math. Ann. 313 (1999), 547-583, Proposition 3.3 and proof, especially the degree choice d=m+1 in part (b). https://arxiv.org/abs/math/9903072
- [S08] T. Szemberg, *An effective and sharp lower bound on Seshadri constants on surfaces with Picard number 1*, J. Algebra 319 (2008), 3112-3119, final question, preprint p.7. https://arxiv.org/abs/0711.0584
- [Primer] T. Bauer et al., *A primer on Seshadri constants*, arXiv:0810.0728v2, Question 6.1.6, p.17. https://arxiv.org/abs/0810.0728
