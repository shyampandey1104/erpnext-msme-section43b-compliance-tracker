# ERPNext MSME Section 43B(h) Statutory Compliance Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Income Tax](https://img.shields.io/badge/Income%20Tax-Section%2043B%28h%29-red.svg)](https://incometaxindia.gov.in)

The #1 operational compliance pain point for Indian businesses. This engine tracks MSME Udyam status, computes statutory 15/45-day payment countdowns, and quantifies 31.2% corporate tax disallowance exposure.

## Key Capabilities
- **Udyam Category Evaluation:** Differentiates Micro, Small, and exempt Medium enterprises.
- **Contractual vs Statutory 15/45 Days:** Automatically enforces 15 days when no written contract exists, or up to 45 days under agreement.
- **Income Tax Disallowance Exposure:** Quantifies unexpected corporate tax liabilities at 31.2% on delayed disbursements.
- **Payment Priority Queue:** Identifies near-due MSME invoices to avert year-end tax penalties.

## Tests
```bash
python3 -m unittest discover tests
```
