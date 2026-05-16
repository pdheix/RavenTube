#!/usr/bin/env python3
import json, os, subprocess, sys, glob, shutil, time, re
from pathlib import Path

with open("download.json", "r", encoding="utf-8") as f:
    data = json.load(f)

settings = data.get("settings", {})
quality = settings.get("quality", "best")
subtitles = settings.get("subtitles", False)
mp3 = settings.get("mp3", False)
password = settings.get("password", "")

urls = data.get("videos", [])
if not urls:
    print("No videos in JSON. Exiting.", flush=True)
    sys.exit(0)

if mp3 or quality == "audio":
    fmt = "bestaudio/best"
    is_audio = True
elif quality == "best":
    fmt = "bestvideo+bestaudio/best"
    is_audio = False
else:
    try:
        h = int(quality)
        fmt = f"bestvideo[height<={h}]+bestaudio/best[height<={h}]"
    except:
        fmt = "bestvideo+bestaudio/best"
    is_audio = False

split_mb = 45
split_bytes = split_mb * 1024 * 1024

repo_owner = os.environ["GITHUB_REPOSITORY_OWNER"]
repo_name = os.environ["GITHUB_REPOSITORY"].split("/")[1]
branch = os.environ["GITHUB_REF_NAME"]

Path("videos").mkdir(exist_ok=True)
info_lines = []

cookies_flag = []
if os.path.exists("cookies.txt"):
    cookies_flag = ["--cookies", "cookies.txt"]
    print("Using cookies.txt for authentication", flush=True)

for idx, url in enumerate(urls, 1):
    print(f"\n===== [{idx}/{len(urls)}] {url} =====", flush=True)
    tmp = f"tmp_{idx}"
    os.makedirs(tmp, exist_ok=True)

    base_cmd = [
        "yt-dlp",
        "--no-playlist",
        "--retries", "5",
        "--fragment-retries", "5",
        "--no-check-certificates",
        "--no-cache-dir",
        "--js-runtimes", "deno",
        "--remote-components", "ejs:github",   # fix JS challenges
        "--output", "%(title)s.%(ext)s"        # no tmp prefix, cwd=tmp handles location
    ] + cookies_flag

    if is_audio:
        base_cmd += ["--extract-audio", "--audio-format", "mp3", "--audio-quality", "0"]
    else:
        base_cmd += ["--merge-output-format", "mp4", "--write-thumbnail", "--convert-thumbnails", "jpg"]
    if subtitles and not is_audio:
        base_cmd += ["--write-subs", "--sub-lang", "fa,en", "--embed-subs"]

    base_cmd += ["--format", fmt]

    methods = [
        ["--proxy", "socks5://127.0.0.1:1080", "--extractor-args", "youtube:player_client=web"],
        ["--proxy", "socks5://127.0.0.1:1080", "--extractor-args", "youtube:player_client=ios"],
        ["--proxy", "socks5://127.0.0.1:1080", "--extractor-args", "youtube:player_client=android"],
        ["--extractor-args", "youtube:player_client=ios"],
        ["--extractor-args", "youtube:player_client=android"],
        ["--extractor-args", "youtube:player_client=web"],
        ["--extractor-args", "youtube:player_client=mweb"],
        []
    ]

    success = False
    for method in methods:
        cmd = base_cmd + method + [url]
        print("Trying:", " ".join(method) if method else "no extra args", flush=True)
        if subprocess.run(cmd, cwd=tmp).returncode == 0:
            success = True
            break
        time.sleep(3)

    if not success:
        print(f"FAILED: {url}", flush=True)
        shutil.rmtree(tmp)
        continue

    for f in glob.glob(f"{tmp}/*.part"):
        os.remove(f)

    media_file = None
    for f in os.listdir(tmp):
        if f.endswith((".mp4", ".webm", ".mkv", ".mp3")):
            media_file = os.path.join(tmp, f)
            break
    if not media_file:
        print("No media file found.", flush=True)
        shutil.rmtree(tmp)
        continue

    filename_no_ext = Path(media_file).stem
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '', filename_no_ext.replace(" ", "-"))
    ext = Path(media_file).suffix[1:]

    timestamp = int(time.time())
    folder = f"{safe_name}_{timestamp}_{os.getpid()}"
    folder_path = Path("videos") / folder
    folder_path.mkdir(parents=True, exist_ok=True)

    thumb = None
    for tf in glob.glob(f"{tmp}/*.jpg"):
        thumb = tf
        break
    if thumb:
        shutil.copy(thumb, folder_path / "thumbnail.jpg")

    file_size = os.path.getsize(media_file)
    size_mb = round(file_size / (1024 * 1024), 2)

    if file_size > split_bytes:
        split_flag = True
        zip_base = folder_path / safe_name
        if password:
            subprocess.run(["zip", "-P", password, "-0", "-s", f"{split_mb}m", f"{zip_base}.zip", media_file], check=True)
        else:
            subprocess.run(["zip", "-0", "-s", f"{split_mb}m", f"{zip_base}.zip", media_file], check=True)
    else:
        split_flag = False
        dest = folder_path / f"{safe_name}.{ext}"
        if password:
            subprocess.run(["zip", "-P", password, "-0", f"{folder_path}/{safe_name}.zip", media_file], check=True)
        else:
            shutil.copy(media_file, dest)

    readme = folder_path / "README.md"
    has_pass = "YES" if password else "NO"
    with open(readme, "w") as rf:
        rf.write(f"# {filename_no_ext}\n\n")
        if thumb:
            rf.write(f'<img src="thumbnail.jpg" width="250"/>\n\n')
        rf.write(f"| Property | Value |\n|----------|-------|\n")
        rf.write(f"| **Quality** | {quality} |\n")
        rf.write(f"| **Size** | {size_mb} MB |\n")
        rf.write(f"| **Password** | {has_pass} |\n\n")
        rf.write("## Download Link\n\n")
        folder_enc = folder.replace(" ", "%20")
        if split_flag:
            parts = sorted(glob.glob(f"{folder_path}/{safe_name}.zip*"))
            rf.write(f"| **Total Size** | {size_mb} MB ({len(parts)} parts) |\n\n")
            for part_file in parts:
                pname = os.path.basename(part_file)
                penc = pname.replace(" ", "%20")
                rf.write(f"| `{pname}` | [Download](https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/videos/{folder_enc}/{penc}) |\n")
        else:
            fname = f"{safe_name}.{ext}" if not password else f"{safe_name}.zip"
            fenc = fname.replace(" ", "%20")
            rf.write(f"| `{fname}` | [Download](https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/videos/{folder_enc}/{fenc}) |\n")

    info_lines.append(f"{filename_no_ext}|{folder}")
    shutil.rmtree(tmp)

master = Path("videos") / "README.md"
with open(master, "w") as mf:
    mf.write("# RavenTube Downloads\n\n")
    mf.write("| # | Video | Folder |\n|---|---|---|\n")
    for i, line in enumerate(info_lines, 1):
        name, fold = line.split("|")
        fold_enc = fold.replace(" ", "%20")
        mf.write(f"| {i} | {name} | [Open](https://github.com/{repo_owner}/{repo_name}/tree/{branch}/videos/{fold_enc}) |\n")

with open("urls.txt", "w") as uf:
    uf.write("\n".join(urls))
)
print("\nDone. All files prepared.", flush=True)
