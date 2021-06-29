from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)
ma = Marshmallow(app)

class Article(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(100))
    date = db.Column(db.DateTime,default=datetime.datetime.now)

    def __init__(self,title,body):
        self.title = title
        self.body = body



class ArticlesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')



article_schema = ArticlesSchema()
articles_schema = ArticlesSchema(many=True)



@app.route('/get', methods=['GET'])
def get_articles():
    all_articles = Article.query.all()
    results = articles_schema.dump(all_articles)
    return jsonify(results)

@app.route('/get/<id>/', methods=['GET'])
def post_details(id):
    article = Article.query.get(id)
   
    return article_schema.jsonify(article)


@app.route('/update/<id>',methods=['PUT'])
def update_article(id):
    article = Article.query.get(id)
    title = request.json['title']
    body = request.json['body']

    article.title = title
    article.body = body

    db.session.commit()
    return article_schema.jsonify(article)



@app.route('/delete/<id>',methods=['DELETE'])
def delete_article(id): 
    article = Article.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return article_schema.jsonify(article)


@app.route('/add', methods=['POST'])
def add_article():
    title = request.json['title']
    body = request.json['body']

    articles =Article(title,body)
    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)


if __name__ == "__main__":
 app.run(debug=True)