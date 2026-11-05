JARVIS ENERGY CORE — ANDROID PWA

FILES
- index.html: complete animated orb
- manifest.json: app installation settings
- sw.js: service worker / app-shell cache
- icons/: app icons

IMPORTANT
Chrome does not install a PWA when you open index.html directly from Downloads
(file://). PWA installation requires the files to be served from HTTPS (or
localhost). Upload this folder to an HTTPS static host, such as GitHub Pages,
Cloudflare Pages, or Netlify.

ANDROID INSTALL STEPS
1. Upload the contents of this folder to an HTTPS website.
2. Open that HTTPS address in Google Chrome on Android.
3. Wait for the page to finish loading, then use the "Install JARVIS" button
   if it appears. Otherwise tap Chrome's ⋮ menu > Install app
   (or Add to Home screen, depending on Chrome version).
4. Confirm Install. JARVIS will appear as an app icon and open standalone.

The 3D engine and post-processing modules are loaded from jsDelivr, so the
first launch needs an internet connection. The app shell is cached by the
service worker; the external Three.js modules may still require internet.
