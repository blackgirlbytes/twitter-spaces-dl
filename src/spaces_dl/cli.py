"""spaces-dl: download recorded Twitter/X Spaces as MP3s.

Thin wrapper around yt-dlp. X requires a logged-in session for Space
replays, so cookies are pulled from a local browser profile.
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

CONFIG_PATH = Path.home() / ".config" / "spaces-dl" / "config.json"

DEFAULTS = {
    "output_dir": str(Path.home() / "Documents" / "work" / "spaces"),
    "browser": "chrome",
}

SUPPORTED_BROWSERS = (
    "brave", "chrome", "chromium", "edge", "firefox", "opera", "safari", "vivaldi", "whale",
)


def load_config() -> dict:
    try:
        with open(CONFIG_PATH) as f:
            return {**DEFAULTS, **json.load(f)}
    except (OSError, json.JSONDecodeError):
        return dict(DEFAULTS)


def save_config(config: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def build_parser(config: dict) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="spaces-dl",
        description="Download recorded Twitter/X Spaces as MP3s.",
        epilog=(
            "Cookies are read from your browser, so stay logged in to x.com there. "
            "Pass --remember to save --output-dir/--browser as defaults "
            f"({CONFIG_PATH})."
        ),
    )
    parser.add_argument(
        "urls",
        nargs="+",
        metavar="URL",
        help="one or more Space URLs (https://x.com/i/spaces/...)",
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=config["output_dir"],
        help=f"where to put MP3s (default: {config['output_dir']})",
    )
    parser.add_argument(
        "-n", "--name",
        help='save the MP3 under this name instead of the Space title, e.g. -n "team standup" (single URL only)',
    )
    parser.add_argument(
        "-b", "--browser",
        default=config["browser"],
        choices=SUPPORTED_BROWSERS,
        help=f"browser to read x.com cookies from (default: {config['browser']})",
    )
    parser.add_argument(
        "--remember",
        action="store_true",
        help="save the output dir and browser from this run as defaults",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="show full yt-dlp output",
    )
    return parser


def download(
    urls: list[str], output_dir: Path, browser: str, verbose: bool, name: str | None = None
) -> list[str]:
    """Download each URL as an MP3 into output_dir. Returns the URLs that failed."""
    if name:
        stem = name.removesuffix(".mp3")
        # % is yt-dlp template syntax; escape any in the user's name
        outtmpl = stem.replace("%", "%%") + ".%(ext)s"
    else:
        outtmpl = "%(title)s [%(uploader)s] %(upload_date>%Y-%m-%d|undated)s.%(ext)s"
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / outtmpl),
        "cookiesfrombrowser": (browser,),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "0",
            }
        ],
        "quiet": not verbose,
        "no_warnings": not verbose,
        "noprogress": False,
        # Replays are HLS; grab from the first chunk even if X marks the
        # stream as live-ish.
        "live_from_start": True,
    }

    failed = []
    with YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            print(f"==> {url}")
            try:
                ydl.download([url])
            except DownloadError as e:
                failed.append(url)
                print(f"    failed: {e}", file=sys.stderr)
    return failed


def main() -> None:
    config = load_config()
    parser = build_parser(config)
    args = parser.parse_args()

    if args.name and len(args.urls) > 1:
        parser.error("--name only works with a single URL (the files would overwrite each other)")

    if shutil.which("ffmpeg") is None:
        sys.exit(
            "spaces-dl: ffmpeg not found. Install it first (macOS: brew install ffmpeg)."
        )

    if args.remember:
        save_config({"output_dir": args.output_dir, "browser": args.browser})
        print(f"Saved defaults to {CONFIG_PATH}")

    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    failed = download(args.urls, output_dir, args.browser, args.verbose, args.name)

    done = len(args.urls) - len(failed)
    if done:
        print(f"Done: {done} MP3{'s' if done != 1 else ''} in {output_dir}")
    if failed:
        print(
            "Failed:\n  " + "\n  ".join(failed) + "\n"
            "Common causes: not logged in to x.com in "
            f"{args.browser} (try -b <browser>), the replay was deleted, or the "
            "host never enabled recording.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
