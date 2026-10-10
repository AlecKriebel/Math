# EP-509 / problem 2150: a bounded component-clustering attempt

## Outcome and exact scope

**The unrestricted problem is not solved or refuted.** This attempt gives an exact covering formula for the restricted family

\[
p(z)=(z-a)^n-c,
\qquad a,c\in\mathbb C,\quad n\ge 1,
\]

an explicit obstruction to covering components separately, and a finite partition reduction that retains the endpoint in the original problem. These are independently written proofs, not a claim of literature novelty. In particular, they are not an improvement of the previously known general bound 2.59 and do not reclassify the known connected case as new progress.

The original target is a cover of the **entire closed region**
\(E_p=\{z:|p(z)|\le1\}\), with total disk radii at most 2, for every monic nonconstant complex polynomial. Disconnected regions and exact equality at 2 are included. In this note, a disk is closed, and a covering family is finite or countable, as in the historical formulation. Arbitrarily many radius-zero singleton sets are not an alternative interpretation of the problem.

## 1. Covering content is a finite component-partition minimum

For a nonempty compact set \(K\subset\mathbb C\), write

\[
\operatorname{rad}(K)=\min_{w\in\mathbb C}\max_{z\in K}|z-w|.
\]

This minimum exists: the objective is continuous and tends to infinity as \(|w|\to\infty\). Let \(\mathcal C(K)\) be the infimum of total radii over finite or countable disk covers of \(K\).

**Proposition 1.** If \(K\) has finitely many connected components \(K_1,\ldots,K_m\), then

\[
\boxed{\quad
\mathcal C(K)=
\min_{\mathcal P}\sum_{B\in\mathcal P}
\operatorname{rad}\!\left(\bigcup_{j\in B}K_j\right),
\quad}                                                     \tag{1}
\]

where \(\mathcal P\) ranges over all set partitions of \(\{1,\ldots,m\}\). In particular, the infimum is attained by at most \(m\) disks.

**Proof.** Two intersecting disks of radii \(r,s\) can be replaced by one disk containing both and of radius at most \(r+s\). Indeed, if their center distance is \(d\), containment of one in the other settles one case; otherwise their smallest enclosing disk has radius \((d+r+s)/2\le r+s\), with center on the segment joining their centers.

Apply this replacement repeatedly to a finite cover, including when two disks merely touch. The process terminates with pairwise disjoint closed disks and never increases total radius. A connected set contained in a finite union of pairwise disjoint closed disks lies in just one disk. Thus each \(K_j\) lies in one surviving disk. Discard disks containing no component. The resulting assignment gives a partition, whose sum in (1) is no greater than the original cover cost. Conversely, the circumdisks for any partition cover \(K\). There are only finitely many partitions, so the finite-cover infimum is the displayed minimum and is attained.

For a countable cover of finite total radius \(R\), enlarge disk \(j\)'s radius by \(\varepsilon2^{-j}\), using open disks. Compactness gives a finite subcover with total radius at most \(R+\varepsilon\). Replace these by closed disks and use the preceding argument. The minimum in (1) is at most \(R+\varepsilon\) for every \(\varepsilon>0\), hence at most \(R\). This proves the same formula for countable covers, with no endpoint loss. \(\square\)

For a degree-\(n\) polynomial, \(E_p\) has at most \(n\) components. Here is a short justification. Every component \(U\) of \(\{|p|<1\}\) is bounded and has \(|p|=1\) on its boundary. Its closure is compact. If it contained no zero, the minimum-modulus principle would contradict the interior minimum of \(|p|\), which is less than 1. Each such component therefore contains a root, so there are at most \(n\) of them. The open-mapping theorem gives \(E_p=\overline{\{|p|<1\}}\). Since this is a finite union of closures of connected sets, it too has at most \(n\) components.

**Endpoint consequence.** For a fixed polynomial, covers of costs \(2+\varepsilon\) for every \(\varepsilon>0\) imply an attained cover of cost at most 2. Merely having a single estimate \(2+\varepsilon_0\), or an asymptotic estimate across a changing sequence of polynomials, does not have this consequence. Formula (1) does not prove the missing bound on its minimum.

## 2. An elementary fractional-power disk lemma

**Lemma 2.** Let \(0<\alpha<1\) and \(0<\ell<u\). The principal power \(w\mapsto w^\alpha\) maps the closed disk with real diameter \([\ell,u]\) into the closed disk with real diameter \([\ell^\alpha,u^\alpha]\).

**Proof.** Put
\[
I_\alpha=\int_0^\infty\frac{s^{\alpha-1}}{1+s}\,ds\in(0,\infty).
\]
For \(\operatorname{Re}w>0\),
\[
w^\alpha=I_\alpha^{-1}
\int_0^\infty\frac{w}{t+w}\,t^{\alpha-1}\,dt.                 \tag{2}
\]
To verify (2), the integral converges locally uniformly and is analytic on the right half-plane. For positive real \(w\), substitution \(t=ws\) gives the identity. The identity theorem gives it throughout that half-plane.

For each \(t>0\), the real Möbius map \(h_t(w)=w/(t+w)\) maps the disk with diameter \([\ell,u]\) onto the disk with diameter \([h_t(\ell),h_t(u)]\). Its pole is outside the input disk; it maps its boundary circle to a circle symmetric about the real axis, with those two real endpoints, and maps the interior to the bounded side. Consequently,
\[
\left|h_t(w)-\frac{h_t(\ell)+h_t(u)}2\right|
\le\frac{h_t(u)-h_t(\ell)}2.
\]
Integrate this inequality with the positive weight \(I_\alpha^{-1}t^{\alpha-1}\), and apply (2). The result is
\[
\left|w^\alpha-\frac{\ell^\alpha+u^\alpha}2\right|
\le\frac{u^\alpha-\ell^\alpha}2,
\]
which proves the lemma for every point of the closed disk. \(\square\)

The case \(\alpha=1\) is immediate. The limiting case \(\ell=0\), when needed, follows by continuity, although the disconnected-family argument below uses only \(\ell>0\).

## 3. A regular-polygon obstruction to intermediate groupings

**Lemma 3.** For \(n\ge2\), any disk containing \(k\ge2\) distinct vertices of a regular \(n\)-gon of circumradius \(b\) has radius at least \(kb/n\).

**Proof.** Normalize \(b=1\), and let the disk radius be \(\rho\). If \(\rho\ge1\), the claim is immediate. If \(\rho<1\), its intersection with the unit circle lies in an arc of length at most \(2\arcsin\rho\le\pi\). To see this bound, if the center has distance \(d>0\) from zero, the half-angle \(\theta\) of the arc satisfies
\[
\cos\theta=\frac{1+d^2-\rho^2}{2d}\ge\sqrt{1-\rho^2}.
\]
The inequality follows from \((d-\sqrt{1-\rho^2})^2\ge0\). A disk centered at zero with \(\rho<1\) contains no unit-circle point.

An arc containing \(k\) vertices must span at least \(2\pi(k-1)/n\). Hence \((k-1)/n\le1/2\) and
\[
\rho\ge\sin\!\left(\frac{\pi(k-1)}n\right)
\ge\frac{2(k-1)}n\ge\frac{k}n.
\]
The middle inequality is the chord bound \(\sin(\pi x)\ge2x\) on \([0,1/2]\), and the last uses \(k\ge2\). Rescale by \(b\). \(\square\)

## 4. Exact solution of the translated-binomial family

Translation and rotation reduce \((z-a)^n-c\) to \(z^n-t\), where \(t=|c|\ge0\): if \(c=t e^{i\theta}\), write \(z-a=e^{i\theta/n}w\). The multiplying phase has modulus one and disk radii are unchanged. For \(n=1\), the region is a unit disk and its covering content is 1 by Proposition 1.

**Theorem 4.** Let \(n\ge2\), and put
\[
b=(t+1)^{1/n}.
\]
Then the exact minimum total radius is
\[
\boxed{
\mathcal C(\{|z^n-t|\le1\})=
\begin{cases}
b,&0\le t\le1,\\[2mm]
\min\!\left\{b,\ \dfrac n2\big((t+1)^{1/n}-(t-1)^{1/n}\big)\right\},&t>1.
\end{cases}}                                               \tag{3}
\]
This is an equality for the full closed region and arbitrary finite/countable covers.

**Proof for \(0\le t\le1\).** The region is star-shaped about zero: for \(z\) in the region and \(0\le\lambda\le1\),
\[
|(\lambda z)^n-t|
\le\lambda^n|z^n-t|+(1-\lambda^n)t\le1.
\]
It is therefore connected. It is contained in \(|z|\le b\), and it contains all \(n\) points \(b\omega_j\), where \(\omega_j=e^{2\pi i j/n}\). No disk of radius smaller than \(b\) contains all these points, since for any center \(w\),
\[
\frac1n\sum_j|b\omega_j-w|^2=b^2+|w|^2\ge b^2.
\]
Proposition 1 now gives exactly \(b\), including \(t=1\).

**Proof for \(t>1\).** Put
\[
a=(t-1)^{1/n},\qquad r=(b-a)/2,\qquad s=(a+b)/2.
\]
The disk \(D(t,1)\) avoids zero. Its inverse image under the power map consists of the \(n\) disjoint connected compact sets
\[
K_j=\{\omega_j w^{1/n}:w\in D(t,1)\}.
\]
They are exactly the components: the analytic inverse branches exist on a neighborhood of the disk and their images cannot intersect without a zero value or equal branches. Lemma 2 gives
\[
K_j\subset D(s\omega_j,r).
\]
Both \(a\omega_j\) and \(b\omega_j\) belong to \(K_j\), so this disk is a smallest circumdisk and \(\operatorname{rad}(K_j)=r\).

Two available covers are now the one disk \(D(0,b)\) and the \(n\) disks \(D(s\omega_j,r)\), costing \(b\) and \(nr\).

It remains to exclude every intermediate grouping, rather than assuming symmetry forces an optimum. Use Proposition 1. For a block of one component the cost is \(r\). For a block of \(k\ge2\) components, its union contains \(k\) distinct outer points \(b\omega_j\); Lemma 3 makes its circumradius at least \(kb/n\).

If \(r\le b/n\), every block of size \(k\) costs at least \(kr\), including singleton blocks. Every partition therefore costs at least \(nr\). If \(r\ge b/n\), every block of size \(k\) costs at least \(kb/n\), again including singleton blocks. Every partition then costs at least \(b\). These lower bounds match the two explicit covers and prove (3). \(\square\)

**Corollary 5 (exact worst parameter in this family).** Put
\[
q_n=(1-2/n)^n,\qquad
 t_n=\frac{1+q_n}{1-q_n},\qquad
 M_n=\left(\frac{2}{1-q_n}\right)^{1/n}.
\]
Then
\[
\sup_{c\in\mathbb C,\ a\in\mathbb C}
\mathcal C(\{|(z-a)^n-c|\le1\})=M_n<2,                       \tag{4}
\]
with the maximum attained at \(|c|=t_n\). For \(n=2\), \(q_2=0\), \(t_2=1\), and \(M_2=\sqrt2\). For example, \(M_3=(27/13)^{1/3}\) and \(M_4=(32/15)^{1/4}\).

**Proof.** On \(t\ge1\), \(b\) strictly increases, while \(n(b-a)/2\) strictly decreases on \(t>1\), as follows by differentiating and using \(1/n-1<0\). Their crossing satisfies
\[
\frac ab=1-\frac2n,\qquad \frac{t-1}{t+1}=q_n,
\]
which gives the displayed parameters. For \(n=2\) the crossing is the endpoint \(t=1\); otherwise it is in \(t>1\). The increasing connected-case value is no larger than this maximum. Finally \(q_n\le1-2/n\), hence \(M_n^n\le n<2^n\). \(\square\)

## 5. Why separate component covers cannot prove the general conjecture

Take the explicit monic quartic
\[
p(z)=z^4-\left(1+\frac1{65536}\right).
\]
It has four disjoint components. In Theorem 4's notation,
\[
a=\frac1{16},\qquad b^4=\frac{131073}{65536}.
\]
The elementary rational comparisons
\[
\left(\frac{19}{16}\right)^4
=\frac{130321}{65536}<b^4
<\left(\frac65\right)^4
\]
show that
\[
\sum_{j=1}^4\operatorname{rad}(K_j)
=2(b-1/16)>\frac94>2,
\qquad
\mathcal C(E_p)=b<\frac65.
\]
The equality \(\mathcal C(E_p)=b\) follows from (3), or from \(b>1/8\), which makes \(2(b-1/16)>b\). Thus the example refutes a **componentwise additive covering route**, not EP-509. Giving each component its own collection of disks does not repair that route: Proposition 1 applied to each connected component makes its separate covering cost at least its circumradius.

More generally, for \(n\ge2\) and \(p_n(z)=z^n-(1+16^{-n})\), each component has diameter at least \((2+16^{-n})^{1/n}-1/16>15/16\). Consequently the sum of separate component costs exceeds \(15n/32\), while the whole region lies in the common disk of radius \((2+16^{-n})^{1/n}\), which tends to 1. The loss from forbidding cross-component grouping is therefore unbounded as degree grows.

## 6. Attempted general step, source check, and precise residual

The attempted route was to combine connected-component circumradius estimates through (1). Section 5 proves that taking the singleton partition cannot work. The regular-polygon outer-point argument controls all intermediate partitions for binomials, but general polynomials do not supply equally spaced outer witnesses or a common fractional-power parametrization. No replacement controlling the best partition for unrestricted root configurations was established.

Pommerenke's 1960 paper was newly recovered and inspected for this attempt. Its pp.147–149 obtain a surrounding contour-length bound and then multiply by 1/4 to obtain disk radii. The optimized displayed length estimate is \(2\pi\sqrt e\) times capacity, leading to \(\pi\sqrt e/2\), rounded to 2.59. On p.143 he reports a prior example preventing a universal surrounding-length bound below 8.248 times capacity. Therefore reducing this same contour-length target to 8 is not a viable general route. The cited 1959 example itself was not retrieved or independently reproved here; the negative source statement is credited to Pommerenke, not presented as a newly verified construction. This contour discussion is not needed in the proofs of Sections 1–5.

What remains is exactly: prove that the minimum in (1) is at most 2 for every monic polynomial, or give a polynomial for which that minimum is greater than 2. The family formula does neither for general polynomials. The prior general 2.59 result and known connected-case 2 result remain prior work. No general 2+epsilon bound, counterexample to EP-509, or literature-priority claim is made.

## References and credit

- P. Erdős, “Some unsolved problems” (1961), printed p.246. Original problem, normalization, and historical bounds. https://users.renyi.hu/~p_erdos/1961-22.pdf
- Ch. Pommerenke, “Einige Sätze über die Kapazität ebener Mengen,” Mathematische Annalen 141 (1960), 143–152; especially pp.143 and 147–149. https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0141/LOG_0031.pdf
- Exact catalog alias: Hayman's Research Problems in Function Theory, Problem 4.7, AMR-022-4007 / problem 2304007. This identifies the duplicate target; no fresh inspection of that full book is claimed. https://arxiv.org/abs/1809.07200

The disk-merging, compactness, power-integral, and regular-polygon arguments above are included in full to make the restricted-family conclusion independently checkable. They use elementary standard tools, and this attempt does not establish whether the resulting exact family formula already appears elsewhere.

## Publication-edition scope

This AI-assisted work is unrefereed. Acceptance means an independent internal
AI mathematical audit, without external human peer review, journal acceptance,
or proof-assistant certification. The complete original written mathematics
above is preserved without correction. It is independently checkable as prose,
including the analytic quartic construction and its exact comparisons.

Supplementary checking programs, scalar certificates, raw computational data,
and copied scholarly PDFs, scans, OCR, and source text are not included. The
supplementary computational runs cannot be replayed from this edition alone;
their hashes and aggregate results are verification metadata, not substitutes
for proof. The analytic and topological conclusions rest on the complete
written arguments. Source-inspection descriptions refer to the original
attempt and independent audit, with no new source inspection for this edition.
The 1959 construction is credited through Pommerenke's report and remains
unverified here. No novelty, priority, improved general bound, or unrestricted
solution is claimed.
