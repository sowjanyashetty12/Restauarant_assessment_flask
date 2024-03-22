from flask_wtf import FlaskForm
import psycopg2
from wtforms import StringField,IntegerField,SubmitField
from wtforms.validators import DataRequired,ValidationError
class add_product_form(FlaskForm):
    productname=StringField('name',validators=[DataRequired()])
    productprice=IntegerField('price',validators=[DataRequired()])
    submit=SubmitField('Submit')
    def validate_productname(self,field):
     print("Field data:", field.data)
     conn=psycopg2.connect(
     database="Restaurant_db",host="localhost",user="postgres",password="shetty12",port="5432"
) 
     cur=conn.cursor()
     cur.execute('''SELECT * FROM produts WHERE name=%s''',(field.data,))
     user=cur.fetchone()
     cur.close()
     conn.close()
     if user:
         raise ValidationError("Product already exsits")


class updateform(FlaskForm):
    productname=StringField('name',validators=[DataRequired()])
    productprice=IntegerField('price',validators=[DataRequired()])
    submit=SubmitField('Submit')
    
    