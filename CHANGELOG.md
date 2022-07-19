# Change Log

## [1.0.7] 2022-06-21
### Improvements

- UI Update: `Soft UI Dashboard` v1.0.6
- Enhanced version:
  - `Dark Mode`

## [1.0.6] 2022-05-25
### Improvements

- Built with [Soft UI Dashboard Generator](https://appseed.us/generator/soft-ui-dashboard/)
  - Timestamp: `2022-05-25 10:05`
- Added CDN/Static Server management
  - `ASSETS_ROOT` env variable

## [1.0.5] 2022-05-23
### Improvements 

- UI Update: `Soft UI Dashboard` v1.0.5
  - upgrade Bootstrap version to v5.1.3
  - upgrade ChartJs plugin version to v3.7.1
  - fix running 'npm install' issue
  - fix SCSS compiling issues
  - update sidebar height
  - fix sidebar button on Safari
  - update dropdown text on RTL page
  - fix navbar scroll error on example pages

## [1.0.4] 2022-01-16
### Improvements

- Bump Flask Codebase to [v2stable.0.1](https://github.com/app-generator/boilerplate-code-flask-dashboard/releases)
- Dependencies update (all packages) 
  - Flask==2.0.2 (latest stable version)
  - flask_wtf==1.0.0
  - jinja2==3.0.3
  - flask-restx==0.5.1
- Forms Update:
  - Replace `TextField` (deprecated) with `StringField`

## [1.0.3] 2021-12-09
### Improvements

- Bump UI: Soft UI Dashboard **v1.0.3**

## [1.0.2] 2021-11-08
### Improvements

- Bump Codebase: [Flask Dashboard](https://github.com/app-generator/boilerplate-code-flask-dashboard) v2.0.0
  - Dependencies update (all packages) 
    - Flask==2.0.1 (latest stable version)
- Better Code formatting
- Improved Files organization
- Optimize imports
- Docker Scripts Update
- Gulp Tooling  (SASS Compilation)
- Fix **ImportError: cannot import name 'TextField' from 'wtforms'**
  - Problem caused by `WTForms-3.0.0`
  - Fix: use **WTForms==2.3.3**

## [1.0.1] 2021-05-16
### Dependencies Update

- Bump Codebase: [Flask Dashboard](https://github.com/app-generator/boilerplate-code-flask-dashboard) v1.0.6
- Freeze used versions in `requirements.txt`
    - jinja2 = 2.11.3

## [1.0.0] 2021-05-12
### Initial Release

- UI: [Jinja Soft UI](https://github.com/app-generator/jinja-soft-ui-dashboard) v1.0.0
- Codebase: [Flask Dashboard](https://github.com/app-generator/boilerplate-code-flask-dashboard) v1.0.5
