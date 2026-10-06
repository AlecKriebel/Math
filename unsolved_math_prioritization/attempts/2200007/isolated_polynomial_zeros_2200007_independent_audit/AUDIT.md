# Independent audit: ID 2200007, Conjecture 4

Date: 6 October 2026. Exact target: AMR-021-0007, rank 899.

## Decision

**The conjecture is false by credited prior work.** The original nine-file author
freeze contains a correct, scope-matched mathematical verification of the
DannyExperiments counterexample. This audit accepts that mathematical conclusion,
with zero new research approaches and no new-discovery claim. The executable
wrapper has three reproducibility/trust-boundary limitations, repaired in a
separately pinned derivative. The original freeze is preserved byte-for-byte.
Use the derivative for the strengthened portable replay contract. This is an
independent mathematical/code audit, not human peer review or formal verification.

The credited work is [Many Isolated Real Zeros of Sums of Squares, Theorem 1.1](https://github.com/DannyExperiments/ottaviani-shapiro-sos-counterexample/blob/41e3d18a8c536e5a859201afd5faefe2b0ecd315/paper/manuscript.tex).
The [public release](https://github.com/DannyExperiments/ottaviani-shapiro-sos-counterexample/releases/tag/v1.0.0)
was published on 10 August 2026. The DOI
[10.5281/zenodo.21875290](https://doi.org/10.5281/zenodo.21875290) is credited from the
pinned public citation file; it is not our publication or discovery. Release
metadata independently reports the manuscript's matching 8,749-byte SHA-256.
The GitHub release itself predates and expressly does not claim the DOI.

## 1. Target identity and exact original hypotheses

All three complete corpus files were independently read and rehashed; their sizes
and hashes match the author packet. Exactly one catalog entry and one problem
record have decimal ID 2200007. The catalog uses a string ID and the problem record
an integer; this representation difference was explicitly normalized. Rank 899,
problem number, exact statement hash, and the hash of the complete record/report
pair all match. The complete record and report contain literature-only triage,
not an inherited proof or computation. `SOURCE_AUDIT.json` records only identities,
hashes and outcomes; no dataset text is redistributed.

The audit independently rehashed the local public Shapiro PDF, extracted its text,
rendered page 2, and visually read the complete page. Live arXiv HTML provides a
second inspection route. [Problem 3 and Conjecture 4](https://arxiv.org/html/1503.05295v1)
concern real nonnegative polynomials of exact degree 2k in l variables, expressible
as a finite sum of squares of real polynomials of degree at most k. The conjecture
sets the maximum number of isolated real zeros equal to k^l. No specified number
of square summands, homogeneity, genericity, or finite complex zero-set condition
is imposed. The discussion of asymptotics for the non-SOS maximum is separate.
The fixed example below meets the exact-degree condition, even though the prior
manuscript's introductory definition is phrased with a degree upper bound.

## 2. Independent mathematical verification

Use ten real coordinates t, x_0, ..., x_8. The nine quadratics, written out to remove
index ambiguity, are

    q_0 = x_0^2 + t^2 - 8t
    q_1 = x_1^2 - t^2 + t
    q_2 = x_2^2 - t^2 + 3t - 2
    q_3 = x_3^2 - t^2 + 5t - 6
    q_4 = x_4^2 - t^2 + 7t - 12
    q_5 = x_5^2 - t^2 + 9t - 20
    q_6 = x_6^2 - t^2 + 11t - 30
    q_7 = x_7^2 - t^2 + 13t - 42
    q_8 = x_8^2 - t^2 + 15t - 56.

Let P be their squared sum. Each summand has degree exactly two. The sum has degree
at most four; the coefficient of x_0^4 is 1 because only q_0 involves x_0. Thus P is
a nonzero polynomial of degree exactly four, and is nonnegative on real inputs.
Since a sum of nonnegative real squares vanishes exactly when every square
vanishes, the real zeros of P are exactly the common real zeros of these nine
quadratics. This equivalence would be invalid over the complex numbers; no complex
argument is being substituted here.

The first equation requires x_0^2=t(8-t), hence 0<=t<=8. For i=1,...,8 the equation
requires x_i^2=(t-(i-1))(t-i). Its right side is negative throughout the open interval
(i-1,i), and nonnegative on the complement. The union of the eight forbidden open
intervals is [0,8] minus its nine integers. Therefore every real zero has an integer
t in {0,...,8}. This is an exclusion of the complete real line by factor signs,
not an inference from sampling finitely many t values.

Conversely, at each retained integer every right side is nonnegative. At t=0,
exactly indices 0 and 1 have zero radicand; at t=8, exactly indices 0 and 8 do. At
an interior integer j, exactly indices j and j+1 do. The remaining seven radicands
are strictly positive. A zero coordinate has one choice, and each positive
radicand gives two distinct real roots of its independent coordinate equation.
Thus there are exactly 2^7=128 zeros in each slice. The slices are disjoint because
t differs, so the entire real zero set has exactly 9*128=1,152 points.

Finiteness already proves isolation. More explicitly, points in different slices
are at Euclidean distance at least one, and different points in one slice differ
in a coordinate by twice the square root of a positive integer. Every radius-1/2
ball about a zero therefore contains no other zero. There is no hidden real curve
or omitted unbounded real component. Possible positive-dimensional complex
components impose no extra hypothesis on the conjecture and do not invalidate
real isolation. A naive zero-dimensional complex Bezout bound is inapplicable.

With k=2 and l=10, the proposed value is 2^10=1,024, whereas this admissible example
has 1,152 isolated real zeros, a strict excess of 128. Hence the universal equality
is false. No upper bound identifying the exact maximum follows, and none is
claimed for the adjacent ID 2200006 / Problem 3. The result does not depend on the
acceptance label or broader conclusions of the adjacent [PR 825](https://github.com/AlecKriebel/Math/pull/825).

## 3. Independent exact computation

The audit checker has a separately written explicit coefficient list for the nine
quadratics. It does not import the author checker to establish its mathematical
result. It enumerates all 1,152 signed-radical coordinate tuples and evaluates all
nine equations using exact integer squared coordinates: **10,368 residual checks,
all zero**. There are 128 distinct tuples per slice and no cross-slice collisions.
The sign/radicand encoding is injective here: for fixed t each coordinate has a
fixed nonnegative radicand, and only a positive radicand receives either sign.
No floating-point approximation is used.

Both original scripts use explicit exceptions, not assert statements. AST checks
confirm no assertion-dependent validation. The independent checker also uses
explicit exceptions. Direct certificate replay under normal Python, -O, and -OO
matches the original deterministic result. Original package replay works locally
and after extraction/relocation. The original claimed seven negative mutations
under normal and -O modes reproduce, including forged count and wrong target with
an updated member hash. Further mutations and -OO checks are included.

## 4. Wrapper defects and actual repair

1. **Optimization was not propagated.** The original wrapper always starts its
   certificate child with `python -B`, even when the parent runs with -O or -OO.
   A correctly rehashed instrumented child confirms optimization level zero in
   those cases. Thus the author's wrapper-level optimized runs do not establish
   optimized child execution. Direct optimized child runs in this audit close
   the mathematical test gap. The derivative passes the exact parent mode onward.

2. **The internal manifest supplied its own allowlist.** A synthetic extra file,
   entered and rehashed in the manifest, passes the original verifier. The
   original unlisted-extra rejection remains genuine, but is not a fixed
   nine-file allowlist guarantee. The derivative fixes the nine expected names
   in the verifier and checks the manifest against that set. It rejects the
   rehashed added member. This still does not make a mutable manifest an external
   authenticity root; externally pinned archive bytes are required.

3. **Plain startup imports before inventory checking.** Harmless synthetic tests
   show that a sibling json.py, legacy json.pyc, or PYTHONPATH sitecustomize hook
   can execute a marker write before the original verifier reaches its checks.
   The sibling cases terminate with failure, while the ambient site hook can
   leave a successful replay. `-B` prevents new bytecode writes but does not
   disable reads of existing bytecode. The documented hardened invocation is
   `python3 -I -S -B verify_package.py`, optionally adding -O or -OO; the verifier
   checks this prerequisite and always uses the same isolation/no-site flags
   for its child. Under that invocation sibling code/bytecode is not imported,
   inventory additions fail, and the ambient startup hook is excluded.

The isolation guarantee begins with the invocation. Running any Python script
without -I/-S can execute startup code before the script can guard against it.
Neither version claims to protect against a compromised interpreter/standard
library, a replaced externally trusted archive pin, or concurrent hostile changes
after hashing. A trusted Python installation and stable extracted directory are
assumptions. Main scripts are run from source; no local certificate-module cache
is imported. Preseeded artifact __pycache__ content is rejected, and clean replay
creates no cache files.

`HARDENING.patch` contains the complete actual changes. Only README.md,
verify_package.py and MANIFEST.json differ in the derivative. The mathematics,
certificate executable, recorded result, source metadata, scope prose, research
log and historical status are byte-identical. Historical status still says that
acceptance was pending when originally frozen; the separate `ACCEPTANCE.json`
is the later, exact-artifact disposition. No original history has been rewritten.

## 5. Evidence and portability

`verify_audit.py` pins both input archives before extracting or executing them,
requires exactly nine regular ZIP members with the expected root and basenames,
checks every member hash, confirms the exact three-file derivative delta, performs
the independent arithmetic, and reproduces 86 replay/adversarial observations.
`CHECK_RESULTS.json` is the deterministic output. Of those observations, 22 are
successful expected replays, 58 are expected rejections (including two deliberate
original optimization probes), three document original pre-check execution, two
show hardened sibling rejection without execution, and one shows the hardened
ambient hook excluded. Do not describe all 86 observations as mutation rejections.
The nine ordinary negative mutations across three modes and two artifacts account
for 54 rejections; the author's original fourteen are a subset.

The entire audit suite was itself rerun with -O and produced byte-identical
results. Isolated relocated normal/-O/-OO certificate/package paths are covered.
All portable replay work is offline and uses only Python's standard library.
PDF and manuscript inspection is separately described in `SOURCE_AUDIT.json`;
portable replay does not claim to retrieve sources or recheck the entire corpus.

## 6. Boundaries and stopping condition

The original conjecture is resolved negatively by existing public work. Zero new
approaches were tried; executable repairs are verification work, not mathematical
research approaches. Exact extremal values, minimal dimension, the prior general
family, exhaustive historical priority, and unrelated later claims remain outside
this audit. No later proof-access restriction was bypassed. The prior PDF was not
freshly downloaded; its hash/size are only independently reconfirmed public release
metadata. The adjacent full investigation was not rerun.

Safe deliverables contain authored proof-verification prose/code, the actual
patch, and permitted public identity/retrieval metadata only. They contain no
third-party source document, source extract, dataset contents, private source,
private personal information, or coordination file. No queue change, remote write,
publication, or claim of human/formal review was made during this audit.
