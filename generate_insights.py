#!/usr/bin/env python3
"""
Generate valuable insights and charts from Bina.az property data
"""
import json
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from collections import Counter, defaultdict
import numpy as np
from pathlib import Path

# Set style
matplotlib.use('Agg')
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

# Create charts directory
Path('charts').mkdir(exist_ok=True)

# Load data
print("Loading data...")
with open('data/bina_sale_20251117_213933.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Loaded {len(data):,} properties\n")

# Filter Baki properties for detailed analysis
baki_data = [item for item in data if item.get('city_name') == 'Bakı']
print(f"Baki properties: {len(baki_data):,}\n")

# ============================================================================
# INSIGHT 1: Price Distribution by City (Top 10)
# ============================================================================
print("1. Generating: Average prices by city...")
city_prices = defaultdict(list)
for item in data:
    if item.get('price_value'):
        city_prices[item['city_name']].append(item['price_value'])

city_avg = {city: np.mean(prices) for city, prices in city_prices.items()}
top_cities = sorted(city_avg.items(), key=lambda x: x[1], reverse=True)[:10]

plt.figure(figsize=(12, 7))
cities, prices = zip(*top_cities)
colors = sns.color_palette("viridis", len(cities))
bars = plt.bar(cities, prices, color=colors)
plt.xlabel('City', fontsize=13, fontweight='bold')
plt.ylabel('Average Price (AZN)', fontsize=13, fontweight='bold')
plt.title('Top 10 Most Expensive Cities in Azerbaijan', fontsize=16, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/01_price_by_city.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# INSIGHT 2: Top 15 Locations in Baki
# ============================================================================
print("2. Generating: Most popular locations in Baki...")
baki_locations = Counter(item['location_name'] for item in baki_data if item.get('location_name'))
top_locations = baki_locations.most_common(15)

plt.figure(figsize=(12, 9))
locations, counts = zip(*top_locations)
colors = sns.color_palette("rocket", len(locations))
bars = plt.barh(range(len(locations)), counts, color=colors)
plt.yticks(range(len(locations)), locations)
plt.xlabel('Number of Properties', fontsize=13, fontweight='bold')
plt.ylabel('District', fontsize=13, fontweight='bold')
plt.title('Top 15 Most Active Real Estate Districts in Baki', fontsize=16, fontweight='bold', pad=20)
plt.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, count) in enumerate(zip(bars, counts)):
    plt.text(count + 50, i, f'{count:,}',
             va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/02_top_locations_baki.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# INSIGHT 3: Price vs Area Scatter (Baki only, filtered outliers)
# ============================================================================
print("3. Generating: Price vs Area relationship...")
areas = []
prices_scatter = []
for item in baki_data:
    if item.get('area_value') and item.get('price_value'):
        area = item['area_value']
        price = item['price_value']
        # Filter reasonable ranges
        if 20 <= area <= 500 and 10000 <= price <= 2000000:
            areas.append(area)
            prices_scatter.append(price)

plt.figure(figsize=(12, 8))
plt.scatter(areas, prices_scatter, alpha=0.3, s=20, c='#2E86AB')
plt.xlabel('Area (m²)', fontsize=13, fontweight='bold')
plt.ylabel('Price (AZN)', fontsize=13, fontweight='bold')
plt.title('Property Price vs Area in Baki', fontsize=16, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3)

# Add trend line
z = np.polyfit(areas, prices_scatter, 1)
p = np.poly1d(z)
plt.plot(sorted(areas), p(sorted(areas)), "r--", linewidth=2, label=f'Trend: {int(z[0]):,} AZN per m²')
plt.legend(fontsize=12)

plt.tight_layout()
plt.savefig('charts/03_price_vs_area.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# INSIGHT 4: Room Distribution (Pie Chart)
# ============================================================================
print("4. Generating: Room distribution...")
rooms = Counter(item['rooms'] for item in baki_data if item.get('rooms') and item['rooms'] <= 6)
room_labels = [f'{r} Room{"s" if r > 1 else ""}' for r in sorted(rooms.keys())]
room_values = [rooms[r] for r in sorted(rooms.keys())]

plt.figure(figsize=(10, 10))
colors = sns.color_palette("Set2", len(room_labels))
wedges, texts, autotexts = plt.pie(room_values, labels=room_labels, autopct='%1.1f%%',
                                      colors=colors, startangle=90, textprops={'fontsize': 12})

# Bold percentage text
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(13)

plt.title('Distribution of Properties by Number of Rooms\n(Baki)',
          fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('charts/04_room_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# INSIGHT 5: Average Price by Number of Rooms
# ============================================================================
print("5. Generating: Price by room count...")
room_prices = defaultdict(list)
for item in baki_data:
    if item.get('rooms') and item.get('price_value') and item['rooms'] <= 6:
        room_prices[item['rooms']].append(item['price_value'])

room_avg_prices = {r: np.mean(prices) for r, prices in room_prices.items()}
sorted_rooms = sorted(room_avg_prices.items())

plt.figure(figsize=(12, 7))
rooms_x, prices_y = zip(*sorted_rooms)
plt.plot(rooms_x, prices_y, marker='o', linewidth=3, markersize=12, color='#E63946')
plt.xlabel('Number of Rooms', fontsize=13, fontweight='bold')
plt.ylabel('Average Price (AZN)', fontsize=13, fontweight='bold')
plt.title('How Property Prices Increase with Number of Rooms', fontsize=16, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3)

# Add value labels
for x, y in zip(rooms_x, prices_y):
    plt.text(x, y + 10000, f'{int(y):,}', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/05_price_by_rooms.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# INSIGHT 6: Mortgage & Repair Status
# ============================================================================
print("6. Generating: Property features distribution...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Mortgage
mortgage_yes = sum(1 for item in baki_data if item.get('has_mortgage'))
mortgage_no = len(baki_data) - mortgage_yes
colors1 = ['#06D6A0', '#EF476F']
wedges1, texts1, autotexts1 = ax1.pie([mortgage_yes, mortgage_no],
                                        labels=['With Mortgage', 'No Mortgage'],
                                        autopct='%1.1f%%', colors=colors1,
                                        startangle=90, textprops={'fontsize': 11})
for autotext in autotexts1:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(12)
ax1.set_title('Mortgage Availability', fontsize=14, fontweight='bold', pad=15)

# Repair
repair_yes = sum(1 for item in baki_data if item.get('has_repair'))
repair_no = len(baki_data) - repair_yes
colors2 = ['#118AB2', '#FFD166']
wedges2, texts2, autotexts2 = ax2.pie([repair_yes, repair_no],
                                        labels=['Renovated', 'Needs Repair'],
                                        autopct='%1.1f%%', colors=colors2,
                                        startangle=90, textprops={'fontsize': 11})
for autotext in autotexts2:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(12)
ax2.set_title('Renovation Status', fontsize=14, fontweight='bold', pad=15)

plt.suptitle('Property Features in Baki Market', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('charts/06_property_features.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# INSIGHT 7: Price Categories Distribution
# ============================================================================
print("7. Generating: Price range distribution...")
def categorize_price(price):
    if price < 50000:
        return 'Under 50K'
    elif price < 100000:
        return '50K-100K'
    elif price < 200000:
        return '100K-200K'
    elif price < 300000:
        return '200K-300K'
    elif price < 500000:
        return '300K-500K'
    else:
        return 'Above 500K'

price_categories = Counter(categorize_price(item['price_value'])
                          for item in baki_data if item.get('price_value'))

category_order = ['Under 50K', '50K-100K', '100K-200K', '200K-300K', '300K-500K', 'Above 500K']
counts = [price_categories[cat] for cat in category_order]

plt.figure(figsize=(12, 7))
colors = sns.color_palette("coolwarm", len(category_order))
bars = plt.bar(category_order, counts, color=colors, edgecolor='black', linewidth=1.5)
plt.xlabel('Price Range (AZN)', fontsize=13, fontweight='bold')
plt.ylabel('Number of Properties', fontsize=13, fontweight='bold')
plt.title('Property Price Range Distribution in Baki', fontsize=16, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/07_price_ranges.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# INSIGHT 8: Top Real Estate Agencies
# ============================================================================
print("8. Generating: Top agencies...")
agencies = Counter(item['company_name'] for item in baki_data
                  if item.get('is_business') and item.get('company_name'))
top_agencies = agencies.most_common(15)

plt.figure(figsize=(12, 9))
companies, counts_agencies = zip(*top_agencies)
colors = sns.color_palette("mako", len(companies))
bars = plt.barh(range(len(companies)), counts_agencies, color=colors)
plt.yticks(range(len(companies)), companies)
plt.xlabel('Number of Active Listings', fontsize=13, fontweight='bold')
plt.ylabel('Agency', fontsize=13, fontweight='bold')
plt.title('Top 15 Most Active Real Estate Agencies in Baki', fontsize=16, fontweight='bold', pad=20)
plt.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, count) in enumerate(zip(bars, counts_agencies)):
    plt.text(count + 10, i, f'{count:,}',
             va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/08_top_agencies.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# INSIGHT 9: VIP vs Regular Listings Price Comparison
# ============================================================================
print("9. Generating: VIP vs Regular comparison...")
vip_prices = [item['price_value'] for item in baki_data
              if item.get('vipped') and item.get('price_value')]
regular_prices = [item['price_value'] for item in baki_data
                  if not item.get('vipped') and item.get('price_value')]

# Calculate statistics
vip_avg = np.mean(vip_prices)
regular_avg = np.mean(regular_prices)
vip_median = np.median(vip_prices)
regular_median = np.median(regular_prices)
vip_count = len(vip_prices)
regular_count = len(regular_prices)

# Create comparison chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# Left: Average and Median Prices
categories = ['Regular\nListings', 'VIP\nListings']
averages = [regular_avg, vip_avg]
medians = [regular_median, vip_median]

x = np.arange(len(categories))
width = 0.35

bars1 = ax1.bar(x - width/2, averages, width, label='Average Price',
                color='#A8DADC', edgecolor='black', linewidth=1.5)
bars2 = ax1.bar(x + width/2, medians, width, label='Median Price',
                color='#E63946', edgecolor='black', linewidth=1.5)

ax1.set_ylabel('Price (AZN)', fontsize=13, fontweight='bold')
ax1.set_title('Price Comparison', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks(x)
ax1.set_xticklabels(categories, fontsize=12, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(axis='y', alpha=0.3)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

# Right: Number of Listings
counts = [regular_count, vip_count]
colors_right = ['#A8DADC', '#E63946']
bars3 = ax2.bar(categories, counts, color=colors_right, edgecolor='black', linewidth=1.5)

ax2.set_ylabel('Number of Listings', fontsize=13, fontweight='bold')
ax2.set_title('Listing Volume', fontsize=14, fontweight='bold', pad=15)
ax2.set_xticks(x)
ax2.set_xticklabels(categories, fontsize=12, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

# Add value labels and percentages
for bar, count in zip(bars3, counts):
    height = bar.get_height()
    percentage = (count / sum(counts)) * 100
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{count:,}\n({percentage:.1f}%)',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# Add premium calculation
premium = ((vip_avg - regular_avg) / regular_avg) * 100
plt.suptitle(f'VIP vs Regular Listings Analysis | VIP Premium: +{premium:.1f}%',
             fontsize=16, fontweight='bold', y=1.00)

plt.tight_layout()
plt.savefig('charts/09_vip_vs_regular.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# INSIGHT 10: Price per Square Meter by Location
# ============================================================================
print("10. Generating: Price per m² by location...")
location_price_per_sqm = defaultdict(list)
for item in baki_data:
    if item.get('location_name') and item.get('price_value') and item.get('area_value'):
        if item['area_value'] > 0:
            price_per_sqm = item['price_value'] / item['area_value']
            if 500 <= price_per_sqm <= 10000:  # Filter outliers
                location_price_per_sqm[item['location_name']].append(price_per_sqm)

# Get top 15 locations by average price per sqm
location_avg_sqm = {loc: np.mean(prices) for loc, prices in location_price_per_sqm.items()
                    if len(prices) >= 50}  # At least 50 properties
top_expensive_locations = sorted(location_avg_sqm.items(), key=lambda x: x[1], reverse=True)[:15]

plt.figure(figsize=(12, 9))
locs, prices_sqm = zip(*top_expensive_locations)
colors = sns.color_palette("flare", len(locs))
bars = plt.barh(range(len(locs)), prices_sqm, color=colors)
plt.yticks(range(len(locs)), locs)
plt.xlabel('Average Price per m² (AZN)', fontsize=13, fontweight='bold')
plt.ylabel('District', fontsize=13, fontweight='bold')
plt.title('Top 15 Most Expensive Districts in Baki (Price per m²)', fontsize=16, fontweight='bold', pad=20)
plt.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, price) in enumerate(zip(bars, prices_sqm)):
    plt.text(price + 50, i, f'{int(price):,}',
             va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/10_price_per_sqm_location.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "="*70)
print("✅ All charts generated successfully in charts/ directory!")
print("="*70)
