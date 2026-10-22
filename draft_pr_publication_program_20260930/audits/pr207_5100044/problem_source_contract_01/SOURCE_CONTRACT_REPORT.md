# PR207 / 5100044 exact problem and dependency contract

Audit completed independently of other PR207 proof reviewers. The initial statement assessment is preserved unchanged with its seal; this report supersedes interpretive phrasing in that initial note. This is a source-contract review, not acceptance of the proof or a priority/current-openness review.

## Finding that needs an explicit qualification

**The original source does not explicitly impose least/primitive period, distinct vertices, or simple/convex orbits.** The candidate does explicitly assume least period N divisible by 4. The original row itself says only N congruent 0 modulo 4. Consequently the source alone does not justify presenting a least-period restriction as an explicitly stated original hypothesis. This is a contract ambiguity, not a demonstrated falsehood of the candidate's expressly restricted theorem.

The entire 17-page PDF was searched, and every TeX file in the independently downloaded v11 source archive was checked. No orbit-admissibility clause uses simple, convex, primitive, minimal/least period, repetition, winding/turning, coprime, or gcd. The sole TeX occurrence of simple is a package comment about URL typesetting. Least occurs only in the least-squares numerical method. Evidence: WORDING_SEARCH.json and SOURCE_TEX_WORDING_SEARCH.json.

The relevant actual statements are on printed pp. 1-3, 4, 9-11 and 13. Section 4, p. 13 / 100_method.tex lines 3-7, initializes N evenly spaced vertices and tests whether incident-side bisectors align with local normals. It supplies no minimal-closure or distinctness test. The p. 3 statement about a distinct caustic for each N and the initialization suggest an experimental choice, but neither formally excludes shorter repeated cycles or defines the admissible winding class. My initial note's simple-period characterization was inference only. There is no explicit simple-orbit restriction to prove that stars are an extension, either.

Recommended exact framing: state that the candidate treats the primitive-period interpretation of the original parity conjecture, for nondegenerate confocal elliptical caustics, and proves its own explicitly stated theorem for every admissible coprime winding. Do not assert that the source explicitly defines N this way. If a campaign contract instead demands every displayed length N, independently resolve repetitions; this audit has not supplied that resolution.

## Object and regular conic scope: matched

The target is arXiv:2004.12497v11 Table 9, printed p. 11: k804,a, A A_j^dagger, N congruent 0 modulo 4, unknown value and proof. Section 2, p. 3, defines all polygon areas by signed consecutive cross products. Section 3.9, pp. 9-10, specifies unit-radius circle inversion of the original orbit vertices about original focus f_j, then the polygon having those inverted vertices. This supports the candidate's straight consecutive chords and signed shoelace area; it does not mean inversion of complete edges, the outer polygon, an ellipse inversion, or a different focus.

The introduction, p. 1, expressly identifies two confocal ellipses and the outer member of the pair. Section 2, p. 2, supplies a>b>0 and the caustic's major/minor semiaxes. Strict inequalities for the caustic are not separately displayed. Nevertheless, for ordinary nondegenerate ellipses and a genuine inscribed/tangent billiard, calling one outer and the other caustic makes strict nesting the regular geometric reading: confocality gives a^2-alpha^2=b^2-beta^2>0. A hyperbola or line segment is not that elliptical caustic. The candidate does not silently remove a hyperbolic case from this stated conic pair. Its circle aside is additional; the original a>b condition also excludes a circle.

## Edition labels and low-period credits: matched

- Published Fifty New Invariants, Table 9, printed p. 350: k804 is the inverse-polygon angle cosine sum; the area-product row is absent.
- Garcia-Reznik, DOI 10.33039/ami.2022.02.001, publisher-hosted accepted manuscript: Table 1, printed p. 7, labels the area product k805,a and lists 4,4i,8 as derived, with '?' in the proofs column. Its caption says bare N denotes simple orbits. Proposition 4.9, printed p. 10, gives k805,a=4 for simple N=4.
- The same later paper, Section 3, printed p. 3, explicitly treats self-intersected 4-periodics with a hyperbolic caustic. Proposition 3.4, p. 4, and Observation 4.11, p. 10, give zero orbit area/product. Thus its 4i is not an elliptical primitive star case missing from the original conic-pair theorem. These facts do not settle any general-N proof status today.

All locators above were confirmed visually. The browser's text extraction reports the later Table 1 and Proposition 4.9 one page early; the rendered printed page numerals are 7 and 10, as the submitted SOURCES says.

## Stachel canonical dependency: matched, with one adjacent source typo

Fresh published PDF, DOI 10.1007/s40879-021-00524-2, Theorem 4.3 and equation (4.9), printed p. 1614 (PDF page 13), says the caustic eccentricity is the Jacobi modulus, parametrizes the outer ellipse by (-a_e sn u,b_e cn u), gives the vertex increment 2 Delta u, and in part (2) explicitly requires gcd(N,tau)=1, with Delta u=2 tau K/N. Equation (4.9) gives a_e=a_c dn(Delta u)/cn(Delta u), b_e=b_c/cn(Delta u). The candidate's rename a_c=alpha, b_c=beta, d=c, Delta u=v and k=c/alpha is exact. Its k'=beta/alpha follows from confocality. Stachel's modulus named m is not the squared numerical-library parameter.

For a strictly nested pair, beta/b lies in (0,1), so v is the unique solution in (0,K) to cn v=beta/b. Then delta=2v in (0,2K). The real parameter circle has length 4K; least period N is equivalent to delta=4K tau/N with gcd(N,tau)=1 and 0<tau<N/2. These are consequences of canonical coordinates and least closure, rather than additional restrictions excluding an elliptical star. Reversal changes the increment's sign. This is enough to support the dependency's claimed coverage; no proof of area constancy is imported from Stachel.

Caution: the surrounding published p. 1613 prints dn(u+2jK)=(-1)^j dn(u), which is erroneous (take u=0,j=1). The correct relation is dn(u+2K)=dn(u), as in DLMF Table 22.4.3. The candidate uses the correct relation, and its specific Theorem 4.3/(4.9) citation is unaffected. Do not copy the adjacent typo into a future source note.

## DLMF dependency: matched

Exact supporting locations:

- 22.2: meromorphic/simple-zero/simple-pole and realness paragraph; parity paragraph after (22.2.10): sn odd, cn and dn even.
- Tables 22.4.1 and 22.4.2: sn/cn/dn common simple poles at iK' modulo 2K,2iK'; dn zeros at K+iK' modulo that lattice; dn full periods 2K,4iK'.
- Table 22.4.3: sn(z+2K)=-sn z, cn(z+2K)=-cn z, dn(z+2K)=dn z; sn(z+2iK')=sn z, dn(z+2iK')=-dn z; sn(z+K+iK')=dn z/(k cn z).
- The reflection used in the candidate is a deduction: with r=K+iK', sn(2r-u)=-sn(-u)=sn u and dn(2r-u)=-dn(-u)=-dn u.
- (22.8.1)-(22.8.3): the sn/cn/dn addition identities used by the candidate. (22.6.1) supplies elementary square identities; (22.6.6)-(22.6.7) give the double-angle forms also derivable from additions. Table 22.13.1 gives derivatives.

The candidate's cited broad sections cover its principal period/shift/addition inputs. Adding explicit 22.2 and 22.6 locators would improve checkability but is not a mathematical dependency defect. The present audit verifies the cited standard inputs, not the correctness of every later Laurent or cyclic-sum deduction.

## Pins, provenance, and boundary of this result

Four fresh official primary PDF downloads match all four submitted source_manifest hashes byte for byte. SHA256s and requested/final URLs, UTC retrieval times, HTTP status and headers are in private_sources/ACQUISITION.json and STACHEL_ACQUISITION.json. The accepted head identity was supplied by the parent; no Git command was run to independently bind it to this local snapshot. Local submitted-file hashes are in INPUT_PINS.json.

The original arXiv TeX source archive was fetched from https://arxiv.org/src/2004.12497v11, SHA256 469a28edb7a0b762fc0515cb0e8d041c97df68165536bdff84b5d62403fa29e2; its bytes, acquisition record and read-only extracted TeX corpus are retained. No downloaded code was executed. All source PDF renderings used ordinary Poppler.

DLMF was accessible through the web tool, which exposed version 1.2.8 dated 2026-09-15. A direct standard-library HTML request received HTTP 403, so it was not retried or bypassed. DLMF web evidence is preserved locally; those tool-extracted records are not asserted to be byte-identical HTML captures.

No broad novelty search, other PR207 reviewer report reading, Git operation, original/global edit, external human communication, PR or service write occurred. No current openness, historical priority, firstness, or full mathematical acceptance is asserted. The strongest verified result is a matching source object, conic setting, edition map and analytic input set, with the explicit remaining primitive-vs-displayed-N contract qualification.
