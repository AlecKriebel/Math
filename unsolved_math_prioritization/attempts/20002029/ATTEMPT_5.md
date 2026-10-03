# Attempt 5: the general restriction strategy and a concrete dimension-eight blind spot

## Target and outcome

Try to extend the successful dimension-six Ricci-flat evaluation argument to every even critical dimension. This attempt identifies a sufficient injectivity theorem that is not proved here, and proves that the entire diagonal-curvature/Kasner test family already misses a nonzero critical conformal invariant in dimension eight. Consequently, merely adding more Kasner examples cannot certify the full higher-dimensional problem.

This is mathematical progress on the proposed method, not a resolution of AIM Problem 10. The general n>=8 statement remains unproved.

## The restriction strategy and its exact logical strength

Let V_n be the finite-dimensional space of metric-contracted scalar conformal invariants of weight -n. By FG Theorem 9.4 it is spanned by ambient curvature contractions. Restrict such invariants to all actual Ricci-flat n-dimensional metrics:

    R_n : V_n -> functions on Ricci-flat metric germs.

Any invariant having a pure-Schouten-jet formula belongs to ker R_n, because P and all its derivatives vanish identically on those germs. Therefore injectivity of R_n would prove the desired nonexistence.

The converse has not been established: a nonzero invariant in ker R_n would not automatically admit a pure-Schouten representative. Thus this is a sufficient route, not an equivalence or a replacement formulation of the original question. Attempt 3 proves the required injectivity for n=6 by an explicit nonsingular matrix; it does not establish a general principle.

## Why a tempting stable-range argument is incomplete

An ambient contraction of L curvature factors with a total of r derivatives has weight -2L-r. At critical weight its total number of covariant slots is 4L+r=n+2L<=2n. This suggests using stable-range orthogonal invariant theory to exclude dimension-dependent relations when restricting from ambient dimension n+2 to dimension n.

However, that count alone does not prove injectivity on Ricci-flat germs. One must control the differential Bianchi identities, nonlinear derivative-commutator identities, the Ricci-flat differential ideal, finite-jet extendability, and the ambient homogeneity constraints simultaneously. Ordinary invariant theory on unconstrained tensor variables does not by itself supply those facts. No valid theorem or complete proof bridging all these steps has been established in this attempt. Treating arbitrary trace-free tensors as freely realizable Ricci-flat curvature jets would repeat the same kind of compatibility error that invalidates unrestricted Schouten-jet normalization.

## A nonzero invariant missed by all diagonal-curvature metrics

For a Weyl tensor W, define the alternating four-tensor

    Q_ijkl = g^ac g^bd [W_abij W_cdkl
                         -W_abik W_cdjl
                         +W_abil W_cdjk].                (5.1)

This is a fixed nonzero normalization of the first Pontryagin four-form. The formula is alternating because it is half the sum of the wedge squares of the curvature two-forms. The all-covariant Weyl tensor transforms by W_hat=e^(2u)W, whereas the two inverse metrics contribute e^(-4u); hence Q_hat=Q. Its squared norm

    H=|Q|^2=(1/4!) Q_ijkl Q^ijkl                         (5.2)

is therefore a scalar conformal invariant of weight -8. It is orientation-even and is a linear combination of complete metric contractions of four Weyl tensors. It is in the same parity sector as the original problem, even though its construction uses a differential four-form.

If curvature is diagonal in an orthonormal basis,

    W_abij=K_ab(delta_ai delta_bj-delta_aj delta_bi),

then for each fixed a,b the two-form W_abij is a multiple of the simple form e^a wedge e^b. Its wedge square is zero. Every term in (5.1) therefore vanishes. In particular H=0 on every Ricci-flat Kasner metric, in every dimension, regardless of the exponent choice. This is an identity on the whole family, not a numerical observation.

## Explicit nonvanishing certificate in dimension eight

On the first four coordinates of Euclidean R^8, put

    omega1=e1 wedge e2+e3 wedge e4,
    omega2=e1 wedge e3-e2 wedge e4,
    omega3=e1 wedge e4+e2 wedge e3,

and set

    W_ijkl=omega1_ij omega1_kl
             +omega2_ij omega2_kl-2 omega3_ij omega3_kl,

with all components involving coordinates 5 through 8 zero. This is an algebraic Weyl tensor: skew symmetry, pair exchange, first Bianchi and trace-freeness can be checked directly; the trace/Bianchi cancellations use 1+1-2=0. Formula (5.1) gives

    Q_1234=24,
    H=576.

Thus H is not the zero polynomial. The ordinary Riemannian curvature jet realization theorem (FG Theorem 8.3 at order zero) realizes this algebraic Weyl tensor as the curvature at a point of a local positive-definite metric, so H is a genuinely nonzero scalar conformal invariant. This last realization is only an unconstrained order-zero metric jet; no Ricci-flat germ realization is needed or claimed.

The rational/integer check verifies every curvature symmetry, every Ricci trace, all independent Q components, and H=576. This is a check of the explicit certificate, not a classification.

## Consequence for extending Attempt 3

In any spanning basis of V_8, the nonzero vector H is annihilated by every evaluation on every Kasner metric. Hence no number of exclusively Kasner/diagonal-curvature tests can yield an injective evaluation matrix for V_8. One needs a richer family with non-diagonal curvature, or a justified general restriction theorem, together with a complete classification/spanning set and a verified full-rank certificate.

H is NOT presented as a counterexample to the original problem: it has not been given a Schouten-only formula, and vanishing on the Kasner family is much weaker than vanishing on every Ricci-flat metric. Its role is to certify a genuine blind spot in the proposed proof method.

## Final mathematical status after five substantive attempts

- The known n=4 answer is recorded in the original source.
- Attempt 3 establishes n=6 using classical classification and explicit Ricci-flat witnesses, subject to fresh review and with no novelty claim.
- Attempts 1 and 2 eliminate useful sectors in all dimensions.
- Attempt 4 excludes the complete span of the two explicit Case et al. dimension-eight divergence examples from the pure-Schouten class.
- The original general assertion for even n>=8 remains unresolved here. No general Ricci-flat restriction injectivity theorem, complete n=8 calculation, or counterexample was obtained.

Primary background: Fefferman–Graham, The Ambient Metric, Theorems 8.3, 9.3 and 9.4; https://arxiv.org/abs/0710.0919. Reproduce the explicit blind-spot certificate with python checks/verify_kasner_blindspot.py.
