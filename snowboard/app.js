(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Language menu: close on outside click or Escape.
  var langs = document.querySelector('.langs');
  if (langs) {
    document.addEventListener('click', function (e) { if (!langs.contains(e.target)) langs.open = false; });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') langs.open = false; });
  }

  // A link to #privacy (the App Store's privacy link lands here) shows the whole policy.
  function openPolicy() {
    if (location.hash !== '#privacy') return;
    document.querySelectorAll('#privacy details').forEach(function (d) { d.open = true; });
  }
  openPolicy();
  window.addEventListener('hashchange', openPolicy);

  // The video plays only while on screen, and never under reduced motion.
  document.querySelectorAll('video[data-loop]').forEach(function (v) {
    if (reduce) { v.controls = true; return; }
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { v.play().catch(function () {}); } else { v.pause(); }
      });
    }, { threshold: 0.25 }).observe(v);
  });

  // The track: one S-line down the run, carved as you scroll.
  // Orange on toe-side arcs and teal on heel-side arcs, like the app's edges.
  var run = document.getElementById('run');
  var NS = 'http://www.w3.org/2000/svg';
  function el(name, attrs, parent) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  var track = el('svg', { class: 'track', 'aria-hidden': 'true' });
  var rider = el('svg', { class: 'rider', 'aria-hidden': 'true' });
  var clip = el('rect', { x: 0, y: 0, width: 0, height: 0 }, el('clipPath', { id: 'carved' }, track));
  var carved = el('g', { 'clip-path': 'url(#carved)' }, track);
  var board = el('g', {}, rider);
  el('rect', { x: -36, y: -8.5, width: 72, height: 17, rx: 8.5, fill: '#12a5a2', stroke: '#15174f', 'stroke-width': 2.5 }, board);
  el('rect', { x: -22, y: -7, width: 4, height: 14, fill: '#f4661b' }, board);
  el('rect', { x: 18, y: -7, width: 4, height: 14, fill: '#f4661b' }, board);
  el('rect', { x: -15, y: -6, width: 9, height: 12, rx: 3, fill: '#15174f' }, board);
  el('rect', { x: 6, y: -6, width: 9, height: 12, rx: 3, fill: '#15174f' }, board);
  run.prepend(track);
  run.appendChild(rider);

  var apex = [];
  var mid = function (p, q) { return { x: (p.x + q.x) / 2, y: (p.y + q.y) / 2 }; };
  var f = function (p) { return p.x.toFixed(1) + ' ' + p.y.toFixed(1); };

  // Split the S between two apexes at its centre, where the edge changes.
  function halves(a, b) {
    var h = (b.y - a.y) / 2;
    var q1 = { x: a.x, y: a.y + h / 2 }, q3 = { x: b.x, y: b.y - h / 2 }, q2 = mid(a, b);
    var r1 = mid(q1, q2), r2 = mid(q2, q3);
    return { first: 'C' + f(q1) + ' ' + f(r1) + ' ' + f(q2), second: 'C' + f(r2) + ' ' + f(q3) + ' ' + f(b), m: q2 };
  }

  function apexes(W, H) {
    var pts = [], phone = W <= 760;
    if (phone) {
      for (var y = 24, right = false; y < H; y += 340, right = !right) pts.push({ x: right ? W - 12 : W - 44, y: y, toe: right });
      pts.push({ x: W - 28, y: H, toe: !right });
      return pts;
    }
    var box = run.getBoundingClientRect();
    pts.push({ x: W * 0.5, y: 24, toe: false });
    run.querySelectorAll('.gate').forEach(function (g) {
      var r = g.getBoundingClientRect(), toe = g.classList.contains('r');
      pts.push({ x: toe ? W * 0.87 : W * 0.13, y: r.top - box.top + r.height / 2, toe: toe });
    });
    pts.push({ x: W * 0.5, y: H, toe: !pts[pts.length - 1].toe });
    return pts;
  }

  var W = 0, H = 0, ticking = false;
  function layout() {
    W = run.clientWidth; H = run.offsetHeight;
    apex = apexes(W, H);
    [track, rider].forEach(function (s) { s.setAttribute('viewBox', '0 0 ' + W + ' ' + H); });
    clip.setAttribute('width', W);
    while (carved.firstChild) carved.removeChild(carved.firstChild);
    var whole = 'M' + f(apex[0]);
    var arcs = [];
    for (var i = 0; i < apex.length; i++) {
      var inn = i > 0 ? halves(apex[i - 1], apex[i]) : null, out = i < apex.length - 1 ? halves(apex[i], apex[i + 1]) : null;
      var d = 'M' + f(inn ? inn.m : apex[i]) + (inn ? inn.second : '') + (out ? out.first : '');
      if (inn) whole += inn.first + inn.second;
      arcs.push({ d: d, toe: apex[i].toe });
    }
    el('path', { class: 'groove', d: whole }, carved);
    arcs.forEach(function (a) { el('path', { class: 'edge ' + (a.toe ? 'toe' : 'heel'), d: a.d }, carved); });
    draw();
  }

  // Where the S is at height y: bisect the cubic, then read its slope.
  function at(y) {
    var i = 0;
    while (i < apex.length - 2 && apex[i + 1].y < y) i++;
    var a = apex[i], b = apex[i + 1], h = (b.y - a.y) / 2, lo = 0, hi = 1, t = 0, u, yt;
    for (var n = 0; n < 18; n++) {
      t = (lo + hi) / 2; u = 1 - t;
      yt = u * u * u * a.y + 3 * u * u * t * (a.y + h) + 3 * u * t * t * (b.y - h) + t * t * t * b.y;
      if (yt < y) lo = t; else hi = t;
    }
    u = 1 - t;
    var x = a.x * (u * u * u + 3 * u * u * t) + b.x * (3 * u * t * t + t * t * t);
    var dx = 6 * u * t * (b.x - a.x);
    var dy = 3 * u * u * h + 6 * u * t * (b.y - h - a.y - h) + 3 * t * t * h;
    return { x: x, angle: Math.atan2(dy, dx) * 180 / Math.PI };
  }

  function draw() {
    ticking = false;
    var head = reduce ? H : Math.max(40, Math.min(H - 2, window.innerHeight * 0.62 - run.getBoundingClientRect().top));
    clip.setAttribute('height', head);
    board.style.display = reduce ? 'none' : '';
    if (reduce) return;
    var p = at(head);
    board.setAttribute('transform', 'translate(' + p.x.toFixed(1) + ' ' + head.toFixed(1) + ') rotate(' + p.angle.toFixed(1) + ') scale(' + (W <= 760 ? 0.68 : 1) + ')');
  }

  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(draw); }
  }, { passive: true });
  new ResizeObserver(layout).observe(run);
  layout();
})();
