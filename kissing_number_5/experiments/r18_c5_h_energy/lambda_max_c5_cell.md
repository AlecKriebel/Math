# A sharp frame bound on the closed `C5` sign cell

## Statement

Let \(z_0,\ldots,z_4\) be unit vectors.  Indices below are read modulo \(5\).
Assume

\[
\langle z_i,z_{i+1}\rangle\le-\frac12
\quad\text{and}\quad
\left|\langle z_i,z_{i+2}\rangle\right|\le\frac12 .
\]

Let \(G=(\langle z_i,z_j\rangle)_{i,j=0}^4\).  Then

\[
\lambda_{\max}(G)\le 3.
\]

All inequalities are non-strict, and no nonzero-coordinate or
nondegeneracy hypothesis is needed.

## Two elementary height lemmas

Fix a unit vector \(u\).  For a unit vector \(p\) whose height
\(h_p=\langle u,p\rangle\) is nonnegative, write
\(h_p=\cos\alpha_p\), where \(0\le\alpha_p\le\pi/2\).

**Lemma A (deep pair).**  If
\(\langle p,q\rangle\le-1/2\) and both heights are nonnegative, then

\[
h_p^2+h_q^2\le\frac34.
\]

Indeed, the angular distance between \(p\) and \(q\) is at least
\(2\pi/3\).  The spherical triangle inequality through \(u\) gives
\(\alpha_p+\alpha_q\ge2\pi/3\).  Since \(\cos^2\) is decreasing on
\([0,\pi/2]\), a maximum occurs when the sum is \(2\pi/3\).  Put
\(\alpha_p=\pi/3+v\) and
\(\alpha_q=\pi/3-v\); necessarily \(|v|\le\pi/6\).  Then

\[
\cos^2(\pi/3+v)+\cos^2(\pi/3-v)
=1-\frac12\cos(2v)\le\frac34.
\]

**Lemma B (ordinary pair).**  If
\(|\langle p,q\rangle|\le1/2\), then

\[
\langle u,p\rangle^2+\langle u,q\rangle^2\le\frac32.
\]

This is the operator-norm bound for the two-vector frame
\(pp^{\mathsf T}+qq^{\mathsf T}\), whose largest eigenvalue is
\(1+|\langle p,q\rangle|\).

We also use the following three-height consequence.

**Lemma C (the four-cut triple).**  Suppose \(p_0,p_2,p_4\) have
nonnegative heights \(\cos\alpha_0,\cos\alpha_2,\cos\alpha_4\), and

\[
\alpha_0+\alpha_2\ge\frac{\pi}{3},\qquad
\alpha_2+\alpha_4\ge\frac{\pi}{3},\qquad
\alpha_0+\alpha_4\ge\frac{2\pi}{3}.
\]

Then

\[
\cos^2\alpha_0+\cos^2\alpha_2+\cos^2\alpha_4\le\frac32.
\]

To prove this, interchange \(0\) and \(4\) if necessary so that
\(\alpha_0\le\alpha_4\).  Monotonicity of \(\cos^2\) permits decreasing
the angles until

\[
\alpha_4=\frac{2\pi}{3}-\alpha_0,\qquad
\alpha_2=\frac{\pi}{3}-\alpha_0.
\]

The ranges \(0\le\alpha_i\le\pi/2\) and
\(\alpha_0\le\alpha_4\) imply
\(\pi/6\le\alpha_0\le\pi/3\), so these replacements stay in the
allowed range.  Finally,

\[
\cos^2 a+\cos^2(\pi/3-a)+\cos^2(2\pi/3-a)=\frac32.
\]

The identity follows on replacing each \(\cos^2 x\) by
\((1+\cos 2x)/2\): the three remaining cosine terms sum to zero.

## Proof of the frame bound

Choose a unit eigenvector \(b=(b_i)\) of \(G\) for its largest
eigenvalue \(\lambda\).  Since \(\operatorname{tr}G=5\), we have
\(\lambda>0\).  Choose \(s_i\in\{-1,1\}\) with
\(s_i b_i=|b_i|\), choosing either sign when \(b_i=0\), and set
\(y_i=s_i z_i\).  Define

\[
u=\frac{\sum_i |b_i|y_i}{\sqrt\lambda}.
\]

The eigenvector equation gives

\[
h_i:=\langle u,y_i\rangle=\sqrt\lambda\,|b_i|\ge0,
\qquad
\sum_i h_i^2=\lambda.
\]

The number of sign changes in the cyclic word
\((s_0,s_1,s_2,s_3,s_4)\) is even, hence is \(0\), \(2\), or \(4\).

### No sign changes

All five switched cycle edges remain deep.  Summing Lemma A over those
five edges counts every \(h_i^2\) twice:

\[
2\lambda\le5\cdot\frac34,
\]

so in fact \(\lambda\le15/8\).

### Two sign changes

The equal-sign runs have lengths \(4+1\) or \(3+2\).

For a run of length four, apply Lemma A to two disjoint internal edges;
its height mass is at most \(3/2\).  Adding the singleton, whose squared
height is at most \(1\), gives \(\lambda\le5/2\).

For a run \(v_0v_1v_2\) of length three, the two internal applications
of Lemma A give

\[
h_{v_0}^2+2h_{v_1}^2+h_{v_2}^2\le\frac32,
\]

so the run mass is at most \(3/2\).  The length-two run has mass at most
\(3/4\) by Lemma A.  Thus \(\lambda\le9/4\).

### Four sign changes

After a cyclic relabeling and a global sign reversal, the signs are
\(+,-,+,-,+\).  The switched edge \(y_4y_0\) remains deep.  The pairs
\((y_0,y_2)\) and \((y_2,y_4)\) are switched chords and therefore have
angular distance at least \(\pi/3\).  Spherical triangle inequalities
through \(u\) give precisely the hypotheses of Lemma C.  Hence

\[
h_0^2+h_2^2+h_4^2\le\frac32.
\]

The remaining pair \((y_1,y_3)\) is a chord, so Lemma B gives

\[
h_1^2+h_3^2\le\frac32.
\]

Consequently \(\lambda=\sum_i h_i^2\le3\), as claimed.

## Boundary and zero cases

- Equality \(\langle z_i,z_{i+1}\rangle=-1/2\) and chord equality
  \(|\langle z_i,z_{i+2}\rangle|=1/2\) are allowed throughout.
- A zero entry of the top eigenvector can be assigned either sign.
  Its height is zero, and the cyclic sign word still has \(0\), \(2\),
  or \(4\) changes.  Every estimate remains valid.
- The proof uses neither the rank of \(G\) nor strict positivity of
  \(G\).
- This theorem is a frame bound only.  By itself it does not prove the
  quartic-energy inequality.
