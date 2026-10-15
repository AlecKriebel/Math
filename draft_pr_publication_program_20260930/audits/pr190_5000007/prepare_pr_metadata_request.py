"""Prepare exact original-head PR metadata only after actual publication/tracker."""
from pathlib import Path
import datetime,json
A=Path(__file__).resolve().parent
def read(n):return json.loads((A/n).read_text())
z=read('ZENODO_PUBLICATION_READBACK.json');tr=read('TRACKER_ACCEPTANCE.json');g=read('ROOT_PUBLICATION_GATE.json');p=read('PR_METADATA_PROPOSAL_02.json')
if z['state']!='published' or g['status']!='READY_FOR_AUTHORIZED_PUBLICATION' or tr['DOI']!=z['doi'] or tr['status']!='TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED':raise RuntimeError('Actual gated publication/tracker absent')
marker='The exact four-page paper and supporting packet are prepared for the required successive new whole-package adversarial reviews.'
if p['body'].count(marker)!=1:raise RuntimeError('Reviewed proposal structure drift')
body=p['body'].split(marker)[0].rstrip()+'\n\n'
body+='Published research note: ['+z['doi']+']('+z['doi_url']+'). The exact four-page paper, standalone LaTeX and verification package completed the successive fresh whole-package adversarial review loop. Review01 required correcting obsolete DOI-file inaccessibility wording; the repair was propagated globally and a new reviewer found no required issues. Current Ferudun DOI-version files match the inspected website copies. The actual publication and tracker '+tr['range']+' are verified; original-head MAIN integration follows separately.\n\n'
body+='The package retains dated assembly/pending-state records as historical provenance. The later Root publication gate binds the immutable upload bytes to the completed review sequence. Original submission head `0c3346c8ebcb3b967a1d8bf9a283f027b44b738c` and all22 historical files are preserved; original effort remains unknown/5(interrupted). Extensive AI was used; this is unrefereed and has not undergone conventional human peer review. No historical firstness, guaranteed novelty, author-authenticated source erratum or independence certification is claimed.\n'
out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'expected_original_head':'0c3346c8ebcb3b967a1d8bf9a283f027b44b738c','request':{'repository_full_name':'AlecKriebel/Math','pr_number':190,'title':p['title'],'body':body},'DOI':z['doi'],'tracker_range':tr['range'],'state':'PREPARED_METADATA_NOT_YET_SENT'}
(A/'PR_METADATA_REQUEST.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['state'],'title':p['title'],'DOI':z['doi'],'body_characters':len(body)}))
