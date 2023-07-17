from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Post:
    db="pulse_schema"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.post = data['post']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.owner = None

#create
    @classmethod
    def create_post(cls, data):
        query= """
        INSERT INTO posts (name, post, users_id)
        VALUES (%(name)s, %(post)s, %(users_id)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)
#read
    @classmethod
    def all_posts(cls):
        query="""
            SELECT * FROM posts
            JOIN users ON posts.users_id = users.id;
        """

        results = connectToMySQL(cls.db).query_db(query)

        all_posts=[]
        for row in results:
            one_post = cls(row)

            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'subscribe': row['subscribe'],
                'new_student': row['new_student'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
            }
            one_post.owner = user.User(user_data)
            all_posts.append(one_post)
        return all_posts

    @classmethod
    def get_one_post(cls, data):
        query="""
            SELECT * FROM posts
            JOIN users ON posts.users_id = users.id
            WHERE posts.id = %(id)s;
            """

        results = connectToMySQL(cls.db).query_db(query, data)

        one_post = cls(results[0])

        user_data = {
            'id': results[0]['users.id'],
            'first_name': results[0]['users.first_name'],
            'last_name': results[0]['users.last_name'],
            'email': results[0]['users.email'],
            'password': results[0]['users.password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at'],
            }
        one_post.owner = user.User(user_data)

        return one_post


#update
    @classmethod
    def update_post(cls, data):
        query= """
            UPDATE posts
            SET name = %(post)s, date_posted = %(date_posted)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)


#delete
    @classmethod 
    def delete_post(cls, data):
        query= """
            DELETE FROM posts
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

#validation for posts
    @staticmethod
    def validate_post(data):
        is_valid=True
        if len (data['post']) ==0:
            is_valid = False
            flash("You cannot submit an empty post", "post")
        return is_valid