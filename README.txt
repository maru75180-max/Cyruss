TAPBIZ - GITHUB PAGES VERSION

FILES
- index.html
- business.html
- assets/style.css
- assets/script.js

PUBLISH
1. Extract this ZIP.
2. Open your existing GitHub repository.
3. Upload/replace index.html, business.html, and the entire assets folder at the repository root.
4. Go to Settings > Pages.
5. Select Deploy from a branch, choose main and /(root), then Save.
6. Wait for deployment and open your published URL.

IMPORTANT LIMITATION
GitHub Pages hosts static files only. This version does not run Flask, Python, Jinja, or SQLite. Add/Edit/Delete uses localStorage, so data is saved only in the browser/device where it was entered. It does not sync to other phones. A business.html?id=... profile will only appear if that business data exists in that browser. For the same NFC profile to display on every phone, use a separate public static page per business or a shared database/backend.

Keep a backup of your current repository before replacing files.
