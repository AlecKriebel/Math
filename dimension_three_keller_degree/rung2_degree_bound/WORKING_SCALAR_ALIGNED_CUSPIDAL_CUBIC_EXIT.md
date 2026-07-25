# Working theorem: the scalar-aligned cuspidal-cubic stratum

**Status:** proved by exact determinant elimination, checked by two exact
implementations, and independently adversarially reconstructed from the raw
systems.  This is not peer reviewed.  The source-specific priority search
found no exact prior statement and is not a guarantee of worldwide priority.

**Recorded:** 2026-07-25T04:19:11Z.

**Promoted after audit:** 2026-07-25T04:36:50Z.

## 1. Statement and the marked-point orbits

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have total degree four, with \(H_i\) homogeneous of degree \(i\), and
suppose
\[
H_4=h(p,q)A(p,q),\qquad
A=(p^2q,p^3,q^3)^T,
\tag{1}
\]
where \(h\) is a nonzero binary linear form.  This is the scalar-aligned
part of the cuspidal-cubic row
\[
(e,a,b,\delta,\nu)=(1,1,3,3,1).
\]

### Theorem

No Keller map satisfying (1) exists.

It is important not to use the full \(\operatorname{PGL}_2\) on the
normalization parameter.  The stabilizer of the embedded cuspidal
parametrization has only a diagonal source action.  Indeed, the cusp has
preimage \([0:1]\), so a source matrix inducing a projective automorphism
of the embedded curve has
\[
p'=ap,\qquad q'=cp+dq.
\]
The pulled-back coordinate \(q'^3\) belongs to
\[
\langle p^2q,p^3,q^3\rangle
\]
only if \(c=0\).  Conversely, every diagonal source matrix preserves this
three-dimensional linear series, with an induced diagonal target change.

Consequently a marked zero of \(h\) has exactly three orbits:
\[
\boxed{h=p,\qquad h=q,\qquad h=p+q.}
\tag{2}
\]
They respectively mark the cusp preimage, the distinguished smooth flex
preimage, and a general smooth preimage.  The diagonal torus is transitive
on the last locus, but it cannot identify any two of the three displayed
positions.

## 2. Degree eight and the ramified normal

Put
\[
S=(2q,3p,0)^T,\qquad
T=(p^2,0,3q^2)^T,\qquad
N=(3pq^2,-2q^3,-p^3)^T.
\tag{3}
\]
For \(B=hA\), direct differentiation gives
\[
B_p\times B_q=
\begin{cases}
4p^3N,&h=p,\\
4pq^2N,&h=q,\\
4p(p+q)^2N,&h=p+q.
\end{cases}
\tag{4}
\]
The reduced normal has the Hilbert--Burch syzygies
\[
S\times T=3N.
\tag{5}
\]

Since \(H_4\) is binary,
\[
\operatorname{adj}(JH_4)=e_r(B_p\times B_q)^T.
\]
The degree-eight Keller identity therefore gives
\[
N\cdot\partial_rH_3=0.
\tag{6}
\]
The degree-one and degree-two syzygies in (5) give the complete solution
\[
\boxed{
H_3=V(p,q)+r\bigl((ap+bq)S+cT\bigr)+dr^2S,
}
\tag{7}
\]
where \(V\) is an arbitrary binary cubic vector.

Order the coefficients of \(V\), component by component, by
\[
(p^3,p^2q,pq^2,q^3)
\tag{8}
\]
and denote them \(v_0,\ldots,v_{11}\).

## 3. The raw degree-seven branch tree

Use the componentwise coefficient order
\[
(p^2,pq,pr,q^2,qr,r^2)
\tag{9}
\]
for a general \(H_2\), with entries \(w_0,\ldots,w_{17}\).
For every form in (2), the coefficient matrix of the degree-seven identity
in the \(w_i\) has exact rank eight.  Its compatibility equations have the
following specialization-safe consequences.

### 3.1 The cusp-marked form \(h=p\)

Successive square equations force
\[
d=c=b=0.
\]
The remaining compatibilities are exactly
\[
a(9v_3+2v_6)=0,\qquad av_7=0.
\tag{10}
\]
Conversely these relations kill every raw compatibility.  Thus there are
two leaves:
\[
\begin{array}{c|c}
a=0&H_3=V,\\
a\ne0&H_3=V+rA_p,\quad v_6=-\frac92v_3,\quad v_7=0,
\end{array}
\tag{11}
\]
where a scaling of \(r\) was used in the second line.

### 3.2 The flex-marked form \(h=q\)

Here the raw equations first force
\[
d=b=0,\qquad ac=0.
\]
They then give the three leaves
\[
\begin{array}{c|c}
a=c=0&H_3=V,\\
a\ne0,\ c=0&H_3=V+rA_p,\quad v_8=0,\\
a=0,\ c\ne0&H_3=V+rA_q,\quad v_8=v_9=0.
\end{array}
\tag{12}
\]
Again the nonzero tangent coefficient is normalized by scaling \(r\), and
substitution of each line kills every remaining compatibility.

### 3.3 A general marked point \(h=p+q\)

The division-free forcing order
\[
d^2,\quad c^2\ \bmod d,\quad b^2\ \bmod d,\quad
a^2\ \bmod(b,c,d)
\]
gives
\[
\boxed{a=b=c=d=0.}
\tag{13}
\]
Thus only the binary cubic leaf \(H_3=V\) remains.

## 4. Excluding every binary-cubic leaf

When \(H_3=V(p,q)\), the complete degree-seven solution is
\[
\boxed{
H_2=B(p,q)+\kappa rS,
}
\tag{14}
\]
with \(B\) an arbitrary binary quadratic vector.  This follows either from
the rank-eight raw solve or directly from the degree-one syzygies of \(N\).

If \(\kappa=0\), the following degree-six coefficients force the third
column \((\lambda_{13},\lambda_{23},\lambda_{33})^T\) of \(L_0\) to vanish:
\[
\begin{array}{c|c|c}
h&\text{monomial}&\text{coefficient of }E_6\\ \hline
p&p^6&-4\lambda_{33}\\
 &p^4q^2&12\lambda_{13}\\
 &p^3q^3&-8\lambda_{23}\\ \hline
q&p^4q^2&-4\lambda_{33}\\
 &p^2q^4&12\lambda_{13}\\
 &pq^5&-8\lambda_{23}\\ \hline
p+q&p^6&-4\lambda_{33}\\
 &p^4q^2&12\lambda_{13}-4\lambda_{33}\\
 &p^3q^3&24\lambda_{13}-8\lambda_{23}.
\end{array}
\tag{15}
\]

If \(\kappa\ne0\), scale \(r\) so that \(\kappa=1\).  The degree-six
systems in
\[
(v_0,\ldots,v_{11},\lambda_{13},\lambda_{23},\lambda_{33})
\]
have ranks \(7,6,7\) for \(h=p,q,p+q\), respectively.  Substitution of
their complete exact solutions into degree five gives the
parameter-independent certificates
\[
\begin{array}{c|c}
h&\text{degree-five certificate}\\ \hline
p&[pq^3r]E_5=24,\\
q&[q^4r]E_5=24,\\
p+q&[pq^3r]E_5=[q^4r]E_5=24.
\end{array}
\tag{16}
\]
Hence no binary-cubic leaf is compatible with a Keller map.

## 5. The three nonzero-tangent leaves

For transparency, the exact affine degree-seven solutions are recorded
before the final obstruction.  All unlisted \(w_i\) below are free; in
each case the free indices are
\[
0,1,3,6,7,8,9,12,13,15.
\tag{17}
\]

### 5.1 \(h=p,\ H_3=V+rA_p\)

Under \(v_6=-9v_3/2\) and \(v_7=0\), the forced coefficients are
\[
\begin{aligned}
w_2&=(27v_0-v_{10})/12,&
w_4&=(15v_1+3v_{11}-18v_4+8w_8)/12,\\
w_5&=0,&w_{10}&=-(3v_2-10v_5)/8,\\
w_{11}&=3/2,&w_{14}&=9v_8/4,\\
w_{16}&=5v_9/4,&w_{17}&=0.
\end{aligned}
\tag{18}
\]
With arbitrary \(L_0\) and all ten free coefficients retained, degree six
contains
\[
\boxed{[pq^3r^2]E_6=-12.}
\tag{19}
\]

### 5.2 \(h=q,\ H_3=V+rA_p\)

Under \(v_8=0\),
\[
\begin{aligned}
w_2&=2(v_1-v_4),&
w_4&=(3v_2-4v_5+2w_8)/3,\\
w_5&=-1,&w_{10}&=v_6,\\
w_{11}&=0,&w_{14}&=2v_9,\\
w_{16}&=-9v_0+v_{10},&w_{17}&=0.
\end{aligned}
\tag{20}
\]
The parameter-free obstruction is
\[
\boxed{[pq^3r^2]E_6=-48.}
\tag{21}
\]

### 5.3 \(h=q,\ H_3=V+rA_q\)

Under \(v_8=v_9=0\),
\[
\begin{aligned}
w_2&=(15v_2-2v_5)/12,&
w_4&=(27v_3-10v_6+8w_8)/12,\\
w_5&=0,&w_{10}&=9v_7/4,\\
w_{11}&=0,&w_{14}&=(9v_0+5v_{10})/4,\\
w_{16}&=-3(v_1-3v_{11}+2v_4)/4,&w_{17}&=3.
\end{aligned}
\tag{22}
\]
This time
\[
\boxed{[p^4r^2]E_6=12.}
\tag{23}
\]

Equations (19), (21), and (23) exclude all nonzero-tangent leaves.  Together
with Section 4, they prove the theorem.

## 6. Verification boundary and disclosure

`verify_scalar_aligned_cusp_sympy.py` reconstructs the stabilizer-independent
normal minors, all three raw degree-seven systems and branch radicals, the
complete degree-seven \(H_2\) families, the rank-\(7,6,7\) degree-six
solves behind (16), and every coefficient in (15), (16), and
(18)--(23).

`verify_scalar_aligned_cusp_pari.gp` independently expands the normalized
branch identities in PARI/GP.  It checks the common reduced normal, the
binary-leaf degree-six and degree-five certificates, all three complete
tangent-leaf \(H_2\) parametrizations, and their constant degree-six
obstructions.

The diagonal-stabilizer and marked-point classification is mathematical
input rather than a computer check.  The exact calculations establish
identities in the encoded coefficient systems; they are not peer review.

The independent audit reconstructed the diagonal stabilizer and all three
marked-point orbits, the complete Hilbert--Burch degree-eight family, every
raw degree-seven compatibility and converse, the tangent-leaf quadratic
kernels, and the rank-\((7,6,7)\) binary-leaf solves.  Direct independent
expansions reproduced the constants \(-12,-48,12,24\), with no omitted
specialization or extraneous branch.

This proof and its regressions were developed with AI assistance.  The
result has not been peer reviewed.
