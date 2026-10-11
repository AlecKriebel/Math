# Covering-homology adversarial audit: PR73 / record 2985 / KP-4.109

Verdict: **no mathematical defect found in the authenticated candidate**. Its connected double cover has nonzero ordinary third homology, obstructing every Weinstein structure and every two-dimensional CW homotopy model of the quotient complement. More precisely,

$$
H_3\!\left(T^4\setminus(S\sqcup S');\mathbb Z\right)\cong\mathbb Z,
\qquad H_3(X\setminus\Sigma;\mathbb Z)=0.
$$

The downstairs equality is an adversarial check, not a defect. The involution reverses the upstairs generator. Novelty and priority remain unverified.

The supplied PR head is 6f82e81631fd43abc0140a831acfb43c150f4210. The restricted candidate is byte-identical to the original candidate in ROOT's custody directory, authenticated after FIRST by offline computation of Git blob SHA1 a26d0c232cdd02aecb177e6d90086d023432130e. No Git command or ref mutation occurred. Candidate SHA256 is 78ab061c9c0c6c16f2e6b249e764001361933782d7381982c733f92cefda3c8f.

FIRST was sealed at 2026-10-04T17:50:52.064410+00:00, SHA256 6e1f4e21c4ea629e0a616217b8b8b248b4bf8d4129e632a49cacd4cfbe809046. It precedes every mathematical computation and original-candidate custody read, and remains unchanged. This v2 corrects formatting in the sealed v1 report/derivation, preserved as disclosed historical snapshots. No proof or verdict changed.

## Target compatibility and conventions

I downloaded, extracted and visually read complete printed p.281, including the question and both remarks, in the genuine [K3 author PDF](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf). The question concerns a prescribed symplectic surface in class $PD(k[\omega])$, permits $k=1$, and has no condition excluding this quotient four-manifold. The surface is connected under the strict convention. The example does not show that every surface in this class has bad complement, give effective degree bounds, or settle the $\mathbb{CP}^2$ case. The candidate already distinguishes those scopes correctly.

The equality of form and surface classes is established in real cohomology. The form $\Omega=2\bar\omega$ is a positive rescaling, with integral lift $PD[\Sigma]$. Transfer gives injectivity of pullback over the reals; the proof does not assert integral injectivity in degree two or ignore torsion. Symplectic area forces positive $k$ for any nonempty surface meeting the condition:

$$
\int_\Sigma\Omega=k\int_X\Omega^2>0.
$$

After the first seal and original final seal, ROOT pointed to K3 printed p.263. I read that complete page in text and pixels. Section 4.9 defines a Weinstein domain on a compact smooth four-manifold with boundary, an exact form, a Liouville field gradient-like for a Morse function having boundary as a regular level, and a compatible almost complex structure. This differs from the complete open-manifold convention in [Cieliebak-Eliashberg, Flexible Weinstein manifolds, pp.1-4](https://library.slmath.org/books/Book62/files/eliashberg.pdf), which uses a complete Liouville field and an exhausting generalized Morse function, perturbable to Morse.

The obstruction applies to both conventions. A compact Weinstein domain has handles of index at most two; its interior and completion have the same homotopy type. Its finite cover is a compact Weinstein domain of the same dimension. A proper Morse exhaustion of an open Weinstein manifold yields a possibly infinite CW model with the same dimension bound, and a finite cover preserves the exhaustion. The restricted form has finite volume, but no volume/completeness objection is used. A mere local gradient-like field without a proper exhaustion or compact Weinstein domain is not the convention being asserted.

## Distinct mechanism and adversarial tests

The independent derivation uses Poincare-Lefschetz duality and pair cohomology. For an oriented compact exterior $M$ and the two normal disk bundles $V$, one has

$$
H_3(M;\mathbb Z)\cong H^1(M,\partial M;\mathbb Z)
\cong H^1(T^4,V;\mathbb Z).
$$

The degree-zero pair map is the diagonal $\mathbb Z\to\mathbb Z^2$. Its cokernel injects into relative degree-one cohomology, producing the ordinary upstairs third-homology class. This is materially distinct from repeating the candidate's homology LES/Thom segment. The detailed v2 derivation also proves the exact upstairs group, the downstairs vanishing, and finite-cover lifting.

| Possible failure | Checked result |
| --- | --- |
| Ordinary versus compact-supported or locally finite homology | The obstruction uses ordinary singular $H_3$. Compact support appears on the cohomology side of duality, not as a substitute homology theory. |
| Fundamental-class coefficients depend on self-intersection | Each oriented local restriction has coefficient one. The diagonal is primitive. The normal Euler class does not enter this degree-four map. |
| Integral subgroup might be torsion or fail to split | The quotient by the primitive diagonal is $\mathbb Z$. The next group is a subgroup of free $H^1(T^4;\mathbb Z)$, so the extension splits. Here the next kernel vanishes. |
| Twisted normal bundles invalidate excision or retraction | Ambient and surface orientations orient the normal bundle. Radial expansion in each punctured disk works without a trivialization of the disk bundle. |
| Complement or covering disconnected | Paths perturb off the closed codimension-two submanifold because $1+2<4$. Both cover and quotient complements are connected. |
| Downstairs third homology vanishes | It does vanish integrally. The cover obstruction deliberately does not need a downstairs class; the deck action upstairs is $-1$. |
| Infinite-type Weinstein manifold evades finite handle arguments | Proper sublevels give a locally finite, possibly infinite handle decomposition with every index at most two. Ordinary $H_3$ still vanishes. |
| Finite cover loses exhaustion or flow hypotheses | Finite covers are proper, preserve compact sublevels and critical indices, pull back gradient inequalities, and lift complete flows when completeness is required. |
| Connectedness of the quotient surface is hidden | The two-node smoothing joins the tori. Disjointness of $S$ and $\tau S$ makes $p|_S$ a diffeomorphism onto the connected embedded surface. |
| Signs, normalization, or products are wrong | Independent exact exterior algebra verifies positive torus restrictions, normal determinant $2$, intersection parameters $1/8,5/8$, $\tau^*\alpha=\beta$, $\alpha+\beta=2\omega_0$, both squares $4\,dx_{1234}$, and zero mixed product. |
| Local smoothing is unsupported | On the complex central annulus, $\beta=\operatorname{Re}(dz\wedge dw)$ vanishes. On fixed outer transition annuli, the cutoff graphs converge in $C^1$ to positive axes. For small parameter the annuli are disjoint and glue on collars, establishing an embedded, compactly supported symplectic smoothing. |

All six candidate sections were read. The affine involution is free, preserves the form and squares to the identity. Its explicit offsets separate every required nodal-union pair. The displayed torus orientations agree with the Poincare duals. Local smoothing preserves homology, positivity and separation from its image. Euler characteristic is $-4$. The quotient surface has genus three, $\Omega$-area four and self-intersection four.

I read the genuine [Giroux paper's Proposition 9 and complete proof](https://arxiv.org/pdf/1803.05929), downloaded pp.8-10, plus pp.1-3 and 7 for context and definitions. This verifies the attributed two-class torus construction and local smoothing. The candidate proves its own explicit disjointness rather than relying on an unrestricted parameter assertion in that source. No novelty inference follows.

No essential mathematical repair was found. Optional clarification: mention downstairs $H_3=0$ and finite-cover properness. The restricted candidate has literal quad/qquad strings lacking TeX backslashes; these are harmless formatting defects to repair before typesetting. No candidate, manuscript or PR file was changed here.

## Source scope and evidence integrity

Before FIRST: only the authentic restricted candidate/target, applicable instructions and PDF skill, complete K3 p.281, Eliashberg's full relevant pp.1-4 definitions, and complete relevant Hatcher pp.251-252 and 262-264 were read. The latter include compact-support definitions and Theorems 3.43-3.44 with their proofs and naturality diagram. After FIRST: the listed Giroux and Cieliebak-Eliashberg pages, and original candidate bytes for custody. After the original final seal: K3 p.263 and ROOT's formatting feedback. SOURCE_READ_SCOPE.json, EXPOSURES.json and the later addenda distinguish those exposures.

Original source_record, TARGET_PROBLEM_ONLY, SOURCES, reviews/checkers and sibling mathematical opinions were not read. No original checker was replayed. ROOT's post-seal messages supplied custody metadata, a source-convention pointer and editorial feedback; these did not alter the mathematical verdict.

Private PDFs, copyrighted extracted text/pixels and text-bearing stdout are outside Git in /tmp/pr73_covering_homology_adversary_20261004_private. Public audit artifacts retain hashes, own proofs/code, process receipts and non-copyright output. An initial MSRI fetch timed out; the authentic SLMath-hosted PDF subsequently succeeded. Web screenshot calls supplied references without image bytes through the bridge; all claimed visual reads used local Poppler renders and view_image.

Process receipts retain actual cwd, PID, UTC bounds, exit and full stdout/stderr. Poppler calls retain actual argv. Python processes 0001-0008 recorded script arguments but omitted interpreter-level executable/orig_argv; that unmeasured information is not fabricated. Later processes include it. The underlying tool launcher before exec replacement is unobserved. Manifests/readback declare their current-process exclusions.

Sealed v1 Markdown is preserved for custody and contains disclosed formatting defects. V2 report and derivation are authoritative readable versions. A global scan checks control characters in every Markdown/JSON artifact; only explicitly identified immutable historical files may retain such defects.

No Git/index/ref/commit/push, PR, native ledger, manuscript, release, Zenodo/DOI or tracker mutation occurred. No external individual was contacted. Remaining gaps are historical novelty/priority, untested original checker behavior, and head provenance supplied by ROOT. No remaining mathematical gap is identified in this assigned family. Completion estimate: 100% of the assigned adversarial audit; cross-family promotion belongs to ROOT.
