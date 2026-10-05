# Exact scope and elementary controls

## 1. The quantified target

Let \(\mathbb D=\{z\in\mathbb C:|z|<1\}\), let
\(\Lambda_0=\mathbb Z+e^{i\pi/3}\mathbb Z\), and let
\(L=b+c\Lambda_0\), where \(b\in\mathbb C\) and \(c\ne0\).
The analytic function under consideration is a holomorphic universal covering
projection \(f:\mathbb D\to\mathbb C\setminus L\). Equivalently, the disk
uniformizes the universal covering surface and \(f\) is its planar projection.
In particular, it is surjective and locally biholomorphic. An arbitrary
holomorphic map whose range merely avoids \(L\), or even an arbitrary
surjection, is not the specified function class.

Write its ordinary Taylor expansion at the disk origin as
\(f(z)=\sum_{n=0}^{\infty}a_nz^n\). The question is whether, for every
such fixed covering map and lattice, \(a_n\to0\) as the integer \(n\to\infty\).
The source's affirmative update supplies the more precise asymptotic
\(|a_n|\le C/\sqrt{\log n}\) for \(n\ge N\), with \(C,N\) allowed to depend
on the fixed map and lattice. It does not supply a common constant for all
lattices, all basepoints, and all covering maps. No explicit optimal constant
or optimal decay rate is asserted here.

There is no prescribed normalization \(f(0)=0\) or \(f'(0)=1\) in the problem.
Indeed, \(f(0)\notin L\) and \(f'(0)\ne0\). In the standard lattice
\(\Lambda_0\), zero is excluded, so a normalization \(f(0)=0\) would be
inconsistent. Rotating the source can set the derivative's phase, but not
arbitrarily set its magnitude while fixing the lattice and basepoint.

## 2. Consequence of the imported historical estimate

Assume the credited estimate in section 1. Given \(\varepsilon>0\), choose
an integer \(n\) larger than both \(N\) and
\(\exp((2C/\varepsilon)^2)\). Then
\(|a_n|<\varepsilon/2<\varepsilon\). Thus \(a_n\to0\).
This elementary implication is complete. The difficult logarithmic estimate
is imported from the explicitly credited literature and is not proved here.

## 3. Similarities and source rotations

For \(g(z)=(f(z)-b)/c\), the target becomes
\(\mathbb C\setminus\Lambda_0\), and
\([z^n]g=a_n/c\) for every \(n\ge1\). Translation changes only the
constant coefficient. Conversely, \(b+cg\) recovers the original cover.
Consequently coefficient decay, and a fixed-map big-O rate, transfer under
target similarities. This follows directly by substituting Taylor series.

For a source rotation \(u\) with \(|u|=1\),
\([z^n]f(uz)=u^na_n\), so coefficient moduli are unchanged.

More general disk automorphisms also produce covering maps, but do not
transform coefficients by this diagonal formula. Their membership in the
problem's class follows from composition of covering isomorphisms. Applying
the source's assertion to each resulting covering map is legitimate; a
general coefficient-decay preservation theorem for arbitrary holomorphic
compositions is not being assumed.

No single pair \(C,N\) can give the above estimate uniformly over every
similarity scale. A universal covering map is unbounded because its range
is the unbounded domain \(\mathbb C\setminus L\). Hence it cannot be a
polynomial, since a polynomial is bounded on the disk. It therefore has
nonzero coefficients of arbitrarily large index. For any proposed common
\(C,N\), choose \(n\ge\max(N,2)\) with \(a_n\ne0\), and then scale
the map and lattice by a factor larger than
\(C/(|a_n|\sqrt{\log n})\). The proposed bound fails at that index.

## 4. Why bounded-function arguments do not settle this target

If an analytic function \(h(z)=\sum b_nz^n\) obeys \(|h|\le M\) on
the disk, orthogonality on a circle of radius \(r<1\) gives
\(\sum |b_n|^2r^{2n}\le M^2\). Fixing any finite partial sum and then
letting \(r\uparrow1\) shows \(\sum |b_n|^2\le M^2\). Therefore
\(b_n\to0\). However a covering map in section 1 is unbounded by its
surjectivity, so this proof's hypothesis is unavailable. Replacing the
universal covering projection by a bounded map changes the problem.

## 5. A complete negative control against a generic Bloch shortcut

The function \(h(z)=\sum_{k=0}^{\infty}z^{2^k}\) is analytic on
\(\mathbb D\), since its series and derivative converge uniformly on
each smaller closed disk. Its Taylor coefficients at \(n=2^k\) are 1,
so its coefficients do not tend to zero.

Nevertheless it is a Bloch function: \(\sup_{z\in\mathbb D}
(1-|z|^2)|h'(z)|<\infty\). For \(0\le r\le1/2\),
\(|h'(z)|\le\sum_{m=1}^{\infty}mr^{m-1}=(1-r)^{-2}\le4\).
For \(1/2<r<1\), put \(t=-\log r>0\). For every \(x=2^k\),

\[
xe^{-tx}\le2\int_{x/2}^{x}e^{-ts}\,ds.
\]

The dyadic intervals partition \([1/2,\infty)\), so
\(\sum_{k\ge0}2^ke^{-t2^k}\le2e^{-t/2}/t\le2/t\).
It follows that \(|h'(z)|\le2/(rt)\le4/t\). Since
\(1-r^2\le2(1-r)\le2t\), its Bloch seminorm is at most 8.
Thus being analytic and Bloch alone does not prove coefficient decay.

This is only a control for an invalid generalized argument. No claim is made
that this lacunary function omits the triangular lattice or is its universal
covering map; it is not a counterexample to Problem 5.33.

## 6. Boundaries of the conclusion

The universal-cover hypothesis cannot simply be removed by invoking
subordination. The neighboring source discussions distinguish universal
covering projections from arbitrary maps into an omitted-value domain.
This packet does not settle the general omitted-values classification,
prove decay for arbitrary subordinates, or claim that an average of squared
coefficients automatically controls every coefficient.

The published rate is used as a reported theorem. No assertion about the
1977 proof's internal hypotheses, theorem numbering, detailed spectral
argument, constants, or the exact improvement in the 1978 sequel is made
without full-text access.
