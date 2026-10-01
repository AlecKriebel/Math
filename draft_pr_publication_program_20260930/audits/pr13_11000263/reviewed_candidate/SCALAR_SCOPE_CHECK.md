# Preliminary scalar route: precise scope and obstruction

This was the sole new proof approach begun before the exact external prior-art
hit. It is retained to account for the attempt honestly, not as a claim of
novelty or a replacement for the full target.

Work over a field of characteristic zero. In any scalar representation of
\(B_n\), all generators have the same nonzero value \(s\): the adjacent braid
relation implies \(s_i^2s_{i+1}=s_{i+1}^2s_i\), and cancellation gives equality.
Let \(x_k\) be the scalar image of \(X_k\). Then

\[
x_2=(1-s)(s+q)/s,
\quad x_3=(q^2s^{-2}-s^2)x_2,
\]

and the first relation reduces to

\[
\frac{(s^2-q)(s^2-s+1)}{s^2}\,x_2=0.
\]

Thus choosing \(s\) to satisfy \(s^2-s+1=0\), with \(q\) transcendental,
gives a scalar witness to \(x_3\ne0\) for the three-strand legal-row
truncation \(A_3\). It proves nothing by itself about additional rows on more
strands.

In fact that route fails in the generic four-strand truncation, and in every
characteristic-zero scalar representation on five or more strands. To see the
latter, suppose \(x_3\ne0\). Then \(x_2\ne0\), \(s\ne1\), and the branch
\(s^2=q\) is impossible because it makes \(x_3=0\). Therefore
\(s^2-s+1=0\), so \(s^3=-1\) and \(s^6=1\). The third-index row becomes

\[
\frac{(s-1)(q^2+s^5)}{s^3}\,x_3=0,
\]

forcing \(q^2=-s^5=s^2\). If \(q=-s\), then \(x_2=0\), a contradiction.
Thus \(q=s\). This is already incompatible with transcendental \(q\).
At that exceptional value the four-strand scalar witness exists, but

\[
x_4=(q^3s^{-3}-s^3)x_3=2x_3\ne0.
\]

The next relation requires

\[
\frac{(s-1)(q^3+s^7)}{s^4}\,x_4=0.
\]

With \(q=s\), its numerator is \((s-1)^2\), which is nonzero. This
contradiction excludes a scalar witness when the fourth-index row is present.

This explains exactly why the small-rank scalar observation cannot be promoted
to an all-strand result. The known Burau representation avoids that obstruction
by being noncommutative.
