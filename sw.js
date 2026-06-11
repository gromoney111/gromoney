// GroMoney Capital — Service Worker v4.0
var CACHE_NAME = 'gromoney-v4';

// Essential pages to cache
var PRECACHE = [
  '/index.html',
  '/assets/css/style.css',
  '/assets/js/main.js',
  '/assets/icons/icon-192x192.png',
  '/assets/icons/icon-512x512.png',
  '/manifest.json',
  '/offline.html'
];

// Install event
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      // Use individual adds so one failure doesn't block all
      return Promise.all(
        PRECACHE.map(function(url) {
          return cache.add(url).catch(function(err) {
            console.warn('Failed to cache:', url, err);
          });
        })
      );
    })
  );
  self.skipWaiting();
});

// Activate event — clean old caches
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(names) {
      return Promise.all(
        names.filter(function(n) { return n !== CACHE_NAME; })
             .map(function(n) { return caches.delete(n); })
      );
    })
  );
  self.clients.claim();
});

// Fetch event — network first, cache fallback
self.addEventListener('fetch', function(event) {
  if (event.request.method !== 'GET') return;

  var url = new URL(event.request.url);

  // Skip cross-origin requests
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    fetch(event.request).then(function(response) {
      // Cache successful responses
      if (response && response.status === 200) {
        var clone = response.clone();
        caches.open(CACHE_NAME).then(function(cache) {
          cache.put(event.request, clone);
        });
      }
      return response;
    }).catch(function() {
      // Offline — serve from cache
      return caches.match(event.request).then(function(cached) {
        if (cached) return cached;
        // For page navigations, show offline page
        if (event.request.mode === 'navigate') {
          return caches.match('/offline.html').then(function(offlinePage) {
            return offlinePage || caches.match('/index.html');
          });
        }
        return new Response('Offline', { status: 503 });
      });
    })
  );
});
