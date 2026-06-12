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

MP3s land in `~/Music/spaces` named `Title [host] YYYY-MM-DD.mp3`.

```bash
# several at once
spaces-dl <url1> <url2> <url3>

# different browser / output dir, saved as the new defaults
spaces-dl -b firefox -o ~/Downloads/spaces --remember <url>

# debug a failing download
spaces-dl -v <url>
```

Config lives at `~/.config/spaces-dl/config.json`.

## Notes

- Only works for Spaces whose host enabled recording (and hasn't deleted the
  replay).
- macOS may prompt for keychain access the first time cookies are read from
  Chrome/Safari — that's expected.
- If downloads suddenly break, X probably changed something; `uv tool upgrade
  twitter-spaces-dl` to pull the yt-dlp fix.
