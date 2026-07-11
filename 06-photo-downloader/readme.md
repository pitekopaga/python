# Photo Downloader & Organizer

A Python tool for downloading and organizing photos from any website with automatic naming and duplicate removal.

## Quick Start
1. Install Python 3.8+ from [python.org](https://python.org).
2. Install the required package: `pip install requests`
3. Download the two main files to the same folder:
   - [`photo_organizer.py`](https://github.com/pitekopaga/python/blob/main/06-photo-downloader/photo_organizer.py)
   - [`extract_urls.js`](https://github.com/pitekopaga/python/blob/main/06-photo-downloader/extract_urls.js)
4. Run the program: `python photo_organizer.py`

## How to Use
### Step 1: Get Photo URLs
1. Open your browser and go to the website with photos. Log in if needed.
2. Load ALL photos (scroll, click "Load more").
3. Press F12 → Console tab.
4. Copy and paste the code from [`extract_urls.js`](https://github.com/pitekopaga/python/blob/main/06-photo-downloader/extract_urls.js) and run `extractAllUrls()`.
5. Save the downloaded `extracted_photo_urls.txt` file.

### Step 2: Download Photos
1. Run: `python photo_organizer.py`
2. Select: `3` → `1` (Download Photos → Import from file)
3. Enter the path to your URLs file.
4. Choose dates: `y` (recommended for organization)
5. Enter the date range (oldest to newest photos).
6. Wait for the download to complete.

### Step 3: Organize Photos
1. From the main menu, select: `4` (Organize Downloaded Photos)
2. Press Enter for the default folder.
3. Wait for organization to complete.
4. Find your organized photos in the `photos_organized/` folder.

## Menu Options
* **Configure Settings** - Change folders, naming style
* **Browser Instructions** - How to extract URLs
* **Download Photos** - Main download function
* **Organize Photos** - Rename and organize
* **View Settings** - Check current configuration
* **Exit** - Quit the program

## Naming Examples
Choose a naming format in Settings → Option 2:
* `YYMMDD` → `240128a.jpg` (Jan 28, 2024, first photo)
* `YYYYMMDD` → `20240128a.jpg` (Same date, 4-digit year)
* `YYYY-MM-DD` → `2024-01-28a.jpg` (ISO format)

Multiple photos from the same day get letters: a, b, c, etc.

## Folder Structure
Copy this exact raw text below (including the blank lines and the backticks):

text
## Folder Structure
your_folder/
photo_organizer.py # Main program
extract_urls.js # Browser helper
config.json # Settings (auto-created)
photos_organized/ # Final organized photos
downloads_raw/ # Original downloads (backup)
thumbnails_backup/ # Removed thumbnails
duplicates_backup/ # Exact duplicates

text
If you paste that and it still doesn't work, try this alternative that uses indentation instead of code blocks:

text
## Folder Structure

    your_folder/
        photo_organizer.py     # Main program
        extract_urls.js        # Browser helper
        config.json            # Settings (auto-created)
        photos_organized/      # Final organized photos
        downloads_raw/         # Original downloads (backup)
        thumbnails_backup/     # Removed thumbnails
        duplicates_backup/     # Exact duplicates
I hope one of these works for y

## Troubleshooting
* **"python not found"**: Install Python from [python.org](https://python.org).
* **"requests not found"**: Run `pip install requests`.
* **URLs not downloading**: Use the JavaScript method and ensure you are logged in.
* **Wrong date order**: Settings → Option 3 → choose `newest_first` or `oldest_first`.

## Tips
* Load ALL photos before extracting URLs.
* Assign dates for better organization.
* Keep `downloads_raw/` as a backup.
* Process large collections in batches (200-300 at a time).

## Need Help?
* Run the program → Option 2 for detailed JavaScript instructions.
* Check `photos_organized/` for final results.
* Original files remain in `downloads_raw/` as backup.

Done! Your photos are now organized with clear, chronological names.
