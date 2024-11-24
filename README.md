# Backend(백엔드)
```
directory
├─ .git
│  ├─ config
│  ├─ description
│  ├─ HEAD
│  ├─ hooks
│  │  ├─ applypatch-msg.sample
│  │  ├─ commit-msg.sample
│  │  ├─ fsmonitor-watchman.sample
│  │  ├─ post-update.sample
│  │  ├─ pre-applypatch.sample
│  │  ├─ pre-commit.sample
│  │  ├─ pre-merge-commit.sample
│  │  ├─ pre-push.sample
│  │  ├─ pre-rebase.sample
│  │  ├─ pre-receive.sample
│  │  ├─ prepare-commit-msg.sample
│  │  ├─ sendemail-validate.sample
│  │  └─ update.sample
│  ├─ index
│  ├─ info
│  │  └─ exclude
│  ├─ objects
│  │  ├─ info
│  │  └─ pack
│  │     ├─ pack-11c5baec2ac2df048484d2bcf9ccd789d400802f.idx
│  │     ├─ pack-11c5baec2ac2df048484d2bcf9ccd789d400802f.pack
│  │     └─ pack-11c5baec2ac2df048484d2bcf9ccd789d400802f.rev
│  ├─ packed-refs
│  └─ refs
│     ├─ heads
│     │  ├─ dev
│     │  └─ main
│     ├─ remotes
│     │  └─ origin
│     │     └─ HEAD
│     └─ tags
├─ .gitignore
├─ backend
│  └─ myDiary
│     ├─ accounts
│     │  ├─ admin.py
│     │  ├─ apps.py
│     │  ├─ migrations
│     │  │  ├─ 0001_initial.py
│     │  │  ├─ 0002_alter_customuser_email.py
│     │  │  ├─ 0003_customuser_followings.py
│     │  │  └─ __init__.py
│     │  ├─ models.py
│     │  ├─ serializers.py
│     │  ├─ signals.py
│     │  ├─ tests.py
│     │  ├─ urls.py
│     │  ├─ views.py
│     │  └─ __init__.py
│     ├─ manage.py
│     ├─ movieDiary
│     │  ├─ admin.py
│     │  ├─ apps.py
│     │  ├─ migrations
│     │  │  ├─ 0001_initial.py
│     │  │  ├─ 0002_remove_journalcomment_title_and_more.py
│     │  │  ├─ 0003_moviejournal_evaluation_moviejournal_hide_and_more.py
│     │  │  ├─ 0004_remove_moviejournal_title.py
│     │  │  └─ __init__.py
│     │  ├─ models.py
│     │  ├─ serializers.py
│     │  ├─ templates
│     │  │  └─ movie_diary
│     │  │     └─ index.html
│     │  ├─ tests.py
│     │  ├─ urls.py
│     │  ├─ views.py
│     │  └─ __init__.py
│     ├─ movies
│     │  ├─ admin.py
│     │  ├─ apps.py
│     │  ├─ fixtures
│     │  │  ├─ genres.json
│     │  │  ├─ movies.json
│     │  │  └─ movie_genre.json
│     │  ├─ migrations
│     │  │  ├─ 0001_initial.py
│     │  │  └─ __init__.py
│     │  ├─ models.py
│     │  ├─ serializers.py
│     │  ├─ tests.py
│     │  ├─ tmdb.py
│     │  ├─ urls.py
│     │  ├─ views.py
│     │  └─ __init__.py
│     ├─ myDiary
│     │  ├─ asgi.py
│     │  ├─ settings.py
│     │  ├─ urls.py
│     │  ├─ wsgi.py
│     │  └─ __init__.py
│     ├─ README.md
│     ├─ requirements.txt
│     ├─ static
│     ├─ media
│     │  └─ profile_images
│     ├─ .env
│     └─ test_gpt.py
├─ frontend
│  └─ test
│     ├─ .gitignore
│     ├─ .vscode
│     │  └─ extensions.json
│     ├─ index.html
│     ├─ jsconfig.json
│     ├─ package-lock.json
│     ├─ package.json
│     ├─ public
│     │  └─ favicon.ico
│     ├─ README.md
│     ├─ src
│     │  ├─ App.vue
│     │  ├─ assets
│     │  │  ├─ base.css
│     │  │  ├─ logo.svg
│     │  │  └─ main.css
│     │  ├─ main.js
│     │  ├─ stores
│     │  │  ├─ api.js
│     │  │  └─ counter.js
│     │  └─ views
│     │     ├─ LoginView.vue
│     │     └─ SignUpView.vue
│     └─ vite.config.js
└─ README.md

```
