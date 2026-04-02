# TikTok Username Checker

A high-performance, multi-threaded tool to check availability of 4-letter TikTok usernames with real-time statistics and resume functionality.

## Features

- 🚀 **Multi-threaded** – Configurable thread count (up to 10)
- 🎲 **Random order scanning** – Avoids pattern detection
- 📊 **Periodic statistics** – Shows progress at customizable intervals
- 💾 **Auto-save** – Found usernames automatically saved to file
- 🔄 **Resume support** – Continue interrupted scans from where you left off
- 🎯 **Two scan modes** – Full scan (456,976 combos) or random sample
- 🎨 **Colorful interface** – Clear visual feedback for available/taken usernames

## Installation

### Requirements
- Python 3.1+
- `requests` library
- `colorama` library

### Install dependencies

```bash
pip install requests colorama
```

### Clone the repository

```bash
git clone https://github.com/0kxs/TikTok-4L-Checker.git
cd TikTok-4L-Checker
```

## Usage

Run the script:

```bash
python tiktokuser.py
```

### Menu Options

| Option | Description |
|--------|-------------|
| `1` | **Full scan** – Checks all 456,976 possible 4-letter combinations in random order |
| `2` | **Sample scan** – Checks a random subset of usernames (specify count) |
| `3` | **Resume scan** – Continues a previous interrupted full scan |

### Configuration Parameters

When starting a scan, you can configure:

| Parameter | Description | Default |
|-----------|-------------|---------|
| **Delay** | Time between requests (seconds) | 0.5 |
| **Threads** | Number of concurrent threads (max 10) | 5 |

### Statistics Display

- **Periodic stats** are shown every:
  - 100 checks for scans with < 1,000 usernames
  - 200 checks for scans with ≥ 1,000 usernames
- **Final summary** shows complete results after scan completion

## Output

### File Output
Found usernames are automatically saved to `available_usernames.txt` (one per line).

### Console Output Example

```
[✗] @abcd Taken
[✗] @efgh Taken
[+] @xqjz AVAILABLE!

╔══════════════════════════════════════════════════════════════════╗
║  🎉 NEW USERNAME AVAILABLE! 🎉                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  @xqjz                                                           ║
║   https://tiktok.com/@xqjz                                       ║
╚══════════════════════════════════════════════════════════════════╝
```

### Final Summary Example

```
============================================================
                    FINAL SUMMARY
============================================================

[+] Usernames found: 3
[-] Usernames taken: 9997
[*] Total checked: 10000
[*] Total time: 52.34 seconds
[*] Output file: available_usernames.txt

────────────────────────────────────────────────────────────
AVAILABLE USERNAMES:
────────────────────────────────────────────────────────────
  @xqjz             @zrwk             @qwpv             @vzqx
────────────────────────────────────────────────────────────
```

## How It Works

1. **Username Generation** – Generates all possible 4-letter combinations (a-z) = 456,976 possibilities
2. **Random Shuffle** – Randomizes order to avoid detection patterns
3. **Multi-threaded Checking** – Sends HEAD requests to `https://www.tiktok.com/@username`
4. **Status Detection**:
   - `404` → Username available
   - `200` → Username taken
   - `429` → Rate limited (automatic handling)
5. **Result Saving** – Available usernames saved immediately to file

## Technical Details

- **API Endpoint**: `https://www.tiktok.com/@username`
- **Request Method**: GET with `allow_redirects=False`
- **Rate Limiting**: Built-in delay between requests (configurable)
- **Thread Safety**: Thread-safe counters using `threading.Lock()`
- **Resume Feature**: Reads existing output file to skip already-found usernames

## Important Notes

- ⚠️ **4-letter usernames are extremely rare** – Only about 100-500 available out of 456,976
- 🔒 **Rate limiting** – TikTok may temporarily block your IP after many requests without proxies
- 🌐 **Proxy support** – Not built-in; use external proxy tools to avoid **IP FLAG**

## Disclaimer

This tool is for **educational purposes only**. Use responsibly and respect TikTok's terms of service. The author is not responsible for any misuse or violation of platform policies.

## License

MIT License

## Author

Created by 0Kxs

## Star History

If you find this tool useful, consider giving it a star ⭐ on GitHub!
