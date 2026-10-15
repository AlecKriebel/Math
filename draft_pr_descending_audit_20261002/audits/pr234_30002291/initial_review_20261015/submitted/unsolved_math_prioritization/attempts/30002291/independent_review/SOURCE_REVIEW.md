# Source and scope review: 30002291

## Exact question

The official [OWR 09/2013 report](https://ems.press/content/serial-article-files/46440), printed p.492, was read as text and visually. It gives a fixed-time stable quadratic-variation limit for compound-Poisson drivers and then asks for an extension to a rather general pure-jump semimartingale under sufficient conditions. It specifies no maximal driver class. The normalization is Delta^(-2 alpha), 0<alpha<1/2, the coefficient is f(0)^2, and each squared jump is weighted by the displayed independent-uniform-phase series. The author theorem matches those objects. It explicitly strengthens the tail regularity to a bound on both f and f'.

## Prior results and edition limits

- Basse-O'Connor, Lachièze-Rey and Podolskij, *Power variation for a class of stationary increments Lévy driven moving averages*, Ann. Probab.45 (2017), 4477-4528, [DOI 10.1214/16-AOP1170](https://doi.org/10.1214/16-AOP1170). The complete [arXiv:1506.06679v1](https://arxiv.org/abs/1506.06679v1) was checked. Its model uses a symmetric Lévy driver, and Theorem1.1(i) gives the jump-weighted stable limit with p>beta and alpha<k-1/p, under its kernel assumptions. The preprint has a different title. Its compiled title page says June2021 while the arXiv version label is June2015; this is not treated as a new publication or theorem.
- Basse-O'Connor, Heinrich and Podolskij, *On limit theory for Lévy semi-stationary processes*, Bernoulli24(4A) (2018), 3117-3146, [DOI 10.3150/17-BEJ956](https://doi.org/10.3150/17-BEJ956). The complete [arXiv:1604.02307v2](https://arxiv.org/abs/1604.02307v2) was checked. Model(1.2) permits adapted càdlàg volatility against a symmetric Lévy process; independence of volatility is not required. Theorem1.2(i), with its (A),(B1), beta<2, p>beta, p>=1 and alpha<k-1/p, gives functional stable M1 convergence. Remark1.4 excludes J1 and J2. At p=2,k=1, replacing U by1-U and shifting the series index gives exactly the candidate's phase weight; the jump amplitude is that of the semimartingale driver.

Journal metadata was cross-checked against the [author's publication list](https://sites.google.com/site/basseoconnor/publications) and the [official Bernoulli issue material](https://www.imstat.org/publications/bej/bej_24_4a/bej_24_4a.pdf). The latter contains article headers/abstracts/references, **not** the complete article proof. The final Euclid article endpoint was unavailable during this review. Thus theorem numbering and detailed hypotheses above were checked in complete primary preprints, and final publication metadata in the official materials. One institutional record has inconsistent Bernoulli pagination; the official header and author's list agree with 3117-3146 used by the packet.

## Scope disposition

The candidate proves a genuine sufficient-conditions theorem for arbitrary predictable time-absolutely-continuous jump kernels with deterministic drift and quadratic-rate bounds. This is not restricted to independent-increment or scalar-volatility Lévy drivers. Its class includes infinite-activity examples of jump index2, and its assumptions control the whole past explicitly. Therefore it supplies the kind of general-driver sufficient conditions requested in the source. I accept it as a complete answer in that explicitly bounded scope, rather than requiring an unspecified maximal-class classification.

This disposition does not certify novelty, characterize all admissible drivers, replace the cited 2017/2018 results, or authorize a claim for arbitrary pure-jump semimartingales. Publication must keep the class and fixed-time/finite-dimensional scope visible. A deterministic-time jump lies outside the hypotheses and demonstrates why a blanket statement would be false.

The three author reading-copy hashes match source_manifest.json. Source PDFs, extracted texts and source-page images are excluded from the portable review packet.
