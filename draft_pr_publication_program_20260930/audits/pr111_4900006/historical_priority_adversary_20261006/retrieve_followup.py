from pathlib import Path
import importlib.util, concurrent.futures, json
root=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('retrieval',root/'retrieve_sources.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
sources=[
 ('leonov_kuznetsov2016_survey','https://arxiv.org/pdf/1510.03835v2'),
 ('leonov2015_lorenz_formula','https://arxiv.org/pdf/1508.07498v1'),
 ('rabinovich2018_published','https://d-nb.info/1160228949/34'),
 ('iucat_general_search','https://iucat.iu.edu/?q=An%20abstract%20theory%20of%20L-exponents'),
]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e:
 records=list(e.map(module.retrieve,sources))
result={'schema':'pr111-historical-followup-retrieval/v1','records':records,'copyright_material_private_ignored':True}
(root/'PUBLIC_FOLLOWUP_RETRIEVAL_RECEIPT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
