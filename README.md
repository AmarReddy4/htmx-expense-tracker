# htmx Expense Tracker

A server-rendered expense tracking dashboard built with Flask and htmx. No JavaScript framework needed — htmx handles all the interactivity with simple HTML attributes.

Wanted to try the htmx approach after seeing all the hype. For a small CRUD app like this, it's surprisingly clean compared to spinning up a full React/Vue frontend.

## Tech Stack

- **Flask 2.3** — Python web framework
- **htmx 1.9** — Interactive HTML without writing JS
- **Tailwind CSS** — Styling via CDN
- **SQLite** — Embedded database

## Features

- Add, edit, and delete expenses (all without full page reloads)
- Category breakdown with visual progress bars
- Summary cards (total spent, entry count, top category)
- Inline row editing via htmx swaps

## Getting Started

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Opens at `http://localhost:5000`

## How htmx Works Here

- `hx-post="/expenses"` — submits the form via AJAX, swaps the dashboard HTML
- `hx-delete="/expenses/{id}"` — deletes with a confirmation dialog
- `hx-get="/expenses/{id}/edit"` — swaps a table row with an inline edit form
- `hx-put="/expenses/{id}"` — saves the edit and refreshes the dashboard

No build step, no node_modules, no bundler. Just Python + HTML.
