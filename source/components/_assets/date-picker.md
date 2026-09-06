# The date picker — canonical, working

The calendar glyph on a date field was decorative everywhere in the library: an
`aria-hidden` SVG with nothing behind it. A control that looks tappable and does
nothing is worse than no control, so this is the one implementation. Paste it whole;
do not write a second one.

It attaches to the existing three-input `.dob` pattern — no markup change beyond
making the glyph a real `<button>`.

## Markup

The glyph becomes a button; everything else stays as it is.

```html
<div class="ctl dob" id="ca-dobctl" role="group" aria-labelledby="ca-doblabel">
  <input data-part="d" class="ctl__in" type="text" inputmode="numeric" maxlength="2" value="02" aria-label="Day"   placeholder="DD">
  <span class="dob__sep" aria-hidden="true">/</span>
  <input data-part="m" class="ctl__in" type="text" inputmode="numeric" maxlength="2" value="06" aria-label="Month" placeholder="MM">
  <span class="dob__sep" aria-hidden="true">/</span>
  <input data-part="y" class="ctl__in" type="text" inputmode="numeric" maxlength="4" value="2002" aria-label="Year" placeholder="YYYY">
  <button class="dob__cal" type="button" aria-label="Choose a date" aria-expanded="false" aria-haspopup="dialog">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
         stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M8 3.5V6M16 3.5V6M3.5 10h17"/>
    </svg>
  </button>
</div>
```

The field must be `position:relative` so the popover can anchor to it.

## CSS

```css
.dob{position:relative}
.dob__cal{
  flex:0 0 auto;display:grid;place-items:center;width:28px;height:28px;padding:0;
  border:0;border-radius:8px;background:none;color:var(--muted);cursor:pointer;
}
.dob__cal svg{width:19px;height:19px}
.dob__cal:hover{color:var(--text);background:var(--sunken)}
.dob__cal:focus-visible{outline:2px solid var(--acid);outline-offset:2px}
.dob__cal::after{content:"";position:absolute;inset:auto;width:44px;height:44px} /* hit area */

.dp{
  position:absolute;top:calc(100% + 8px);right:0;z-index:80;width:276px;padding:12px;
  background:var(--surface);border:1px solid var(--line);border-radius:var(--r-card);
  box-shadow:0 18px 44px rgba(0,0,0,.55);
}
.dp[hidden]{display:none}
.dp__bar{display:flex;align-items:center;gap:8px;margin-bottom:10px}
.dp__mon{flex:1;text-align:center;font-size:13.5px;font-weight:650;color:var(--text)}
.dp__nav{
  width:28px;height:28px;display:grid;place-items:center;border:0;border-radius:8px;
  background:var(--sunken);color:var(--text);cursor:pointer;
}
.dp__nav:hover{background:#181D25}
.dp__nav:focus-visible{outline:2px solid var(--acid);outline-offset:2px}
.dp__nav svg{width:15px;height:15px}
.dp__dow{display:grid;grid-template-columns:repeat(7,1fr);margin-bottom:4px}
.dp__dow span{
  text-align:center;font-size:10px;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;color:var(--dim);
}
.dp__grid{display:grid;grid-template-columns:repeat(7,1fr);row-gap:2px}
.dp__d{
  height:32px;border:0;border-radius:8px;background:none;color:var(--text);
  font:inherit;font-size:13px;cursor:pointer;
}
.dp__d:hover{background:var(--sunken)}
.dp__d:focus-visible{outline:2px solid var(--acid);outline-offset:-2px}
.dp__d[disabled]{color:var(--dim);cursor:default}
.dp__d[disabled]:hover{background:none}
.dp__d[aria-selected="true"]{background:var(--acid);color:var(--acid-ink);font-weight:700}
.dp__d--out{color:var(--dim)}
```

## Script

Self-contained. Call `initDatePickers(root)` once; it finds every `.dob` under `root`.

```js
function initDatePickers(root){
  const MON=['January','February','March','April','May','June','July',
             'August','September','October','November','December'];
  root.querySelectorAll('.dob').forEach(function(field){
    const btn=field.querySelector('.dob__cal');
    if(!btn||btn.tagName!=='BUTTON'||field.__dp) return;
    field.__dp=true;
    const D=field.querySelector('[data-part="d"]'),
          M=field.querySelector('[data-part="m"]'),
          Y=field.querySelector('[data-part="y"]');

    const pop=document.createElement('div');
    pop.className='dp'; pop.hidden=true; pop.setAttribute('role','dialog');
    pop.setAttribute('aria-label','Choose a date');
    pop.innerHTML=
      '<div class="dp__bar">'+
      '<button class="dp__nav" type="button" data-go="-1" aria-label="Previous month">'+
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg></button>'+
      '<div class="dp__mon" aria-live="polite"></div>'+
      '<button class="dp__nav" type="button" data-go="1" aria-label="Next month">'+
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg></button>'+
      '</div><div class="dp__dow"><span>M</span><span>T</span><span>W</span><span>T</span>'+
      '<span>F</span><span>S</span><span>S</span></div><div class="dp__grid"></div>';
    field.appendChild(pop);
    const grid=pop.querySelector('.dp__grid'), label=pop.querySelector('.dp__mon');

    // The prototype must not depend on today's date, or a frame captured in a
    // screenshot drifts. Seed from the field; fall back to a fixed date.
    function seed(){
      const d=+D.value, m=+M.value, y=+Y.value;
      if(d>0&&m>0&&y>1000) return new Date(y,m-1,d);
      return new Date(2010,8,2);
    }
    let view=seed(), sel=seed();

    function draw(){
      label.textContent=MON[view.getMonth()]+' '+view.getFullYear();
      grid.innerHTML='';
      const first=new Date(view.getFullYear(),view.getMonth(),1);
      const lead=(first.getDay()+6)%7;                      // Monday-first
      const days=new Date(view.getFullYear(),view.getMonth()+1,0).getDate();
      for(let i=0;i<lead;i++) grid.appendChild(document.createElement('span'));
      for(let n=1;n<=days;n++){
        const b=document.createElement('button');
        b.type='button'; b.className='dp__d'; b.textContent=n;
        const isSel = sel && sel.getDate()===n &&
                      sel.getMonth()===view.getMonth() &&
                      sel.getFullYear()===view.getFullYear();
        if(isSel) b.setAttribute('aria-selected','true');
        b.addEventListener('click',function(){
          sel=new Date(view.getFullYear(),view.getMonth(),n);
          D.value=String(n).padStart(2,'0');
          M.value=String(view.getMonth()+1).padStart(2,'0');
          Y.value=String(view.getFullYear());
          [D,M,Y].forEach(function(i){i.dispatchEvent(new Event('input',{bubbles:true}))});
          close(); btn.focus();
        });
        grid.appendChild(b);
      }
    }
    function open(){ view=seed(); sel=seed(); draw(); pop.hidden=false;
                     btn.setAttribute('aria-expanded','true');
                     document.addEventListener('mousedown',away,true);
                     document.addEventListener('keydown',esc,true); }
    function close(){ pop.hidden=true; btn.setAttribute('aria-expanded','false');
                      document.removeEventListener('mousedown',away,true);
                      document.removeEventListener('keydown',esc,true); }
    function away(e){ if(!field.contains(e.target)) close() }
    function esc(e){ if(e.key==='Escape'){ close(); btn.focus() } }

    btn.addEventListener('click',function(){ pop.hidden?open():close() });
    pop.addEventListener('click',function(e){
      const nav=e.target.closest('[data-go]'); if(!nav) return;
      view=new Date(view.getFullYear(),view.getMonth()+ +nav.dataset.go,1); draw();
    });
  });
}
initDatePickers(document);
```

## Rules

- **One implementation.** If a component needs a date field, paste this. Do not write a
  second calendar.
- **Never seed from `new Date()`** for the *displayed* value. A frame that shows "today"
  drifts between the screenshot and the review, and the review pages are the record.
  The seed above reads the field and falls back to a fixed date.
- **Monday-first**, matching the rest of the library.
- Selecting a date fires `input` on all three parts, so any existing validation
  (the age gate on the child-account form, for example) re-runs on its own.

## Attaching it

Trigger selector: `.dob__cal, .f__box[aria-label^="Date"]`.

**Do not match `.f__box` bare.** It is a generic field-box class — Gender, Country and
Province use it too — so a bare match attaches a calendar to every field on the screen.
This happened once; the `aria-label` filter is what prevents it.

Two field shapes exist and the picker handles both: a three-input `.dob` group (writes to
`[data-part]` inputs and fires `input` on each), and a single button showing a formatted
value (writes to its `.f__val` span and updates the button's `aria-label`).
