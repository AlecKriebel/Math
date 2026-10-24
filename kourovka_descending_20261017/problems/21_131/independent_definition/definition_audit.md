# Rozhkov AT: original definition and scope audit

Audit timestamp: 2026-10-24 18:32 UTC. Scope: primary definition/scope only; no construction, impossibility argument, or mathematical research beyond source interpretation. Definition audit completion estimate: 95%; original PDF byte/raster verification remains unavailable.

## Original 1986 definition

Primary source: A. V. Rozhkov, *Theory of Aleshin type groups*, Russian original *Mat. Zametki* 40(5) (1986), 572–589; translation *Math. Notes* 40(5), 827–836, DOI [10.1007/BF01159699](https://doi.org/10.1007/BF01159699). [MathNet record](https://www.mathnet.ru/eng/mzm5213). The mathematical definition below follows original Russian printed pp.573–575, read in the primary full-PDF web extraction; it is not replaced by the 2022 definition.

Let

\[
A=(A_0,A_1,\ldots),\qquad |A_i|\ge2,
\quad T=\coprod_{n\ge0}\prod_{i=0}^{n-1}A_i,
\]

ordered by prefix. Sets may be infinite. A mutation changes at most one coordinate of any tuple. Root mutations act only on coordinate 0.

A longitudinal mutation \(d\) has **infinite support**, fixes a directing ray \(\gamma(d)\), and changes only coordinate \(n+1\) when \(n\) is the first coordinate where an input ray differs from \(\gamma(d)\). Its permutation there depends only on \(d,n\), and the differing symbol. In the original convention,

\[
\operatorname{supp}(d)=\{n:\text{some tuple's coordinate }n\text{ is changed by }d\}.
\]

For \(n\ge1\), write \(\pi_n(d,a)\in\operatorname{Sym}(A_n)\) for the accompanying permutation at the vertex

\[
\gamma_0(d)\cdots\gamma_{n-2}(d)a,
\qquad a\ne\gamma_{n-1}(d).
\]

The value for the ray symbol can be taken as identity when indexing over all \(a\in A_{n-1}\).

Choose a **subgroup** \(C\) of root mutations and a **subset** \(D\) of longitudinal mutations. Then

\[
H=\langle C,D\rangle,\qquad
\Pi_0(C)=\langle\pi_0(c):c\in C\rangle,
\qquad
\Pi_n(D)=\langle\pi_n(d,a):d\in D,\ a\in A_{n-1}\rangle\ (n\ge1)
\]

is an AT-group precisely when every \(\Pi_n\) acts transitively on \(A_n\).

Consequences for interpreting the **definition**: each designated \(d\in D\) has infinite support, so the identity cannot belong to \(D\). The subgroup \(C\) includes identity. There is no requirement that \(D\) be a subgroup or that its elements share one ray. Products of members of \(D\) need not be longitudinal mutations. The definition imposes no prime, cyclicity, regularity, finite-generation, periodicity, local-finiteness, or non-local-finiteness hypothesis. The introduction p.572 expressly permits nonperiodic and infinitely generated groups.

## Prime cyclic subclass in the same original source

Original §4, printed p.580, defines \(AT_\omega\) separately:

\[
\omega=(p_0,p_1,\ldots)\quad(p_n\text{ prime}),\quad
A_n=\{0,\ldots,p_n-1\},\quad
\sigma_n=(0\ 1\ \cdots\ p_n-1),
\]

\[
\operatorname{Wr}(\omega)=
\{g\in\operatorname{Aut}(T):\pi(g,v)\in\langle\sigma_{|v|}\rangle
\text{ for every vertex }v\}.
\]

An AT-group on this sequence lying in \(\operatorname{Wr}(\omega)\) is an \(AT_\omega\)-group. The primes may vary; a constant prime sequence is a special case. Periodicity is then a theorem with additional hypotheses (Theorem 1, p.581), not the definition.

## Independent later-primary check and exact difference

Rozhkov (2022), *AT-groups that are not AT-subgroups: Transition from ATω-groups to ATΩ-groups*, *Trudy IMM UrO RAN* 28(1), 218–231, DOI [10.21538/0134-4889-2022-28-1-218-231](https://doi.org/10.21538/0134-4889-2022-28-1-218-231), [publisher record](https://journal.imm.uran.ru/node/1017), [publisher PDF](https://journal.imm.uran.ru/sites/default/files/content/28_1/TrIMMUrORAN_2022_1_p218_L.pdf).

Printed pp.219–220, Definitions 1–3, retain arbitrary sets \(|A_n|\ge2\), root/longitudinal generators, and the transitive accompanying groups. Definition 2 formulates longitudinal portrait support by

\[
d(u)\ne1\Longrightarrow
u=\gamma_0\cdots\gamma_{n-1}a_n,
\quad a_n\ne\gamma_n.
\]

**Exact difference:** this 2022 formulation does not explicitly require infinite support. It can admit finite-support or identity automorphisms as longitudinal under its literal implication. Original 1986 p.574 explicitly requires infinite support. Do not silently substitute the later generator definition, and do not infer equality of the resulting group classes without an argument. Also, 2022 uses a set of root generators where 1986 uses a subgroup; replacing a root-generating set by its generated root subgroup is only a presentation-level normalization.

Definitions 7–8 call an AT-group *regular* when the underlying sets are groups and all accompanying permutations are their regular translations. Regular AT over prime-order cyclic groups is \(AT_\omega\); over arbitrary finite cyclic groups it is \(AT_\Omega\). Both are subclasses, with periodicity separate. Definition 3's following paragraph expressly states that all AT-groups are infinite; finite underlying sets imply residual finiteness; a rank-three free group can be AT.

## Evidence and remaining access gap

- Original PDF primary extraction succeeded twice in this conversation: `turn1109view0` (L0–279) and `turn1123view0` (L169–446). See [preserved relevant OCR receipt](sources/rozhkov_1986_successful_web_excerpt_receipt.md). This receipt clearly labels itself as manually preserved excerpt, not PDF bytes or full tool output.
- Subsequent original-PDF fetches and all direct MathNet file downloads timed out or disconnected. Springer returned a subscription preview, preserved as `sources/rozhkov_1986_probe_4.html`; original English PDF unavailable.
- Original formulas have not been checked against locally rendered original pages. Indexing is normalized above using the later primary definition; the infinite-support wording and subgroup/subset distinction are explicit in the original OCR.
- Actual 2022 publisher PDF is present at `sources/later_check_rozhkov_2022.pdf`, 257008 bytes, SHA256 `004cc7f54d6881c96ca0a27d5a3011db34380474391974c556dc061a8e25fd46`. Its extracted text is `sources/rozhkov_2022_extracted.txt`. Independent check: [later_check.md](later_check.md).
- Failed responses are clearly named failures. No raw original PDF was acquired. The residual gap is original-byte/raster acquisition, not identification of the definition's main scope.

No Git changes, publication, outreach, substantive proof, construction, or computation was performed in this audit.
