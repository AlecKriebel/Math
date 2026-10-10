# KP-3.71: odd torsion does not certify a nonzero boundary class

**Target:** 2869 / KP-3.71.
**Outcome:** unresolved after two approaches. No new theorem is claimed.

## 1. Exact source scope

Problem 3.71 in the [2026 K3 list](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf),
printed pp.182–183, asks whether

\[
 \ker\bigl(\Theta^3_{\mathbb Z}\longrightarrow
                 \Theta^3_{\mathbb F_2}\bigr)\ne0.
 \tag{1}
\]

The required witness is an integral homology sphere \(Y\) which bounds a smooth
mod-2 homology four-ball and bounds **no** smooth integral homology four-ball.
The issue is the boundary class, not whether one chosen filling has integral
torsion. All manifolds below are smooth, compact, connected and oriented unless
otherwise stated. The source's rational-ball question, Problem 3.72, is distinct.

The source expressly notes that \(\Sigma(2,3,7)\) is not a witness to (1):
its nonzero Rokhlin invariant excludes a mod-2 ball. That exclusion applies to
all possible mod-2 fillings of that sphere, not merely to the familiar rational
filling. The problem is retained in the April 2026 source; the present bounded
literature audit located no verified resolution.

## 2. Necessary integral homology of a filling

The following is a standard duality calculation, included to make the
coefficient distinction precise.

**Lemma.** Let \(W\) be an oriented rational homology four-ball with boundary
an integral homology sphere \(Y\), and let \(A=H_1(W;\mathbb Z)\). Then \(A\)
is finite and

\[
 H_2(W;\mathbb Z)\cong A^\vee,\qquad
 H_3(W;\mathbb Z)=H_4(W;\mathbb Z)=0,
 \quad A^\vee=\operatorname{Hom}(A,\mathbb Q/\mathbb Z).
 \tag{2}
\]

In particular, \(W\) is a mod-2 homology ball exactly when \(|A|\) is odd.
It is an integral homology ball exactly when \(A=0\).

**Proof.** Rational acyclicity and finite generation make positive-dimensional
integral homology finite. In particular \(H^1(W;\mathbb Z)=0\). Since
\(H^0(W;\mathbb Z)\to H^0(Y;\mathbb Z)\) is an isomorphism, the cohomology
sequence of the pair gives \(H^1(W,Y;\mathbb Z)=0\). Poincaré–Lefschetz
duality then gives \(H_3(W;\mathbb Z)=0\). Also \(H_4(W;\mathbb Z)=0\)
because the connected oriented manifold has nonempty boundary.

The homology sequence and \(H_2(Y)=H_1(Y)=0\) give
\(H_2(W)\cong H_2(W,Y)\). Duality and the universal coefficient theorem give

\[
 H_2(W,Y)\cong H^2(W)
 \cong\operatorname{Ext}(H_1(W),\mathbb Z)
 \cong A^\vee,
\]

since \(\operatorname{Hom}(H_2(W),\mathbb Z)=0\). This proves (2).
For a finite group \(A\), tensor and Tor with \(\mathbb F_2\) vanish exactly
when \(A\) has odd order. Applying the homological universal coefficient
theorem to (2) proves both final assertions. \(\square\)

More explicitly, if
\(r=\dim_{\mathbb F_2}(A/2A)\), then

\[
 (b_1(W;\mathbb F_2),b_2(W;\mathbb F_2),b_3(W;\mathbb F_2))
 =(r,2r,r).
 \tag{3}
\]

Thus a witness to (1) must admit a filling with nonzero finite odd-order first
homology and its dual second homology. This is a requirement on homology, not
a claim that the fundamental group is finite or has odd order.

### Spin and Rokhlin obstruction

A mod-2 homology ball has \(H^1(W;\mathbb F_2)=H^2(W;\mathbb F_2)=0\).
It therefore has a unique spin structure, and its signature is zero. The
boundary integral homology sphere satisfies

\[
 \mu(Y)=\sigma(W)/8\pmod2=0.
 \tag{4}
\]

This recovers the source's exclusion of \(\Sigma(2,3,7)\). It also excludes
the subfamilies in [Akbulut–Larson, Theorem 1](https://arxiv.org/abs/1704.07739)
whose nontriviality is established by \(\mu=1\), namely their odd-parameter
subfamilies, and the corresponding even-parameter subfamilies with
\(\bar\mu=1\) in [Şavk, Theorem 1.1](https://arxiv.org/abs/1912.04654).
No blanket exclusion of the other parameter values is inferred.

### Three-handles are necessary for a nonintegral filling

If a handle decomposition of \(W\) had no three-handles, its second homology
would be a subgroup of the free group of two-handles and hence free. By (2) it
is finite, so it vanishes, and then \(A=0\). Consequently a rational ball
with integral homology sphere boundary that is not an integral ball requires
three-handles in every handle decomposition. This standard obstruction is
already stated in the introduction of Akbulut–Larson. It does not prove that
the boundary cannot have a different integral filling.

## 3. Approach 1: reuse rational-ball and invariant-vanishing examples

The mod-2 condition cannot be replaced by rational acyclicity: equation (3)
retains the two-primary part that rational homology discards. In particular,
the \(\mu=1\) examples just cited are ruled out at the level of their boundary.
A particular rational filling with two-primary torsion would fail the mod-2
condition, but that fact alone would not exclude a different mod-2 filling.

Nor does the vanishing of familiar Floer invariants establish the existence
of a mod-2 ball. A concrete current warning is
[Lee–Şavk, Theorem 1.2, arXiv v2 (2026)](https://arxiv.org/abs/2508.15384):
under their stated Seifert-sphere hypotheses, they produce nontrivial classes
in the kernel of the involutive Heegaard Floer local-equivalence map which
remain nontrivial, and in the specified families independent, even in
rational homology cobordism. Those examples cannot be witnesses to (1),
because every mod-2 ball is a rational ball. No equivalence between trivial
local-equivalence data and a mod-2 filling is assumed here.

**Gap.** This route gives useful exclusions but supplies neither a smooth
odd-torsion filling of a suitable nonzero class nor an integral nonbounding
obstruction for a class that actually has such a filling. The untreated
parameter values are not settled by the parity argument.

## 4. Approach 2: realize odd torsion geometrically

It is easy to realize precisely the required torsion pattern in actual smooth
fillings, but that does not make their boundaries nonzero in
\(\Theta^3_{\mathbb Z}\). The following standard spin construction provides
a useful negative control, with a complete homology calculation.

Fix \(p\ge2\), let \(L=L(p,1)\) be a lens space, and put
\(X=L\setminus\operatorname{int}(D^3)\). Form the closed four-manifold

\[
 M_p=\partial(X\times D^2)
     =(X\times S^1)\cup_{S^2\times S^1}(S^2\times D^2),
 \tag{5}
\]

with corners smoothed. This is the ordinary spin of the three-manifold,
as recalled in [Meier, Section 2](https://arxiv.org/abs/1708.01214),
not a new construction. Let \(W_p=M_p\setminus\operatorname{int}(D^4)\),
where the removed ball is a coordinate ball. In particular,
\(\partial W_p\cong S^3\).

The punctured lens space has
\(H_1(X)=\mathbb Z/p\) and \(H_2(X)=H_3(X)=0\). Write
\(U=X\times S^1\), \(V=S^2\times D^2\), \(E=S^2\times S^1\).
Künneth gives

\[
 H_1(U)=\mathbb Z/p\oplus\mathbb Z,\quad H_2(U)=\mathbb Z/p,\quad H_3(U)=0,
\]

and \(H_2(V)=\mathbb Z\), with other positive groups zero. In the
Mayer–Vietoris sequence the map from \(H_1(E)=\mathbb Z\) injects onto the
\(S^1\) summand of \(H_1(U)\). The map from \(H_2(E)=\mathbb Z\) to
\(H_2(U)\oplus H_2(V)\) is \(a\mapsto(0,\pm a)\): the boundary sphere is
zero in \(H_2(X)\) and generates \(H_2(V)\). These two injective maps give

\[
 H_1(M_p)=\mathbb Z/p,\quad H_2(M_p)=\mathbb Z/p,
 \quad H_3(M_p)=0,\quad H_4(M_p)=\mathbb Z.
 \tag{6}
\]

Van Kampen also gives \(\pi_1(M_p)=\mathbb Z/p\): the gluing kills the
extra product-circle generator. Removing the coordinate ball leaves the
first and second homology unchanged and removes the top-dimensional class;
the orientation class maps isomorphically onto the new boundary sphere, so
\(H_3(W_p)=0\). Therefore

\[
 H_1(W_p)=H_2(W_p)=\mathbb Z/p,
 \qquad H_3(W_p)=H_4(W_p)=0.
 \tag{7}
\]

For odd \(p>1\), this is a smooth mod-2 homology ball which is not an
integral homology ball. Nevertheless its boundary is \(S^3\), which of course
also bounds \(D^4\). Thus it represents the **zero** boundary class in (1).

Boundary connected sums of these examples similarly realize any prescribed
finite odd abelian group \(A\) as \(H_1\), with \(H_2\cong A^\vee\), while
the boundary remains \(S^3\). The positive-dimensional homology is the direct
sum under this operation. In particular, no criterion depending only on the
presence or size of this filling torsion can establish the nonzero boundary
class required by the problem.

**Gap.** Modifying such a filling must change the boundary to a sphere known
not to admit *any* integral ball while preserving mod-2 acyclicity. No such
modification is constructed here. Boundary summing with another filling does
not erase its two-primary homology: positive-dimensional homology adds.
An attempted proof of injectivity by removing odd torsion would likewise need
a smooth geometric cancellation argument, not merely a chain-complex or
intersection-form calculation. None is provided.

## 5. Checks and disposition

The exact checker uses small free chain complexes with
\(d_2=[D\ 0]\), \(d_3=[0\ D]^T\), where \(D\) is diagonal, to verify the
tensor/Tor dimensions in (3), including both odd and even controls. These are
algebraic diagnostics, not substitutes for a manifold realization. The actual
manifold control is (5), whose boundary is explicitly the standard sphere.

The homology, spin, and handle observations are standard, and the examples
are controls rather than a new answer. The attempt stops at the missing
geometric filling/nonbounding combination. Neither a nonzero kernel element
nor injectivity has been established. The full source question remains
**unsolved in this attempt**.
