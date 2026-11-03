(function () {
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Reveal blocks once as they scroll in.
  var rises = document.querySelectorAll('.rise');
  if ('IntersectionObserver' in window && !reduce) {
    var seen = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); seen.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    rises.forEach(function (el) { seen.observe(el); });
  } else {
    rises.forEach(function (el) { el.classList.add('in'); });
  }

  // Videos play only while on screen, and never under reduced motion.
  document.querySelectorAll('video[data-loop]').forEach(function (v) {
    if (reduce) { v.controls = true; return; }
    if (!('IntersectionObserver' in window)) { v.play().catch(function () {}); return; }
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { v.play().catch(function () {}); } else { v.pause(); }
      });
    }, { threshold: 0.25 }).observe(v);
  });

  // The ball: same idea as the app's balance pad. A model, not a measurement.
  var stage = document.querySelector('.pad-stage');
  if (!stage) return;
  var board = stage.querySelector('.board');
  var ball = stage.querySelector('.ball');
  var toes = stage.querySelector('.edge.toes');
  var heels = stage.querySelector('.edge.heels');
  var out = document.querySelector('.readout');
  var msgs = JSON.parse(document.getElementById('pad-messages').textContent);
  var edge = 0, weight = 0; // edge: -1 heels .. +1 toes. weight: -1 rear foot .. +1 leading foot.

  function clamp(v) { return Math.max(-1, Math.min(1, v)); }

  function render() {
    var r = board.getBoundingClientRect();
    var x = -weight * r.width * 0.34;
    var y = -edge * (board.offsetHeight / 2 - 15);
    ball.style.transform = 'translate(' + x + 'px,' + y + 'px)';
    board.style.transform = reduce ? 'none' : 'rotateX(' + (edge * 24) + 'deg) rotateY(' + (weight * 7) + 'deg)';
    toes.style.opacity = edge > 0.18 ? 1 : 0;
    heels.style.opacity = edge < -0.18 ? 1 : 0;
    var m = weight < -0.4 ? msgs.back
      : edge > 0.18 ? msgs.toes
      : edge < -0.18 ? msgs.heels
      : weight > 0.3 ? msgs.nose
      : msgs.flat;
    if (out.textContent !== m) out.textContent = m;
    ball.setAttribute('aria-valuetext', m);
  }

  function fromPointer(e) {
    var r = stage.getBoundingClientRect();
    weight = clamp(-(e.clientX - (r.left + r.width / 2)) / (r.width * 0.34));
    edge = clamp((r.top + r.height / 2 - e.clientY) / (board.offsetHeight / 2 - 15));
    render();
  }

  var dragging = false;
  stage.addEventListener('pointerdown', function (e) {
    dragging = true;
    stage.setPointerCapture(e.pointerId);
    fromPointer(e);
  });
  stage.addEventListener('pointermove', function (e) { if (dragging) fromPointer(e); });
  ['pointerup', 'pointercancel'].forEach(function (t) {
    stage.addEventListener(t, function () { dragging = false; });
  });
  ball.addEventListener('keydown', function (e) {
    var k = e.key, s = 0.15;
    if (k === 'ArrowUp') edge = clamp(edge + s);
    else if (k === 'ArrowDown') edge = clamp(edge - s);
    else if (k === 'ArrowLeft') weight = clamp(weight + s);
    else if (k === 'ArrowRight') weight = clamp(weight - s);
    else return;
    e.preventDefault();
    render();
  });
  window.addEventListener('resize', render);
  render();
})();
