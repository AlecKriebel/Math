# Local-count augmented two-point search

This experiment asks whether the exact local theorem

\[
\#\{j\ne i:\langle x_i,x_j\rangle\ge 1/4\}\le 23
\]

can strengthen an ordinary Schoenberg/Delsarte polynomial enough to exclude
41 points.

For a polynomial \(f=\sum_k a_kP_k^{(5)}\), \(a_0=1\), \(a_k\ge0\), and
numbers \(L\le H\) satisfying

\[
f(t)\le L\quad(-1\le t<1/4),\qquad
f(t)\le H\quad(1/4\le t\le1/2),
\]

every 41-point code would obey

\[
41\le f(1)+17L+23H.
\]

The search program only discretizes the two intervals and is therefore
discovery code.  Any promising result must be converted to an exact
full-interval polynomial certificate.

## First result

Dense-grid runs at degrees \(12,16,20,24,30,36,44\) all return the
constant polynomial \(f=1\), with objective \(41\) to solver precision.
The same happens after adding nested projected-code count bounds at heights
\(1/4,3/10,1/3,3/8,2/5,9/20,1/2\).  Thus this scalar augmentation provides
no numerical indication of a strict bound.  This is evidence about the
specified LP only, not an exact dual-optimality proof.
