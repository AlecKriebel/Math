# Independent algebra and exact-scope audit of PR421

Completed 2026-10-12 UTC. Frozen head:
`d5bf8b5a25cabb177433338fae60af52ebfecf1c`. Assigned-family audit completion:
100%; additional proof attempts: 0.

**PASS within the algebra/topology scope.** The proposed cube complex's actual
two-skeleton has fundamental group exactly

    G=<a,b,c,t | tat^-1=a, tbt^-1=ab, tct^-1=bcb>.

There is a reversible Tietze proof, with no extra relation, missed relation,
finite-index substitution, monodromy power, or stable-letter reversal. The
two maps from Q induce injections, even without using the cubical
local-isometry theorem. The optional ribbon and lifted involution assertions
are correct. No mathematical repair is required by this audit family.

This report does not independently adjudicate the full three-cube incidence
and flag-link certificate. The geometric verdict must combine this algebra
certificate with that separately audited finite geometry and the standard
local-to-global CAT(0) theorem. Source recovery, historical priority, and
publication operations are outside this assigned family.

## Independence and inputs

`INDEPENDENCE_SEAL.md` was saved after reading the applicable instructions,
source receipt, canonical full statement/prior report, and ATTEMPT_1.md, but
before reading historical audit programs, results, AUDIT.md, the addendum, or
peer conclusions. It contains the raw square-boundary derivation and reverse
Tietze reduction. The one minor administrative correction was replacing a
manually estimated future timestamp in the log with an approximate actual
time; the order of the reads is unchanged.

The historical programs were subsequently read in full before execution.
All 13 frozen files were copied and their SHA-256 values matched to the
receipt. Only these isolated copies under
`private_sources/algebra_adversary/historical_execution` were executed.
All three programs returned zero. Regenerated checks.json and the two
independent result JSON files were byte-identical to the frozen records.
These reruns corroborate reproducibility; they do not replace the fresh proof
or fresh controls below.

The checkable new artifacts are `check_exact_algebra.py` and
`exact_algebra_results.json`. The script uses only Python's standard library;
it imports neither an author program nor a historical audit program.

## 1. Exact automorphism and mapping-torus convention

The claim concerns the positive final b, with

    phi(a)=a, phi(b)=ab, phi(c)=bcb.

Its inverse is

    psi(a)=a, psi(b)=a^-1b, psi(c)=b^-1 a c b^-1 a.

For c, applying phi to psi(c) gives

    (b^-1a^-1) a (bcb) (b^-1a^-1) a = c.

Applying psi to phi(c) gives

    (a^-1b)(b^-1 a c b^-1 a)(a^-1b) = c.

Both compositions also fix a and b. Thus these are genuine mutually inverse
free-group automorphisms, not just matrices with determinant one. The fresh
program checks both compositions by free reduction.

The normal form used for arithmetic is f t^n with multiplication

    (f,n)(g,m)=(f phi^n(g), n+m).

It implements precisely t f t^-1=phi(f), including negative powers by psi.
Consequently a nonempty reduced free word in a residual is a falsifiable
failure, rather than an inconclusive nonabelian symbolic expression.

## 2. Q and its two maps

The oriented edges are

    p:B->A (x), q:A->C (y), r:D->C (x), s:B->D (y),
    d:A->B (b), e:C->A (b).

The square boundaries are pq r^-1 s^-1 and dp e^-1 q^-1. The first is
closed through B,A,C,D; the second is closed through A,B,A,C. Repetition of
A in the second boundary is retained in this audit.

The connected three-edge tree p,q,s has all four vertices. Collapsing it
leaves generators r,d,e with relators r^-1 and d e^-1. It follows that
pi_1(Q,A) is infinite cyclic. The based loop dp is a generator. It maps to
bx under j and b^-1y under lambda j; no connecting basepoint path was omitted.

In H=<x,y,b | [x,y]=1, bxb^-1=y>, the map epsilon_b:H->Z sending b to 1 and
x,y to 0 respects both relations. It sends bx to 1 and b^-1y to -1. Both
elements have infinite order, proving injectivity of both homomorphisms
Z=pi_1(Q)->H. It also proves neither generator is a proper power. This
argument does not presuppose CAT(0), convexity, or injective maps of spaces.

For completeness, the raw corner calculation gives link images

    A: b^- -- x^- -- y^+ -- b^+;
    B: b^- -- x^+ -- y^+;
    C: x^- -- y^- -- b^+;
    D: x^+ -- y^-.

In the K-link, each is the full induced subgraph on its vertices, and there
are no duplicate germs or corners. The fresh script reconstructs this from
the Q endpoints and its square words. This independently verifies the
local-isometry input used in the auxiliary convexity claim.

The cubical involution is lambda(x)=y, lambda(y)=x, lambda(b)=b^-1. On the
first base square its boundary becomes yxY X, the reversed boundary. On the
second it becomes B y b X, a cyclic rotation of the reversed boundary. Thus
each target square receives an actual Euclidean square isometry. Their
restrictions agree on the edge cells. Squaring these maps fixes each edge
and each square, so lambda is a cubical isometric involution.

## 3. Van Kampen with nonembedded attaching maps

The quotient K union (Q times [0,1]) is a double mapping cylinder. An end
map can identify distant points without invalidating its CW structure or
van Kampen calculation. An open neighborhood of K with the two end collars,
together with an open middle cylinder, has two intersection components.
Van Kampen with basepoint paths (or its fundamental-groupoid formulation)
introduces one stable edge z_A and one conjugacy relation for each element
of pi_1(Q,A). Since that group is Z, the result is

    <H,z_A | z_A^-1(bx)z_A=b^-1y>.

Injectivity of the two end homomorphisms makes this an actual HNN extension.
Injectivity is not needed to obtain the quotient presentation itself.

The product-square calculation in the next section independently removes
any reliance on that graph-of-spaces statement. In particular it checks the
based paths, vertical orientation, and all six edge-cylinder relations.
Attaching the two three-cells cannot change fundamental group: fundamental
group is determined by the two-skeleton.

## 4. Seven generators and eight actual square relations

Write z,w,k,l for vertical edges at A,B,C,D, each from the j end to the
lambda j end. For an edge h:V->W, the product square has oriented boundary

    h z_W lambda(h)^-1 z_V^-1.

This gives the two base relators and six additional relators

    xyXY, bxBY,
    xzYW, ykXZ, xkYL, ylXW, bwbZ, bzbK.

Uppercase letters denote inverse generators. The presentation is exactly
seven generators and eight relators before elimination.

The p,q,r relations eliminate w,k,l by

    w=x z y^-1,
    k=y^-1 z x,
    l=x y^-1 z x y^-1.

The s relation becomes y l x^-1=w. Its left side simplifies using [x,y]=1:

    y x y^-1 z x y^-1 x^-1 = x z y^-1 = w.

The d relation is b w b=z, or

    b x z y^-1 b=z
    <=> z^-1 b x z=b^-1y.

The e relation is b z b=k=y^-1 z x, or

    y b z b=z x
    <=> z^-1 y b z=x b^-1.

From bxb^-1=y we have yb=bx and b^-1y=xb^-1. Thus the e relation is exactly
the d relation, not an additional restriction. The reduced presentation is

    P=<x,y,b,z | [x,y]=1, bxb^-1=y, z^-1(bx)z=b^-1y>.

Conversely, in P define w,k,l by the displayed expressions. The p,q,r
relations then hold by definition; s holds by commutation; d holds by the
top relation; e holds by the two base identities. All eight raw relators
are recovered. This proves a reversible Tietze equivalence, including the
direction that forward numerical or word checks alone could not prove.

## 5. Reversible identification with the target

Put

    t=x, a=x y^-1, c=(zx)^-1;
    x=t, y=a^-1t, z=c^-1t^-1.

These changes are inverse already in the corresponding free groups. The
fresh program checks both four-generator free-basis round trips.

The relation [x,y]=1 becomes [a,t]=1. The other base relation becomes

    b t b^-1=a^-1t
    <=> b t=a^-1 t b
    <=> a b t=t b
    <=> t b t^-1=a b.

Every step is reversible. For the top relation put u=b^-1x and v=bx.
The base relation gives b^-1y=xb^-1=xu x^-1. Hence

    z^-1 v z=x u x^-1
    <=> (zx)u(zx)^-1=v
    <=> c^-1(b^-1t)c=bt
    <=> b^-1 t c=c b t
    <=> t c t^-1=b c b.

This completes both directions of the isomorphism pi_1(Z)=G.
In the new normal forms, x=t, y=a^-1t, z=c^-1t^-1, and the solved vertical
generators evaluate to

    z=(c^-1,-1),
    w=(b^-1 c^-1 b^-1 a,-1),
    k=(b c^-1 a^-1 b,-1),
    l=(a c^-1 a,-1).

The fresh script evaluates every one of the actual eight square words to
identity, then recovers a,b,c,t exactly. Its use of t rather than t^k is
literal. The quotient group is G itself. There is no passage to a cover,
subgroup, rational change of basis, or different monodromy.

## 6. Controls that detect nearby groups and convention errors

The fresh controls change substantive features and evaluate them in exact
normal forms. All behave as required:

- Changing phi(c) to b c b^-1, with its own verified inverse, makes the d
  product relation evaluate to b^2 and the e relation to b a^-1 b a^-1.
- Changing phi(b) to aba, with its own verified inverse, makes the base
  annulus evaluate to b a^-1 b^-1; the d and e relations also fail.
- Changing the generator assignment to c=(xz)^-1, so z=t^-1c^-1, makes the
  HNN relator evaluate to c a c^-1 b^-1 a b, a nonempty free word.
- Changing lambda(b)=b^-1 to lambda(b)=b makes the second base-square image
  fail its actual cubical attaching-word test.

The nearby groups are not merely different presentations of the same group.
Their abelianizations, computed directly from exponent rows, are

    ab,bcb target: Z^2 direct-sum Z/2;
    ab,bcB mutant: Z^3;
    aba,bcb workshop variant: Z^2 direct-sum (Z/2)^2.

These invariants distinguish the groups, not only their chosen basis maps.
The workshop variant cannot be silently transferred to this target.

## 7. Auxiliary ribbon, convexity, and isometry

These optional assertions are not needed for the fundamental-group proof.
They nevertheless pass this audit.

Since the Q link maps are full and injective, Q is locally CAT(0) and j is
a cubical local isometry. The lifted map from its CAT(0) universal cover to
the CAT(0) universal cover X of K is a global isometric embedding: a domain
geodesic maps to a local geodesic and hence to a geodesic in X. Uniqueness of
geodesics proves the image is convex. The image is a cubical subcomplex,
invariant under <bx>, with compact quotient Q. This justifies convexity
without an assumption that an unspecified convex hull is cocompact.

Writing v=bx and A_i=v^i, its other vertices are

    B_i=v^i x^-1, C_i=v^i y, D_i=v^i x^-1y.

The flat square is B_i,A_i,C_i,D_i. The annulus square is
A_i,B_(i+1),A_(i+1),C_i, because

    v^i b=v^(i+1)x^-1,
    v^i yb=v^(i+1).

Thus the claimed right-side to next-bottom-side ribbon is the lifted Q
itself. It is two squares per cyclic period. Its periodic gluing graph is
an infinite line, so it is the universal cover, rather than an unverified
finite subcomplex pictured inside X.

Let Lambda be the lift of lambda fixing the identity vertex, and let L_h
denote left deck multiplication by h. Lambda L_h Lambda^-1=L_lambda(h),
and Lambda^2=1. The claimed f is L_(b^-1) Lambda. Then

    f^2=L_(b^-1 lambda(b^-1))=1,
    f L_u f^-1=L_(b^-1 lambda(u)b)=L_(yb)=L_v,

where u=b^-1x. This is an identity among ambient isometries. The notation
f u f^-1 in the candidate must be understood in that sense; f is not being
asserted to be an element of H. This interpretation is consistent with the
candidate's stated lift and isometry construction.

## 8. Historical comparison and strongest result

The later reading of AUDIT.md found the same raw square relations and
reversible target identification, using p,q,s rather than p,q,r for the
vertical elimination. That alternate tree choice gives l=y^-1 x z y^-1 x;
it agrees with the fresh expression by [x,y]=1. Historical algebra normal
forms agree exactly. Its written warning that forward word evaluation alone
does not prove an isomorphism is correct and is met by both two-way proofs.

The fresh audit adds discriminating controls for the final inverse b, the
workshop aba monodromy, and the order of zx in c. No substantive mathematical
failure or correction was found. The historical addendum's claim of no
algebraic repair is corroborated. Its complete geometric PASS is left for
the independent geometry family; historical source and novelty claims are
not inherited by this report.

Strongest verified result: the actual finite quotient has fundamental group
exactly the canonical G; Q is cyclic with two injective edge maps; the
generator and stable-letter signs, and the optional ribbon/isometry, are
correct. Exact remaining gap for promoting the global result: combine this
with the independent audit of Z's cube face/corner incidences and flagness.
There is no unresolved central difficulty within this algebraic route.
