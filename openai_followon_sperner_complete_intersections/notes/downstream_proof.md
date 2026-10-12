# Conditional EGH-to-Sperner implication and scope reductions

Independent check: 2026-10-06 22:17:06 America/Los_Angeles
(2026-10-07 05:17:06 UTC). This note proves the downstream implication. It does
**not** certify the new upstream EGH argument. Downstream mathematical
completion: 100%; unconditional project completion remains undetermined
pending the upstream audit. Publication-package completion is not assessed
by this subtask.

## Exact statement and exact dependency

Let k have characteristic zero, R=k[x_1,...,x_n], and
A=R/(f_1,...,f_n), where the sequence is homogeneous regular of positive
degrees d_i and A is standard graded Artinian. Write m=A_{>0}, h_j=dim_k A_j,
and

\[
D(A)=\max_{I\triangleleft A}\mu_A(I),\qquad
\mu_A(I)=\dim_k(I/mI).
\]

The maximum includes **all** ideals and includes the unit ideal. The target is

\[
D(A)=\max_{j\ge0}h_j
=\max_{j\ge0}[t^j]\prod_{i=1}^n(1+t+\cdots+t^{d_i-1}). \tag{T}
\]

The needed EGH assertion for this particular sequence is: for **every
homogeneous ideal** Q of R containing (f_1,...,f_n), there is a homogeneous
ideal Q' containing (x_1^{d_1},...,x_n^{d_n}) such that

\[
H_{R/Q}(j)=H_{R/Q'}(j)\quad\text{for every }j. \tag{EGH_A}
\]

Equivalently, every homogeneous I in A has a homogeneous representative J
in B=k[x_1,...,x_n]/(x_1^{d_1},...,x_n^{d_n}) with H_{A/I}=H_{B/J}.
Equality of Hilbert functions of Q and Q' themselves is equivalent because
the ambient polynomial ring is the same. Merely identifying H_A=H_B is
insufficient and already holds for every complete intersection.

Theorem 11 of Harima–Wachi–Watanabe proves this conditional implication to
the Sperner property over an arbitrary field. Their Definition 2 uses all
ideals. Their Proposition 7 supplies matching for B; Proposition 8 combines
matching, Gorenstein duality and unimodality; Sublemma 9 supplies truncation.
The proof below rederives the mechanism and makes all-ideal descent explicit.

Primary full text checked:
[arXiv v1](https://arxiv.org/html/1601.06928),
[PDF](https://arxiv.org/pdf/1601.06928), and
[version record](https://arxiv.org/abs/1601.06928).
Citation: T. Harima, A. Wachi, J. Watanabe, *The EGH Conjecture and the
Sperner property of complete intersections*, Proc. Amer. Math. Soc. 145
(2017), no. 4, 1497–1503,
[DOI 10.1090/proc/13347](https://doi.org/10.1090/proc/13347).
The DOI redirects to the AMS identifier S0002-9939-2016-13347-9.
The corresponding publisher PDF returned HTTP 403; no comparison with
publisher typesetting is claimed. The project-local primary arXiv PDF
sources/priority/HWW_arxiv1601.06928v1.pdf has SHA-256
b66c69b4c9e901ddb2b9fc6e655a9d4a7c276558638014ee5bb0075fbf453172.

## Degenerate cases and linear elimination

For n=0 the ring is k, the sequence and product are empty, and D(k)=1=h_0;
the ideals are 0 and k. If all degrees are 1, elimination gives the same
case. The unit ideal must be allowed for this equality.

Let r count the degree-one generators. Their linear forms are independent:
otherwise the Artinian defining ideal would have at most n-1 generators,
contradicting height n by Krull's height theorem. A linear change of
coordinates identifies their ideal with (y_1,...,y_r), giving

\[
A\simeq k[z_1,\ldots,z_q]/(g_1,\ldots,g_q),\qquad q=n-r.
\]

The images of the remaining forms have the original degrees, all at least
2. None vanishes, by the same height argument in q variables. They are a
homogeneous system of parameters and hence regular, since a polynomial
ring is Cohen–Macaulay. Equivalently one may permute the homogeneous
regular sequence and quotient by its linear subsequence first. A graded
isomorphism preserves the maximal ideal, all ideals, each number dim(I/mI),
and every h_j. Each removed factor in (T) equals 1. Thus an upstream theorem
requiring all degrees at least 2 applies after this exact elimination.

The multiplication exact sequences for the regular generators give

\[
H_A(t)=\frac{\prod_i(1-t^{d_i})}{(1-t)^n}
=\prod_i(1+t+\cdots+t^{d_i-1}). \tag{1}
\]

The standard Artinian complete-intersection duality theorem gives a
one-dimensional socle in degree c=sum_i(d_i-1) and perfect multiplication
pairings A_j x A_{c-j}->A_c\simeq k. One derivation is the Koszul resolution
with final shift sum_i d_i, giving the graded canonical module A(c).
In particular h_j=h_{c-j}. Unimodality follows from the elementary
monomial-basis construction below and H_A=H_B.

## Matching for the monomial complete intersection

The monomial basis of B is the ranked product of the chains
0<=e_i<=d_i-1. It has a symmetric saturated chain decomposition. For
completeness, two chains of lengths a<=b (ranks 0 through a and 0 through b)
have the rectangle partition

\[
(r,0),(r,1),\ldots,(r,b-r),
(r+1,b-r),\ldots,(a,b-r),\qquad r=0,\ldots,a. \tag{2}
\]

Endpoint ranks sum to a+b. A point (i,j) belongs to the row part of chain i
if j<=b-i, and otherwise to the column part of chain b-j; thus the chains
are disjoint and exhaustive. Exchange the factors when a>b. Multiply each
chain of a previously decomposed product by the next factor and repeat
(2). If the old chain starts at rank s and has length a, then 2s+a is the
old total rank, so symmetry of the new endpoint ranks is preserved.

This proves symmetric unimodality of the rank sizes. Whenever h_j<=h_{j+1},
every chain meeting rank j extends to rank j+1. For j<c/2 this is immediate.
For j>=c/2 no chain starts at j+1, so h_{j+1}-h_j is minus the number ending
at j; the assumed inequality excludes any ending. Taking each monomial to
its chain successor injects every rank-j set S into its upper shadow.

For an arbitrary subspace W\subset B_j, echelonize a basis with respect to
a multiplicative monomial order. Its leading monomial set S has size dim W.
If m\in S and x_i m survives the pure-power quotient, the corresponding
basis vector times x_i still has leading term x_i m: lower terms stay
lower and the leading term survives. Thus the upper shadow of S lies in
the leading monomial set of B_1W, proving

\[
\dim W\le\dim B_1W\quad\text{if }h_j\le h_{j+1}. \tag{3}
\]

No weak or strong Lefschetz assertion is used.

## EGH transfers matching to A

For V\subset A_j, let I=AV. Handle V=0 separately. Standard grading gives
I_j=V and I_{j+1}=A_1V. Apply (EGH_A) to get J in B. Equality of the quotient
Hilbert functions and H_A=H_B give

\[
\dim J_j=\dim V,\qquad \dim J_{j+1}=\dim A_1V.
\]

If h_j<=h_{j+1}, (3) and the ideal property give

\[
\dim V=\dim J_j\le\dim B_1J_j
\le\dim J_{j+1}=\dim A_1V. \tag{4}
\]

This is matching for A. J need not be generated in degree j; its possible
additional generators make the second inequality valid. Neither equality
of generator counts of I and J nor Betti domination is assumed. Only the
quotient-Hilbert-function consequence of EGH is needed.

## Homogeneous bound via matching and Gorenstein duality

Here is a direct presentation of the established HWW mechanism that avoids
their auxiliary Dilworth-lattice proposition. Let p be the last degree
attaining max h_j. Symmetry and unimodality give c-p<=p, and matching holds
for every j<p. Standard grading gives m^u=\bigoplus_{j>=u}A_j.

If I is homogeneous with initial degree alpha<p, remove that degree:
I'=\bigoplus_{j>=alpha+1}I_j. Counting the graded pieces of I/mI gives

\[
\mu(I')-\mu(I)=\dim A_1I_\alpha-\dim I_\alpha\ge0. \tag{5}
\]

Iterate to obtain

\[
\mu(I)\le\mu(I\cap m^p). \tag{6}
\]

Suppose now I\subset m^p and set J=Ann_A(mI). The Frobenius pairing gives
dim Ann(U)=dim A-dim U for each ideal U. To verify the exact annihilator
identity, project multiplication onto A_c: a vector orthogonal to all of
U is orthogonal to all multiples of each u\in U, hence annihilates u by
nondegeneracy. Since mJ\subset Ann(I),

\[
\begin{aligned}
\mu(J)&=\dim J-\dim mJ\\
&\ge\dim Ann(mI)-\dim Ann(I)\\
&=\dim I-\dim mI=\mu(I). \tag{7}
\end{aligned}
\]

The graded perfect pairings give

\[
Ann(m^u)=m^{c-u+1}\quad(0\le u\le c+1). \tag{8}
\]

For u>=1, inclusion of the right side follows by degree. A nonzero element
in degree e<=c-u pairs nontrivially with something in degree c-e>=u, proving
the reverse inclusion. The endpoint u=0 says Ann(A)=0=m^{c+1}.
Since mI\subset m^{p+1},

\[
J\supset Ann(m^{p+1})=m^{c-p}\supset m^p. \tag{9}
\]

Apply (6) to J. Its truncation J\cap m^p equals m^p, so (7) gives
\mu(I)<=\mu(J)<=\mu(m^p)=h_p. Apply (6) first to any homogeneous I to obtain
the same bound. The zero ideal is immediate. Equality is attained by m^p,
because m^p/m^{p+1}\simeq A_p.

## Exact passage to every ideal

For an arbitrary ideal I, filter A by F^jA=m^j=A_{>=j} and filter I and mI
by intersection with F. Then

\[
J=\operatorname{gr}_F I
=\bigoplus_j(I\cap m^j)/(I\cap m^{j+1}) \tag{10}
\]

embeds naturally as a homogeneous ideal in gr_m(A)\simeq A. It consists of
lowest-degree initial parts, not highest-degree terms in a term order.
Multiplication respects this filtration, giving

\[
mJ\subset\operatorname{gr}_F(mI). \tag{11}
\]

A degree-one element times an initial part is either the degree-j+1
initial part of the original product or zero. This verifies (11) directly;
iteration handles all positive degrees. Total dimensions are preserved by
finite associated grading, so

\[
\begin{aligned}
\mu_A(I)&=\dim I-\dim mI\\
&=\dim J-\dim\operatorname{gr}_F(mI)\\
&\le\dim J-\dim mJ=\mu_A(J). \tag{12}
\end{aligned}
\]

The homogeneous bound applies to J and proves the all-ideal upper bound.
Its equality witness m^p proves (T). No equality gr(mI)=m gr(I) is asserted
or needed.

## Field extensions and descent

If upstream EGH is available over an algebraic closure K of k, apply the
conditional proof to A_K=A\otimes_k K. Regularity survives flat extension
and the Hilbert function is unchanged. For every ideal I of A, flatness
gives

\[
\frac{IA_K}{m_KIA_K}\simeq(I/mI)\otimes_k K,
\qquad \mu_{A_K}(IA_K)=\mu_A(I). \tag{13}
\]

The all-ideal upper bound in A_K therefore descends to all ideals of A;
the lower witness m^p already exists over k. There is no need to descend
an EGH representative J and no assertion that every ideal over K descends.
If upstream EGH already has arbitrary characteristic-zero field scope,
this extension is unnecessary. A result solely over the rationals is
insufficient without a separate checked scope or extension mechanism.

## Findings and remaining gap

- The downstream conditional implication and the boundary reductions are
  sound. Degree-one elimination preserves the exact target algebra.
- The all-ideal quantifier is justified by (10)–(12), with the correct
  inequality direction. The unit ideal covers A=k.
- EGH representatives may acquire degree-j+1 generators; (4) handles this.
- The zero V case is separate from HWW's assertion that AV has initial
  degree j. It presents no substantive gap.
- No weak/strong Lefschetz, nongraded complete-intersection, or unconditional
  positive-characteristic conclusion follows here.
- This is a verification and explicit presentation of a known conditional
  mechanism, not a claim of a new downstream general theorem.
- The exact unresolved dependency for the unconditional target is a valid
  proof of (EGH_A) in the necessary characteristic-zero scope, over k or
  a suitable extension. This note cannot repair a material upstream gap.

No external individuals were contacted. No commits or publication actions
were performed by this subtask.
