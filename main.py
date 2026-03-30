from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is active!"}

@app.get("/download")
def download_video(url: str):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'noplaylist': True,
        # ዩቲዩብን ለማለፍ የሚረዱ ጠንከር ያሉ Headers
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # መጀመሪያ መረጃውን ብቻ መሳብ
            info = ydl.extract_info(url, download=False)
            if not info:
                return {"status": "error", "message": "Could not extract info"}
                
            return {
                "status": "success",
                "title": info.get('title', 'No Title'),
                "url": info.get('url'),
                "thumbnail": info.get('thumbnail'),
                "platform": info.get('extractor_key')
            }
    except Exception as e:
        # ስህተቱን ለይቶ ለተጠቃሚው ለመንገር
        error_msg = str(e)
        if "confirm you're not a bot" in error_msg:
            return {"status": "error", "message": "YouTube blocked this request. Try TikTok or Instagram."}
        return {"status": "error", "message": error_msg}
