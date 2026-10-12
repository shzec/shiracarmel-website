# Shira Z. Carmel — Website

Static artist website and electronic press kit, prepared for GitHub Pages.

## Publish

Publish the `main` branch from the repository root in **Settings → Pages → Build and deployment**. The `CNAME` file configures `shiracarmel.com` after the repository's Pages settings and DNS are updated.

## Update tour dates

Edit the `tourDates` array near the top of `content.js`. Add each show with its date, ISO date, title, venue, optional venue URL, and time.

## EPK PDF

The online EPK downloads `assets/epk-shira-z-carmel.pdf`. Rebuild it after content changes with `python make_epk_pdf.py` (requires ReportLab and Pillow).
