import yt_dlp
import sys

def fetch_and_download():
    print("=============================================")
    print("                YT-DOWNLOADER                ")
    print("=============================================")
    url = input("Enter video URL: ").strip()
    
    if not url:
        print("No URL provided. Exiting.")
        return

    print("\nFetching available formats (this may take a moment)...")
    
    # 1. Fetch metadata without downloading
    fetch_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(fetch_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return

    # 2. Display formatted options
    print(f"\nTitle: {info.get('title')}")
    print(f"{'ID':<15} | {'Resolution':<12} | {'Ext':<6} | {'Details'}")
    print("-" * 65)
    
    for f in info.get('formats', []):
        # Filter out garbage data and show formats that contain video
        if f.get('vcodec') != 'none' and f.get('resolution') != 'audio only':
            f_id = f.get('format_id', 'N/A')
            res = f.get('resolution', 'Unknown')
            ext = f.get('ext', 'N/A')
            acodec = f.get('acodec', 'none')
            
            # YouTube separates HD video and audio. 
            audio_stat = "Included" if acodec != 'none' else "Video Only"
            print(f"{f_id:<15} | {res:<12} | {ext:<6} | {audio_stat}")

    # 3. Handle User Input
    print("-" * 65)
    print("PRO TIP: If you choose a 'Video Only' ID (like 1080p), type your ID")
    print("followed by '+bestaudio' to automatically merge them (e.g., 137+bestaudio).")
    
    chosen_format = input("\nEnter the format ID to download: ").strip()

    if not chosen_format:
        print("Download cancelled.")
        return

    # 4. Execute Download
    print(f"\nDownloading format: {chosen_format}...")
    download_opts = {
        'format': chosen_format,
        'outtmpl': '%(title)s.%(ext)s', # Saves to the directory where the script is run
    }
    
    try:
        with yt_dlp.YoutubeDL(download_opts) as ydl:
            ydl.download([url])
        print("\nDownload complete!")
    except Exception as e:
        print(f"\nDownload failed: {e}")

if __name__ == "__main__":
    try:
        fetch_and_download()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)