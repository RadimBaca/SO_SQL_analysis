# StackOverflow Post.xml Importer

This script parses a `posts.xml` file, filters relevant PostgreSQL-related questions/answers, and inserts them into a PostgreSQL database using a schema defined in `init.sql`.

## Requirements

- Python 3.7+
- PostgreSQL instance
- Virtual environment (recommended)

## Setup on Windows

### 1. Clone the repository or download the files

Make sure you have:
- `main.py`
- `dao.py`
- `init.sql`
- `posts.xml`
- `.env`
- `requirements.txt`

### 2. Init and Run

Clone the repository and set up the virtual environment:

```powershell
git clone https://github.com/RadimBaca/SO_SQL_analysis
cd SO_SQL_analysis
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python init.py  
```

