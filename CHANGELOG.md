# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog] and this project adheres to [Semantic Versioning].

[Keep a Changelog]: http://keepachangelog.com/en/1.0.0/
[Semantic Versioning]: http://semver.org/spec/v2.0.0.html

---

## Unreleased

### Added

- Support travis-ci

---

## [v0.9.0] - 2018/08/11

### Added

- Add `pipenv run exec`
- Add `post-query-filters`

### Remove

- Remove XmlStrategy.post_query(), use `post-query-filters`

---

## [v0.8.0] - 2018/05/12

### Added

- Add version option `--version`
- Support pipenv

### Remove

- Remove requirements.txt, use pipfile instead

---

## [v0.7.0] - 2018/03/25

### Changed

- Divide `kamoshika.py` into several files
- Remove `responce` (typo of "response") field from `sample.yml` because change `kamoshika.py` behavior not to refer the field

[v0.7.0]: https://github.com/km45/kamoshika/releases/tag/v0.7.0

---

## [v0.6.0] - 2018/03/24

### Changed

- Change directory layout

[v0.6.0]: https://github.com/km45/kamoshika/releases/tag/v0.6.0

---

## [v0.5.0] - 2018/03/21

### Changed

- Change repository name
- Change script name and default config file name

[v0.5.0]: https://github.com/km45/kamoshika/releases/tag/v0.5.0

---

## [v0.4.0] - 2018/03/01

### Added

- Add log level option `--log-level`

### Changed

- Change default log level from ERROR to INFO

### Removed

- Remove verbose options `-v` / `-vv` / `-vvv` (use `--log-level` instead of them)

[v0.4.0]: https://github.com/km45/responce-diff-checker/releases/tag/v0.4.0

---

## [v0.3.0] - 2018/01/29

### Added

- Support non UTF-8 file for post process xml

[v0.3.0]: https://github.com/km45/responce-diff-checker/releases/tag/v0.3.0

---

## [v0.2.1] - 2018/01/29

### Changed

- Remove a dependency for an external command xmllint

[v0.2.1]: https://github.com/km45/responce-diff-checker/releases/tag/v0.2.1

---

## [v0.2.0] - 2018/01/17

### Added

- Add post process mode xml

### Fixed

- Remove output directory only when target directory already exists

[v0.2.0]: https://github.com/km45/responce-diff-checker/releases/tag/v0.2.0

---

## [v0.1.0] - 2018/01/16

### Added

- Add main script file `diff_checker.py`
- Add dependencies as `requirements.txt`
- Add config file `diff_checker.yml`
- Add development helper script file `develop_helper_server.py`
- Add license file `LICENCE`
- Add document files `CHANGELOG.md` and `README.md`
- Add `.gitignore`

[v0.1.0]: https://github.com/km45/responce-diff-checker/releases/tag/v0.1.0
