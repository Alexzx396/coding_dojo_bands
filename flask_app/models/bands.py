from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Bands:
    db_name = 'examen'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.Founding = db_data['Founding']
        self.Genre = db_data['Genre']

        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO bands (name, Founding, Genre) VALUES (%(name)s,%(Founding)s,%(Genre)s );"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def saveJoin(cls,data):
        query = "INSERT INTO examen.join (Bands_id, users_id) VALUES (%(id)s,%(user)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def quitJoin(cls,data):
        query = "delete from examen.join where Bands_id =%(id)s and users_id =%(user)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def get_all(cls,data):
        query = "SELECT j.users_id, u.first_name, u.last_name, u.email, b.id as bands_id, b.name, b.Founding, b.Genre from examen.bands b left join examen.join j on b.id = j.Bands_id left join examen.users u on j.users_id = u.id and u.id=%(id)s;"
        results =  connectToMySQL(cls.db_name).query_db(query,data)
        all_bands = []
        for row in results:
            all_bands.append( row )
        return all_bands

    @classmethod
    def getBands_by_user(cls,data):
        query = "SELECT j.users_id, u.first_name, u.last_name, u.email, j.bands_id, b.name, b.Founding, b.Genre FROM examen.join j inner join examen.users u on j.users_id = u.id inner join examen.bands b on j.bands_id = b.id where u.id =%(id)s group by j.users_id, u.first_name, u.last_name, u.email, j.bands_id, b.name, b.Founding, b.Genre;"
        results =  connectToMySQL(cls.db_name).query_db(query,data)
        all_bands = []
        for row in results:
            all_bands.append( row )
        return all_bands

    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM bands WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )


    @classmethod
    def update(cls, data):
        query = "UPDATE bands SET name=%(name)s, Founding=%(Founding)s, Genre=%(Genre)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM bands WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_bands(bands):
        is_valid = True
        if len(bands['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters","bands")
        if len(bands['Genre']) < 3:
            is_valid = False
            flash("Genre must be at least 3 characters","bands")
        if len(bands['Founding']) < 3:
            is_valid = False
            flash("Founding must be at least 3 characters","bands")
        return is_valid