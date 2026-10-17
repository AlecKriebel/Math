# Source audit: consecutive nonorientable embedding obstructions

Date: 12 October 2026. This is a bounded literature and convention audit, not a solution, novelty claim, or certification of the entire current literature.

## Result

The inspected primary literature explicitly treats simultaneous obstructions to two nonorientable surfaces as unresolved in a January 2024 journal article. No later resolution was verified in this focused search. The two relevant 2020 preprints were published in 2024; their absence of journal references on arXiv does not mean they remain unpublished.

The proposed orientably-simple/Euler-hopper existence reduction is consistent with the inspected genus facts, subject to the convention and minor-minimality precautions below. The reduction is an independently checked deduction here, not a theorem located verbatim in these sources.

## Precisely identified sources and coverage

1. Bojan Mohar and Petr Škoda, *Excluded minors for the Klein bottle I. Low connectivity case*, Journal of Combinatorial Theory, Series B 164 (January 2024), 299–320. DOI: https://doi.org/10.1016/j.jctb.2023.10.002 . Publisher preview: https://www.sciencedirect.com/science/article/abs/pii/S0095895623000849 . Full inspected preprint: https://arxiv.org/abs/2002.00258v1 (1 February 2020).

   The 2024 publisher introduction retains the simultaneous-obstruction open question and reports no constructed high-genus hoppers. Preprint coverage: pp.1–3 definitions/status; p.7 Lemma 4.1; p.8 hopper definitions; pp.10–11 Lemma 5.5; pp.15–16 Theorem 6.2, Lemma 6.4, Corollary 6.5. Theorem 2.2 (p.3) gives Euler-genus block additivity. Theorem 6.2 (p.15) gives the 1-sum formula n(G)=E(G1)+E(G2)+σ(G1)σ(G2), σ=n−E. Lemma 5.5 concerns specified terminal-labelled low-genus classes. Corollary 6.5 concerns connectivity exactly two. Neither result settles unrestricted higher-genus existence. Relevant equations on pp.3 and15 were visually checked; the full computer enumeration was not independently reproduced.

2. Bojan Mohar and Petr Škoda, *Excluded minors for the Klein bottle II. Cascades*, Journal of Combinatorial Theory, Series B 166 (May 2024), 80–108. DOI: https://doi.org/10.1016/j.jctb.2023.12.006 . Publisher preview: https://www.sciencedirect.com/science/article/abs/pii/S0095895624000017 . Full inspected preprint: https://arxiv.org/abs/2002.00261v1 (1 February 2020).

   Scope and definitions inspected, together with preprint Theorem 8.9 and proof summary, pp.20–21: 21 cascades in the specified Euler-genus-two class. The proof summary explicitly identifies computer verification steps. This does not construct unrestricted ordinary Euler hoppers or orientably simple Euler-critical graphs. Its complete proof and computations were not independently audited. Both journal identities were also checked against publisher-deposited Crossref records.

3. Torrence D. Parsons, Giustina Pica, Tomaž Pisanski, and Aldo G. S. Ventre, *Orientably simple graphs*, Mathematica Slovaca 37(4) (1987), 391–394. Primary digital archive: https://dml.cz/handle/10338.dmlcz/129376 . Full article inspected; printed p.391 visually checked.

   Printed p.391 defines nonorientable genus using at least one crosscap, so every planar graph has value one. Printed p.392 Theorem 2 distinguishes cellular/noncellular minimum embeddings, including the tree exception. Printed p.393 discusses orientably simple families and a characterization question. It supplies a primary precedent for the normalized surface-embeddability invariant used below, but no Euler-critical existence theorem.

4. Russell J. Campbell, *Finding obstructions within irreducible triangulations*, PhD dissertation, University of Victoria, 2017. Institutional record: https://dspace.library.uvic.ca/items/cca9ac7d-a34e-4991-99ba-0b0d458e2e62 . Inspected definitions in §5.1 and Lemma 5.3, printed pp.47–48, plus Theorem 5.5, printed pp.48–50; not a whole-thesis audit.

   Lemma 5.3 covers an obstruction of any surface containing a triangle and gives an embedding in a nonorientable surface with Euler genus one higher. No connectedness hypothesis is stated. The local proof uses edge-deletion embeddability. Theorem 5.5 addresses minor obstructions outside the double-wye-delta-minimal class. Consequently, an exact target witness must be triangle-free and in that stronger minimal class. The thesis's scaffolding conjecture has additional restrictions and is not a proof of the target's nonexistence.

5. Saul Stahl and Lowell W. Beineke, *Blocks and the nonorientable genus of graphs*, Journal of Graph Theory 1(1) (1977), 75–78. DOI: https://doi.org/10.1002/jgt.3190010114 . Publisher metadata/abstract checked. The original full PDF was unavailable through the attempted publisher retrieval; it has not been audited. The precise formula above is supported by its explicit restatement in Mohar–Škoda, not a claimed reading of the 1977 proof.

## Convention and transfer precautions

Write E(G) for Euler genus and ν(G)=min{h≥1: G embeds in N_h}. Thus ν=1 on every planar graph, including forests. Set σ=ν−E. Then σ is 0 or1, and σ=1 implies E is even.

The 2020 Part I paper instead assigns nonorientable genus zero to trees. Its printed Theorem 6.2 cannot be applied literally with this convention to an arbitrary tree summand: adjoining a leaf to an orientably simple cyclic graph does not lower its genus, whereas setting the tree's σ to zero would incorrectly remove the correction term. Use the normalized ν convention, or remove genus-neutral tree attachments and restrict applications to cyclic summands. This is a boundary-convention issue, not a counterexample to the block theorem in its appropriate form.

Source hopper classes are defined on graphs with two distinguished nonadjacent terminals. Ordinary E-hopper assertions require every ordinary edge deletion and contraction. With nonadjacent terminals these elementary operations coincide; augmented-genus and weak hopper definitions do not coincide with ordinary E-hoppers. All-proper-minor formulations must also exclude isolated vertices or explicitly check vertex deletions.

## Independently checked deduction

Suppose G is a target witness for h≥1. By adding one handle to an embedding of G−e in N_h, G embeds in N_(h+2). Hence ν(G)=h+2. If σ(G)=0, E(G)=h+2 and every proper minor has Euler genus at most h, giving an ordinary E-hopper. If σ(G)=1, E(G)=h+1 and every proper minor has strictly smaller Euler genus, giving a positive orientably simple Euler-critical graph.

Conversely, let H be positive orientably simple Euler-critical, with E(H)=r. Then r is even and ν(H)=r+1. For a proper minor J, if E(J)=r−1 its odd Euler genus forces ν(J)=r−1; if E(J)≤r−2 then ν(J)≤r−1. Thus H is a target witness for h=r−1.

For a non-orientably-simple ordinary E-hopper H with E(H)=r, use two copies in a 1-sum, or in a disjoint union with the corresponding component version of the block formula. The unchanged copy forces the total orientability correction to zero. The whole graph has ν=2r and every one-step edge minor has ν≤2r−2. Provided ordinary vertex-minor cases and graph conventions are handled, this yields a target for h=2r−2. This is a conditional construction, not an actual witness: no suitable H has been exhibited here.

## Bounded forward check

An OpenAlex citation-index query found three records citing Part I and two citing Part II. After removing mutual citation, the additional records were:

- Thomas J. Savitsky and Steven A. Schluchter, *Some Excluded Minors for the Spindle Surface*, JCMCC119 (2024), 213–229, https://doi.org/10.61091/jcmcc119-22 . Primary PDF pp.213–214 inspected. The topic is a pinched-sphere pseudosurface and an incomplete computational obstruction list, not the simultaneous ordinary-surface target.
- Volodymyr Petrenjuk and Dmytro Petreniuk, *On the Synthesis of Planar Graphs with Given Properties*, Cybernetics and Computer Technologies 2025(2), 17–36, https://doi.org/10.34229/2707-451X.25.2.2 . Primary PDF introduction, main theorem locations, conclusion, references and English abstract inspected. It concerns planar cell-distance constructions and genus bounds; no resolution of the exact target was established from inspected material. Its full proofs were not audited.

Focused searches for ordinary/Euler hoppers, orientably simple critical graphs, simultaneous nonorientable obstructions, and follow-up to Campbell's result yielded no verified later resolution or stronger short-cycle exclusion. Search/index completeness is not guaranteed. Unrelated automated conjecture-status repositories were not accepted as primary status evidence.
