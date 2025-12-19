const CACHE_NAME = 'simple-share-v2';
const APP_NAME = 'Simple Share';

// Files to cache for offline use
const FILES_TO_CACHE = [
  '/',
  '/mobile',
  '/manifest.json',
  '/static/style.css',
  '/static/mobile.css',
  '/static/icon-192.png',
  '/static/icon-512.png',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
  'https://cdn.rawgit.com/davidshimjs/qrcodejs/gh-pages/qrcode.min.js'
];

// Install event - cache files
self.addEventListener('install', (event) => {
  console.log(`${APP_NAME}: Service Worker installing...`);
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log(`${APP_NAME}: Caching app files`);
        return cache.addAll(FILES_TO_CACHE);
      })
      .then(() => {
        console.log(`${APP_NAME}: Service Worker installed`);
        return self.skipWaiting();
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log(`${APP_NAME}: Service Worker activating...`);
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log(`${APP_NAME}: Deleting old cache`, cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log(`${APP_NAME}: Service Worker activated`);
      return self.clients.claim();
    })
  );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', (event) => {
  const requestUrl = new URL(event.request.url);
  
  // Skip non-GET requests and chrome-extension
  if (event.request.method !== 'GET' || requestUrl.protocol === 'chrome-extension:') {
    return;
  }
  
  // Skip file downloads (let them go to network)
  if (event.request.url.includes('/download/') || 
      event.request.url.includes('/api/') ||
      event.request.url.includes('/upload')) {
    return;
  }
  
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Cache hit - return response
        if (response) {
          return response;
        }
        
        // Clone the request
        const fetchRequest = event.request.clone();
        
        // Make network request
        return fetch(fetchRequest).then((response) => {
          // Check if we received a valid response
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }
          
          // Clone the response
          const responseToCache = response.clone();
          
          // Cache the response
          caches.open(CACHE_NAME)
            .then((cache) => {
              cache.put(event.request, responseToCache);
            });
          
          return response;
        }).catch(() => {
          // If both cache and network fail, show offline page
          if (event.request.headers.get('accept').includes('text/html')) {
            return caches.match('/mobile');
          }
        });
      })
  );
});

// Push notifications (optional - for future features)
self.addEventListener('push', (event) => {
  if (!event.data) return;
  
  const data = event.data.json();
  const options = {
    body: data.body || 'New file shared!',
    icon: '/static/icon-192.png',
    badge: '/static/icon-192.png',
    vibrate: [100, 50, 100],
    data: {
      url: data.url || '/'
    }
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title || APP_NAME, options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  event.waitUntil(
    clients.matchAll({type: 'window'}).then((clientList) => {
      for (const client of clientList) {
        if (client.url === '/' && 'focus' in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow(event.notification.data.url || '/');
      }
    })
  );
});