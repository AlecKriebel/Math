#!/usr/bin/env python3
"""Read-only remote release and immutable-tag audit."""
import hashlib,json,pathlib,subprocess,urllib.request
HERE=pathlib.Path(__file__).resolve().parent
SOURCE=HERE.parent/'source_snapshot'
REV='953c836a12b9d9d474521feb4a96e218c1155203'
TAG='maximally-collective-stable-turing-v1.0.10'
meta=json.loads(subprocess.check_output(['gh','api','repos/AlecKriebel/Math/releases/tags/'+TAG]))
(HERE/'RELEASE_METADATA.json').write_text(json.dumps(meta,indent=2)+'\n')
remote=subprocess.check_output(['git','ls-remote','origin','refs/tags/'+TAG+'*'],text=True)
assert REV+'\trefs/tags/'+TAG+'^{}' in remote
(HERE/'REMOTE_TAG.txt').write_text(remote)
lookup={'arxiv_source.zip':'submission/arxiv/arxiv_source.zip','biorxiv_source_package.zip':'submission/biorxiv/source_package.zip','journal_source_package.zip':'submission/journal/source_package.zip','Exact_Diffusion_Design_main.pdf':'manuscript/main.pdf','Exact_Diffusion_Design_supplement.pdf':'manuscript/supplement.pdf','final_release_data.zip':'public/data_archive/final_release_data.zip',**{n+'_audit_packet.zip':'external_audit/packets/'+n+'_audit_packet.zip' for n in ('reaction_network','pde','symbolic')}}
assert len(meta['assets'])==9
out=HERE/'scratch/release_assets';out.mkdir(exist_ok=True)
results=[]
for a in meta['assets']:
    content=urllib.request.urlopen(a['browser_download_url'],timeout=90).read()
    (out/a['name']).write_bytes(content)
    local=SOURCE/lookup[a['name']]
    digest=hashlib.sha256(content).hexdigest()
    assert content==local.read_bytes(),a['name']
    assert len(content)==a['size'] and a['digest']=='sha256:'+digest
    results.append(dict(name=a['name'],bytes=len(content),sha256=digest,local=str(local.relative_to(SOURCE)),same=True))
(HERE/'RELEASE_ASSET_INTEGRITY.json').write_text(json.dumps(results,indent=2)+'\n')
print('REMOTE_TAG_AND_NINE_ASSETS_PASS')
