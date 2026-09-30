# No open cover admits exact root selections in the printed Problem 2A

**Status:** Complete literal-source obstruction; separate adversarial review is pending. The argument is the classical square-root monodromy obstruction applied to a parameter slice. No historical-priority or new-discovery claim is made. The intended finite-genus variant, if different from the printed question, is not silently substituted.

## 1. Exact statement and answer

Write the six real coefficients as
\[
 a(x,y)=a_1x+a_2y+a_0,\qquad
 b(x,y)=b_1x+b_2y+b_0.
\]
The parameter space is all of \(\mathbb R^6\), and the equations are
\[
 x^2-y^2+a(x,y)=0,\qquad xy+b(x,y)=0.
\tag{1}
\]
An admissible open set U, in the usual coefficient-space topology, must have a continuous function \(\varphi:U\to\mathbb R^2\) selecting an **exact** solution of (1) at every parameter in U.

**Theorem.** No open neighborhood of the zero coefficient vector admits such a selection. Consequently, there is **no open cover of all \(\mathbb R^6\)** by admissible sets, regardless of the cover's cardinality. In the extended convention assigning \(+\infty\) when no finite section cover exists, the covering number is \(+\infty\). More precisely, the class of such covers is empty; a countably or uncountably infinite admissible cover does not repair the problem.

This answers the exact all-parameter, open-set, exact-section formulation printed in Problem 2A of Vassiliev's article [1, p. 205]. It does not compute a genus after removing a ramification set, or the approximate-selection quantity in the separately numbered Problem 2B.

## 2. The constant-coefficient slice

For \(\zeta=u+iv\in\mathbb C\), define the parameter embedding
\[
 \iota(\zeta)=(a_1,a_2,a_0,b_1,b_2,b_0)
             =(0,0,-u,0,0,-v/2).
\tag{2}
\]
This is an injective continuous real-linear map, and \(\iota(0)=0\). On this slice, equations (1) become
\[
 x^2-y^2=u,\qquad 2xy=v,
\]
which are exactly
\[
 (x+iy)^2=\zeta.
\tag{3}
\]
In particular there are no additional real solutions on this slice through which a selection could evade the two square-root branches. At \(\zeta=0\), the only real solution is \((0,0)\). Algebraic multiplicity does not change its value as a point of \(\mathbb R^2\).

Suppose U is open, contains the zero parameter, and has a continuous exact selection. Then \(\iota^{-1}(U)\) is an open neighborhood of zero in \(\mathbb C\), so it contains a disk \(D_r=\{|\zeta|<r\}\), for some \(r>0\). Composing the selection with \(\iota\) and identifying \(\mathbb R^2\) with \(\mathbb C\) gives a continuous function s on \(D_r\) satisfying
\[
 s(\zeta)^2=\zeta.
\tag{4}
\]
We next rule this out directly.

## 3. An elementary closed-loop contradiction

Define a continuous path \(\gamma:[0,2]\to\mathbb C\setminus\{0\}\) by
\[
 \gamma(t)=
 \begin{cases}
 1-t+it,&0\le t\le1,\\
 1-t+i(2-t),&1\le t\le2.
 \end{cases}
\tag{5}
\]
It follows the two line segments from 1 to i and then to −1. The formulas agree at t=1. On both segments \(|\gamma(t)|\le1\), and \(\gamma(t)\ne0\). The endpoint values are \(\gamma(0)=1\), \(\gamma(2)=-1\).

Choose \(c>0\) with \(c^2<r\), and put
\[
 \zeta(t)=c^2\gamma(t)^2.
\]
This is a closed parameter loop contained in \(D_r\): its two endpoint values both equal \(c^2\). If (4) held, the function
\[
 q(t)=\frac{s(\zeta(t))}{c\gamma(t)}
\tag{6}
\]
would be continuous and satisfy \(q(t)^2=1\). Thus it takes values in \(\{1,-1\}\) and is constant, because \([0,2]\) is connected. But the numerator has the same value at t=0 and t=2, while the denominator changes sign. Hence \(q(2)=-q(0)\), a contradiction.

This proves that the open neighborhood U cannot have an exact continuous root selection. Every open cover of \(\mathbb R^6\) has at least one member containing the zero coefficient vector; that member would be such a U. The theorem follows. \(\square\)

The proof uses openness at the ramified parameter, not merely absence of a single global branch. It is therefore stronger than a lower bound of two for a cover of a punctured parameter space. Disconnectedness of an open set does not help, since its component containing the zero parameter still contains a neighborhood of that parameter.

## 4. Reconciling the source's square-root remark

I inspected the complete Section 2 in the original arXiv manuscript, the journal's HTML text, and the final published PDF, including a rendered view of p. 205. All three specify open sets covering **all** of \(\mathbb R^6\), with exact continuous selections. No discriminant or ramification locus is removed from Problem 2A. Problem 2B then explicitly relaxes exactness to an approximation requirement.

The next paragraph of the source says that the complex model \(z^2=A\) has covering number two. Under the printed open-set/exact-section definition, this assertion requires a domain qualification: it is true over \(\mathbb C\setminus\{0\}\), but not over all of \(\mathbb C\).

Here is the distinction explicitly. The two open sets
\[
 V_1=\mathbb C\setminus(-\infty,0],\qquad
 V_2=\mathbb C\setminus[0,\infty)
\]
cover the punctured plane. Continuous choices of argument in \((-\pi,\pi)\) and \((0,2\pi)\), respectively, give a continuous square root on each. The loop argument above rules out a single branch on the entire punctured plane, so its covering number is exactly two. Neither of those open sets contains zero. Adding zero to a slit domain does not make it an open neighborhood of zero, and any genuinely open neighborhood of zero has the obstruction in Section 3.

This explains the scope distinction without presuming the author's intended repair. Removing a suitable ramification set, permitting a different type of cover, replacing strict sections by another notion, or asking for approximate solutions changes the problem. The present argument does not resolve those altered questions.

In particular it does not answer Problem 2B. Already on the constant-coefficient slice, for a fixed \(\varepsilon>0\), the constant value zero is within \(\varepsilon\) of a square root whenever \(|\zeta|<\varepsilon^2\). Thus the exact local obstruction used here does not persist unchanged for approximate selections.

## 5. Provenance and finite diagnostics

The imported report correctly reproduces the six-parameter polynomial family, but retains a finite-cover question between two and a larger number. It does not address the local obstruction at the zero parameter. No prior Alec/campaign attempt or matching PR for this target was found; the upstream report is credited as prior source triage, not treated as an author/campaign attempt. Problem 2B is a separate adjacent record.

Bounded searches for the exact title, Problem 2A, and a correction did not locate a primary erratum or later reformulation. That does not establish priority or prove that no correction exists. The conclusion here is confined to the text actually recovered and visually verified.

The accompanying exact checker verifies the slice coefficients, the polynomial identities, and rational controls for the two-segment loop. A finite loop sample does not prove the nonexistence of a continuous section: connectedness of the interval and the two-valued ratio in (6) are the topological proof. No heavy search, root solver, or numerical continuity inference is used.

## Primary source

[1] V. A. Vassiliev, *A Few Problems on Monodromy and Discriminants*, Arnold Mathematical Journal 1 (2015), 201–209, DOI [10.1007/s40598-015-0011-9](https://doi.org/10.1007/s40598-015-0011-9), Section 2, p. 205. [Final published PDF](https://armj.math.stonybrook.edu/pdf-Springer-final/015-0011-9.pdf); [journal HTML](https://armj.math.stonybrook.edu/html-articles/Files-2015-2024/15-11/); [original primary preprint](https://arxiv.org/abs/1504.01997). The final published statement, not only the dataset extraction, was checked.
