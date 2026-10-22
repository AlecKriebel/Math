# Analytical adversarial controls

These are exact mathematical countermodels and boundary checks. They are not simulations or finite evidence for a Baire conclusion. They test which hypotheses carry the argument in DERIVATION.md.

## 1. A single bad boundary does not yield generic failure

Fix \(b=1/2\). For each \(n\), let \(J_n=[\lfloor nb\rfloor/n,(\lfloor nb\rfloor+1)/n)\). Define a synthetic rank-cell law \(T_n(t)\) by

\[
\mathcal L(T_n(t))=\begin{cases}(\delta_0+\delta_n)/2,&t\in J_n,\\\delta_0,&t\notin J_n.\end{cases}
\]

This law depends only on \(\lfloor nt\rfloor+1\), so it has the actual locality required in the proof. At \(b\), \(T_n(b)/n\) is exactly a two-atom equal-weight mixture, and for fixed \(M\), its square-root concentration equals \(1/2\) once \(n>4M^2\). But every fixed \(t\ne b\) eventually leaves \(J_n\), since all its points are within \(1/n\) of \(b\). Then \(T_n(t)=0\) for all sufficiently large \(n\). Centering by zero makes the entire sequence tight: only finitely many earlier finite-valued distributions remain. Thus one bad boundary is insufficient. Density of bad boundaries is used essentially.

## 2. Relative local constancy alone does not connect deleted boundary points

On \((0,1)\), define

\[
\mathcal L(T_n(t))=\begin{cases}(\delta_0+\delta_n)/2,&t\in\mathbb Q,\\\delta_0,&t\notin\mathbb Q.\end{cases}
\]

The bad points are dense, and at each such point the normalized law has the required equal-weight two-atom limit. On \(X=(0,1)\setminus\mathbb Q\), every concentration function is identically one, hence locally constant and continuous. Nevertheless every point of \(X\) admits zero centering and is tight. This model fails the exact rank-cell identity: bad boundary values do not propagate to neighboring irrational points. Therefore dense bad values on the removed set together with relative continuity on \(X\) do not suffice as an abstract lemma. DERIVATION.md explicitly uses the stronger identity \(C_n(t,M)=C_n(b,M)\) when \(\lfloor nt\rfloor=\lfloor nb\rfloor\), which is automatic for the actual rank process. This negative control does not falsify the actual theorem; it isolates a necessary transfer assumption.

## 3. Atom weights determine the usable concentration threshold

Let \(\mathcal L(T_n(t))=(9/10)\delta_0+(1/10)\delta_n\) for all \(t\). Every rank has a nondegenerate two-atom limit under division by \(n\), and the law is constant on all rank cells. For fixed \(M\) and \(n>4M^2\), an interval of length \(2M\sqrt n\) cannot cover both atoms, so its maximal concentration is exactly \(9/10\). The \(3/4\) threshold sets are then all of \(X\) for sufficiently large starting index, and the proposed \(3/4\)-threshold residual construction is empty. Yet every deterministic centering fails tightness, because every such interval misses probability at least \(1/10\). A threshold above \(9/10\), such as \(19/20\), would work with this law.

The actual boundary mixture has largest atom mass \(1/2\), so \(3/4\) is strictly above it. Distinct atoms alone would not justify the particular \(3/4\) threshold. More generally a fixed maximal atom mass \(\alpha<1\) allows any threshold in \((\alpha,1)\).

## 4. Membership in one E-set is not tightness

The law in Control 3 has \(C_n(t,M)\ge9/10>3/4\) for every fixed positive \(M\), yet no deterministic centering is tight. Thus membership in \(E_{M,N}\) is not a characterization of the existence of a tight centering. The valid implication in DERIVATION.md is only: existence of a tight centering implies membership in some \(E_{M,N}\). Its residual complement consequently supplies a sufficient set of bad ranks. Tightness concerns every error level; a single error level does not suffice.

## 5. Category gives no Lebesgue measure classification

Enumerate the rational points of \((0,1)\) as \(x_1,x_2,\ldots\). For each positive integer \(j\), let

\[
O_j=\bigcup_{\ell\ge1}\left((x_\ell-2^{-(j+\ell+3)},x_\ell+2^{-(j+\ell+3)})\cap(0,1)\right).
\]

Every \(O_j\) is open and dense, because it contains all rationals. Its Lebesgue measure is at most \(2^{-j-2}\), by summing interval lengths. Baire's theorem makes \(\bigcap_jO_j\) a dense \(G_\delta\), while its measure is zero. Intersecting it with the irrationals remains a dense \(G_\delta\) of measure zero. Thus even the same ambient category type as the theorem's \(R\) is compatible with zero measure. No almost-everywhere classification can be inferred from the category conclusion.

## 6. Source-specific cancellations and the memoryless control

For the root split of the actual stationary source, the codes \(0\,111\ldots\) and \(1\,000\ldots\) have equal profiles, each equal to two. They have no profile jump. The proof correctly excludes the root while retaining every nonroot interior split.

For the symmetric source with \(q=1/2\), all depth-\(d\) cylinder masses are \(2^{-d}\). Every profile equals \(\sum_{d\ge0}2^{-d}=2\), and every boundary jump vanishes. More generally the nonroot jump for the symmetric stationary transition source with stay probability \(q\in(0,1)\) is \(\pm(4q-2)\pi(W)\); this follows from the same geometric sums since the change probability is \(1-q\). In particular the zero-jump case lies exactly at \(q=1/2\). A boundary law there has coincident profile atoms, and the separated-band concentration argument cannot apply. The category argument would be unsupported if one imported the nonzero-jump premise into that memoryless case.

## 7. Rational coincidences and endpoint rounding

The actual nonroot split of the cylinder \(W=0\) is \(b=3/8\). At \(n=8\), \(nb=3\) and the selected rank is \(\lfloor nb\rfloor+1=4\). Its cell is \([3/8,1/2)\), with a positive right-hand part. At \(n=9\), its cell is \([1/3,4/9)\), and the right-hand part \((3/8,4/9)\) again has positive length. Deleting the countable set \(D\cup\mathbb Q\) cannot empty either open interval. The general identity is

\[
0<(\lfloor nb\rfloor+1)/n-b\le1/n.
\]

This holds for every real \(b\in(0,1)\) and every \(n\). The proof therefore works along the infinitely many exact-grid coincidences of a rational boundary as well as between them. The binomial side probability likewise uses \(0<\lfloor nb\rfloor+1-nb\le1\), whose normalized rounding error tends to zero.

## 8. Singleton stopping is essential to the cost's finiteness

For a selected input string \(S_{(k)}\), once its bucket is a singleton, the untruncated count equals one at every deeper prefix. The alternative sum \(\sum_d\Lambda_{n,d}(S_{(k)})\), without the indicator, would therefore diverge to infinity. The exact singleton-stopping indicator is essential, not a harmless convention. The direct cost bound in DERIVATION.md eliminates all deep terms only on an event where every bucket is a singleton or empty. For \(n=1\), the actual cost is zero; the empirical-grid estimate is deliberately formulated for \(n\ge2\), so no small-sample singularity is used.

## 9. Eventual estimates suffice, and no uniform boundary rate is hidden

At a fixed bad boundary the two-atom limit implies \(C_n(b,M)<3/4\) for every sufficiently large \(n\), for that fixed \(b,M\). The nowhere-density proof first chooses one boundary in the given open interval and then one sufficiently large \(n\ge N\). It does not require a common threshold in \(n\) for all boundaries. For a residual rank, the resulting failures occur at arbitrarily large indices for each radius; they need not occur at every index. Tightness is nevertheless excluded by the fixed positive tail lower bound in every radius. Any finite initial segment of proper laws is tight and cannot repair this persistent subsequence obstruction.

## 10. Square-word and publication-scope control

The theorem does not compute the candidate's square-word rank or its membership in \(R\). An explicit nonboundary witness can be established by a separate mechanism without being shown to belong to this particular residual set. Likewise, an implication assembled from published ingredients does not establish that the implication itself was historically published. These distinctions are logical boundaries, not failures in the proved category theorem.
