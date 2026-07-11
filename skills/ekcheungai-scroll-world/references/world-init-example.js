/* ekcheung.com — scroll-world homepage journey (「升級之旅」The Upgrade Journey)
   Vinyl-toy miniature Hong Kong, light theme. 5 scenes, one continuous flight:
   城市 → 返工 → 茶餐廳 → 屋邨 → 你間房部電腦.
   Mounts the vendored scrub-engine on #world and coordinates the site nav:
   body.in-world  → nav is a transparent overlay on the world
   body.world-done → world layers hidden, nav back to the sticky look. */
(function () {
  var container = document.getElementById('world');
  if (!container || typeof mountScrollWorld !== 'function') return;

  var YT = 'https://www.youtube.com/channel/UCaqu5I6nqegDt-zs7jr284A?sub_confirmation=1';
  var BLUE = '#075BFF';
  var AMBER = '#C88A00';   // yellow family, darkened for text contrast on light bg

  mountScrollWorld(container, {
    nav: false,          // the site nav is the nav; engine topbar stays empty + hidden
    atmosphere: true,
    diveScroll: 1.15,
    crossfade: 0.08,     // one-take chain: legs hand off directly, small seam dissolve
    hint: '向下滾動',
    sections: [
      {
        id: 'city', label: '城市', accent: BLUE,
        still: '/images/world/scene-01.webp?v=4',
        clip: '/videos/world/scene-01.mp4?v=1',
        clipMobile: '/videos/world/scene-01-m.mp4?v=1',
        scroll: 1.5, linger: 0.3,
        eyebrow: 'THE CITY',
        title: '香港咁大，節奏咁快',
        body: 'AI 浪潮殺到，成個城市都喺度轉速 — 但冇人話你知點追。'
      },
      {
        id: 'grind', label: '返工', accent: BLUE,
        still: '/images/world/scene-02.webp?v=4',
        clip: '/videos/world/scene-02.mp4?v=1',
        clipMobile: '/videos/world/scene-02-m.mp4?v=1',
        eyebrow: 'THE GRIND',
        title: '日日搏殺，時間永遠唔夠',
        body: '開唔完嘅會、覆唔完嘅 message — 你唔係唔努力，你係冇槓桿。'
      },
      {
        id: 'hustle', label: '茶餐廳', accent: AMBER,
        still: '/images/world/scene-03.webp?v=4',
        clip: '/videos/world/scene-03.mp4?v=1',
        clipMobile: '/videos/world/scene-03-m.mp4?v=1',
        scroll: 1.2,
        eyebrow: 'THE HUSTLE',
        title: '全香港都喺度捱',
        body: '由茶餐廳到寫字樓，個個都咁拼 — 差嘅只係一套啱嘅方法。'
      },
      {
        id: 'home', label: '屋邨', accent: AMBER,
        still: '/images/world/scene-04.webp?v=4',
        clip: '/videos/world/scene-04.mp4?v=1',
        clipMobile: '/videos/world/scene-04-m.mp4?v=1',
        eyebrow: 'THE HOME',
        title: '返到屋企，先係你嘅時間',
        body: '夜晚嗰幾個鐘，就係你同人拉開距離嘅位。'
      },
      {
        id: 'room', label: '你間房', accent: BLUE,
        still: '/images/world/scene-05.webp?v=4',
        clip: '/videos/world/scene-05.mp4?v=1',
        clipMobile: '/videos/world/scene-05-m.mp4?v=1',
        scroll: 1.8, linger: 0.45,
        eyebrow: 'YOUR ROOM',
        title: '一部電腦，就夠你升級',
        body: '我用廣東話教你由工具、Agent 到自動化系統 — 喺你自己間房開始。',
        tags: ['工具', 'Agent', '自動化'],
        cta: {
          primary: { label: '由呢度開始', href: '#content-entry' },
          secondary: { label: '睇最新 YouTube', href: YT }
        }
      }
    ],
    connectors: []       // continuous forward take — the legs ARE the journey
  });

  // ---- site-nav coordination -------------------------------------------------
  var body = document.body;
  var worldEnd = 0;

  function measure() {
    var track = container.querySelector('.sw-track');
    worldEnd = track ? track.offsetHeight : 0;
  }

  function update() {
    var y = window.scrollY || window.pageYOffset;
    var navH = 72;
    var inWorld = worldEnd > 0 && y < worldEnd - navH;
    body.classList.toggle('in-world', inWorld);
    body.classList.toggle('world-done', !inWorld);
  }

  measure();
  update();
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', function () { measure(); update(); });
  window.addEventListener('orientationchange', function () { measure(); update(); });
  window.addEventListener('load', function () { measure(); update(); });
})();
