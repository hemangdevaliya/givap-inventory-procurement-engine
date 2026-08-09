# 🛒 GIVAP — Inventory & Procurement Management Engine

**GIVAP** is a real-time inventory and procurement management application built with **Python, Streamlit, Pandas, and PostgreSQL**.

The system connects directly to a PostgreSQL inventory database, provides live inventory monitoring, records customer sales and distributor stock receipts, calculates profit, evaluates inventory conditions, and generates automated procurement recommendations.

---

## 🚀 Features

* 📊 Real-time PostgreSQL inventory dashboard
* 🛒 Customer sales transaction management
* 📦 Distributor stock receiving
* 📈 Weekly sales and inventory analysis
* 💰 Automatic profit calculation
* 🤖 Automated procurement decision engine
* 🚨 Stockout protection
* 📥 CSV report generation and export
* 🔐 Secure database configuration using `.env`
* 📁 Input and generated-result folder support
* 🐍 Python virtual environment support
* 🗄️ PostgreSQL-backed inventory ledger

---

## 🧰 Technology Stack

| Technology    | Purpose                                |
| ------------- | -------------------------------------- |
| Python        | Application development                |
| Streamlit     | Web application interface              |
| Pandas        | Data processing and analytics          |
| PostgreSQL    | Inventory database                     |
| Psycopg2      | PostgreSQL database connection         |
| python-dotenv | Secure environment variable management |

---

## 📁 Project Structure

```text
givap-inventory-procurement-engine/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── input/
│   └── Input files used by the application
│
├── generated_result/
│   └── Automatically generated output files
│
├── venv/
│   └── Local Python virtual environment
│
└── .env
    └── Local environment configuration
```

### Important

The following are **local-only files/folders** and should not be uploaded to GitHub:

```text
.env
venv/
.venv/
```

Generated result files can also be excluded from GitHub depending on your project requirements.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd givap-inventory-procurement-engine
```

---

## 2. Create a Python Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
streamlit
pandas
psycopg2-binary
python-dotenv
```

---

# 🔐 Environment Configuration

GIVAP uses environment variables to securely store PostgreSQL connection information.

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_NAME=my_retail_db
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
DB_PORT=5432
```

### Environment Variables

| Variable      | Description               | Example         |
| ------------- | ------------------------- | --------------- |
| `DB_HOST`     | PostgreSQL server address | `localhost`     |
| `DB_NAME`     | PostgreSQL database name  | `my_retail_db`  |
| `DB_USER`     | PostgreSQL username       | `postgres`      |
| `DB_PASSWORD` | PostgreSQL password       | `your_password` |
| `DB_PORT`     | PostgreSQL port           | `5432`          |

---

## 🔒 Security

**Never commit your real `.env` file to GitHub.**

Your `.env` file may contain sensitive database credentials.

Instead, create `.env.example`:

```env
DB_HOST=localhost
DB_NAME=my_retail_db
DB_USER=postgres
DB_PASSWORD=
DB_PORT=5432
```

The `.env.example` file can safely be committed to GitHub.

---

# 🛡️ Git Ignore Configuration

Create a `.gitignore` file in the project root:

```gitignore
# Python virtual environments
venv/
.venv/

# Environment variables and secrets
.env
.env.*
!.env.example

# Python cache
__pycache__/
*.py[cod]

# Streamlit secrets
.streamlit/secrets.toml

# Generated result files
generated_result/*
!generated_result/.gitkeep
```

If you want GitHub to display the `generated_result` folder even when it is empty, create:

```text
generated_result/.gitkeep
```

This keeps the folder structure while preventing generated output files from being committed.

---

# 🗄️ PostgreSQL Database

GIVAP expects a PostgreSQL database containing an `inventory_ledger` table.

The application uses the following columns:

| Column              | Description                          |
| ------------------- | ------------------------------------ |
| `sku`               | Unique product identifier            |
| `item_name`         | Product name                         |
| `weekly_units_sold` | Number of units sold during the week |
| `current_stock`     | Current inventory quantity           |
| `unit_cost_inr`     | Product purchase cost                |
| `selling_price_inr` | Product selling price                |

---

## Database Table

Example PostgreSQL table:

```sql
CREATE TABLE inventory_ledger (
    sku VARCHAR(50) PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    weekly_units_sold INTEGER DEFAULT 0,
    current_stock INTEGER DEFAULT 0,
    unit_cost_inr NUMERIC(12,2) NOT NULL,
    selling_price_inr NUMERIC(12,2) NOT NULL
);
```

---

## Example Inventory Data

```sql
INSERT INTO inventory_ledger
    (
        sku,
        item_name,
        weekly_units_sold,
        current_stock,
        unit_cost_inr,
        selling_price_inr
    )
VALUES
    ('SKU001', 'Product A', 350, 100, 50, 80),
    ('SKU002', 'Product B', 20, 100, 40, 65),
    ('SKU003', 'Product C', 4, 60, 30, 45);
```

You can replace this example data with your actual inventory records.

---

# 🧠 Procurement Decision Engine

GIVAP automatically evaluates inventory based on:

* Weekly units sold
* Current stock
* Profit per unit
* Inventory-to-demand ratio

The system produces one of the following procurement decisions:

```text
add stock
remove stock
change stock
no new stock needed
```

---

## 📦 Add Stock

A product receives an **`add stock`** recommendation when:

```text
Weekly sales >= 300
AND
Current stock < 50% of weekly sales
```

This identifies high-demand products with relatively low inventory.

---

## 🗑️ Remove Stock

A product receives a **`remove stock`** recommendation when:

```text
Weekly sales <= 5
AND
Current stock > 10 × weekly sales
```

This identifies slow-moving products with excessive inventory.

---

## ✅ No New Stock Needed

A product receives a **`no new stock needed`** recommendation when:

```text
0.8 × weekly sales <= current stock <= 1.5 × weekly sales
```

This indicates that current inventory is reasonably aligned with demand.

---

## 🔄 Change Stock

A product may receive a **`change stock`** recommendation when:

```text
Weekly sales > 5
AND
Current stock > 2 × weekly sales
AND
Profit per unit >= ₹20
```

This identifies products with excess inventory where the product still generates a relatively strong profit.

---

# 💰 Profit Calculation

GIVAP calculates profit per unit using:

```text
Profit Per Unit =
Selling Price - Unit Cost
```

For example:

```text
Selling Price = ₹80
Unit Cost = ₹50

Profit Per Unit = ₹30
```

---

## Weekly Total Profit

Weekly profit is calculated using:

```text
Total Profit =
Weekly Units Sold × Profit Per Unit
```

The dashboard aggregates these values to display:

```text
Weekly Net Total Profit
```

---

# 🛒 Customer Sales

The **Live Register Terminal** allows the operator to record customer purchases.

When a sale is completed, the application updates PostgreSQL:

```text
Current Stock
    ↓
Current Stock - Quantity Sold
```

and:

```text
Weekly Units Sold
    ↓
Weekly Units Sold + Quantity Sold
```

The application also checks inventory availability before processing a sale.

If there is insufficient stock, the transaction is rejected and a stockout warning is displayed.

---

# 📦 Distributor Stock Receiving

The application supports incoming distributor inventory.

When new stock is received:

```text
Current Stock
    ↓
Current Stock + Quantity Received
```

The PostgreSQL inventory ledger is updated immediately.

---

# 📊 Real-Time Dashboard

The GIVAP dashboard provides:

* Current inventory
* Weekly sales
* Unit cost
* Selling price
* Profit per unit
* Total profit
* Procurement decision

The procurement decision is visually highlighted using different colors:

| Decision                 | Meaning                           |
| ------------------------ | --------------------------------- |
| 🟥 `add stock`           | Additional inventory recommended  |
| ⬜ `remove stock`         | Reduce excess inventory           |
| 🟨 `change stock`        | Review and adjust inventory       |
| 🟩 `no new stock needed` | Inventory is currently acceptable |

---

# 📥 CSV Export

GIVAP provides an operational data export feature.

The analyzed inventory data can be exported as:

```text
postgres_procurement_result.csv
```

The exported report contains the inventory information along with calculated profit and procurement decisions.

---

# ▶️ Running the Application

Make sure:

1. PostgreSQL is running.
2. The database exists.
3. The `inventory_ledger` table exists.
4. Your `.env` file contains the correct database credentials.
5. Your virtual environment is activated.

Then run:

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

# 🔧 Troubleshooting

## PostgreSQL Connection Error

If you see a database connection error, check:

```text
DB_HOST
DB_NAME
DB_USER
DB_PASSWORD
DB_PORT
```

Also verify that PostgreSQL is running.

---

## Module Not Found

If Python reports that a module is missing:

```bash
pip install -r requirements.txt
```

Make sure the virtual environment is activated before running the application.

---

## `.env` Not Working

Make sure the `.env` file is located in the project root:

```text
givap-inventory-procurement-engine/
│
├── app.py
├── .env
└── requirements.txt
```

The application loads the environment variables using `python-dotenv`.

---

# 🌿 Git & GitHub Setup

After creating the project:

```bash
git init
```

Check your files:

```bash
git status
```

Add the project:

```bash
git add .
```

Create your first commit:

```bash
git commit -m "Initial GIVAP project setup"
```

Rename the branch to `main`:

```bash
git branch -M main
```

Connect your GitHub repository:

```bash
git remote add origin YOUR_GITHUB_REPOSITORY_URL
```

Push the project:

```bash
git push -u origin main
```

---

# 🔐 Before Pushing to GitHub

Always run:

```bash
git status
```

Make sure you **do not see**:

```text
.env
venv/
.venv/
```

You can also verify which files Git is tracking:

```bash
git ls-files
```

Your real `.env` file and virtual environment should not appear in the output.

---

# ⚠️ If `.env` Was Already Committed

If you accidentally added `.env` or `venv` to Git before creating `.gitignore`, remove them from Git tracking:

```bash
git rm --cached .env
git rm -r --cached venv
```

If `.venv` was also tracked:

```bash
git rm -r --cached .venv
```

Then commit:

```bash
git add .
git commit -m "Remove local environment files from repository"
git push
```

If a real password, API key, or other secret was already pushed to GitHub, **rotate/change that credential immediately**. Removing the file from the latest commit does not make an exposed secret safe.

---

# 📌 Recommended Repository Information

### Repository Name

```text
givap-inventory-procurement-engine
```

### GitHub Description

> Real-time inventory and procurement management engine built with Python, Streamlit, PostgreSQL, and Pandas, featuring automated stock decisions, sales tracking, profit analytics, and CSV reporting.

---

# 🎯 Project Objective

The goal of GIVAP is to provide a centralized inventory intelligence platform that helps businesses:

* Monitor inventory in real time
* Track customer sales
* Record incoming stock
* Understand product profitability
* Identify overstocked products
* Identify products requiring replenishment
* Support data-driven procurement decisions
* Export operational inventory reports

---

# 📈 Future Improvements

Potential future enhancements include:

* 📊 Interactive sales charts
* 📅 Historical inventory analysis
* 📈 Demand forecasting
* 🤖 Machine-learning-based procurement recommendations
* 🔔 Low-stock notifications
* 👥 User authentication and role management
* 📋 Supplier management
* 🧾 Invoice history
* 📱 Mobile-friendly dashboard
* ☁️ Cloud PostgreSQL deployment
* 🚀 Streamlit Cloud or other cloud deployment

---

# 👨‍💻 Project

**GIVAP — Inventory & Procurement Management Engine**

Built with:

**Python • Streamlit • Pandas • PostgreSQL**

GIVAP combines real-time inventory data with automated analytical rules to support smarter procurement and inventory management.
