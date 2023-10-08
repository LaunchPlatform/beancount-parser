# beancount-parser [![CircleCI](https://circleci.com/gh/LaunchPlatform/beancount-parser/tree/master.svg?style=svg)](https://circleci.com/gh/LaunchPlatform/beancount-parser/tree/master)
Standalone [Lark](https://github.com/lark-parser/lark) LALR(1) based Beancount syntax parser (not relying on Beancount library), MIT license

Please also checkout out [beancount-black](https://github.com/LaunchPlatform/beancount-black), an opinionated beancount code formatter based on beancount-parser.

## Features

- **MIT licensed** - the only dependency is [Lark](https://github.com/lark-parser/lark)
- **Extremely fast** - LALR(1) is used
- **Section awareness** - emac org symbol mark `*` will be parsed
- **Comment awareness** - comments will be parsed
- **Not a validator** - it does not validate beancount syntax, invalid beancount syntax may still pass the parsing

# Sponsor

The original project beancount-parser was meant to be an internal tool built by [Launch Platform LLC](https://launchplatform.com) for 

<p align="center">
  <a href="https://beanhub.io"><img src="https://github.com/LaunchPlatform/beancount-black/raw/master/assets/beanhub.svg?raw=true" alt="BeanHub logo" /></a>
</p>

A modern accounting book service based on the most popular open source version control system [Git](https://git-scm.com/) and text-based double entry accounting book software [Beancount](https://beancount.github.io/docs/index.html).
We realized adding new entries with BeanHub automatically over time makes the beancount file a mess.
So, a strong code formatter is needed.
While SaaS businesses won't be required to open-source an internal tool like this, we still love that the service is only possible because of the open-source tool we are using.
It would be greatly beneficial for the community to access a tool like this, so we've decided to open-source it under an MIT license. We hope you find this tool useful 😄

## Install

To install the parser, simply run

```bash
pip install beancount-parser
```

## Usage

If you want to run the parse beancount code, you can do this

```python
import io

from beancount_parser.parser import make_parser

parser = make_parser()
tree = parser.parse(beancount_content)
# do whatever you want with the tree here
```

## Feedbacks

Feedbacks, bugs reporting or feature requests are welcome 🙌, just please open an issue.
No guarantee we have time to deal with them, but will see what we can do.
