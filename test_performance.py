#!/usr/bin/env python3
"""Test performance tracking - scrapes 30 pages to see progress reports"""
import asyncio
import logging
from sale import BinaScraper

# Configure simple logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_performance():
    """Test with 30 pages to see multiple progress reports"""
    logger.info("Testing performance tracking with 30 pages...")

    async with BinaScraper() as scraper:
        cursor = None
        max_pages = 30  # Enough to see 3 progress reports (every 10 pages)

        scraper.start_time = asyncio.get_event_loop().time()

        for page in range(max_pages):
            import time
            page_start = time.time()

            data = await scraper.fetch_page(cursor)

            if not data or 'data' not in data:
                logger.error("Failed to fetch data")
                break

            items_conn = data['data']['itemsConnection']

            # Get total count
            if page == 0:
                total_count = items_conn.get('totalCount', 0)
                logger.info(f"Total items available: {total_count:,}")

            items_added = 0
            items_skipped = 0

            for edge in items_conn.get('edges', []):
                node = edge.get('node')
                if node:
                    item_data = scraper.extract_item_data(node)

                    # Validate and check duplicates
                    if not scraper.validate_item(item_data):
                        items_skipped += 1
                        continue

                    item_id = item_data['id']
                    if item_id in scraper.seen_ids:
                        items_skipped += 1
                        continue

                    scraper.all_items.append(item_data)
                    scraper.seen_ids.add(item_id)
                    items_added += 1

            # Track page time
            page_time = time.time() - page_start
            scraper.page_times.append(page_time)

            # Log progress (will show detailed report every 10 pages)
            scraper.log_progress(page + 1, total_count, items_added, items_skipped)

            cursor = items_conn['pageInfo'].get('endCursor')
            if not cursor:
                break

            await asyncio.sleep(0.5)

        # Force final progress report
        if scraper.all_items:
            logger.info("\nForcing final progress report...")
            scraper.log_progress(page + 1, total_count, items_added, items_skipped, force=True)

        # Show final summary
        total_time = time.time() - scraper.start_time
        logger.info(f"\n✅ Test completed!")
        logger.info(f"Scraped {len(scraper.all_items)} items in {scraper.format_time_detailed(total_time)}")
        logger.info(f"Average: {len(scraper.all_items) / total_time:.1f} items/second")

        return True


if __name__ == "__main__":
    try:
        success = asyncio.run(test_performance())
        logger.info("\n🎉 Performance tracking test PASSED!")
    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
