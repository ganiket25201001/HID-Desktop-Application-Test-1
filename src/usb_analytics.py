"""
USB Analytics Module for Device Monitor Pro
Analyzes file contents of storage devices to provide a categorized summary (Images, Documents, etc.).
"""
import os
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, Any, List
import logging

# Configure logging
logger = logging.getLogger(__name__)

class USBAnalytics:
    """Analyzes storage content and categorizes files by type."""

    def __init__(self):
        """Initialize with file type definitions."""
        self.categories = {
            "Images": {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.ico', '.svg', '.raw', '.heic', '.psd'},
            "Documents": {'.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.rtf', '.csv', '.md', '.epub', '.log', '.tex'},
            "Audio": {'.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma', '.m4a', '.midi', '.aiff'},
            "Video": {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp', '.mpeg', '.mpg'},
            "Archives": {'.zip', '.rar', '.7z', '.tar', '.gz', '.iso', '.dmg', '.pkg', '.deb', '.rpm', '.cab'},
            "Executables": {'.exe', '.msi', '.bat', '.sh', '.dll', '.bin', '.cmd', '.com', '.apk', '.jar'},
            "Code": {'.py', '.java', '.c', '.cpp', '.h', '.cs', '.js', '.ts', '.html', '.css', '.php', '.rb', '.go', '.rs', '.swift', '.json', '.xml', '.yaml', '.yml', '.sql', '.vbs'},
            "Fonts": {'.ttf', '.otf', '.woff', '.woff2', '.eot'},
            "Disk Images": {'.img', '.vhd', '.vhdx', '.vmdk'},
            "Database": {'.db', '.sqlite', '.sqlite3', '.mdb', '.accdb'}
        }

    def analyze_path(self, path: str) -> Dict[str, Any]:
        """
        Walks through the given path and generates a statistical analysis of file types.
        
        Args:
            path: The root directory path to analyze (e.g., 'E:\\')
            
        Returns:
            Dictionary containing summary stats and categorized breakdown.
        """
        root_path = Path(path)
        if not root_path.exists():
            logger.error(f"Path not found: {path}")
            return {"error": f"Path '{path}' does not access."}

        stats = {
            "total_files": 0,
            "total_size_bytes": 0,
            "categories": defaultdict(lambda: {"count": 0, "size_bytes": 0, "extensions": Counter()})
        }

        logger.info(f"Starting analysis of {path}...")
        
        try:
            for root, _, files in os.walk(root_path):
                for file in files:
                    try:
                        file_path = Path(root) / file
                        # Skip system files if needed, or handle permission errors gracefully
                        stat = file_path.stat()
                        size = stat.st_size
                        ext = file_path.suffix.lower()
                        
                        stats["total_files"] += 1
                        stats["total_size_bytes"] += size

                        # Determine Category
                        category = "Others"
                        for cat_name, extensions in self.categories.items():
                            if ext in extensions:
                                category = cat_name
                                break
                        
                        # Update Category Stats
                        cat_stats = stats["categories"][category]
                        cat_stats["count"] += 1
                        cat_stats["size_bytes"] += size
                        cat_stats["extensions"][ext] += 1
                        
                    except (PermissionError, OSError) as e:
                        # Skip files we can't read
                        continue
                        
        except Exception as e:
            logger.error(f"Error during scan: {e}")
            return {"error": str(e)}

        return self._format_report(stats)

    def _format_report(self, stats: Dict) -> Dict:
        """Formats the raw statistics into a clean, human-readable structure."""
        
        breakdown = {}
        
        # Sort categories by count descending
        sorted_categories = sorted(
            stats["categories"].items(), 
            key=lambda x: x[1]['count'], 
            reverse=True
        )

        for cat, data in sorted_categories:
            # Sort extensions within category by count descending
            sorted_exts = dict(sorted(
                data["extensions"].items(), 
                key=lambda x: x[1], 
                reverse=True
            ))
            
            breakdown[cat] = {
                "total_count": data["count"],
                "total_size_mb": round(data["size_bytes"] / (1024 * 1024), 2),
                "file_types": sorted_exts
            }

        return {
            "summary": {
                "total_files": stats["total_files"],
                "total_size_gb": round(stats["total_size_bytes"] / (1024 * 1024 * 1024), 2),
            },
            "details": breakdown
        }

def print_analysis(results: Dict):
    """Helper to pretty print the results to console."""
    if "error" in results:
        print(f"❌ Error: {results['error']}")
        return

    summary = results["summary"]
    print("\n" + "="*50)
    print(f" 📊 DRIVE ANALYSIS REPORT")
    print("="*50)
    print(f" Total Files: {summary['total_files']}")
    print(f" Total Size:  {summary['total_size_gb']} GB")
    print("-" * 50)
    
    for cat, data in results["details"].items():
        print(f"\n 📁 {cat.upper()} ({data['total_count']} files, {data['total_size_mb']} MB)")
        
        # Print top 5 extensions for brevity in console
        exts = list(data["file_types"].items())
        for ext, count in exts:
            clean_ext = ext.lstrip('.') if ext else "no-ext"
            print(f"   • {clean_ext.ljust(8)} : {count}")

if __name__ == "__main__":
    # Simple CLI test
    import sys
    if len(sys.argv) > 1:
        path_arg = sys.argv[1]
        print(f"Scanning: {path_arg}")
        analytics = USBAnalytics()
        res = analytics.analyze_path(path_arg)
        print_analysis(res)
    else:
        print("Usage: python usb_analytics.py <drive_path>")
