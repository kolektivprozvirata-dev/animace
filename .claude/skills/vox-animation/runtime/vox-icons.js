/*
 * vox-icons.js — jednoduché papírové ilustrace (SVG řetězce) pro Vox scény.
 * Styl: tlustý inkoustový obrys, papírová výplň, bílý trhaný okraj (výřez).
 *
 *   el.innerHTML = VOXI.cow();                 // kráva z boku (hlavou doleva)
 *   el.innerHTML = VOXI.cow({ calf: true });   // tele
 *   el.innerHTML = VOXI.icon('germ');          // ikony: germ, cart, milk, plant, scissors, clock, tag
 *
 * Kreslí se do viewBoxu; velikost určuje CSS šířka obalového elementu.
 */
(function () {
  const INK = '#141414', PAPER = '#fbf8f2', PINK = '#e8b4a6', SHADE = '#e6dfd1';
  let uid = 0;

  // obrys papírového výřezu: stejný tvar s tlustým bílým tahem a trhaným filtrem
  const cutBorder = (inner, w = 22) =>
    `<g filter="url(#vox-torn)" opacity="0.98"><g stroke="${PAPER}" stroke-width="${w}" fill="${PAPER}" stroke-linejoin="round">${inner}</g></g>`;

  /** Kráva / tele z boku. opts: {calf, spots, facing:'left'|'right'} */
  function cow(opts = {}) {
    const calf = !!opts.calf;
    const id = 'c' + uid++;
    const L = calf ? 0.74 : 1;           // délka těla
    const legLen = calf ? 112 : 92;      // délka nohou
    const bx = (x) => 112 + (x - 112) * L;
    const body = `M118,96 C120,70 150,62 190,64 L320,60 C360,58 372,84 370,118 L368,170 C366,196 346,204 318,204 L160,206 C128,206 112,190 112,160 Z`;
    const bodyT = `transform="translate(112 0) scale(${L} 1) translate(-112 0)"`;
    const leg = (x, far) => {
      const y0 = 168, y1 = y0 + legLen;
      return `<rect x="${x}" y="${y0}" width="26" height="${legLen}" rx="8" fill="${far ? SHADE : PAPER}" stroke="${INK}" stroke-width="6"/>
              <rect x="${x}" y="${y1 - 16}" width="26" height="16" rx="5" fill="${INK}"/>`;
    };
    const legs = leg(bx(166), true) + leg(bx(330), true) + leg(bx(128)) + leg(bx(292));
    const tailX = bx(366);
    const tail = `<path d="M${tailX},96 C${tailX + 26},130 ${tailX + 18},170 ${tailX + 14},${calf ? 190 : 206}" fill="none" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>
                  <ellipse cx="${tailX + 14}" cy="${calf ? 198 : 214}" rx="9" ry="15" fill="${INK}"/>`;
    const spots = opts.spots === false ? '' : `
      <g clip-path="url(#${id}-clip)" fill="${INK}">
        <path d="M178,64 C214,58 236,80 226,108 C214,134 180,128 172,104 C166,86 168,70 178,64 Z"/>
        <path d="M268,96 C306,86 334,112 322,146 C308,176 266,168 258,140 C252,118 254,102 268,96 Z"/>
        <path d="M330,52 C364,54 376,80 372,104 C352,108 334,92 330,52 Z"/>
        <path d="M130,150 C150,140 172,156 168,180 C160,200 134,198 126,180 Z"/>
      </g>`;
    const udder = calf ? '' : `<path d="M${bx(266)},200 C${bx(268)},236 ${bx(314)},236 ${bx(316)},200 Z" fill="${PINK}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>
      <path d="M${bx(278)},228 l0,10 M${bx(292)},231 l0,10 M${bx(305)},228 l0,10" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
    const hs = calf ? 1.14 : 1;
    const head = `<g transform="translate(118 140) scale(${hs}) translate(-118 -140)">
        ${calf ? '' : `<path d="M80,76 C76,58 84,48 94,46 C92,58 92,68 92,76 Z" fill="#efe4c9" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>`}
        <path d="M96,92 C110,70 142,68 154,80 C138,96 116,102 96,96 Z" fill="${PAPER}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>
        <path d="M108,90 C120,80 134,78 142,82 C130,90 118,94 108,92 Z" fill="${PINK}"/>
        <path d="M132,104 C112,86 92,70 70,72 C50,74 40,90 38,110 L34,160 C32,182 46,194 66,194 L84,194 C104,194 112,180 112,166 L118,140 Z" fill="${PAPER}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>
        <path d="M60,78 C80,72 100,84 96,106 C80,114 62,104 60,78 Z" fill="${INK}"/>
        <ellipse cx="62" cy="174" rx="32" ry="23" fill="${PINK}" stroke="${INK}" stroke-width="6"/>
        <ellipse cx="50" cy="171" rx="4" ry="5" fill="${INK}"/><ellipse cx="74" cy="171" rx="4" ry="5" fill="${INK}"/>
        <circle cx="68" cy="126" r="7" fill="${INK}"/><circle cx="70" cy="123" r="2.2" fill="#fff"/>
      </g>`;
    const shape = `
      <g>${legs}</g>
      ${tail}
      <g ${bodyT}><path d="${body}" fill="${PAPER}" stroke="${INK}" stroke-width="6" vector-effect="non-scaling-stroke" stroke-linejoin="round"/>
        <clipPath id="${id}-clip"><path d="${body}"/></clipPath>${spots}</g>
      ${udder}
      ${head}`;
    const silhouette = `<g>${legs}</g><g ${bodyT}><path d="${body}"/></g>${head}${udder}`;
    const flip = opts.facing === 'right' ? `transform="translate(420 0) scale(-1 1)"` : '';
    const h = 168 + legLen + 20;
    return `<svg viewBox="-20 30 460 ${h - 10}" width="100%" overflow="visible"><g ${flip}>${cutBorder(silhouette)}${shape}</g></svg>`;
  }

  /** Kráva shora (do přeplněných stájí). */
  function cowTop(opts = {}) {
    const calf = !!opts.calf;
    const s = calf ? 0.62 : 1;
    return `<svg viewBox="-10 -10 120 200" width="100%" overflow="visible"><g transform="translate(50 95) scale(${s}) translate(-50 -95)">
      <ellipse cx="50" cy="105" rx="36" ry="66" fill="${PAPER}" stroke="${INK}" stroke-width="5"/>
      <path d="M30,80 C44,70 58,86 50,104 C40,112 26,100 30,80 Z M58,120 C74,114 84,134 74,150 C62,156 52,140 58,120 Z" fill="${INK}"/>
      <ellipse cx="22" cy="40" rx="12" ry="6" fill="${PAPER}" stroke="${INK}" stroke-width="4"/>
      <ellipse cx="78" cy="40" rx="12" ry="6" fill="${PAPER}" stroke="${INK}" stroke-width="4"/>
      <ellipse cx="50" cy="34" rx="20" ry="26" fill="${PAPER}" stroke="${INK}" stroke-width="5"/>
      <ellipse cx="50" cy="16" rx="14" ry="9" fill="${PINK}" stroke="${INK}" stroke-width="4"/>
      <path d="M50,171 L50,186" stroke="${INK}" stroke-width="4" stroke-linecap="round"/>
    </g></svg>`;
  }

  const icons = {
    germ: (c = '#c8442a') => {
      let spikes = '';
      for (let i = 0; i < 10; i++) {
        const a = (i / 10) * Math.PI * 2, x1 = 50 + Math.cos(a) * 26, y1 = 50 + Math.sin(a) * 26;
        const x2 = 50 + Math.cos(a) * 40, y2 = 50 + Math.sin(a) * 40;
        spikes += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${INK}" stroke-width="5" stroke-linecap="round"/><circle cx="${x2}" cy="${y2}" r="5" fill="${c}" stroke="${INK}" stroke-width="3"/>`;
      }
      return `<svg viewBox="0 0 100 100" width="100%" overflow="visible">${spikes}<circle cx="50" cy="50" r="27" fill="${c}" stroke="${INK}" stroke-width="5"/>
        <circle cx="42" cy="44" r="5" fill="${INK}"/><circle cx="58" cy="56" r="4" fill="${INK}"/><circle cx="56" cy="40" r="3" fill="${INK}"/></svg>`;
    },
    scissors: () => `<svg viewBox="0 0 120 120" width="100%" overflow="visible">
      <path d="M58,62 L112,18 M58,58 L112,102" stroke="${INK}" stroke-width="10" stroke-linecap="round"/>
      <path d="M58,62 L112,18" stroke="#cfd3d6" stroke-width="5" stroke-linecap="round"/><path d="M58,58 L112,102" stroke="#cfd3d6" stroke-width="5" stroke-linecap="round"/>
      <circle cx="30" cy="36" r="20" fill="none" stroke="#e4472b" stroke-width="10"/><circle cx="30" cy="84" r="20" fill="none" stroke="#e4472b" stroke-width="10"/>
      <circle cx="58" cy="60" r="5" fill="${INK}"/></svg>`,
    milk: () => `<svg viewBox="0 0 120 200" width="100%" overflow="visible">
      <path d="M20,60 L60,20 L100,60 Z" fill="#e6dfd1" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>
      <rect x="44" y="6" width="32" height="18" fill="#2f6db5" stroke="${INK}" stroke-width="5"/>
      <rect x="20" y="60" width="80" height="130" fill="${PAPER}" stroke="${INK}" stroke-width="6"/>
      <rect x="20" y="96" width="80" height="44" fill="#2f6db5"/>
      <text x="60" y="126" text-anchor="middle" font-family="Inter Display, Inter, sans-serif" font-weight="900" font-size="22" fill="#fff">MLÉKO</text></svg>`,
    cart: () => `<svg viewBox="0 0 160 140" width="100%" overflow="visible">
      <path d="M6,16 L34,16 L54,96 L136,96 L152,36 L42,36" fill="none" stroke="${INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M46,56 L146,56 M50,76 L140,76" stroke="${INK}" stroke-width="5"/>
      <circle cx="62" cy="120" r="12" fill="${INK}"/><circle cx="126" cy="120" r="12" fill="${INK}"/></svg>`,
    plant: () => `<svg viewBox="0 0 140 200" width="100%" overflow="visible">
      <path d="M30,70 L110,70 L100,190 L40,190 Z" fill="${PAPER}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>
      <path d="M36,110 L104,110 L100,186 L40,186 Z" fill="#f1e9d4"/>
      <path d="M70,70 C70,40 70,24 70,8" stroke="#2f8a2f" stroke-width="6" stroke-linecap="round"/>
      <path d="M70,40 C50,30 44,16 48,6 C62,12 70,24 70,40 Z M70,30 C90,20 96,8 92,0 C80,6 70,16 70,30 Z M70,58 C52,52 44,40 46,30 C60,34 70,44 70,58 Z" fill="#00c800" stroke="${INK}" stroke-width="4"/>
      <text x="70" y="160" text-anchor="middle" font-family="Inter Display, Inter, sans-serif" font-weight="900" font-size="20" fill="${INK}">OVES</text></svg>`,
    tag: (txt = 'Kč') => `<svg viewBox="0 0 140 80" width="100%" overflow="visible">
      <path d="M30,6 L132,6 L132,74 L30,74 L4,40 Z" fill="#fff200" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>
      <circle cx="28" cy="40" r="7" fill="${PAPER}" stroke="${INK}" stroke-width="4"/>
      <text x="84" y="52" text-anchor="middle" font-family="Inter Display, Inter, sans-serif" font-weight="900" font-size="34" fill="${INK}">${txt}</text></svg>`,
    barn: () => `<svg viewBox="0 0 200 170" width="100%" overflow="visible">
      <path d="M10,70 L100,8 L190,70 L190,164 L10,164 Z" fill="#c9533b" stroke="${INK}" stroke-width="7" stroke-linejoin="round"/>
      <path d="M70,164 L70,96 L130,96 L130,164" fill="${PAPER}" stroke="${INK}" stroke-width="6"/>
      <path d="M70,96 L130,164 M130,96 L70,164" stroke="${INK}" stroke-width="5"/>
      <rect x="84" y="44" width="32" height="26" fill="${PAPER}" stroke="${INK}" stroke-width="5"/></svg>`,
  };

  window.VOXI = { cow, cowTop, icon: (name, ...a) => icons[name](...a) };
})();
