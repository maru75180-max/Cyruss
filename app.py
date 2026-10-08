from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("database.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS businesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT NOT NULL,
            owner_name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            category TEXT,
            details TEXT,
            facebook TEXT,
            instagram TEXT,
            website TEXT,
            logo_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    count = conn.execute("SELECT COUNT(*) FROM businesses").fetchone()[0]

    if count == 0:
        samples = [
            ("Juan's Computer Shop", "Juan Dela Cruz", "0917-123-4567",
             "juan@email.com", "General Trias, Cavite", "Computer Services",
             "Computer repair, printing, accessories and software services.",
             "https://facebook.com/", "https://instagram.com/", "", ""),
            ("Maria's Bakery", "Maria Santos", "0918-555-7890",
             "maria@email.com", "Dasmarinas, Cavite", "Food & Bakery",
             "Fresh bread, cakes, pastries and customized desserts.",
             "https://facebook.com/", "https://instagram.com/", "", ""),
            ("TechFix Solutions", "Carlo Reyes", "0920-333-1111",
             "carlo@email.com", "Imus, Cavite", "IT Services",
             "Computer troubleshooting, networking and technical support.",
             "https://facebook.com/", "https://instagram.com/", "", "")
        ]

        conn.executemany("""
            INSERT INTO businesses
            (business_name, owner_name, phone, email, address, category,
             details, facebook, instagram, website, logo_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, samples)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    businesses = [dict(row) for row in conn.execute(
        "SELECT * FROM businesses ORDER BY id DESC").fetchall()]
    total = conn.execute("SELECT COUNT(*) FROM businesses").fetchone()[0]
    categories = conn.execute("""
        SELECT COUNT(DISTINCT category) FROM businesses
        WHERE category IS NOT NULL AND category != ''
    """).fetchone()[0]
    conn.close()
    return render_template("index.html", businesses=businesses,
                           total=total, categories=categories)


@app.route("/business/<int:business_id>")
def business_profile(business_id):
    conn = get_db()
    business = conn.execute(
        "SELECT * FROM businesses WHERE id = ?", (business_id,)).fetchone()
    conn.close()
    if business is None:
        return render_template("404.html"), 404
    return render_template("business.html", business=business)


@app.route("/add", methods=["POST"])
def add_business():
    data = request.form
    if not data.get("business_name", "").strip() or not data.get("owner_name", "").strip():
        return redirect(url_for("index"))

    conn = get_db()
    conn.execute("""
        INSERT INTO businesses
        (business_name, owner_name, phone, email, address, category,
         details, facebook, instagram, website, logo_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("business_name", "").strip(),
        data.get("owner_name", "").strip(),
        data.get("phone", "").strip(),
        data.get("email", "").strip(),
        data.get("address", "").strip(),
        data.get("category", "").strip(),
        data.get("details", "").strip(),
        data.get("facebook", "").strip(),
        data.get("instagram", "").strip(),
        data.get("website", "").strip(),
        data.get("logo_url", "").strip()
    ))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/edit/<int:business_id>", methods=["POST"])
def edit_business(business_id):
    data = request.form
    conn = get_db()
    conn.execute("""
        UPDATE businesses
        SET business_name = ?, owner_name = ?, phone = ?, email = ?,
            address = ?, category = ?, details = ?, facebook = ?,
            instagram = ?, website = ?, logo_url = ?
        WHERE id = ?
    """, (
        data.get("business_name", "").strip(),
        data.get("owner_name", "").strip(),
        data.get("phone", "").strip(),
        data.get("email", "").strip(),
        data.get("address", "").strip(),
        data.get("category", "").strip(),
        data.get("details", "").strip(),
        data.get("facebook", "").strip(),
        data.get("instagram", "").strip(),
        data.get("website", "").strip(),
        data.get("logo_url", "").strip(),
        business_id
    ))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:business_id>", methods=["POST"])
def delete_business(business_id):
    conn = get_db()
    conn.execute("DELETE FROM businesses WHERE id = ?", (business_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/api/businesses")
def api_businesses():
    conn = get_db()
    businesses = [dict(row) for row in conn.execute(
        "SELECT * FROM businesses ORDER BY id DESC").fetchall()]
    conn.close()
    return jsonify(businesses)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
