# Crash Recovery & Data Integrity Features

## Overview
The scraper now includes comprehensive crash recovery and data integrity features to ensure no data is lost during scraping, even if the process is interrupted.

## Features Implemented

### 1. Checkpoint System
- **Automatic checkpoints** saved every 50 pages
- Stores current progress (cursor, page number, item count)
- Located at: `data/checkpoint.json`

### 2. Incremental Backups
- **Automatic backups** saved every 100 pages
- Full data snapshots with timestamps
- Format: `data/backup_page{N}_YYYYMMDD_HHMMSS.json`
- Keeps last 3 backups automatically

### 3. Resume Capability
- Automatically resumes from last checkpoint on restart
- Loads previously scraped data from backup
- Continues from exact cursor position

### 4. Data Validation
- Validates all items have required fields (`id`, `scraped_at`)
- Skips invalid items with warning logs
- Tracks validation failures

### 5. Deduplication
- Tracks all scraped IDs in memory
- Prevents duplicate items from being saved
- Reports duplicate count at completion

### 6. Crash Handling
- Graceful handling of:
  - Keyboard interrupts (Ctrl+C)
  - Network errors
  - API failures
  - Unexpected exceptions
- Always saves checkpoint before exiting

## Usage

### Normal Operation
```bash
python sale.py
```

### Resume After Crash
```bash
# Just run again - it will automatically resume from checkpoint
python sale.py
```

### Fresh Start (Ignore Checkpoint)
```bash
# Delete checkpoint file first
rm data/checkpoint.json
rm data/backup_*.json
python sale.py
```

## Data Integrity Report

After scraping completes, you'll see a comprehensive data integrity report:

```
DATA INTEGRITY REPORT
================================================================================
Total items scraped: 73201
Unique items: 73201
Duplicates removed: 0

Data Completeness:
  id: 100.0%
  price: 98.5%
  location: 99.8%
  area: 97.2%

Data Quality:
  Items with photos: 71543
  Missing price: 1103
  Missing location: 146
  Missing area: 2050
```

## Files Created

### Checkpoint Files
- `data/checkpoint.json` - Current progress state

### Backup Files
- `data/backup_page100_*.json` - Backup at page 100
- `data/backup_page200_*.json` - Backup at page 200
- `data/backup_page300_*.json` - Backup at page 300
- (Only last 3 backups kept)

### Final Output Files
- `data/bina_sale_YYYYMMDD_HHMMSS.json` - Complete dataset
- `data/bina_sale_YYYYMMDD_HHMMSS.csv` - CSV format
- `data/bina_sale_YYYYMMDD_HHMMSS.xlsx` - Excel format

## Recovery Scenarios

### Scenario 1: Network Failure
- Scraper detects failure
- Saves checkpoint automatically
- On restart: Resumes from last successful page

### Scenario 2: User Interruption (Ctrl+C)
- Catches interrupt signal
- Saves current progress
- On restart: Continues where left off

### Scenario 3: System Crash
- Last checkpoint (max 50 pages old) is available
- Last backup (max 100 pages old) contains data
- On restart: Loads backup + continues from checkpoint

### Scenario 4: API Rate Limiting
- Automatic retry with exponential backoff
- Saves checkpoint if persistent failure
- Can resume after waiting period

## Configuration

Adjust these settings in `sale.py`:

```python
# Save checkpoint every N pages
CHECKPOINT_INTERVAL = 50

# Save full backup every N pages
INCREMENTAL_SAVE_INTERVAL = 100

# Number of backup files to keep
cleanup_backups(keep_last=3)
```

## Monitoring Progress

Check the log file for detailed progress:
```bash
tail -f scraper.log
```

Look for key indicators:
- `Checkpoint saved: page N` - Progress saved
- `Incremental backup saved` - Data snapshot created
- `Page N: +X items, Y skipped` - Items per page with validation status
- `Unique items: X, Duplicates removed: Y` - Deduplication stats

## Data Analytics Safety

For strategic analytics, this implementation ensures:

1. **No Data Loss**: Multiple backup layers prevent data loss
2. **Data Quality**: Validation ensures clean data
3. **No Duplicates**: Deduplication guarantees unique records
4. **Completeness Tracking**: Reports show data coverage
5. **Auditability**: Full logging of all operations
6. **Reproducibility**: Can verify/resume at any point

## Best Practices

1. **Monitor disk space** - Backups accumulate (auto-cleaned after 3)
2. **Check integrity report** - Verify data quality after completion
3. **Keep checkpoint until done** - Don't delete while scraping
4. **Save final output** - Move to permanent storage after completion
5. **Review logs** - Check for validation warnings or errors

## Troubleshooting

**Q: Scraper keeps restarting from beginning?**
A: Check if checkpoint.json exists. If corrupted, delete it.

**Q: High memory usage?**
A: Large datasets are held in memory. For 73K items, expect ~500MB RAM.

**Q: Duplicate detection not working?**
A: Ensure you're not deleting backup files between runs.

**Q: Backups taking too much space?**
A: Adjust `INCREMENTAL_SAVE_INTERVAL` to save less frequently.
