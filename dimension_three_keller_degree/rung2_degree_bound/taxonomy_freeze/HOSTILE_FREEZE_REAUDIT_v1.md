# Corrected hostile re-audit of the version-one quartic freeze

**Re-audit date:** 2026-07-25 (America/Los_Angeles).

**Files inspected:** `FROZEN_TAXONOMY_v1.md`,
`frozen_manifest_v1.json`, `verify_frozen_manifest_v1.py`,
`FREEZE_PROTOCOL.md`, `HOSTILE_FREEZE_AUDIT_v1.md`,
`RECONCILIATION.md`, and `blind_independent/BLIND_TAXONOMY.md`.
No exclusion proof was inspected.

## 1. Verdict

\[
\boxed{\textbf{PASS — CONTENT APPROVED FOR THE FINAL MECHANICAL FREEZE STEPS.}}
\]

Every release blocker in `HOSTILE_FREEZE_AUDIT_v1.md` has been corrected.
The deliberately pending manifest status and absent checksum file are not
defects at this stage. They are the next fail-closed mechanical steps
triggered by this content pass.

No mathematical correction, new leaf, or denominator change is required.

## 2. Blocker-by-blocker result

| Prior blocker | Corrected result | Re-audit |
|---|---|---|
| Compressed \(L^{-1}\) normalization | Section 1 now constructs \(L=J\Phi(x_0)\), postcomposes by \(L^{-1}\), and obtains determinant \(1\) | **PASS** |
| Rank-one assertion lacked cone proof | Section 2 proves that the equal-weight one-dimensional image cone projectivizes to one point | **PASS** |
| Rationality of the relative closure was asserted | Section 2 proves domination by \(\mathbb P^2\), restriction to a general line, unirationality, then rationality over \(\mathbb C\) | **PASS** |
| Projective factorization was not upgraded to a polynomial equality | Section 2 proves primitivity of \(A(p,q)\) and invokes UFD primitivity to obtain \(G=A(p,q)\) | **PASS** |
| Least-degree uniqueness needed the canonical field | Section 2 uses the relative algebraic closure and proves every other presentation degree is \((\deg R)a\) | **PASS** |
| “Atlas” overstated the pivot geometry | Section 5 calls the pieces a disjoint locally closed coefficient-pivot partition and explicitly says they are not a Zariski-open atlas | **PASS** |
| Routing rule 5 was not a specialization case | Section 6 now has three ordered mathematical routing rules and separates the fail-closed proof-coverage condition | **PASS** |
| Checksums were optional | The verifier now fails when the checksum file is absent or empty and requires an exact filename set | **PASS, static** |
| Stable IDs were not checked against tuples | The verifier parses every `Q2-E-A-B-D-N` ID and compares it to the attached tuple | **PASS** |
| Monomial strings were checked only for cardinality | The verifier compares against the exact ordered list of fifteen quartic monomials | **PASS** |
| Verifier success message claimed semantic mathematics | It now reports only schema, synchronization, arithmetic, and checksum success | **PASS** |
| Markdown/manifest relation was not checked | The verifier parses the Markdown table and compares rank, tuple, and status with the manifest | **PASS** |
| Moduli might be mistaken for finite orbit types | Taxonomy, manifest, and protocol all state that leaves are inclusive and retain continuous moduli | **PASS** |

## 3. Mathematical replay

### 3.1 Normalization

For a Keller map \(\Phi\), \(L=J\Phi(x_0)\) is invertible because the
Jacobian determinant is a nonzero constant. Source translation, target
translation, and postcomposition by \(L^{-1}\) preserve exact degree four and
give
\[
                         F=X+H_2+H_3+H_4,\qquad H_4\ne0.
\]
Since \(\det L=\det J\Phi\), the normalized determinant is \(1\).
No singular-linear-part counterexample is possible.

### 3.2 Rank one

Equation \(\det JH_4=0\) gives rank at most two. Rank zero would make the
positive-degree triple zero. In rank one, the image closure is an irreducible
one-dimensional cone with the standard equal-weight target scaling
\[
                         H_4(\lambda x)=\lambda^4H_4(x).
\]
Its projectivization is one point, so the cone is a line and
\[
                         H_4=a h.
\]
Thus `Q1` is complete and disjoint from rank two.

### 3.3 Relative closure and polynomial factorization

For rank two, exact gcd extraction gives a primitive triple \(G\). Its
projective ratio field \(K_G\) has transcendence degree one. The relative
algebraic closure \(E_G\) of \(K_G\) in
\(\mathbb C(\mathbb P^2)\) is finite over \(K_G\). Its curve is dominated by
\(\mathbb P^2\); a general source line maps nontrivially to it. Hence it is a
unirational curve over \(\mathbb C\), therefore rational:
\[
                         E_G=\mathbb C(p/q).
\]

The inclusion \(K_G\subset E_G\) produces a finite map from the smooth
projective curve with function field \(E_G\) to the normalization of the
projective image curve. If the image degree is \(\delta\) and the field
degree is \(\nu=[E_G:K_G]\), pullback of a line has degree
\[
                         b=\delta\nu.
\]
It is represented by a basepoint-free binary triple \(A\).

The equality \([G]=[A(p,q)]\) is genuinely polynomial. If a source prime
divided every component of \(A(p,q)\), it would divide both \(p,q\) or give a
base point of \(A\). Neither is possible. Both triples are primitive over
\(\mathbb C[x,y,z]\), so their rational proportionality factor is a unit.
After a scalar is absorbed into \(A\),
\[
                         G=A(p,q),\qquad e+ab=4.
\]

This defeats the two main attempted counterexamples:

* a nonrational relative-closure curve cannot be dominated by a general
  source line; and
* a nonconstant rational scalar between \(G\) and \(A(p,q)\) would introduce
  a common prime factor into one primitive triple.

### 3.4 Canonicity and least degree

The relative algebraic closure is unique. Its rational generators differ by
\(\mathrm{PGL}_2\), so the primitive pencil and its degree \(a\) are unique.
For any other polynomial presentation \(u=r/s\),
\[
                         K_G\subset\mathbb C(u)\subset E_G,
\]
and \(u=R(p/q)\). Primitivity gives
\[
                         \deg r=\deg s=(\deg R)a.
\]
Thus the canonical pencil is least-degree, with equality only for a Möbius
change. The tuple
\[
             (\operatorname{rank}JH_4,e,a,b,\delta,\nu)
\]
is single-valued and invariant.

### 3.5 Completeness and disjointness

Solving \(e+ab=4\) for rank two and then \(b=\delta\nu\) produces exactly the
thirteen tuples in the table and manifest. Rank one contributes `Q1`;
rank zero is \(H_4=0\), outside exact degree four.

The corrected artifacts therefore prove:

\[
\boxed{14\text{ exhaustive, disjoint, canonical inclusive leading leaves}.}
\]

Here “canonical” refers to the leading invariant assignment. It does not mean
that a leaf is a single source/target orbit.

## 4. Pivot-partition replay

The manifest and Markdown use the same exact order of the fifteen ternary
quartic monomials and the three target components, giving 45 coefficients
\(c_0,\ldots,c_{44}\).

Every nonzero coefficient vector has a unique first nonzero coordinate.
Consequently the sets
\[
 \{c_0=\cdots=c_{i-1}=0,\ c_i\ne0\},\qquad 0\le i\le44,
\]
are disjoint and cover \(H_4\ne0\). Intersecting with each of the fourteen
leaves preserves coverage and disjointness. Thus:

* there are 45 fixed pivot strata per row;
* there are 630 row/pivot intersections when empty intersections are counted;
* no continuous modulus is discarded;
* an equivalence orbit may meet several pivot strata; and
* the strata are not asserted to be Zariski-open coordinate charts.

The pivot device is therefore a valid fixed fail-closed coverage partition,
not a finite moduli taxonomy.

## 5. Manifest and Markdown synchronization

A content dry run, omitting only the intentionally pending status/checksum
gates, verified:

* 14 rows with 14 unique IDs;
* `Q1` has rank one and null tuple;
* every other row has rank two;
* every stable rank-two ID exactly encodes its attached tuple;
* the actual tuples equal the complete expected set of thirteen;
* the exact monomial order agrees with the Markdown;
* pivot IDs are exactly `C00` through `C44`;
* the coverage kind is a disjoint locally closed coefficient-pivot partition;
* the total intersection count is 630; and
* the Markdown table and manifest agree exactly on row rank, tuple, and
  status.

The 7 `open`/7 `excluded-audited` strings also agree. Their mathematical
exclusion content was not inspected and is not certified by this re-audit.

## 6. Static verification of mandatory checksum logic

The corrected verifier is genuinely fail-closed once the final mechanical
phase begins. It:

1. requires manifest status `frozen`;
2. requires `FROZEN_SHA256_v1.txt` to exist and be nonempty;
3. requires well-formed lowercase SHA-256 digests;
4. rejects duplicate entries;
5. rejects absolute paths, `..`, and paths escaping the freeze directory;
6. requires the checksum filename set to equal the explicit expected set;
7. hashes every required file and rejects any mismatch; and
8. reports only manifest schema, Markdown synchronization, finite arithmetic,
   and required checksums.

The expected set includes the taxonomy, manifest, verifier, protocol, blind
derivation, reconciliation, first hostile audit, and this corrected re-audit.
This is consistent with `FREEZE_PROTOCOL.md`.

The current `pending_corrected_reaudit` status and absent checksum file would
correctly make the verifier fail **now**. Per the re-audit instructions, that
is expected sequencing rather than a defect.

## 7. Protocol consistency

`FREEZE_PROTOCOL.md` now distinguishes:

1. canonical leading rows;
2. inclusive frozen leaves, one per leading row; and
3. locally closed coefficient pivot strata.

It explicitly rejects the historical 68-bucket proposal, disclaims finite
orbit classification, requires independent derivation and reconciliation,
and makes any unassigned leading case a freeze violation. These rules agree
with the taxonomy, manifest, verifier, and both hostile audits.

## 8. Mechanical steps authorized by this content pass

The following are pending actions, not remaining content corrections:

1. synchronize the taxonomy/protocol status headers with the completed
   content replay and set the manifest status to `frozen`;
2. generate `FROZEN_SHA256_v1.txt` with exactly the filenames required by the
   verifier, after this re-audit is final;
3. run `verify_frozen_manifest_v1.py`;
4. record the successful result in `FREEZE_CERTIFICATE_v1.md`; and
5. only then reopen quartic exclusion work.

The checksum must be generated after all hashed files, including this
re-audit and the verifier, are final.

## 9. Precisely what is certified

This PASS certifies the **content** of the following claim:

> Every normalized exact-degree-four Keller map over \(\mathbb C\) has a
> nonzero leading quartic \(H_4\) in exactly one of fourteen inclusive leaves,
> determined by rank one or by the canonical relative-closure tuple
> \((e,a,b,\delta,\nu)\). Every such map also lies in exactly one of 45 fixed
> locally closed coefficient pivot strata within its leaf.

It also certifies the denominator arithmetic and Markdown/manifest
synchronization described above.

It does **not** certify:

* any of the seven exclusion claims or audits;
* existence of a non-linear Keller map in any leaf;
* a finite source/target orbit classification;
* a finite classification of continuous moduli, singularities,
  ramification, contacts, base schemes, or stabilizers;
* that the pivot strata are Zariski-open charts;
* coverage of a future proof's preferred normal forms without its explicit
  map back to the pivot partition or a division-free argument;
* a Jacobian-conjecture conclusion; or
* novelty or peer review.

No further content correction is required before the final mechanical freeze
steps.
