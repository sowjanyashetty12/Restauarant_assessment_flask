from flask import Flask,render_template,url_for,redirect,flash,request
import psycopg2,os
from form import add_product_form,updateform,orderForm
app=Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
# connecting  to the db function
def db_connection():
    conn=psycopg2.connect(database="Restaurant_db",host="localhost",user="postgres",password="shetty12",port="5432")
    return conn

   
@app.route('/Products')
def get_allproducts():
 conn=db_connection()
 cur=conn.cursor()
 cur.execute('''SELECT * FROM produts''')
 productss=cur.fetchall()
 conn.close()
 if len(productss)==0:
  return("No products at the moment")
 else:
   return render_template("allproducts.html",products=productss)

@app.route('/addProduct',methods=['GET','POST'])
def add_product():
  form=add_product_form()
  if form.validate_on_submit():
    print("atleat here")
    product_name=form.productname.data
    product_price=form.productprice.data
    conn=db_connection()
    cur=conn.cursor()
    print("came here")
    cur.execute('''INSERT INTO produts(name,price) VALUES(%s,%s)''',(product_name,product_price))
    conn.commit()
    conn.close()
    flash("Product added successfully")
    return redirect(url_for('get_allproducts'))
  else:
    return render_template("addproduct.html",form=form)


@app.route("/deleteproduct/<int:id>",methods=["POST","GET"])

def delete(id):
 if request.method=="POST":

  conn=db_connection()
  cur=conn.cursor()
  cur.execute('''DELETE FROM produts WHERE id=%s''',(id,))
  conn.commit()
  conn.close()
  flash("The product has been deleted successfully")
  return redirect(url_for("get_allproducts"))
 else:
  return render_template("Delete.html",idgiven=id)
 
@app.route("/updateproduct/<int:id>" ,methods=["GET","POST"])
def update(id):
  form=updateform()
  name=form.productname.data
  price=form.productprice.data
  if request.method=="POST":
   conn=db_connection()
   cur=conn.cursor()
   cur.execute('''Update produts set name=%s , price=%s WHERE id =%s''' ,(name,price,id))
   conn.commit()
   conn.close()
   flash("The product has been updated successfully")
   return redirect(url_for("get_allproducts"))
  else:
  
    return render_template("updateform.html",id=id,form=form)
  
@app.route("/order", methods=["GET","POST"])
def order():
  form=orderForm()
  productname=request.form.get("productname")
  quantity=form.quantity.data
  if request.method=='POST':
   conn=db_connection()
   cur=conn.cursor()
   cur.execute('''INSERT INTO orders (prodcut_name,quantity) VALUES(%s,%s)''',(productname,quantity)) 
   conn.commit()
   conn.close()
   flash("your order has been taken")
   conn=db_connection()
   cur=conn.cursor()
   cur.execute('''SELECT * FROM orders''')
   order=cur.fetchall()
   conn.commit()
   conn.close()
   return render_template("orderlist.html",list=order)
  else:
    conn=db_connection()
    cur=conn.cursor()
    cur.execute('''SELECT name FROM produts''')
    data=cur.fetchall()
    conn.commit()
    conn.close()
    return render_template("orderform.html",form=form,products=data)
if __name__=="__main__":
 app.run(debug=True)