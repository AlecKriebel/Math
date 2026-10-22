# PR1265 /10000003: independent original-question, mathematical and existing-publication audit

Date:22October2026 UTC. PR head `b1f0bc241aa84d7bef150b77a50c986889970240`, base `4b27092a448d53b61408355ce44ec38d103a1ce4`. Exactly eight added paths under attempts/10000003, no QUEUE edit; immutable object contents, full PR description and all eight bodies independently read. This audit makes no external write, Git mutation, source-author-program execution or contact. Its private folder is separate from all closed earlier reviews.

## Decision and action boundary

**Accept full prior coverage of the original inverse-square equilibrium problem under the established finite-one-sided-force and increasing-enumeration convention.** Alper Ferudun's Theorem1.2 gives the result for every `1<s<=2`, including the exact original `s=2`, without any uniform lower or upper gap bound. Its full primary proof has been independently challenged and is supported. The original is not reduced here to periodic configurations, an attained extremal gap or a density-bounded subclass.

The existing publication is Ferudun's **version1.0,3October2026**, DOI **10.5281/zenodo.23113437**, concept DOI **10.5281/zenodo.23113436**, and later arXiv **2610.06944v1**, DOI **10.48550/arXiv.2610.06944**. Both Zenodo DOIs and the arXiv DOI resolve to the correct family. Zenodo is DONE/submitted; latest-version and version-list APIs return the same single published version. All three public payloads were freshly downloaded and verified by declared size, MD5 and independent SHA256; source ZIP CRCs and every33 nondirectory-member hash were checked. The author-hosted PDF and source ZIP are byte-identical to their Zenodo counterparts. This is an unrefereed, explicitly AI-assisted preprint, not a journal article or an independently human-refereed proof.

An original-only four-string spreadsheet proposal is justified and retained in `PROPOSED_ROW.json`, with B blank. Two fresh numeric-gid43-column reads,09:16:09 and09:25:14UTC, both return191rows and no relevant target, DOI, author-result, title or semantic match. Equilibrium leads114/139 concern reinforcement/Nash problems. No row has been written; parent adoption and an immediate concurrency recheck are still required. Do not create a new record for this already published original result.

**Material source-version finding:** the earlier Zenodo manuscript's Remark5.3 already sketches the same little-o counting/Hölder mechanism, polynomial exponent `s²-3s+1`, and endpoint `(3+sqrt5)/2` used by the PR extension. It expressly withholds an `s>2` theorem claim. The later arXiv revision removes this sketch and retains only the small-gap obstruction. Therefore the extension may be accepted as a completed proof, but should be attributed as filling in an already public Ferudun sketch. It is not supported as an independently new mechanism. The proposed row does not turn that unclaimed sketch into a formal prior theorem for the larger range. This distinction does not affect full prior coverage of `s=2`.

## 1. Original sources: what was and was not specified

The actual one-page [Benjamini note](https://arquivo.pt/wayback/20201231041612id_/https://www.wisdom.weizmann.ac.il/~itai/equilibrium.pdf), datedMay2015, was freshly retrieved and read in full and as a page image. The original Weizmann URL now returns404; the archived actual PDF is151376bytes, SHA256 `b90532901e2eb878b85f5ef52b51c898a7edcb535b7bb1d553884cc61c4f693d`.

It starts with a locally finite configuration on the real line, introduces a pair force with inverse square as its displayed example, indexes particle positions by Z, and imposes zero signed force at every position. Question0.1 asks for an affine position sequence. The independent Warwick workshop PDF, Section4, Question5, repeats the question on PDF3; both text and the relevant page were checked. The short sources do not expressly specify summation convention or increasing labels. They are not evidence that a principal value or arbitrary relabeling was intended.

The primary [Georgakopoulos–Kolountzakis arXivv1](https://arxiv.org/abs/1604.01649v1), PDF2, explicitly requires finite force separately from each side and zero net force. Its Problem1 asks about subsequent-particle distances, and its Theorem1 proof uses spatially ordered particles. This supplies a documented mathematical convention for the original question, not a newly manufactured restriction. Definition3.1 and Theorem4 in the older paper concern a separately restricted continuation result with both lower and upper gap bounds; those bounds are not smuggled into the present theorem. Only the stated portions of this older work were independently read; its journal PDF was not inspected here.

The accepted original instance is therefore: a nontrivial set of distinct real particles, with finite left and right inverse-square sums at each particle and equality between them, must be `b+hZ`, `h>0`; its strictly increasing enumeration has `a_n=b+hn`. Distinctness is forced by a defined inverse-power interaction. The original bi-infinite enumeration excludes the singleton. A standalone set theorem must explicitly exclude it, as the corrected PR does.

An arbitrary permutation of Z can relabel a lattice nonaffinely without changing its set or physical equilibrium, so an affine arbitrary-label assertion would be false for a trivial reason. This audit does not substitute that artificial assertion for the spatial-order question. Similarly, mere local finiteness does not ensure finite force: `0` and `±sqrt(n)` are locally finite, and at0 each side gives the divergent harmonic series even though symmetric partial sums cancel there. This is a convention control, not a claimed equilibrium of that set at all its other particles. No principal-value classification or universal strictly decreasing force-law theorem is accepted. The original note suggests general forces, but the catalogue's inverse-square instance is fully answered within the established finite-force convention.

## 2. The proof's hypotheses are enough: no hidden uniform spacing

Let `s>1` and assume the two signed-side force sums are finite and equal at every x in a set X with at least two points. Fix x0. Every other point within distance L contributes at least L^(-s) to a finite positive force sum. Thus every bounded interval has finitely many particles and X is countable. A finite force at one particle also gives finiteness at any other particle: finitely many nearby terms are harmless, and sufficiently distant distances are uniformly comparable with those from x0.

If X were bounded above, local finiteness would give a largest particle. All its nonzero forces point the same way and there is at least one, contradicting equilibrium. The same holds below. X therefore has a bi-infinite increasing enumeration, unique up to an integer shift, tending to both infinities. Put `g_n=a_(n+1)-a_n>0` and translate a0 to0. No uniform infimum or supremum of the g_n is used.

For consecutive gaps u,v, positive-force comparisons at the two neighboring particles, followed by cancellation of finite equal forces, give

`1 <= 2(v/u)^(-s)+(1+v/u)^(-s)`.

The right side strictly decreases from infinity to0 and has value greater than1 at ratio1. Its unique value-one root r_s is greater than1. Reflection gives both directions, so adjacent gaps have ratio between1/r_s and r_s. Inverse square has r2 approximately1.538615. This is only an adjacent-ratio estimate; it permits gaps shrinking to0 or growing without bound along the line.

For n!=j use `D=|a_j-a_n|`, `D'=|a_(j+1)-a_(n+1)|` and the positive divided difference

`c(n,j)=(D^(-s)-D'^(-s))/(D'-D)`, or `s D^(-s-1)` if D'=D.

Exchanging n,j preserves both distances, hence c is symmetric. Subtract the two absolutely convergent force equations after shifting indices. For j<n both the sign and the distance difference reverse; for j>n neither does. Termwise this gives `sum_{j!=n}c(n,j)(g_j-g_n)=0`, with absolute convergence bounded by the two positive force sums. The D'=D case contributes0 to that identity and has a valid positive continuous-limit conductance.

The adjacent case and the nonadjacent gap decomposition give `min(D,D')>=D/(1+r_s)`. The mean-value theorem yields `c(n,j)<=K_s D^(-s-1)` with `K_s=s(1+r_s)^(s+1)`. For each fixed n, all D are at least `delta_n=min(g_(n-1),g_n)>0`; its conductance row is bounded by `K_s delta_n^(-1)` times its finite force. Only this pointwise delta_n, not a global lower gap, is needed. Adding the convergent constant-gap row to the difference identity establishes `sum_j c(n,j)g_j=pi(n)g_n`.

The transformed conductances `c*(n,j)=c(n,j)g_ng_j` have row mass `pi*(n)=pi(n)g_n²`, finite and positive. They define an irreducible discrete-time Markov kernel P*, and `1/g` is a positive integrable harmonic function for it. Nothing about continuous-time nonexplosion is required. The transformed row is proved finite before recurrence is considered; recurrence is not being inferred merely from Z indexing or from doing a Doob transform.

## 3. Recurrence with infinitely many neighbors

Both actual source versions include a proof of the needed finite-row version of the Dirichlet principle. If u is finitely supported and w is integrable against each conductance row, the bilinear Green sum is absolutely summable: bound it by twice a finite sum of `|u(x)| sum_y c(x,y)(|w(x)|+|w(y)|)`. Symmetry then proves the Green identity without an unjustified interchange of two infinite sums.

For a finite set B containing an origin o and a finitely supported f with f(o)=1, let H be the probability of hitting o before exiting B, extended by0 outside B. This is bounded and supported in B, with H(o)=1 and harmonicity on B minus o. Irreducibility guarantees an exit path from each state of the finite set B minus o. Finitely many positive path probabilities have a positive minimum, so the probability of avoiding both o and the exterior forever is0. This detail remains valid with infinitely many neighbors.

First-step analysis and Green's identity give `E(H)=pi(o) Pr_o(exit B before return)`. The mixed energy of H and f-H vanishes by harmonicity, hence `E(f)>=E(H)>=pi(o) Pr_o(never return)`. Finite row masses make the finite-support energies finite. Thus finite-support origin-one functions of energy tending to0 prove recurrence.

For an irreducible recurrent chain a positive harmonic function evaluated along the chain is a nonnegative integrable martingale, so it converges almost surely to a finite limit. The chain visits each state infinitely often, simultaneously over the countable state space. Each state's constant subsequence has that same limit, proving the positive harmonic function constant. Applying this to1/g will finish the gap theorem once cutoff energies vanish. No boundedness of g or1/g is assumed. The standard nonnegative martingale convergence theorem is the usual imported background; the network extensions are explicitly proved in the source.

## 4. All tails, support boundaries and the inverse-square logarithm

Use the spatial tent cutoff `f_R(n)=min(1,max(0,2-|a_n|/R))`. Local finiteness gives finite support. For sufficiently large R, a0=0 lies on its plateau and the open support interval contains at least two particles. Every pair with different cutoff values has an endpoint in that interval. Its difference is at most `min(1,|a_j-a_n|/R)`. Split its unordered energy sum into distances at most R and greater than R; the conductance estimate bounds energy by K_s times these near/far sums.

For n<j, integrate on `[a_j,a_(j+1)]` for the right comparison and `[a_(n-1),a_n]` for the left. Adjacent ratios control the distance variation by1+r_s, and the left comparison additionally needs the factor r_s to convert the interval's length to g_n. Nonnegative additivity sums these disjoint intervals over the entire infinite half-lines. The far tails are bounded by convergent integrals of `t^(-s-1)`.

At the supported endpoint set, the sum of g_n includes the outgoing right-boundary gap. If m<M are its extreme indices, that sum is `a_M-a_m+g_M`; `g_M<=r_s g_(M-1)<=r_s(a_M-a_m)`. Therefore it is at most `4(1+r_s)R`. It would be incorrect to discard that outgoing gap or assume it small merely because a_M is supported. Charging each far pair to its supported endpoint(s), permitting harmless double charging, gives

`S_far <= 4(1+r_s)^(s+3) R^(1-s)/s`.

For a contributing near pair both endpoints lie inside (-3R,3R), and its initial gap is at most R. Let I_R contain such eligible initial indices; their disjoint intervals lie in (-3R,4R), so `Sigma_R=sum_(I_R)g_n<=7R`. Their upper integral endpoint is at most `(1+r_s)R`, including the last interval beyond the last near particle. The exact common bound is

`S_near <= (1+r_s)^(s-1) R^(-2) sum_(I_R) g_n integral_[g_n,(1+r_s)R] t^(1-s) dt`.

For1<s<2, enlarge the lower integral limit to0, giving `7(1+r_s)R^(1-s)/(2-s)`, which tends to0. At s=2 the integral is logarithmic. Concavity of `z log((1+r_s)R/z)` gives a sum bounded by `Sigma_R log((1+r_s)R N_R/Sigma_R)`. Substituting7R is not unconditionally monotone: split at the maximum of `z log(Lambda/z)`, Lambda=(1+r_s)R N_R. This yields

`S_near <= 7(1+r_s)/R * max(1,log((1+r_s)N_R/7))`.

Finite force at a0 bounds the count by `N_R<=1+(3R)^2 T`, T the total force at0, in the translated presentation; the source's untranslated4R variant is also valid. Thus the near bound is O(log R/R). If I_R is empty the near energy is0. The earlier Zenodo prose omitted stating this trivial separate branch before its Jensen division by N_R; the arXiv revision explicitly adds it. This is a harmless local repair, not a missing case invalidating the theorem.

Both near and far energies vanish at every fixed1<s<=2. The preceding Dirichlet argument proves recurrence, then1/g is constant, and telescoping gives the positive-spacing affine sequence. Conversely each such lattice has equal finite one-sided sums `h^(-s) sum_{k>=1}k^(-s)`. This proves the complete inverse-square statement and its prior wider range.

## 5. Extension: mathematically valid, but the exact earlier sketch must be credited

The PR's completed argument for2<s<=s* also survives scrutiny. Finite positive force gives `A(L)=o(L^s)`: separate a fixed finite inner set from an arbitrarily small tail of the convergent force series, take L to infinity first, then enlarge the inner set. It follows that `N_R=o(R^s)`, with no rate claimed. For2<s<3, the last integral is bounded by `g_n^(2-s)/(s-2)`. Concavity with exponent3-s in(0,1) gives

`sum g_n^(3-s) <= N_R^(s-2) Sigma_R^(3-s)`.

Consequently `S_near <= C_s (N_R/R^s)^(s-2) R^(s²-3s+1)`. At `s*=(3+sqrt5)/2`, the power of R is exactly0, while s*-2 is positive; the little-o factor therefore gives decay even at the endpoint. For2<s<s* the R power is negative. I_R empty is handled separately. The far bound and all network facts already hold for fixed s>1. These deductions genuinely prove the corrected extension, including its endpoint, without requiring a uniform force bound across all particles.

Above s* an unspecified little-o rate does not make this upper bound decay: at s=8/3 its R exponent is1/9, and an epsilon_R=R^(-1/12) would still leave positive exponent1/18. This is a limitation of the estimate, not a counterexample to rigidity. At s<=1 the lattice's finite-force hypothesis fails. No all-force-law or principal-value theorem follows.

**Attribution repair before promoting extension prose:** Zenodo23113437's actual PDF printed9 and its main.tex Remark5.3 already identify `A(3R)=o(R^s)`, Hölder, the same exponent and the same closed endpoint. Its verification report independently records that range as an unclaimed sketch. ArXivv1 retains only the small-gap expression and omits those details; the315-line private TeX diff authenticates the change. The PR's limited description is accurate for its cited arXiv version but incomplete across the earlier family. If the extension is separately presented, describe it as a full exposition/proof completion of that earlier sketched mechanism, and cite the earlier DOI. Do not say Ferudun formally proved the larger range in Theorem1.2, or that the same-endpoint deduction is a newly discovered mechanism of this PR. No historical discovery or worldwide firstness certification is supplied.

## 6. Independent controls and their limits

`verify_readonly.py` is reviewer-authored standard-library code, written without importing any packaged implementation. It uses exact Fraction arithmetic, rational enclosures for logarithms via a range-reduced atanh series, and exact arithmetic in Q(sqrt5) for the endpoint. Explicit RuntimeError guards remain active in normal/-O/-OO modes. Its source was inspected before execution; none of the external programs, TeX or Lean sources was executed.

It checks10800 ordered pair controls on rational gap profiles at scales10^-6,1,10^6, including constant, alternating, very small and very large nonuniform gaps. Shifted force identities include both sign directions and equal-distance branches; conductance and both integral comparisons are checked exactly at integer exponents2,3,4. Exponents3/4 test the common algebra only, not a claimed theorem there. Finite cutoff energies are compared with the analytic near/far bounds using rational logarithm enclosures. Those profiles are expressly not assumed equilibria.

An infinite-degree complete network with geometric vertex weights provides an exactly summed Green-identity control for an unbounded row-integrable function, including all edges outside the finite test support; dropping the tails fails. A transient birth-death network with a nonconstant positive harmonic function tests finite transformed rows, reciprocal harmonicity and return probabilities, and prevents a circular assumption that the transform itself creates recurrence. Additional controls cover the exact endpoint, invalid power concavity outside its range, insufficient little-o above the endpoint, local finiteness versus force divergence, arbitrary labels and the singleton. Finite controls supplement the universal written deductions; they do not establish those deductions by sampling.

The same read-only checker authenticates the closed inventory, fresh source receipts, all three Zenodo payloads, every ZIP member, both spreadsheet captures, immutable PR blobs, nested PUBLIC_MANIFEST and proposed-row restrictions. It reads only this audit folder and writes nothing. Normal/-O/-OO outputs and the final validation metadata are retained. No source-author numerical result is claimed independently reproduced merely because its output exists in the archive.

## 7. Publication identity, support and bounded priority/accounting evidence

Zenodo record23113437 is version1.0 with publication date3October2026, creator Ferudun, Alper, licenseCC BY4.0, preprint type and explicit AI/unrefereed disclosure. Registry creation is3October02:00:53UTC. Current arXiv metadata has only v1, submitted3October09:46:28UTC, and explicitly links this earlier Zenodo DOI. The author's current canonical reading-copy PDF/source are identical to the published Zenodo payloads, not to the later arXiv PDF: their different sizes/hashes and the substantive Remark5.3 difference are preserved. The family identity therefore rests on exact records, source crosslinks, full mathematical content and payload checks, not title similarity alone.

Published support comprises the147782-byte11-page PDF,79029-byte source ZIP and15912-byte verification report. The ZIP contains33 nondirectory files totaling203433bytes, including manuscript, references, reproduction instructions, diagnostic programs and outputs from several runs. Every member's bytes/hash and CRC are checked. The standalone report equals its archive copy. The reproduction README and report were read for scope and the nonessential role of diagnostics. The programs are present and their outputs preserved; no author-program execution or blanket computational reproduction is claimed. The theorem is a complete analytic/probabilistic proof and does not rely on those diagnostics.

The relevant predecessor is Georgakopoulos–Kolountzakis, arXiv1604.01649v1, journal DOI10.1090/proc/13492, Proc.AMS145(2017),3501–3511. Its exact inspected primary body proves the attained-extremal-gap subclass and describes the unrestricted aperiodic inverse-square question as unresolved. This is partial antecedent coverage, not the full target DOI to record. The complete Ferudun theorem is a current prior publication regardless of whether another still earlier proof may exist.

Targeted public searches, recorded in SEARCH_INDEX, recovered the exact family. Zenodo original-ID/title searches each return only23113437. DataCite title search returns precisely the version DOI, concept DOI and arXiv DOI of this same family, not three different mathematical publications. No second family or public partial upload was authenticated. Private drafts cannot be excluded by public searches. The arXiv and source discussion of crystallization/Aubry–Mather background is not treated here as an independently exhaustive survey of every classical dependency or priority claim; it is unnecessary to claim such firstness to reconcile an already complete matching publication. No claim that the original was still open at PR development is made: the completed original theorem is already public before the dated PR exposition.

Both full43-column numeric-gid spreadsheet reads give the same SHA256 `fadcb0e361e60b8267883420bd979f37695303592a800019b65d7cb04ad7e8d1`. No matching original, DOI family, result or PR is present. The proposal credits the external author, leaves Solution Chat URL blank, uses the exact existing version DOI and states the force/label conventions. It does not add a separate row for the concept/arXiv alias or claim the exponent extension as a prior formal theorem. Immediate pre-write semantic deduplication remains the parent's responsibility.

## 8. Final disposition and privacy

Accept original inverse-square mathematics and matching existing publication; reconcile one existing-paper row after adoption and the fresh concurrency check. No new Zenodo record is warranted. Preserve the further correct extension with the explicit earlier-sketch attribution correction and no novelty assertion. Do not reject a full original answer merely because the short2015 note omitted a summation convention that the subsequent primary literature makes explicit; also do not overstate the result as a principal-value, arbitrary-label or general-force classification.

`ALIASES.json`, `VERSION_COMPARISON.json`, `SOURCE_INDEX.json`, `SEARCH_INDEX.json`, `PUBLISHED_SUPPORT_INDEX.json`, `PRIORITY_DECISION.json` and `PROPOSED_ROW.json` give the machine-readable boundaries and provenance. All primary/PR bodies, ledger contents, source extracts/diffs/renders and search responses stay in ignored private_sources and are marked private in the final manifest. Only authored reports/checkers and hash metadata are public-scope artifacts. The closed hash inventory includes nested manifests and excludes exactly its own top MANIFEST.json. No prior closed review was changed.
