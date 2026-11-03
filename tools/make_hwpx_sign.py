import sys, re, zipfile, os
ref_dir, out_path, line1, line2 = sys.argv[1:5]
hdr = open(os.path.join(ref_dir,'Contents/header.xml'),encoding='utf-8').read()
sec_ref = open(os.path.join(ref_dir,'Contents/section0.xml'),encoding='utf-8').read()

# --- header: add 2 charPr (HY헤드라인M clones of id 46) and 1 paraPr (clone of 13, line spacing 130)
n_char = int(re.search(r'<hh:charProperties itemCnt="(\d+)"',hdr).group(1))
c46 = re.search(r'<hh:charPr id="46".*?</hh:charPr>',hdr,re.S).group(0)
cp1 = c46.replace('id="46"',f'id="{n_char}"').replace('height="2000"','height="4000"')
cp2 = c46.replace('id="46"',f'id="{n_char+1}"').replace('height="2000"','height="8800"')
hdr = hdr.replace(f'<hh:charProperties itemCnt="{n_char}"',f'<hh:charProperties itemCnt="{n_char+2}"')
hdr = hdr.replace('</hh:charProperties>', cp1+cp2+'</hh:charProperties>')
n_para = int(re.search(r'<hh:paraProperties itemCnt="(\d+)"',hdr).group(1))
p13 = re.search(r'<hh:paraPr id="13".*?</hh:paraPr>',hdr,re.S).group(0)
pp = p13.replace('id="13"',f'id="{n_para}"').replace('<hh:lineSpacing type="PERCENT" value="160"','<hh:lineSpacing type="PERCENT" value="130"')
hdr = hdr.replace(f'<hh:paraProperties itemCnt="{n_para}"',f'<hh:paraProperties itemCnt="{n_para+1}"')
hdr = hdr.replace('</hh:paraProperties>', pp+'</hh:paraProperties>')
CH1, CH2, PCENTER = n_char, n_char+1, n_para

# --- section
ns_open = re.match(r'(<\?xml[^>]*\?>\s*<hs:sec[^>]*>)',sec_ref).group(1)
secpr = re.search(r'<hp:secPr .*?</hp:secPr>',sec_ref,re.S).group(0)
secpr = re.sub(r'<hp:pagePr [^>]*>', '<hp:pagePr landscape="NARROWLY" width="59528" height="84188" gutterType="LEFT_ONLY">', secpr)
secpr = re.sub(r'<hp:margin [^/]*/>', '<hp:margin header="0" footer="0" gutter="0" left="5669" right="5669" top="4251" bottom="4251"/>', secpr)
colpr = '<hp:ctrl><hp:colPr id="" type="NEWSPAPER" layout="LEFT" colCount="1" sameSz="1" sameGap="0"/></hp:ctrl>'
pic = re.search(r'<hp:pic .*?</hp:pic>',sec_ref,re.S).group(0)
# logo: bottom center of page, ~70mm wide (keep aspect 668:72)
LW = 19843; LH = round(LW*72/668)
pic = re.sub(r'<hp:curSz [^/]*/>', f'<hp:curSz width="{LW}" height="{LH}"/>', pic)
pic = re.sub(r'<hp:sz [^/]*/>', f'<hp:sz width="{LW}" widthRelTo="ABSOLUTE" height="{LH}" heightRelTo="ABSOLUTE" protect="0"/>', pic)
pic = re.sub(r'<hp:pos [^/]*/>', '<hp:pos treatAsChar="0" affectLSpacing="0" flowWithText="0" allowOverlap="1" holdAnchorAndSO="0" vertRelTo="PAPER" horzRelTo="PAPER" vertAlign="BOTTOM" horzAlign="CENTER" vertOffset="4251" horzOffset="0"/>', pic)
sx, sy = LW/50100, LH/5400
pic = re.sub(r'<hc:scaMatrix [^/]*/>', f'<hc:scaMatrix e1="{sx:.5f}" e2="0" e3="0" e4="0" e5="{sy:.5f}" e6="0"/>', pic)
pic = re.sub(r'<hc:transMatrix [^/]*/>', '<hc:transMatrix e1="1" e2="0" e3="0" e4="0" e5="1" e6="0"/>', pic)
pic = re.sub(r'<hp:offset [^/]*/>', '<hp:offset x="0" y="0"/>', pic)
pic = re.sub(r'<hp:rotationInfo [^/]*/>', f'<hp:rotationInfo angle="0" centerX="{LW//2}" centerY="{LH//2}" rotateimage="1"/>', pic)
pic = pic.replace('textWrap="TOP_AND_BOTTOM"','textWrap="IN_FRONT_OF_TEXT"')

TW = 84188 - 2*5669
BAR = 567
def cell(row, bf, h, inner, valign="CENTER"):
    return (f'<hp:tr><hp:tc name="" header="0" hasMargin="0" protect="0" editable="0" dirty="0" borderFillIDRef="{bf}">'
            f'<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="{valign}" linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" hasNumRef="0">{inner}</hp:subList>'
            f'<hp:cellAddr colAddr="0" rowAddr="{row}"/><hp:cellSpan colSpan="1" rowSpan="1"/><hp:cellSz width="{TW}" height="{h}"/>'
            f'<hp:cellMargin left="141" right="141" top="141" bottom="141"/></hp:tc></hp:tr>')
empty = '<hp:p id="2147483648" paraPrIDRef="4" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="37"/></hp:p>'
def para(cp, text): return f'<hp:p id="2147483648" paraPrIDRef="{PCENTER}" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="{cp}"><hp:t>{text}</hp:t></hp:run></hp:p>'
TH = 26000
rows = cell(0,9,BAR,empty) + cell(1,7,TH, para(CH1,line1)+para(CH2,line2)) + cell(2,8,BAR,empty)
tbl = (f'<hp:tbl id="1999000001" zOrder="1" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="0" rowCnt="3" colCnt="1" cellSpacing="0" borderFillIDRef="5" noAdjust="0">'
       f'<hp:sz width="{TW}" widthRelTo="ABSOLUTE" height="{2*BAR+TH}" heightRelTo="ABSOLUTE" protect="0"/>'
       '<hp:pos treatAsChar="0" affectLSpacing="0" flowWithText="0" allowOverlap="0" holdAnchorAndSO="0" vertRelTo="PAPER" horzRelTo="PAPER" vertAlign="CENTER" horzAlign="CENTER" vertOffset="0" horzOffset="0"/>'
       '<hp:outMargin left="0" right="0" top="0" bottom="0"/><hp:inMargin left="141" right="141" top="141" bottom="141"/>'
       + rows + '</hp:tbl>')
body = (f'<hp:p id="0" paraPrIDRef="30" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0"><hp:run charPrIDRef="19">{secpr}{colpr}</hp:run>'
        f'<hp:run charPrIDRef="19">{tbl}{pic}</hp:run></hp:p>')
sec = ns_open + body + '</hs:sec>'

with zipfile.ZipFile(out_path,'w') as z:
    z.writestr(zipfile.ZipInfo('mimetype'), open(os.path.join(ref_dir,'mimetype'),'rb').read(), compress_type=zipfile.ZIP_STORED)
    for name in ['version.xml','META-INF/container.xml','META-INF/container.rdf','META-INF/manifest.xml','Contents/content.hpf','settings.xml','BinData/image1.bmp']:
        data = open(os.path.join(ref_dir,name),'rb').read()
        if name=='settings.xml': data = re.sub(rb'<ha:CaretPosition [^/]*/>', b'<ha:CaretPosition listIDRef="0" paraIDRef="0" pos="0"/>', data)
        z.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr('Contents/header.xml', hdr.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
    z.writestr('Contents/section0.xml', sec.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
    z.writestr('Preview/PrvText.txt', (line1+' '+line2).encode('utf-16-le') if False else (line1+' '+line2).encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
    if len(sys.argv)>5: z.writestr('Preview/PrvImage.png', open(sys.argv[5],'rb').read(), compress_type=zipfile.ZIP_DEFLATED)
print('ok')
