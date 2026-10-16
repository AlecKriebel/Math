from pathlib import Path
import hashlib,json,datetime,subprocess
ROOT=Path(__file__).resolve().parent
SOURCES=[('hayman_lingham_2018','https://arxiv.org/pdf/1809.07200',1706228,'8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0'),('hedberg_wolff_1983','https://www.numdam.org/item/10.5802/aif.944.pdf',1782353,'f351a967ae723f590d85da9a886ca4f6d8a1a21f7de8315f83180d9dcf3b5006')]
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':'before any author proof, code, history, or other reviewer analysis','mechanism_not_yet_sealed':True,'receipts':[]}
for name,url,size,digest in SOURCES:
    source=ROOT.parent/'root_primary_private'/f'{name}.pdf'
    data=source.read_bytes(); actual=hashlib.sha256(data).hexdigest()
    assert len(data)==size and actual==digest,(name,len(data),actual)
    dest=ROOT/'private_sources'/f'{name}.txt'
    result=subprocess.run(['pdftotext','-layout',str(source),str(dest)],capture_output=True,text=True)
    out['receipts'].append({'name':name,'url':url,'original_pdf_path':str(source),'size':len(data),'sha256':actual,'extraction_exit':result.returncode,'extraction_stdout':result.stdout,'extraction_stderr':result.stderr,'extracted_text_sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
    assert result.returncode==0
(ROOT/'PRIMARY_SOURCE_RECEIPTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
