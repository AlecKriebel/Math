# Source-first scientific scope INITIAL — row 186 / 23205294

2026-11-17 04:08 UTC. Status: original-only reading and actual hand
controls frozen before support. Completion estimate: 30% of the complete
scientific scope review. No final scientific disposition is issued.

## Identity, exposure and correspondence

Alec Kriebel, *Nonnegative binary rational hafnians: an exact reduction
and approximation and sampling consequences*, DOI10.5281/zenodo.23205294.
Native version1.0.0; publication date6October2026; record created
7October2026UTC and current assets updated10October2026UTC. The PDF
prints6October2026 without a numeric version. Native returned order is
source-and-verification.zip, standalone README.md, paper.pdf; the API's
explicit order value is an empty array. Native record license isCCBY4.
Actual LICENSES.md specifies CCBY4 for newly authored prose/proofs/
documents/audits/data representation and MIT for newly authored Python;
third-party authorship/rights remain. Both rights files were read as
rights statements only.

I personally read the entire sole165-line,18376-byte controlling
main.tex (SHA256 fd84468f33be9164afb796192b397fbbe7165333912603fbef680940f90a247c),
the whole extracted text of all six native PDF pages, and all six fresh
own145dpi page images. The native75751-byte paper.pdf has SHA256
8c93b0f14bc4fd935dbc3a489c5ecca63a8262ba4560a09822b7f65e1036bee7.
It is byte-identical to the archived paper.pdf. Title, abstract, every
lemma/theorem/proof, sampling specification, limits and bibliography in
the native PDF correspond to this TeX; no other TeX candidate occurs in
the opaque finite source inventory. No source compilation was needed.

The whole native record/Description and ordered file API were read.
The Description has three substantive HTML paragraphs and contains
claims about prior checks, audits and Lean statement inspection. The
manuscript repeats that kind of assertion. This is unavoidable native
source exposure, not an independently adopted verdict. The standalone
and archived README bodies, support proofs, programs, stored results,
archived audits/opinions, foreign proof bodies and current peer/root
findings remain closed. Only filenames and opaque byte/mode tables of
those objects have been seen. No peer coordination occurred.

I remember no prior reading of this hafnian paper or the cited
general-graph FPRAS proof. I previously read a different OpenAI
group-algebra construction at the same repository commit during row177
scope review. I also have ordinary prior mathematical knowledge of
matching sums, positive weights, reductions and counting-to-sampling;
absence of all relevant prior knowledge is not claimed. This source-first
family does not claim a fresh mathematical discovery or human review.

## Complete original abstract

We give a self-contained implementation of classical positive-integer
weight removal for perfect matchings. A binary directed acyclic graph
with W paths gives a simple two-terminal graph with matching signature
(W,1,0,0) using4bits(W)−2 vertices. Gluing these gadgets and clearing
denominators reduces every nonnegative binary rational hafnian to an
unweighted simple-graph perfect-matching count with polynomial encoding
length. Consequently, the general-graph FPRAS of OpenAI gives a uniform
FPRAS for this rational model, with exact zero detection. We specify a
bounded-bit counting self-reduction sampler with explicit total-variation
and runtime bounds. The approximation breakthrough, logarithmic weight
removal, and count-to-sample framework are inherited; this note supplies
explicit proofs, bit bounds, boundary cases, and reproducible finite
checks. Its approximation conclusions rely on the cited general-graph
theorem and do not concern signed or complex hafnians.

## Full claim and mathematical contracts

1. Input is an explicitly encoded symmetric2m-by-2m matrix with
   nonnegative binary rational off-diagonal entries. Its diagonal is
   irrelevant. There is no density, connectivity, or positive lower
   weight promise. For m=0 the hafnian is1 and the matching is empty.
   For m>0, positivity is equivalent to support perfect-matching
   feasibility. Negative/complex weights and succinct matrix or graph
   encodings are not licensed by the stated model.
2. For every integer W>=1, a simple bipartite two-terminal gadget has
   signature (W,1,0,0),4ell−2 vertices and at most6ell−5 edges, where
   ell=bits(W). W=0 is removed as a support edge, not passed to bits(0).
3. Put D=product of positive-entry denominators and W_e=p_e(D/q_e).
   The full simple graph H has #PM(H)=D^m haf(A), with exactly
   D^m product_{e in M}A_e lifts of each original matching. It has
   O(L^2) vertices/edges, O(L^2 log(L+2)) encoding length, and the scale
   D^m has O(mL+1) bits. It must not expand an integer W into W copies.
4. The FPRAS consequence is uniform for rational0<epsilon,delta<1,
   has relative error<=epsilon with failure probability<=delta, and
   every execution takes polynomial bit time in full encoded input,
   epsilon^-1 and log(delta^-1). Output is zero iff the exact hafnian
   is zero, on every tape. This stronger exact-zero interface comes
   from deterministic feasibility and a positive-output wrapper, not
   from treating a random zero estimate as a proof of zero.
5. For feasible unweighted N=2k>=2, the sampler always returns a
   perfect matching; TV from uniform is<eta. It uses at most C=k^2
   counting calls with alpha=eta/(4k), gamma=eta/(4C), fixed categorical
   budget b=ceil(log2(4C/eta)), at most C+1 exact feasibility/witness
   checks and at most kb categorical fair bits. Oracle randomness is
   additional. The runtime must hold on failed tapes too. No rejection
   loop or expected-runtime-only substitution is allowed.
6. Projection of this sampler through gadget fibers gives TV<=eta
   from the weighted law product A_e / haf(A). Zero inputs report
   infeasibility exactly; the m=0 case returns the empty matching.
   The runtime is polynomial in eta^-1, not promised polynomial in
   log(eta^-1), and TV is not pointwise multiplicative near-uniformity.

The whole original approximation/sampling consequence is the review
target. Establishing only a gadget lemma or a conditional wrapper would
not clear that complete claim. No narrower replacement or extended
repair is authorized if the central imported theorem cannot be justified.

## Actual independent controls, not merely planned tests

HAND_CONTROLS.md freezes an independent path/signature derivation and
small W boundary counts, a full fiber/bit-size proof, an exact rational
four-vertex example with an irrelevant positive edge and zero entries,
an explicit signed cancellation boundary, the exact-zero wrapper proof,
an adaptive-history TV coupling, rational finite-CDF examples (including
bad-count fallback), call/bit complexity, and projection contraction.
These are written mathematical controls, not native test outputs.

No native or own mathematical program has been executed. The only
programs applied to the source were installed pdftotext and pdftoppm for
reading; both exited0 with literal empty stdout/stderr. One initial
directory setup command reported a missing reviews parent; mkdir -p then
created only the incidental parent and this owned scope/pixels folder.
No source or older packet was changed by that setup diagnostic.

## Central imported interfaces that remain to be checked after resume

The exact cited primary is OpenAI, *A Fully Polynomial Randomized
Approximation Scheme for Perfect Matchings in General Graphs*,
23September2026, Theorem1.1, pinned at
adc7f1241b42e322a6451854ab7e4b4c146bf78a, source path
preprints/A-Fully-Polynomial-Randomized-Approximation-Scheme-for-Perfect-Matchings-in-General-Graphs-September-23-2026/main.pdf.
Required interfaces are every finite simple undirected graph (not only
bipartite/dense/positive-count promised inputs), a uniform relative
approximation, nonnegative rational output, amplified failure bound,
and worst-case EVERY-TAPE polynomial BIT time/output length for encoded
parameters. The theorem's substantive proof and the algorithmic steps
that supply these properties must actually be checked. A favorable
abstract, theorem label, finite enumeration or a statement-only Lean
inspection is insufficient for the central universal FPRAS claim.

Edmonds' exact feasibility/witness interface is required separately.
The Horner/signature and sampling arguments are supplied directly here;
McQuillan/Dell/JVV are credited precedents, not uninspected replacements
for the written local proofs. The entropy512^n approximation is not a
relative FPRAS and cannot substitute for the general-graph theorem.
The cited comparisons/priority statements need honest scope, without
turning this attributed consequence into a firstness claim.

Status at this boundary: those foreign bodies and support are unopened,
and the imported central proof is unresolved by this lane so far. No
global scientific PASS, DEFER or repaired theorem is issued at INITIAL.
Default follow_up:null. No Git/W/Sheet/deployment/release/contact or
prepared outreach action. Freeze the finite boundary and HOLD all owned
writes/executions pending the root checkpoint and explicit resume.
