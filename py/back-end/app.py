from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# Ensure you have the correct username, password, host, and database name in the URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Wulinmp_930724@localhost/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

@app.route('/get_user_list', methods=['GET'])
def get_user_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)
    users = pagination.items
    
    return jsonify({
        'users': [{'id': user.id, 'name': user.name, 'gender': user.gender} for user in users],
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page
    }), 200

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    gender = data.get('gender')

    if not name or not gender:
        return jsonify({'message': 'Name and gender are required.'}), 400

    new_user = User(name=name, gender=gender)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'id': new_user.id, 'name': new_user.name, 'gender': new_user.gender}), 201

@app.route('/edit_user/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    user.name = data.get('name', user.name)
    user.gender = data.get('gender', user.gender)
    
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name, 'gender': user.gender}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
