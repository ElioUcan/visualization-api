# VisualizationAPI

Loads CSV data files into a PostgreSQL database for visualization and analysis.

## Requirements

- Python 3.8+
- PostgreSQL

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and fill in your database credentials:

```bash
cp .env.example .env
```

| Variable      | Description              | Default     |
|---------------|--------------------------|-------------|
| `DB_HOST`     | PostgreSQL host          | `localhost` |
| `DB_PORT`     | PostgreSQL port          | `5432`      |
| `DB_NAME`     | Database name            | required    |
| `DB_USER`     | Database user            | required    |
| `DB_PASSWORD` | Database password        | _(empty)_   |

## Data

CSV files in `data/` are loaded automatically. Known tables are created with typed columns, primary keys, and foreign keys when the necessary CSV columns exist.

Current datasets:

- `accounts.csv`
- `branches.csv`
- `cards.csv`
- `customers.csv`
- `loans.csv`
- `merchants.csv`

Relationships currently supported by the repo data:

- `accounts.customer_id -> customers.customer_id`
- `cards.account_id -> accounts.account_id`
- `loans.customer_id -> customers.customer_id`

If future CSVs include columns such as `accounts.branch_id`, `loans.account_id`, or a `transactions.csv` file, the loader is prepared to create those relationships too.

## Usage

```bash
python scripts/load_csv_to_db.py
```

The script will:

1. Connect to the database using the `.env` credentials.
2. Create or extend tables based on the CSV headers.
3. Add primary keys and supported foreign-key relationships.
4. Insert all rows in dependency order.
