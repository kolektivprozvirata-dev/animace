/*
 * kpz-theme.js — vizuální styl KPZ pro Vox scény (doplněk ke kpz-theme.css).
 *
 *   VOX.setup({ ..., background: 'none' });
 *   KPZ.theme();                       // filtry + růžové zrnité pozadí
 *   layer.innerHTML = KPZ.bg('#0b3f43'); // stejná textura v jiné barvě (tmavé záběry)
 *   KPZ.blocks('.h1, .h2');            // text → bloky po řádcích (teal)
 *   el.innerHTML = KPZ.badge(170);     // kulaté černé logo
 *   el.innerHTML = KPZ.sticker('sprig'|'wheat'|'heart');   // linoryt nálepky
 *   <path filter="url(#kpz-brush)">    // tah štětcem (šipky, škrty)
 *
 * Vše je deterministické (pevné seedy), takže render je opakovatelný.
 */
(function () {
  const BASE = (document.currentScript && document.currentScript.src || '').replace(/[^/]*$/, '');
  const NAVY = '#17323d', CREAM = '#efe4dd', RASP = '#d9465f', MAROON = '#920637';

  const FILTERS = `
    <!-- tiskový grunge na bloky textu: lehce roztřepené hrany + vybledlá místa -->
    <filter id="kpz-print" x="-4%" y="-10%" width="108%" height="120%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="4" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="4" xChannelSelector="R" yChannelSelector="G" result="d"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.32" numOctaves="2" seed="9" result="g"/>
      <feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -10 0 0 0 7.2" result="m"/>
      <feComponentTransfer in="m" result="m2"><feFuncA type="linear" slope="0.5" intercept="0.5"/></feComponentTransfer>
      <feComposite in="d" in2="m2" operator="in"/>
    </filter>
    <filter id="kpz-print-soft" x="-4%" y="-10%" width="108%" height="120%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="6" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="2.5" xChannelSelector="R" yChannelSelector="G" result="d"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.35" numOctaves="2" seed="12" result="g"/>
      <feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -10 0 0 0 7.4" result="m"/>
      <feComponentTransfer in="m" result="m2"><feFuncA type="linear" slope="0.3" intercept="0.7"/></feComponentTransfer>
      <feComposite in="d" in2="m2" operator="in"/>
    </filter>
    <!-- tah štětcem: roztřepený okraj + suché pruhy -->
    <filter id="kpz-brush" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="3" seed="2" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="9" xChannelSelector="R" yChannelSelector="G" result="d"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.004 0.16" numOctaves="2" seed="7" result="s"/>
      <feColorMatrix in="s" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -9 0 0 0 6.6" result="m"/>
      <feComposite in="d" in2="m" operator="in"/>
    </filter>
    <!-- linoryt: zrnité vybrání barvy -->
    <filter id="kpz-lino" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.5" numOctaves="2" seed="15" result="g"/>
      <feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -12 0 0 0 8.3" result="m"/>
      <feComposite in="SourceGraphic" in2="m" operator="in"/>
    </filter>`;

  // pozadí: růžový papír – skvrny, vlákna, zrnka (filtry jsou v #kpz-defs)
  const BG_DEFS = `
        <filter id="kpz-bg-light" x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.0032" numOctaves="5" seed="17"/>
          <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 0.86  0 0 0 0 0.88  3.2 0 0 0 -1.55"/>
        </filter>
        <filter id="kpz-bg-dark" x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.005" numOctaves="5" seed="5"/>
          <feColorMatrix type="matrix" values="0 0 0 0 0.62  0 0 0 0 0.12  0 0 0 0 0.2  0 3.4 0 0 -1.7"/>
        </filter>
        <filter id="kpz-bg-fiber" x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.25 0.04" numOctaves="3" seed="8"/>
          <feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.05  0 0 0 0 0.15  0 0 4 0 -2.25"/>
        </filter>
        <filter id="kpz-bg-speck" x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="2" seed="3"/>
          <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 0.93  0 0 0 0 0.93  16 0 0 0 -11"/>
        </filter>
        <filter id="kpz-bg-dot" x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="2" seed="23"/>
          <feColorMatrix type="matrix" values="0 0 0 0 0.35  0 0 0 0 0.02  0 0 0 0 0.1  0 16 0 0 -11"/>
        </filter>
        <radialGradient id="kpz-bg-vig" cx="50%" cy="42%" r="75%">
          <stop offset="55%" stop-color="#5a0a22" stop-opacity="0"/>
          <stop offset="100%" stop-color="#5a0a22" stop-opacity=".28"/>
        </radialGradient>`;
  const bgLayers = (color) => `
      <rect width="100%" height="100%" fill="${color}"/>
      <rect width="100%" height="100%" filter="url(#kpz-bg-light)" opacity=".22"/>
      <rect width="100%" height="100%" filter="url(#kpz-bg-dark)" opacity=".18"/>
      <rect width="100%" height="100%" filter="url(#kpz-bg-fiber)" opacity=".22"/>
      <rect width="100%" height="100%" filter="url(#kpz-bg-speck)" opacity=".45"/>
      <rect width="100%" height="100%" filter="url(#kpz-bg-dot)" opacity=".4"/>
      <rect width="100%" height="100%" fill="url(#kpz-bg-vig)"/>`;
  /** Pozadí: SVG s filtry se jednou vykreslí do <canvas> (bitmapa), aby render nezdržovalo
   *  přepočítávání filtrů na celé ploše v každém snímku. Do načtení je vidět stejný obrázek
   *  jako <img>. Barva musí být hex (uvnitř obrázku nejsou CSS proměnné). */
  const bgHTML = (color = '#e05d73') => {
    const st = document.getElementById('stage');
    const w = (st && st.offsetWidth) || 1080, h = (st && st.offsetHeight) || 1920;
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}"><defs>${BG_DEFS}</defs>${bgLayers(color)}</svg>`;
    const id = 'kpzbg' + (bgN++);
    const url = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
    const img = new Image();
    img.onload = () => {
      const cv = document.getElementById(id);
      if (!cv) return;
      cv.getContext('2d').drawImage(img, 0, 0, w, h);
      cv.style.visibility = 'visible';
      const im = cv.previousElementSibling; if (im) im.remove();
    };
    img.src = url;
    const css = 'position:absolute; inset:0; width:100%; height:100%';
    return `<img alt="" style="${css}; background:${color}" src="${url}"><canvas id="${id}" width="${w}" height="${h}" style="${css}; visibility:hidden"></canvas>`;
  };
  let bgN = 0;

  /** Filtry + pozadí. opts.bg = barva pozadí (výchozí růžová). */
  function theme(opts = {}) {
    document.body.classList.add('kpz');
    if (!document.getElementById('kpz-defs')) {
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.id = 'kpz-defs';
      svg.setAttribute('width', '0'); svg.setAttribute('height', '0');
      svg.style.position = 'absolute';
      svg.innerHTML = `<defs>${FILTERS}</defs>`;
      document.body.prepend(svg);
    }
    const stage = document.getElementById('stage');
    if (stage && !stage.querySelector(':scope > .kpz-bg')) {
      const bg = document.createElement('div');
      bg.className = 'kpz-bg';
      bg.innerHTML = bgHTML(opts.bg || '#e05d73');
      stage.prepend(bg);
    }
  }

  /** Texturované pozadí do libovolné vrstvy: el.innerHTML = KPZ.bg('#0b3f43') */
  const bg = (color = '#e05d73') => bgHTML(color);

  /** Obsah prvků zabalí do inline bloku – každý řádek dostane vlastní plný blok. */
  function blocks(sel, cls = '') {
    document.querySelectorAll(sel).forEach((el) => {
      if (el.dataset.kb) return;
      el.dataset.kb = '1';
      el.classList.add('kblocks');
      el.innerHTML = `<span class="kb ${cls}">${el.innerHTML}</span>`;
    });
  }

  /** Text bloku pro šablonu: KPZ.kb('Text', 'cream') */
  const kb = (txt, cls = '') => `<span class="kb ${cls}">${txt}</span>`;

  /** Kulaté černé logo (jako na grafice KPZ). */
  const badge = (size = 170) =>
    `<div class="kpz-badge" style="width:${size}px; height:${size}px"><img src="${BASE}logo-kpz-tmave.png" alt=""><span>KOLEKTIV<br>PRO ZVÍŘATA</span></div>`;

  // ---------- linoryt nálepky ----------
  /** list podél osy (0,0)→(L,0), šířka W; světlá středová žilka (rytá linka) */
  const leaf = (x, y, L, W, rot, fill = NAVY, vein = CREAM, veins = true) =>
    `<g transform="translate(${x} ${y}) rotate(${rot})">
      <path d="M0,0 C${L * 0.22},${-W * 1.1} ${L * 0.72},${-W} ${L},0 C${L * 0.72},${W} ${L * 0.22},${W * 1.1} 0,0 Z" fill="${fill}"/>
      ${veins ? `<path d="M${L * 0.14},0 C${L * 0.4},${-W * 0.08} ${L * 0.6},${-W * 0.08} ${L * 0.82},0" fill="none" stroke="${vein}" stroke-width="${Math.max(2, W * 0.12)}" stroke-linecap="round"/>
      ${[0.34, 0.56].map((f) => `<path d="M${L * f},${-W * 0.04} q${L * 0.08},${-W * 0.3} ${L * 0.16},${-W * 0.5} M${L * (f + 0.08)},${W * 0.04} q${L * 0.08},${W * 0.3} ${L * 0.16},${W * 0.46}" fill="none" stroke="${vein}" stroke-width="${Math.max(1.5, W * 0.08)}" stroke-linecap="round"/>`).join('')}` : ''}
    </g>`;

  const STICKERS = {
    // olivová snítka
    sprig: () => {
      let s = `<path d="M18,186 C70,150 122,104 192,34" fill="none" stroke="${NAVY}" stroke-width="7" stroke-linecap="round"/>`;
      [[48, 163, -150, 1], [70, 147, -62, 1], [100, 123, -140, 0.95], [118, 106, -52, 0.92], [150, 80, -128, 0.85], [166, 62, -45, 0.8], [190, 36, -48, 0.6]]
        .forEach(([x, y, r, k]) => { s += leaf(x, y, 78 * k, 22 * k, r); });
      return `<svg viewBox="0 0 210 210" width="100%" overflow="visible"><g filter="url(#kpz-lino)">${s}</g></svg>`;
    },
    // tři klasy na dvou listech
    wheat: () => {
      let s = leaf(98, 196, 120, 34, -150) + leaf(112, 196, 120, 34, -30);
      const ear = (x0, y0, x1, y1) => {
        const ang = Math.atan2(y1 - y0, x1 - x0) * 180 / Math.PI, len = Math.hypot(x1 - x0, y1 - y0);
        let e = `<g transform="translate(${x0} ${y0}) rotate(${ang})"><path d="M0,0 L${len},0" stroke="${NAVY}" stroke-width="6" stroke-linecap="round"/>`;
        for (let i = 0; i < 6; i++) {
          const x = len * (0.42 + i * 0.1);
          e += `<ellipse cx="${x}" cy="-9" rx="12" ry="7" transform="rotate(-24 ${x} -9)" fill="${NAVY}"/><ellipse cx="${x}" cy="9" rx="12" ry="7" transform="rotate(24 ${x} 9)" fill="${NAVY}"/>`;
          e += `<path d="M${x - 6},-8 l9,-3 M${x - 6},8 l9,3" stroke="${CREAM}" stroke-width="2.4" stroke-linecap="round"/>`;
        }
        return e + `<ellipse cx="${len + 4}" cy="0" rx="12" ry="7" fill="${NAVY}"/></g>`;
      };
      s += ear(100, 190, 52, 40) + ear(105, 190, 108, 20) + ear(110, 190, 162, 40);
      return `<svg viewBox="0 0 210 210" width="100%" overflow="visible"><g filter="url(#kpz-lino)">${s}</g></svg>`;
    },
    // srdce na dvou listech
    heart: () => {
      let s = leaf(104, 176, 132, 44, -140) + leaf(104, 176, 132, 44, -40);
      s += `<path d="M104,182 C44,134 36,94 58,72 C78,54 98,62 104,84 C110,62 130,54 150,72 C172,94 164,134 104,182 Z" fill="${RASP}"/>
            <path d="M68,90 C74,78 84,76 92,80 M70,114 C68,106 68,100 70,96" fill="none" stroke="${CREAM}" stroke-width="5" stroke-linecap="round"/>`;
      return `<svg viewBox="0 0 210 210" width="100%" overflow="visible"><g filter="url(#kpz-lino)">${s}</g></svg>`;
    },
  };
  const sticker = (name) => STICKERS[name]();

  window.KPZ = { theme, bg, blocks, kb, badge, sticker, colors: { NAVY, CREAM, RASP, MAROON } };
})();
