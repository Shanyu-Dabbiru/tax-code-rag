# Parsing Discoveries & Constraints

- **Data Format**: The US Code Bulk data is fragmented into thousands of individual `.htm` files (e.g., `sec9834.htm`).
- **Front-Matter Skips**: Files ending in `-front.htm` are tables of contents and lack statutes. They should be skipped safely.
- **Hidden Metadata**: Critical hierarchy and ID data are hidden in HTML comments.
  - Regex for Hierarchy: `<!-- itempath:(.*?)-->`
  - Regex for Primary ID: `<!-- documentid:(.*?)usckey:(.*?)-->`
- **Content Boundaries**: The actual law begins immediately after the marker: `<!-- field-start:statute -->`.