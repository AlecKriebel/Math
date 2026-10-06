# Semilinear dual-kernel formula and regression controls

This corrects a supporting computational helper. The main manuscript's symbolic
Cartier-duality obstruction, elliptic filtration and Honda lift are unchanged.
Historical original audit controls and adverse-review evidence are preserved;
`SOURCE_IDENTITY.json` records the exact corrected public derivation.

Let k be a perfect field with Frobenius sigma. Write F(x)=A sigma(x) and
V(x)=B sigma^-1(x), using column coordinates. Set

    C = A sigma(A),     D = B sigma^-1(B).

Thus F^2(x)=C sigma^2(x) and V^2(x)=D sigma^-2(x). Evaluation duality gives
Fdual(phi)(x)=sigma(phi(V(x))) and Vdual(phi)(x)=sigma^-1(phi(F(x))). Its
first matrices are sigma(B)^T and sigma^-1(A)^T. Its second matrices are

    Fdual^2: sigma^2(D)^T,     Vdual^2: sigma^-2(C)^T.

Consequently the dimension of their image intersection is

    rank(C) + rank(D)
      - rank([ sigma^2(D)^T | sigma^-2(C)^T ]).

The actual semilinear kernels are sigma^-2 ker(C) and sigma^2 ker(D).
Taking their annihilators gives the same expression, or equivalently

    dim(M) - dim(ker(F^2) + ker(V^2)).

These statements hold without assuming Frobenius has finite order. Applying
an automorphism preserves a single rank, but it does not preserve a union of
two row spaces when different automorphisms are applied. The previous generic
helper incorrectly replaced the displayed union with `[C^T | D^T]`.

For a concrete counterexample, take k=F5[t]/(t^3+t+1). The cubic has no F5
root and is irreducible. Let A0,B0 be the manuscript's six-dimensional matrices,
so their squares are E20 and E40 (zero-based indices). Change coordinates by
P=I+t E01:

    A = P^-1 A0 sigma(P),     B = P^-1 B0 sigma^-1(P).
    C = e2 (e0^T + t^25 e1^T),
    D = e4 (e0^T + t^5  e1^T).

Here t^25 differs from t^5. The untwisted row lines therefore differ, giving
0 for the old expression. Applying the opposite squared twists makes both
row lines `e0^T+t e1^T`, giving the correct value1. Direct computation of the
dual operators and of the actual semilinear kernel spaces also gives1. The
original module's image intersection has dimension0, as in the manuscript.

The corrected intrinsic control checks minimal, dense upper-triangular and
dense lower-triangular coordinate changes over F125, F343 and F32. It checks
inverses, basis invariance, equality with the direct dual calculation, and
actual kernel bases obtained by elimination with their scalar twists. Each
minimal and dense upper-triangular case rejects the old bare-row expression.
The F32 sample, of Frobenius order five, tests only the generic linear-algebra
formula; it does not extend the group-scheme theorem's p>3 range. These finite
controls supplement the symbolic derivation, not prove universality.
