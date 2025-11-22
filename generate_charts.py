#!/usr/bin/env python3
"""
Data Analysis and Chart Generation Script for KADR ENIC Candidates
Generates comprehensive visualizations and insights from candidate data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking charts
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create charts directory
os.makedirs('charts', exist_ok=True)

print("Loading data...")
# Load the CSV data
df = pd.read_csv('kadr_enic_candidates.csv')

# Clean data - remove rows with missing critical information
df_clean = df[df['name'] != '--'].copy()
df_clean = df_clean[df_clean['country'] != '--'].copy()

print(f"Total records: {len(df)}")
print(f"Valid records: {len(df_clean)}")
print(f"Records with missing data: {len(df) - len(df_clean)}")

# Parse birth dates
df_clean['birth_date'] = pd.to_datetime(df_clean['birth_date'], format='%d.%m.%Y', errors='coerce')
df_clean['birth_year'] = df_clean['birth_date'].dt.year
df_clean['age'] = 2025 - df_clean['birth_year']

# ============================================================================
# CHART 1: Distribution by Country (Top 15)
# ============================================================================
print("\nGenerating Chart 1: Distribution by Country...")
plt.figure(figsize=(14, 8))
country_counts = df_clean['country'].value_counts().head(15)

colors = sns.color_palette("viridis", len(country_counts))
bars = plt.bar(range(len(country_counts)), country_counts.values, color=colors, edgecolor='black', linewidth=1.2)

plt.xlabel('Country', fontsize=14, fontweight='bold')
plt.ylabel('Number of Candidates', fontsize=14, fontweight='bold')
plt.title('Top 15 Countries by Number of Candidates', fontsize=16, fontweight='bold', pad=20)
plt.xticks(range(len(country_counts)), country_counts.index, rotation=45, ha='right', fontsize=11)
plt.yticks(fontsize=11)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, country_counts.values)):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f'{int(value)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/01_distribution_by_country.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/01_distribution_by_country.png")

# ============================================================================
# CHART 2: Distribution by Education Level
# ============================================================================
print("\nGenerating Chart 2: Distribution by Education Level...")
plt.figure(figsize=(12, 8))
education_counts = df_clean['education_level'].value_counts()

colors = sns.color_palette("Set3", len(education_counts))
wedges, texts, autotexts = plt.pie(education_counts.values,
                                     labels=education_counts.index,
                                     autopct='%1.1f%%',
                                     startangle=90,
                                     colors=colors,
                                     textprops={'fontsize': 11, 'fontweight': 'bold'},
                                     explode=[0.05] * len(education_counts))

# Make percentage text more visible
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(12)
    autotext.set_fontweight('bold')

plt.title('Distribution by Education Level', fontsize=16, fontweight='bold', pad=20)
plt.axis('equal')
plt.tight_layout()
plt.savefig('charts/02_distribution_by_education_level.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/02_distribution_by_education_level.png")

# ============================================================================
# CHART 3: Top 15 Specializations
# ============================================================================
print("\nGenerating Chart 3: Top 15 Specializations...")
plt.figure(figsize=(14, 10))
spec_counts = df_clean['specialization'].value_counts().head(15)

colors = sns.color_palette("rocket", len(spec_counts))
bars = plt.barh(range(len(spec_counts)), spec_counts.values, color=colors, edgecolor='black', linewidth=1.2)

plt.ylabel('Specialization', fontsize=14, fontweight='bold')
plt.xlabel('Number of Candidates', fontsize=14, fontweight='bold')
plt.title('Top 15 Most Popular Specializations', fontsize=16, fontweight='bold', pad=20)
plt.yticks(range(len(spec_counts)), spec_counts.index, fontsize=11)
plt.xticks(fontsize=11)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, spec_counts.values)):
    plt.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
             f'{int(value)}', ha='left', va='center', fontsize=10, fontweight='bold')

plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('charts/03_top_specializations.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/03_top_specializations.png")

# ============================================================================
# CHART 4: Age Distribution
# ============================================================================
print("\nGenerating Chart 4: Age Distribution...")
plt.figure(figsize=(14, 8))

# Remove outliers and invalid ages
age_data = df_clean['age'].dropna()
age_data = age_data[(age_data >= 18) & (age_data <= 80)]

plt.hist(age_data, bins=25, color='skyblue', edgecolor='black', linewidth=1.2, alpha=0.8)
plt.axvline(age_data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean Age: {age_data.mean():.1f}')
plt.axvline(age_data.median(), color='green', linestyle='--', linewidth=2, label=f'Median Age: {age_data.median():.1f}')

plt.xlabel('Age (years)', fontsize=14, fontweight='bold')
plt.ylabel('Number of Candidates', fontsize=14, fontweight='bold')
plt.title('Age Distribution of Candidates', fontsize=16, fontweight='bold', pad=20)
plt.legend(fontsize=12)
plt.grid(axis='y', alpha=0.5)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)

plt.tight_layout()
plt.savefig('charts/04_age_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/04_age_distribution.png")

# ============================================================================
# CHART 5: Top 15 Universities
# ============================================================================
print("\nGenerating Chart 5: Top 15 Universities...")
plt.figure(figsize=(14, 10))
uni_counts = df_clean['university'].value_counts().head(15)

colors = sns.color_palette("mako", len(uni_counts))
bars = plt.barh(range(len(uni_counts)), uni_counts.values, color=colors, edgecolor='black', linewidth=1.2)

plt.ylabel('University', fontsize=14, fontweight='bold')
plt.xlabel('Number of Candidates', fontsize=14, fontweight='bold')
plt.title('Top 15 Universities by Number of Candidates', fontsize=16, fontweight='bold', pad=20)
plt.yticks(range(len(uni_counts)), uni_counts.index, fontsize=10)
plt.xticks(fontsize=11)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, uni_counts.values)):
    plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
             f'{int(value)}', ha='left', va='center', fontsize=10, fontweight='bold')

plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('charts/05_top_universities.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/05_top_universities.png")

# ============================================================================
# CHART 6: Birth Year Trends
# ============================================================================
print("\nGenerating Chart 6: Birth Year Trends...")
plt.figure(figsize=(14, 8))

# Filter valid birth years
birth_year_data = df_clean['birth_year'].dropna()
birth_year_data = birth_year_data[(birth_year_data >= 1950) & (birth_year_data <= 2010)]
birth_year_counts = birth_year_data.value_counts().sort_index()

plt.plot(birth_year_counts.index, birth_year_counts.values,
         marker='o', linewidth=2.5, markersize=6, color='darkblue', alpha=0.7)
plt.fill_between(birth_year_counts.index, birth_year_counts.values, alpha=0.3, color='lightblue')

plt.xlabel('Birth Year', fontsize=14, fontweight='bold')
plt.ylabel('Number of Candidates', fontsize=14, fontweight='bold')
plt.title('Candidate Distribution by Birth Year', fontsize=16, fontweight='bold', pad=20)
plt.grid(True, alpha=0.5)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)

plt.tight_layout()
plt.savefig('charts/06_birth_year_trends.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/06_birth_year_trends.png")

# ============================================================================
# CHART 7: Country vs Education Level (Heatmap for Top 10 Countries)
# ============================================================================
print("\nGenerating Chart 7: Country vs Education Level Heatmap...")
plt.figure(figsize=(14, 10))

# Get top 10 countries
top_countries = df_clean['country'].value_counts().head(10).index
df_top_countries = df_clean[df_clean['country'].isin(top_countries)]

# Create cross-tabulation
country_edu_crosstab = pd.crosstab(df_top_countries['country'],
                                    df_top_countries['education_level'])

# Create heatmap
sns.heatmap(country_edu_crosstab, annot=True, fmt='d', cmap='YlOrRd',
            linewidths=0.5, cbar_kws={'label': 'Number of Candidates'})

plt.xlabel('Education Level', fontsize=14, fontweight='bold')
plt.ylabel('Country', fontsize=14, fontweight='bold')
plt.title('Top 10 Countries vs Education Level Distribution', fontsize=16, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right', fontsize=11)
plt.yticks(rotation=0, fontsize=11)

plt.tight_layout()
plt.savefig('charts/07_country_education_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/07_country_education_heatmap.png")

# ============================================================================
# CHART 8: Specialization Categories (Grouped)
# ============================================================================
print("\nGenerating Chart 8: Specialization Categories...")
plt.figure(figsize=(14, 8))

# Categorize specializations
def categorize_specialization(spec):
    spec_lower = str(spec).lower()
    if any(word in spec_lower for word in ['kompüter', 'informatik', 'it', 'texnologi', 'proqramlaşdırma']):
        return 'IT & Computer Science'
    elif any(word in spec_lower for word in ['hüquq', 'law']):
        return 'Law'
    elif any(word in spec_lower for word in ['iqtisad', 'biznes', 'menec', 'maliyyə', 'economy', 'finance']):
        return 'Business & Economics'
    elif any(word in spec_lower for word in ['tibb', 'müalicə', 'stomatolo', 'bacı', 'medical', 'health']):
        return 'Medicine & Health'
    elif any(word in spec_lower for word in ['mühəndis', 'engineer', 'texnik']):
        return 'Engineering'
    elif any(word in spec_lower for word in ['dil', 'language', 'linqvistik']):
        return 'Languages & Linguistics'
    elif any(word in spec_lower for word in ['psixolog', 'pedaqo', 'təhsil', 'psychology', 'education']):
        return 'Psychology & Education'
    elif any(word in spec_lower for word in ['dövlət', 'idarə', 'government', 'administration']):
        return 'Public Administration'
    else:
        return 'Other'

df_clean['spec_category'] = df_clean['specialization'].apply(categorize_specialization)
category_counts = df_clean['spec_category'].value_counts()

colors = sns.color_palette("Set2", len(category_counts))
bars = plt.bar(range(len(category_counts)), category_counts.values, color=colors, edgecolor='black', linewidth=1.2)

plt.xlabel('Specialization Category', fontsize=14, fontweight='bold')
plt.ylabel('Number of Candidates', fontsize=14, fontweight='bold')
plt.title('Distribution by Specialization Categories', fontsize=16, fontweight='bold', pad=20)
plt.xticks(range(len(category_counts)), category_counts.index, rotation=45, ha='right', fontsize=11)
plt.yticks(fontsize=11)

# Add value labels on bars
for bar, value in zip(bars, category_counts.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f'{int(value)}', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/08_specialization_categories.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: charts/08_specialization_categories.png")

# ============================================================================
# Generate Summary Statistics
# ============================================================================
print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

print(f"\nTotal Candidates: {len(df_clean)}")
print(f"Number of Countries: {df_clean['country'].nunique()}")
print(f"Number of Universities: {df_clean['university'].nunique()}")
print(f"Number of Specializations: {df_clean['specialization'].nunique()}")

print("\n--- Age Statistics ---")
print(f"Mean Age: {age_data.mean():.1f} years")
print(f"Median Age: {age_data.median():.1f} years")
print(f"Age Range: {age_data.min():.0f} - {age_data.max():.0f} years")

print("\n--- Top 5 Countries ---")
for i, (country, count) in enumerate(country_counts.head(5).items(), 1):
    percentage = (count / len(df_clean)) * 100
    print(f"{i}. {country}: {count} ({percentage:.1f}%)")

print("\n--- Education Level Distribution ---")
for level, count in education_counts.items():
    percentage = (count / len(df_clean)) * 100
    print(f"  {level}: {count} ({percentage:.1f}%)")

print("\n--- Top 5 Specializations ---")
for i, (spec, count) in enumerate(spec_counts.head(5).items(), 1):
    percentage = (count / len(df_clean)) * 100
    print(f"{i}. {spec}: {count} ({percentage:.1f}%)")

print("\n" + "="*80)
print("✓ All charts generated successfully in /charts directory!")
print("="*80)

# Save statistics to file
with open('charts/statistics.txt', 'w', encoding='utf-8') as f:
    f.write("KADR ENIC CANDIDATES - STATISTICAL SUMMARY\n")
    f.write("="*80 + "\n\n")
    f.write(f"Total Candidates: {len(df_clean)}\n")
    f.write(f"Number of Countries: {df_clean['country'].nunique()}\n")
    f.write(f"Number of Universities: {df_clean['university'].nunique()}\n")
    f.write(f"Number of Specializations: {df_clean['specialization'].nunique()}\n")
    f.write(f"\nMean Age: {age_data.mean():.1f} years\n")
    f.write(f"Median Age: {age_data.median():.1f} years\n")
    f.write(f"Age Range: {age_data.min():.0f} - {age_data.max():.0f} years\n")
    f.write("\nTop 5 Countries:\n")
    for i, (country, count) in enumerate(country_counts.head(5).items(), 1):
        percentage = (count / len(df_clean)) * 100
        f.write(f"{i}. {country}: {count} ({percentage:.1f}%)\n")

print("\n✓ Statistics saved to: charts/statistics.txt")
