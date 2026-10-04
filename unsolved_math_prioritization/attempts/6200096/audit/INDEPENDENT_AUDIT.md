# Independent adversarial audit: 6200096

Audit date: 2026-10-04 UTC. Target: AMR-061-0096, rank 648.

## Verdict

**PASS: `already_solved`, negative for the unrestricted homotopy-compatible
Nielsen realization question.** No mathematical correction is required.
The compact two-dimensional example and the obstruction for every
homotopy-equivalent replacement space are valid. This is verified prior work,
not a new discovery or a solution of a restricted variant.

The inspected author payload is bound by manifest SHA-256
`ddc7550f12c0b732ac42a5eb1238002d1877950b4d74d8a81ba98ccd15632f99`.
The 12 listed payloads, the manifest itself, and all archive members match.
The 12,868-byte frozen archive has SHA-256
`9b7ff841bdde3323e364149fb5081e09e5a9942295296f19eb1d5648a3757571`.
Originals were preserved. No remote writes or external communications occurred.

## 1. Exact target and attribution

I compared the selected dataset statement against Kapovich's author-hosted
Problem 96, page 24, using an independently implemented normalizer, and
visually inspected that page. They agree. The immediately following Remark 32
already attributes negative examples to Cooke. Its historical discussion of
known examples in dimension at least five does not impose a dimension bound
on the question. Neither does it assert that later low-dimensional examples
are impossible. The packet correctly confines its disposition to the
unrestricted question.

Source: M. Kapovich, *Problems on Boundaries of Groups and Kleinian Groups*,
Problem 96 and Remark 32, page 24:
https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf

The printed problem is informal about the word "group" and compatibility.
The intended homotopy Nielsen interpretation is a homomorphism into unbased
homotopy classes, realized under a homotopy equivalence. This is the standard
interpretation made explicit in Smrekar's Example 1 and the author's proof.
A strict group of actual continuous maps whose inverses are actual continuous
maps would already consist of homeomorphisms. An unrelated action of the
abstract group on a replacement is also a different question: the same
polyhedron below already admits an unrelated, zero-twist involution.

I freshly retrieved Kapovich's PDF, Smrekar's published PDF, and Smrekar's
author manuscript. All three byte counts and SHA-256 hashes match the source
manifest. I inspected the published Example 1 on page 5, its publication
information on page 1, and the corresponding manuscript passage. The
published specialization is p=2, A=(-1), central twist one, with rotation
period q=4 rather than p=2. Its stated non-realizability agrees with the
reconstructed argument. The university record identifies the published
article as Journal of Pure and Applied Algebra 227(7) (2023), 107350.

Sources:
- https://doi.org/10.1016/j.jpaa.2023.107350
- https://repozitorij.uni-lj.si/IzpisGradiva.php?id=148644
- https://repozitorij.uni-lj.si/Dokument.php?id=172925&lang=slv
- https://users.fmf.uni-lj.si/smrekar/research/rroafo2022.pdf

The proof does not invoke the conditional Bass-conjecture results elsewhere
in Smrekar's article. I did not independently retrieve Cooke's full original
proof or rerun the live repository and full-corpus duplicate searches. Those
historical discovery checks are not needed for the mathematical verdict and
are not promoted to fresh audit results here.

## 2. Algebra and outer-versus-based issue

Let H=Z x F(a,b,d), with central generator c, and define

    phi(c)=c^-1, phi(a)=ca, phi(b)=d, phi(d)=a^-1 b a.

The displayed inverse in the author proof is correct. Both homomorphisms
respect the central commutator relations. On each generator,
phi^2(h)=a^-1 h a; equality on generators establishes the all-elements
identity. Thus the order in Out(H) divides two. It is exactly two because an
inner automorphism fixes c while phi inverts this infinite-order central
letter. No based finite-order automorphism is asserted or needed.

This distinction is essential. The graph involution moves the chosen vertex,
so its induced based automorphism incorporates a path. Ignoring this path
would erase the inner square and destroy the actual obstruction.

## 3. Geometry, simple homotopy, and a direct square homotopy

The graph has four edges and two vertices, so its fundamental group has rank
three. With e:u->v, f:v->u and loops B,D at u,v, the loops

    a=ef, b=B, d=f^-1 D f

form a basis. The edge exchange delta is an honest PL involution. The path
p=f^-1 runs from u to delta(u)=v. Applying p delta(loop) p^-1 gives, in this
basis, a, d, a^-1 b a. The circle winding introduced by kappa is one on a
and zero on b,d. Circle reflection sends c to c^-1. Consequently the total
map F(s,x)=(-s+kappa(x),delta(x)) induces precisely phi after basepoint
transport. Every orientation and endpoint in these formulas checks.

The inverse formula F^-1(s,x)=(-s+kappa(delta(x)),delta(x)) checks by direct
composition. On every product cell the formula is affine in coordinates,
modulo finitely many circle wrap lines. Finite compatible subdivisions make
it PL. The circle times this finite graph is a compact two-dimensional
polyhedron, and a PL homeomorphism of finite polyhedra is simple: take
subdivisions on which it is simplicial and use invariance of simple type
under finite subdivision. No Whitehead-group vanishing assumption is hidden.

There is also a direct verification of the finite-order *homotopy class*,
which is independent of the aspherical classification used by the author.
Give each indicated edge its parameter t in [0,1] and define a real function
lambda on the graph by

    lambda(e(t))=-t, lambda(f(t))=t-1,
    lambda(B(t))=0, lambda(D(t))=-1.

These formulas agree at vertices: lambda(u)=0 and lambda(v)=-1. Modulo one,
lambda(x)=kappa(delta(x))-kappa(x). Therefore

    F^2(s,x)=(s+lambda(x),x),
    J_r(s,x)=(s+r lambda(x),x), 0<=r<=1,

is an explicit homotopy from the identity to F^2. In fact every J_r is a
homeomorphism. The class of F is nontrivial since its action on the central
circle generator is inversion. Hence it determines an injective C2 subgroup
of unbased simple self-homotopy classes. F itself is not an involution, as
one sees at t=1/2 in edge e. Confusing F with an involution is not part of the
author argument.

## 4. Arbitrary replacement spaces and possibly nonfaithful actions

Suppose Y is homotopy equivalent to X. It is path-connected: for a homotopy
inverse pair, a homotopy from their composite to id_Y connects every point of
Y to the path-connected image of X. This conclusion does not require Y to
be locally path-connected, semilocally simply connected, or a CW complex.
The homotopy equivalence identifies its fundamental group with H. It need
not supply a convenient universal cover.

For any left K-action by homeomorphisms of such a Y, use pairs (g,[gamma])
with gamma a path from y to g(y). The product is

    (g,[gamma])(h,[eta])=(gh,[gamma * g(eta)]).

Endpoint-fixed path homotopies make this a well-defined associative group.
The inverse is (g^-1,[g^-1(reverse gamma)]); the identity uses the constant
path. Projection is surjective by path-connectedness, and its kernel is
exactly pi_1(Y,y), not a quotient of that group. Conjugation on the kernel is
the usual basepoint-adjusted action. Thus every such action gives

    1 -> pi_1(Y,y) -> E -> K -> 1.

The construction does not require a free or faithful action. Homotopy
compatibility, transported through the chosen homotopy equivalence, forces
the outer action of C2 on H to be [phi]. A change of identification merely
conjugates the outer representation and cannot repair non-existence of an
extension. The compactness requirement on Y is therefore harmless: the
obstruction holds even when compactness is dropped.

## 5. All-elements extension obstruction

Assume an extension inducing [phi] exists. If a lift initially induces
inn(u) composed with phi, replace it by u^-1 times that lift. We may thus
choose t with conjugation exactly phi. Since its quotient has order two,
t^2 belongs to H. Its conjugation is phi^2=inn(a^-1), so

    t^2=c^n a^-1

for some integer n, because Z(H)=<c>. Every element commutes with its square.
Conjugating this equation by t consequently requires

    c^n a^-1 = phi(c^n a^-1) = c^(-n-1) a^-1.

Infinite order of c gives 2n=-1, a contradiction. The argument rules out
all extensions, not only split extensions or extensions with finite-order
lifts. It does not presume fixed points, basepoint preservation, covering
space regularity, or any finiteness of Y.

For the twist k, the same necessary equation is 2n=-k. Odd twists fail and
zero twist has the genuine involution (-s,delta(x)). Replacing the integral
center with a rational one changes the problem. Passing from C2 to a larger
acting group, such as C4 with a nonfaithful homotopy action, also changes the
specified group; it does not evade this obstruction.

## 6. Reproducibility and audit limitations

- Author manifest verifier: PASS, 12 payloads.
- Author algebra/graph controls: PASS, 632,826 assertions; replayed JSON is
  byte-identical to CONTROL_RESULTS.json.
- Independently written verifier: PASS, 74,902 assertions. It uses raw words
  in four generators, signed graph-edge paths, and exact rational coordinates.
  It imports none of the author's verifier code.
- Independent diagnostics include 4,681 raw words, four twists, 4,224 exact
  geometric points, gluing at vertices, both inverse compositions, the square
  homotopy endpoint, a strict non-involution witness, and parity checks.
- The finite checks only detect mistakes. The preceding generator, PL,
  path-group, and integer arguments prove the universal statements.

The original normalized-statement digest needs an exact executable
normalization specification for bit-for-bit replay. Independent normalization
nevertheless gives exact equality of the selected statement and the primary
source, and the raw selected-statement digest matches. This is a metadata
reproducibility clarification, not a mathematical gap. See
CORRECTIONS_AND_SCOPE.json for the current disposition of this point.

No source PDF, extracted full text, dataset record or corpus, private source,
or private coordination file is included in this audit package. Source
records contain public URLs, titles, status, locators, byte counts, hashes,
and inspection history only.
