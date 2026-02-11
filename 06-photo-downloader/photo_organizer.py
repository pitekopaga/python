"""
Photo Downloader & Organizer
============================

A general-purpose tool for downloading and organizing photos from websites
with automatic chronological naming and duplicate removal.

Features:
- Bulk photo downloading from any website
- Multiple URL input methods (file, clipboard, manual)
- Smart duplicate removal (thumbnails, exact duplicates)
- Flexible naming conventions
- Date-based organization
- Cross-platform compatibility

Usage:
    python photo_organizer.py
"""

import os
import re
import json
import time
import shutil
import hashlib
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Tuple, Dict, Optional
import sys
import webbrowser
import subprocess

class PhotoOrganizer:
    """Main class for downloading and organizing photos from websites"""
    
    def __init__(self):
        self.config_file = "config.json"
        self.config = self.load_config()
        self.setup_folders()
    
    def load_config(self) -> Dict:
        """Load or create configuration file"""
        default_config = {
            "download_folder": "downloads_raw",
            "organized_folder": "photos_organized",
            "thumbnails_folder": "thumbnails_backup",
            "duplicates_folder": "duplicates_backup",
            "naming_convention": "YYMMDD",  # Options: YYMMDD, YYYYMMDD, MMDDYY, etc.
            "date_order": "newest_first",   # newest_first or oldest_first
            "min_file_size_kb": 100,        # Minimum file size to keep
            "download_delay": 0.2,          # Delay between downloads
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in default_config.items():
                    if key not in loaded_config:
                        loaded_config[key] = value
                return loaded_config
            except:
                print("Error loading config, using defaults")
                return default_config
        else:
            return default_config
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_folders(self):
        """Create necessary folders for organization"""
        folders = [
            self.config["download_folder"],
            self.config["organized_folder"],
            self.config["thumbnails_folder"],
            self.config["duplicates_folder"]
        ]
        
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
    
    def show_main_menu(self):
        """Display main menu and get user choice"""
        print("\n" + "="*70)
        print("PHOTO DOWNLOADER & ORGANIZER")
        print("="*70)
        print("\nMain Menu:")
        print("  1. Configure Settings")
        print("  2. Extract URLs from Website (Browser Method)")
        print("  3. Download Photos from URLs")
        print("  4. Organize Downloaded Photos")
        print("  5. View Current Configuration")
        print("  6. Exit")
        print("="*70)
        
        while True:
            try:
                choice = int(input("\nSelect option (1-6): ").strip())
                if 1 <= choice <= 6:
                    return choice
                else:
                    print("Please enter a number between 1 and 6")
            except ValueError:
                print("Please enter a valid number")
    
    def configure_settings(self):
        """Allow user to configure application settings"""
        print("\n" + "="*70)
        print("CONFIGURATION SETTINGS")
        print("="*70)
        
        print("\nCurrent Configuration:")
        for key, value in self.config.items():
            print(f"  {key}: {value}")
        
        print("\nConfigure Settings:")
        print("  1. Change download folder")
        print("  2. Change naming convention")
        print("  3. Change date order")
        print("  4. Change minimum file size")
        print("  5. Return to main menu")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            new_folder = input(f"Enter new download folder [current: {self.config['download_folder']}]: ").strip()
            if new_folder:
                self.config["download_folder"] = new_folder
                os.makedirs(new_folder, exist_ok=True)
        
        elif choice == "2":
            print("\nAvailable Naming Conventions:")
            print("  YYMMDD - 250128 (YearMonthDay, 2-digit year)")
            print("  YYYYMMDD - 20250128 (YearMonthDay, 4-digit year)")
            print("  MMDDYY - 012825 (MonthDayYear)")
            print("  DDMMYY - 280125 (DayMonthYear)")
            print("  YYYY-MM-DD - 2025-01-28 (ISO format)")
            
            new_convention = input(f"\nEnter naming convention [current: {self.config['naming_convention']}]: ").strip().upper()
            if new_convention in ["YYMMDD", "YYYYMMDD", "MMDDYY", "DDMMYY", "YYYY-MM-DD"]:
                self.config["naming_convention"] = new_convention
            else:
                print("Invalid convention. Keeping current.")
        
        elif choice == "3":
            print("\nDate Order Options:")
            print("  newest_first - Most recent photos first")
            print("  oldest_first - Oldest photos first")
            
            new_order = input(f"\nEnter date order [current: {self.config['date_order']}]: ").strip()
            if new_order in ["newest_first", "oldest_first"]:
                self.config["date_order"] = new_order
            else:
                print("Invalid order. Keeping current.")
        
        elif choice == "4":
            try:
                new_size = int(input(f"\nEnter minimum file size in KB [current: {self.config['min_file_size_kb']}]: ").strip())
                if new_size > 0:
                    self.config["min_file_size_kb"] = new_size
            except:
                print("Invalid size. Keeping current.")
        
        self.save_config()
        print("\n✅ Configuration updated!")
    
    def show_javascript_instructions(self):
        """Display instructions for using JavaScript URL extraction"""
        print("\n" + "="*70)
        print("URL EXTRACTION INSTRUCTIONS")
        print("="*70)
        
        print("\n📋 METHOD 1: Using provided JavaScript file")
        print("  1. Open your browser and navigate to the website with photos")
        print("  2. Log in if necessary and load all photos (scroll/click 'Load more')")
        print("  3. Press F12 to open Developer Tools")
        print("  4. Go to the Console tab")
        print("  5. Copy the code from 'extract_urls.js' file")
        print("  6. Paste it into the Console and press Enter")
        print("  7. Follow the on-screen instructions")
        
        print("\n📋 METHOD 2: Manual URL collection")
        print("  1. Save all image URLs to a text file (one per line)")
        print("  2. Use option 3 in main menu to import the file")
        
        print("\n📋 METHOD 3: Browser extensions")
        print("  1. Install 'Image Downloader' or similar extension")
        print("  2. Use it to extract URLs from the page")
        
        print("\nThe extracted URLs file should contain one URL per line.")
        print("Example:")
        print("  https://example.com/photos/photo1.jpg")
        print("  https://example.com/photos/photo2.jpg")
        print("  https://example.com/photos/photo3.jpg")
        print("="*70)
        
        input("\nPress Enter to return to main menu...")
    
    def get_urls_from_user(self) -> List[str]:
        """Get photo URLs from user through various methods"""
        print("\n" + "="*70)
        print("GET PHOTO URLs")
        print("="*70)
        print("\nOptions:")
        print("  1. Import from text file")
        print("  2. Paste URLs manually")
        print("  3. Use URLs from clipboard")
        print("  4. Cancel")
        
        choice = input("\nSelect option (1-4): ").strip()
        urls = []
        
        if choice == "1":
            filepath = input("\nEnter path to URLs file: ").strip()
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip()]
                print(f"Loaded {len(urls)} URLs from file")
            else:
                print("File not found!")
        
        elif choice == "2":
            print("\nPaste URLs (one per line). Enter 'done' on a new line when finished:")
            while True:
                line = input().strip()
                if line.lower() == 'done':
                    break
                if line and (line.startswith('http://') or line.startswith('https://')):
                    urls.append(line)
            print(f"Added {len(urls)} URLs")
        
        elif choice == "3":
            try:
                import pyperclip
                clipboard = pyperclip.paste()
                if clipboard:
                    urls = [line.strip() for line in clipboard.split('\n') if line.strip()]
                    print(f"Found {len(urls)} URLs in clipboard")
                else:
                    print("Clipboard is empty")
            except ImportError:
                print("Install pyperclip first: pip install pyperclip")
        
        return urls
    
    def download_photos(self, urls: List[str], start_date: Optional[datetime] = None, 
                       end_date: Optional[datetime] = None) -> List[Tuple[str, datetime]]:
        """Download photos and optionally assign dates"""
        if not urls:
            print("No URLs to download")
            return []
        
        print(f"\nDownloading {len(urls)} photos...")
        
        # Ask about dates if not provided
        assign_dates = False
        if start_date is None or end_date is None:
            date_choice = input("\nAssign dates to photos? (y/n): ").strip().lower()
            if date_choice == 'y':
                assign_dates = True
                start_date_str = input("Start date (YYYY-MM-DD, e.g., 2025-01-01): ").strip()
                end_date_str = input("End date (YYYY-MM-DD, e.g., 2025-12-31): ").strip()
                
                try:
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                    print(f"Date range: {start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}")
                except:
                    print("Invalid date format. Proceeding without dates.")
                    assign_dates = False
        
        downloaded_files = []
        download_folder = self.config["download_folder"]
        
        for i, url in enumerate(urls):
            try:
                # Download image
                headers = {'User-Agent': self.config["user_agent"]}
                response = requests.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                
                # Check if it's an image
                content_type = response.headers.get('content-type', '').lower()
                if 'image' not in content_type:
                    print(f"  Skipping non-image: {url}")
                    continue
                
                # Generate filename
                ext = self.get_file_extension(content_type, url)
                temp_name = f"photo_{i+1:04d}{ext}"
                temp_path = os.path.join(download_folder, temp_name)
                
                # Save file
                with open(temp_path, 'wb') as f:
                    f.write(response.content)
                
                # Assign date if requested
                photo_date = None
                if assign_dates and start_date and end_date:
                    total_days = (end_date - start_date).days
                    progress = i / (len(urls) - 1) if len(urls) > 1 else 0
                    if self.config["date_order"] == "newest_first":
                        days_from_end = int(total_days * progress)
                        photo_date = end_date - timedelta(days=days_from_end)
                    else:
                        days_from_start = int(total_days * progress)
                        photo_date = start_date + timedelta(days=days_from_start)
                
                downloaded_files.append((temp_path, photo_date))
                
                # Progress indicator
                if (i + 1) % 10 == 0:
                    print(f"  Downloaded {i+1}/{len(urls)}...")
                
                # Delay to be nice to server
                time.sleep(self.config["download_delay"])
                
            except Exception as e:
                print(f"  Failed to download: {str(e)[:50]}")
                continue
        
        print(f"\n✅ Successfully downloaded {len(downloaded_files)} photos")
        return downloaded_files
    
    def get_file_extension(self, content_type: str, url: str) -> str:
        """Determine file extension from content type or URL"""
        # Try content type first
        if 'jpeg' in content_type or 'jpg' in content_type:
            return '.jpg'
        elif 'png' in content_type:
            return '.png'
        elif 'gif' in content_type:
            return '.gif'
        elif 'webp' in content_type:
            return '.webp'
        
        # Fall back to URL extension
        url_lower = url.lower()
        if url_lower.endswith('.jpg') or url_lower.endswith('.jpeg'):
            return '.jpg'
        elif url_lower.endswith('.png'):
            return '.png'
        elif url_lower.endswith('.gif'):
            return '.gif'
        elif url_lower.endswith('.webp'):
            return '.webp'
        
        # Default
        return '.jpg'
    
    def remove_duplicates(self, folder_path: str) -> List[str]:
        """Remove thumbnail duplicates and return unique files"""
        print(f"\nAnalyzing {folder_path} for duplicates...")
        
        all_files = []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                filepath = os.path.join(folder_path, filename)
                all_files.append(filepath)
        
        print(f"  Found {len(all_files)} image files")
        
        # Remove thumbnails based on size and filename
        thumb_files = []
        candidate_files = []
        min_size_kb = self.config["min_file_size_kb"]
        
        for filepath in all_files:
            size_kb = os.path.getsize(filepath) / 1024
            filename = os.path.basename(filepath).lower()
            
            # Check for thumbnail indicators
            is_thumbnail = (
                size_kb < min_size_kb or
                'thumb' in filename or
                'thumbnail' in filename or
                '_sm' in filename or
                '_xs' in filename or
                '-small' in filename or
                'mini' in filename
            )
            
            if is_thumbnail:
                thumb_files.append(filepath)
            else:
                candidate_files.append(filepath)
        
        # Move thumbnails to backup folder
        if thumb_files:
            thumb_folder = self.config["thumbnails_folder"]
            for thumb_file in thumb_files:
                filename = os.path.basename(thumb_file)
                dest_path = os.path.join(thumb_folder, filename)
                shutil.move(thumb_file, dest_path)
            print(f"  Moved {len(thumb_files)} thumbnails to backup")
        
        # Remove exact duplicates by hash
        unique_files = []
        seen_hashes = set()
        dup_count = 0
        
        for filepath in candidate_files:
            file_hash = self.get_file_hash(filepath)
            if file_hash not in seen_hashes:
                seen_hashes.add(file_hash)
                unique_files.append(filepath)
            else:
                dup_folder = self.config["duplicates_folder"]
                filename = os.path.basename(filepath)
                dest_path = os.path.join(dup_folder, filename)
                shutil.move(filepath, dest_path)
                dup_count += 1
        
        if dup_count > 0:
            print(f"  Removed {dup_count} exact duplicates")
        
        print(f"  Kept {len(unique_files)} unique photos")
        return unique_files
    
    def get_file_hash(self, filepath: str) -> str:
        """Calculate MD5 hash of a file"""
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def organize_photos(self, files_with_dates: List[Tuple[str, Optional[datetime]]]):
        """Organize photos with user-specified naming convention"""
        if not files_with_dates:
            print("No files to organize")
            return
        
        print(f"\nOrganizing {len(files_with_dates)} photos...")
        
        # Separate files with and without dates
        dated_files = [(f, d) for f, d in files_with_dates if d is not None]
        undated_files = [f for f, d in files_with_dates if d is None]
        
        organized_folder = self.config["organized_folder"]
        naming_convention = self.config["naming_convention"]
        
        # Process dated files
        if dated_files:
            print(f"  Organizing {len(dated_files)} dated photos...")
            
            # Sort by date
            if self.config["date_order"] == "newest_first":
                dated_files.sort(key=lambda x: x[1], reverse=True)
            else:
                dated_files.sort(key=lambda x: x[1])
            
            date_counters = defaultdict(int)
            
            for filepath, photo_date in dated_files:
                # Format date according to naming convention
                date_key = self.format_date(photo_date, naming_convention)
                
                # Get next letter/number for this date
                date_counters[date_key] += 1
                counter = date_counters[date_key]
                
                # Create filename
                ext = os.path.splitext(filepath)[1]
                new_name = self.create_filename(date_key, counter, ext)
                new_path = os.path.join(organized_folder, new_name)
                
                # Copy to organized folder
                shutil.copy2(filepath, new_path)
        
        # Process undated files
        if undated_files:
            print(f"  Organizing {len(undated_files)} undated photos...")
            
            for i, filepath in enumerate(undated_files, 1):
                ext = os.path.splitext(filepath)[1]
                new_name = f"photo_{i:04d}{ext}"
                new_path = os.path.join(organized_folder, new_name)
                shutil.copy2(filepath, new_path)
        
        # Show summary
        organized_files = os.listdir(organized_folder)
        print(f"\n✅ Organized {len(organized_files)} photos")
        print(f"Saved to: {organized_folder}")
        
        # Show sample
        print("\nSample files:")
        sample_files = sorted(organized_files)[:10]
        for file in sample_files:
            print(f"  {file}")
    
    def format_date(self, date_obj: datetime, convention: str) -> str:
        """Format date according to naming convention"""
        if convention == "YYMMDD":
            return date_obj.strftime("%y%m%d")
        elif convention == "YYYYMMDD":
            return date_obj.strftime("%Y%m%d")
        elif convention == "MMDDYY":
            return date_obj.strftime("%m%d%y")
        elif convention == "DDMMYY":
            return date_obj.strftime("%d%m%y")
        elif convention == "YYYY-MM-DD":
            return date_obj.strftime("%Y-%m-%d")
        else:
            return date_obj.strftime("%y%m%d")  # Default
    
    def create_filename(self, base_name: str, counter: int, extension: str) -> str:
        """Create filename with sequential indicator"""
        if counter <= 26:
            # Use letters a-z
            suffix = chr(96 + counter)  # 97='a'
        else:
            # Use numbers for large counts
            suffix = str(counter)
        
        return f"{base_name}{suffix}{extension}"
    
    def run(self):
        """Main application loop"""
        while True:
            choice = self.show_main_menu()
            
            if choice == 1:
                self.configure_settings()
            
            elif choice == 2:
                self.show_javascript_instructions()
            
            elif choice == 3:
                urls = self.get_urls_from_user()
                if urls:
                    downloaded = self.download_photos(urls)
                    if downloaded:
                        organize_now = input("\nOrganize photos now? (y/n): ").strip().lower()
                        if organize_now == 'y':
                            self.organize_photos(downloaded)
            
            elif choice == 4:
                folder = input(f"\nEnter folder path to organize [current: {self.config['download_folder']}]: ").strip()
                if not folder:
                    folder = self.config["download_folder"]
                
                if os.path.exists(folder):
                    unique_files = self.remove_duplicates(folder)
                    
                    if unique_files:
                        # Ask about dates
                        date_files = []
                        assign_dates = input("\nAssign dates to these photos? (y/n): ").strip().lower()
                        
                        if assign_dates == 'y':
                            start_date_str = input("Start date (YYYY-MM-DD): ").strip()
                            end_date_str = input("End date (YYYY-MM-DD): ").strip()
                            
                            try:
                                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                                
                                for i, filepath in enumerate(unique_files):
                                    total_days = (end_date - start_date).days
                                    progress = i / (len(unique_files) - 1) if len(unique_files) > 1 else 0
                                    
                                    if self.config["date_order"] == "newest_first":
                                        days_from_end = int(total_days * progress)
                                        photo_date = end_date - timedelta(days=days_from_end)
                                    else:
                                        days_from_start = int(total_days * progress)
                                        photo_date = start_date + timedelta(days=days_from_start)
                                    
                                    date_files.append((filepath, photo_date))
                                
                                self.organize_photos(date_files)
                            except:
                                print("Invalid date format. Organizing without dates.")
                                self.organize_photos([(f, None) for f in unique_files])
                        else:
                            self.organize_photos([(f, None) for f in unique_files])
                else:
                    print(f"Folder not found: {folder}")
            
            elif choice == 5:
                print("\nCurrent Configuration:")
                for key, value in self.config.items():
                    print(f"  {key}: {value}")
                input("\nPress Enter to continue...")
            
            elif choice == 6:
                print("\nThank you for using Photo Downloader & Organizer!")
                break

def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("PHOTO DOWNLOADER & ORGANIZER")
    print("="*70)
    print("\nA general-purpose tool for downloading and organizing photos")
    print("from websites with automatic naming and duplicate removal.")
    print("\nVersion 1.0")
    print("="*70)
    
    # Check for required packages
    try:
        import requests
    except ImportError:
        print("\n⚠️  Required package missing: requests")
        print("Install with: pip install requests")
        print("Exiting...")
        return
    
    # Create organizer instance and run
    organizer = PhotoOrganizer()
    organizer.run()

if __name__ == "__main__":
    main()