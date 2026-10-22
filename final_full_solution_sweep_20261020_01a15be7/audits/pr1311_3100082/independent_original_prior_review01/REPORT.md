# PR1311 /3100082: independent original and prior review

**Complete negative answer to the stated universal temporal-unimodality
conjecture passes. Credit the existing Anonymous preprint, DOI
10.5281/zenodo.22849717; no new publication.** Its concept DOI is
10.5281/zenodo.22849716. This DOI was newly authenticated during this
review, rather than assumed from the initial scope record.

## Exact original and counterexample

Cooper–Spencer's [author manuscript](https://cs.nyu.edu/~spencer/papers/cooperjssubm.pdf)
has nine physical pages in reverse printed order. The complete Conjecture3
on printed8/physical2 concerns occupation at v at time n on the parity
class n↔v. Printed2/physical8 defines this parity by the coordinate sum
and defines the occupation kernel. Uniform averaging over the2d signed
coordinate directions fixes the simple symmetric nearest-neighbour walk.
The surrounding d=1 and d=2 examples confirm the convention. The
[author problem list](https://people.math.sc.edu/cooper/combprob.html)
agrees. Both key manuscript pages were read in text and visually inspected.
There is no first-passage, lazy-walk, or continuous-time substitution.

For d=26 and v=(17,0,…,0), the times65,67,69 are consecutive odd times
and are all at least the lattice distance17. They are reachable, not
merely parity compatible. The exact inequalities are

\[
 p_{65}(v)>p_{67}(v)<p_{69}(v).
\]

A rise-then-fall sequence cannot have a strict decrease followed by a
strict increase. This includes plateaus, an initial zero segment, and
monotone limiting cases. Thus one finite valley fully disproves the
universal conjecture. No dimension-minimality or complete mode count is
required for this conclusion.

## Independent exhaustive argument and certificate

At time n=m+2r an axis-endpoint walk has k_1 negative first-coordinate
steps, m+k_1 positive first-coordinate steps, and k_i positive and k_i
negative steps in each transverse coordinate. Necessarily Σk_i=r.
Conversely every such allocation and ordering is a valid walk. The
multinomial count for one allocation is

\[
 \frac{(m+2r)!}{(m+k_1)!k_1!\prod_{i=2}^d(k_i!)^2}.
\]

Summing all allocations is exact. In particular, with
A_m(z)=Σ_{j≥0}z^j/[j!(m+j)!], the answer is
\((m+2r)![z^r]A_m(z)A_0(z)^{d-1}\). No coefficient above r can contribute
to that coefficient, so truncation through26 is mathematically exact for
the three target times. The first independent implementation uses rational
polynomial convolution and verifies integrality after multiplication by n!.

A second implementation enumerates nonincreasing partitions of each
transverse allocation budget. If c_j transverse coordinates each use j
pairs, their coordinate-label multiplicity is
(d−1)!/[(d−1−Σc_j)!∏c_j!]. Multiplying by the time-order multinomial and
summing partitions reconstructs exactly the same allocation set, with
zero-remainder checks. The sum of the label multiplicities is checked
against the weak-composition count. This is an independent grouping and
implementation, not execution of the source's time-slot program.

Both methods give

```
W65=472771905154760476735080239062089851901956874836451641200273716209080628940936220800
W67=1278150092304717629532379079186301753285243215753138416912978330730296859707833144726912
W69=3456384842264444627112655114583494162563305352377408768216137840217183860729498596697993728
```

Each step has52 choices, so p_n=W_n/52^n. Exact subtraction yields

```
2704W65-W67=225139233754699559277887237589206257648173804626820892561797899057160948458396316288
W69-2704W67=266992672488156857102084463734221680007696980922488883444433922461152079517773356423680
```

Both integers are positive. This is a complete finite certificate using
only integer/rational arithmetic and a proved exhaustive count. The
normalizing factor is52²=2704, not52; comparing the increasing raw counts
would not prove the probability inequalities.

The new standard-library checker also propagates every signed-coordinate
neighbour directly in dimensions1–3, times0–9, axis endpoints0–11, giving
360 exact kernel comparisons and mass checks. Eleven controls per mode
cover parity, dimension, endpoint, normalization, the missing highest
coefficient, occupation/first passage, and boundary/positive foils. Normal,
-O,-OO outputs are byte-identical, with33 control passes. The parent's
existing walk receipt and historical checker claims were not used to
compute these results. No source-author code was executed.

## Primary prior identity and precise credit

The full eight-page Anonymous paper was read; the audited mathematical
scope is its finite Theorem1, Section2 and AppendixA. Its printed Python
program was read as source material and not run. Infinite-family,
continuous-time, Bessel, Poissonisation and priority claims are not
certified by this review and are not needed for the universal negative.

The tag v1.0.0-candidate resolves through annotated tag
b4fafd301da6a74b71bb9caefd0715bbbce0ce46 to commit
95678898ede180f04d6b416e605faa73aed58196. The public release is a
prerelease dated September19,2026. It identifies Anonymous as scholarly
creator and states unrefereed/AI-assisted status; maintainer metadata is
not substituted for authorship. The tag is unsigned; no digital signature
or unaffiliated peer-review claim is made.

The immutable commit PDF, tag PDF, Zenodo PDF and source-ZIP paper all
have SHA-256
`f2e4e599df9ba9d750950b2848d7faf9ad495eaacf12fe3b0550043e55922c33`.
Actual [Zenodo record22849717](https://zenodo.org/records/22849717) is
submitted/done, gives the exact title, Anonymous creator, date and version,
and identifies concept22849716. DataCite independently marks the version
DOI findable with matching identity. All three Zenodo payloads were
downloaded and match their metadata checksums. The40 ZIP files pass CRC;
all39 entries in its internal SHA256SUMS match. The PDF within the ZIP
matches the separate archived PDF. Source code, certificates and internal
editorial records are present, but no author software or historical
review execution is claimed reproduced.

The release page changed bytes since the historical PR capture; its current
body and source hashes are retained separately. The substantive finite
witness agrees. Direct DOI landing retrieval was unavailable/HTTP403, so
no successful landing-body inspection is claimed: authentication uses the
actual Zenodo API/payloads and DataCite DOI record. An initial parallel
retrieval encountered a403; current source downloads subsequently
succeeded, and their exact bytes are retained.

## Duplicate, scope and remaining limits

A fresh numeric-gid43-column read preceded mathematics:191 nonempty
response rows. Its broad Cooper lead is response index191, problem3100034,
the perfectly k-symmetric permutation problem, DOI10.1007/s00493-024-00127-x.
That is mathematically distinct. Exact target, title, release, version,
concept and DOI aliases have no matching record in this fresh snapshot.
This does not establish exhaustive historical priority.

The full pinned PR body and seven attempt files were read at head
985522a94e9fa9ef824f76c1abc5ef874cf2cfb2. Its complete QUEUE blob is
byte-pinned; the exact target diff, rather than unrelated rows, is reviewed.
The claimed_solved status is a claim examined here, not acceptance evidence.
All eight blob identities and the nested six-entry manifest pass.

One qualified existing-preprint row with B blank and the real version DOI
in C is proposed, including the exact PR1311 URL. No new publication,
service, Git, QUEUE, CASE or readiness action occurs. The strongest verified
result is the finite dimension26 disproof; no mathematical gap remains for
that universal negative. Other claims in the source, formalization,
minimality, exhaustive priority and external peer review remain outside
the verdict. Raw third-party/ledger/PR bodies are private. This AI-assisted
review preserves the earlier closed packets. Its complete closing seal
includes every own retained file and nested checksum/manifest artifact,
excluding only its exact own seal filename.
