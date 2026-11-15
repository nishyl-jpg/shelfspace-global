"""One-off restyle: applies the moonlit night art direction to the three sites.
Run once from the repo root: python3 tests/night_theme.py"""
import random, re

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600'
         '&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">')
DISPLAY = '"Cormorant Garamond",Georgia,serif'


def stars(n, w, h, seed):
    r = random.Random(seed)
    return ''.join(f'<circle cx="{r.randint(0, w)}" cy="{r.randint(0, h)}" r="{r.choice([.6, .8, 1, 1.4])}" opacity="{r.choice([.4, .6, .9])}"/>'
                   for _ in range(n))


def candles(rows):
    out = ''
    for x, y, s in rows:
        out += f'<circle cx="{x}" cy="{y}" r="{5 * s:.1f}" fill="#ff8a2b" opacity=".35"/><circle cx="{x}" cy="{y}" r="{1.8 * s:.1f}" fill="#ffe2a8"/>'
    return out


DEFS = '''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#04061c"/><stop offset=".55" stop-color="#16228f"/><stop offset="1" stop-color="#4a34a8"/></linearGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#cfd4ff" stop-opacity=".55"/><stop offset="1" stop-color="#cfd4ff" stop-opacity="0"/></radialGradient>
<radialGradient id="amber"><stop offset="0" stop-color="#ffe0a0"/><stop offset=".7" stop-color="#ff9a3d"/><stop offset="1" stop-color="#e2581c"/></radialGradient>
<radialGradient id="ahalo"><stop offset="0" stop-color="#ff9a3d" stop-opacity=".5"/><stop offset="1" stop-color="#ff9a3d" stop-opacity="0"/></radialGradient>
<linearGradient id="drape" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset="1" stop-color="#c9cdf5" stop-opacity=".35"/></linearGradient>
<linearGradient id="fall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#cfd4ff" stop-opacity="0"/></linearGradient>
</defs>'''

# Mooimaak: a pointed arch looking onto a candlelit pool, crescent moon, white drapes.
r = random.Random(7)
pool = [(260 + side * (30 + i * 17) + r.randint(-6, 6), 372 + i * 15 + r.randint(-3, 3), .6 + i * .09) for i in range(11) for side in (-1, 1)]
pool += [(260 + side * (70 + i * 19) + r.randint(-8, 8), 400 + i * 13, .7 + i * .08) for i in range(9) for side in (-1, 1)]
MOOI = f'''<svg class="scene" viewBox="0 0 520 560" role="img" aria-label="A moonlit arch with white drapes over a candlelit pool">{DEFS}
<clipPath id="arch"><path d="M40 560V250Q60 70 260 10Q460 70 480 250V560Z"/></clipPath>
<g clip-path="url(#arch)"><rect width="520" height="560" fill="url(#sky)"/><g fill="#fff">{stars(70, 520, 330, 3)}</g>
<circle cx="260" cy="128" r="90" fill="url(#halo)"/>
<mask id="cres"><rect width="520" height="560" fill="#000"/><circle cx="260" cy="128" r="46" fill="#fff"/><circle cx="282" cy="114" r="42" fill="#000"/></mask>
<rect width="520" height="560" fill="#f3f0ff" mask="url(#cres)"/>
<path d="M205 360V292Q208 232 260 214Q312 232 315 292V360Z" fill="#2f43e0" opacity=".55"/><path d="M228 360V300Q230 262 260 250Q290 262 292 300V360Z" fill="#8fa0ff" opacity=".5"/>
<rect y="356" width="520" height="204" fill="#04061c" opacity=".82"/>
<path d="M40 60C190 230 170 400 96 560H40Z" fill="url(#drape)"/><path d="M40 120C140 260 130 410 70 560H40Z" fill="#fff" opacity=".35"/>
<path d="M480 60C330 230 350 400 424 560H480Z" fill="url(#drape)"/><path d="M480 120C380 260 390 410 450 560H480Z" fill="#fff" opacity=".35"/>
{candles(pool)}</g>
<path d="M40 560V250Q60 70 260 10Q460 70 480 250V560" fill="none" stroke="#ffb347" stroke-width="2" opacity=".7"/>
<path d="M28 560V248Q50 56 260 -4Q470 56 492 248V560" fill="none" stroke="#2a3176" stroke-width="6"/></svg>'''

# Groengeld: floating gardens with waterfalls above the clouds, pale full moon.
def island(x, y, w, seed):
    r = random.Random(seed)
    trees = ''.join(f'<rect x="{x + dx - 3}" y="{y - 26}" width="6" height="28" fill="#06140f"/><circle cx="{x + dx}" cy="{y - 40 - r.randint(0, 10)}" r="{r.randint(20, 30)}" fill="#12583a"/>'
                    f'<circle cx="{x + dx - 14}" cy="{y - 30}" r="16" fill="#0d4028"/><circle cx="{x + dx + 15}" cy="{y - 32}" r="17" fill="#17704a"/>'
                    for dx in (-w * .45, w * .1, w * .5))
    lights = candles([(x + r.randint(int(-w * .8), int(w * .8)), y - r.randint(2, 10), .7) for _ in range(9)])
    falls = ''.join(f'<rect x="{x + dx}" y="{y + 4}" width="{ww}" height="{r.randint(120, 170)}" fill="url(#fall)"/>' for dx, ww in ((-w * .7, 7), (w * .25, 10), (w * .62, 5)))
    return (f'{falls}<path d="M{x - w} {y}Q{x - w * .6} {y + 70} {x - w * .1} {y + 120}Q{x + w * .5} {y + 70} {x + w} {y}Z" fill="#07130f"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="13" fill="#0f4a30"/>{trees}{lights}')
r = random.Random(11)
clouds = ''.join(f'<ellipse cx="{r.randint(-20, 540)}" cy="{r.randint(430, 520)}" rx="{r.randint(60, 120)}" ry="{r.randint(22, 40)}" fill="#b9b4ee" opacity="{r.choice([.35, .5, .7])}"/>' for _ in range(16))
GROEN = f'''<svg class="scene" viewBox="0 0 520 520" role="img" aria-label="Gardens floating above moonlit clouds, with waterfalls">{DEFS}
<clipPath id="frame"><rect width="520" height="520" rx="28"/></clipPath>
<g clip-path="url(#frame)"><rect width="520" height="520" fill="url(#sky)"/><g fill="#fff">{stars(90, 520, 300, 5)}</g>
<circle cx="396" cy="92" r="84" fill="url(#halo)"/><circle cx="396" cy="92" r="34" fill="#f3f0ff"/>
{island(350, 250, 120, 2)}<path d="M150 318Q200 268 250 262" fill="none" stroke="#06140f" stroke-width="5"/>{island(140, 330, 100, 4)}
{clouds}</g><rect x="1" y="1" width="518" height="518" rx="27" fill="none" stroke="#ffb347" stroke-width="2" opacity=".6"/></svg>'''

# Ship in a Bottle: an amber moon over a lit harbour city, a ship, and three glowing drinks.
r = random.Random(21)
def tower(x, w, h, dome=False):
    top = 400 - h
    cap = f'<path d="M{x} {top}Q{x + w / 2} {top - w * .9} {x + w} {top}Z" fill="#04061c"/>' if dome else f'<path d="M{x} {top}L{x + w / 2} {top - w * 1.6}L{x + w} {top}Z" fill="#04061c"/>'
    win = ''.join(f'<rect x="{x + 4 + i * 7}" y="{top + 10 + j * 13}" width="2.5" height="5" fill="#ffb347" opacity="{r.choice([0, .5, .9, .9])}"/>'
                  for i in range(int((w - 6) // 7)) for j in range(int((h - 14) // 13)))
    return f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="#04061c"/>{cap}{win}'
city = ''.join([tower(20, 34, 150), tower(64, 60, 90, True), tower(134, 26, 210), tower(170, 44, 120), tower(330, 40, 130), tower(378, 30, 230), tower(416, 70, 100, True), tower(490, 30, 160)])
refl = ''.join(f'<ellipse cx="260" cy="{412 + i * 12}" rx="{46 - i * 4}" ry="2.5" fill="#ff9a3d" opacity="{.7 - i * .07:.2f}"/>' for i in range(8))
def orb(x, y, rad, c):
    return (f'<circle cx="{x}" cy="{y}" r="{rad * 1.7}" fill="{c}" opacity=".18"/><rect x="{x - rad * .3}" y="{y - rad - 8}" width="{rad * .6}" height="12" rx="3" fill="#e9ecff"/>'
            f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{c}"/><ellipse cx="{x - rad * .35}" cy="{y - rad * .4}" rx="{rad * .28}" ry="{rad * .18}" fill="#fff" opacity=".55"/>')
SHIP = f'''<svg class="scene" viewBox="0 0 520 520" role="img" aria-label="An amber moon over a lit harbour city, a ship on the water, and three glowing cocktails">{DEFS}
<clipPath id="frame"><rect width="520" height="520" rx="28"/></clipPath>
<g clip-path="url(#frame)"><rect width="520" height="520" fill="url(#sky)"/><g fill="#fff">{stars(80, 520, 260, 9)}</g>
<circle cx="260" cy="118" r="120" fill="url(#ahalo)"/><circle cx="260" cy="118" r="50" fill="url(#amber)"/>
<g fill="#2536b8" opacity=".75"><ellipse cx="150" cy="176" rx="150" ry="20"/><ellipse cx="380" cy="186" rx="170" ry="22"/><ellipse cx="260" cy="200" rx="260" ry="18"/></g>
{city}<rect y="400" width="520" height="120" fill="#04061c"/>{refl}
<path d="M226 404h70l-10 14h-50z" fill="#000"/><path d="M262 360v44M262 364l26 36h-26z" stroke="#e9ecff" stroke-width="2" fill="#e9ecff"/>
{orb(110, 452, 34, '#3fbf7a')}{orb(260, 468, 30, '#ff5a36')}{orb(410, 452, 34, '#ffb347')}</g>
<rect x="1" y="1" width="518" height="518" rx="27" fill="none" stroke="#ffb347" stroke-width="2" opacity=".6"/></svg>'''

COMMON = f'''
/* ===== Moonlit night art direction ===== */
:root{{color-scheme:dark}}
body{{background:var(--night);color:var(--ink)}}
h1,h2,h3{{font-family:{DISPLAY};letter-spacing:0;font-weight:700}}
.eyebrow,.logo{{font-family:Cinzel,Georgia,serif;letter-spacing:.14em}}
.logo{{font-size:19px;font-weight:700;text-transform:uppercase}}
.scene{{display:block;width:100%;max-width:460px;height:auto;margin:0 auto;filter:drop-shadow(0 20px 50px #000a)}}
select,input,textarea,input.txt{{background:#0a0f38;color:var(--ink);border:1px solid #3a4296}}
::placeholder{{color:#7d83b8}}
details p,.fine{{color:var(--muted)}}
'''

SITES = {
    'mooimaak': dict(
        root=':root{--night:#070a24;--clay:#c7283f;--clay-dark:#ff9d7a;--cream:#070a24;--sand:#0d1238;--ink:#efeaff;--muted:#a9add6;--sage:#ffb347;--blush:#ffb347;--card:#131949;--line:#2a3176}',
        art=(r'<div class="collage" aria-hidden="true">.*?</div>\s*</div>\s*</div>\s*\n\s*<section class="alt" id="services">', MOOI + '\n  </div>\n</div>\n\n<section class="alt" id="services">'),
        css='''
header.top{background:rgba(7,10,36,.92)}
.hero{background:radial-gradient(900px 500px at 80% 0,#1a2aa8 0,transparent 60%),var(--night)}
.hero h1{font-size:clamp(44px,8vw,78px)}
.hero h1 em{color:var(--sage)}
.btn{box-shadow:0 0 24px #c7283f66}
.btn:hover{background:#e0364f}
.btn.ghost{color:#ffd9a0;box-shadow:inset 0 0 0 2px var(--sage)}
.tabs button{color:#ffd9a0;border-color:var(--sage)}
.tabs button[aria-selected="true"]{background:var(--sage);color:#1a1030}
.price{color:var(--sage)}
.steps li::before{color:#1a1030}
.card.pick{box-shadow:0 0 40px #c7283f44}
.shot{border-radius:999px 999px 14px 14px;border:1px solid #ffb34766;background-image:radial-gradient(circle at 50% 28%,#f3f0ff 0 9%,transparent 10%),linear-gradient(180deg,#04061c,#16228f 60%,#4a34a8)!important;padding-bottom:16px;justify-content:center;text-align:center}
.shot:nth-child(even){background-image:radial-gradient(circle at 50% 28%,#ffb347 0 9%,transparent 10%),linear-gradient(180deg,#04061c,#1b1670 60%,#7a2340)!important}
footer{background:#03051a;color:var(--muted)}
'''),
    'groengeld': dict(
        root=':root{--night:#070a24;--green:#5fd08a;--green-dark:#03051a;--leaf:#7fe0a6;--gold:#ffb347;--cream:#070a24;--paper:#0d1238;--ink:#efeaff;--muted:#a9add6;--line:#2a3176;--tomato:#c8412d}',
        art=(r'(<div class="hero">\s*<div class="wrap">)(.*?)(</ul>\s*)(</div>\s*</div>\s*\n\s*<section id="order">)',
             lambda m: m.group(1) + '<div>' + m.group(2) + m.group(3) + '</div>' + GROEN + m.group(4)),
        css='''
.hero{background:radial-gradient(900px 500px at 85% 0,#1a2aa8 0,transparent 60%),var(--night)}
.hero::before,.hero::after{display:none}
.hero .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:28px;align-items:center}
@media(max-width:860px){.hero .wrap{grid-template-columns:1fr}}
.hero h1{font-size:clamp(42px,7.5vw,72px)}
.facts{grid-template-columns:repeat(auto-fit,minmax(130px,1fr))}
.facts b{font-family:"Cormorant Garamond",Georgia,serif;font-size:24px;color:var(--gold)}
.btn{color:#1a1030;box-shadow:0 0 24px #ffb34755}
.btn.green{color:#04121a}
.btn.ghost{color:#fff}
.btn[aria-disabled="true"]{background:#232a66;color:#7d83b8;box-shadow:none}
.switch{background:#131949}
.switch button{color:var(--ink)}
.switch button[aria-pressed="true"],.days input:checked+span{color:#04121a}
.items,.summary,.steps li,.panel,details{background:#131949;border-color:var(--line)}
.summary{border-color:var(--green);box-shadow:0 0 40px #5fd08a22}
.group{background:#0d1238;color:var(--leaf)}
.item{border-top-color:#232a66}
.step button{background:#0a0f38;border-color:#3a4296}
.step button:hover{background:#1b2260}
.days span{border-color:#3a4296}
.tot b,.steps li::before{font-family:"Cormorant Garamond",Georgia,serif}
.steps li::before{color:#1a1030;font-size:20px}
.areas li{background:#131949;color:var(--leaf);border:1px solid var(--line)}
footer{color:var(--muted)}
'''),
    'ship-in-a-bottle': dict(
        root=':root{--night:#070a24;--navy:#0b1040;--deep:#03051a;--sea:#9fb0ff;--coral:#ff5a36;--sun:#ffb347;--foam:#070a24;--ink:#efeaff;--muted:#a9add6;--line:#2a3176}',
        art=(r'<div class="art" aria-hidden="true">.*?</div>\s*</div>\s*<svg class="waves".*?</svg>', SHIP + '\n  </div>'),
        css='''
h1,h2,h3{font-weight:700}
#gate{background:radial-gradient(700px 500px at 50% 0,#1a2aa8 0,transparent 65%),var(--deep)}
.hero{background:radial-gradient(900px 500px at 85% 0,#1a2aa8 0,transparent 60%),var(--night);padding-bottom:56px}
.hero h1{font-size:clamp(44px,8vw,78px)}
.btn{box-shadow:0 0 24px #ff5a3655}
.btn.sun{color:#1a1030;box-shadow:0 0 24px #ffb34755}
section.alt{background:#0d1238}
.fl,.rules li,details,section.alt details,.panel,section:not(.alt) .panel{background:#131949;border-color:var(--line)}
.rules b{color:var(--sun)}
.pack{border:1px solid var(--line)}
.pack.hot{border-color:transparent;box-shadow:0 0 40px #ff5a3655}
.pack .price{font-family:"Cormorant Garamond",Georgia,serif;font-size:44px}
.resp{color:#1a1030}
.logo{font-size:15px}
'''),
}

for site, cfg in SITES.items():
    path = f'{site}/index.html'
    s = open(path).read()
    assert 'Moonlit night' not in s, f'{site} already restyled'
    s, n = re.subn(r'<link href="https://fonts\.googleapis\.com/css2[^>]*>', FONTS, s); assert n == 1, (site, 'font')
    s, n = re.subn(r':root\{[^}]*\}', cfg['root'], s, count=1); assert n == 1, (site, 'root')
    s, n = re.subn(cfg['art'][0], cfg['art'][1], s, count=1, flags=re.S); assert n == 1, (site, 'art')
    s = s.replace('</style>', COMMON + cfg['css'] + '</style>', 1)
    open(path, 'w').write(s)
    print('restyled', site)
