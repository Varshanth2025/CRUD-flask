from flask import Flask,jsonify,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
from datetime import datetime

#Flask appp setup
app=Flask(__name__)
Scss(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///drinks_data.db'
db=SQLAlchemy(app)

#database object-table
class drinks(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40),unique=True,nullable=False)
    size=db.Column(db.String(25),nullable=False) 
    price=db.Column(db.Integer,default=0)
    added=db.Column(db.DateTime,default=datetime.utcnow)

    def to_dict(self):
       return {
        "id":self.id,
        "name":self.name,
        "size":self.size,
        "price":self.price
       }
        
#Home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        size = request.form['size']
        price = request.form['price']
        
        new_data = drinks(name=name, size=size, price=int(price))
        try:

            db.session.add(new_data)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"ERROR:{e}"    
    else:
        data=drinks.query.order_by(drinks.added).all()    
    return render_template('index.html',data=data)


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


