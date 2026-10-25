# Adversarial review — Zenodo23181280

**Complete: the full stated NP-completeness theorem and its strong, positive-cost and inward-convention consequences survive this independent review. No substantive mathematical defect or source-applicability gap was found.** This assessment does not certify first discovery, continued open status in2026 or conventional peer review. Root retains publication authority.

The controlling paper is *NP-completeness of aggregate root-dependent spanning-tree cost*,6October2026,v1.0. I read the entire actual four-page public PDF,57,772bytes,SHA256 `f51acb267822dd082fdb28a14bc581b37fc3b3a75008647a3e04fa8a3d84fbf4`, and all260lines of its12,790-byte controlling TeX,SHA256 `a0e7e6158267fbf9ca4cafbd5ccb4cfa4ac79a1e0aea61282c9ee09d7e8d11d5`. All four actual rendered pages were also viewed. The original59-binding source manifest was rehashed at completion; no original source, earlier review or shared state was changed.

## Literal scope and independence

The input is a connected finite simple undirected graph with N≥1 vertices, a freely specified nonnegative integral directed arc-cost vector for **each vertex root**, and an integer threshold. All2N|E| costs are explicitly binary encoded. A single common undirected spanning tree is oriented away from each root; every one of itsN−1 oriented edges is charged at each root. The decision asks whether their aggregate is at mostK. The theorem proves NP-completeness even for costs{0,1,2}, hence strong NP-completeness, and NP-hardness of minimization. Uniformly adding1 gives the same result for{1,2,3}; transposing every cost pair gives the inward convention.

Before any primary body or historical/current review opinion, the full paper and TeX were read and ten attack families were recorded. The early ledger was sealed2026-10-25T07:09:30.570127Z: ledger SHA256 `e8363908e1b43bc3d2b4024ff33d4d729630740bf89532033e08b207e2076227`; INITIAL_SEAL SHA256 `86092866592b18afa4d24f4296e7e217be693d11bd03bc34cfe76d29c8bdd5d2`. Raw primary paths/hashes were requested only after this seal. No sibling/root mathematical derivation or historical evaluative report was read. Later code inspection included its binding/provenance metadata; the historical proof file was copied and hashed solely for an isolated reproducibility replay, not scientifically read or executed.

## All-size proof assessment

The universal reconstruction is in ATTACK_DERIVATIONS.md. Its decisive step is unrestricted objective accounting, not a census of a chosen tree family. For any spanning tree, letp count hub–variable edges,q count clause–variable edges, andh indicate the hub edge. Every clause has positive degree, so q≥m. Tree cardinality gives p+q+h=n+m+1. The symmetric t-root vector then gives exactly

    F_t=p+2q=K+(1−h)+(q−m),  K=n+2m.

All other root contributions are nonnegative. Hence a tree at threshold must haveh=1,q=m. Every clause is therefore a leaf. Removing those leaves gives a connected tree on the two hubs and variables; each variable has exactly one hub attachment, since zero attachments disconnect it and two create a triangle. This excludes unintended trees globally.

In such a structured tree, rooting at a clause leaf directs its selected variable toward that variable's chosen hub. Every other variable's hub edge points from hub to variable. Thus the clause-root vector charges only its selected variable-to-hub arc. Its cost is0 exactly when that selected literal is true and1 otherwise. Consequently F=K+the number of false **selected** literals. A satisfying assignment and one true selection per clause produce a tree of valueK; conversely, any tree at threshold supplies a satisfying assignment. Both directions hold for every normalized formula, including repeated clauses and disconnected incidence patterns.

The reduction writes the whole input table, including zeros. After deleting unused declarations and densely relabelling occurring variables, n is bounded by literal occurrences rather than the magnitude of old binary labels. N=n+m+2,|E|≤1+2n+3m,all cost entries are constant-sized andK≤2N. Normalization handles repeated literals, tautological clauses, empty clauses and the empty conjunction without changing satisfiability. These checks remove a potential exponential-label loophole. NP verification has polynomial traversal cost and bit lengths; its aggregate sum has at most the maximum cost bit length plusO(logN) extra bits. Numerical bounds stay polynomial under unary encoding. The positive shift adds exactlyN(N−1) to every tree, including the fixed yes/no instances; the inward transpose preserves root indices and all costs.

## Attack outcomes and meaningful negative controls

| Attack | Outcome |
|---|---|
| Hidden root-edge-only or independent-tree objective | Actual source and current definition agree on entire rooted orientations of one common tree. |
| Cheaper unstructured spanning tree at threshold | The unrestricted identity excludes every such tree; no exchange heuristic is required. |
| Clause-root costs accidentally charging other false literals | Only the selected variable's hub edge points in a potentially charged direction. Full-table checks agree for every structured tree tested. |
| Wrong reverse implication or arbitrary literal choice | Threshold enforces every selected literal true; satisfiability permits choosing one such literal per clause. |
| Large labels, unused variables or implicit cost encoding | Dense relabelling and explicit2N|E| table are polynomial in the actual input length. |
| Strong NP-completeness or positive shift overstated | Cost alphabet is constant and thresholds are polynomially bounded; every tree has exactlyN(N−1) charged arcs. |
| Martin lift claimed to make every lifted objective easy | Primary formulations establish the x-projection. For integralx, the tree and every root orientation are unique; projection integrality alone says nothing about all lifted objectives. |
| Input boundary failures | Contradictory units, repeated clauses, sparse labels, tautologies, empty clauses/conjunction and N=1 are consistent with the proof and controls. |

I constructed two exact negative controls. With four sign clauses onx2,x3 plus(x1∨x2), lowering the clause-edge base penalty toB=1 admits a tree at threshold despite unsatisfiability. The submittedB=2 excludes it. Repeating each of the four sign clauses three times gives minimum unsatisfied count3, yet an explicit unstructured tree has F=K+2=31 withK=29. Thus the unrestricted optimum cannot always equalK+minimum-unsatisfied-clauses. The current paper explicitly disclaims that stronger identity and correctly restricts its literal formula to structured trees. These witnesses support the necessity of its stated boundaries; they are not defects in the paper.

## Primary scope, imported hardness and attribution

[Kaibel's actual Oberwolfach report](https://ems.press/content/serial-article-files/46772?nt=1),pp3014–3015, was read completely for his contribution. Problem1 has exactly the aggregate whole-arborescence objective and independent real cost vectors. Hardness on the present nonnegative integer subclass answers it under finite encoding. Its neighboring Problem2 has a different directed-path objective and is not claimed here. The cover dates the workshop4–10November2018; the [official EMS record](https://ems.press/journals/owr/articles/16633) confirms publication17December2019.

[CCZ's actual author manuscript](https://www.andrew.cmu.edu/user/gc0v/webpub/ExtFor-Feb2010.pdf),§6.1,pp25–26, and [Friesen's dissertation](https://d-nb.info/1219966134/34),Proposition2,p8, match the common-edge/root-indegree formulation. I checked those bodies, including the direction-index conventions. For integral projectedx the tree orientation is uniquely determined, as can also be proved by leaf elimination. No new formulation theorem is needed for the reduction itself.

Karp's actual scanned1972 body was inspected visually, including its reducibility/NP definitions, Cook's SAT-hardness theorem onp92, and the explicit conversion to clauses with at most three literals onp98. This authenticates the sole hardness import at precisely the required input scope. I did not reprove Cook's theorem or read all19pages. The copy is hash-bound in ignored primary cache; the actual scanned body, rather than a search snippet, supports this import.

The paper expressly qualifies its dated negative historical audit. This review verifies the mathematics and exact source question, not the completeness of that6October2026 audit. No current/historical evaluative report was used as evidence, and no exhaustive later-literature search was performed. **Absolute priority and whether someone had already answered the question remain unknown.** No attribution defect was found in the primary passages read; that is a bounded finding, not a first-discovery certificate.

## Computation, reproducibility and limits

Own controls were written and first run before reading supplied program bodies. The final independent run covers520formulas and all72,790associated spanning trees across35distinct graphs. It exhausts normalized one- and two-variable clause multisets with up to four clauses, then adds width-three controls. Every tree was independently oriented from every root and checked by edge-cut sides. It checked unrestricted accounting,12,072structured-tree literal identities, both decision directions, transposition and positive shifting; explicit constructed witnesses checked the tempting false variants. Final elapsed time1.48seconds under a25-second process-group watchdog; exit0,empty stderr. These finite exact results supplement the universal argument, not establish NP-hardness.

I inspected the complete supplied389-line verifier, complete runner and proof-binding metadata before replaying only their fresh default mode in an own-folder quarantine. Normal and optimized executions agree; the runner reports2,727,845checks per valid run and rejects all12intentional controls. Historical programs were not executed. The replay took7.89seconds under the same25-second watchdog and finally cleaned its process group. The quarantine binds exact copied inputs and writes temporary files only inside this review namespace. Its PASS status supplies reproducibility evidence, not independent proof or priority.

The first successful own control run used a simple algebraic transpose check. I strengthened that to independently computed inward edge-cut accounting and reran; the earlier script and output remain in ignored cache. No failed scientific result was discarded. The only orchestration parse error occurred before any command executed and was corrected. No mathematical repair or narrowed promotion was required.

The strongest verified conclusion is the full original decision/optimization result, including its constant alphabets and ordinary finite encoding, together with exact applicability to Kaibel Problem1. No substantive defect or remaining proof gap was found beyond the accepted foundational SAT-hardness theorem. All complete read ranges, original custody and limitations are in READ_LEDGER.json, SOURCE_CUSTODY.json and PRIMARY_LIMITS.md; the final manifest/seal makes the handoff immutable. No source edit, outreach, deployment, UI, Sheet or Git operation occurred.
