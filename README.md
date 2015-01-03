# pylsdj


[![Documentation Status](https://readthedocs.org/projects/pylsdj/badge/?version=latest)](https://readthedocs.org/projects/pylsdj/?badge=latest)

pylsdj is a suite of tools for reading, writing and editing LSDJ’s save data,
which includes the user’s saved songs and instruments.

## Why?

Before pylsdj, the suite of tools available for interacting with LSDJ’s save
data was sparse and fragmented. People who wanted to share and re-use
instruments between songs or move songs between saves were met with partial
solutions at best. pylsdj endeavors to be a one-stop solution for save data
reading, writing and editing.

## How Can I Help?

First and foremost, use it! You can also try out [LSMC][lsmc], which is really
just a GUI on top of many of pylsdj’s functions.

Second, if you find a bug, file it. I know I haven’t hit all the potential use
cases for this in tests, and your input will help me find and squash bugs.

Third, if you’re a developer, write some tests. If you find a feature pylsdj
doesn’t have and you want to take a crack at it, fork the code and send me a
pull request. I’m ready and willing to receive contributions from the
community.

## Known Limitations

pylsdj only works on save data for LSDJ versions 3.0.0 and above. Given that
version 3.0.0 came out back in 2006 and marked a significant change in file
structure since then, I feel like this is a reasonable point at which to freeze
backwards-compatibility.

This codebase grew rather organically over a period of several years, and some
of it is a lot more complex than I'd like it to be. However, perfect is the
enemy of done. If you'd like to help me clean it up or make it faster, have at
it.

[lsmc]: https://www.github.com/alexras/lsmc/
