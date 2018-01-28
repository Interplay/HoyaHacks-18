var dataCacheName = 'HoyaHacks-PWA-Data-Cache'

var cacheName = 'HoyaHacks-PWA-Cache'

var filesToCache = [
    './',
    './scripts/app.js',
    './styles/inline.css',
    './styles/materialize.css',
    './scripts/materialize.js',
    './index.html',
    './manifest.json',
    './favicon.ico'
]

self.addEventListener('install', function (e) {
      console.log('[ServiceWorker] Install')
      e.waitUntil(
             caches.open(cacheName).then(function (cache) {
                     console.log('[ServiceWorker] Caching app shell')
                     return cache.addAll(filesToCache)
              })
      )
})

self.addEventListener('activate', function (e) {
      console.log('[ServiceWorker] Activate')
      e.waitUntil(
              caches.keys().then(function (keyList) {
                       return Promise.all(keyList.map(function (key) {
                               if (key !== cacheName && key !== dataCacheName) {
                                    console.log('[ServiceWorker] Removing old cache', key)
                                    return caches.delete(key)
                               }
                        }))
              })
      )
      return self.clients.claim()
})

self.addEventListener('fetch', function (e) {
      console.log('[ServiceWorker] Fetch', e.request.url)
      e.respondWith(
             caches.match(e.request).then(function (response) {
                     return response || fetch(e.request)
             })
       )
})