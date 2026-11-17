#!/usr/bin/env python3
"""One source-only opaque data intake. Prints metadata; executes no source code."""
from pathlib import Path
import datetime, hashlib, json, stat

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
N=P/'verification/outer-pedal-godbillon-vey-production-sol-20261116'
A=P/'verification/root-outer-pedal-godbillon-vey-gramian-editorial-adoption-20261116.json'
def need(ok,label):
    if not ok:raise ValueError(label)
def pin(data):return {'bytes':len(data),'SHA256':hashlib.sha256(data).hexdigest()}
def read(path):
    need(path.is_absolute() and '..' not in path.parts and all(not q.is_symlink() for q in [path,*path.parents]),'canonical ordinary path')
    a=path.lstat();need(stat.S_ISREG(a.st_mode),'regular source file')
    data=path.read_bytes();b=path.lstat()
    need((a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(b.st_ino,b.st_size,b.st_mtime_ns,b.st_ctime_ns),'stable opaque read')
    return data
def row(path):return {'path':str(path),**pin(read(path)),'mode':stat.S_IMODE(path.lstat().st_mode)}
def bound(item):
    path=Path(item['path']);path=path if path.is_absolute() else P/path
    need(pin(read(path))=={key:item[key] for key in ('bytes','SHA256')},'exact approved input '+str(path))
    return row(path)
def census(root):
    files={};directories={}
    def walk(directory):
        need(all(not q.is_symlink() for q in [directory,*directory.parents]),'ordinary namespace')
        before=directory.lstat();need(stat.S_ISDIR(before.st_mode),'directory')
        directories[directory.relative_to(root).as_posix()]=stat.S_IMODE(before.st_mode)
        for path in sorted(directory.iterdir()):
            kind=path.lstat().st_mode
            if stat.S_ISDIR(kind):walk(path)
            elif stat.S_ISREG(kind):files[path.relative_to(root).as_posix()]={key:value for key,value in row(path).items() if key!='path'}
            else:raise ValueError('special source/private entry')
        after=directory.lstat();need((before.st_ino,before.st_mtime_ns,before.st_ctime_ns)==(after.st_ino,after.st_mtime_ns,after.st_ctime_ns),'stable finite namespace')
    walk(root);return {'root':str(root),'files':files,'directories':directories}

authority_raw=read(A)
need(pin(authority_raw)=={'bytes':18652,'SHA256':'7b5367a6c98c13e304f93d8a582cc22c7fe0688e5cc0378bbbf1dce04b182cab'},'actual three-copy authority')
authority=json.loads(authority_raw)
need(authority['status']=='ROOT_ADOPTED_THREE_FULL_PRIVATE_EDITORIAL_COPIES__EXACT22PATH_PRIVATE_STAGE_GO' and authority['public_install_Git_deploy_AA_authority'] is False,'private copy authority only')
need([record['record'] for record in authority['records']]==['23398175','23357329','23153134'],'fixed exact three records')
receipt_raw=read(N/'BASELINE_CAPTURE_RECEIPT.json')
need(pin(receipt_raw)=={'bytes':3177,'SHA256':'640359149dbe8b8745630bccdf4f7868e59907808339f233042412a09becd280'},'frozen original receipt')
for item in json.loads(receipt_raw)['payloads']:
    need(pin(read(N/item['path']))=={key:item[key] for key in ('bytes','SHA256')},'all seven original baseline payloads remain exact')
records=[];namespaces=[];scope={'public/research/index.html','public/research/sitemap.xml'}
for record in authority['records']:
    identifier=record['record'];slug=record['proposed_slug'];pins=record['writer_pins']
    need('/' not in slug and '..' not in slug,'one exact approved slug')
    for item in pins.values():bound(item)
    for key in ('fact_FINAL','fact_manifest','fact_REPORT'):bound(record[key])
    source=census(P/'papers'/identifier/'sources')
    writer=census(P/'papers'/identifier/'reviews/editorial')
    fact=census((P/record['fact_FINAL']['path']).parent)
    need(len(source['files'])==record['source_extent']['files'] and len(source['directories'])-1==record['source_extent']['child_directories'],'exact frozen source extent')
    need(len(writer['files'])==record['writer_extent']['files'] and len(writer['directories'])-1==record['writer_extent']['child_directories'],'exact frozen writer extent')
    need(len(fact['files'])==record['fact_packet_files'],'exact fact file extent')
    namespaces.extend([source,writer,fact])
    prefix='public/research/'+slug+'/'
    assets=[{'native_name':name,'source':bound(pins['preview/'+name])} for name in record['native_assets_order']]
    article={'record':identifier,'sheet_row':record['sheet_row'],'slug':slug,'MAIN':bound(pins['MAIN.html']),'Bib':bound(pins['preview/citation.bib']),'assets':assets}
    records.append(article);scope.update([prefix+'index.html',prefix+'citation.bib',*[prefix+item['native_name'] for item in assets]])
need(len(scope)==22 and sum(len(item['assets']) for item in records)==14,'fixed22/14-native asset scope')
need(sum(len(item['files']) for item in namespaces)==703,'531 source plus172 editorial/fact files')
need(sum(len(namespaces[index]['files']) for index in (0,3,6))==531,'all531 source files')
need(read(A)==authority_raw and read(N/'BASELINE_CAPTURE_RECEIPT.json')==receipt_raw,'closing immutable authority/control guards')
print(json.dumps({'schema':'fixed-three-page-source-and-private-contract-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'OPAQUE_SOURCE_PRIVATE_CUSTODY_ONLY_NO_RELEASE_EXECUTION','copy_authority':row(A),'records':records,'scope_paths':sorted(scope),'namespaces':namespaces,'source_files':531,'editorial_fact_files':172,'total_guarded_files':703,'source_program_or_science_execution':False,'stage_namespace_or_implementation_read':False,'website_Git_Sheet_network_mutation':False,'all8_original_baseline_files_unchanged':True,'production_authority':False},indent=2,ensure_ascii=False))
