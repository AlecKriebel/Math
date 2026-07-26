# Root probe log — `D4-DN-3` lower descent

## 2026-07-26T05:07:00Z — both plane interiors provisionally excluded

Starting from the certified all-18-variable \(E_6\) atlas, solve the
seven-pivot system on
\[
\Pi_+:\quad
(a,b,x,y)=
\left(k,k,s+\frac{-4+2\sqrt2}{3}k,s\right),
\qquad k\ne0.
\]
All eleven unpivoted \(E_6\) variables remain free.  Four coefficients of
\(E_5\) are nevertheless independent of every lower coefficient.  The two
extreme ones are
\[
\begin{aligned}
[p^3r^2]E_5
 &=3(\sqrt2-2)k
   \left(s+\frac{-4+2\sqrt2}{3}k\right)^2,\\
[q^3r^2]E_5
 &=3(\sqrt2-2)k
   \left(s-\frac43k\right)^2.
\end{aligned}
\]
In characteristic zero, with \(k\ne0\), they force
\[
s=\frac{4-2\sqrt2}{3}k
\quad\text{and}\quad
s=\frac43k,
\]
which are incompatible.  Galois conjugation gives the identical
exclusion on \(\Pi_-\).

This is an exact candidate exclusion of the two plane interiors only.
It is not yet independently verified.  It does not cover the punctured
intersection \(k=0,s\ne0\) or the origin, and therefore does not yet
exclude `D4-DN-3`.

The exact reconstruction is
`explore_root_lower_descent.py`; its marker is
`D4_DN3_PLUS_INTERIOR_E5_EXCLUDED`.
