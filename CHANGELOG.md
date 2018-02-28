# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog] and this project adheres to [Semantic Versioning].

[Keep a Changelog]: http://keepachangelog.com/en/1.0.0/
[Semantic Versioning]: http://semver.org/spec/v2.0.0.html

---

## Unreleased

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
