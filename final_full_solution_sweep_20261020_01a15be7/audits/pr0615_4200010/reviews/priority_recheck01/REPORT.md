# PR615: independent recheck of the priority rejection

**Verdict: maintain the priority hold/closed-unmerged disposition for the
current novel-full-solution workflow. The mathematical classical implication
survives attempted falsification. This is not a rejection of the candidate's
correctness. No older explicit answer to the named Knill question has been
authenticated.**

The candidate at exact Git head
`f1bb8d0eabb63548d9008c291a564f42b714ab19` correctly supplies a compact smooth
autonomous Hamiltonian with a full Liouville-volume 1/4 band, all four tangent
Lyapunov exponents zero, and no positive-measure invariant almost-periodic
subregion. Its central unrestricted conclusion is obtained by the standard
suspension and Hamiltonian extension of the exact Anzai skew shift, followed
by elementary measure and frame calculations. I found no substantive new
mechanism remaining after these directly inspected older inputs are credited.
`DERIVATION.md` records the complete independent implication and its limits.

## Exact source scope

Knill's [author-hosted problem list](https://people.math.harvard.edu/~knill/seminars/intr/),
dated19 October2000, item10, asks for positive measure outside the almost-periodic
invariant good region and the positive-exponent bad region. The existence
question prints no Euclidean, cotangent, analytic, natural-mechanical, contact,
genericity or weak-mixing requirement. Weak mixing occurs in a separately
marked guess. Its informal almost-periodicity wording is interpreted here in
the same standard full-L2 Koopman and modulo-null subset sense explicitly used
by this PR; this review does not certify the author's unstated intentions.

Anzai's [1951 version-of-record paper](https://doi.org/10.18910/11966),
Section6/Theorem6 and corollary, printed pp91-92, was visually inspected from
the exact primary PDF. It treats precisely (x,y) mapped to (x+alpha,y+mx).
Formula39 gives the Fourier shift; at m=1 this is the candidate's exact map.
The corollary supplies ergodicity and continuous spectrum on the orthogonal
complement of the x-only functions. It does **not** assert continuous spectrum
on the entire L2 space. The x-only/clock factors therefore create no contradiction.

The full proof of de Leon-Saralegi's [1993 Lemma3.2](https://doi.org/10.1088/0305-4470/26/19/032),
printed pp5036-5037, and the extended-Hamiltonian passages on pp5037,5042 were
visually inspected. The symplectic form and the Reeb realization agree exactly
with the required extension. The S1 remark on p5037 is only a statement about
the symplectic form; it is not permission to write a real Hamiltonian equal to
the circle coordinate. The dated first scientific page, p5033, was also checked.
No assertion of reading every unrelated section of either article is made.

Both PDF bodies were reused from the prior private source cache only after
rechecking their exact recorded hashes. `PRIMARY_CUSTODY.json` gives bytes,
hashes and local provenance. The exact relevant pages were newly rendered and
inspected. The web reader independently exposed the institutional Anzai record
and current author problem list; its de Leon PDF request timed out. No fabricated
fresh-download claim is made for the reused de Leon body.

## Deliberate attacks

| Attack | Independent outcome |
|---|---|
| The cited skew shift is merely analogous | Exact map at m=1; displayed older Fourier formula matches. |
| An area map is silently assumed Hamiltonian on its original torus | It is suspended as a cosymplectic Reeb field and then thickened. No Hamiltonian torus isotopy is assumed. |
| One null energy surface is being substituted for full phase volume | The product Liouville form is nu dE. An interval of length1/4 supplies full four-dimensional measure1/4. |
| The thickening has infinite volume or an incomplete flow | Restrict to N times(0,1): finite volume one, real H=E, fixed E and compact N give completeness. A compact cutoff version is also explicit. |
| H=E on a circle is not globally real | True; the correct compact construction uses a smooth periodic cutoff h that equals E only on the band. |
| Only tangential/return-map exponents vanish | The global frame gives I+s h' L+s h'' K in all four directions, with every product of two generators zero. Derivative and inverse are polynomially bounded. |
| Continuous spectrum comes only from averaging integrable energy frequencies | Each conditional suspension flow already has an orthogonal integer-time L2 orbit. |
| Another positive invariant subset could be almost periodic | Rational-time Fubini plus strong continuity and fiber ergodicity force every such subset to be N times J modulo null sets; each positive J retains the orthogonal orbit. |
| A clock eigenfunction makes a positive good region | It supplies a factor, not a subset whose entire Koopman representation is almost periodic. |
| An L2 seam trace is assumed | The proof uses interior translation invariance and the actual time-one L2 identity; no trace at a null seam is required. |
| Compactness or globally real H introduces a substantial new mechanism | A standard cutoff on the classical circle thickening supplies both, with the same tangent and invariant-subset calculations. |
| Classical derivability proves an earlier named resolution was published | False. That historical assertion remains unsupported and must not be used. |

## Checkable computation and limits

The original12628-byte proof was compared directly with its exact immutable Git
blob, not just trusted from the older audit folder. The independent standard-library
checker verifies1089 skew-iterate group identities,1089 Fourier-index comparisons,
5 frame-descent identities,625 full tangent identities,625 inverse identities,
625 symplectic identities, and the four nilpotent-generator products. Its six
false-formula/incorrect-inference witnesses distinguish wrong frame sign,
missing shear, missing energy derivative, wrong return sign, clock-factor
confusion and a global circle-coordinate Hamiltonian. These are exact finite
formula checks, **not** six copied-process mutations or independent proofs.
Normal and optimized runs produced identical complete JSON.

These computations supplement the universal derivation. They do not prove
irrational ergodicity, strong continuity, disintegration, smooth cutoff existence,
historical priority, or the universal theorem by enumeration. The proof supplies
those arguments conventionally; no numerical approximation to sqrt2 is used as
an ergodicity certificate. `VALIDATION.json` records exact input/output hashes.

## Priority adjudication and remaining gap

The exact old mechanisms remove the central unrestricted existence difficulty.
The present workflow asks whether the result follows directly from existing
literature and requires a genuinely new full solution. Under that criterion,
the current PR does not clear the novelty gate. Its compact presentation and
careful full-band proof are mathematically useful safeguards, but give an
attributed classical-corollary exposition of the same existence mechanism.

It would be incorrect to record “Anzai/de Leon already explicitly solved Knill's
question.” Neither inspected older paper names the later question or states
this exact combined conclusion. The first historical explicit observation of
the connection remains unverified. No bounded search proves its absence:
three fresh broad exact-term searches returned no authenticated primary exact
resolution and substantial irrelevant matches, which supply no priority evidence.
The positive primary match and checkable deduction, rather than search failure,
support the present recommendation.

A useful attributed expository note is not thereby prohibited in general; it
would need a different publication objective and appropriately modest framing.
This recheck supplies no genuinely new restricted theorem to substitute for the
original target. The current repository audit should preserve the correct
candidate and the precise classical implication, keep the already closed PR
unmerged, and avoid a new DOI or ledger row in this workflow. No new comment,
closure, queue edit, Git mutation, provider write or outreach was performed.
Publication/draft deduplication and final disposition remain the parent's task.

Review limitations: no global historical-first certification, no formal proof
assistant, no independent human peer review. AI was extensively involved in
this review. It is an adversarial audit artifact, not a new research preprint.
