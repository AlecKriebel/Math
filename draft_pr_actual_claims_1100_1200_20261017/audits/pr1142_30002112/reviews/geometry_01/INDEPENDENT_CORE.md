# Independent geometry core, locked before prior-audit exposure

Recorded 2026-10-17 23:15:30 UTC. Review target: PR 1142, head
`c29139d2c2a98f1a0284d0dc794c88f51c680a0c`, problem 30002112 /
OWR-12005-004. The exact base proof has SHA-256
`c4608dbf5f9e39b398f7db20100273fdab085598382293f8224488585015f658`.

## Exposure and order

I was assigned the proposed route and intended full negative claim by the
parent; independence does not extend to route discovery. I read the complete
base PROOF.md and SOURCE_DEPENDENCIES.json, then freshly retrieved CDE
arXiv:0909.5346v1 and the De Lellis-Szekelyhidi author PDF. Before writing
this core I inspected CDE Theorem 1.4 (printed p. 6), the complete Section 5
(printed pp. 14-15), the connected/closed/indexing convention (printed p. 1),
and DLS Definition 1.1/Theorem 1.2 with immediate context (printed pp. 2-4).
I visually inspected rendered CDE pp. 6, 14, 15 and DLS p. 4.

The filenames of prior audit/status material were incidentally listed by a
directory inventory. None of their contents was opened. The base PROOF.md
itself contains a sentence announcing an old internal acceptance, and its
dependency JSON reports old inspection limits; these sentences were exposed
but are not evidence for this review. No root/concurrent review reports,
AUDIT.md, ACCEPTANCE.md, STATUS files, or VERIFICATION_SUMMARY.md were read.

## Source check

CDE's ambient codimension in Theorem 1.4(2) may be chosen to be one and its
manifold may be chosen to be the standard smooth sphere for every m >= 3.
Part (1) provides the required embedded orientable surface sequence for m=2;
the paper's convention is connected and without boundary. Its Section 5
explicitly makes the dimension-two large-genus distinction and passes from
C1 embeddings to smooth embeddings by C1 approximation. This is the exact
established result needed; I have not reproved its cited large-eigenvalue
metric theorems.

DLS Theorem 1.2 applies to a smooth closed n-manifold, a smooth short
immersion, and every ambient N >= n+1; it provides arbitrarily small C0
error and expressly retains embedding when the initial map is an embedding.
Thus the codimension-one embedding conclusion is not being inferred from
an immersion-only theorem. Strictly short is stronger than its hypothesis.

## Universal core reconstructed independently

Fix m >= 2 and S,L,r > 0. CDE supplies a smooth connected closed
hypersurface metric with lambda_firstpositive * area^(2/m) >
2 L S^(2/m). Rescale this intrinsic metric to g of area S. Then
lambda_firstpositive(g) > 2L. Its underlying smooth manifold already
admits a codimension-one smooth embedding e0.

Let K = max_{g-unit tangent vectors} |de0(v)|^2 and
R = max_M |e0|. Both are finite; K > 0. Choose t > 0 with
t^2 K < 1 and tR < r/8. Scaling e0 by t preserves embedding and gives
e^*e_Eucl < g, e(M) contained in B(0,r/8). DLS with C0 error less
than r/8 gives a C1 isometric embedding f in B(0,r/4).

Smooth maps are C1 dense in C1 maps on a compact smooth manifold.
Embeddings of a compact manifold form a C1-open set: near each point use
an injective linear projection of df and uniform derivative control on a
smaller coordinate ball to obtain injectivity for nearby pairs; a finite
cover/Lebesgue number handles all sufficiently close pairs. On the remaining
compact set of separated pairs, |f(x)-f(y)| has a positive minimum, and
C0-small perturbations preserve separation. The positive least singular
value of df on finitely many charts also preserves immersion. Therefore
smooth approximants f_j can be chosen to be embeddings. Uniform derivative
convergence gives h_j=f_j^*e_Eucl -> f^*e_Eucl=g as quadratic forms.

For c^-1 g <= h <= c g, the volume ratios lie between c^(-m/2)
and c^(m/2). The energy density ratios lie between c^(-1-m/2)
and c^(1+m/2), so Rayleigh quotients lie between c^(-m-1)
and c^(m+1). All eigenvalues, zeros included, obey these inequalities by
min-max on the SAME full H1 space. One must not use a fixed metric-dependent
mean-zero subspace. Uniform equivalence identifies H1 spaces and uniform
metric convergence permits c -> 1. This proves volume and fixed-index
eigenvalue continuity without defining a differential operator on a rough
embedded image.

Writing S_j=area(h_j) and a_j=(S/S_j)^(1/m), the corrected smooth
embedding a_j f_j has exact area S. Also

    c^(-1/2) <= a_j <= c^(1/2),
    c^(-m-2) lambda(g) <= lambda(a_j^2 h_j)
                             <= c^(m+2) lambda(g).

Choose c close enough to one that c^(m+2)<2. Since the original gap
exceeds 2L, a sufficiently accurate smooth approximant has corrected gap
greater than L. Since f_j(M) lies in B(0,r/3) and a_j -> 1, choose
the same j sufficiently large that a_j<2. This puts the corrected image
inside B(0,2r/3), hence inside B(0,r). All tolerances are for a single
fixed m,S,L,r and may deteriorate with them; no uniform j is required.

Every final H is smooth, compact, connected, embedded, and closed.
There is no C2 closeness or curvature bound, so high smooth curvature is
allowed. The orientable m=2 surfaces embed as ordinary closed orientable
surfaces; m>=3 can use S^m. No prohibited nonorientable codimension-one
closed embedding is needed. The general smooth Jordan-Brouwer separation
theorem gives exactly the bounded inside and unbounded outside, both with
boundary H. Since H is inside B(0,r), every point of norm at least r can
reach infinity without meeting H, so the bounded component is inside that
ball as well.

## Initial assessment and exact remaining work

The prescribed-small-ball/exact-area/arbitrarily-large-gap lemma survives
the attempted falsification. No mathematical defect found in this core.
This is not acceptance of historical novelty or of the exact original
problem-scope gate. Remaining review work: exact algebra diagnostics,
write a complete adversarial report, seal exposure/source/artifact receipts.
No numerical construction of a Nash embedding is needed or claimed.

Best-guess completion: 70% of this assigned geometry review, 0% judgment
about originality. This file is not a prior-audit comparison.
