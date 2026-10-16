"""Primary literature followups; all payloads remain under ignored private/."""
from retrieve_primary import BASE, PRIVATE, fetch
import concurrent.futures, json

SOURCES = {
    'liu_research_20261015': 'https://www.math.univ-paris13.fr/~mingkun.liu/research.html',
    'delecroix_research_20261015': 'https://www.labri.fr/perso/vdelecro/research.html',
    'dl_publisher_metadata': 'https://ems.press/journals/jems/articles/14297869',
    'dgzz_publisher_metadata': 'https://link.springer.com/article/10.1007/s00222-022-01123-y',
    'metric_maps_arxiv': 'https://arxiv.org/abs/2312.10517',
    'metric_maps_final': 'https://www.cambridge.org/core/services/aop-cambridge-core/content/view/556F7E6B21E3E0F5C15C887034EA7A9A/S2050509425000313a.pdf/div-class-title-length-spectrum-of-large-genus-random-metric-maps-div.pdf',
    'non_simple_curves_2026_arxiv': 'https://arxiv.org/abs/2605.03833',
    'dl_arxiv_v1': 'https://arxiv.org/pdf/2202.10255v1',
}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    entries = list(pool.map(fetch, SOURCES.items()))
(PRIVATE / 'followup_retrieval_raw.json').write_text(json.dumps(entries, indent=2) + '\n')
safe = [{k: v for k, v in entry.items() if k != 'response_headers'} for entry in entries]
(BASE / 'FOLLOWUP_SOURCE_PINS.json').write_text(json.dumps(safe, indent=2) + '\n')
print(json.dumps(safe, indent=2))
