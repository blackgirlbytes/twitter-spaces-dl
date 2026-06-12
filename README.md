# twitter-spaces-dl

Download recorded Twitter/X Spaces as MP3s. A small personal CLI wrapping
[yt-dlp](https://github.com/yt-dlp/yt-dlp) + ffmpeg.

## Install

Requires [uv](https://docs.astral.sh/uv/) (or pipx) and ffmpeg:

```bash
brew install uv ffmpeg
uv tool install git+https://github.com/blackgirlbytes/twitter-spaces-dl
```

To update later (picks up both your pushes and new yt-dlp releases):

```bash
uv tool upgrade twitter-spaces-dl
```

## Use

Be logged in to x.com in your browser (cookies are read from it — X requires
auth for Space replays), then:

```bash
spaces-dl https://x.com/i/spaces/1dRJZEpyjlNGB
```

MP3s land in `~/Documents/work/spaces` named `Title [host] YYYY-MM-DD.mp3`.

```bash
# pick your own filename instead of the Space title
spaces-dl -n "design review june" <url>     # -> design review june.mp3

# several at once
spaces-dl <url1> <url2> <url3>

# different browser / output dir, saved as the new defaults
spaces-dl -b firefox -o ~/Downloads/spaces --remember <url>

# debug a failing download
spaces-dl -v <url>
```

Config lives at `~/.config/spaces-dl/config.json`.

Copied Space links often end in `?s=20` (X's share tracking — harmless), but
zsh treats the `?` as a wildcard and errors with `no matches found` unless the
URL is quoted. To paste links bare, add this to `~/.zshrc`:

```bash
alias spaces-dl="noglob spaces-dl"
```

## Notes

- Only works for Spaces whose host enabled recording (and hasn't deleted the
  replay).
- macOS may prompt for keychain access the first time cookies are read from
  Chrome/Safari — that's expected.
- If downloads suddenly break, X probably changed something; `uv tool upgrade
  twitter-spaces-dl` to pull the yt-dlp fix.
