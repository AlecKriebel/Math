"""Administrative semantic rejection controls; reads only, no network."""
from pathlib import Path
import copy,json,sys
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;T=W.parent
import verify_admin as v
get=lambda n:json.loads((W/n).read_text())
ext=lambda n:json.loads((T/n).read_text())
public=[ext('preprint/zenodo-metadata.json')['metadata'],get('ZENODO_PUBLIC_RECORD.json'),ext('publication/STAGE_RECEIPT.json'),ext('publication/PUBLISH_RECEIPT.json'),ext('publication/INSPECT_AFTER_PUBLISH.json'),get('PUBLICATION_INDEPENDENT_CHECK.json')]
merge=[get('MERGE_SCOPE_PROOF.json'),get('QUEUE_SCOPE_WITNESS.json'),ext('intake/ROOT_SOURCE_IDENTITY.json')]
tracker=[ext('publication/SHEET_VERIFICATION.json'),ext('publication/SHEET_APPEND_RECEIPT.json'),get('TRACKER_INDEPENDENT_READBACK.json'),ext('TRACKER_SCOPE.json')]
results=[]
def run(name,fn,args,mutate,expected):
 a=copy.deepcopy(args);mutate(a)
 try:fn(*a);accepted=True
 except (ValueError,KeyError,TypeError,IndexError):accepted=False
 if accepted!=expected:raise RuntimeError('Control failed '+name)
 results.append({'name':name,'accepted':accepted,'expected_accept':expected})
run('exact public record',v.check_public,public,lambda a:None,True)
run('exact scope tree',v.check_merge,merge,lambda a:None,True)
run('exact four tracker cells',v.check_tracker,tracker,lambda a:None,True)
run('changed DOI',v.check_public,public,lambda a:a[1]['metadata'].update(doi='10.5281/zenodo.1'),False)
run('changed public description',v.check_public,public,lambda a:a[1]['metadata'].update(description=a[1]['metadata']['description']+'changed'),False)
run('changed public payload SHA',v.check_public,public,lambda a:a[5]['public_files'][0].update(sha256='0'*64),False)
run('metadata normalization introduced',v.check_public,public,lambda a:a[3].update(metadata_normalizations=['changed']),False)
run('extra merge path',v.check_merge,merge,lambda a:a[0]['updates'].update({'unrelated.txt':{'mode':'100644','type':'blob','sha':'0'*40}}),False)
run('changed merge parent',v.check_merge,merge,lambda a:a[0]['merge_commit']['parents']['nodes'][1].update(oid='0'*40),False)
run('changed original source blob',v.check_merge,merge,lambda a:a[0]['original_candidate_files'][0].update(git_blob='0'*40),False)
run('changed baseline Merkle entry',v.check_merge,merge,lambda a:next(iter(a[0]['base_tree_objects_used'].values())).pop(next(iter(next(iter(a[0]['base_tree_objects_used'].values()))))),False)
run('changed tracker DOI',v.check_tracker,tracker,lambda a:a[2]['values'][0].__setitem__(2,'https://doi.org/10.5281/zenodo.1'),False)
run('tracker writes extra row',v.check_tracker,tracker,lambda a:a[1]['updates'].update(updatedRows=2),False)
run('tracker scope qualification deleted',v.check_tracker,tracker,lambda a:a[3].update(priority_summary='priority absent'),False)
print(json.dumps({'result':'PASS','positive_controls':3,'negative_controls':11,'controls':results},sort_keys=True))
