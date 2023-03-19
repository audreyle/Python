from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

import main

app = Flask(__name__, instance_path=str(Path.cwd().absolute()))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
api = Api(app)
db = SQLAlchemy(app)



class UserRecord(db.Model):
    __tablename__ = "usertable"
    user_id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    user_name = db.Column(db.String)
    user_last_name = db.Column(db.String)

    def serialize(self):
        """
        Helper method to generate json
        """
        return {
            "user_id": self.user_id,
            "email": self.email,
            "first_name": self.user_name,
            "last_name": self.user_last_name}


class ImageRecord(db.Model):
    __tablename__ = "picturetable"
    picture_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String)
    tags = db.Column(db.String)

    def serialize(self):
        """
        Helper method to generate json
        """
        return {
            "picture_id": self.picture_id,
            "user_id": self.user_id,
            "tags": self.tags}


class DifferenceRecord(db.Model):
    __tablename__ = "differencetable"
    missing_picture_in_disk = db.Column(db.String)
    user_id = db.Column(db.String, primary_key=True)

    def serialize(self):
        """
        Helper method to generate json
        """
        return {
            "missing_picture_in_disk": self.missing_picture_in_disk,
            "user_id": self.user_id}

class Users(Resource):
    def get(self):
        return jsonify([user.serialize() for user in UserRecord.query.all()])


class LookUpUser(Resource):
    def get(self, user_id):
        """
        Note that our people_id here matches what our route specified
        """
        return jsonify(
            UserRecord.query
            # Filter by id
            .filter_by(user_id=user_id)
            # Get the first one, or else raise a 404
            .first_or_404(description=f"Could not find user where id={user_id}")
            # Serialize it for json
            .serialize()
        )

class Images(Resource):
    def get(self):
        return jsonify([image.serialize() for image in ImageRecord.query.all()])

class LookUpImage(Resource):
    def get(self, picture_id):
        return jsonify(
            ImageRecord.query
            # Filter by id
            .filter_by(picture_id=picture_id)
            # Get the first one, or else raise a 404
            .first_or_404(description=f"Could not find user where id={picture_id}")
            # Serialize it for json
            .serialize()
        )

class Differences(Resource):
    def get(self):
        return jsonify([difference.serialize() for difference in DifferenceRecord.query.all()])

api.add_resource(Users, "/users/")
api.add_resource(LookUpUser, "/users/<user_id>")
api.add_resource(Images, "/images/")
api.add_resource(LookUpImage, "/images/<picture_id>")
api.add_resource(Differences, "/differences/")

if __name__ == '__main__':
    # my machine IP address:port: http://127.0.0.1:5002
    app.run(port=5002, debug=True)
