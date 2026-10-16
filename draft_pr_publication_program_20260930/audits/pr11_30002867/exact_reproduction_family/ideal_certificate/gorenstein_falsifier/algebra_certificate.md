# Independent algebra certificate for the five-generator ideal

Let `k` be any field, let `S=k[x,y,z]`, let `m=(x,y,z)`, and let

\[
J=(x^2,y^2,xz,yz,z^2-xy),\qquad R=S_m,\qquad A=R/JR.
\]

**Verified conclusion.** The quotient has length 5, `JR` has minimal
generator number 5, `A` is Artinian Gorenstein, and its minimal free
resolution over `R` has ranks `(1,5,5,1)`. The proof works over every
field; it does not require characteristic zero or invertibility of 2.
These statements are proved below without a Koszul homology rank
calculation.

## 1. Quotient, length, and minimal generators

All ten degree-three monomials lie in `J`. Nine are visibly divisible
by one of `x^2,y^2,xz,yz` or follow from such divisibility, and the
remaining one satisfies

\[
z^3=z(z^2-xy)+y(xz)\in J.
\]

Consequently `m^3` is contained in `J`. The five listed quadratic
generators are linearly independent in `S_2`: the coefficients of
`x^2,y^2,xz,yz,z^2` successively determine their coefficients. Thus
`S/J` has graded dimensions `(1,3,1)` and basis

\[
1,x,y,z,q,\qquad q=xy=z^2.
\]

Its maximal ideal is nilpotent, so this quotient is already local;
localizing at `m` does not change it. Therefore

\[
\operatorname{length}_R A=\dim_k A=5,
\qquad H_{S/J}(t)=1+3t+t^2.
\]

For additional precision about localization, since `J` is generated
by degree-two forms,

\[
J/mJ\cong J_2\cong k^5.
\]

Localization preserves this quotient, so Nakayama's lemma gives
`mu_R(JR)=5`. The height is 3 because `m^3` is contained in `J`.
In particular the ideal is not a complete intersection.

## 2. Socle and a direct Gorenstein certificate

The multiplication table is determined by

\[
x^2=y^2=xz=yz=0,\quad xy=z^2=q,\quad xq=yq=zq=q^2=0.
\]

For an arbitrary element

\[
a=a_0+a_1x+a_2y+a_3z+a_4q,
\]

we have

\[
xa=a_0x+a_2q,\quad ya=a_0y+a_1q,\quad za=a_0z+a_3q.
\]

The displayed basis implies that all three products vanish exactly
when `a_0=a_1=a_2=a_3=0`. Hence

\[
\operatorname{Soc}(A)=(0:_A m)=kq.
\]

One may certify the Gorenstein conclusion directly, without relying
only on the socle criterion. Let `lambda:A -> k` extract the
coefficient of `q`. The bilinear pairing `(a,b) -> lambda(ab)` has
matrix, in the ordered basis `(1,x,y,z,q)`,

\[
\begin{pmatrix}
0&0&0&0&1\\
0&0&1&0&0\\
0&1&0&0&0\\
0&0&0&1&0\\
1&0&0&0&0
\end{pmatrix}.
\]

Its determinant is 1. It induces an `A`-module isomorphism

\[
A\longrightarrow\operatorname{Hom}_k(A,k),\quad
a\longmapsto[b\mapsto\lambda(ab)].
\]

For any `A`-module `M`, evaluation at `1` gives the natural
isomorphism

\[
\operatorname{Hom}_A(M,\operatorname{Hom}_k(A,k))
\cong\operatorname{Hom}_k(M,k).
\]

Its inverse sends a linear functional `f` to
`m -> [a -> f(am)]`. Vector-space duality is exact. Therefore
`Hom_k(A,k)` is injective as an `A`-module, and the pairing identifies
`A` itself as injective. Thus the Artinian local algebra has injective
dimension zero and is Gorenstein. No division by 2 or characteristic
restriction occurs.

## 3. An elementary exact minimal resolution

Write the generators in the order

\[
g=(x^2,y^2,xz,yz,z^2-xy).
\]

Consider the homogeneous complex

\[
0\longrightarrow S(-5)
\xrightarrow{d_3}S(-3)^5
\xrightarrow{d_2}S(-2)^5
\xrightarrow{d_1}S
\longrightarrow S/J\longrightarrow0,
\]

where

\[
d_1=\begin{pmatrix}x^2&y^2&xz&yz&z^2-xy\end{pmatrix},
\]

\[
d_2=\begin{pmatrix}
z&0&0&y&0\\
0&z&0&0&x\\
-x&0&y&-z&0\\
0&-y&-x&0&-z\\
0&0&0&x&y
\end{pmatrix},\qquad
d_3=\begin{pmatrix}
-y^2\\x^2\\z^2-xy\\yz\\-xz
\end{pmatrix}.
\]

The columns of `d_2` encode the five polynomial identities

\[
\begin{aligned}
z x^2-x(xz)&=0,\\
z y^2-y(yz)&=0,\\
y(xz)-x(yz)&=0,\\
y x^2-z(xz)+x(z^2-xy)&=0,\\
x y^2-z(yz)+y(z^2-xy)&=0.
\end{aligned}
\]

Direct multiplication gives `d_2 d_3=0` as well.

To prove exactness at the middle-left term, suppose
`d_2(A,B,C,D,E)^T=0` in `S^5`. The last row gives
`xD+yE=0`. Since `x` and `y` are relatively prime in `S`, there is
`T in S` with

\[
D=yT,\qquad E=-xT.
\]

The first row now gives `zA=-y^2T`. Since `z` and `y` are relatively
prime, `z` divides `T`; write `T=zU`. The first two rows give

\[
A=-y^2U,\qquad B=x^2U.
\]

The third row gives

\[
y\bigl(xyU+C-z^2U\bigr)=0,
\]

and `S` is a domain, so `C=(z^2-xy)U`. The fourth row is then an
identity. Consequently

\[
\ker(d_2)=S\,(-y^2,x^2,z^2-xy,yz,-xz)^T=\operatorname{im}(d_3).
\]

Also `d_3` is injective because its first coordinate is a nonzero
polynomial in the domain `S`.

It remains to prove exactness at `S(-2)^5`. We already know
`im(d_2)` is contained in `ker(d_1)`. Exactness just proved gives

\[
H_{\operatorname{im}(d_2)}(t)
=\frac{5t^3-t^5}{(1-t)^3}.
\]

Since `im(d_1)=J` and the quotient basis above proves
`H_{S/J}=1+3t+t^2`, we obtain

\[
\begin{aligned}
H_{\ker(d_1)}(t)
&=\frac{5t^2-1}{(1-t)^3}+(1+3t+t^2)\\
&=\frac{5t^3-t^5}{(1-t)^3}.
\end{aligned}
\]

Here the last equality is the polynomial identity

\[
(1+3t+t^2)(1-t)^3=1-5t^2+5t^3-t^5.
\]

The inclusion of graded modules with equal Hilbert series is an
equality in every degree, proving the missing exactness. Localizing
this exact complex at `m` gives a free resolution over `R`. Every
matrix entry belongs to `mR`; hence tensoring with the residue field
makes every differential zero. This resolution is minimal and

\[
(\beta_0^R(A),\beta_1^R(A),\beta_2^R(A),\beta_3^R(A))=(1,5,5,1).
\]

## 4. Adversarial findings and exact gap

- **Characteristic 2:** signs specialize consistently. The pairing
  determinant remains 1 and the polynomial-kernel argument uses only
  coprimeness and the domain property. All conclusions survive.
- **Localization:** the global quotient is already local because its
  maximal ideal is nilpotent. Length does not change on localization.
- **Minimality:** generator independence is checked modulo `mJ`, and
  the resolution matrices have no unit entries after localization.
- **Hidden complete-intersection issue:** height 3 and minimal
  generator number 5 exclude that issue for this ideal.
- **Scope limitation:** this is a fully verified local-algebra
  example. It does not by itself reproduce any unrelated global
  projective or affine construction, or validate its stated hypotheses.

There is **no remaining gap in the four local claims** under the
stated assumption that `k` is a field. The attached dependency-free
script checks polynomial compositions over the integers, associativity
of the multiplication table, and nondegeneracy of the pairing. Its
checks corroborate the proof; they are not substitutes for exactness.
