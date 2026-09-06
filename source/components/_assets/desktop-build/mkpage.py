"""Build a desktop page from the war-room kit head + a body file.
usage: mkpage.py <body.html> <out.html> <title> <active-nav> <extra-css-file|->
Active nav: war|merits|backchat|alerts|profile|none
"""
import sys, re, pickle
ROOT = '/Users/mk/Documents/Sportsheist/02-DOCUMENTATION/Branding Designs/components/'
src = open(ROOT+'desktop-fan-war-room.html', encoding='utf-8').read()
body_f, out_f, title, active, css_f = sys.argv[1:6]
rail_f = sys.argv[6] if len(sys.argv) > 6 else '-'


head = src.split('<main class="page">')[0]
# retitle
head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head)
comp = out_f.split('/')[-1].replace('.html','')
head = re.sub(r'data-component="[^"]*"', f'data-component="{comp}"', head)
# strip the war-room provenance comment
head = re.sub(r'<!-- REBRANDED.*?-->', '<!-- REBRANDED — hand-authored against the Figma Desktop file; kit inherited from desktop-fan-war-room.html -->', head, flags=re.S)
# nav active state
nav_names = {'war':'War Room','merits':'Merits','backchat':'Backchat','alerts':'Alerts','profile':'Profile'}
head = head.replace(' rail__item--on', '')
if active in nav_names:
    label = nav_names[active]
    head = re.sub(r'class="rail__item" (href="#"><svg viewBox="0 0 24 24"><use href="#i-'+ {'war':'war','merits':'cup','backchat':'mic','alerts':'bell','profile':'user'}[active] +r'"/></svg>'+label+')', r'class="rail__item rail__item--on" \1', head)
if active == 'none':
    # remove the rail entirely
    head = re.sub(r'<aside class="rail">.*?</aside>', '', head, flags=re.S)
if rail_f != '-':
    rail = open(rail_f, encoding='utf-8').read()
    active_label = sys.argv[7] if len(sys.argv) > 7 else ''
    if active_label:
        rail = rail.replace(f'class="rail__item" href="#"><svg viewBox="0 0 24 24"><use href="#i-', 'class="rail__item" href="#"><svg viewBox="0 0 24 24"><use href="#i-')
        needle = '</svg>' + active_label + '</a>'
        i = rail.find(needle)
        if i != -1:
            j = rail.rfind('<a class="rail__item"', 0, i)
            if j != -1:
                rail = rail[:j] + rail[j:].replace('class="rail__item"', 'class="rail__item rail__item--on"', 1)
    head = re.sub(r'<aside class="rail">.*?</aside>', rail, head, flags=re.S)
    import pickle as _p2
    _s2 = _p2.load(open('/private/tmp/claude-501/-Users-mk-Documents-Sportsheist/ac9fa6d2-8833-4e57-a64e-d17d1c9259a5/scratchpad/figma/subs.pkl','rb'))
    for _k,_v in _s2.items(): head = head.replace(_k,_v)
# extra css
head = re.sub(r'\.hero__prop--war\{[^}]+\}', '', head)
if css_f != '-':
    extra = open(css_f, encoding='utf-8').read()
    import pickle as _p
    _subs = _p.load(open('/private/tmp/claude-501/-Users-mk-Documents-Sportsheist/ac9fa6d2-8833-4e57-a64e-d17d1c9259a5/scratchpad/figma/subs.pkl','rb'))
    for _k,_v in _subs.items(): extra = extra.replace(_k,_v)
    head = head.replace('@media (prefers-reduced-motion:reduce)', extra + '\n@media (prefers-reduced-motion:reduce)')

body = open(body_f, encoding='utf-8').read()
subs = pickle.load(open('/private/tmp/claude-501/-Users-mk-Documents-Sportsheist/ac9fa6d2-8833-4e57-a64e-d17d1c9259a5/scratchpad/figma/subs.pkl','rb'))
for k,v in subs.items():
    body = body.replace(k, v)

tail = '''
<script>
(function(){
  function fit(){
    var s = Math.min(1, document.documentElement.clientWidth / 1440);
    document.body.style.zoom = s;
  }
  fit(); addEventListener('resize', fit);
})();
</script>
</body>
</html>
'''
out = head + '<main class="page">\n' + body + '\n</main>\n' + tail
left = set(re.findall(r'__[A-Z_]+__', out))
open(out_f, 'w', encoding='utf-8').write(out)
print('wrote', out_f, len(out)//1024, 'KB', 'unresolved:', left or 'none')
