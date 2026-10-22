# PR833: independent root reconstruction of the lower-bound gap

2026-10-21 UTC. Original head: `0e6e23213494ecb4a7208f920d25d7b49502a5cb`.
Fresh Google Workspace CLI and full authenticated Zenodo inventory searches
preceded substantive work. This is an audit note, not a publication package.

The original author proof explicitly imports the lower bound eight and proves
an upper bound. Its exact equality therefore depends on a valid lower theorem
for the same ordinary section genus. Connected full-cover trivialization and
algorithmic branching are stronger/different requirements, explicitly outside
that manuscript. Neither a convention change nor the upper bound establishes
the missing inequality.

Here is a direct reconstruction of the obstruction described in the earlier
correction. With the original coordinate-cycle matrix A and diagonal matrix
B=diag(1,w,w²), BA=wAB. Thus the actual inverse image of their projective
group in SU(3) consists of w^t A^a B^b and has multiplication

    (a,b,t)(d,e,s)=(a+d,b+e,t+s+bd), over F3.

This faithful 27-element matrix group H has center and commutator subgroup
equal to the three scalar matrices; H_ab=K=C3². Its universal-cover quotient
SU(3)/H is the actual manifold M=PU(3)/K. In particular it is not appropriate
to replace the extension by an abstract split product. The classifying map
c:M→BK of PU(3)→M factors, up to homotopy, through BH by the quotient
H→K. This follows by taking the universal H-cover SU(3)→M and quotienting
its total space by the scalar center. The induced map on fundamental groups
is exactly H→K, so c* on H¹ with F3 coefficients is an isomorphism.

Let y,y' be the coordinate homomorphisms on K. For the normalized group
cochain f(a,b,t)=t−ab, direct substitution gives

    (δf)(g,h)=f(h)−f(gh)+f(g)=a(g)b(h).

Thus the pullback of yy' to BH, and therefore M, is zero. The mod-three
cohomology of BK is the exterior algebra on y,y' tensored with the polynomial
algebra on their degree-two Bocksteins x,x'. Every degree-seven class has
the form yP₃(x,x')+y'Q₃(x,x'), and its product with any degree-one class is
zero or divisible by yy'. All such pulled-back products vanish.

The manifold M is connected, closed, oriented and real eight-dimensional.
It is the quotient of SU(3) by finitely many right translations; each such
translation is homotopic to the identity in the connected Lie group and
preserves orientation. Poincare duality over F3 gives a nondegenerate pairing
H⁷(M)×H¹(M)→F3. Since c* is onto on H¹, the preceding vanishing forces
c*:H⁷(BK;F3)→H⁷(M;F3) to be zero. This challenges the particular constant-F3
degree-seven nonzero detector in Chen–Wan arXiv2306.17303v2 Proposition4.2(1).
It does not establish that the exact genus is smaller than eight.

The independent finite program checks the actual matrix/group law, all729
cup/coboundary pairs,19683 associativity triples, center/commutators and
coordinate homomorphisms. It rejects the wrong sign, zero primitive and split
group substitutions. These are finite supporting controls. The classifying-map
identification, group-cohomology ring and duality deduction remain mathematical
proof obligations, not machine-certified topology.

A different constant-F3 class in degree seven cannot repair this detector:
the whole map in that degree vanishes. Twisted coefficients, a different
subgroup, a replacement geometric lower bound, or a verified later proof
could be materially new evidence; merely assuming such a detector transfers
the exact lower-bound problem. The route is blocked pending such evidence.
Two fresh independent reviewers are checking the topology and source-version
repair possibilities. The genuine upper bound is useful partial work and
must remain preserved. No lower-bound or final-journal falsity claim is made.

Primary version: https://arxiv.org/abs/2306.17303v2 (official current listing
still v2, dated21July2023). The final 2025 article, DOI10.1090/proc/17184,
must be distinguished from that preprint. An abstract or publication metadata
does not authenticate an unseen final proof. The fresh source family is
investigating normal public access to later versions without outreach.

OpenAI tools were used extensively. No human peer review, formal topology
verification, novelty, or completed full-solution clearance is claimed.
