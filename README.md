
# Olist Sales & Marketing Analytics

## Project Overview

This project builds a reproducible analytics workflow using real-world Brazilian e-commerce and marketing funnel datasets published by Olist.

The goal is to connect marketing funnel information with seller and order performance while applying analytics engineering practices such as data validation, documented business definitions, reliable transformations, and automated testing.

## Business Questions

- How do qualified marketing leads progress to closed deals?
- How long does it take for qualified leads to convert?
- How can seller and order performance be measured consistently?
- Which data quality issues could affect business reporting?

## Data Sources

1. **Brazilian E-Commerce Public Dataset:**  
   https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

2. **Marketing Funnel by Olist:**  
   https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist

The datasets cover historical activity. They will be downloaded and stored locally; raw CSV files will not be committed to this repository.

## Planned Technology Stack

- Python and pandas for data preparation
- SQL for analytical transformations
- Data quality checks and automated tests
- Git and GitHub for version control
- dbt and a cloud data warehouse as later project stages
- A dashboard for communicating business insights

## Data Quality and Modeling Principles

- Document the grain of each dataset.
- Define keys and relationships before joining tables.
- Validate uniqueness, completeness, and referential integrity.
- Separate observed facts from assumptions.
- Document metric definitions and transformation logic.

## Project Status

**Stage 1 — Project setup and source data preparation.**

Further stages will add validated transformations, tests, analytical models, and business insights.

## Licensing and Attribution

The datasets are published by Olist on Kaggle. Please review the applicable dataset licenses before redistributing data or derived materials.
