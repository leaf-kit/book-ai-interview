/* 채용을 위한 AI 엔지니어 기술 면접 노트 : 마크다운 뷰어
 *
 * 차례를 따로 관리하지 않는다. README.md 의 "차례" 절을 읽어서 만든다.
 * 원고를 고치면 뷰어의 차례도 같이 바뀌고, 둘이 어긋날 자리가 없다. */

(function () {
  'use strict';

  var REPO  = 'https://github.com/leaf-kit/book-ai-interview';
  var BLOB  = REPO + '/blob/main/';
  var TREE  = REPO + '/tree/main/';
  var BASE  = location.pathname.replace(/[^/]*$/, '');
  var HOME  = 'README.md';

  var LS = {
    read:  'aiinterview.read',
    theme: 'aiinterview.theme',
    fs:    'aiinterview.fs',
    width: 'aiinterview.width',
    last:  'aiinterview.last',
    fold:  'aiinterview.fold',
    stars: 'aiinterview.stars'
  };

  var $  = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  var el = {
    toc:      $('#toc'),
    doc:      $('#doc'),
    main:     $('#main'),
    sidebar:  $('#sidebar'),
    minitoc:  $('#minitoc'),
    mininav:  $('#minitoc nav'),
    pager:    $('#pager'),
    prev:     $('#pg-prev'),
    next:     $('#pg-next'),
    bar:      $('#progressbar'),
    q:        $('#q'),
    qclear:   $('#q-clear'),
    qhint:    $('#q-hint'),
    fulltext: $('#fulltext'),
    menu:     $('#menu'),
    scrim:    $('#scrim'),
    totop:    $('#totop'),
    ghSec:    $('#gh-section')
  };

  var state = {
    parts: [],        // [{title, items:[{num,title,label,path}]}]
    flat: [],         // 읽는 순서대로 펼친 목록
    byPath: {},
    path: '',
    cache: {},        // path -> 원문
    scrollAt: {},     // path -> 스크롤 위치
    corpus: null,     // 본문 검색용 전체 원문
    repos: null,      // 실재가 확인된 저장소 이름 -> 현재 이름
    mmdSeq: 0
  };

  /* ───────── 저장값 ───────── */

  function store(k, v) {
    try {
      if (v === undefined) { var s = localStorage.getItem(k); return s === null ? null : JSON.parse(s); }
      localStorage.setItem(k, JSON.stringify(v));
    } catch (e) { return null; }
  }

  var readSet = (function () {
    var arr = store(LS.read) || [];
    var set = {};
    arr.forEach(function (p) { set[p] = 1; });
    return set;
  })();

  function markRead(path) {
    if (readSet[path]) return;
    readSet[path] = 1;
    store(LS.read, Object.keys(readSet));
    var a = $('#toc a[data-path="' + cssEsc(path) + '"]');
    if (a) a.classList.add('read');
  }

  function cssEsc(s) { return s.replace(/["\\]/g, '\\$&'); }

  /* ───────── 가져오기 ───────── */

  function fetchDoc(path) {
    if (state.cache[path]) return Promise.resolve(state.cache[path]);
    return fetch(BASE + path, { cache: 'no-cache' }).then(function (r) {
      if (!r.ok) throw new Error(r.status + ' ' + r.statusText);
      return r.text();
    }).then(function (t) { state.cache[path] = t; return t; });
  }

  function loadScript(src) {
    return new Promise(function (ok, no) {
      var s = document.createElement('script');
      s.src = src; s.onload = ok; s.onerror = function () { no(new Error(src)); };
      document.head.appendChild(s);
    });
  }

  /* ───────── 차례 ───────── */

  function parseToc(md) {
    var lines = md.split('\n');
    var start = -1;
    for (var i = 0; i < lines.length; i++) {
      if (/^##\s+차례\s*$/.test(lines[i].trim())) { start = i; break; }
    }
    var parts = [], cur = null;
    if (start < 0) return parts;

    for (var k = start + 1; k < lines.length; k++) {
      var l = lines[k];
      if (/^##\s/.test(l)) break;                 // 다음 대제목에서 끝낸다
      var h = l.match(/^###\s+(.+?)\s*$/);
      if (h) { cur = { title: h[1].trim(), items: [] }; parts.push(cur); continue; }
      var it = l.match(/^\s*-\s+\[(.+?)\]\(([^)]+)\)\s*$/);
      if (it && cur) {
        var label = it[1].trim(), path = it[2].trim();
        if (!/\.md(#|$)/.test(path)) continue;
        var m = label.match(/^((?:\d+\.\d+)|(?:[A-Z]\.))\s+(.*)$/);
        cur.items.push({
          num: m ? m[1] : '',
          title: m ? m[2] : label,
          label: label,
          path: path.replace(/^\.\//, '')
        });
      }
    }
    return parts;
  }

  function buildIndex() {
    state.flat = [{ num: '', title: '표지와 소개', label: '표지와 소개', path: HOME }];
    state.parts.forEach(function (p) {
      p.items.forEach(function (x) { state.flat.push(x); });
    });
    state.byPath = {};
    state.flat.forEach(function (x, i) { x.i = i; state.byPath[x.path] = x; });
  }

  function partLabel(title) {
    var m = title.match(/^(.+?)\s*[—–-]\s*(.+)$/);
    return m ? { n: m[1], t: m[2] } : { n: '', t: title };
  }

  function renderToc() {
    var folded = store(LS.fold) || {};
    var html = '';

    html += '<div class="part" data-open="1" data-part="__home">' +
            '<ul><li><a href="#/' + HOME + '" data-path="' + HOME + '">' +
            '<span class="t">표지와 소개</span></a></li></ul></div>';

    state.parts.forEach(function (p, pi) {
      var lab = partLabel(p.title);
      var open = folded[pi] ? '0' : '1';
      html += '<div class="part" data-open="' + open + '" data-part="' + pi + '">';
      html += '<button class="part-h" type="button" aria-expanded="' + (open === '1') + '">' +
              '<svg class="caret" viewBox="0 0 20 20" aria-hidden="true"><path d="M6 8l4 4 4-4"/></svg>' +
              (lab.n ? '<span class="n">' + esc(lab.n) + '</span>' : '') +
              '<span>' + esc(lab.t) + '</span></button><ul>';
      p.items.forEach(function (x) {
        html += '<li><a href="#/' + encodeURI(x.path) + '" data-path="' + esc(x.path) + '"' +
                (readSet[x.path] ? ' class="read"' : '') + '>' +
                '<span class="num">' + esc(x.num) + '</span>' +
                '<span class="t">' + esc(x.title) + '</span></a></li>';
      });
      html += '</ul></div>';
    });

    el.toc.innerHTML = html;

    $$('.part-h', el.toc).forEach(function (b) {
      b.addEventListener('click', function () {
        var part = b.parentNode;
        var open = part.getAttribute('data-open') === '1' ? '0' : '1';
        part.setAttribute('data-open', open);
        b.setAttribute('aria-expanded', open === '1');
        var f = store(LS.fold) || {};
        f[part.getAttribute('data-part')] = open === '1' ? 0 : 1;
        store(LS.fold, f);
      });
    });
  }

  function syncToc() {
    $$('#toc a').forEach(function (a) {
      var on = a.getAttribute('data-path') === state.path;
      a.classList.toggle('active', on);
      if (on) {
        var part = a.closest('.part');
        if (part && part.getAttribute('data-open') === '0') {
          part.setAttribute('data-open', '1');
        }
        var r = a.getBoundingClientRect(), b = el.toc.getBoundingClientRect();
        if (r.top < b.top + 8 || r.bottom > b.bottom - 8) {
          a.scrollIntoView({ block: 'center' });
        }
      }
    });
    renderResume();
  }

  function renderResume() {
    var old = $('.resume', el.toc);
    if (old) old.parentNode.removeChild(old);
    var last = store(LS.last);
    if (!last || !last.path || last.path === state.path) return;
    var item = state.byPath[last.path];
    if (!item) return;
    var d = document.createElement('div');
    d.className = 'part resume';
    d.innerHTML = '<ul><li><a href="#/' + encodeURI(item.path) + '">' +
                  '<span class="num">이어</span><span class="t">' +
                  esc((item.num ? item.num + ' ' : '') + item.title) + '</span></a></li></ul>';
    el.toc.insertBefore(d, el.toc.firstChild);
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  /* ───────── 경로 ───────── */

  function resolvePath(from, href) {
    var dir = from.indexOf('/') >= 0 ? from.slice(0, from.lastIndexOf('/') + 1) : '';
    var u;
    try { u = new URL(dir + href, 'http://local/'); } catch (e) { return null; }
    var p = decodeURIComponent(u.pathname.replace(/^\//, ''));
    var a = u.hash ? decodeURIComponent(u.hash.slice(1)) : '';
    return { path: p, anchor: a };
  }

  function route() {
    var raw = location.hash.replace(/^#/, '');
    if (raw.charAt(0) === '?') {
      var q = decodeURIComponent(raw.slice(1).replace(/^q=/, ''));
      return { search: q };
    }
    if (!raw || raw === '/') return { path: HOME, anchor: '' };
    var s = raw.charAt(0) === '/' ? raw.slice(1) : raw;
    var i = s.indexOf('#');
    var p = i < 0 ? s : s.slice(0, i);
    var a = i < 0 ? '' : s.slice(i + 1);
    try { p = decodeURIComponent(p); } catch (e) {}
    try { a = decodeURIComponent(a); } catch (e) {}
    return { path: p || HOME, anchor: a };
  }

  /* ───────── 슬러그 ───────── */

  function slugify(text) {
    return String(text).trim().toLowerCase()
      .replace(/[`*_~]/g, '')
      .replace(/[^\p{L}\p{N}\s-]/gu, '')
      .replace(/\s+/g, '-');
  }

  /* ───────── 본문 그리기 ───────── */

  function go(path, anchor) {
    location.hash = '#/' + encodeURI(path) + (anchor ? '#' + encodeURIComponent(anchor) : '');
  }

  var renderSeq = 0;

  function open(path, anchor) {
    var mine = ++renderSeq;

    if (path === state.path) { scrollTo(anchor); return; }
    if (state.path) state.scrollAt[state.path] = el.main.scrollTop;

    state.path = path;
    syncToc();
    closeNav();
    el.doc.innerHTML = '<p class="loading">여는 중…</p>';
    el.pager.hidden = true;
    el.mininav.innerHTML = '';
    el.minitoc.classList.add('empty');
    el.ghSec.href = BLOB + path;

    fetchDoc(path).then(function (md) {
      if (mine !== renderSeq) return;
      el.doc.innerHTML = marked.parse(md);
      enhance(el.doc, path);
      if (path === HOME) renderCover(el.doc);
      buildMiniToc();
      renderPager();
      document.title = titleOf(path) + ' — 채용을 위한 AI 엔지니어 기술 면접 노트';
      store(LS.last, { path: path });
      renderResume();

      var y = anchor ? null : state.scrollAt[path];
      el.main.scrollTop = 0;
      if (anchor) scrollTo(anchor, true);
      else if (y) el.main.scrollTop = y;

      if (el.main.scrollHeight <= el.main.clientHeight + 80) markRead(path);
      updateProgress();
      renderMermaid();
    }).catch(function (e) {
      if (mine !== renderSeq) return;
      el.doc.innerHTML =
        '<div class="err"><h2>이 문서를 열지 못했다</h2>' +
        '<p><code>' + esc(path) + '</code> 를 읽는 데 실패했다. (' + esc(e.message) + ')</p>' +
        '<p>경로가 바뀌었거나 아직 없는 파일일 수 있다. ' +
        '<a href="' + BLOB + esc(path) + '" target="_blank" rel="noopener">깃허브에서 확인</a>하거나 ' +
        '<a href="#/' + HOME + '">처음으로</a> 돌아간다.</p></div>';
      document.title = '찾지 못함 — 채용을 위한 AI 엔지니어 기술 면접 노트';
    });
  }

  /* 첫 화면에만 표지를 세운다. README 맨 앞의 가로 배너는 깃허브에서 보라고 둔 것이라
     뷰어에서는 표지로 갈음한다. 같은 자리에 그림 둘이 겹치지 않게 하려는 것이다. */
  function renderCover(root) {
    var first = root.firstElementChild;
    while (first && first.tagName === 'P' && first.children.length === 1 &&
           first.firstElementChild.tagName === 'IMG') {
      root.removeChild(first);
      first = root.firstElementChild;
    }

    var start = state.flat[1];
    var last = store(LS.last);
    var resume = last && last.path && last.path !== HOME ? state.byPath[last.path] : null;

    var hero = document.createElement('div');
    hero.className = 'hero';
    hero.innerHTML =
      '<img class="hero-cover" src="' + BASE + 'images/cover-front-2edition.png" ' +
      'alt="채용을 위한 AI 엔지니어 기술 면접 노트 표지">' +
      '<div class="hero-side">' +
        '<p class="hero-meta"><b>질문 61개, 도식 97개.</b><br>' +
        '외운 답과 해 본 답을 가르는 법을 한 질문씩 짚어간다.<br>' +
        '판정 기준과 꼬리 질문까지 그대로 가져가 쓴다.</p>' +
        '<div class="hero-act">' +
        (start ? '<a class="hero-btn primary" href="#/' + encodeURI(start.path) + '">첫 장부터 읽기</a>' : '') +
        (resume ? '<a class="hero-btn" href="#/' + encodeURI(resume.path) + '">이어 읽기 — ' +
                  esc((resume.num ? resume.num + ' ' : '') + resume.title) + '</a>' : '') +
        '</div></div>';
    root.insertBefore(hero, root.firstChild);
  }

  function titleOf(path) {
    var x = state.byPath[path];
    if (!x) return path;
    return (x.num ? x.num + ' ' : '') + x.title;
  }

  function scrollTo(anchor, instant) {
    if (!anchor) return;
    var t = document.getElementById(anchor) || $('[data-raw-id="' + cssEsc(anchor) + '"]', el.doc);
    if (!t) return;
    var top = t.getBoundingClientRect().top - el.main.getBoundingClientRect().top + el.main.scrollTop - 14;
    if (instant) el.main.scrollTop = top;
    else el.main.scrollTo({ top: top, behavior: 'smooth' });
  }

  /* 본문의 `owner/repo` 는 깃허브 저장소를 가리킨다. 1500번쯤 나오는데 전부 맨 텍스트라
     독자가 저장소를 보려면 주소창에 직접 쳐야 했다. 링크로 건다.

     생김새로 판정하지 않는다. 저장소 안의 경로가 같은 모양이기 때문이다. 8.1 의
     `ai/offensive-ai-security` 는 저장소가 아니라 Claude-Red 안의 디렉터리다. 그래서
     viewer/build-repos.py 가 원고의 이름을 깃허브 API 로 전부 확인해 viewer/repos.json
     에 적어 두고, 뷰어는 그 목록에 있는 것만 건다. 목록을 못 읽으면 하나도 걸지 않는다.
     죽은 링크가 맨 텍스트보다 나쁘다. */
  function linkRepos(root) {
    var map = state.repos;
    if (!map) return;
    $$('code', root).forEach(function (c) {
      if (c.closest('pre') || c.closest('a')) return;
      var full = map[c.textContent.trim()];
      if (!full) return;
      var a = document.createElement('a');
      a.className = 'repo';
      a.href = 'https://github.com/' + full;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.title = full + ' — 깃허브에서 열기';
      c.parentNode.insertBefore(a, c);
      a.appendChild(c);
    });
  }

  /* 마크다운이 낸 HTML을 손본다 — 제목 id, 링크, 표, 코드 */
  function enhance(root, path) {
    var used = {};
    $$('h1, h2, h3, h4', root).forEach(function (h) {
      var base = slugify(h.textContent) || 'h';
      var id = base;
      if (used[base]) id = base + '-' + used[base];
      used[base] = (used[base] || 0) + 1;
      h.id = id;
      if (h.tagName !== 'H1' && h.tagName !== 'H4') {
        var a = document.createElement('a');
        a.className = 'anchor';
        a.href = '#/' + encodeURI(path) + '#' + encodeURIComponent(id);
        a.textContent = '#';
        a.setAttribute('aria-label', '이 소제목 링크');
        h.insertBefore(a, h.firstChild);
      }
    });

    $$('a[href]', root).forEach(function (a) {
      var href = a.getAttribute('href');
      if (!href || a.classList.contains('anchor')) return;

      if (/^(https?:|mailto:|tel:)/i.test(href)) {
        a.target = '_blank'; a.rel = 'noopener noreferrer';
        a.classList.add('ext');
        return;
      }
      if (href.charAt(0) === '#') {                       // 같은 문서 안의 소제목
        a.setAttribute('href', '#/' + encodeURI(path) + '#' + encodeURIComponent(href.slice(1)));
        return;
      }
      var r = resolvePath(path, href);
      if (!r) return;
      if (/\.md$/i.test(r.path)) {
        a.setAttribute('href', '#/' + encodeURI(r.path) + (r.anchor ? '#' + encodeURIComponent(r.anchor) : ''));
      } else {                                            // 원고가 아닌 파일은 깃허브로 보낸다
        var isDir = /\/$/.test(r.path) || !/\.[a-z0-9]+$/i.test(r.path);
        a.setAttribute('href', (isDir ? TREE : BLOB) + r.path.replace(/\/$/, ''));
        a.target = '_blank'; a.rel = 'noopener noreferrer';
        a.classList.add('ext');
      }
    });

    linkRepos(root);

    $$('img[src]', root).forEach(function (img) {
      var src = img.getAttribute('src');
      if (/^(https?:|data:)/i.test(src)) return;
      var r = resolvePath(path, src);
      if (r) img.setAttribute('src', BASE + r.path);
      img.loading = 'lazy';
    });

    $$('table', root).forEach(function (t) {
      if (t.parentNode.classList.contains('table-wrap')) return;
      var w = document.createElement('div');
      w.className = 'table-wrap';
      t.parentNode.insertBefore(w, t);
      w.appendChild(t);
    });

    $$('pre > code', root).forEach(function (c) {
      var lang = (c.className.match(/language-([\w-]+)/) || [])[1];
      if (lang === 'mermaid') {
        var d = document.createElement('div');
        d.className = 'mermaid';
        d.setAttribute('data-src', c.textContent);
        d.textContent = '다이어그램을 그리는 중…';
        c.parentNode.parentNode.replaceChild(d, c.parentNode);
        return;
      }
      if (lang && window.hljs && window.hljs.getLanguage(lang)) {
        try { window.hljs.highlightElement(c); } catch (e) {}
      }
      var b = document.createElement('button');
      b.className = 'copy'; b.type = 'button'; b.textContent = '복사';
      b.addEventListener('click', function () {
        navigator.clipboard.writeText(c.textContent).then(function () {
          b.textContent = '복사됨';
          setTimeout(function () { b.textContent = '복사'; }, 1200);
        });
      });
      c.parentNode.appendChild(b);
    });
  }

  function renderMermaid() {
    var nodes = $$('.mermaid[data-src]', el.doc);
    if (!nodes.length) return;
    var ready = window.mermaid
      ? Promise.resolve()
      : loadScript('https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js').then(function () {
          window.mermaid.initialize({
            startOnLoad: false,
            securityLevel: 'loose',
            theme: 'neutral',
            fontFamily: '"Apple SD Gothic Neo", "Noto Sans KR", system-ui, sans-serif',
            fontSize: 15,
            /* 라벨을 HTML 대신 SVG text 로 그린다. mermaid 는 본문 바깥에서 상자 크기를
               재는데, HTML 라벨이면 본문의 line-height 와 letter-spacing 이 나중에 끼어들어
               글자가 상자 밖으로 밀린다. text 라벨은 그 영향을 받지 않는다. */
            htmlLabels: false,
            flowchart: { htmlLabels: false, useMaxWidth: true, padding: 10 }
          });
        });

    ready.then(function () {
      nodes.forEach(function (n) {
        var src = n.getAttribute('data-src');
        window.mermaid.render('mmd-' + (++state.mmdSeq), src).then(function (out) {
          n.innerHTML = out.svg;
          n.removeAttribute('data-src');
        }).catch(function () {
          n.textContent = '';
          var pre = document.createElement('pre');
          pre.textContent = src;
          n.appendChild(pre);
          n.removeAttribute('data-src');
        });
      });
    }).catch(function () {
      nodes.forEach(function (n) {
        var pre = document.createElement('pre');
        pre.textContent = n.getAttribute('data-src');
        n.textContent = ''; n.appendChild(pre); n.removeAttribute('data-src');
      });
    });
  }

  /* ───────── 소제목 목차 ───────── */

  function buildMiniToc() {
    var hs = $$('h2, h3', el.doc);
    if (hs.length < 2) { el.minitoc.classList.add('empty'); el.mininav.innerHTML = ''; return; }
    el.minitoc.classList.remove('empty');
    el.mininav.innerHTML = hs.map(function (h) {
      var text = h.textContent.replace(/^#/, '');
      return '<a href="#/' + encodeURI(state.path) + '#' + encodeURIComponent(h.id) + '"' +
             ' data-id="' + esc(h.id) + '" class="' + (h.tagName === 'H3' ? 'lv3' : 'lv2') + '">' +
             esc(text) + '</a>';
    }).join('');
  }

  function syncMiniToc() {
    var links = $$('a', el.mininav);
    if (!links.length) return;
    var top = el.main.getBoundingClientRect().top + 96;
    var cur = null;
    $$('h2, h3', el.doc).forEach(function (h) {
      if (h.getBoundingClientRect().top <= top) cur = h.id;
    });
    if (!cur) cur = links[0].getAttribute('data-id');
    links.forEach(function (a) {
      var on = a.getAttribute('data-id') === cur;
      a.classList.toggle('active', on);
      if (on) {
        var r = a.getBoundingClientRect(), b = el.minitoc.getBoundingClientRect();
        if (r.top < b.top + 6 || r.bottom > b.bottom - 6) a.scrollIntoView({ block: 'nearest' });
      }
    });
  }

  /* ───────── 이전 다음 ───────── */

  function renderPager() {
    var x = state.byPath[state.path];
    if (!x) { el.pager.hidden = true; return; }
    var p = state.flat[x.i - 1], n = state.flat[x.i + 1];
    el.pager.hidden = false;

    if (p) {
      el.prev.hidden = false;
      el.prev.href = '#/' + encodeURI(p.path);
      $('.t', el.prev).textContent = (p.num ? p.num + ' ' : '') + p.title;
    } else el.prev.hidden = true;

    if (n) {
      el.next.hidden = false;
      el.next.href = '#/' + encodeURI(n.path);
      $('.t', el.next).textContent = (n.num ? n.num + ' ' : '') + n.title;
    } else el.next.hidden = true;
  }

  function step(d) {
    var x = state.byPath[state.path];
    if (!x) return;
    var t = state.flat[x.i + d];
    if (t) go(t.path, '');
  }

  /* ───────── 진행률 ───────── */

  function updateProgress() {
    var max = el.main.scrollHeight - el.main.clientHeight;
    var r = max > 0 ? el.main.scrollTop / max : 1;
    el.bar.style.width = (r * 100).toFixed(1) + '%';
    el.totop.hidden = el.main.scrollTop < 400;
    if (r > 0.6 && state.path) markRead(state.path);
  }

  /* ───────── 차례 거르기 ───────── */

  function filterToc(q) {
    var needle = q.trim().toLowerCase();
    el.qclear.hidden = !needle;
    var ft = el.fulltext;
    if (needle.length >= 2) {
      ft.hidden = false;
      $('span', ft).textContent = q.trim();
    } else ft.hidden = true;

    var resume = $('.resume', el.toc);
    if (resume) resume.classList.toggle('hidden', !!needle);

    if (!needle) {
      $$('#toc .part', el.toc).forEach(function (p) { p.classList.remove('hidden'); });
      $$('#toc li', el.toc).forEach(function (li) {
        li.classList.remove('hidden');
        var a = $('a', li), t = $('.t', a);
        if (t) t.innerHTML = esc(t.textContent);
      });
      el.qhint.hidden = true;
      return;
    }

    var hits = 0;
    $$('#toc .part', el.toc).forEach(function (p) {
      if (p.classList.contains('resume')) return;
      var any = false;
      $$('li', p).forEach(function (li) {
        var a = $('a', li), t = $('.t', a);
        var num = $('.num', a) ? $('.num', a).textContent : '';
        var text = t.textContent;
        var i = text.toLowerCase().indexOf(needle);
        var inNum = num.toLowerCase().indexOf(needle) >= 0;
        if (i >= 0 || inNum) {
          any = true; hits++;
          li.classList.remove('hidden');
          t.innerHTML = i >= 0
            ? esc(text.slice(0, i)) + '<mark>' + esc(text.slice(i, i + needle.length)) + '</mark>' + esc(text.slice(i + needle.length))
            : esc(text);
        } else {
          li.classList.add('hidden');
        }
      });
      p.classList.toggle('hidden', !any);
      if (any) p.setAttribute('data-open', '1');
    });

    el.qhint.hidden = false;
    el.qhint.textContent = hits ? '제목에서 ' + hits + '개를 찾았다.' : '제목에는 없다. 본문까지 찾아본다.';
  }

  /* ───────── 본문 전체 검색 ───────── */

  function fullTextSearch(q) {
    var needle = q.trim();
    if (needle.length < 2) return;
    location.hash = '#?q=' + encodeURIComponent(needle);
  }

  /* 검색 결과에 마크다운 기호가 그대로 보이면 읽기 나쁘다. 눈에 띄는 것만 걷어낸다. */
  function stripMd(s) {
    return s
      .replace(/^#{1,6}\s+/, '')
      .replace(/^\s*[-+*]\s+/, '')
      .replace(/^\s*>\s?/, '')
      .replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1')
      .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
      .replace(/[*_`]/g, '')
      .replace(/\s*\|\s*/g, '  ')
      .trim();
  }

  function loadCorpus(onProgress) {
    if (state.corpus) return Promise.resolve(state.corpus);
    var paths = state.flat.map(function (x) { return x.path; });
    var done = 0;
    return Promise.all(paths.map(function (p) {
      return fetchDoc(p).then(function (t) {
        done++; onProgress(done, paths.length);
        return { path: p, text: t };
      }).catch(function () {
        done++; onProgress(done, paths.length);
        return { path: p, text: '' };
      });
    })).then(function (docs) { state.corpus = docs; return docs; });
  }

  function showSearch(q) {
    state.path = '';
    state.scrollAt = state.scrollAt || {};
    syncToc();
    closeNav();
    el.pager.hidden = true;
    el.mininav.innerHTML = '';
    el.minitoc.classList.add('empty');
    el.main.scrollTop = 0;
    document.title = '“' + q + '” 검색 — 채용을 위한 AI 엔지니어 기술 면접 노트';
    el.doc.innerHTML = '<h1>본문 검색</h1><p class="loading">원고를 모으는 중… <span id="dl">0</span></p>';

    loadCorpus(function (d, n) {
      var s = $('#dl');
      if (s) s.textContent = d + ' / ' + n;
    }).then(function (docs) {
      var needle = q.toLowerCase();
      var hits = [];
      docs.forEach(function (d) {
        var lines = d.text.split('\n');
        var count = 0, snips = [], heading = '';
        for (var i = 0; i < lines.length; i++) {
          var raw = lines[i];
          var hm = raw.match(/^(#{1,4})\s+(.*)$/);
          if (hm) { if (snips.length === 0) heading = hm[2]; }
          if (/^\s*```/.test(raw)) continue;
          var line = stripMd(raw);
          var at = line.toLowerCase().indexOf(needle);
          if (at < 0) continue;
          count++;
          if (snips.length < 3) {
            var from = Math.max(0, at - 42);
            var to = Math.min(line.length, at + needle.length + 70);
            snips.push({
              pre: (from > 0 ? '…' : '') + line.slice(from, at),
              hit: line.slice(at, at + needle.length),
              post: line.slice(at + needle.length, to) + (to < line.length ? '…' : ''),
              anchor: heading ? slugify(heading) : ''
            });
          }
        }
        if (count) hits.push({ path: d.path, count: count, snips: snips });
      });

      hits.sort(function (a, b) { return b.count - a.count; });

      var html = '<h1>본문 검색</h1>';
      html += '<p class="rhead">“' + esc(q) + '” — 문서 ' + hits.length + '개에서 ' +
              hits.reduce(function (s, h) { return s + h.count; }, 0) + '번 나온다. 많이 나온 순서다.</p>';
      if (!hits.length) {
        html += '<p>찾지 못했다. 다른 말로 찾아본다.</p>';
      } else {
        html += '<div class="results">';
        hits.forEach(function (h) {
          var a = h.snips[0] && h.snips[0].anchor ? '#' + encodeURIComponent(h.snips[0].anchor) : '';
          html += '<a class="hit" href="#/' + encodeURI(h.path) + a + '">' +
                  '<b>' + esc(titleOf(h.path)) + ' <span style="font-weight:400;opacity:.6">(' + h.count + ')</span></b>' +
                  '<span class="where">' + esc(h.path) + '</span>';
          h.snips.forEach(function (s) {
            html += '<div class="snip">' + esc(s.pre) + '<mark>' + esc(s.hit) + '</mark>' + esc(s.post) + '</div>';
          });
          html += '</a>';
        });
        html += '</div>';
      }
      el.doc.innerHTML = html;
      updateProgress();
    });
  }

  /* ───────── 서랍 ───────── */

  function openNav() {
    document.body.classList.add('nav-open');
    el.scrim.hidden = false;
    el.menu.setAttribute('aria-expanded', 'true');
  }
  function closeNav() {
    document.body.classList.remove('nav-open');
    el.scrim.hidden = true;
    el.menu.setAttribute('aria-expanded', 'false');
  }
  function narrow() { return window.matchMedia('(max-width: 860px)').matches; }

  /* ───────── 설정 ───────── */

  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    store(LS.theme, t);
  }
  /* 본문 너비. 글만 읽을 때는 좁은 쪽이 편하고, 11부처럼 표가 긴 장은 넓은 쪽이 편하다.
     어느 쪽이 맞는지는 글이 아니라 읽는 사람이 정한다. */
  var WIDTHS = [
    { key: 'narrow', css: '680px',  name: '좁게' },
    { key: 'normal', css: '840px',  name: '보통' },
    { key: 'wide',   css: '1080px', name: '넓게' },
    { key: 'full',   css: 'none',   name: '전체' }
  ];

  function applyWidth(key) {
    var i = 0;
    for (var k = 0; k < WIDTHS.length; k++) if (WIDTHS[k].key === key) i = k;
    var w = WIDTHS[i];
    document.documentElement.style.setProperty('--paper-w', w.css);
    var lab = $('#width-label');
    if (lab) lab.textContent = w.name;
    var btn = $('#width');
    if (btn) btn.title = '본문 너비 — ' + w.name + ' (W)';
    store(LS.width, w.key);
    return w.key;
  }

  function stepWidth() {
    var cur = store(LS.width) || 'wide';
    var i = 0;
    for (var k = 0; k < WIDTHS.length; k++) if (WIDTHS[k].key === cur) i = k;
    applyWidth(WIDTHS[(i + 1) % WIDTHS.length].key);
  }

  function applyFs(n) {
    n = Math.max(15, Math.min(21, n));
    document.documentElement.style.setProperty('--fs', n + 'px');
    store(LS.fs, n);
    return n;
  }

  /* ───────── 별 개수 ───────── */

  /* 깃허브 API 는 로그인 없이 시간당 60번이다. 한 시간 동안은 받아 둔 값을 쓴다.
     못 받아 오면 개수 칸만 접고 Star 단추는 그대로 둔다. */
  function loadStars() {
    var cached = store(LS.stars);
    var now = Date.now();
    if (cached && cached.n != null && now - cached.at < 3600000) { showStars(cached.n); return; }

    fetch('https://api.github.com/repos/leaf-kit/book-ai-interview')
      .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error(r.status)); })
      .then(function (d) {
        if (typeof d.stargazers_count !== 'number') return;
        store(LS.stars, { n: d.stargazers_count, at: now });
        showStars(d.stargazers_count);
      })
      .catch(function () { if (cached && cached.n != null) showStars(cached.n); });
  }

  function showStars(n) {
    var e = $('#star-n');
    if (!e) return;
    e.textContent = n >= 1000 ? (n / 1000).toFixed(1).replace(/\.0$/, '') + 'k' : String(n);
    /* /stargazers 로 보내지 않는다. 깃허브가 그 페이지를 더 이상 열어 주지 않는다(404). */
    e.title = '별 ' + n.toLocaleString('ko-KR') + '개';
    e.hidden = false;
  }

  /* ───────── 연결 ───────── */

  function wire() {
    window.addEventListener('hashchange', function () {
      var r = route();
      if (r.search !== undefined) showSearch(r.search);
      else open(r.path, r.anchor);
    });

    var tick = null;
    el.main.addEventListener('scroll', function () {
      if (tick) return;
      tick = requestAnimationFrame(function () {
        tick = null;
        updateProgress();
        syncMiniToc();
      });
    }, { passive: true });

    el.totop.addEventListener('click', function () { el.main.scrollTo({ top: 0, behavior: 'smooth' }); });
    el.menu.addEventListener('click', function () {
      document.body.classList.contains('nav-open') ? closeNav() : openNav();
    });
    el.scrim.addEventListener('click', closeNav);
    el.toc.addEventListener('click', function (e) {
      if (e.target.closest('a') && narrow()) closeNav();
    });

    el.q.addEventListener('input', function () { filterToc(el.q.value); });
    el.q.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); fullTextSearch(el.q.value); }
      if (e.key === 'Escape') { el.q.value = ''; filterToc(''); el.q.blur(); }
    });
    el.qclear.addEventListener('click', function () { el.q.value = ''; filterToc(''); el.q.focus(); });
    el.fulltext.addEventListener('click', function () { fullTextSearch(el.q.value); });

    $('#theme').addEventListener('click', function () {
      applyTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });
    $('#width').addEventListener('click', stepWidth);
    $('#font-up').addEventListener('click', function () { applyFs((store(LS.fs) || 17) + 1); });
    $('#font-down').addEventListener('click', function () { applyFs((store(LS.fs) || 17) - 1); });

    $('#reset-read').addEventListener('click', function () {
      readSet = {};
      store(LS.read, []);
      try { localStorage.removeItem(LS.last); } catch (e) {}
      $$('#toc a.read').forEach(function (a) { a.classList.remove('read'); });
      renderResume();
    });

    document.addEventListener('keydown', function (e) {
      var t = e.target;
      var typing = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
      if (e.key === '/' && !typing) { e.preventDefault(); el.q.focus(); el.q.select(); return; }
      if (typing || e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === 'ArrowLeft') { step(-1); }
      else if (e.key === 'ArrowRight') { step(1); }
      else if (e.key === 't' || e.key === 'T' || e.key === 'ㅅ') {
        applyTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
      } else if (e.key === 'w' || e.key === 'W' || e.key === 'ㅈ') { stepWidth(); }
      else if (e.key === 'Escape') { closeNav(); }
    });

    window.addEventListener('beforeunload', function () {
      if (state.path) store(LS.last, { path: state.path });
    });
  }

  /* ───────── 시작 ───────── */

  function boot() {
    var saved = store(LS.theme);
    applyTheme(saved || 'light');
    applyFs(store(LS.fs) || 17);
    applyWidth(store(LS.width) || 'wide');
    loadStars();

    if (window.marked && marked.setOptions) {
      marked.setOptions({ gfm: true, breaks: false });
    }

    wire();

    var repos = fetch(BASE + 'viewer/repos.json')
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) { if (d && d.repos) state.repos = d.repos; })
      .catch(function () { /* 목록이 없으면 저장소 링크만 걸지 않는다 */ });

    Promise.all([fetchDoc(HOME), repos]).then(function (out) {
      var md = out[0];
      state.parts = parseToc(md);
      buildIndex();
      renderToc();
      var r = route();
      if (r.search !== undefined) showSearch(r.search);
      else open(r.path, r.anchor);
    }).catch(function (e) {
      el.toc.innerHTML = '<p class="loading">차례를 읽지 못했다.</p>';
      el.doc.innerHTML = '<div class="err"><h2>README.md 를 읽지 못했다</h2>' +
        '<p>' + esc(e.message) + '</p>' +
        '<p>파일을 직접 여는 대신 로컬 서버로 띄워야 한다. 저장소 안에서 ' +
        '<code>python3 -m http.server 8000</code> 을 돌리고 ' +
        '<code>http://localhost:8000/</code> 로 들어간다.</p></div>';
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
