# 30002957 / OWR-13940-005: flag faces versus Poisson–Delaunay faces

## Exact primary source

Ulrich Bauer's **Problem TWO**, *Computational Geometric and Algebraic Topology*, Oberwolfach Report45/2015, printed p.2692 (PDF p.56), DOI10.4171/OWR/2015/45. [Official complete report](https://publications.mfo.de/bitstream/handle/mfo/3492/OWR_2015_45.pdf?isAllowed=y&sequence=1).

The complete contribution and its comments were read and visually verified. It starts from a Poisson process in Euclidean dimension d, takes the Delaunay triangulation's1-skeleton and forms its flag complex. It asks how many of the flag d-simplices, and more generally flag k-simplices for k≤d, are Delaunay. Its comments ask how the likelihood changes with dimension, motivate storing only the1-skeleton, and mention related stochastic-geometry results for specified simplex shapes. Neighboring immersion and knot questions are separate.

The imported expanded title does not specify the sampling rule or add an authoritative theorem. The source itself does not state a finite observation window, an anchor, or a precise Palm law. In the full infinite-space process, raw total counts are not the intended informative quantity. This attempt will use a stationary homogeneous Poisson process of intensity λ>0 and explicitly define **simplex intensities and large-window fractions**, with each simplex counted once using its barycenter. A vertex-Palm count must be divided by k+1 and a uniform point in a simplex would have a different volume bias. These distinctions must be proved/maintained, not silently identified. Any broader inhomogeneous interpretation is outside that convention.

## Existing numerator results

Herbert Edelsbrunner, Anton Nikitenko and Matthias Reitzner, *Expected Sizes of Poisson–Delaunay Mosaics and Their Discrete Morse Functions*, Advances in Applied Probability49(3)(2017),745–767, DOI **10.1017/apr.2017.20**. The imported literature note instead links .4; the title's actual DOI is confirmed by the primary arXiv record. [arXiv:1607.05915v1](https://arxiv.org/abs/1607.05915), [PDF](https://arxiv.org/pdf/1607.05915).

The retrieved PDF is explicitly the2016 arXiv v1, not a publisher-typeset copy. Its introduction, Theorem1, Corollary2 and Table2 were read. They give expected **Delaunay** simplex intensities and radius distributions; their counts use smallest empty circumball centers. In dimension2, the vertex/edge/triangle intensity coefficients are1,3,2. Any transfer to a barycenter anchoring will be justified separately. These results do not by themselves count all cliques of the Delaunay graph, so they provide the numerator rather than the missing flag-complex denominator.

Related higher-order Delaunay-mosaic formulas count a different geometric complex and cannot be substituted for graph clique counts. A bounded current-literature search by the exact source wording, Poisson–Delaunay flag complexes, graph cliques, and separating triangles found no complete general answer to the requested flag fractions. A later application reports empirical large cliques, but its full PDF retrieval failed; no theorem or quantitative conclusion is based on that search snippet. The bounded search is not a certification of absence of later work.

## Prior-attempt and alias gate

Target and OWR-alias PR/commit searches, semantic Delaunay/flag and Poisson/Delaunay searches, both conventional repository target paths,365 live branch names and425 locally mirrored refs found no matching attempt. See PRIOR_GATE.json. Dataset questions about skeletal complexes on Delone sets, Delaunay realization spaces and polytope unfoldings are distinct. No exact duplicate was found. These checks do not certify inaccessible/deleted history. Direct UnsolvedMath access failed; pinned imports were checked against the primary report.

## Eligibility and budget

Eligible for a new five-turn attempt. **Substantive author count0/5.** No complete resolution or counterexample is claimed by this source gate. The immediate goals are to make the stationary fraction well-defined, derive nontrivial exact relations/bounds, and seek an evaluable formula rather than rename an uncomputed probability as an answer. Known Delaunay intensity formulas remain credited prior work.
