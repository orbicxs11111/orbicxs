self.addEventListener('push', event => {
  const data = event.data?.json() || {};
  const title = data.title || 'Yangi xabar';
  const options = {
    body: data.body || 'Sizga yangi xabar keldi',
    icon: 'logo.png',
    badge: 'logo.png!',
    tag: 'orbicxs-chat',
    renotify: true,
    data: data.url || '/'
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil(
    clients.openWindow(event.notification.data || '/')
  );
});
