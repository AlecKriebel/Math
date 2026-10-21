# Mechanism and historical priority audit — PR73 /2985 /KP-4.109

Exact head: `6f82e81631fd43abc0140a831acfb43c150f4210`. Audit date: 2026-10-04. Author metadata supplied by project: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. This report is a priority audit, not a new proof-search turn or a publication decision.

## Verdict

**Novelty remains unestablished.** The disconnected surface, its genus-three specialization, explicit affine arrangements, and local smoothing mechanism are prior. The candidate’s ambient manifold is a standard type-one bielliptic quotient. Non-Stein obstructions using homology above the middle dimension are also prior.

The full connected four-dimensional target follows from Giroux’s explicit construction after an additional free symmetry and covering argument. The implication is checked below at the exact hypotheses. It is short and uses standard topology; the bare existential disconnected-divisor theorem would not alone ensure the needed symmetry. No primary source read in this bounded audit explicitly states the combined connected four-dimensional conclusion. Logical availability as a corollary and documented historical priority are different claims; neither this search nor this report certifies novelty.

Strongest verified historical result: the numerical disconnected genus-three existence statement appears in the archived body of a thesis defended on1999-01-22. Contemporary public dissemination of that exact archived thesis body was not measured. Giroux’s explicit proof is securely publicly available by arXivv1 on2018-03-15; the journal carries nominal volume-year2017, whose actual release date was not established. Attribution also cites Auroux’s private February 2010 email, which is inaccessible evidence and was neither sought nor contacted.

## Exact target and boundaries

The claim audited is existence of a closed connected symplectic four-manifold X and a prescribed connected embedded symplectic surface Sigma with PD[Sigma]=k[omega], k a positive integer, such that X minus Sigma admits no Weinstein structure. The candidate achieves k=1 after choosing Omega=2 bar-omega on the quotient. It does not assume X simply connected.

This does not answer the existential choice of a good representative, Donaldson’s sufficiently large degree construction, an effective-degree bound, or the CP2 special case. A connected real-four-dimensional hypersurface in ambient T6 is not an ambient-four-dimensional example. A square-zero or negative-square surface cannot be a positive multiple of a symplectic class on a closed four-manifold, since its square would be k² times the positive symplectic volume.

## Prior construction and normalization

The [actual Auroux thesis](https://people.math.harvard.edu/~auroux/papers/these.pdf), printed p.7 / PDF p.11, contrasts connected genus 4k²+1 representatives with two-component representatives whose components have genus 2k²+1. Its form is 4pi omega0 and its class is PD(k omega/(2pi))=PD(2k omega0). At k=1 each component has genus three. This is an actual assertion in the public thesis; the explicit four affine equations are absent from that passage.

[Giroux, Proposition 9 and full proof](https://arxiv.org/pdf/1803.05929v1), v1 pp.8–10 / journal pp.376–377, supplies explicit arrangements and smoothing. The proposition is attributed to Auroux and references the thesis and private email. The construction’s general disjointness assertion for any a different from b is overbroad; the candidate uses specific offsets that repair it. The publisher version’s local cutoff smoothing formula was read and visually checked.

The [2020 Roux-divisor post and attributed Auroux comment](https://symplectosaurus.wordpress.com/2020/03/06/roux-divisors/#comment-1) give a connected ambient-six-dimensional example with nonzero H4. The author-name and timestamp are public platform attribution, not separately authenticated authorship. The comment explains that the explicit torus construction was intended for the thesis but cut from the final version. This is consistent with the thesis retaining its numerical existence statement. No dimension-four quotient is given in the post or comment read.

## Checkable full-target implication from the explicit prior mechanism

This section checks the candidate’s extension, using the supplied candidate equations; it makes no claim that Giroux wrote this extension.

On T4, let omega0=dx1 wedge dx2 + dx3 wedge dx4. The arrangements specialize to a=(0,0,1/4,1/4) and b=(1/2,1/4,0,3/4). Their pieces are

- A: x1=0, x2−x3=0; B: x2+x3=1/4, x4=1/4.
- A-prime: x1=1/2, x2+x3=0; B-prime: x2−x3=1/4, x4=3/4.

All cross-arrangement intersections are empty: A/A-prime have different x1; B/B-prime different x4; A/B-prime different x2−x3; B/A-prime different x2+x3. Each arrangement has two positive nodes. Smoothing two tori at two nodes gives Euler characteristic −4, hence genus three.

The map tau=(x1+1/2,x2,−x3,−x4) has order two on T4, has no fixed point, preserves omega0, and exchanges the two arrangements. Choose a smoothing S in a sufficiently small neighborhood of the first arrangement; its tau-image S-prime is the smoothing of the second arrangement in a disjoint neighborhood. This is an implementation of the prior local smoothing, not a new analytic existence requirement.

Write alpha=PD[S] and beta=PD[S-prime]. The candidate’s equations give alpha+beta=2[omega0], alpha²=beta²=4 and alpha beta=0. On the connected quotient p:T4→X=T4/tau, the map p restricted to S is an embedding onto the connected surface Sigma=p(S), and p inverse(Sigma)=S disjoint-union S-prime. Hence Sigma has genus three. The invariant form descends to bar-omega. For Omega=2 bar-omega,

p*(PD[Sigma])=alpha+beta=2[omega0]=p*[Omega].

Pullback by a finite cover is injective in real cohomology (transfer followed by pullback multiplies by degree), so PD[Sigma]=[Omega] over R. Thus [Omega] is integral in the required sense, being the real image of the integral divisor class. This avoids assuming that omega0 itself descends integrally. Sigma²=4. The rescaling changes degree bookkeeping but preserves the symplectic property.

Let N=X minus Sigma and N-tilde=T4 minus (S disjoint-union S-prime). General position for paths makes both complements connected, and restriction of p is a connected double cover. Thom excision in the pair (T4,N-tilde) gives H4(T4,N-tilde;Z)=Z². The fundamental class map H4(T4;Z)=Z→Z² is the oriented diagonal. Exactness injects its cokernel Z into H3(N-tilde;Z). A Weinstein four-manifold has the homotopy type of a CW complex of dimension at most two; every cover of such a complex does too. Consequently this nonzero H3 forbids every Weinstein structure on N, independently of its symplectic form. The same CW obstruction excludes Stein structures.

The new H3 class changes sign under the deck involution, because its relative precursor is the difference of the two component classes. Thus the covering calculation can also be expressed as nonzero degree-three rational homology with the sign local system on N. Ordinary homology of the base need not detect this particular class; a base-only homology argument would lose the decisive evidence.

This extension meets the full stated target without an unsupported equivalent conjecture. It still leaves historical priority of the extension unresolved.

## Other approach families checked

| Family | Verified evidence | Exact gap or exclusion |
|---|---|---|
| Bielliptic / hyperelliptic / flat quotient | [Serrano’s institutional 1989 preprint](https://hdl.handle.net/2445/151641), §1, and [Nuer v1](https://arxiv.org/pdf/2107.13370v1), §2.1, describe translation on one elliptic factor and inversion on the other for type one. In coordinates z1=x1+i x2, z2=x3+i x4, the candidate is (z1+1/2,−z2). It also inherits a flat metric. | Standard ambient model; the read passages provide no disconnected-lift symplectic divisor or non-Weinstein complement. Algebraic ample-divisor constructions cannot automatically be substituted for an arbitrary symplectic divisor. |
| Genus-three surfaces / surface fibrations | [Smith 2001](https://msp.org/pjm/2001/198-1/pjm-v198-n1-p10-p.pdf) constructs nonisotopic symplectic representatives; Theorem 1.1 explicitly excludes g=3 and Proposition 1.2 uses multiples of a square-zero factor surface. | Positive symplectic class condition and complement obstruction not supplied. Altering the class transfers the main difficulty and does not prove this target. |
| Canonical representatives | [Vidussi 2007](https://ems.press/content/serial-article-files/31609) gives simply connected four-manifolds with connected and disconnected representatives of the canonical class. | Read construction does not establish canonical class proportional to the ambient symplectic form together with a non-Weinstein connected complement. Simply connected ambient manifolds have no nontrivial connected ambient covers. |
| Toric complement obstructions | [Acu et al. v1](https://arxiv.org/pdf/2012.08666v1), full §6 pp.41–46, proves nonexactness and absence of compatible convex neighborhoods in examples. | Smooth examples have square zero or negative. The positive CP1×CP1 example retains two crossing components. Nonexactness of the restricted form is incompatible with a smooth divisor PD positive symplectic class. No obstruction to every alternative Weinstein form is proved for the target. |
| Convex non-Stein manifolds | [Macarini 2003](https://arxiv.org/pdf/math/0304273v1), pp.1–2, explicitly records H(4n−1)=Z for completions of disconnected-boundary examples. | Earlier homological obstruction, but read passages do not supply a free component-exchanging symmetry plus a closed positive-class divisor cap. These additions cannot be assumed from a two-boundary convex example. |
| Donaldson / approximately holomorphic representatives | Auroux 1997/2002 and the 2013 MathOverflow discussion concern constructed representatives. | Existential good representatives do not imply that every prescribed connected representative has Weinstein complement. |
| Recent embedded Weinstein-domain obstructions | Mark–Tosun v1 (2025), introduction and theorem passages, concerns embedded domains and Brieskorn boundaries in positive/rational ambient manifolds. | No matching divisor boundary or closed bielliptic ambient hypothesis was established; not a verified full-target implication. |

Routes marked excluded or with a gap are not reopened by renaming a divisor, changing units, or invoking a broad theorem without its hypotheses.

## Search coverage, independence and residual uncertainty

The public WEB_LEDGER records 22 web calls, queries, UTC boundaries and hashes of exact private returned JSON. Search strings include quotient, finite cover, disconnected lift, local coefficients, hyperelliptic/bielliptic, genus three, arbitrary divisors, Stein/Weinstein complements, and source/citation follow-ups. Exact-problem-ID searches were not used in this family. Search results were leads; decisive claims above use retrieved primary full text and specified pages.

FIRST was sealed at 2026-10-04T18:22:00.335067Z, 3246 bytes, SHA256 4905094448f7ca75f26b4c8b40e734d197929f29bbf05774f280ffcc71b975ab. Only the supplied candidate and target were project math inputs before sealing. After sealing, further independent primary sources were read. At 2026-10-04T18:33:26Z, after ROOT authorized post-seal comparison, the authenticated original SOURCE_AUDIT.md dated2026-09-30 was read in full. It agrees that priority is unresolved and credits the prior construction; its opinion is not primary-source evidence. No original readiness file, source wrapper, checker or proof-review opinion was read. ROOT also supplied typed native metadata: separate prior-report field present as JSON null, raw separate lookup absent, SQL normalized to an empty object. These distinct metadata states do not establish historical novelty. The independent FIRST remains unchanged.

Residual works: Auroux’s cited private email; Geiges 1994/1995 full texts (1995 publisher PDF HTTP403; author publication list checked); McDuff 1991 full proof; older classification books and original early-twentieth-century classifications; source families not exhaustively indexed. No negative inference is drawn from these gaps. Outside input could resolve private-source attribution, but the project forbids external communication; no contact or request was initiated or prepared.

## Reproducibility and limits

Copyright-bearing PDFs, HTML, extracted text, rendered pixels, raw web results and source-bearing process streams are private outside Git. Public files contain original analysis, bibliographic locators and byte/hash metadata. PUBLIC_MANIFEST and PRIVATE_MANIFEST inventory the evidence at the final snapshot, with explicit self/closure exclusions.

Every runner-managed subprocess has recorded exact child argv, cwd, PID, UTC launch/exit, executable and runner pins, exit code and complete raw stdout/stderr hashes. Declared input pins are recorded prelaunch. Some early/ad hoc reads did not declare every input pin; the final source manifest is retrospective evidence for those files, not a claim of prelaunch hashing. Remote downloads necessarily have URL/executable pins before bytes exist. The initial setup/instruction-read launcher and the host exec/web/view-image internals do not expose complete process instrumentation; this limitation is disclosed, not fabricated. A brief public-log read after compaction was also outside the runner.

The initial public process ledger temporarily held large raw web arguments. Before any commit or push, its exact original bytes were moved to the private cache and the public arguments replaced by hashes. The complete exact ledger is reconstructed privately for readback. No source payload was committed or pushed. Tool presentation sometimes truncated large outputs; full raw streams are retained, and decisive passages were reread in bounded outputs. Parser warnings from publisher PDFs were preserved and important pages checked visually.

The finite audit is complete; the research goal of establishing novelty is not achieved. No merge, publication, upload, release, branch, Git-index or shared tracker mutation was performed.
