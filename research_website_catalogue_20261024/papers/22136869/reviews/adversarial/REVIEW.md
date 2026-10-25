# Adversarial review — Zenodo 22136869

**Conclusion: the main published collision, rank, local-family, edgewise continuous-time, and single-blob grafting claims are supported at their stated scope.** No substantive counterexample to those claims was established. A construction sentence on page 12 has an important scope ambiguity: its claimed forced ratio needs the equal-coordinate comparison-factor specialization used immediately beforehand. An unrestricted reading is false, but the contextual restricted reading is correct. This is recorded below without treating it as a failure of Theorems 12–19.

This review is AI-assisted mathematical verification, not human peer review, a proof-assistant certificate, or a worldwide priority certificate. No source repair or publication mutation was made.

## Exact publication and independence

Title: *Exact Tree–Theta-Trinet Collisions under the Kimura 2- and 3-Parameter Models*. Author: Alec Kriebel. DOI: [10.5281/zenodo.22136869](https://doi.org/10.5281/zenodo.22136869). The record metadata says **version 1.2.6**; the published manuscript filename and package description say **v1.2.7**. These are retained as distinct facts, not silently reconciled. The record date is 2026-08-28.

The fresh public files were checked against the acquisition receipt, their byte lengths, SHA-256 and Zenodo MD5. In particular:

| Asset | SHA-256 |
|---|---|
| `Kriebel_2026_Exact_Tree_Theta_Trinet_Collisions_v1.2.7.pdf` — 20 pages, 178692 bytes | `7f1ecd0e70504736146eb8f2d4ebfb43980fd1feef50cf39bbe7e751ad5afa8f` |
| `k2p-k3p-theta-collision-19cf11f65ed4.zip` — 443027 bytes | `7c603e15f6afb7546f618b88bbefdc52ee264b656399f6656fc742aeabb786c7` |

The third asset is the public `SHA256SUMS` sidecar, also bound in `source_identity.json`. The ZIP's `combined-paper-clarified.pdf` is byte-identical to the public main PDF. Both additional reader PDFs, `k2p_displayed_tree_clarification.pdf` and `technical-summary-clarified.pdf`, were read completely; each has two pages. The manuscript, mathematical source sections, certificate arithmetic and principal verification paths were inspected. Stored historical verification transcripts and the dedicated `ADVERSARIAL_REVIEW_DISPOSITION.md` were not read as evidence. The package manifests verified 46 and 45 paths respectively; these are internal integrity checks, not authentication of authorship.

The full main manuscript was read before the parent supplied a targeted candidate for the page-12 sentence. Its acknowledgments necessarily exposed statements about prior external examination/confirmation; these were not used as evidence. No sibling report or sibling code was read. The parent later communicated the competing contextual interpretation, which was tested independently. Thus the initial full-manuscript reconstruction was independent, while the page-12 falsification/adjudication was a disclosed targeted collaboration, not a blind discovery. The first fresh witness and rank checks preceded the submitted replay. Later structural controls were added after replay but do not import its source or results.

## Exact claims and hypotheses

The substitution model uses the Klein group, the stated (A,C,G,T) character order, a uniform root distribution, symmetric K2P/K3P edge matrices, and **independent displayed-tree parent choices** at the two reticulations. The network is the literal rooted graph

\[
\rho\to1,\ \rho\to u,\ u\to p,\ u\to q,\
p\to r_2,\ q\to r_2,\ p\to r_3,\ q\to r_3,\
r_2\to2,\ r_3\to3.
\]

The selected witnesses give both arcs out of (p) the vector (S), and both out of (q) the vector (T). They do **not** put (S) on both arcs entering one reticulation and (T) on both arcs entering the other. That distinction matters computationally.

Every actual witness edge has strictly positive transition entries and nontrivial eigenvalues strictly between zero and one; both inheritance probabilities are (1/2). The parameter domain is the source paper's restricted stochastic, nonidentity, positive-definite domain, strengthened to strict entrywise positivity for the explicit collisions. The continuous-time claims are **edgewise**: generators, rate ratios and times may differ between edges. No common generator, molecular clock, global node timing or alternative reticulation semantics is asserted.

The reviewed conclusions are:

1. The compact (\mathbb Q(\sqrt{71})) K2P tree–theta collision, its strict interior status, and its exact minimum pattern probability.
2. K3P non-disjointness by inclusion, the independent negative-invariant point, the fixed-order displayed-child obstruction, and the cubic strict-continuous-time K2P collision.
3. Rank nine for the K2P theta map, a six-dimensional tree model, the 17-dimensional local collision locus and 11-dimensional fixed-output fibers; the two-equation six-dimensional symmetric family.
4. The quartic K3P witness: a network parameter outside every global K2P character specialization whose **shared distribution is nevertheless globally relabelled K2P**.
5. Rank fifteen for the K3P theta map, a nine-dimensional tree model, a 23-dimensional collision locus, 14-dimensional fibers, the analytic strict-continuous-time extension, nearby observably genuine K3P collisions and Zariski density in the effective ambient spaces.
6. A single theta replacement at any selected internal vertex of any labelled unrooted binary tree, preserving every leaf-pattern probability, including the explicitly scoped continuous-time and observable-symmetry versions.

These are pointwise collisions and local families. They do not assert generic tree equivalence on the theta topology, arbitrary common-generator models, multi-blob composability, or genuine four-attachment-blob collisions.

## Reconstruction and adversarial checks

### Fourier conventions, literal graph and topology

For a uniform root, the Fourier coordinate is zero unless the leaf labels sum to the identity. Each retained tree contributes the product of edge eigenvalues indexed by its descendant-label sum. A retained dangling branch has no labelled descendants, so its factor is the identity eigenvalue one; ordinary-state pruning reaches the same conclusion by summing a stochastic row. Suppression of degree-two vertices multiplies the eigenvalues coordinatewise. The root-adjacent factors are (K_xK_{y+z}=K_x^2), not a single (K_x).

Independent graph reconstruction gives the four core terms

\[
S_yS_zU_{y+z},\quad S_yT_zU_yV_z,\quad
T_yS_zU_zV_y,\quad T_yT_zV_{y+z},
\]

each with weight (1/4). The root, leaf, tree-node and reticulation degrees match the source definition, and the graph is acyclic. Root suppression leaves the three internally disjoint (p)-to-(q) paths through (u,r_2,r_3). Their cyclic core has two reticulations and exactly three incident pendant edges. It is a strict level-two nontrivial 3-blob, not a disguised tree or a genuine four-attachment blob. A compatible rooting exists on the terminal-1 side. Since (p) and (q) each have two prescribed outgoing reticulation edges, neither can acquire a nonreticulation child in a compatible binary rooting; no tree-child rooting exists.

The ordinary-state calculations use the full (4\times4) transition matrices and sum internal states by pruning on each literal retained graph. They do not merely compare two copies of the Fourier formula. Fresh checks reproduce all 64 pattern equalities for each of the compact K2P, quartic K3P and cubic continuous-time K2P witnesses. A negative control that changes the (S/T) placement on the third-leaf incoming arcs destroys the compact equality.

### Compact and continuous-time K2P witnesses

The compact witness satisfies (M_{y,z}=P_{y+z}R_yR_z) in (\mathbb Q(\sqrt{71})). Restoring the common (K) factors gives the stated comparison-tree edge vectors. All 48 inconsistent Fourier coordinates vanish, the remaining 16 agree, and the inverse transform agrees with ordinary-state pruning in all 64 patterns. The exact claimed minimum (1188799/79626240) is attained, and every other probability is at least that value. Strict positivity and the eigenvalue bounds hold on every rooted edge, the effective suppressed edge and the comparison-tree edges.

The compact network is not claimed to be strictly continuous-time. For example, its (U) edge has (g=19/30< (4/5)^2). Its comparison-tree edges are in the strict continuous-time cone, which is enough for the later tree root-splitting statement.

The cubic witness uses the isolated real root (ell) of the printed cubic and (t=\sqrt{1423}). Fresh controls used an independently constructed exact number field with primitive element (ell+t), rather than the submitted six-coordinate implementation. Rational root counts bind the printed isolating interval to the middle real root; a later structural control explicitly checks the CRootOf index. Rational interval evaluation certifies every relevant strict sign. The full state probabilities, core equality, minimum-probability bounds and minimum K2P rate margin (11/900) agree with the claims. The published degree-six arithmetic has a valid field interpretation: the cubic is irreducible, and its degree-three field cannot contain a quadratic subfield.

For a K3P edge with positive eigenvalues, the rate–time products are

\[
\lambda_Ct=\tfrac14\log\frac{a_C}{a_Ga_T},
\]

with cyclic analogues. Hence the three strict inequalities in equation (4) are exactly positive symmetric K3P rates; in the K2P specialization the only additional inequality is (g>s^2). Multiplication of edge eigenvalues preserves these strict inequalities. Positive square roots halve the rate–time products, so the tree splitting argument is justified for the stated edges. None of this supplies a common rate matrix or globally compatible timing.

The exact fixed-order child computation is also reproduced. At least one child has the negative value in the parent order and the positive value after the designated swap, within the printed intervals. An initial reviewer control incorrectly demanded this of **both** children; the paper only says one. That overstrong test was corrected, and its initial run log is retained. It was not evidence of a manuscript defect. The supplied replay independently verifies the fully specified rational point with negative invariant in all six orders and its stated minimum probability.

### Ranks and local families

The K2P global (C\leftrightarrow T) symmetry partitions the 16 consistent Fourier coordinates into ten orbits; normalization leaves dimension nine. The K3P effective normalized space has dimension fifteen. The tree pair-coordinates ((\alpha_g\beta_g,\alpha_g\gamma_g,\beta_g\gamma_g)) have derivative determinant (-2\alpha_g\beta_g\gamma_g\ne0), and the positive square-root recovery formulas give a smooth inverse. Thus the positive K2P and K3P tree images are embedded germs of dimensions six and nine, respectively.

Fresh Jacobian controls differentiate the literal retained-graph monomials by the product rule. They use the exact row/column orders printed in the manuscript. This independently reproduces

\[
\det J_{\mathrm{K2P}}=
-\frac{7^2\,11^2\,19\,107\,151^2\,15013}{2^{60}3^{25}5^{10}},
\qquad
\det J_{\mathrm{K3P}}=
\frac{h(10h^2+1)}{2^{61}3^4 5^{14}}.
\]

The K2P minor at the cubic continuous-time point lies in the printed negative interval. Varying the first rooted factor while fixing the other root-adjacent factor is an invertible diagonal change to the effective pendant coordinates, so these minors genuinely give ranks nine and fifteen for the 20- and 29-dimensional semi-directed parameter maps. They are not merely rank claims for the smaller symmetric ansatz.

The transverse-preimage argument is applicable: a full-rank smooth map is transverse to the embedded tree germ, and its restriction to the preimage remains a submersion onto that germ. Therefore the dimensions are (20-9+6=17) and (29-15+9=23), with fixed-output fibers (20-9=11) and (29-15=14). The local product statement is local, as the paper says. It is not a claim of global parametrization or complete classification of the intersections.

For the symmetric K2P family, the two equations in (15) are sufficient in the positive chamber because every factor and recovered square root is positive; squaring introduces no additional sign branch there. Fresh symbolic differentiation gives the stated positive two-variable Jacobian (675554683609333/194995116803358720000000). The implicit-function theorem consequently gives the local six-dimensional semialgebraic family, and openness preserves the actual stochastic tree and network edges near the known interior witness.

### Quartic K3P and analytic extension

At (h=5^{-1/4}>0), the published quartic factorization and all actual transition inequalities are verified exactly. The (U) edge has three distinct nonidentity eigenvalues, ruling out each global equal-pair parameter specialization. But the comparison tree has (\alpha=(1,a,a,t)) and (\beta=\gamma=(1,t,t,t)), so its distribution is fixed by (C\leftrightarrow G). Since (a\ne t), it is not JC. This is a parameter/output distinction, not a contradiction or a claim that the explicit quartic output is already observably genuine K3P.

The full rank supplies the stronger observable conclusion. On a positive three-leaf tree the pair-coordinate recovery uniquely determines every edge's three eigenvalues. If the output is fixed by a global character transposition, the recovered edge vectors have the corresponding equality. Thus the fixed locus is precisely the respective six-dimensional K2P tree specialization. The union of three such relatively closed lower-dimensional sets has empty interior in the nine-dimensional tree germ. A local section of the theta submersion covers a tree neighborhood, and removing those three loci leaves a relatively open dense set of genuinely K3P outputs. This is relative to that covered tree neighborhood, not a generic statement in the full theta parameter domain.

For the strict continuous-time extension, only the two stated (U,V) rate margins vanish at the quartic point. The two free directions are distinct from the fifteen pivot coordinates. Fresh exact checks reproduce every row of

\[
J_*p'(0)+F_{U_C}+F_{V_G}=0
\]

and the positive margin derivatives ((21-20h^2)/19) and (1). Invertibility of the pivot Jacobian gives an actual real-analytic fixed-output branch; the tangent alone would not suffice without that hypothesis. Positive right derivatives move the two zero margins into the strict cone, and all already strict inequalities persist by continuity. The rank and distinct-eigenvalue conditions also persist. Repeating the local-section argument at one small positive branch point gives the claimed strict-continuous-time neighborhood of observably genuine outputs. The theorem is an existence result near zero; it does not supply a certified large numerical continuation radius.

The full-rank physical images contain ordinary real open sets. A polynomial vanishing on such an open set is identically zero in the effective affine coordinates, giving the claimed Zariski closures. Normalization, inconsistent-coordinate zeros and the K2P symmetry relations have already been removed from those spaces. The conclusion does not fill the physical probability simplex or erase inequalities. Since the tree varieties are proper, their preimages under a dominant theta map are proper algebraic subsets; generic theta parameters are not tree-equivalent, consistently with the claimed local collision families.

### Single-vertex replacement on arbitrary binary trees

The common-subtree lemma is an exact linear operation on the three interface-state distribution. Conditional kernels on the three disjoint components multiply and sum against that interface distribution. Equality of the interface laws therefore preserves every full-leaf pattern probability, with no independence assertion beyond the tree components being conditionally independent given their attachment states.

Deleting any internal degree-three vertex separates a binary tree into three nonempty leaf-bearing components. Installing the same comparison-star or theta interface edges at their adjacent vertices, and the same remaining matrices in the components, applies the lemma directly. The inserted theta core has only the three attachment edges; every other tree edge remains a bridge. Hence it is the sole nontrivial blob, contains exactly two reticulations, and contracts back to the selected tree topology. The terminal-1-side root yields the required directed binary network. Because that side and the other two sides all contain leaves, no downstream vertex dominates all root-to-leaf paths; the source's root convention is respected. The argument does not require a compatible rooting through a reticulation-side terminal.

For the observably genuine version, the components are given JC edges with strictly positive eigenvalues. Marginalizing any component output to a selected leaf gives an invertible product transition matrix. Thus its conditional kernel has column rank four; the tensor product of the three kernels is injective. JC kernels intertwine the relevant state-group automorphisms. If a global character symmetry appeared after grafting, injectivity and equivariance would force it at the original interface, a contradiction. This proof is stronger than merely observing that equality survives grafting: it explains why absence of K2P symmetry survives as well.

Fresh structural checks construct an explicit subtree left inverse, verify equivariance and tensor-product injectivity, and show rank loss at a zero-eigenvalue negative control. They also test 63 internal-vertex replacements across several binary tree families with 3–8 leaves, checking binary degrees, the sole cyclic blob, strict level two and exact tree-of-blobs recovery. These finite checks are supporting controls; the preceding conditional-kernel argument is the proof for all labelled binary trees and all (n\ge3). The submitted four-leaf replay checks all 256 coordinates and patterns by graph Fourier calculation, ordinary-state pruning and common-kernel extension. It is correctly described as a regression rather than a proof for every (n).

No independent multi-blob replacement theorem follows from this reasoning, and none is claimed. Likewise, substitution-supermodel inheritance is conditional on containing the complete rooted parameter tuples and the same independent displayed-tree mixture; the manuscript explicitly excludes a general common-(Q) GTR conclusion.

## The page-12 construction sentence: exact adjudication

The paragraph immediately after Theorem 12 displays

\[
U=(1,b\tau,b,\tau),\quad V=(1,b,b\tau,\tau),\quad
S=(1,\kappa d,d,e),\quad T=(1,d,\kappa d,e)
\]

and says that, on (\tau=1/3), the factorization equations force (\kappa=3/\sqrt5), (b^2=1/\sqrt5), and (e/d=6/5).

**Unrestricted reading:** if “factorization” means any positive (M_{y,z}=P_{y+z}B_yB_z) for the displayed network ansatz, the ratio claim is false. Set

\[
b=h,\quad\kappa=3h^2,\quad d=e=1/4,\quad\tau=1/3,
\]

keep the printed (P), and use

\[
B=(1,h^2/2,h^2/2,5h^2/12).
\]

All sixteen factorization identities hold. The actual network and resulting comparison-tree edges are strictly stochastic with eigenvalues in ((0,1)); all 64 Fourier and ordinary-state probabilities agree exactly. Rational interval checks give a common lower bound (1/20) for their transition entries and (2216149/147456000>0) for their pattern probabilities. Yet (e/d=1\ne6/5). The checked symbolic family is even broader: with (d=1/4), (b=h), (\kappa=3h^2), the factorization holds with (B_T=5eh^2/3), leaving (e) free wherever the strict inequalities persist.

**Contextual reading:** the preceding displayed equation (17) specifically uses equal nonidentity entries of (B), and the paragraph describes deriving that particular quartic point. The counterexample violates this equal-(B) specialization. The supplied construction certificate also uses a single scalar (r) and a scale equation corresponding to it. Under this additional comparison-factor restriction, the claimed necessity is correct. Independently put (\sigma=\sqrt{2(1+\tau^2)}); the shape equations include

\[
\kappa(1+\tau^2)+2\tau=\sigma(\kappa\tau+1),
\]

and

\[
2\kappa\tau+b^2(\kappa^2\tau^2+1)
=\frac{2\tau}{\sigma}(\kappa^2+1+2\kappa b^2\tau).
\]

At (\tau=1/3) these force the printed positive (\kappa,b). The common-square condition then gives

\[
(e/d)^2=\frac{\kappa^2+1+2\kappa b^2\tau}{2(1+\tau^2)}=36/25,
\]

so positivity gives (e/d=6/5). Fresh symbolic controls verify all three deductions.

**Disposition:** this is a genuine ambiguity in the isolated wording, with a real counterexample to the broader reading, but not a demonstrated substantive defect in the contextual construction or the main theorems. The published (e=3/10,d=1/4) witness is a member of the verified free-(e) family and remains valid. The rank, tangent, local-family and all-leaf arguments use that explicit valid witness rather than the unqualified necessity assertion. The exact boundary evidence is retained in `counterexample_controls.py`, `counterexample_results.json`, and `structural_controls.py`. No manuscript change was made.

## Primary interfaces and limited historical claims

Fresh primary URLs and hashes are in `reference_receipts.json`.

| Primary source | Interface checked |
|---|---|
| [Brits et al., arXiv:2607.12919v2](https://arxiv.org/pdf/2607.12919v2) | The actual formal Lemma 5.6 asserts K2P trinet disjointness under its restricted parameter set and positive value of the same invariant; Corollary 5.8 includes K2P arbitrary-level disjointness. The explicit compact witness fits those stated hypotheses and contradicts the K2P conclusions. The appendix's relabelling step supports the fixed-order diagnosis. |
| [Brits et al., arXiv:2607.12919v3](https://arxiv.org/pdf/2607.12919v3) | Definitions of rooted/semi-directed networks, blobs, displayed-tree mixture and the restricted parameter domain match the construction. The Fourier descendant-label rule and K2P (C=T) convention agree. The K2P high-level lemma/global extension are removed; the text explains the leaf-order obstruction and leaves the Kimura extension open. The JC and level-one assertions are separate and are not refuted here. |
| [Ardiyansyah, arXiv:2104.12479](https://arxiv.org/pdf/2104.12479) | Lemma 5.1 explicitly excludes simple nice strict level-two networks with two or three leaves. Thus that cited class does not include this non-nice theta trinet. The current pointwise intersection does not refute a restricted variety-noncontainment statement on another class. |

The group-based Fourier mechanism was independently reconstructed and checked against state pruning rather than relying only on a historical transform citation. The local differential and algebraic arguments are standard finite-dimensional consequences with their required full-rank/embeddedness hypotheses checked explicitly. No proof of a generic identifiability theorem is imported to establish the collision itself.

A secondary editorial scope issue concerns §12, item 5: whether JC excludes theta/tree collisions under the same restricted model is already answered affirmatively by the cited v3 Lemma 5.5, which the present manuscript itself invokes in its introduction. That item should not be promoted as a new unresolved question without specifying a changed model or hypothesis. This does not undermine the Kimura collision proofs. This review is not an exhaustive priority search and does not audit all prior literature claims or correspondence.

## Computation, reproducibility and limits

The first independent full-witness script passed **2,732 exact assertions in 67 families**, including the 688 page-12 boundary controls. The independent structural script passed **1,273 assertions in 21 families**. The combined count is **4,005**, without double-counting the imported 688 checks. Counts include entries of matrices and finite graph instances; they are coverage records, not quantitative proof confidence.

The fresh implementations use SymPy 1.14.0 only for exact number fields, rational polynomial operations and exact finite matrix algebra. Equality tests do not use floating tolerances. Sign claims use rational root isolation and interval enclosures. In particular the cubic witness uses a different field representation from the submitted code, and its embedding is bound explicitly.

After those witness controls, the unchanged submitted package was copied byte-for-byte into an ignored private replay directory. All ten stages of `python3 verify.py` passed, ending with `ALL EXACT CHECKS PASSED`, with exit status zero and empty stderr. These include convention checks, strict JSON/schema rejection, compact K2P, graph-derived pruning, cubic continuous-time K2P, the four-leaf graft, K2P ranks/family, semantic mutations, quartic K3P/rank/tangent checks, and K3P semantic mutations. `replay_receipt.json`, the complete fresh stdout/stderr, and `replay_inputs.json` preserve the execution evidence. Stored historical transcripts were not accepted as replay evidence.

The schema hashes check structure, not mathematical truth. Exact mathematical fields are independently recomputed; sidecars that mirror embedded certificate sections are transport consistency checks rather than additional independent certificates. The source's field-coverage inventory states these distinctions accurately. The suite's ansatz residual verification validates the chosen constrained point; it does not independently prove an unrestricted uniqueness classification. The analytic implicit-function existence, local-section, dominance and arbitrary-(n) conclusions require the written reasoning above and are not consequences of a finite transcript alone.

## Strongest supported conclusion and exact limitations

The fixed strict level-two theta trinet and a tree share exact strict-interior K2P distributions, including an edgewise strict-continuous-time example. Model inclusion supplies K3P collisions. The quartic example additionally breaks K2P at the network-parameter level; full ranks and the checked implicit-function direction produce local families with observably genuine K3P outputs in both positive stochastic and edgewise strict-continuous-time chambers. The local collision dimensions and fixed-output fiber counts are supported. A single theta insertion at any internal vertex of any labelled unrooted binary tree preserves the full distribution, with the specified topology, rooting, continuous-time and observable-symmetry scope.

**Exact remaining mathematical gap for those main stated claims:** none identified in this review. The page-12 necessity sentence requires its contextual equal-(B) restriction and should not be read as a classification of the unrestricted positive ansatz. The JC future-question wording is not an unresolved problem in the cited restricted model. Neither caveat is evidence that the explicit witnesses or Theorems 12–19 are false.

The review establishes no common-generator/clock result, generic theta tree-equivalence, arbitrary multiple-theta composability, genuine four-attachment-blob collision, edge-dependent character-relabelling classification, complete global intersection classification, numerical inference guarantee or worldwide priority certification. Sources, website, spreadsheet, Git and Zenodo were not modified; no external communication was initiated. Only this review directory was written, with private runtime, downloads and replay caches ignored.
