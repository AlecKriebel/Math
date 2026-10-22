# Proof of the finite-generator extra shift-invariance criterion

This AI-assisted, unrefereed edition records an internal AI audit of an established prior theorem. Acceptance here is an internal mathematical assessment, not human peer review or formal proof-assistant certification. Finite checks are corroboration only. This is a full written proof and audit edition, not a computational reproduction package. Source retrieval and inspection occurred during the preceding audit on 11 October 2026; this editorial preparation performed no fresh scholarly-source retrieval or inspection.

**Target:** problem 30000035, OWR-720-001.
**Status:** finite-generator characterization established by a prior theorem; original-source scope qualification retained.
**Authorship boundary:** this is an authored reconstruction and mathematical audit, not a new characterization, formal verification, or external peer review.

## 1. Exact conclusion and attribution

Let \(n\geq1\) be an integer and \(\Phi=(\phi_1,\ldots,\phi_r)\) a finite family in \(L^2(\mathbb R)\). Let \(S\) be the **norm-closed** span of all its integer translates. Define

\[
B_k=\bigcup_{q\in\mathbb Z}([k,k+1)+nq),\qquad
\widehat{\phi_i^k}=1_{B_k}\widehat\phi_i,
\quad 0\leq k<n.
\]

With the Fourier convention \(\widehat f(\xi)=\int f(x)e^{-2\pi ix\xi}\,dx\), define

\[
G(\omega)_{ij}=\sum_{\ell\in\mathbb Z}
\widehat\phi_i(\omega+\ell)\overline{\widehat\phi_j(\omega+\ell)},
\qquad
G_k(\omega)_{ij}=\sum_{\ell\equiv k\pmod n}
\widehat\phi_i(\omega+\ell)\overline{\widehat\phi_j(\omega+\ell)}
\tag{1}
\]

for \(\omega\in[0,1)\). Then

\[
T_{1/n}S=S
\quad\Longleftrightarrow\quad
\operatorname{rank}G(\omega)=\sum_{k=0}^{n-1}\operatorname{rank}G_k(\omega)
\quad\text{for almost every }\omega\in[0,1).
\tag{2}
\]

This is Theorem 5.2 of Aldroubi, Cabrelli, Heil, Kornelson and Molter, *Invariance of a Shift-Invariant Space*, J. Fourier Anal. Appl. 16 (2010), 60–75, [DOI](https://doi.org/10.1007/s00041-009-9068-y), [arXiv:0804.1597v3](https://arxiv.org/abs/0804.1597v3). The arXiv version is dated 21 December 2008 in its submission history and watermark; its generated PDF also has a 29 October 2018 typesetting date. The latter is not treated as a new theorem date.

No linear independence, nonzero-fiber, Riesz-basis or frame-bound hypothesis is required in (2). Zero generators, dependent generators and variable rank are allowed. This establishes a general characterization of finitely generated closed shift-invariant spaces. It does **not** certify every intended interpretation of the original workshop question.

## 2. Original-source scope qualification

The original workshop question sought a qualitative, useful support-style criterion in the identity-Gramian case. The established rank criterion and its normalized specialization do not by themselves certify that unspecified qualitative standard. The full original-source discussion is retained in [AUDIT.md](AUDIT.md), Section 2. Its printed scalar support test is valid under Fourier interpretation; the literal time-domain display fails for sinc. This notation issue and the closure repair below do not make the prior rank theorem false. Chui and Sun (2003) already supplied a related vector-orthogonality condition in their affine-frame setting, so the normalized orthogonality formulation is not claimed as new.

## 3. Definitions, measure and topology

All functions are equivalence classes modulo Lebesgue-null sets. Fourier transforms on \(L^2\) are defined by the unitary Plancherel extension. The operator is \(T_af(x)=f(x-a)\), so its Fourier multiplier is \(e^{-2\pi ia\xi}\). No \(2\pi\) factor belongs in the integer frequency shifts of (1).

By Tonelli, for almost every \(\omega\in[0,1)\), each sequence
\(v_i(\omega)=(\widehat\phi_i(\omega+\ell))_{\ell\in\mathbb Z}\)
is in \(\ell^2(\mathbb Z)\). Cauchy–Schwarz makes every series in (1) absolutely convergent there. Removing a countable union of exceptional sets makes all required generator, coordinate and residue identities simultaneous. The matrices are measurable, positive semidefinite, and \(G=\sum_kG_k\). Their ranks are measurable, for example by the nonvanishing of finitely many minors. Statements are a.e., not at every point, and half-open interval endpoints have no effect.

The residue formula for \(G_k\) in (1) is asserted on the chosen fundamental interval. The globally defined Gramian of \(\Phi^k\) is 1-periodic; carrying the same residue labels unchanged outside that interval would require adjusting for the integer part of the frequency.

Under the original assumption \(G=I_r\), Plancherel shows
\(\langle T_a\phi_i,T_b\phi_j\rangle=\delta_{ij}\delta_{ab}\)
for integers \(a,b\), since these inner products are Fourier coefficients of the entries of \(G\). Consequently the synthesis map from \(\ell^2(\mathbb Z)^r\) is an isometry. Its image is closed and equals the closed span; its series converge unconditionally in \(L^2\). This justifies identifying the original coefficient-defined space with \(S\). For arbitrary generators an unqualified \(\ell^2\) synthesis description is unsafe; it is the closed-span definition that is used in (2).

Also, on an integer-invariant space, \(T_{1/n}S\subseteq S\) already gives equality: \(T_{-1/n}=T_{-1}T_{1/n}^{n-1}\) preserves \(S\). Thus the paper's invariance formulation and the source's equality formulation agree.

## 4. Independent proof of the finite-generator theorem

### 4.1 Standard facts used

The proof uses the Plancherel theorem and its translation formula; Tonelli/Fubini, Cauchy–Schwarz and dominated convergence; Hilbert-space orthogonal complements and projections; uniqueness of Fourier coefficients for \(L^1\) functions on the circle; and finite-dimensional Gram–Schmidt, rank and the spectral theorem for Hermitian matrices. Fourier uniqueness can be obtained from convergence of Fejér means in \(L^1\). These are imported standard results. No unproved extra-invariance theorem or general range-function theorem is needed below.

### 4.2 The fiber membership lemma

The map
\[
\mathcal Tf(\omega)=(\widehat f(\omega+\ell))_{\ell\in\mathbb Z}
\]
is unitary from \(L^2(\mathbb R)\) to \(H=L^2([0,1);\ell^2(\mathbb Z))\): the norm identity is Tonelli plus Plancherel, and any measurable square-integrable field reconstructs a Fourier transform on the disjoint unit intervals. Put
\(J(\omega)=\operatorname{span}\{v_1(\omega),\ldots,v_r(\omega)\}\).
This span is finite-dimensional and closed. We prove
\[
f\in S\quad\Longleftrightarrow\quad\mathcal Tf(\omega)\in J(\omega)\text{ a.e.}
\tag{3}
\]

Use the inner product linear in the first argument. For \(h\in H\), the function
\(b_i(\omega)=\langle h(\omega),v_i(\omega)\rangle\)
is in \(L^1\) by Cauchy–Schwarz in \(H\). Orthogonality of \(\mathcal T^{-1}h\) to every \(T_j\phi_i\), \(j\in\mathbb Z\), is exactly the vanishing of every Fourier coefficient of every \(b_i\). Fourier uniqueness gives
\[
\mathcal T(S^\perp)=N:=\{h\in H:h(\omega)\perp J(\omega)\text{ a.e.}\}.
\]

For completeness the pointwise projection onto \(J\) is measurable. Run Gram–Schmidt on the finite ordered list \(v_i\), leaving a zero vector whenever a residual has zero norm, and dividing by its norm otherwise. Norms and inner products are measurable. This produces measurable fields \(e_i\), with nonzero fields orthonormal at each point, and
\(P(\omega)h=\sum_i\langle h,e_i\rangle e_i\).
Both \(P\) and \(I-P\) act as bounded orthogonal projections on \(H\). Their ranges are, respectively, the fields in \(J\) and the fields in \(J^\perp\). Taking orthogonal complements now proves (3). This construction avoids ill-defined pointwise evaluation across an uncountable family of \(L^2\) representatives.

### 4.3 Translation and residue projections

Define \(D\) on \(\ell^2(\mathbb Z)\) by
\((Dz)_\ell=e^{-2\pi i\ell/n}z_\ell\). Then
\[
\mathcal T(T_{1/n}f)(\omega)=e^{-2\pi i\omega/n}D\mathcal Tf(\omega).
\]
By (3), invariance implies \(Dv_i\in J\) a.e. for the finite list of generators; hence \(DJ\subseteq J\). Conversely that pointwise inclusion, applied to every field in (3), implies invariance of \(S\). Since \(D^n=I\), \(DJ\subseteq J\) and \(DJ=J\) are equivalent.

Let \(Q_k\) select coordinates \(\ell\equiv k\pmod n\). Its spectral formula is
\[
Q_k=\frac1n\sum_{s=0}^{n-1}e^{2\pi iks/n}D^s.
\tag{4}
\]
This follows coordinatewise from the finite geometric sum. Thus \(DJ=J\) is equivalent to \(Q_kJ\subseteq J\) for all \(k\): one direction uses (4), and the other uses \(D=\sum_ke^{-2\pi ik/n}Q_k\).

The spaces \(Q_kJ\) are mutually orthogonal, have dimension at most \(r\), and
\(J\subseteq\bigoplus_k Q_kJ\), since \(z=\sum_kQ_kz\). Therefore
\[
Q_kJ\subseteq J\ \forall k
\quad\Longleftrightarrow\quad
\dim J=\sum_k\dim Q_kJ.
\tag{5}
\]
The reverse implication uses equality of the dimensions of **finite-dimensional** spaces under inclusion.

The Gram matrix of the list \(v_i\), with the stated inner-product convention, is exactly \(G\); the Gram matrix of \(Q_kv_i\) is \(G_k\). The rank of a Gram matrix equals the dimension of the span of its list, even for a dependent list or the zero list. Consequently (5) is precisely (2), proving both directions.

## 5. Closure repair in the published proof presentation

The primary paper defines \(U_k=P_kS\), where \(P_k\) is Fourier cutoff to \(B_k\). Its Lemma 4.3 correctly proves closedness **when** \(U_k\subseteq S\). Before invariance is established, an image of a closed subspace under a bounded orthogonal projection need not be closed. Unqualified identification of this image with a closed cutoff-generated SIS in the dimension/Gramian discussion needs care.

A counterexample already satisfies the original normalization. Take \(n=2,r=1\), and prescribe, for \(0<\omega<1\),
\[
\widehat\phi(\omega)=\sqrt\omega,\qquad
\widehat\phi(\omega+1)=\sqrt{1-\omega},
\]
with zero values outside \([0,2)\). Then \(G=1\). By the isometric synthesis description, members of \(S\) have Fourier values
\((a(\omega)\sqrt\omega,a(\omega)\sqrt{1-\omega})\)
with \(a\in L^2(0,1)\). The cutoff image on the first interval is
\(\sqrt\omega L^2(0,1)\), which is not closed in \(L^2(0,1)\):
\[
g_N=1_{[1/N,1)}=\sqrt\omega\,a_N,
\quad a_N=\omega^{-1/2}1_{[1/N,1)},
\quad\|a_N\|_2^2=\log N<\infty.
\]
But \(g_N\to1\) in \(L^2(0,1)\), while \(1/\sqrt\omega\notin L^2(0,1)\). Thus the limit is outside the cutoff image. Also \(P_0S\ne S\cap\{\widehat f\text{ supported in }B_0\}\): the intersection is zero, while the image is nonzero.

The safe replacement before proving invariance is
\[
W_k=S(\phi_1^k,\ldots,\phi_r^k)=\overline{P_kS}^{\,L^2}.
\tag{6}
\]
Indeed \(P_k\) is bounded and commutes with integer translations, so applying it to the dense finite span proves both inclusions after taking closures. Lemma (3) applied to the cutoff generators gives fiber space \(Q_kJ\). The proof in Section 4 therefore establishes the rank criterion without assuming \(P_kS\) is closed. Once invariance holds, \(P_kS\subseteq S\), and
\(P_kS=S\cap\operatorname{ran}P_k=W_k\) is closed. The general theorem survives this repair; the counterexample is not a counterexample to Theorem 5.2.

## 6. Exact specialization to the original normalized case

Assume \(G=I_r\) a.e. Put
\(a_\ell(\omega)=(\widehat\phi_1(\omega+\ell),\ldots,\widehat\phi_r(\omega+\ell))^T\).
Then \(G_k=\sum_{\ell\equiv k}a_\ell a_\ell^*\), \(0\leq G_k\leq I_r\), and \(\sum_kG_k=I_r\). The following are equivalent, a.e.:

1. \(T_{1/n}S=S\).
2. \(\sum_k\operatorname{rank}G_k=r\).
3. Every \(G_k\) is an orthogonal projection and these projections have mutually orthogonal ranges.
4. For all integers \(p,q\) in different residue classes modulo \(n\), \(a_p(\omega)^*a_q(\omega)=0\).

Here is a proof of the additional equivalences. Every eigenvalue of \(G_k\) lies in \([0,1]\), so \(\operatorname{tr}G_k\leq\operatorname{rank}G_k\). Their traces sum to \(r\). Equality of the total ranks to \(r\) therefore forces equality for each matrix, and every nonzero eigenvalue is 1. Thus the \(G_k\) are projections. If \(x\in\operatorname{ran}G_k\), then
\(\sum_{j\ne k}\langle G_jx,x\rangle=0\); positivity gives \(G_jx=0\) for \(j\ne k\). The ranges are mutually orthogonal. Conversely mutually orthogonal projections summing to identity have ranks summing to \(r\).

Finally,
\(\ker G_k=\{x:a_\ell^*x=0\text{ for all }\ell\equiv k\}\),
because its nonnegative quadratic form is \(\sum_{\ell\equiv k}|a_\ell^*x|^2\). Taking orthogonal complements in finite-dimensional \(\mathbb C^r\) gives
\(\operatorname{ran}G_k=\operatorname{span}\{a_\ell:\ell\equiv k\}\).
Hence orthogonality of the ranges is precisely condition 4.

For \(r=1\), write
\(E_k=\{\omega\in[0,1):\widehat\phi(\omega+k+nq)\ne0\text{ for some }q\in\mathbb Z\}\).
The scalar \(G_k\) is positive exactly on \(E_k\). Since \(\sum_kG_k=1\), their union has full measure. Equation (2) says that exactly one is positive a.e.; equivalently, the \(E_k\) are pairwise disjoint modulo null sets. At \(n=2\) this is the valid Fourier-domain interpretation of the original test.

Without \(G=1\), the principal-space statement is instead that **at most** one residue is active a.e.; the zero fiber is allowed. Without normalization in higher rank, the vector-orthogonality formulation is not asserted: the always-valid test is the rank equality (2).

## 7. Adverse examples and practical boundaries

**The scalar support pattern does not generalize componentwise.** Take \(r=n=2\), \(u=(1,1)^T/\sqrt2\), \(v=(1,-1)^T/\sqrt2\). On each unit interval \([\ell,\ell+1)\), set the Fourier generator vector to the following constant, and set it to zero elsewhere:

- Family A: \((a_0,a_1,a_2,a_3)=(u,v,u,v)/\sqrt2\).
- Family B: \((a_0,a_1,a_2,a_3)=(u,u,v,v)/\sqrt2\).

Both families have \(G=uu^*+vv^*=I_2\), and each individual generator has the same nonzero support \([0,4)\) modulo endpoints. For A, \(G_0=uu^*\), \(G_1=vv^*\), and the rank sum is 2: it is invariant. For B, \(G_0=G_1=I_2/2\), and the rank sum is 4: it is not invariant. Thus the zero/nonzero support sets of the original components cannot determine the answer for general finite rank. Values and their relative directions matter.

**Finite generation matters for dimension counting.** Let \(\phi_j\), \(j\in\mathbb Z\), have Fourier transform \(2^{-1/2}(1_{[2j,2j+1)}+1_{[2j+1,2j+2)})\). The closed space generated by all their integer translates has constant fiber
\(J=\overline{\operatorname{span}}\{e_{2j}+e_{2j+1}:j\in\mathbb Z\}\).
Its elements have equal paired coordinates. For \(n=2\), \(D\) changes one sign in every pair, so \(DJ\ne J\). Nevertheless \(\dim J=\dim Q_0J+\dim Q_1J\) as infinite cardinal dimensions: both sides are countably infinite. The membership assertion follows either by the orthogonal-complement proof of (3), now using a countable list, or by applying scalar Fourier uniqueness separately to every pair. Extending (2) by treating infinite ranks as ordinary dimensions would lose its force.

**Exact classification is not a finite numerical decision algorithm for arbitrary input functions.** Even for normalized principal generators, let
\(\widehat\phi_\varepsilon=\sqrt{1-\varepsilon^2}1_{[0,1)}+\varepsilon1_{[1,2)}\), with \(0\leq\varepsilon<1\). Then \(G=1\), the \(\varepsilon=0\) space is invariant, and every \(\varepsilon>0\) space fails (2), while \(\phi_\varepsilon\to\phi_0\) in \(L^2\). Rank is discontinuous at the exact-invariance boundary. The criterion also contains infinite alias sums and an a.e. assertion over a continuum. A finite collection of samples can miss a positive-measure failure set. An effective symbolic or certified numerical decision procedure needs an input representation and additional error-control hypotheses, none supplied by the original request or by (2). This is a limitation of the claimed deliverable, not a proof that every possible restricted algorithm is impossible.

## 8. Scope and review boundary

The accepted scope is exact characterization of norm-closed, finitely generated shift-invariant subspaces of L2(R), for a fixed positive integer n. No effective finite algorithm on arbitrary L2 data, separate approximate-invariance result, infinite-generator rank theorem, fulfillment of the original unspecified qualitative support-style standard, novelty, external review or formal verification is claimed. [AUDIT.md](AUDIT.md) preserves the complete original-source qualification, source inspection boundaries and audit disposition. The proof in Sections 3–7 above is retained verbatim from the accepted authored reconstruction.
