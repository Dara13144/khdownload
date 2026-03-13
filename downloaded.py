#!/usr/bin/env python3
"""
downloader.py - Core video downloader using yt-dlp
Supports TikTok, Facebook, YouTube, and many others.
"""

import os
import sys
import yt_dlp

def download_video(url, output_path):
    """
    Download the best quality video (prefer mp4) from the given URL.
    Returns the full path to the downloaded file, or None on failure.
    """
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        # 'format': 'best',  # simpler alternative
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': True,
        'restrictfilenames': True,  # avoid special characters
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # The actual filename may have a different extension; find it
            filename = ydl.prepare_filename(info)
            # If the file doesn't exist, try with the extension from info
            if not os.path.exists(filename):
                ext = info.get('ext', 'mp4')
                filename = filename.rsplit('.', 1)[0] + '.' + ext
            return filename
    except Exception as e:
        print(f"Download error: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python downloader.py <URL> <output_folder>")
        sys.exit(1)
    url = sys.argv[1]
    out = sys.argv[2]
    result = download_video(url, out)
    if result:
        print(f"SUCCESS:{result}")
    else:
        print("FAILED")
        sys.exit(1)
