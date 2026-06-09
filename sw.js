// GroMoney Capital — Service Worker v2.0 (Performance Optimized)
const CACHE_NAME = 'gromoney-v2';
const OFFLINE_URL = '/';

// Core assets to cache on install (critical for fast repeat visits)
const PRECACHE_ASSETS = [
  '/',
  '/index.html',
  '/assets/css/style.css',
  '/assets/js/main.js',
  '/assets/icons/favicon.svg',
  '/assets/icons/icon-192x192.png',
  '/manifest.json'
];

// Assets that benefit from long cache (images, icons)
const CACHE_FIRST_PATTERNS = [
  /\/assets\/icons\//,
  /\/assets\/images\//,
  /\.png$/,
  /\.svg$/,
  /\.jpg$/,
  /\.webp$/
];

// Install — precache core assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS);
    })
  );
  self.skipWaiting();
});

// Activate — clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

// Fetch strategy
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Skip external requests (analytics, fonts CDN, APIs, etc.)
  if (url.origin !== self.location.origin) return;

  // Cache-first for static assets (images, icons, fonts)
  if (CACHE_FIRST_PATTERNS.some(pattern => pattern.test(url.pathname))) {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) return cachedResponse;
        return fetch(event.request).then((response) => {
          if (response && response.status === 200) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return response;
        });
      })
    );
    return;
  }

  // Stale-while-revalidate for HTML and CSS/JS (fast load + fresh content)
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      const fetchPromise = fetch(event.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const clone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return networkResponse;
      }).catch(() => {
        // Offline fallback for navigation
        if (event.request.mode === 'navigate') {
          return caches.match(OFFLINE_URL);
        }
        return new Response('', { status: 503, statusText: 'Offline' });
      });

      // Return cached immediately if available, fetch updates in background
      return cachedResponse || fetchPromise;
    })
  );
});
