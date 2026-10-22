"""Read-only semantic preservation of final immutable publication-review bindings."""
from capture import *
import zipfile

def require(ok,msg):
    if not ok:raise ValueError(msg)
def check(data,pin):require(len(data)==pin['bytes'] and sha(data)==pin['sha256'],'pin')
results=[]
for n,pid in [(1141,30006210),(1150,30003045)]:
    c=json.loads((PRIVATE/'checkpoint'/HERE.parents[1].name/f'PR{n}_PUBLICATION_COVERAGE_DETAILS.json').read_text())
    prefix=f'draft_pr_actual_claims_1100_1200_20261017/audits/pr{n}_{pid}'
    root=PRIVATE/'release'/c['postfreeze_commit']/prefix
    pub=root/'publication';assets=c['all_six_release_assets']
    for name,pin in assets.items():check((pub/name).read_bytes(),pin)
    zfile=next((pub/'output').glob('*source-and-verification.zip'))
    pdf=next((pub/'output/pdf').glob('*.pdf'))
    with zipfile.ZipFile(pub/'output/zenodo-upload-kit.zip') as z:
        require(set(z.namelist())=={'README.md',zfile.name,pdf.name,'zenodo-metadata.json','zenodo-deposit.json'},'five-flat-kit-members')
        require(z.read(zfile.name)==zfile.read_bytes(),'kit-source')
        require(z.read(pdf.name)==pdf.read_bytes(),'kit-pdf')
        require(z.read('zenodo-metadata.json')==(pub/'zenodo-metadata.json').read_bytes(),'kit-metadata')
        deposit=json.loads(z.read('zenodo-deposit.json'))
        require(deposit['metadata']==json.loads((pub/'zenodo-metadata.json').read_text()),'kit-deposit-metadata')
        require({f['path'] for f in deposit['files']}=={zfile.name,pdf.name},'kit-deposit-paths')
    with zipfile.ZipFile(zfile) as z:
        require(z.read('main.tex')==(pub/'main.tex').read_bytes(),'operative-tex')
        require(z.read('zenodo-metadata.json')==(pub/'zenodo-metadata.json').read_bytes(),'source-metadata')
        require(z.read('zenodo-deposit.json')==(pub/'zenodo-deposit.json').read_bytes(),'source-deposit')
    reviews=[]
    for r in c.get('two_clean_reviews',c.get('two_clean_review_bindings')):
        folder=root/'reviews'/r['round'];report=(folder/'REPORT.md').read_bytes()
        require(sha(report)==r['report_sha256'],'report-root-pin')
        if n==1141:
            recdata=(folder/'RECEIPT.json').read_bytes()
            require(sha(recdata)==r['receipt_sha256'],'receipt-root-pin')
            rec=json.loads(recdata);require(rec['verdict']=='CLEAN_PASS','clean')
            if r['round']=='package_01':end=json.loads((folder/'END_PINS.json').read_text())['files']
            else:
                raw=json.loads((folder/'END_CUSTODY.json').read_text())['files']
                end={x['path'].split('/publication/')[1]:x for x in raw}
        else:
            recdata=(folder/'EXTERNAL_FINAL_RECEIPT.json').read_bytes()
            require(sha(recdata)==r['external_receipt_sha256'],'external-receipt-root-pin')
            rec=json.loads(recdata);require(rec['disposition']=='CLEAN_PASS' and rec['remaining_operative_issues']==[],'clean')
            check(report,rec['report'])
            check((folder/'FINAL_CHECKS.json').read_bytes(),rec['evidence']['FINAL_CHECKS.json'])
            end=json.loads((folder/'FINAL_CHECKS.json').read_text())['frozen_six']
        require(set(end)==set(assets),'six-end-assets')
        for name,pin in assets.items():
            require(all(end[name][k]==pin[k] for k in ['bytes','sha256']),'actual-end-pin')
        reviews.append({'round':r['round'],'report_sha256':sha(report),'receipt_sha256':sha(recdata),'all_six_actual_end_assets_bound':True,'clean_verdict_authenticated':True})
    results.append({'pr':n,'postfreeze_commit':c['postfreeze_commit'],'six_assets':assets,'flat_kit_five_exact_members':True,'two_clean_reviews':reviews,'scope':'Custody of specified review artifacts, not independent reexecution or repetition of their full mathematical audits.'})
(HERE/'PUBLICATION_BINDINGS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'publications':2,'immutable_assets':12,'clean_review_bindings':4,'passed':True}))
