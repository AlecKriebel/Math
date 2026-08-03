# Presentation-suggestion audit

Audit date: 2026-08-01 (America/Los_Angeles).

This note records the disposition of seven presentation suggestions received
after an external AI audit. The mathematical proof was rechecked before the
edits, and no suggested change was treated as evidence of correctness by
itself.

1. **Named author and affiliation — applied in part.** The manuscript now
   names Alec Kriebel and gives `Independent Researcher` as the affiliation.
   No email address was added because none was supplied or approved for public
   release; inventing or inferring contact data would be inappropriate.
2. **Less ambiguous title — applied.** The title is now *The quantum
   chromatic number of the G19 join family*. In addition, the joined family is
   denoted `J_n` in the note, removing the collision between the fixed base
   graph `G_19` and the old family notation `G_n` at `n=19`.
3. **Bridge to the standard quantum chromatic number — applied.** The
   projector definition now cites Lalonde's Theorem 2.19 and the foundational
   Cameron–Montanaro–Newman–Severini–Winter paper.
4. **Expand two proof transitions — applied.** The tail lemma now states the
   equal-dimension argument that turns orthogonality inclusions into complement
   equalities. The final proof now displays the cross-color inner-product
   calculation term by term.
5. **Immutable provenance — applied without self-reference.** The manuscript
   identifies audited commit
   `b1944a23707eb69d2f9f25eda0bb73c32cd5500a` and both exact certificate
   SHA-256 digests, supplies a retrievable immutable repository URL and
   project-relative paths, and distinguishes the coverage of the two
   independent obstruction verifiers. The final manuscript commit and
   rendered-PDF hashes are recorded only after the PDF is frozen, in the
   public page and checksum manifest.
6. **GitHub Action — declined.** No workflow was added. This follows the
   author's explicit instruction. The same three verifier commands are run
   locally before publication and their exact scope remains documented.
7. **Expanded bibliography — applied.** The bibliography now includes the
   foundational quantum-coloring paper and Mančinska–Roberson's `G_13` paper,
   and the body explains their relevance.

The manuscript also now includes an explicit AI-assistance and non-peer-review
disclosure. No researcher or other individual was contacted, and no outreach
draft was prepared or sent.

## Final two-review pass

Two further AI reviews were scrutinized on the same date. Their mathematical
claims were checked against Lalonde's arXiv source and against the exact local
artifacts rather than accepted as authority.

1. **Finite-witness framing and Lalonde's notation — applied with a notation
   safeguard.** The abstract and theorem now lead with the fact that the result
   confirms the finite-witness family proposed in Lalonde's Section 4.2:
   $\xi(J_n)=n<\chi_q(J_n)=n+1$. The note retains $J_n$ and explicitly says
   that this is Lalonde's $G_n$, because his notation otherwise gives two
   meanings to $G_{19}$ when $n=19$.
2. **Every fixed rank and dimension — applied.** In Lalonde's Section 2.4.2
   notation, the theorem now records
   $\chi_q^{[d]}(J_n)=\chi_q^{(r)}(J_n)=n+1$ for every $d,r\ge1$. The lower
   bound follows because these are finite-dimensional colorings; the classical
   coloring supplies the matching upper bounds.
3. **Rank-one specialization — applied.** The tail remark displays
   $M=\operatorname{span}(1,\sigma i)$ and all six resulting tail vectors,
   identifies Lalonde's sign as $b=\sigma$, and cites his Theorem 4.5. It also
   states that the higher-rank derivation does not invoke his computer-assisted
   Lemma 4.4.
4. **Core gauge convention — applied.** The coordinate unitary is now typed as
   a map $G:K_1^3\to K_1\oplus K_2\oplus K_3$, and the pullback convention is
   explicitly $M\mapsto G^*MG$.
5. **Published four-coloring — applied.** The note now cites and prints
   Lalonde's Section 4.2 coloring instead of retaining a different valid
   coloring.
6. **Walsh and tail bookkeeping — applied.** The four idempotency equations
   leading to the anticommutators are displayed. The tail proof now states that
   the frames are injective rather than necessarily isometric and formulates
   orthogonality through the exact cross-Gram pullbacks.
7. **PDF metadata — applied.** Both PDFs now embed title, author, subject, and
   keyword metadata. No contact address was inferred or invented.
8. **Graph consistency checks — strengthened.** The exact graph checker now
   verifies absence of a four-clique, Lalonde's published coloring, and
   exhaustive non-three-colorability, hence $\chi(G_{19})=4$.
9. **Provenance labels — reconciled.** The manuscript calls commit `b1944a23`
   the initial algebra-audit snapshot, while the landing page identifies one
   later canonical source snapshot for the current typeset revision together
   with its PDF hashes.
10. **Optional notation changes — declined.** The compact edge notation and
    the local block letters $X,Y,Z$ remain: both are defined, exact, and aligned
    with the certificates, so changing them would add churn without resolving
    an ambiguity.
11. **Automation and outreach — declined.** No GitHub Action was added, per the
    author's instruction. No email, contact draft, or external communication
    was prepared or initiated.
12. **Verifier optimization mode — hardened.** The two assertion-based tools
    now refuse to run under Python's `-O` mode, so stripped assertions can
    never be followed by a misleading `PASS`. Their ordinary and adversarial
    optimized-mode invocations were both tested.
13. **All-$n$ verifier wording — strengthened rather than weakened.** The
    short verifier's former bounded sanity loop was replaced by an exact
    symbolic coefficient replay of the certificate's terminal
    $3nr\le2nr$ contradiction. The independent long verifier continues to
    check the full recurrence in $\mathbb Q[n,f,d]$.

The public action row is also simplified in the final site revision; the
individual verifier and audit links remain available in the verification
section rather than competing with the paper and source links.

## Focused Section 4.2 comparison pass

A further AI review was checked on 2026-08-02 against Lalonde's primary
source and the proof itself.

1. **Three stated obstacles — applied with precise scope.** The paper now
   maps Lalonde's closing Section 4.2 discussion to the fixed-color SOS and
   tail classification, the cross-color plane flip and sector relations, and
   the uniform all-\(n\) packing argument. It says these replace the role
   needed from Lemma 4.6, not that they literally generalize that lemma.
2. **Finitary sphere corollary — applied.** The homomorphism
   \(J_n\to S_{\mathbb C}^{n-1}\) now yields
   \(\chi_q(S_{\mathbb C}^{n-1})\ge n+1\). The accompanying compactness
   sentence is deliberately narrow: Proposition 3.3 rules out a general
   de Bruijn--Erdős extraction, not every conceivable graph-specific
   argument.
3. **Prior \(n=3\) case — applied.** The note now says explicitly that
   \(\chi_q(G_{19})=4\) was already known and that the first new unrestricted
   case is \(J_4\).
4. **Genuinely higher-rank tail — applied after an independent calculation.**
   The rank-two nongraph plane is distinguished from every orthogonal direct
   sum of scalar fixed-color representations by
   \(\dim(E_+\cap E_-)\), which is invariant under the residual labeled-core
   gauge \(\operatorname{diag}(U,U,U)\). The conclusion is limited to the
   fixed-color classification.
5. **Local clarity fixes — applied.** “The graph in the question” was
   removed, \(s\) is reserved for the generic fixed-rank parameter, the
   cyclic-relabeling upper bound is motivated, the human/machine boundary is
   explicit, and the landing-page address is printed.
6. **References — selective.** Lalonde's published 2025 small-graphs paper
   was added because the body now discusses the algorithmic lineage of his
   Lemma 4.4. Yu--Oh and Tian--Xu were not added because the revised note
   makes no claim requiring those additional contextual detours.
7. **Scope discipline — retained.** No commuting-operator extension was
   pursued, no GitHub Action was added, and no outreach or external
   communication was prepared or initiated.
