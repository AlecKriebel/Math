# Independent adversarial novelty and source-scope challenge: PR234 / 30002291

Author of this audit: independent research agent. No external individual was contacted. No candidate, status, manuscript, provider, Git, index, or ref was changed. Candidate mathematics is stipulated PASS by the assignment; this is an independent priority and target-classification challenge.

## Disposition

**A qualified historical `already_solved` classification is defensible: the original open-ended request has a substantial published sufficient-conditions answer. It is not defensible to use that label to claim the candidate's exact theorem was proved earlier.** The source never fixes the larger class against which completeness could be decided. The defensible claim is therefore “prior affirmative sufficient answer exists,” with an explicit scope note, rather than a containment assertion about all predictable kernels.

**For the user's actual gate—publish only a genuinely new solution of an original unsolved target—do not promote this candidate on the evidence reviewed.** The exact candidate could be a new, source-aligned extension; that possibility survives. It does not by itself show that the historical target remained unsolved, and noncoverage by one theorem is not a novelty certificate. If a status system makes `already_solved` mean “the entire exact candidate is previously established” or “every natural interpretation of the original is settled,” that code overstates the evidence: use a qualified hold or a separate research-note disposition. This is a semantic condition on the code, not a new mathematical uncertainty.

This judgment does not depend on the candidate's current lack of a novelty claim. Even if its author now claimed a complete new solution, the same evidence and gate would apply. No classification mutation is made here.

## 1. Exact claims and success criteria

Let C be the frozen candidate class. It consists of real pure-jump Itô drivers on the real line with no continuous martingale part,

    dY_s=b_s ds + integral z (mu(ds,dz)-nu_s(dz)ds),
    |b_s|<=B,   integral z² nu_s(dz)<=K,

for deterministic B,K, predictable coefficients, at most one nonzero jump at a time, and compensation in L² on finite intervals. The time compensator is absolutely continuous; the mark measure may have atoms. Let g(x)=1_(x>0)x^alpha f(x), 0<alpha<1/2, with f in C¹, f(0) nonzero and both f,f' bounded by an exponential. The prehistory convolution is included. For every deterministic positive mesh sequence tending to zero and every finite list of positive fixed horizons, C asserts full-F stable convergence of normalized squared increments to

    f(0)² sum_(0<T_k<=t) (Delta Y_(T_k))² W_alpha(U_k),
    W_alpha(u)=sum_(l>=1)[(l-u)_+^alpha-(l-1-u)_+^alpha]²,

with independent uniforms independent of all original randomness. These are the candidate's conditions, not conditions silently inserted into the 2013 source.

Let P denote the predecessor class and conclusion recorded in capsule S2. For driver-class comparisons below use the common gamma kernel g(x)=x_+^alpha exp(-x), g0=0, so that tail and kernel distinctions cannot confound the comparison.

There are three independent success criteria:

1. **Truth:** checkable proof of the exact C assertion. This audit takes the independent PASS as stipulated; it does not infer truth from source alignment.
2. **Newness:** the assertion, or a materially distinguishing subtheorem, is not already a theorem or a valid corollary of earlier work. Neither a successful proof nor C not contained in P establishes this.
3. **Original-target alignment:** the proved new statement supplies a previously missing answer to the actual historical request, with its quantifiers preserved. A new extension of a previously answered research question can satisfy truth and newness while failing the user's third criterion.

## 2. Independent reconstruction of the original quantifiers

The complete original contribution was read before any parent reconstruction or sibling report. Its only operative pure-jump conjecture is in capsule S1. The source gives no H_* such that its assertion is “for every pure-jump semimartingale satisfying H_*.” Consequently no reader can establish an exact maximal-class equality merely from that sentence.

Two interpretations must be kept separate.

**Existential sufficient-answer interpretation.** Find a substantial, genuinely non-Lévy class of pure-jump semimartingale drivers, state sufficient conditions, and obtain the displayed type of limit. This cannot mean just another compound-Poisson special case: that baseline was already supplied. The natural question is whether the proposed class advances beyond that baseline in a mathematically meaningful way.

**Arbitrary-characteristic interpretation.** Establish a theorem whose assumptions are stated directly in terms of semimartingale characteristics, permitting general predictable changes in jump-law shape. This is a natural ambitious research program, and C addresses one version. But the source neither prescribes those particular conditions nor explicitly requires freedom from a scalar-volatility representation. Declaring this the unique controlling target adds a substantive quantifier after the fact.

The adjective “rather general” prevents a purely formal argument that any nonempty subclass solves the question. It is not a mathematical predicate with a source-supplied threshold. A classification is therefore a documented judgment about whether a prior sufficient answer is substantial. It is not a proof that all potential future extensions are already known.

### Why P is a substantial answer under the first interpretation (own application)

P supplies entire families of infinite-activity non-Lévy drivers, with arbitrary bounded adapted càdlàg volatility processes allowed by its conditions. For the common gamma kernel, bounded sigma makes the required remote-past integrability finite. Such sigma may depend on the driving past; it need not be constant, deterministic, stationary, or independent. This is a canonical way to move from a Lévy driver to a genuinely semimartingale driver. Treating it as merely the original compound-Poisson result understates the mathematical advance.

Taking p=2, k=1 in P yields the required parameter range on the common kernel. Its jump coefficient is exactly Delta Y_T=sigma_(T-)Delta L_T. Define h(x)=x_+^alpha-(x-1)_+^alpha. Its mark functional and C's are identical in law, because

    sum_(l>=0) h(l+v)² = sum_(j>=1) h(j-(1-v))² = W_alpha(1-v).

The transformation v -> 1-v preserves independent uniform marks and their independence from the original sigma field. The g0 subtraction contributes a time-constant random offset, which cancels in increments. At deterministic horizons the jump-sum limit is almost surely continuous, so the stable continuous-mapping argument transfers functional convergence to joint fixed-horizon convergence. This establishes the substantive match without pretending that P includes all of C.

## 3. Rigorous noncontainment witnesses (own deductions)

### 3.1 C has an index-2 driver outside P

Use the symmetric Lévy measure

    nu(dz)=1_(0<|z|<exp(-1)) dz/(|z|³ log²(1/|z|)).

For b=0 its quadratic rate is

    integral z² nu(dz) = 2 integral_1^infinity u^(-2) du = 2.

For every r<2 its small-jump r-moment is

    2 integral_1^infinity exp((2-r)u)u^(-2) du = infinity.

Thus its jump index is exactly2 although the second-moment integral is finite. It meets C. A nonzero scalar dilation of a fixed Lévy measure preserves its small-jump index: the finite range between a changed cutoff and1 adds only a finite amount. Hence a driver whose compensator has index2 at almost every time cannot have P's scalar representation with a base index below2. This example alone disproves containment of C in P. It does not prove novelty against every earlier result.

### 3.2 C permits symmetric shape changes that no scalar volatility can produce

Take a deterministic time-dependent kernel

    nu_s = delta_1+delta_(-1)                         for s<1,
    nu_s = delta_1+delta_(-1)+delta_2+delta_(-2)      for s>=1.

Construct the corresponding two-sided independent Poisson random measure, with b=0 and all jumps compensated. Its quadratic rate is2 before1 and10 afterwards, so C applies with K=10. It is symmetric and has only finite activity on bounded intervals; neither asymmetry nor index2 is responsible for this distinction.

If this driver were integral sigma_- dL for a single base Lévy measure relative to the same filtration, compensation would give, for nonzero sigma_(s-),

    nu_s(A)=nu_L({x: sigma_(s-)x in A}).

Nonzero scaling is a bijection on nonzero marks and preserves the number of support points. Before1 this forces two support points in nu_L; after1 it forces four. A zero volatility cannot help because the target kernel is nonzero throughout. Contradiction. This is an explicit “general predictable kernel” witness, not an unsupported statement that some mixture must fail scalar representation.

A non-symmetric compensated positive Poisson process is another immediate C/P separator because scaling a symmetric measure preserves symmetry, but the symmetric shape-change witness is stronger.

### 3.3 P has drivers outside C

Choose a symmetric beta-stable Lévy process with 0<beta<2, sigma=1 and the common gamma kernel. Its convolution exists since the kernel is in L^beta; all remote-past integrability conditions reduce to deterministic exponentially convergent integrals. The required tail and eventual derivative conditions hold. But

    integral_(|z|>1) z² nu_beta(dz) = infinity.

It violates C's global quadratic-rate bound. Therefore P is not contained in C either. The candidate's removal of a strict small-jump index bound comes with stronger global moment and characteristic assumptions. Calling C a strict generalization of P is false.

### 3.4 Kernel differences are also real but do not certify priority

The common kernel above was chosen to isolate drivers. Separately, C permits f(x)=exp(-x)(2+sin(x²)); f and f' satisfy exponential bounds, but g' changes sign infinitely often, so |g'| cannot be eventually decreasing. Thus one must also check kernel hypotheses before claiming theorem containment. A harmless remote-tail modification may make this difference easy to handle; no novelty claim follows from the failed literal hypothesis alone.

## 4. Mesh, topology, filtration and boundary attacks

### Mesh quantifier

C explicitly treats every deterministic sequence Delta_n ->0. P is written on reciprocal-integer meshes. A result on 1/n cannot be converted to all meshes by merely rounding the frequency: squared increment sums on two shifted nonnested grids need not be close. For one impulse the leading phase is W_alpha({s/Delta_n}), and changing 1/Delta_n by an order-one amount shifts the phase by an order-one amount times s. Pathwise closeness is not the relevant mechanism.

For a finite vector S of jump times with a weighted density, however, arbitrary-frequency phase mixing follows directly from the Riemann–Lebesgue lemma:

    integral a(s) exp(2 pi i q·s/Delta_n) ds ->0,  q nonzero integer vector.

The deterministic kernel estimates likewise depend on a positive mesh, not on integer arithmetic. This makes the mesh extension a plausible direct adaptation of the established truncation proof, rather than evidence that the old research question is substantively still open. This audit does not silently upgrade P's printed statement to a theorem for every mesh. If literal equality to every source quantifier is required for a binary status, that adaptation must be written and checked, or the scope note must state the difference. C itself supplies such an argument on its bounded-rate class, but one cannot retroactively attribute that proof to the old paper.

### Topology and filtration

On the common driver/kernel regime, functional stable convergence is stronger than C's joint fixed-time assertion. C therefore cannot be marketed as a new functional strengthening. Full-F stability is not a newness argument unless a real filtration mismatch is demonstrated; none was found here. “Stable” must retain its precise sigma-field meaning in either statement.

### Excluded boundary drivers

An atom at a deterministic jump time s can retain the deterministic phase0 on Delta_n=s/n. At alpha=1/4,

    W_alpha(0)>=1,    W_alpha(1/2)<=5/(4sqrt(2))<1.

By continuity W_alpha(U) is nonconstant. The deterministic phase cannot be replaced by the independently uniform mark. This disproves the universal no-hypotheses extension to every pure-jump semimartingale; it does not refute the original invitation to state sufficient conditions.

Time-diffuse and time-absolutely-continuous are different conditions. A continuous marginal distribution for each jump time is weaker than a density for each finite jump-time vector: for example, (T,2T) is singular jointly. C uses a bounded truncated intensity and compensation to obtain the latter property. Do not weaken its assumptions to “random jump times” in publicity. Do not describe its mark kernels as diffuse: the finite-support witness above is allowed.

The alpha endpoints, continuous martingale components, uncontrolled remote history, singular drifts and time-atomic compensators are outside C. Neither C's sufficient conditions nor the original source promise to cover these limits.

## 5. Adversarial tests of the competing dispositions

| Proposed inference | Strongest attack | Disposition |
|---|---|---|
| P answers every driver in C | Sections3.1–3.2 give explicit counterexamples to containment | Rejected |
| C strictly generalizes P | Section3.3 violates C while satisfying P | Rejected |
| C not contained in P proves C is new | A third theorem, an older general result, or a valid corollary could still cover C | Rejected |
| Every sufficient subclass settles “rather general” | An arbitrary tiny subclass would make the qualifier meaningless | Rejected; substantiality must be justified |
| P cannot answer the source because it is not all semimartingales | The source explicitly invites sufficient conditions and names no maximal class | Rejected as a necessary rule |
| Index2 was required by the original conjecture | No such source requirement exists | Rejected |
| The original question remains unsolved whenever a further class is new | This would reopen any open-ended sufficient-conditions question forever | Rejected |
| An unqualified `already_solved` status certifies C as known | Historical target-answering and exact theorem priority are different claims | Rejected |
| Qualified `already_solved` means a substantial earlier sufficient answer exists | P supplies a natural broad non-Lévy family; the predicate “rather general” remains qualitative | Defensible editorial classification, with mesh qualification |
| A scoped new note might survive | Explicit noncontainment and the broad-kernel proof create a concrete distinct theorem to investigate | Viable, with priority unresolved |

A particularly important failed novelty route is to define the original target retroactively as exactly C. That does not identify a missing original quantifier; it replaces the target by the candidate. Conversely, an opponent who claims P is the unique largest intended class has equally exceeded the source. Both routes are blocked as classification proofs unless materially new source evidence appears.

## 6. Strongest defensible novelty salvage and exact remaining gap

The strongest salvage is a separately named theorem about **square-integrable pure-jump Itô convolutions with arbitrary predictable time-absolutely-continuous jump kernels**, explicitly allowing changing mark-law shape and index2, and with convergence specified at joint fixed times on every deterministic mesh. It should credit the finite-jump/truncation mechanism and avoid claiming the first semimartingale-driver answer. The index2 and symmetric shape-change examples should accompany the claim; they make the distinction independently checkable.

This is a salvage of a potentially new theorem, not a certification that an original unsolved problem has newly been solved. No manuscript or upload is prepared under this assignment.

The exact remaining priority gap is: establish whether an earlier result or checkable chain of corollaries already yields that bounded-rate arbitrary-kernel theorem, including its prehistory and full-F phase marking. A theorem merely sharing words such as “power variation” or “semimartingale” does not close the gap, because here the observed convolution need not itself be a semimartingale. Conversely, a general stochastic-convolution result may close it even if its title never mentions ambit processes. This audit's focused primary-source search found no such covering theorem; search nonfinding is only partial evidence.

The exact original-target gap is different: obtain independent source evidence or an explicit project rule identifying a still-unanswered, substantive condition that the historical phrase demands and P fails. The 2013 text alone does not identify one. A plausible desire for arbitrary characteristics is insufficient to certify that requirement retrospectively.

Thus the research disposition for the user's gate is **do not release as a certified new solution of an unsolved original target**. Record a qualified prior-answer finding; preserve the candidate theorem and its open novelty question. If later priority work establishes newness, consider a research note on the exact scoped theorem. Even then, the claim “original problem was previously unsolved” would need its own support.

## 7. Reading provenance, search limits and artifacts

- Independence preserved: only the frozen candidate and primary reading files were read; no parent initial priority reconstruction, no sibling report, no sibling chat coordination.
- Original: extracted text covering all of pp491–493, then rendered and visually inspected PDF pages9–11, stopping at the end of Podolskij's references before the next contribution. Fresh official retrieval reproduced the cached SHA256 exactly.
- Predecessor: model, assumptions(A),(B1), Theorem1.2(i), Remark1.4 and the finite-/small-jump proof in Section4.1 read directly; theorem page5 visually inspected. Fresh arXiv v2 retrieval reproduced the cached SHA256 exactly. arXiv version history independently verified the 14October2016 v2 date.
- Earlier paper: introduction/model, assumptions and Theorem1.1(i) read to distinguish the Lévy-only baseline. It is not used as a substitute for the semimartingale theorem.
- Search: focused primary-paper searches on general semimartingale moving averages, predictable compensators, power variation, Volterra jump convolutions, index2, and the exact predecessor. Generic realized-variation results for the driver itself and discrete pre-averaging/noise models were not treated as coverage. No comprehensive all-literature novelty assertion is made.
- Whole external sources, rendered pages and search payloads stay in the ignored private_reading/ directory. Public-safe authored capsules are each below200 words. Their direct quote totals18 words from S1 and0 from other sources. Authored independent deductions are separated here.
- Completion estimate for this assigned scope challenge:100%. Completion estimate for certifying all-literature novelty of C:unknown, not claimed complete. This work establishes noncontainment and a defensible qualified disposition; it does not resolve the exact candidate's priority.
