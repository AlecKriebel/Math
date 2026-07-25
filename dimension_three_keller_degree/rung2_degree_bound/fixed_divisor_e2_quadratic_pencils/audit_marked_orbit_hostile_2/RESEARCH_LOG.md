# Clean-room research log: marked quadratic-pencil companion orbits

## 2026-07-25T23:21:44Z — independent derivation sealed before candidate access

### Independence boundary

At this timestamp I have **not opened or read any file** below either

```text
fixed_divisor_e2_quadratic_pencils/audit_marked_orbit_reconstruction/
fixed_divisor_e2_quadratic_pencils/marked_h_distinct/
```

I also have not read the top-level candidate `NOTE.md`, verification note,
or discovery scripts in `fixed_divisor_e2_quadratic_pencils/` during this
audit.  Before this seal I read only the frozen row label and invariant
tuple in `FROZEN_TAXONOMY_v1.md` / `FROZEN_MANIFEST_v1.json`, plus the
intrinsic object stated in the audit assignment:

- a minimal ternary quadratic pencil \(V\);
- its unique double-line point \([s]\);
- the marked component-gcd point \([h]\ne[s]\); and
- a normal companion point \([g]\in\mathbb P(V)\).

The assignment itself disclosed the candidate answer ("two discrete
three-orbit pair types plus one \(\mathbb P^1\) family"), so this is not a
blind audit.  The action and orbit calculations below were nevertheless
derived without candidate formulas.

### 1. Intrinsic action, including translations and target changes

Let \(U=\mathbb C^3\) be the source linear-form space and
\(V\subset\operatorname{Sym}^2U^*\) the pencil.  Write the unique
double-line member as
\[
s=\ell^2.
\]
On the all-vertical top kernel the normal cubic has the intrinsic form
\[
G_3=\ell g,\qquad 0\ne g\in V.
\]

An affine source change \(X\mapsto TX+a\) has the following effect on
homogeneous pieces:

- \(H_4\) changes only by \(T^*H_4\); the translation \(a\) contributes
  nothing to degree four.
- The translation contributes the directional derivative
  \(dH_4(TX)[a]\) to degree three.  In leading normal form the third target
  component of \(H_4\) is zero, so the third component of this derivative
  is also zero.
- Therefore the normal cubic changes only by
  \(G_3\mapsto c\,T^*G_3\) after the target normalization, for a nonzero
  scalar \(c\).  In particular, source translations do not translate or
  shear the point \([g]\).

For an arbitrary invertible affine target change, target translation
affects only the constant term.  Its linear part acts as follows.  The two
leading target components span a two-plane.  Because the leading rank is
two, its annihilator in the dual target is one-dimensional.  Any target
change that returns to a normal form with third leading component zero
must use this same annihilator for its third row, up to a scalar.  Hence:

- \(\operatorname{GL}_2\) on the first two target rows changes only the
  chosen basis of \(V\);
- adding the third target row to the first two changes lower gauges but
  not \(G_3\);
- adding a nonzero first/second leading row to the third is incompatible
  with a zero third leading component; and
- the third normal cubic is only rescaled.

Thus target changes do not move \([g]\) relative to the intrinsic marked
points \([s]\) and \([h]\).  A simultaneous basis change on \(V\) changes
all projective coordinates together and preserves their cross-ratio.

Consequently the actual orbit problem is:
\[
(V,[s],[h],[g])/\operatorname{GL}(U),
\]
where the roles of \(s\) (unique double line) and \(h\) (component gcd) are
marked and cannot be permuted.

### 2. The two unmarked pencils and the three marked-pair orbits

After sending \(\ell\) to \(x\), the relevant minimal pencils with a unique
double-line member have the two forms
\[
V_{\mathrm{red}}=\langle x^2,yz\rangle,\qquad
V_{\mathrm{sm}}=\langle x^2,y^2+xz\rangle.
\]
The determinant divisors of their general members are, up to nonzero
constants,
\[
\det(a x^2+b yz)=-ab^2,\qquad
\det(a x^2+b(y^2+xz))=-b^3.
\]
For \(V_{\mathrm{red}}\), \([x^2]\) is the unique rank-one point and
\([yz]\) is a second singular point of a different multiplicity.  The
induced group on \(\mathbb P(V_{\mathrm{red}})\) fixes both and contains
all scalings.  Indeed,
\[
x\mapsto \alpha x,\quad y\mapsto\beta y,\quad
z\mapsto\gamma z
\]
(and optionally \(y\leftrightarrow z\)) sends
\[
[a:b]\longmapsto[\alpha^2a:\beta\gamma b],
\]
so the ratio \(\beta\gamma/\alpha^2\) is arbitrary in
\(\mathbb C^\times\).

It follows that a marked point \([h]\ne[x^2]\) has two orbits:
\[
\begin{array}{c|c}
\mathrm{R0}&(s,h)=(x^2,yz),\\
\mathrm{R1}&(s,h)=(x^2,x^2+yz).
\end{array}
\]

For \(V_{\mathrm{sm}}\), write a nonsingular member as
\[
u x^2+(y^2+xz),\qquad u\in\mathbb A^1.
\]
The source shear \(z\mapsto z+t x\) acts by \(u\mapsto u+t\), while
relative scaling of \(x\) against \(y,z\) acts by \(u\mapsto\lambda u\).
Thus the induced group is the full affine group on the complement of the
unique singular point \([x^2]\), and it is transitive there.  The third
marked-pair orbit is
\[
\mathrm{S0}:\qquad(s,h)=(x^2,y^2+xz).
\]

The determinant divisors distinguish \(V_{\mathrm{red}}\) and
\(V_{\mathrm{sm}}\), and within \(V_{\mathrm{red}}\) they distinguish
\(\mathrm{R0}\) from \(\mathrm{R1}\).  Hence these three marked-pair
orbits cannot merge.

### 3. Companion orbits on each marked pair

Use the following projective coordinates.

#### R0: \((s,h)=(x^2,yz)\)

The residual induced group is
\[
[a:b]\mapsto[a:\lambda b],\qquad\lambda\in\mathbb C^\times.
\]
It has exactly three companion orbits:
\[
[g]=[x^2],\qquad [g]=[yz],\qquad
[g]=[x^2+yz].
\]
These are respectively the unique double-line point, the other singular
point, and the nonsingular complement.

#### R1: \((s,h)=(x^2,x^2+yz)\)

Any source transformation preserving \(s\) and \(h\) acts trivially on
\(\mathbb P(V_{\mathrm{red}})\).  To see this without assuming a diagonal
form, write \(T^*x=\alpha x\) and suppose
\[
T^*(x^2+yz)=\lambda(x^2+yz).
\]
Then
\[
(T^*y)(T^*z)=(\lambda-\alpha^2)x^2+\lambda yz.
\]
The left side is reducible and has quadratic rank at most two.  The right
side has rank three if \(\lambda-\alpha^2\ne0\), because both coefficients
are nonzero.  Hence \(\lambda=\alpha^2\), and unique factorization makes
\(\{T^*y,T^*z\}\) proportional to \(\{y,z\}\).  The induced map on the
whole pencil is scalar.

Therefore every companion point is its own orbit:
\[
[g_\tau]=[x^2+\tau yz],\qquad \tau\in\mathbb P^1.
\]
Equivalently, \(\tau\) is the cross-ratio coordinate of
\([g]\) relative to the three fixed intrinsic points
\[
[s]=[x^2],\qquad [h]=[x^2+yz],\qquad [r]=[yz].
\]
No two distinct values of \(\tau\), including \(0,1,\infty\), can merge
under a legal affine source or target equivalence.

#### S0: \((s,h)=(x^2,y^2+xz)\)

After fixing \(h\), the residual affine action on the coordinate \(u\) is
the scaling \(u\mapsto\lambda u\).  It again has exactly three orbits:
\[
[g]=[x^2],\qquad [g]=[y^2+xz],\qquad
[g]=[x^2+y^2+xz].
\]

### 4. Clean-room predicted taxonomy and boundary attack

The predicted orbit space is therefore the disjoint union
\[
\{\mathrm{R0}_s,\mathrm{R0}_h,\mathrm{R0}_{\mathrm{gen}}\}
\ \sqcup\
\{[g_\tau]:\tau\in\mathbb P^1\}
\ \sqcup\
\{\mathrm{S0}_s,\mathrm{S0}_h,\mathrm{S0}_{\mathrm{gen}}\}.
\]

The points \(\tau=0,1,\infty\) must remain in the \(\mathbb P^1\) family;
they are boundary companions \(s,h,r\), not separate marked-pair orbits.
The only ways the claimed family could collapse would be:

1. a source translation adding a leading derivative to the normal cubic;
   this fails because the derivative has zero normal component;
2. a target row operation adding a leading component to the normal row;
   this fails because the leading target-plane annihilator is unique;
3. a source transformation fixing \(s,h\) but inducing a nontrivial
   automorphism of the reduced pencil; the rank/reducibility calculation
   above forces that action to be scalar; or
4. swapping intrinsic roles among \(s,h,r\); their roles and/or determinant
   multiplicities distinguish them.

This completes and seals the pre-comparison derivation.
