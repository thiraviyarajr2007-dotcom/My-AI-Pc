"""
File Search AI Module - Intelligent File Search Across User Directories
Supports: search by name, extension, content, size, and recent modifications.
"""

import os
import sys
import fnmatch
import time
from datetime import datetime, timedelta


# ─── Default search roots ──────────────────────────────────────
DEFAULT_SEARCH_PATHS = [
    os.path.expanduser("~\\Desktop"),
    os.path.expanduser("~\\Documents"),
    os.path.expanduser("~\\Downloads"),
    os.path.expanduser("~\\Pictures"),
    os.path.expanduser("~\\Videos"),
    os.path.expanduser("~\\Music"),
]

# Skip these directories for performance
SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv",
    "AppData", ".cache", ".npm", ".nuget", "Temp",
}

# Max file size for content search (5 MB)
MAX_CONTENT_SEARCH_SIZE = 5 * 1024 * 1024


def search_by_name(query, search_paths=None, case_sensitive=False, max_results=50):
    """
    Search for files/folders matching a name pattern.
    Supports wildcards: *.py, report*, *.txt, etc.
    """
    if search_paths is None:
        search_paths = DEFAULT_SEARCH_PATHS

    if "*" not in query and "?" not in query:
        query = f"*{query}*"

    results = []
    for root_path in search_paths:
        if not os.path.exists(root_path):
            continue
        for dirpath, dirnames, filenames in os.walk(root_path):
            # Skip excluded directories
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

            for filename in filenames:
                match = fnmatch.fnmatch(
                    filename if case_sensitive else filename.lower(),
                    query if case_sensitive else query.lower(),
                )
                if match:
                    full_path = os.path.join(dirpath, filename)
                    try:
                        stat = os.stat(full_path)
                        results.append({
                            "path": full_path,
                            "name": filename,
                            "size": stat.st_size,
                            "modified": datetime.fromtimestamp(stat.st_mtime),
                        })
                    except OSError:
                        continue

                    if len(results) >= max_results:
                        return results
    return results


def search_by_extension(extension, search_paths=None, max_results=50):
    """Search for all files with a given extension (e.g., '.py', '.pdf')."""
    if not extension.startswith("."):
        extension = f".{extension}"
    return search_by_name(f"*{extension}", search_paths, max_results=max_results)


def search_by_content(text, search_paths=None, file_pattern="*.*", max_results=20):
    """
    Search for files containing specific text content.
    Only searches text-readable files under MAX_CONTENT_SEARCH_SIZE.
    """
    if search_paths is None:
        search_paths = DEFAULT_SEARCH_PATHS

    results = []
    text_lower = text.lower()

    for root_path in search_paths:
        if not os.path.exists(root_path):
            continue
        for dirpath, dirnames, filenames in os.walk(root_path):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

            for filename in filenames:
                if not fnmatch.fnmatch(filename.lower(), file_pattern.lower()):
                    continue

                full_path = os.path.join(dirpath, filename)
                try:
                    size = os.path.getsize(full_path)
                    if size > MAX_CONTENT_SEARCH_SIZE or size == 0:
                        continue

                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    if text_lower in content.lower():
                        # Find the line containing the match
                        lines = content.split("\n")
                        match_lines = []
                        for i, line in enumerate(lines, 1):
                            if text_lower in line.lower():
                                match_lines.append((i, line.strip()[:100]))
                                if len(match_lines) >= 3:
                                    break

                        results.append({
                            "path": full_path,
                            "name": filename,
                            "size": size,
                            "matches": match_lines,
                        })

                except (OSError, PermissionError, UnicodeDecodeError):
                    continue

                if len(results) >= max_results:
                    return results
    return results


def search_recent_files(hours=24, search_paths=None, max_results=50):
    """Find files modified within the last N hours."""
    if search_paths is None:
        search_paths = DEFAULT_SEARCH_PATHS

    cutoff = datetime.now() - timedelta(hours=hours)
    results = []

    for root_path in search_paths:
        if not os.path.exists(root_path):
            continue
        for dirpath, dirnames, filenames in os.walk(root_path):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                try:
                    stat = os.stat(full_path)
                    mod_time = datetime.fromtimestamp(stat.st_mtime)
                    if mod_time >= cutoff:
                        results.append({
                            "path": full_path,
                            "name": filename,
                            "size": stat.st_size,
                            "modified": mod_time,
                        })
                except OSError:
                    continue

                if len(results) >= max_results:
                    results.sort(key=lambda x: x["modified"], reverse=True)
                    return results

    results.sort(key=lambda x: x["modified"], reverse=True)
    return results


def search_large_files(min_size_mb=100, search_paths=None, max_results=20):
    """Find files larger than a specified size in MB."""
    if search_paths is None:
        search_paths = DEFAULT_SEARCH_PATHS

    min_bytes = min_size_mb * 1024 * 1024
    results = []

    for root_path in search_paths:
        if not os.path.exists(root_path):
            continue
        for dirpath, dirnames, filenames in os.walk(root_path):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                try:
                    size = os.path.getsize(full_path)
                    if size >= min_bytes:
                        results.append({
                            "path": full_path,
                            "name": filename,
                            "size": size,
                            "modified": datetime.fromtimestamp(os.path.getmtime(full_path)),
                        })
                except OSError:
                    continue

                if len(results) >= max_results:
                    results.sort(key=lambda x: x["size"], reverse=True)
                    return results

    results.sort(key=lambda x: x["size"], reverse=True)
    return results


def _format_size(bytes_size):
    """Format bytes into human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"


def _print_results(results, show_content=False):
    """Pretty-print search results."""
    if not results:
        print("  No results found.")
        return

    print(f"\n  Found {len(results)} result(s):\n")
    for i, r in enumerate(results, 1):
        print(f"  {i:3}. 📄 {r['name']}")
        print(f"       Path: {r['path']}")
        print(f"       Size: {_format_size(r['size'])}", end="")
        if "modified" in r:
            print(f"  |  Modified: {r['modified'].strftime('%Y-%m-%d %H:%M')}")
        else:
            print()
        if show_content and "matches" in r:
            for line_num, line_text in r["matches"]:
                print(f"       Line {line_num}: {line_text}")
        print()


def run_file_search():
    """Interactive file search menu."""
    print("=" * 55)
    print("  🔍 AI File Search - Intelligent File Finder")
    print("=" * 55)

    while True:
        print("\n  Search Options:")
        print("    1. Search by filename")
        print("    2. Search by extension")
        print("    3. Search by file content")
        print("    4. Find recently modified files")
        print("    5. Find large files")
        print("    6. Exit")

        try:
            choice = input("\n  Choose option (1-6): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 File search stopped.")
            return

        if choice == "1":
            query = input("  Enter filename (supports wildcards like *.py): ").strip()
            if query:
                print(f"\n  🔍 Searching for: {query}...")
                start = time.time()
                results = search_by_name(query)
                elapsed = time.time() - start
                _print_results(results)
                print(f"  ⏱️ Search completed in {elapsed:.2f}s")

        elif choice == "2":
            ext = input("  Enter extension (e.g. py, pdf, docx): ").strip()
            if ext:
                print(f"\n  🔍 Searching for .{ext} files...")
                start = time.time()
                results = search_by_extension(ext)
                elapsed = time.time() - start
                _print_results(results)
                print(f"  ⏱️ Search completed in {elapsed:.2f}s")

        elif choice == "3":
            text = input("  Enter text to search inside files: ").strip()
            pattern = input("  File pattern (default *.txt, or press Enter for all): ").strip()
            if not pattern:
                pattern = "*.*"
            if text:
                print(f"\n  🔍 Searching file contents for: \"{text}\"...")
                start = time.time()
                results = search_by_content(text, file_pattern=pattern)
                elapsed = time.time() - start
                _print_results(results, show_content=True)
                print(f"  ⏱️ Search completed in {elapsed:.2f}s")

        elif choice == "4":
            hours = input("  Modified within last N hours (default 24): ").strip()
            hours = int(hours) if hours.isdigit() else 24
            print(f"\n  🔍 Finding files modified in the last {hours} hours...")
            start = time.time()
            results = search_recent_files(hours=hours)
            elapsed = time.time() - start
            _print_results(results)
            print(f"  ⏱️ Search completed in {elapsed:.2f}s")

        elif choice == "5":
            size = input("  Minimum size in MB (default 100): ").strip()
            size = int(size) if size.isdigit() else 100
            print(f"\n  🔍 Finding files larger than {size} MB...")
            start = time.time()
            results = search_large_files(min_size_mb=size)
            elapsed = time.time() - start
            _print_results(results)
            print(f"  ⏱️ Search completed in {elapsed:.2f}s")

        elif choice == "6":
            print("\n👋 File search stopped.")
            return
        else:
            print("  [!] Invalid option. Choose 1-6.")


if __name__ == "__main__":
    run_file_search()
