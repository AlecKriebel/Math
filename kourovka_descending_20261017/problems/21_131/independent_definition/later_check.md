# Later-definition audit: Rozhkov 2022

Checkpoint: 2026-10-24 18:27:52 UTC. Definition/scope audit complete: **100%**. No proof, research computation, Git action, publication, or outreach performed. This percentage concerns this source audit only.

## Primary evidence

Article: A. V. Rozhkov, *AT-groups that are not AT-subgroups: Transition from ATω-groups to ATΩ-groups*, 2022, 28(1), 218–231; DOI [10.21538/0134-4889-2022-28-1-218-231](https://doi.org/10.21538/0134-4889-2022-28-1-218-231).

- Requested [MathNet record](https://www.mathnet.ru/rus/timm1893) and [MathNet full text](https://www.mathnet.ru/php/getFT.phtml?jrnid=timm&paperid=1893&what=fullt): repeated timeouts in this audit.
- Successful [publisher page](https://journal.imm.uran.ru/2022-v.28-1-pp.218-231), saved unchanged as `sources/later_check_publisher.html`.
- Successful [publisher PDF](https://journal.imm.uran.ru/sites/default/files/content/28_1/TrIMMUrORAN_2022_1_p218_L.pdf), saved unchanged as `sources/later_check_rozhkov_2022.pdf` (257008 bytes; SHA-256 `004cc7f54d6881c96ca0a27d5a3011db34380474391974c556dc061a8e25fd46`). Full PDF text was inspected independently, especially printed pp. 219–220 (PDF pages 2–3); findings below do not rely on the abstract.

## Definition and scope findings

Section 1, pp. 219–220, Definitions 1–3: arbitrary sets \(A_i\), \(|A_i|\ge2\), define the rooted word tree. Rooted generators have only their root label nonidentity. Each longitudinal generator has its own ray \(\gamma\), with nonidentity labels allowed only at
\[
u=\gamma_0\cdots\gamma_{n-1}a_n,\qquad a_n\ne\gamma_n.
\]
For \(G=\langle C,D\rangle\), AT means
\[
\Pi_0=\langle c(\varnothing):c\in C\rangle\text{ transitive on }A_0,
\quad
\Pi_n=\langle f(u):f\in D,\ |u|=n\rangle\text{ transitive on }A_n\quad(n\ge1).
\]

Definitions 7–8, p. 220:

- **Regular AT:** the underlying sets are groups; accompanying permutations are translations in their regular representations.
- **ATω:** regular AT over cyclic groups of prime order; \(\omega=(p,q,\ldots)\), so primes may vary.
- **ATΩ:** regular AT over cyclic groups of arbitrary finite order (at least two, by the initial convention).

Thus these are subclasses of general AT, not replacement definitions. General AT has no finite branching, finite generation, periodicity, or fixed-prime assumption. The paragraph immediately after Definition 3 explicitly includes a free group of rank three as AT. Periodic, finitely generated, or p-group scope requires an additional hypothesis.

## Comparison boundary

Compared with the original-definition evidence supplied by the parent auditor, the later definition preserves the arbitrary-set/transitivity framework, but the literal longitudinal-generator definitions differ: the 1986 text, p. 574, explicitly requires infinite coordinate-level support, whereas 2022 Definition 2 states only the portrait-support implication above and does not explicitly require infinite support. Therefore this audit does **not** assert equivalence of the two resulting group classes. The 1986 presentation uses a subgroup C where the 2022 presentation uses a set C; this is a presentation-level normalization through generation. This audit does not independently certify the 1986 wording.

The scope expansion emphasized by the 2022 title is from the previously favored prime-cyclic subclass to finite-cyclic regular AT; it does not identify either subclass with all AT-groups.

No remaining access gap for this article's full definition: the publisher copy resolves the MathNet download failure. No conclusion about Kourovka 21.131 itself is asserted.
