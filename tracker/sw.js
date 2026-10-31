// Offline support for the Canada Visa Wait Times app.
// App files: served from cache, refreshed in the background.
// Processing-time data: always tries the network first, falls back to the saved copy offline.
const CACHE = 'ktis-tracker-v2';
const SHELL = ['./', 'index.html', 'manifest.webmanifest', 'data/country-names.json', 'data/processing-times.json',
  'icons/icon-192.png', 'icons/icon-512.png', 'icons/apple-touch-icon.png', 'icons/favicon-32.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys()
    .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;

  if (url.pathname.endsWith('/data/processing-times.json')) {
    e.respondWith(
      fetch(e.request).then((res) => {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put('data/processing-times.json', copy));
        return res;
      }).catch(async () => {
        const saved = await caches.match('data/processing-times.json');
        if (!saved) return Response.error();
        const headers = new Headers(saved.headers);
        headers.set('x-from-cache', '1');
        return new Response(await saved.blob(), { status: 200, headers });
      })
    );
    return;
  }

  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then((hit) => {
      const net = fetch(e.request).then((res) => {
        if (res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(e.request, copy)); }
        return res;
      }).catch(() => hit);
      return hit || net;
    })
  );
});
