# Olist Sales & Marketing Analytics Engineering

## Project Overview

This project develops a reproducible analytics workflow using Olist's Brazilian e-commerce and marketing funnel datasets.

The primary objective is to build a reliable seller-level analytical dataset and apply explainable machine learning to identify seller segments based on commercial performance and operational characteristics.

The project combines analytics engineering practices—data validation, documented metric definitions, reproducible transformations, and automated testing—with practical business analysis.

## Business Objectives

The project aims to answer the following questions:

- How do sellers differ in order volume and commercial performance?
- How does delivery performance vary across sellers?
- Can sellers be grouped into meaningful segments based on their observed business characteristics?
- Which characteristics distinguish each segment?
- What operational opportunities might each segment suggest?

The analysis is exploratory and observational. Segment membership will not be interpreted as evidence of causation.

## Data Sources

### Brazilian E-Commerce Public Dataset

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Includes orders, order items, customers, sellers, payments, reviews, products, and geolocation data.

### Marketing Funnel by Olist

https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist

Includes qualified marketing leads and closed-deal records. These tables may support exploratory analysis of lead-to-deal relationships and seller acquisition.

The datasets cover historical activity. Raw CSV files are stored locally and are not intended to be committed to this repository.

## Planned Analytical Approach

### 1. Data Validation and Modeling

- Document source table grains, keys, and relationships.
- Validate uniqueness, completeness, accepted values, and referential integrity.
- Define business metrics and their calculation rules.
- Aggregate source tables carefully to prevent duplicated or inflated metrics.

### 2. Seller Performance Dataset

Build a dataset with one row per seller, subject to source-data coverage and validation.

Candidate features include:

- Distinct order count
- Number of items sold
- Total item sales value, excluding freight
- Average order value, with a documented definition
- Average review score
- On-time delivery rate
- Average delivery time

Features will be evaluated for completeness, reliability, and suitability before being used in the model.

### 3. Seller Segmentation

Use K-Means clustering as the initial machine learning approach.

The workflow will include:

- Feature preparation and scaling
- Evaluation of candidate cluster counts
- Cluster quality assessment using metrics such as the silhouette score
- Segment profiling and interpretation
- Business recommendations grounded in observed segment characteristics

The final number of clusters and segment labels will be determined from the analysis rather than assumed in advance.

## Engineering Practices

The planned workflow will emphasize:

- Python-based data preparation
- Reproducible transformations
- Automated data quality tests
- Version control with Git and GitHub
- Clear metric definitions and technical documentation
- Automated test execution with GitHub Actions

Cloud warehouse integration and live API ingestion are outside the initial scope and may be considered as future extensions.

## Technology Stack

- Python
- pandas
- SQL, where appropriate for analytical transformations
- pytest
- scikit-learn for clustering
- Git and GitHub
- GitHub Actions for continuous integration
- A lightweight dashboard or visual report for communicating results

## Project Status

**Current stage: Interactive dashboard and exploratory seller segmentation completed.**

The project includes:

- Seller-level analytical feature engineering and data validation.
- Documented metric definitions and checks for table relationships.
- K-Means clustering with evaluation of candidate cluster counts.
- Seller segment profiling and interpretation of business implications.
- Automated tests for core analytical transformations.
- An interactive Streamlit dashboard with filters, visualizations, seller exploration, and CSV export.

The analysis is exploratory and observational. Cluster labels are descriptive, and sellers with limited order histories should be interpreted cautiously.

### Running the Dashboard

Install the dependencies and run the Streamlit app from the project root:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The dashboard requires the processed seller dataset at `data/processed/seller_segments.csv`. Raw source datasets and generated analytical outputs are excluded from version control. A deployment-ready data distribution strategy remains to be defined.

## Data Limitations

- The data represents historical activity and does not necessarily reflect current seller performance.
- Missing values require interpretation in context; they are not automatically data-quality failures.
- Seller performance metrics depend on documented aggregation and eligibility rules.
- Clusters describe patterns in the selected features and should not be interpreted as causal explanations.
- The marketing funnel data does not, by itself, establish that a particular lead caused subsequent seller revenue.

## Licensing and Attribution

The datasets are published by Olist on Kaggle. Review the applicable dataset licenses before redistributing raw data or derived materials. Raw source files are excluded from this repository.