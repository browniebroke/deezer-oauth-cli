# Deezer OAuth CLI

<p align="center">
  <a href="https://github.com/browniebroke/deezer-oauth-cli/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/browniebroke/deezer-oauth-cli/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://codecov.io/gh/browniebroke/deezer-oauth-cli">
    <img src="https://img.shields.io/codecov/c/github/browniebroke/deezer-oauth-cli.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/deezer-oauth-cli/">
    <img src="https://img.shields.io/pypi/v/deezer-oauth-cli.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/deezer-oauth-cli.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/deezer-oauth-cli.svg?style=flat-square" alt="License">
</p>

---

**Source Code**: <a href="https://github.com/browniebroke/deezer-oauth-cli" target="_blank">https://github.com/browniebroke/deezer-oauth-cli</a>

---

A small CLI to quickly obtain an API token for the Deezer API.

Obtaining API token to develop API applications can be complicated and sometimes feel like a chicken and egg situation: it's hard to play with the API without a token, but it can be difficult to get a token without an application to do the OAuth flow.

Given the app ID and secret, this tool lets you quickly get an API token.

## Installation

Install this via pip (or your favourite package manager):

`pip install deezer-oauth-cli`

## Usage

Before starting to use this tool, you first need to declare your Deezer app in [their developer portal](https://developers.deezer.com). Create a new app with the following Redirect URL: `http://localhost:8080/oauth/return`.

Once created, Deezer will generate an application ID and secret key for you, that's the 2 parameters that you need to run this tool:

```shell
$ deezer-oauth APP_ID APP_SECRET
```

This will:

- Spin up a webserver in the background running at `http://localhost:8080`.
- Open your browser to grant authorisation access to your Deezer account.
- Redirect to a page showing the API token & expiry.
- Write the token to a `.env` file.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- prettier-ignore-start -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://browniebroke.com/"><img src="https://avatars.githubusercontent.com/u/861044?v=4?s=80" width="80px;" alt="Bruno Alla"/><br /><sub><b>Bruno Alla</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-oauth-cli/commits?author=browniebroke" title="Code">💻</a> <a href="#ideas-browniebroke" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/browniebroke/deezer-oauth-cli/commits?author=browniebroke" title="Documentation">📖</a></td>
      <td align="center"><a href="https://github.com/prndrbr"><img src="https://avatars.githubusercontent.com/u/96344856?v=4?s=80" width="80px;" alt="Pierre"/><br /><sub><b>Pierre</b></sub></a><br /><a href="https://github.com/browniebroke/deezer-oauth-cli/commits?author=prndrbr" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-end -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[browniebroke/cookiecutter-pypackage](https://github.com/browniebroke/cookiecutter-pypackage)
project template.
