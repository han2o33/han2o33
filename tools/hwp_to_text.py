import sys, olefile, zlib, struct
def text(path):
    ole = olefile.OleFileIO(path)
    hdr = ole.openstream('FileHeader').read()
    compressed = hdr[36] & 1
    out=[]
    secs = sorted([s for s in ole.listdir() if s[0]=='BodyText'], key=lambda s:int(s[1][7:]))
    for s in secs:
        data = ole.openstream(s).read()
        if compressed: data = zlib.decompress(data, -15)
        i=0
        while i < len(data):
            h = struct.unpack_from('<I', data, i); i+=4
            tag = h[0] & 0x3ff; size = (h[0]>>20)&0xfff
            if size == 0xfff: size = struct.unpack_from('<I', data, i)[0]; i+=4
            rec = data[i:i+size]; i+=size
            if tag == 67:
                chars=[]; j=0
                while j < len(rec):
                    c = struct.unpack_from('<H', rec, j)[0]
                    if c < 32:
                        if c in (0,10,13,24,25,26,27,28,29,30,31): 
                            if c==13: chars.append('\n')
                            j+=2
                        else:
                            if c==9: chars.append('\t')
                            j+=16
                        continue
                    chars.append(chr(c)); j+=2
                out.append(''.join(chars))
    return ''.join(out)
for p in sys.argv[1:]:
    print('=====', p); print(text(p))
