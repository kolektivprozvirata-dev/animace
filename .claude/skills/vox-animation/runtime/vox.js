/*
 * vox.js — malý deterministický runtime pro animace ve stylu Vox.
 *
 * Scéna je obyčejné HTML. Veškerý pohyb se počítá z času `t` uvnitř
 * funkce předané do VOX.scene(). Žádné CSS animace / transitions —
 * renderer volá window.__render(t) snímek po snímku, takže výstup je
 * vždy stejný a dá se renderovat rychleji/pomaleji než realtime.
 *
 *   VOX.setup({ duration: 8 });
 *   VOX.scene((t, raw) => { ... nastav styly podle t ... });
 *
 * t   = čas kvantovaný na animFps (default 12 fps → "animace na dvojky")
 * raw = nekvantovaný čas (pro věci, které mají jet plynule)
 */
(function () {
  const cfg = {
    width: 1920,
    height: 1080,
    fps: 24,        // výstupní fps videa
    animFps: 12,    // fps grafiky – typický Vox "stutter"
    duration: 6,
    grain: 0.07,    // síla zrna přes celý obraz (0 = vypnuto)
    vignette: 0.18, // síla vinětace (0 = vypnuto)
    background: 'paper', // 'paper' | 'dark' | 'none'
  };

  // ---------- matematika & easing ----------
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, p) => a + (b - a) * p;
  const ease = {
    linear: (p) => p,
    outCubic: (p) => 1 - Math.pow(1 - p, 3),
    inCubic: (p) => p * p * p,
    inOutCubic: (p) => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2),
    outExpo: (p) => (p === 1 ? 1 : 1 - Math.pow(2, -10 * p)),
    inOutSine: (p) => -(Math.cos(Math.PI * p) - 1) / 2,
    outBack: (p, s = 1.70158) => 1 + (s + 1) * Math.pow(p - 1, 3) + s * Math.pow(p - 1, 2),
  };

  /** Průběh 0..1 mezi t0 a t0+dur s easingem. */
  function prog(t, t0, dur, e = ease.outCubic) {
    if (dur <= 0) return t >= t0 ? 1 : 0;
    return e(clamp((t - t0) / dur));
  }

  /** Průběh "tam a zpět": náběh v t0, odchod v t1. */
  function inOut(t, t0, t1, durIn = 0.4, durOut = 0.3, eIn = ease.outCubic, eOut = ease.inCubic) {
    return prog(t, t0, durIn, eIn) * (1 - prog(t, t1, durOut, eOut));
  }

  // ---------- deterministický random ----------
  function rng(seed) {
    let a = seed >>> 0;
    return function () {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      let r = Math.imul(a ^ (a >>> 15), 1 | a);
      r = (r + Math.imul(r ^ (r >>> 7), 61 | r)) ^ r;
      return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
    };
  }
  const hash = (s) => { let h = 2166136261; for (const c of String(s)) h = Math.imul(h ^ c.charCodeAt(0), 16777619); return h >>> 0; };

  /** Index animačního kroku (mění se animFps-krát za sekundu). */
  const step = (t) => Math.floor(t * cfg.animFps + 1e-6);

  // ---------- pomocníci pro elementy ----------
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  /**
   * Nastaví transform elementu. Všechny hodnoty volitelné.
   * {x, y, s, sx, sy, r, o, blur}
   */
  function set(el, { x = 0, y = 0, s = 1, sx, sy, r = 0, o, blur, origin } = {}) {
    if (typeof el === 'string') el = $(el);
    if (!el) return;
    const scx = sx ?? s, scy = sy ?? s;
    el.style.transform = `translate(${x}px, ${y}px) rotate(${r}deg) scale(${scx}, ${scy})`;
    if (origin) el.style.transformOrigin = origin;
    if (o !== undefined) {
      el.style.opacity = o;
      el.style.visibility = o <= 0.001 ? 'hidden' : 'visible';
    }
    if (blur !== undefined) el.style.filter = blur > 0.05 ? `blur(${blur}px)` : '';
  }

  /**
   * "Pop" – vyskočení z 0 % s malým překmitem (signature Vox pohyb).
   * Vrací scale. Délka default 0.33 s (= 4 kroky na dvojky).
   */
  function pop(t, t0, dur = 0.33, overshoot = 1.9) {
    return ease.outBack(clamp((t - t0) / dur), overshoot) * (t >= t0 ? 1 : 0);
  }

  /**
   * "Boil" – jemné chvění papírového výřezu, mění se každý animační krok.
   * Vrací {x, y, r}. amp v px, rot ve stupních.
   */
  function boil(t, seed = 1, amp = 1.2, rot = 0.25) {
    const R = rng(hash(seed) + step(t) * 7919);
    return { x: (R() * 2 - 1) * amp, y: (R() * 2 - 1) * amp, r: (R() * 2 - 1) * rot };
  }

  /** Zvýrazňovač přes text: element s třídou .hl, p = 0..1 */
  function highlight(el, p) {
    if (typeof el === 'string') el = $(el);
    if (el) el.style.setProperty('--hl', clamp(p).toFixed(4));
  }

  /** Kreslení SVG cesty (path/line/polyline/circle). p = 0..1 */
  function draw(el, p) {
    if (typeof el === 'string') el = $(el);
    if (!el) return;
    if (!el.__len) el.__len = el.getTotalLength();
    el.style.strokeDasharray = `${el.__len} ${el.__len}`;
    el.style.strokeDashoffset = `${el.__len * (1 - clamp(p))}`;
  }

  /** Psací stroj. Ukládá původní text do data-text. */
  function typeOn(el, p) {
    if (typeof el === 'string') el = $(el);
    if (!el) return;
    if (el.dataset.text === undefined) el.dataset.text = el.textContent;
    const full = el.dataset.text;
    el.textContent = full.slice(0, Math.round(full.length * clamp(p)));
  }

  /** Počítadlo čísla. fmt = (n) => string */
  function count(el, from, to, p, fmt = (n) => Math.round(n).toLocaleString('cs-CZ')) {
    if (typeof el === 'string') el = $(el);
    if (el) el.textContent = fmt(lerp(from, to, clamp(p)));
  }

  /**
   * Kamera nad elementem "world" – interpolace mezi klíči.
   * keys: [{t, x, y, s, r, e}]  (x/y = bod, na který se kamera dívá, v px světa)
   */
  function camera(el, t, keys) {
    if (typeof el === 'string') el = $(el);
    if (!el || !keys.length) return;
    let a = keys[0], b = keys[keys.length - 1];
    for (let i = 0; i < keys.length - 1; i++) {
      if (t >= keys[i].t && t <= keys[i + 1].t) { a = keys[i]; b = keys[i + 1]; break; }
    }
    const span = b.t - a.t;
    const p = span > 0 ? (b.e || ease.inOutCubic)(clamp((t - a.t) / span)) : (t < a.t ? 0 : 1);
    const g = (k, d) => lerp(a[k] ?? d, b[k] ?? d, p);
    const s = g('s', 1), x = g('x', cfg.width / 2), y = g('y', cfg.height / 2), r = g('r', 0);
    el.style.transformOrigin = '0 0';
    el.style.transform =
      `translate(${cfg.width / 2}px, ${cfg.height / 2}px) rotate(${r}deg) scale(${s}) translate(${-x}px, ${-y}px)`;
  }

  /**
   * Rozmazání přes střih (Vox "camera blur" přechod).
   * Vrací px blur: roste před cutT, vrchol ve střihu, rychle opadá.
   */
  function cutBlur(t, cutT, peak = 18, before = 0.25, after = 0.2) {
    if (t < cutT - before || t > cutT + after) return 0;
    if (t <= cutT) return peak * ease.inCubic(clamp((t - (cutT - before)) / before));
    return peak * (1 - ease.outCubic(clamp((t - cutT) / after)));
  }

  /** Pomalý "push-in" – Ken Burns. Vrací scale od s0 do s1 přes celý záběr. */
  const push = (t, t0, t1, s0 = 1, s1 = 1.06) => lerp(s0, s1, clamp((t - t0) / (t1 - t0)));

  /** Viditelnost záběru (shot) v čase. */
  const shot = (el, t, t0, t1) => {
    if (typeof el === 'string') el = $(el);
    if (el) el.style.display = t >= t0 && t < t1 ? '' : 'none';
    return t >= t0 && t < t1;
  };

  // ---------- textury & filtry ----------
  function injectFilters() {
    if ($('#vox-defs')) return;
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.id = 'vox-defs';
    svg.setAttribute('width', '0');
    svg.setAttribute('height', '0');
    svg.style.position = 'absolute';
    svg.innerHTML = `
      <defs>
        <!-- trhaný okraj papíru -->
        <filter id="vox-torn" x="-5%" y="-5%" width="110%" height="110%">
          <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="4" seed="3" result="n"/>
          <feDisplacementMap in="SourceGraphic" in2="n" scale="14" xChannelSelector="R" yChannelSelector="G"/>
        </filter>
        <!-- jemně roztřesená linka (ručně kreslený dojem) -->
        <filter id="vox-rough" x="-5%" y="-5%" width="110%" height="110%">
          <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="8" result="n"/>
          <feDisplacementMap in="SourceGraphic" in2="n" scale="4" xChannelSelector="R" yChannelSelector="G"/>
        </filter>
        <!-- zrno (seed se mění každý krok) -->
        <filter id="vox-grain-f" x="0" y="0" width="100%" height="100%">
          <feTurbulence id="vox-grain-turb" type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="1" stitchTiles="stitch"/>
          <feColorMatrix type="saturate" values="0"/>
        </filter>
        <!-- vlákna papíru (statické) -->
        <filter id="vox-paper-f" x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.55" numOctaves="3" seed="11"/>
          <feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.38  0 0 0 0 0.28  0 0 0 0.6 -0.22"/>
        </filter>
      </defs>`;
    document.body.prepend(svg);

    const stage = $('#stage') || document.body;
    if (cfg.background !== 'none' && !$('.vox-paper', stage)) {
      const paper = document.createElement('div');
      paper.className = 'vox-paper';
      if (cfg.background === 'dark') paper.classList.add('vox-paper--dark');
      paper.innerHTML = `<svg width="100%" height="100%"><rect width="100%" height="100%" filter="url(#vox-paper-f)"/></svg>`;
      stage.prepend(paper);
    }
    if (cfg.grain > 0 && !$('.vox-grain', stage)) {
      const g = document.createElement('div');
      g.className = 'vox-grain';
      g.style.opacity = cfg.grain;
      g.innerHTML = `<svg width="100%" height="100%"><rect width="100%" height="100%" filter="url(#vox-grain-f)"/></svg>`;
      stage.append(g);
    }
    if (cfg.vignette > 0 && !$('.vox-vignette', stage)) {
      const v = document.createElement('div');
      v.className = 'vox-vignette';
      v.style.opacity = cfg.vignette;
      stage.append(v);
    }
  }

  function updateGrain(t) {
    const turb = document.getElementById('vox-grain-turb');
    if (turb) turb.setAttribute('seed', String((step(t) % 97) + 1));
  }

  // ---------- registrace scény ----------
  function setup(opts = {}) {
    Object.assign(cfg, opts);
    window.__VOX_CONFIG = { ...cfg };
    const stage = $('#stage');
    if (stage) {
      stage.style.width = cfg.width + 'px';
      stage.style.height = cfg.height + 'px';
    }
    injectFilters();
  }

  function scene(fn) {
    window.__render = (rawT) => {
      const t = step(rawT) / cfg.animFps;
      updateGrain(t);
      fn(t, rawT);
    };
    // náhled v prohlížeči: ?t=2.5 zobrazí konkrétní čas, ?play přehraje
    const q = new URLSearchParams(location.search);
    const go = () => {
      if (q.has('play')) {
        const start = performance.now();
        const loop = () => {
          const tt = ((performance.now() - start) / 1000) % cfg.duration;
          window.__render(tt);
          requestAnimationFrame(loop);
        };
        loop();
      } else {
        window.__render(parseFloat(q.get('t') || '0'));
      }
    };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go);
    else go();
  }

  // ---------- voiceover & titulky ----------
  /** Segment voiceoveru podle id (z vo-timing.js generovaného scripts/tts.py). */
  function vo(id) {
    const segs = (window.VO && window.VO.segments) || [];
    const s = segs.find((x) => x.id === id);
    if (!s) throw new Error('VO segment nenalezen: ' + id);
    return s;
  }

  /**
   * Odhad času, kdy v segmentu zazní dané slovo (interpolace podle znaků
   * uvnitř titulkového kousku). Přesnost ~0.1–0.2 s – na nástupy grafiky stačí.
   */
  function wordT(id, word) {
    const s = vo(id);
    const w = word.toLowerCase();
    for (const c of s.chunks) {
      const plain = c.text.replace(/\*/g, '');
      const i = plain.toLowerCase().indexOf(w);
      if (i >= 0) return c.t0 + (c.t1 - c.t0) * (i / Math.max(1, plain.length));
    }
    console.warn('slovo nenalezeno v segmentu', id, word);
    return s.t0;
  }

  /**
   * Vypálené titulky. Vytvoří #vox-captions (pokud chybí) a ukáže aktuální
   * kousek textu. *slovo* = zvýraznění. Segmenty s cap:false se přeskočí.
   * opts: {y (střed v px), hold (s po konci segmentu), hide: [[t0,t1],...]}
   */
  function captions(t, opts = {}) {
    const segs = (window.VO && window.VO.segments) || [];
    let box = document.getElementById('vox-captions');
    if (!box) {
      box = document.createElement('div');
      box.id = 'vox-captions';
      ($('#stage') || document.body).append(box);
    }
    if (opts.y !== undefined) box.style.top = opts.y + 'px';
    const hold = opts.hold ?? 0.25;
    let cur = null, start = 0;
    for (const s of segs) {
      if (s.cap === false) continue;
      for (let i = 0; i < s.chunks.length; i++) {
        const c = s.chunks[i];
        const end = i < s.chunks.length - 1 ? s.chunks[i + 1].t0 : s.t1 + hold;
        if (t >= c.t0 && t < end) { cur = c; start = c.t0; }
      }
    }
    if (cur && (opts.hide || []).some(([a, b]) => t >= a && t < b)) cur = null;
    if (!cur) { box.style.visibility = 'hidden'; box.__txt = null; return; }
    if (box.__txt !== cur.text) {
      const html = cur.text.split(' ').map((w) =>
        /^\*.*\*[.,!?…:;]*$/.test(w) || /^\*[^*]+\*?$/.test(w)
          ? `<span class="cap-hl">${w.replace(/\*/g, '')}</span>` : w).join(' ');
      box.innerHTML = `<span class="cap">${html}</span>`;
      box.__txt = cur.text;
    }
    box.style.visibility = 'visible';
    const p = prog(t, start, 0.17, ease.outBack);
    box.style.transform = `translate(-50%, -50%) scale(${0.9 + 0.1 * p})`;
  }

  window.VOX = {
    cfg, setup, scene, ease, clamp, lerp, prog, inOut, rng, hash, step,
    $, $$, set, pop, boil, highlight, draw, typeOn, count, camera, cutBlur, push, shot, vo, wordT, captions,
  };
})();
