"""Compare independently fetched raw body against GitHub pinned contents API."""
from pathlib import Path
from datetime import datetime,UTC
import base64,hashlib,json
p=Path(__file__).resolve().parent
raw=(p/'private/PINNED_PROBLEM_AND_PROOF.md').read_bytes()
api=json.loads((p/'private/pinned_api_contents.json').read_bytes())
commit=json.loads((p/'private/pinned_api_commit.json').read_bytes())
decoded=base64.b64decode(api['content'])
blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
if not(raw==decoded and blob==api['sha'] and api['size']==len(raw) and commit['sha']=='7b403decdc9317f6ba3dc2c4a91243a0bf0c9ff9'):raise ValueError('pinned source consistency failure')
record={'utc':datetime.now(UTC).isoformat(),'raw_url':api['download_url'],'github_contents_api_url':api['url'],'path':api['path'],'pinned_commit_sha':commit['sha'],'pinned_commit_tree_sha':commit['tree']['sha'],'body_bytes':len(raw),'body_sha256':hashlib.sha256(raw).hexdigest(),'git_blob_sha1_computed':blob,'git_blob_sha1_api':api['sha'],'raw_equals_decoded_api_body':True,'commit_object_hash_independently_recomputed':False,'scope':'HTTPS GitHub commit endpoint and pinned contents endpoint agree with independent raw URL acquisition; Git blob object hash recomputed. This authenticates bytes/provenance, not mathematical correctness. No downloaded code was run.'}
(p/'PINNED_SOURCE_PROVENANCE.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
