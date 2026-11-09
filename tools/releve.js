// Relevé d'une page, à coller dans la console (ou à lancer par un outil) :
// titres h1/h2 avec étoile, étoile mal placée, petits titres étoilés,
// rubrique en cours avec ou sans carré, boutons principaux avec ou sans grande étoile.
(() => {
  const visible = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.top < innerHeight * 2; };
  const nom = e => e.tagName.toLowerCase() + '.' + String(e.className).trim().split(/\s+/)[0];
  const texte = e => e.textContent.trim().replace(/\s+/g, ' ').slice(0, 18);
  const st = (e, p) => getComputedStyle(e, p);

  const titres = [...document.querySelectorAll('h1,h2')].filter(visible);
  const etoiles = titres.filter(h => st(h, '::before').clipPath.startsWith('shape'));
  const malPlacees = etoiles.filter(h => {
    const g = document.createRange();
    g.selectNodeContents(h);
    const r = [...g.getClientRects()].find(r => r.width > 2);
    return r && r.top - h.getBoundingClientRect().top - parseFloat(st(h).paddingTop) > parseFloat(st(h).fontSize) * 1.1;
  }).map(texte);
  const petits = etoiles.filter(h => parseFloat(st(h).fontSize) < 15).map(texte);

  const aCarre = a => [a, ...a.querySelectorAll('*')].some(e => st(e, '::before').backgroundImage.includes('50% 50% at'));
  const menus = [...document.querySelectorAll(':is(nav,aside,header,[role=navigation]) :is([aria-current]:not([aria-current=false]),.active,.selected,.is-active)')]
    .filter(visible).slice(0, 3).map(a => nom(a) + '«' + texte(a) + '»' + (aCarre(a) ? 'OK' : 'NON'));
  const boutons = [...document.querySelectorAll('button[type=submit],:is(button,a)[class*=btn-primary i],:is(button,a)[class*=button--primary i],[data-variant=primary]')]
    .filter(visible).slice(0, 3).map(b => nom(b) + '«' + texte(b) + '»' + (st(b, '::after').clipPath.startsWith('polygon') ? 'OK' : 'NON'));

  return JSON.stringify({ site: location.host, titres: titres.length + '/' + etoiles.length, malPlacees, petits, menus, boutons });
})();
