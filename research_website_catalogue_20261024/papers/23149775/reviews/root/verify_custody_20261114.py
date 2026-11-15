"""Read-only authentication of the three immutable116 review envelopes."""
from pathlib import Path
import hashlib,json

R=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def main():
    lanes=[('scope','OWNED_MANIFEST.json','SEAL.json','2cc7abb54975e50ba7b5e67ed2f30344411dd56aee1247746d53f46869af9fe1','SHA256'),
           ('analytic','FINAL_MANIFEST.json','FINAL_SEAL.json','bfbc556e108438e4e737264f63769a3cbec1640b9fd3cb1605221e02e3bf5d38','SHA256'),
           ('adversarial','FINAL_MANIFEST.json','FINAL_SEAL.json','abfe6f9077c01a0f978e9c74646450d2df6dad9c1806bbd6566cbb4a5dcae679','sha256')]
    results=[]
    for lane,mn,sn,pin,hkey in lanes:
        folder=R.parent/lane;seal=load(folder/sn);manifest=load(folder/mn)
        require(sha(folder/sn)==pin,'exact final seal '+lane)
        mh=seal['bound_files_SHA256'][mn] if lane=='scope' else seal['owned_manifest_SHA256'] if lane=='analytic' else seal['manifest_sha256']
        require(sha(folder/mn)==mh,'manifest pin '+lane)
        for entry in manifest['files']:
            p=Path(entry['path']);p=p if p.is_absolute() else folder/p
            require(p.is_file() and not p.is_symlink(),'regular bound file')
            require(p.stat().st_size==entry['bytes'] and sha(p)==entry[hkey],'whole bound payload '+str(p))
        if lane=='analytic':
            actual={str(p.relative_to(folder)) for p in folder.rglob('*') if p.is_file()}-{'FINAL_MANIFEST.json','FINAL_SEAL.json'}
            require(actual=={e['path'] for e in manifest['files']},'entire analytic owned inventory')
        results.append({'lane':lane,'owned_payloads':len(manifest['files']),'seal_sha256':pin,'literal_verdict':load(folder/'VERDICT.json')})
    require(sha(R/'INITIAL_SEAL_20261114.json')=='8d3a6612e86cae3c76ee2f9237040421d8931b58065f7eafc4e96d8882c4259f','root independent initial')
    require(all(x['exit_code']==0 for x in load(R/'CUSTODY_EXECUTIONS_20261114.json')['actual_executions']),'actual three closures and root exact certificate')
    print(json.dumps({'status':'PASS_ROOT116_THREE_WHOLE_SEALED_PACKETS_NO_CAMPAIGN_REPLAY','lanes':results,'scientific_programs_rerun':False,'source_or_peer_mutation':False,'publication_authority':False},sort_keys=True))
if __name__=='__main__':main()
