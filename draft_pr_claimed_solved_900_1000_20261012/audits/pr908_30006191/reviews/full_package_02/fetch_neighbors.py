#!/usr/bin/env python3
"""Refresh specified neighboring primary references, retaining raw bodies privately."""
import concurrent.futures,json
from fetch_sources import HERE,fetch
URLS={
 'gnrs2020.pdf':'https://arxiv.org/pdf/1912.12552v2',
 'gnrs2020_abs.html':'https://arxiv.org/abs/1912.12552',
 'hls2025.pdf':'https://arxiv.org/pdf/2310.17736v2',
 'hls2025_abs.html':'https://arxiv.org/abs/2310.17736',
 'buchholz2018.pdf':'https://arxiv.org/pdf/1709.08107v7',
 'buchholz2018_abs.html':'https://arxiv.org/abs/1709.08107',
 'buchholz2020.pdf':'https://arxiv.org/pdf/1807.07885v2',
 'buchholz2020_abs.html':'https://arxiv.org/abs/1807.07885',
 'frames2025.pdf':'https://arxiv.org/pdf/2406.15670v2',
 'frames2025_abs.html':'https://arxiv.org/abs/2406.15670',
 'pachon2026.pdf':'https://arxiv.org/pdf/2604.26267v2',
 'pachon2026_abs.html':'https://arxiv.org/abs/2604.26267',
 'br97_chapter.pdf':'https://page-one.springer.com/pdf/preview/10.1007/978-3-662-03444-6_7',
 'aps1990.html':'https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.64.1863',
 'thesis_landing.html':'https://escholarship.org/uc/item/45h4t6mj',
 'siebert_publications.html':'https://oliver-siebert.github.io/publications/',
 'gnrs_published.pdf':'https://link.springer.com/content/pdf/10.1007/s00023-020-00959-5.pdf',
 'hls_published.pdf':'https://link.springer.com/content/pdf/10.1007/s00023-024-01453-y.pdf',
}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:out=dict(pool.map(fetch,URLS.items()))
 (HERE/'SOURCE_NEIGHBOR_ACCESS.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({n:{k:v for k,v in r.items() if k not in ('pdf_info','final_url')} for n,r in out.items()},indent=2))
