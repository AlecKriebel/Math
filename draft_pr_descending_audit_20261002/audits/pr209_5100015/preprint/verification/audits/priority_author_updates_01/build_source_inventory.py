"""Build checkable byte/version receipts from actual read-only source files.
No network calls, downloaded code execution, or Git mutation.
"""
from pathlib import Path
import datetime, hashlib, html, json, re, subprocess, zipfile
BASE=Path(__file__).resolve().parent
PRIVATE=BASE/'private_reading'
MATH=Path('/Users/alec/Documents/Math')
AUDITS=MATH/'draft_pr_descending_audit_20261002/audits'
def receipt(path,url=None):
    data=path.read_bytes()
    return {'path':str(path),'source_url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'md5':hashlib.md5(data).hexdigest()}
aliases=[
 ('ferudun_v11',AUDITS/'pr210_5100033/initial_review_20261015/priority_author_updates_01/private_reading/ferudun14_v11.pdf','https://zenodo.org/api/records/23088516/files/main.pdf/content'),
 ('original_v11',AUDITS/'pr210_5100033/initial_review_20261015/source_domain_adversary_01/private_reading/invariants_v11.pdf','https://arxiv.org/pdf/2004.12497v11'),
 ('original_published',AUDITS/'pr210_5100033/initial_review_20261015/source_domain_adversary_01/private_reading/invariants_final.pdf','https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf'),
 ('stachel_published',AUDITS/'pr210_5100033/initial_review_20261015/source_domain_adversary_01/private_reading/stachel_published.pdf','https://link.springer.com/content/pdf/10.1007/s40879-021-00524-2.pdf'),
 ('chavez_published',AUDITS/'pr211_5100063/initial_review_20261015/priority_classical_general_01/private_reading/chavez_published.pdf','https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf'),
 ('bialy_v2',AUDITS/'pr255_5100022/initial_review_20261013/priority_classical_adversary_01/sources/bialy_tabachnikov.pdf','https://arxiv.org/pdf/2001.08469v2'),
 ('bicentric_v3',AUDITS/'pr211_5100063/initial_review_20261015/priority_author_updates_01/private_reading/bicentric.pdf','https://arxiv.org/pdf/2103.11260v3'),
 ('bicentric_published',AUDITS/'pr211_5100063/initial_review_20261015/priority_author_updates_01/private_reading/bicentric_final.pdf','https://armj.math.stonybrook.edu/pdf-Springer-final/021-0188.pdf'),
 ('pedallike_v3',AUDITS/'pr210_5100033/initial_review_20261015/priority_author_updates_01/private_reading/pedallike_2009.02581v3.pdf','https://arxiv.org/pdf/2009.02581v3'),
 ('topics_v1',AUDITS/'pr210_5100033/initial_review_20261015/priority_author_updates_01/private_reading/topics_2108.08293v1.pdf','https://arxiv.org/pdf/2108.08293v1'),
]
for family,prefix,versions,arxiv in [
 ('self_intersect','self_intersect_v',[1,2,3],'2011.06640'),
 ('talented_inversive','talented_inversive_v',[1,2],'2012.03020')]:
 for v in versions:
  aliases.append((family+'_v'+str(v),AUDITS/('pr211_5100063/initial_review_20261015/priority_author_updates_01/private_reading/'+prefix+str(v)+'.pdf'),'https://arxiv.org/pdf/'+arxiv+'v'+str(v)))
out=[]
for name,path,url in aliases:
    row=receipt(path,url);row['name']=name;row['existing_bytes_read_in_place']=True;out.append(row)
    # Reading aids are newly derived only if not already available here.
    target=PRIVATE/(name+'.txt')
    if not target.exists(): subprocess.run(['pdftotext','-layout',str(path),str(target)],check=True)
assert out[0]['sha256']=='5ff816c279e39f478e96ae5454779cc3b5280bc9eed1084429578540b3d352b6'
meta=json.loads((PRIVATE/'zenodo23088516.json').read_text())
pdf_entry=next(x for x in meta['files'] if x['key']=='main.pdf')
assert pdf_entry['size']==out[0]['bytes'] and pdf_entry['checksum']=='md5:'+out[0]['md5']

downloads=json.loads((BASE/'SOURCE_ACCESS_RECEIPTS.json').read_text())
for row in downloads:
    if row['success']:
        actual=receipt(Path(row['saved_private_path']))
        assert actual['bytes']==row['bytes'] and actual['sha256']==row['sha256']
    elif 'saved_private_error_path' in row:
        actual=receipt(Path(row['saved_private_error_path']))
        assert actual['bytes']==row['error_bytes'] and actual['sha256']==row['error_sha256']
for f in ['bicentric_v1','bicentric_v2','harmonic_v1','harmonic_v2']:
    target=PRIVATE/(f+'.txt')
    if not target.exists(): subprocess.run(['pdftotext','-layout',str(PRIVATE/(f+'.pdf')),str(target)],check=True)

archive_members=[]
for version in ['v10','v11']:
    path=PRIVATE/('ferudun14_'+version+'_source.zip')
    with zipfile.ZipFile(path) as archive:
        members=[]
        for name in archive.namelist():
            data=archive.read(name)
            members.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        archive_members.append({'version':version,'archive':receipt(path),'members':members,'downloaded_code_executed':False})

original_versions=[]
for v in range(1,12):
    path=PRIVATE/('invariants_v%d.pdf'%v) if v<11 else Path(out[1]['path'])
    text=(PRIVATE/('invariants_v%d.txt'%v)).read_text()
    pages=text.split('\f'); matches=[]
    for page_no,page in enumerate(pages,1):
        if 'k303,b' in page:
            table=re.search(r'Table\s+(\d+)',page[page.index('k303,b'):])
            matches.append({'pdf_page':page_no,'table':int(table.group(1)) if table else None,
                            'target_row_still_question_mark':True})
    assert len(matches)==1
    original_versions.append({'version':v,'byte_receipt':receipt(path,'https://arxiv.org/pdf/2004.12497v%d'%v),'target_locations':matches})

data={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'existing_primary_files':out,'download_receipts_checked':len(downloads),
      'all_saved_successful_HTTP_bytes_match':True,'source_archives':archive_members,
      'all_retained_HTTP_error_bytes_match':True,
      'original_arxiv_versions':original_versions,'scope':'Hash/byte/source-location evidence; question-mark interpretation independently read in the actual full target passages. No inference that an old question mark proves present openness.'}
(BASE/'SOURCE_BYTE_INVENTORY.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'existing_files':len(out),'http_receipts':len(downloads),'original_versions':len(original_versions),'archives':len(archive_members),'all_saved_HTTP_bytes_match':True}))
