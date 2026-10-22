# Exact prior type A W-algebra isomorphism: OWR-16635-009

## Status of this edition

This AI-assisted proof reconstruction and internal AI audit are unrefereed. Acceptance in this edition is the audit's mathematical judgment within its explicit imported-theorem boundary; it is not journal acceptance, external human peer review, or formal proof-assistant certification. The AVM source article is separately published in Forum of Mathematics, Sigma (2024). No novelty or new general-family claim is made.

This is a complete authored proof/audit edition, not a computational reproduction package. Finite checks support exact identities only; they do not establish imported vertex-algebra theorems. Source hashes authenticate retrieved bytes, not mathematical correctness. Source PDFs, extracted text, images, programs, and raw outputs are not distributed here.

This proof and the companion AUDIT.md partition one accepted reconstruction and audit. AUDIT.md retains the complete discussion of inspected arguments, established imports, corrections, and limits. They are not two independent audits.

## Decision and exact scope

The exact 2018 question has an affirmative previously published resolution:

\[
\mathcal W_{-14/3}(\mathfrak{sl}_7,f_{(3,2,2)})
\cong L_{-4/3}(\mathfrak{sl}_2)
\cong \mathcal W_{-8/3}(\mathfrak{sl}_4,f_{(2,2)}).
\]

Here \(\mathcal W_k\) means the **simple graded quotient** of the universal affine W-algebra, over \(\mathbb C\), and \(L_\ell\) means the simple affine vertex algebra. The isomorphisms also preserve the standard Dynkin conformal vectors. The central charge is \(-6\).

**Acceptance:** accept the exact pair as a prior result, with the explicitly identified established vertex-algebra results below as imports. This is a reconstruction and audit of the applicable written argument, including independent exact checks of every specialization-specific finite calculation. It is not merely acceptance of the Allegra attribution, and it is not a proof of a new general family. It is not a formal verification of vertex-algebra foundations or a recursive reproof of every paper cited by the main article.

The absence of Allegra's thesis is **not** a missing link in this proof route. Arakawa, van Ekeren and Moreau (AVM) give another written proof that covers the pair. The thesis's independent proof and priority details beyond the published attribution remain uninspected.

The authenticated local source is arXiv:2102.13462v3, dated 21 February 2023, 92 pages. The corresponding published article is *Forum of Mathematics, Sigma* 12 (2024), e95, DOI [10.1017/fms.2024.81](https://doi.org/10.1017/fms.2024.81). The published Theorem 8.8 and its proof were text-checked at pages 46-48; this is not a claim to have hashed or compared every byte of the published PDF. All AVM page citations below, unless expressly marked published, refer to the authenticated arXiv v3 PDF.

## The original problem and the theorem match

Anne Moreau's contribution, joint with Tomoyuki Arakawa, in Oberwolfach Report 52/2018 defines the distinction between \(\mathcal W^k\) and \(\mathcal W_k\) on printed page 3121. Printed page 3123, PDF page 43, conjectures exactly the two simple W-algebras above, with levels written \(-7+7/3\) and \(-4+4/3\). The partitions and subscripts were checked visually. The source is [the EMS workshop report](https://ems.press/content/serial-article-files/46773).

AVM Theorem 8.8(2), page 46, concerns \(n=q\widetilde m+\widetilde s\), \(\widetilde s=q-2\), and nilpotent partition \((q^m,(q-1)^2)\) with \(m=\widetilde m-1\). Its affirmative formula at \(p=n\) is

\[
\mathcal W_{-n+n/q}(\mathfrak{sl}_n,f_{(q^m,(q-1)^2)})
\cong L_{-2+2/q}(\mathfrak{sl}_2).
\]

The two substitutions are:

| Quantity | Seven dimensional defining representation | Four dimensional defining representation |
|---|---:|---:|
| \(n,p,q\) | \(7,7,3\) | \(4,4,3\) |
| \(k=-n+p/q\) | \(-14/3\) | \(-8/3\) |
| \(\widetilde m,\widetilde s\) | \(2,1\) | \(1,1\) |
| \(m=\widetilde m-1\) | \(1\) | \(0\) |
| Partition of \(f\) | \((3,2,2)\) | \((2,2)\) |
| Dense associated orbit partition | \((3,3,1)\) | \((3,1)\) |
| Remaining affine level | \(-2+2/3=-4/3\) | \(-2+2/3=-4/3\) |

Admissibility is immediate from the type A criterion: \(p\geq n\) and \(\gcd(p,q)=1\). The respective gcds are \(\gcd(7,3)=\gcd(4,3)=1\). The affine \(\mathfrak{sl}_2\) level has numerator 2, denominator 3 and is admissible as well. All three levels are noncritical.

**Orbit closure matters.** The actual hypothesis is \(f\in\overline{\mathbb O_k}\), not \(f\in\mathbb O_k\). The overbars are visible in the PDF and can disappear in text extraction. In dominance order \((3,2,2)\leq(3,3,1)\) and \((2,2)\leq(3,1)\); neither chosen orbit is the dense orbit. The reductions are nonzero, but this is not the dense-orbit rational/lisse case.

AVM page 48 explicitly credits Allegra for the \(n=7,q=3,s=4\) example and names \((3,2^2)\) among the covered partitions. That paragraph is corroboration, not a proof premise here. The preceding Conjecture 8.11 literally prints \(1<m\), whereas this named example has \(m=1\). We do not silently change that bound or invoke the conjecture. The exact statement and proof of Theorem 8.8(2) suffice.

## A proof specialized to this pair

### Structural inputs and the collapse criterion

Write \(V_n=\mathcal W_{-2n/3}(\mathfrak{sl}_n,f)\) for \(n=7,4\) with the stated partitions, and write
\(\widetilde V_n=H^0_{DS,f}(L_{-2n/3}(\mathfrak{sl}_n))\).
AVM Theorems 3.2 and 4.3 provide nonvanishing of \(\widetilde V_n\) from the orbit-closure check, and a graded surjection \(\widetilde V_n\twoheadrightarrow V_n\). In Dynkin grading, \(V_n\) is conical and self-dual, by the W-algebra construction and AVM Proposition 4.2. The current fields associated with the \(\mathfrak{sl}_2\)-triple centralizer give affine homomorphisms into \(V_n\); their levels will be calculated below.

We use AVM Theorem 3.10, pages 19-20, restricted to the simple Lie algebra \(\mathfrak{sl}_2\). Its pertinent hypotheses are:

1. An admissible level \(\ell\) and a homomorphism \(V^\ell(\mathfrak{sl}_2)\to V\), where \(V\) is conical and self-dual.
2. The affine Sugawara vector maps to weight 2 and is annihilated by \((\omega_V)_{(2)}\). These are the current-embedding properties in AVM (35), page 28.
3. A surjection \(\widetilde V\to V\) whose source has asymptotic weight 0 and the same growth and asymptotic dimension as \(L_\ell(\mathfrak{sl}_2)\).

The conclusion is that this map factors through an isomorphism \(L_\ell(\mathfrak{sl}_2)\cong V\). Thus equality of numerical invariants alone is not being used as an isomorphism criterion: the actual affine map, self-duality, grading, admissibility, and quotient hypotheses are essential.

We apply this criterion directly to the \(\mathfrak{sl}_2\) factor. This avoids treating a zero-level abelian algebra as if it had a nondegenerate Sugawara vector, and it does not require an artificial central factor in the \(m=0\) case.

### Centralizers and the affine levels

Let \(E_d\) denote the \(d\)-dimensional irreducible representation of the nilpotent triple's \(\mathfrak{sl}_2\). For the seven dimensional representation the decomposition is
\(E_3\oplus(E_2\otimes\mathbb C^2)\). Its triple centralizer in \(\mathfrak{sl}_7\) is the trace-zero part of \(\mathfrak{gl}_1\oplus\mathfrak{gl}_2\), hence \(\mathbb C\oplus\mathfrak{sl}_2\). For the four dimensional representation it is \(E_2\otimes\mathbb C^2\); the trace-zero condition removes the scalar, so the centralizer is exactly \(\mathfrak{sl}_2\).

Take the following diagonal grading elements and Cartan elements in the multiplicity \(\mathfrak{sl}_2\):

\[
\begin{aligned}
x_7&=(1,\tfrac12,\tfrac12,0,-\tfrac12,-\tfrac12,-1),&
t_7&=(0,1,-1,0,1,-1,0),\\
x_4&=(\tfrac12,\tfrac12,-\tfrac12,-\tfrac12),&
t_4&=(1,-1,1,-1).
\end{aligned}
\]

For type A the normalized form is the trace form, so \((t_n,t_n)_{\mathfrak{sl}_n}=4\). On the multiplicity \(\mathfrak{sl}_2\), its normalized form gives \((H,H)=2\). AVM (32) gives the induced form

\[
\phi(t,t)=k\operatorname{tr}(t^2)
 +\tfrac12\bigl(\kappa_{\mathfrak g}(t,t)
 -\kappa_{\mathfrak g_0}(t,t)
 -\operatorname{tr}_{\mathfrak g_{1/2}}(\operatorname{ad}t)^2\bigr).
\]

The three trace terms are, respectively, \((56,16,8)\) for \(n=7\), and \((32,16,0)\) for \(n=4\). They can be obtained directly by summing \((t_i-t_j)^2\) over matrix units of the indicated degree. Dividing \(\phi(H,H)\) by 2 gives

\[
\ell_7=2k_7+8=-4/3,\qquad \ell_4=2k_4+4=-4/3.
\]

As a check, the extra center in the seven dimensional case is generated by
\(z=(4,-3,-3,4,-3,-3,4)\). Its trace-square is 84, its full Killing value is 1176, its degree-zero trace value is 0, and its half-degree trace value is 392. Hence its induced form is \(84(-14/3)+(1176-392)/2=0\). No such center exists for \((2,2)\).

### Reduction growth and dimension from Dynkin roots

AVM Proposition 4.10(1), page 25, gives \(w=0\) and

\[
g_{\widetilde V_n}=\dim\mathfrak g^f-\frac{n(n^2-1)}{pq}.
\]

At \(p=n,q=3\), the transposed partitions \((3,3,1)\) and \((2,2)\) give
\(\dim\mathfrak g^f=3^2+3^2+1^2-1=18\) and \(2^2+2^2-1=7\). Therefore

\[
g_{\widetilde V_7}=18-48/3=2,\qquad
g_{\widetilde V_4}=7-15/3=2.
\]

For the asymptotic dimension, first cancel the common finite Weyl product in Proposition 4.10. In type \(A_{n-1}\), \(|P/Q|=n\), so
\(|P/(nq)Q|^{1/2}=n^{n/2}q^{(n-1)/2}\). Also

\[
\prod_{\alpha>0}2\sin\frac{\pi(\rho,\alpha)}n
=\prod_{d=1}^{n-1}(2\sin(\pi d/n))^{n-d}=n^{n/2}.
\]

For completeness, pair \(d\) with \(n-d\). The square of the product is the \(n\)th power of \(\prod_{d=1}^{n-1}2\sin(\pi d/n)=n\), which follows by evaluating \((z^n-1)/(z-1)\) at \(z=1\). All factors are positive, so the positive square root is legitimate. This proves the exact finite identity used here without needing a numerical trigonometric approximation.

Put \(r_0=|\Delta^0_+|\) and \(r_{1/2}=|\Delta^{1/2}|\), using the Dynkin grading. We obtain

\[
A_{\widetilde V_n}=
\frac{\prod_{\alpha>0,\ (x_n,\alpha)>0}
 2\sin(\pi(x_n,\alpha)/3)}
 {2^{r_{1/2}/2}3^{r_0+(n-1)/2}}.
\]

Positive roots are \(e_i-e_j\) with \(i<j\), and their grades are \(x_i-x_j\). The complete grade counts are:

| Grade | 0 | 1/2 | 1 | 3/2 | 2 |
|---|---:|---:|---:|---:|---:|
| \((3,2,2)\) in \(\mathfrak{sl}_7\) | 2 | 8 | 6 | 4 | 1 |
| \((2,2)\) in \(\mathfrak{sl}_4\) | 2 | 0 | 4 | 0 | 0 |

These counts sum to 21 and 6, the required numbers of positive roots. For the first row the product is
\(1^8(\sqrt3)^6 2^4\sqrt3=16\,3^{7/2}\), while the denominator is \(2^4 3^5\). For the second it is \((\sqrt3)^4=9\), while the denominator is \(3^{7/2}\). Thus

\[
A_{\widetilde V_7}=A_{\widetilde V_4}=3^{-3/2}.
\]

This direct Dynkin computation is important: the first nilpotent has a half-integral Dynkin grading. Using only an even left-adjusted grading and then asserting self-duality in that grading would not check the correct hypotheses. Here the data and self-duality use the same Dynkin conformal structure.

As a separate check against the written proof of Theorem 8.8, the left-adjusted grade counts are \((r_0,r_1,r_2)=(6,12,3)\) for \((3,2,2)\), and \((2,4,0)\) for \((2,2)\). They yield the same \(A\). We have therefore verified the particular grading-independence comparison needed here without relying on the sentence in Lemma 8.6 that leaves the type \((q^m,(q-1)^2)\) argument to analogous calculations.

### Comparison with the affine algebra and conclusion

For \(L_{-4/3}(\mathfrak{sl}_2)\), Corollary 3.9 with \(p=2,q=3\) gives

\[
w=0,\qquad g=(1-2/6)\cdot3=2,\qquad
A=\frac{2\sin(\pi/2)}{3\sqrt{12}}=3^{-3/2}.
\]

Every hypothesis of Theorem 3.10 is now checked. The two affine homomorphisms therefore identify both simple W-algebras with this same simple affine algebra. Composing one isomorphism with the inverse of the other proves the original exact statement.

For an independent conformal normalization check, AVM (21) gives

\[
c=\dim\mathfrak g_0-\tfrac12\dim\mathfrak g_{1/2}
  -\frac{12}{k+n}|\rho-(k+n)x_n|^2.
\]

For \(n=7\) the ingredients are \((\dim\mathfrak g_0,\dim\mathfrak g_{1/2},|\rho-(7/3)x_7|^2)=(10,8,7/3)\), giving \(c=-6\). For \(n=4\) they are \((7,0,13/9)\), again giving \(c=-6\). The affine value is \((-4/3)\cdot3/(2/3)=-6\). Central charge equality is a check, not a replacement for the collapse criterion.
