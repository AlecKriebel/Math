from pathlib import Path
import importlib.util, json
root=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('retrieval',root/'retrieve_sources.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
record=module.retrieve(('kaplan_mallet_paret_yorke1984_author','https://yorke.umd.edu/Yorke_papers_most_cited_and_post2000/1984_01_Kaplan_Mallet-Paret_ETDS_Lyap_Dimension_of_torus.pdf'))
result={'schema':'pr111-historical-torus-retrieval/v1','records':[record],'copyright_material_private_ignored':True}
(root/'TORUS1984_RETRIEVAL_RECEIPT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
