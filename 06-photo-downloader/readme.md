# Photo Downloader & Organizer

A Python tool for downloading and organizing photos from any website with automatic naming and duplicate removal.

## Quick Start

1. **Install Python 3.8+** from [python.org](https://python.org)

2. **Install required package:**
   ```bash
   pip install requests
Download these two files to the same folder:

photo_organizer.py (main Python program)

extract_urls.js (browser helper script)

Run the program:

bash
python photo_organizer.py
How to Use
Step 1: Get Photo URLs
Open your browser, go to website with photos, log in if needed

Load ALL photos (scroll, click "Load more")

Press F12 → Console tab

Copy/paste code from extract_urls.js

Run extractAllUrls() in Console

Save the downloaded extracted_photo_urls.txt file

Step 2: Download Photos
Run: python photo_organizer.py

Select: 3 → 1 (Download Photos → Import from file)

Enter path to your URLs file

Choose dates: y (recommended for organization)

Enter date range (oldest to newest photos)

Wait for download to complete

Step 3: Organize Photos
Back in main menu, select: 4 (Organize Downloaded Photos)

Press Enter for default folder

Wait for organization to complete

Find your organized photos in photos_organized/ folder

Menu Options

1. Configure Settings    - Change folders, naming style
2. Browser Instructions - How to extract URLs
3. Download Photos      - Main download function
4. Organize Photos      - Rename and organize
5. View Settings        - Check current configuration
6. Exit                 - Quit program
Naming Examples
Choose format in Settings → Option 2:

Format	Example	Result
YYMMDD	240128a.jpg	Jan 28, 2024, first photo
YYYYMMDD	20240128a.jpg	Same date, 4-digit year
YYYY-MM-DD	2024-01-28a.jpg	ISO format
Multiple photos same day get letters: a, b, c, etc.

Folder Structure

your_folder/
├── photo_organizer.py      # Main program
├── extract_urls.js         # Browser helper
├── config.json             # Settings (auto-created)
├── photos_organized/       # ✅ Final organized photos
├── downloads_raw/          # Original downloads (backup)
├── thumbnails_backup/      # Removed thumbnails
└── duplicates_backup/      # Exact duplicates
Troubleshooting
"python not found": Install Python from python.org

"requests not found": Run pip install requests

URLs not downloading: Use JavaScript method, ensure logged in

Wrong date order: Settings → Option 3 → choose newest_first or oldest_first

Tips
Load ALL photos before extracting URLs

Assign dates for better organization

Keep downloads_raw/ as backup

Process large collections in batches (200-300 at a time)

Need Help?
Run program → Option 2 for detailed JavaScript instructions

Check photos_organized/ for final results

Original files remain in downloads_raw/ as backup

Done! Your photos are now organized with clear, chronological names.