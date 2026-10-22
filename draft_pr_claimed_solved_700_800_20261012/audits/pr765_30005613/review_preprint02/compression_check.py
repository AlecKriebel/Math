"""Read-only raw-DEFLATE comparison for the frozen source ZIP."""
from pathlib import Path
import json,struct,zipfile,zlib
archive=Path(__file__).resolve().parent.parent/'preprint/source-and-verification.zip'
raw=archive.read_bytes();rows=[]
with zipfile.ZipFile(archive) as z:
    for info in z.infolist():
        begin=info.header_offset
        namelen,extralen=struct.unpack_from('<HH',raw,begin+26)
        begin+=30+namelen+extralen
        actual=raw[begin:begin+info.compress_size]
        levels={}
        for level in (-1,6,9):
            c=zlib.compressobj(level=level,wbits=-15)
            expected=c.compress(z.read(info))+c.flush()
            levels[str(level)]={'compressed_bytes':len(expected),'matches_actual':actual==expected}
        rows.append({'member':info.filename,'actual_bytes':len(actual),'levels':levels})
print(json.dumps({'all_default':all(x['levels']['-1']['matches_actual'] for x in rows),
    'different_from_9':sum(not x['levels']['9']['matches_actual'] for x in rows),
    'paper_tex':next(x for x in rows if x['member']=='paper.tex')},indent=2))
