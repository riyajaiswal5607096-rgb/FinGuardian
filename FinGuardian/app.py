from flask import Flask,render_template,request,redirect
import sqlite3
def init_db():
    conn = sqlite3.connect("expense.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount INTEGER,
            category TEXT
        )
    """)
    conn.commit()
    conn.close()

app=Flask(__name__)
init_db()

def get_db():
	return sqlite3.connect("expense.db")

@app.route("/",methods=["GET","POST"])
def login():
	if request.method == "POST":
		return redirect("/add")
	return render_template("login.html")

@app.route("/add",methods=["GET","POST"])
def add_expense():
	if request.method=="POST":
		amount=request.form["amount"]
		category=request.form["category"]

		conn=get_db()
		cur=conn.cursor()
		cur.execute("INSERT INTO expenses (amount,category) VALUES (?,?)",(amount,category))
		conn.commit()
		conn.close()

		return redirect("/dashboard")
	return render_template("add_expense.html")

@app.route("/dashboard")
def dashboard():
		conn=get_db()
		cur=conn.cursor()
		cur.execute("SELECT * FROM expenses")
		data=cur.fetchall()
		conn.close()

		#total spending (expenses table:id,amount,category)
		total=sum([i[1] for i in data ]) if data else 0

		#build category totals of the chart
		category_data={}
		for i in data:
			category=i[2]
			amount=i[1]
			category_data[category]=category_data.get(category,0)+amount

		#ai suggestion logic
		if total>2000:
			ai_message="⚠ Overspending Alert !!! Reduce unnecessary expenses."
		else:
			ai_message="✅ Good spending control!! Try Saving more."
		return render_template("dashboard.html",expenses=data,total=total,ai_message=ai_message,categories=category_data)

if __name__=="__main__":

		app.run()
