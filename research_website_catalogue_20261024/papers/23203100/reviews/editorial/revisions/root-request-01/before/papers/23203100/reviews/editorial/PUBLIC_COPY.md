Alec Kriebel
[Research](/research/) | [Blog](/blog/) | [ORCID](https://orcid.org/0009-0001-9320-500X)

# Pure-loss bosonic dynamic capacities: EPnI consequences and consumed-key secrecy accounting

By Alec Kriebel, independent researcher.  
Manuscript dated 6 October 2026 · No version number supplied · **Unrefereed preprint**

[Read the paper (PDF, 7 pages)](paper.pdf) · [Download PDF](paper.pdf) · [Published source and supporting materials (ZIP)](zenodo-upload-kit.zip) · [Zenodo record](https://doi.org/10.5281/zenodo.23203100)

[Plain-English explanation](#plain-language) · [Read on this page](#paper) · [Collaboration](#collaborate)

## Abstract

The finite-energy multimode entropy photon-number inequality proved in the OpenAI mathematics release supplies the sharp entropy premise in the previously conditional pure-loss bosonic dynamic-capacity converses. We give its precise classical, quantum and entanglement consequence under an average photon constraint, including arbitrary entanglement across uses. For public, private and secret-key resources, an operational correction is necessary: the printed catalytic secrecy condition of Wilde–Hsieh protects consumed key jointly with generated secrets and excludes the one-time pad. A zero-energy converse disproves the displayed region under that literal condition. We establish the formula with an explicit generated-secret secrecy criterion, corrected converse accounting, and direct key-assisted coding. The formulas and original conditional reductions are inherited; this is a consequence and operational audit, not an independent proof of EPnI. We rely on the cited unrefereed EPnI proof. Its analytical arguments and formal-source semantics were audited, but its Lean build was not reproduced.

## The idea in plain English

A lossy optical channel can carry ordinary messages, quantum information and shared resources in different combinations. A capacity region describes every combination of rates that can be approached with errors tending to zero. This note identifies the trade-offs for a pure-loss channel under a finite average photon budget, using the cited entropy photon-number inequality (EPnI).

The private-communication part asks what a protocol should protect after it uses up a secret key. A one-time pad keeps a message secret from someone who sees the ciphertext, but the message and the used key are correlated with that ciphertext. Requiring them both to remain jointly secret rules out the one-time pad. The paper proves that this literal requirement also obstructs the claimed private capacity region at zero channel energy.

The positive private theorem therefore states its changed promise explicitly: the generated message and new key are secret, while the used key is discarded. With that convention, the paper establishes the public/private/secret-key trade-off formula. The formulas and their original EPnI-conditional route are credited to earlier work; the note supplies a consequence of the external entropy proof and an operational correction.

## The precise result

Let Lη be the one-mode pure-loss bosonic channel with a fresh independent vacuum environment at each use, 1/2 ≤ η ≤ 1, and 0 ≤ N < ∞ average input photons per use. Arbitrary entanglement among the finitely many channel inputs is allowed. All logarithms are base two. Write g(u) = (u+1) log₂(u+1) − u log₂u, with g(0)=0. Rates are signed forward net rates: positive rates generate resources and negative rates consume them.

For classical communication C, quantum communication Q and entanglement E, the capacity region is the closed union over λ ∈ [0,1] of all triples satisfying the three inequalities simultaneously: C+2Q ≤ g(λN)+g(ηN)−g((1−η)λN); Q+E ≤ g(ηλN)−g((1−η)λN); C+Q+E ≤ g(ηN)−g((1−η)λN). The general equality uses the cited unrefereed finite-energy multimode EPnI proof, together with the named coding results.

For public communication R, private communication P and secret key S, under the explicit generated-secret convention, the capacity region is the closed union over λ ∈ [0,1] of all triples satisfying simultaneously: R+P ≤ g(ηN); P+S ≤ g(ηλN)−g((1−η)λN); R+P+S ≤ g(ηN)−g((1−η)λN). This is the corrected model’s region, rather than the region for the unchanged literal secrecy target in the cited source.

More precisely, the corrected convention requires ‖ω(W,X,Eⁿ)−π(W)⊗ω(X,Eⁿ)‖₁→0, where W=(M,T_A) denotes the jointly uniform generated message and key, X=(K,L) the public data, and Eⁿ Eve’s environment. Consumed private communication and key V=(J,S_B) are traced out and may correlate with W and X. Eve does not additionally receive the consumed key. Generated communication messages are fresh, uniform and initially independent of the preshared key; public common randomness is not counted as communication.

Separately, the literal source target protects U=(M,T_A,J,S_B) jointly and uniformly against Z=(K,L,Eⁿ). At N=0, its secrecy and reliability errors obey 1 ≤ 1/(d_M d_T_A)+(ε_sec+ε_rel)/2, where d_M and d_T_A are the generated message and key register sizes and the errors use the unhalved trace norm. Vanishing errors force d_M d_T_A=1 eventually. The one-time-pad rate vector (−1,1,−1) belongs to the displayed zero-energy private cone but violates this literal promise. For a uniform d-symbol one-time pad, the minimum unhalved trace norm against an independent uniform message/key pair is 2(1−1/d), even after optimizing the comparison public marginal. This obstruction does not depend on EPnI.

## Why the result holds

The external finite-energy multimode EPnI gives H(L_t^{⊗n}(ρ))/n ≥ g(t g⁻¹(H(ρ)/n)) for every fixed finite n, every finite-energy n-mode input ρ and t ∈ [0,1], with an independent vacuum port. It permits arbitrary internal entanglement. The nondecreasing function f_t(s)=g(t g⁻¹(s)) is convex for 0≤t≤1 and concave for t≥1. This is a use of the cited theorem, not an independent proof of EPnI.

For an arbitrary input ensemble, thermal entropy maximization bounds the average receiver entropy. Choose one common λ by the ensemble’s conditional receiver entropy. Applying the vacuum entropy bound to the channel and its degrading map, followed by Jensen’s inequality, bounds both conditional environment entropy and conditional input entropy using that same λ. Substitution into the regularized dynamic capacity bounds gives the displayed outer regions. The private converse explicitly charges the consumed public, private and key registers; degradability justifies pure spectral refinement.

The known displaced thermal ensemble and classically enhanced father protocol attain the quantum-resource region. For generated-secret private coding, an outer public code is combined with key-indexed private codebooks: Bob decodes using the key, while averaging the unknown key hides the message from Eve. Coherent Gaussian inputs give the stated corner, and the charged noiseless resource conversions give its polyhedron.

Finite ensembles and photon cutoffs are fixed before taking coding limits. A strict mean-energy margin N′<N lets the expected-cost bound and vanishing error bounds select a code that meets the exact average budget. Approximation limits and N′↑N then give the region by closure. Compactness of λ establishes closedness; the entropy parameter gives convexity. The zero-energy refutation instead follows directly from the vacuum input and a decoder-success probability bound.

## Scope and limitations

The exact-region theorems concern the one-mode pure-loss channel with independent vacuum environments, 1/2 ≤ η ≤ 1 and finite N. They do not cover infinite energy, η<1/2, thermal-channel quantum capacity, amplifiers or confidential broadcast.

The photon budget is Tr(G_n ρ̄_n)≤nN, averaged over classical messages, shared key and encoder randomness; G_n is the sum of input photon-number operators. Quantum communication uses the maximally mixed logical source, equivalently half of a maximally entangled reference pair. No peak, per-codeword or arbitrary-source energy constraint, or strong converse, is asserted. Noiseless side resources are charged by rate rather than optical energy.

The resource model has forward communication without free feedback, finite gross generation and consumption rates, and finite resource registers with logarithmic dimensions O(n). Required finite seeds are charged. No free two-way assistance, superlinear catalysts or elimination of all gross seed input is established.

The positive private theorem protects uniform generated messages and keys after consumed registers are discarded. It gives no semantic-security guarantee for arbitrary message distributions and no secrecy guarantee after revealing consumed key. Vanishing trace secrecy gives the normalized information estimates used here; it does not promise dimension-free absolute leakage tending to zero.

At N=0 and at η=1 both complete regions follow without a nontrivial EPnI input. At η=1/2 the complete corrected-private region also does; the full classical/quantum/entanglement equality generally retains its EPnI dependence. At λ=0 and λ=1 the conditional thermal terms are interpreted at their zero and full values.

The general capacity equalities rely on the soundness and stated finite-energy multimode scope of the cited external unrefereed EPnI proof. The note does not supply a new EPnI proof, classify all entropy equality cases or prove uniqueness of Gaussian optimizers. Its finite computational checks supplement analytic arguments.

The upstream formal-source theorem interface was inspected as documentary evidence. Its Lean build and axiom closure were not reproduced, and the comparator’s intentional sorry is not proof evidence. No proof-assistant certification is claimed for the upstream theorem or these capacity consequences.

Wilde, Hayden and Guha already gave the formulas, Gaussian ensembles and original conditional converse route. The entropy result belongs to the cited OpenAI proof, with De Palma’s entropy-bound formulation and the earlier coding literature explicitly credited. No firstness, exhaustive novelty clearance, new ordinary single-resource capacity or general broadcast theorem is claimed.

## Status and AI use

AI tools were used extensively in research, derivation, drafting, literature comparison and verification, including independent adversarial AI reviews. These reviews are not independent human or journal peer review. This is an unrefereed preprint; its external EPnI dependency is also unrefereed. No reproduced Lean build or proof-assistant certification is claimed. The named author is responsible for the claims and citations.

The manuscript is dated 6 October 2026, matching Zenodo’s declared publication date. Zenodo records creation on 7 October 2026 UTC. Neither the manuscript nor Zenodo metadata supplies a version number. These dates do not establish first priority.

## Read the paper

[Open PDF in a full window](paper.pdf) · [Download PDF](paper.pdf) · [Download the original from Zenodo](https://zenodo.org/records/23203100/files/paper.pdf)

<iframe class="paper-pdf" src="paper.pdf#view=FitH" title="Pure-loss bosonic dynamic capacities: EPnI consequences and consumed-key secrecy accounting — full paper PDF" loading="lazy"></iframe>

## Supporting materials

- [Original source and supporting materials on Zenodo (ZIP)](https://zenodo.org/records/23203100/files/zenodo-upload-kit.zip)

## Collaborate on this result

I welcome substantive collaboration in quantum information theory and bosonic communication on independent verification, careful comparison with prior work and development toward journal review. Coauthorship would reflect actual research contributions and mutual agreement.

Authorship and responsibilities would be discussed in relation to the substantive contributions made.

[Contact Alec](mailto:me@aleckriebel.com)

## Cite this paper

Alec Kriebel. (2026). *Pure-loss bosonic dynamic capacities: EPnI consequences and consumed-key secrecy accounting* (No version number supplied) [Preprint]. Zenodo. [https://doi.org/10.5281/zenodo.23203100](https://doi.org/10.5281/zenodo.23203100).

[Download BibTeX](citation.bib)

## Background and prior work

- [Wilde, Hayden and Guha — Quantum trade-off coding for bosonic communication (2012)](https://doi.org/10.1103/PhysRevA.86.062306): Source of both capacity formulas, the Gaussian ensembles and the original EPnI-conditional converses. The 2011 arXiv versions already contain these formulas and the conditional route.
- [De Palma — New lower bounds to the output entropy of multi-mode quantum Gaussian channels (2019)](https://arxiv.org/abs/1805.12469v3): Theorem 11 and Corollary 12 give the convex entropy-bound formulation of the capacity implication.
- [OpenAI — The entropy photon-number inequality (2026)](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-entropy-photon-number-inequality-September-24-2026/paper.pdf): External unrefereed finite-energy multimode EPnI proof. Its independent-vacuum specialization supplies the sharp entropy bound used for the capacity equalities. The note gives a consequence of this proof.
- [Wilde and Hsieh — The quantum dynamic capacity formula of a quantum channel (2012)](https://arxiv.org/abs/1004.0458v3): Regularized classical/quantum/entanglement resource theorem and finite forward resource framework.
- [Wilde and Hsieh — Public and private resource trade-offs for a quantum channel (2012)](https://arxiv.org/abs/1005.3818v3): Section 5’s printed secrecy condition retains consumed private communication and key in the jointly protected tuple. The note refutes the literal target’s displayed region at zero energy and states a changed generated-secret criterion explicitly.
- [Wilde and Hsieh — Joint dynamic-capacity erratum (2012)](https://doi.org/10.1007/s11128-012-0451-2): Corrects generic optimization claims; it does not remove the consumed-key secrecy condition. No generic efficient optimization or additivity assertion is used here.
- [Hsieh and Wilde — Entanglement-assisted communication of classical and quantum information (2010)](https://arxiv.org/abs/0811.4227v4): Classically enhanced father coding and the expected-input properties needed for the quantum mean-cost selection.
- [Hsieh and Wilde — Public and private communication with a quantum channel and a secret key (2009)](https://arxiv.org/abs/0903.3920v1): Related public/private/key coding work; its printed key-retaining secrecy condition is distinguished from the generated-secret convention.
- [Hsieh, Luo and Brun — Secret-key-assisted private classical communication capacity over quantum channels (2008)](https://arxiv.org/abs/0806.3525): Prior secret-key-assisted private coding and generated-message secrecy.
- [Devetak — The private classical capacity and quantum capacity of a quantum channel (2005)](https://arxiv.org/abs/quant-ph/0304127): Classical-quantum packing and covering machinery used in the direct generated-secret construction.
- [Hayashi and Nagaoka — General formulas for capacity of classical–quantum channels (2003)](https://arxiv.org/abs/quant-ph/0206186v4): Lemma 2 supplies the operator inequality used in decoding. The coding mechanisms are credited to their sources.

[Research home](/research/) | [me@aleckriebel.com](mailto:me@aleckriebel.com)

© 2013–2026 Kriebel LLC.
