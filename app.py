from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///drinks_data.db'
db=SQLAlchemy(app)

class drinks(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40),unique=True,nullable=False)
    size=db.Column(db.String(25),nullable=False)

    def to_dict(self):
       return {
        "id":self.id,
        "name":self.name,
        "size":self.size
       }
        


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return "Hello! sunny  welcum"


@app.route('/data',methods=['GET'])
def page1():
    d=drinks.query.all()
    return jsonify([drink.to_dict() for drink in d])



@app.route('/data/<int:id>',methods=['GET'])
def get_data(id):
    d=drinks.query.get(id)
    if d:
        return   jsonify(d.to_dict())
    else:
        return jsonify({"error":"data not found"}),404


@app.route('/data',methods=['POST'])
def post_data():
    data=request.get_json()
    new=drinks(name=data['name'],size=data['size'])
    db.session.add(new)
    db.session.commit()
    return jsonify(new.to_dict()),201


@app.route('/data/<int:id>',methods=['PUT'])
def put_data(id):
    data=request.get_json()
    drink=drinks.query.get(id)
    if drink:
        drink.name=data.get('name',drink.name)
        drink.size=data.get('size',drink.size)
        db.session.commit()
        return jsonify(drink.to_dict()),201
    else:
 
        return jsonify({'error':"id not found"}),404

@app.route('/data/<int:id>',methods=['DELETE'])
def delete_data(id):
    data=drinks.query.get(id)
    if data:
        db.session.delete(data)
        db.session.commit()

        return jsonify({"message":"delted the data"}),201
    else:
        return jsonify({"message":"Id not found"}),404    

if __name__=="__main__":
    app.run(debug=True)


