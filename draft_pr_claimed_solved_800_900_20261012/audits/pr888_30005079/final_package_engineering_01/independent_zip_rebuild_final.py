"""Independent manual ZIP reconstruction: no portable.py or ZipFile writer.

Usage: python3 -I -S -B independent_zip_rebuild.py PACKAGE_ROOT INDEX_SHA ZIP_PATH
Only the receipt is written beside this audit helper; the ZIP is built in RAM.
"""
from pathlib import Path
import datetime,hashlib,json,re,stat,struct,sys,zlib

def require(ok,message):
    if not ok:raise ValueError(message)

def sha(raw):return hashlib.sha256(raw).hexdigest()

def pairs(rows):
    result={}
    for k,v in rows:
        require(k not in result,'duplicate JSON key');result[k]=v
    return result

def parse(raw):return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError('nonfinite JSON')))

def main():
    require(len(sys.argv)==4,'expected root, independent digest, ZIP path')
    root=Path(sys.argv[1]);pin=sys.argv[2];target=Path(sys.argv[3])
    require(re.fullmatch('[0-9a-f]{64}',pin),'external SHA syntax')
    raw=(root/'package_index.json').read_bytes();require(sha(raw)==pin,'external index mismatch')
    index=parse(raw);require(index['schema']=='rank-two-fano-30005079-verification-v1' and index['problem_id']=='30005079','target schema')
    blobs={'package_index.json':raw};folds=set()
    for row in index['files']:
        name=row['path'];require(type(name) is str and re.fullmatch('[A-Za-z0-9_./-]+',name) and all(p not in ('','.','..') for p in name.split('/')),'safe ASCII path')
        require(name.casefold() not in folds,'aliased path');folds.add(name.casefold())
        p=root/name;require(stat.S_ISREG(p.lstat().st_mode),'regular file required')
        data=p.read_bytes();require(type(row['bytes']) is int and len(data)==row['bytes'] and sha(data)==row['sha256'],'indexed input mismatch')
        blobs[name]=data
    local=bytearray();central=bytearray();dosdate=((2026-1980)<<9)|(10<<5)|16
    for name in sorted(blobs):
        encoded=name.encode('ascii');data=blobs[name];crc=zlib.crc32(data)&0xffffffff
        compressor=zlib.compressobj(9,zlib.DEFLATED,-15)
        compressed=compressor.compress(data)+compressor.flush(zlib.Z_FINISH)
        offset=len(local)
        local+=struct.pack('<4s5H3I2H',b'PK\x03\x04',20,0,8,0,dosdate,crc,len(compressed),len(data),len(encoded),0)+encoded+compressed
        central+=struct.pack('<4s6H3I5H2I',b'PK\x01\x02',(3<<8)|20,20,0,8,0,dosdate,crc,len(compressed),len(data),len(encoded),0,0,0,0,(stat.S_IFREG|0o644)<<16,offset)+encoded
    count=len(blobs)
    rebuilt=bytes(local+central)+struct.pack('<4s4H2IH',b'PK\x05\x06',0,0,count,count,len(central),len(local),0)
    original=target.read_bytes();require(rebuilt==original,'independent manual reconstruction differs')
    receipt={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_estimate_percent':90,'scope':'Independent manual ZIP reconstruction of the final candidate verification archive; auxiliary archive-byte evidence only, no mathematical, priority, whole-package or publication verdict.','mechanism':'Manual local headers, central headers and EOCD plus direct zlib.compressobj(9,DEFLATED,-15); does not import portable.py or use ZipFile to write.','package_index_sha256':pin,'member_count':count,'bytes':len(rebuilt),'sha256':sha(rebuilt),'actual_zip_rebuilt_in_memory':True,'byte_equal_to_default_build':True,'zlib_runtime':zlib.ZLIB_RUNTIME_VERSION,'compressed_byte_scope':'Same CPython/zlib runtime; cross-runtime compressed-byte identity is not claimed.'}
    (Path(__file__).absolute().parent/'INDEPENDENT_ZIP_REBUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))

if __name__=='__main__':main()
