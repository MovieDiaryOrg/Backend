# Backend(백엔드)
```
github
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
│  │     ├─ pack-3beb9432d0b5cf3c303a4fbbda3e7dc3f70934b8.idx
│  │     ├─ pack-3beb9432d0b5cf3c303a4fbbda3e7dc3f70934b8.pack
│  │     └─ pack-3beb9432d0b5cf3c303a4fbbda3e7dc3f70934b8.rev
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
│     │  │  └─ counter.js
│     │  └─ views
│     │     ├─ LoginView.vue
│     │     └─ SignUpView.vue
│     └─ vite.config.js
└─ README.md

```
```
github
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
```
github
├─ .git
│  ├─ COMMIT_EDITMSG
│  ├─ config
│  ├─ description
│  ├─ FETCH_HEAD
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
│  │  ├─ 0d
│  │  │  └─ bd1f7afca10e1bb597c2358c77cff6ad68e9c2
│  │  ├─ 1c
│  │  │  └─ 1c9a9657c12fa27838f774a79b0568a245e57f
│  │  ├─ 26
│  │  │  └─ 0aa41aa8d04ea7a602a4c2f0dbee1646188494
│  │  ├─ 2a
│  │  │  └─ 93bbba1c68c8ac9646e0ca3e73feb08717cd9a
│  │  ├─ 3f
│  │  │  └─ c5d2c48ba5a974251ab6763db8d31cccad2f6a
│  │  ├─ 48
│  │  │  └─ 869f613367f1d4053dd0504af12190be6caf05
│  │  ├─ 49
│  │  │  └─ 9448966a28ff20eb7ab2ffb6a3fd919d889d04
│  │  ├─ 5f
│  │  │  └─ 0516d1d8c52ce41406807d47ab4308d72816b5
│  │  ├─ 61
│  │  │  ├─ 56a083ad57d7e38109f50814607e443af91720
│  │  │  └─ e24edc033060cc4295f42afd56ba5a491207c7
│  │  ├─ 6a
│  │  │  └─ 3ce3f16dc547cf8767bdfe5e46f7ea978614e1
│  │  ├─ 72
│  │  │  └─ e72d676dfe54b5ed1a927209db6ec21739720f
│  │  ├─ 78
│  │  │  └─ ffb58a12398c549ca44964d2a3d5821f861540
│  │  ├─ 7c
│  │  │  └─ 5b012ba1256ca91208a8bc077a002cc763653f
│  │  ├─ 81
│  │  │  └─ 73323e814b522898f0cbff205840c9eb47e834
│  │  ├─ b6
│  │  │  └─ ac0307709b59eab9030f50e892645ee314262d
│  │  ├─ b7
│  │  │  └─ c7fd326c42381f7495b1c8acc4d74eda5f3544
│  │  ├─ b9
│  │  │  └─ 673fcdb82f8709c123723eb8d8d7fe8838f44f
│  │  ├─ c0
│  │  │  └─ 39796c1a35035f4ea3dfe4681033ede8d746c7
│  │  ├─ c8
│  │  │  └─ 544ed83166750c99e0ee883986e9504e2ae41b
│  │  ├─ ca
│  │  │  └─ 3c79ceae028f60ba2009446b558d1c9c1e6ad1
│  │  ├─ d4
│  │  │  └─ ed55ca120a7f1a01f8e175d78d7b003149b10e
│  │  ├─ e3
│  │  │  └─ 1582bda5e1d8950572da1439dddddf2bb41b6d
│  │  ├─ ed
│  │  │  ├─ 875aeec69d5ede0fd5d97d8a5b557623b113c7
│  │  │  └─ f930265562c8f9b1ce59f46d841ce1ce0f22cb
│  │  ├─ f2
│  │  │  └─ 4e15c463eac03e755b3e3ebef508c73fb08e56
│  │  ├─ info
│  │  └─ pack
│  │     ├─ pack-11c5baec2ac2df048484d2bcf9ccd789d400802f.idx
│  │     ├─ pack-11c5baec2ac2df048484d2bcf9ccd789d400802f.pack
│  │     └─ pack-11c5baec2ac2df048484d2bcf9ccd789d400802f.rev
│  ├─ ORIG_HEAD
│  ├─ packed-refs
│  └─ refs
│     ├─ heads
│     │  ├─ dev
│     │  └─ main
│     ├─ remotes
│     │  └─ origin
│     │     ├─ dev
│     │     ├─ HEAD
│     │     └─ main
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
│     │  ├─ views.py
│     │  ├─ wsgi.py
│     │  └─ __init__.py
│     ├─ README.md
│     ├─ requirements.txt
│     ├─ static
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