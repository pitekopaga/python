// Photo URL Extractor for Web Browsers
// =====================================
// Use this script to extract image URLs from any website
// Instructions:
// 1. Navigate to the website with photos in Chrome/Firefox
// 2. Log in if necessary and load ALL photos (scroll, click "Load more")
// 3. Press F12 to open Developer Tools
// 4. Go to the Console tab
// 5. Paste this entire script and press Enter
// 6. Follow the on-screen instructions

(function() {
    'use strict';
    
    // Configuration
    const CONFIG = {
        minWidth: 100,        // Minimum image width to consider
        minHeight: 100,       // Minimum image height to consider
        fileTypes: ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
        excludeKeywords: ['icon', 'logo', 'avatar', 'spinner', 'loading']
    };
    
    // Utility functions
    function isLikelyPhoto(img) {
        // Check if element is likely a photo (not icon/logo)
        const src = (img.src || '').toLowerCase();
        const alt = (img.alt || '').toLowerCase();
        const className = (img.className || '').toLowerCase();
        
        // Exclude based on keywords
        for (const keyword of CONFIG.excludeKeywords) {
            if (src.includes(keyword) || alt.includes(keyword) || className.includes(keyword)) {
                return false;
            }
        }
        
        // Check file type
        let hasValidExtension = false;
        for (const ext of CONFIG.fileTypes) {
            if (src.includes(ext)) {
                hasValidExtension = true;
                break;
            }
        }
        
        if (!hasValidExtension) {
            return false;
        }
        
        // Check dimensions
        if (img.naturalWidth < CONFIG.minWidth || img.naturalHeight < CONFIG.minHeight) {
            return false;
        }
        
        return true;
    }
    
    function getBestQualityUrl(url) {
        // Try to get the highest quality version of an image
        const lowerUrl = url.toLowerCase();
        
        // Common patterns for lower quality images
        const qualityPatterns = [
            { low: 'thumb', high: 'large' },
            { low: 'thumbnail', high: 'original' },
            { low: '_sm', high: '_lg' },
            { low: '_xs', high: '_xl' },
            { low: '-small', high: '-large' },
            { low: 'w100', high: 'w1000' },
            { low: 'h100', high: 'h1000' }
        ];
        
        let bestUrl = url;
        for (const pattern of qualityPatterns) {
            if (lowerUrl.includes(pattern.low)) {
                bestUrl = url.replace(new RegExp(pattern.low, 'i'), pattern.high);
                break;
            }
        }
        
        return bestUrl;
    }
    
    function scrollToLoadAll(callback) {
        console.log('📜 Scrolling to load all content...');
        
        let scrollAttempts = 0;
        let lastHeight = document.body.scrollHeight;
        const maxAttempts = 20;
        
        function attemptScroll() {
            // Scroll to bottom
            window.scrollTo(0, document.body.scrollHeight);
            
            // Wait for content to load
            setTimeout(() => {
                const newHeight = document.body.scrollHeight;
                
                if (newHeight === lastHeight) {
                    scrollAttempts++;
                    if (scrollAttempts >= 3) {
                        console.log('✅ Finished scrolling');
                        if (callback) callback();
                    } else {
                        // Try a few more times in case of lazy loading
                        setTimeout(attemptScroll, 2000);
                    }
                } else {
                    scrollAttempts = 0;
                    lastHeight = newHeight;
                    attemptScroll();
                }
                
                if (scrollAttempts > maxAttempts) {
                    console.log('⚠️  Max scroll attempts reached');
                    if (callback) callback();
                }
            }, 2000);
        }
        
        attemptScroll();
    }
    
    function extractAllUrls() {
        console.log('🔍 Extracting image URLs...');
        
        // Find all image elements
        const images = Array.from(document.querySelectorAll('img'));
        console.log(`Found ${images.length} total image elements`);
        
        // Filter for likely photos
        const photoUrls = [];
        images.forEach(img => {
            if (isLikelyPhoto(img)) {
                const src = img.src || img.dataset.src || img.currentSrc;
                if (src && !src.startsWith('data:')) {
                    const bestUrl = getBestQualityUrl(src);
                    photoUrls.push(bestUrl);
                }
            }
        });
        
        // Remove duplicates
        const uniqueUrls = [...new Set(photoUrls)];
        
        console.log(`✅ Found ${uniqueUrls.length} unique photos`);
        
        // Create downloadable file
        const blob = new Blob([uniqueUrls.join('\n')], {type: 'text/plain'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'extracted_photo_urls.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        // Display results
        console.log('\n📋 RESULTS:');
        console.log(`Total URLs extracted: ${uniqueUrls.length}`);
        console.log('File downloaded: extracted_photo_urls.txt');
        
        if (uniqueUrls.length > 0) {
            console.log('\nFirst 5 URLs:');
            uniqueUrls.slice(0, 5).forEach((url, i) => {
                console.log(`  ${i + 1}. ${url}`);
            });
        }
        
        console.log('\n💡 Next steps:');
        console.log('1. Save the downloaded .txt file');
        console.log('2. Use it with the Python photo organizer');
        console.log('3. Select "Download Photos from URLs" option');
        
        return uniqueUrls;
    }
    
    // Main execution
    console.log('🖼️  PHOTO URL EXTRACTOR');
    console.log('='.repeat(50));
    console.log('\nAvailable commands:');
    console.log('  scrollToLoadAll()   - Scroll to load all content');
    console.log('  extractAllUrls()    - Extract URLs immediately');
    console.log('\nRecommended workflow:');
    console.log('1. Make sure all photos are loaded on the page');
    console.log('2. Run scrollToLoadAll() if there are "Load more" buttons');
    console.log('3. Run extractAllUrls() to extract and download URLs');
    console.log('='.repeat(50));
    
    // Make functions globally available
    window.scrollToLoadAll = scrollToLoadAll;
    window.extractAllUrls = extractAllUrls;
    
    return 'Ready! Use scrollToLoadAll() or extractAllUrls()';
})();