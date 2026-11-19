"""Titanium OS / Minimal. Generates self-contained animated SVGs. Python stdlib only.
Run: python scripts/render_cards.py ; STATIC=1 python scripts/render_cards.py
Edit config.json for text, project URLs and identity. No GitHub API required.
"""
import html, json, os, base64, io
from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path
R=Path(__file__).resolve().parents[1]
C=json.loads((R/'config.json').read_text(encoding='utf-8'))
OUT=R/'cards'; OUT.mkdir(exist_ok=True)
STATIC=os.environ.get('STATIC')=='1'
BG='#080A0B'; PANEL='#101415'; IVORY='#F1EEE5'; GOLD='#D7B54A'; CYAN='#19A9D1'; MUTED='#A3A39A'; LINE='#293034'
def e(s): return html.escape(str(s),quote=True)
def t(x,y,s,size=18,color=IVORY,weight=400,spacing=0,family='sans',extra=''):
    fam="'Arial Narrow',Impact,'DejaVu Sans',sans-serif" if family=='sans' else "'DejaVu Sans Mono',Consolas,monospace"
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}" fill="{color}" {extra}>{e(s)}</text>'
def r(x,y,w,h,fill=PANEL,stroke='none',rx=0,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" {extra}/>'
def path(d,color=CYAN,width=1,extra=''):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" {extra}/>'
def svg(name,w,h,body):
    css="""<style>
    .portrait-appear{animation:portrait-enter 1.6s ease-out both}.ascii-pixel{opacity:0;animation:pixel-in .45s steps(2,end) both}
    .hero-name{animation:name-rise 1.25s cubic-bezier(.16,1,.3,1) both}
    .reveal{animation:reveal 1.05s cubic-bezier(.2,.75,.2,1) both}
    .draw{stroke-dasharray:1000;stroke-dashoffset:1000;animation:draw 3.2s cubic-bezier(.3,.6,.3,1) forwards}
    .trace{stroke-dasharray:18 12;animation:trace 16s linear infinite}
    .cube{transform-box:fill-box;transform-origin:center;animation:cube-float 8s ease-in-out infinite alternate}
    .glow{animation:glow 4s ease-in-out infinite}.scan{animation:scan 4s ease-in-out infinite}.float{animation:float 6s ease-in-out infinite}
    .pulse{transform-box:fill-box;transform-origin:center;animation:pulse 3s ease-in-out infinite}
    @keyframes portrait-enter{from{opacity:0;filter:brightness(2)}to{opacity:.92;filter:brightness(1)}}
    @keyframes pixel-in{from{opacity:0;transform:translateY(-3px)}to{opacity:1;transform:translateY(0)}}
    @keyframes name-rise{from{opacity:0;transform:translateY(115px) skewY(3deg)}to{opacity:1;transform:translateY(0) skewY(0)}}
    @keyframes reveal{from{opacity:0;transform:translateY(26px)}to{opacity:1;transform:translateY(0)}}
    @keyframes draw{to{stroke-dashoffset:0}}@keyframes trace{to{stroke-dashoffset:-360}}
    @keyframes cube-float{0%{transform:translate(0,0) rotate(-3deg)}100%{transform:translate(8px,-17px) rotate(6deg)}}
    @keyframes pulse{50%{opacity:.25;transform:scale(2.8)}}
    @keyframes glow{50%{opacity:.3}}@keyframes scan{0%,100%{transform:translateY(0)}50%{transform:translateY(125px)}}@keyframes float{50%{transform:translateY(-7px)}}
    @media(prefers-reduced-motion:reduce){*{animation:none!important;stroke-dashoffset:0!important;opacity:1!important}}
    """+(' *{animation:none!important;stroke-dashoffset:0!important;opacity:1!important}' if STATIC else '')+'</style>'
    (OUT/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{e(name)}">{css}{body}</svg>',encoding='utf-8')
def grid(w,h,step=42):
    return ''.join(path(f'M{x} 0 V{h}',LINE,.55, 'opacity=".28"') for x in range(0,w,step))+''.join(path(f'M0 {y} H{w}',LINE,.55,'opacity=".28"') for y in range(0,h,step))
def header(w,label,num):
    return t(32,34,'MA  /  TITANIUMFEATHER',13,GOLD,700,2,'mono')+t(w-32,34,f'{label}   /   {num}',12,MUTED,500,1,'mono','text-anchor="end"')+path(f'M32 49 H{w-32}',LINE)
def ascii_portrait():
    """Crisp transparent portrait base + animated ASCII ink texture.

    Embedded PNG is self-contained in the SVG, so GitHub needs no external assets.
    Adjust portrait alpha/scale here; the photo is not placed in a rectangular card.
    """
    im = Image.open(R/'portrait-source.png').convert('RGBA')
    # Crop to head and shoulders, keeping the hair and jaw intact.
    w,h=im.size
    im=im.crop((int(w*.10),int(h*.015),int(w*.94),int(h*.91)))
    im.thumbnail((420,425),Image.Resampling.LANCZOS)
    pixels=im.load()
    for y in range(im.height):
        for x in range(im.width):
            rr,gg,bb,_=pixels[x,y]
            brightness=max(rr,gg,bb)
            # Remove the almost-black backdrop gradually, preserve dark hair details.
            alpha=max(0,min(255,int((brightness-12)*5)))
            pixels[x,y]=(rr,gg,bb,alpha)
    out=io.BytesIO();im.save(out,format='PNG',optimize=True)
    data=base64.b64encode(out.getvalue()).decode('ascii')
    # Keep the face legible even at 350px GitHub preview width.
    base=f'<image x="0" y="0" width="360" height="405" preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{data}" opacity=".92" class="portrait-appear"/>'
    # Lightweight glyph texture at the edges rather than solid blocks over the face.
    gray=ImageOps.grayscale(im).resize((43,45),Image.Resampling.LANCZOS)
    chars=' .·:+*#@'
    marks=[]
    for y in range(45):
        for x in range(43):
            val=gray.getpixel((x,y))
            if val<65 or val>215 or (x+y)%3:continue
            char=chars[min(len(chars)-1,int(val/256*len(chars)))]
            marks.append(f'<text x="{x*8.0+7:.1f}" y="{y*8.3+13:.1f}" fill="{GOLD if (x+y)%4==0 else IVORY}" font-family="monospace" font-size="8" opacity=".38" class="ascii-pixel" style="animation-delay:{.75+y*.023:.3f}s">{e(char)}</text>')
    return base+''.join(marks)

def cube(cx,cy,size,color,delay):
    """Three wireframe faces, separately animated with a slow perspective drift."""
    s=size; dx=s*.30; dy=-s*.22
    front=f'{cx},{cy} {cx+s},{cy} {cx+s},{cy+s} {cx},{cy+s}'
    top=f'{cx},{cy} {cx+dx},{cy+dy} {cx+s+dx},{cy+dy} {cx+s},{cy}'
    side=f'{cx+s},{cy} {cx+s+dx},{cy+dy} {cx+s+dx},{cy+s+dy} {cx+s},{cy+s}'
    return f'<g class="cube" style="animation-delay:{delay}s"><polygon points="{front}" fill="{color}" fill-opacity=".055" stroke="{color}" stroke-width="1.6"/><polygon points="{top}" fill="{color}" fill-opacity=".11" stroke="{color}" stroke-width="1.2"/><polygon points="{side}" fill="{color}" fill-opacity=".08" stroke="{color}" stroke-width="1.2"/></g>'

def hero():
    w,h=1200,525
    b=r(0,0,w,h,BG)+grid(w,h,58)+header(w,'PORTFOLIO 2026','00')
    b+='<defs><linearGradient id="goldSweep" x1="0" x2="1"><stop offset="0" stop-color="#F1EEE5"/><stop offset=".48" stop-color="#F1EEE5"/><stop offset=".52" stop-color="#D7B54A"/><stop offset=".57" stop-color="#F1EEE5"/><stop offset="1" stop-color="#F1EEE5"/></linearGradient><clipPath id="nameClip"><rect x="30" y="110" width="720" height="270"/></clipPath></defs>'
    b+=f'<g opacity=".33">{cube(770,205,104,CYAN,0)}{cube(1045,124,48,GOLD,1.2)}{cube(1115,365,60,CYAN,2.3)}{cube(690,382,45,GOLD,1.7)}</g>'
    b+=path('M710 360 Q865 60 1130 140 M730 440 Q900 505 1175 280',CYAN,1,'class="trace" opacity=".25"')
    b+=t(40,108,'SOFTWARE ENGINEER  /  CREATIVE BUILDER',14,GOLD,500,2,'mono')
    b+='<g clip-path="url(#nameClip)"><g class="hero-name" style="animation-delay:.12s">'+t(32,247,'MUHAMMED',111,'url(#goldSweep)',900,-5)+'</g>'
    b+='<g class="hero-name" style="animation-delay:.4s">'+t(32,368,'ADIL.',147,IVORY,900,-7)+'</g></g>'
    b+=t(40,449,'BUILDING WITH PRECISION.',18,MUTED,400,2,'mono')
    b+=t(40,478,'PROGRAMMING WITH PURPOSE.',18,MUTED,400,2,'mono')
    # Portrait is floating transparent ASCII, not a rectangular block.
    b+=f'<g transform="translate(790 73)">{ascii_portrait()}</g>'
    b+=path('M766 70 H792 M766 70 V98 M1173 70 H1145 M1173 70 V98 M766 485 H792 M766 485 V456 M1173 485 H1145 M1173 485 V456',CYAN,1.3,'opacity=".85"')
    b+=t(787,503,'FIG. 01 / HUMAN, NOT MACHINE',11,CYAN,500,1,'mono')
    b+='<circle cx="1144" cy="87" r="3" fill="'+GOLD+'" class="pulse"/>'
    svg('hero.svg',w,h,b)
def statement():
    w,h=1200,365
    b=r(0,0,w,h,BG)+header(w,'THE HUMAN ELEMENT','01')
    b+=t(40,120,'A little bit of',65,IVORY,800,-2)
    b+=t(40,201,'everything.',85,GOLD,800,-3)
    b+=t(43,273,'ALWAYS CURIOUS. ALWAYS BUILDING.',15,CYAN,600,1.5,'mono')
    b+=path('M645 83 V320',LINE,1)
    b+=t(680,111,"I'm Muhammed, a Computer Science student",21,IVORY)
    b+=t(680,143,'at the University of Toronto.',21,IVORY)
    b+=t(680,193,'Some days I build operating systems.',20,MUTED)
    b+=t(680,225,'Other days I experiment with AI,',20,MUTED)
    b+=t(680,257,'design interfaces, or take things apart',20,MUTED)
    b+=t(680,289,'just to understand how they work.',20,MUTED)
    b+=t(680,332,'SYSTEMS   /   INTELLIGENCE   /   DESIGN',12,GOLD,500,1.4,'mono')
    svg('about.svg',w,h,b)

def section():
    w,h=1200,146
    b=r(0,0,w,h,BG)+header(w,'SELECTED WORK','02')
    b+=t(36,117,'Ideas, made real.',66,IVORY,800,-2)
    b+=t(1163,111,'04 / BUILDS',14,GOLD,500,2,'mono','text-anchor="end"')
    svg('projects-heading.svg',w,h,b)
def art(i):
    if i==0:
        a=r(650,83,475,228,'#0B1519',CYAN,10)+r(666,103,443,29,'#15242B',rx=4)
        a+= ''.join(f'<circle cx="{x}" cy="117" r="4" fill="{c}"/>' for x,c in [(685,GOLD),(699,CYAN),(713,MUTED)])
        a+=r(666,146,105,150,'#10232B',rx=4)+r(784,146,325,150,'#11191B',rx=4)
        a+=t(803,176,'lunara / workspace',13,CYAN,500,0,'mono')
        for k in range(3):a+=r(806+k*93,196,77,72,'#18323B',CYAN if k==1 else LINE,4)
        a+=path('M841 196 V268 M806 231 H883',GOLD,1.5,'class="draw"')
        return a
    if i==1:
        a=r(704,68,338,255,'#0C171B',CYAN,14)+r(724,87,298,216,'#111C20',LINE,7)
        # schematic scan cross section
        for rad in [100,80,61,40]:a+=f'<ellipse cx="873" cy="196" rx="{rad}" ry="{rad*.85}" fill="none" stroke="{CYAN if rad%2==0 else GOLD}" stroke-width="1.3" opacity=".55"/>'
        a+=path('M873 110 V283 M762 196 H985',CYAN,1,'opacity=".6"')
        a+=path('M804 173 Q834 133 861 170 T931 160 Q967 192 927 232 T853 246 Q801 236 804 173',GOLD,2,'class="draw"')
        a+=r(724,125,298,2,CYAN,rx=1,extra='class="scan" opacity=".8"')
        a+=t(1065,113,'SCAN / 002',12,CYAN,400,1,'mono')
        return a
    if i==2:
        a=r(650,78,485,240,'#0C171B',LINE,9)
        for yy in range(116,293,40):a+=path(f'M674 {yy} H1111',LINE,.8)
        for xx in range(685,1111,55):a+=path(f'M{xx} 100 V293',LINE,.8)
        a+=path('M679 264 L723 250 L755 259 L789 201 L823 222 L858 184 L892 202 L930 135 L964 160 L1003 122 L1044 145 L1100 109',CYAN,3,'class="draw"')
        a+=path('M679 278 L723 272 L755 267 L789 249 L823 256 L858 236 L892 231 L930 215 L964 224 L1003 203 L1044 211 L1100 188',GOLD,1.7,'class="draw" opacity=".75"')
        a+=t(688,105,'SIGNAL / MARKET STRUCTURE',12,GOLD,400,1,'mono')
        return a
    a=r(670,74,445,245,'#0C171B',CYAN,9)+r(670,74,445,29,'#16272C',rx=9)
    a+=''.join(f'<circle cx="{x}" cy="89" r="4" fill="{c}"/>' for x,c in [(690,GOLD),(705,CYAN),(720,MUTED)])
    a+=r(690,120,405,83,'#17282C',rx=4)+r(707,141,186,12,IVORY,rx=3)+r(707,162,125,8,GOLD,rx=3)
    a+=r(690,218,122,81,'#12252C',rx=4)+r(823,218,122,81,'#172F37',rx=4)+r(956,218,139,81,'#12252C',rx=4)
    a+=path('M977 261 L1003 237 L1029 261 L1052 245 L1080 261',CYAN,2,'class="draw"')
    return a
def project(i,p):
    w,h=1200,365
    b=r(0,0,w,h,BG)+r(16,8,w-32,h-16,PANEL,LINE,12)
    b+=t(44,56,p['category'],13,GOLD,600,2,'mono')
    b+='<g class="reveal" style="animation-delay:.1s">'+t(42,135,p['name'],56,IVORY,800,-2)+'</g>'
    b+=t(45,186,p['description'],18,MUTED)
    b+=path('M45 225 H555',LINE,1)+t(45,265,p['stack'],13,CYAN,500,1,'mono')
    b+=t(45,321,'EXPLORE PROJECT  ↗',15,GOLD,600,1,'mono')
    b+='<g class="reveal" style="animation-delay:.35s">'+art(i)+'</g>'
    svg(f'project-{i+1}.svg',w,h,b)
def footer():
    w,h=1200,215
    b=r(0,0,w,h,BG)+header(w,'OPEN FOR WHAT COMES NEXT','03')
    b+=t(36,128,'Have something ambitious in mind?',48,IVORY,750,-1)
    b+=t(40,180,'LET’S BUILD IT.',17,GOLD,600,3,'mono')
    b+=t(1160,182,'PORTFOLIO  /  GITHUB',14,CYAN,500,1,'mono','text-anchor="end"')
    svg('footer.svg',w,h,b)
hero();statement();section()
for i,p in enumerate(C['projects']):project(i,p)
footer()
print('Generated 8 SVGs in cards/')
