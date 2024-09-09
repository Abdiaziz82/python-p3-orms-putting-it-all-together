import sqlite3

# Database connection
CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
    
    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS dogs"
        CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO dogs(name, breed)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.lastrowid  # Set the dog's id to the last inserted row id
    
    @classmethod
    def create(cls, name, breed):  
        new_dog = cls(name, breed)
        new_dog.save()
      
        return new_dog


    @classmethod
    def new_from_db(cls, row):
     
        dog = cls(row[1], row[2])  # Create a new instance using name and breed
        dog.id = row[0]  # Set the id attribute from the row
        return dog
    
    @classmethod
    def get_all(cls):
       
        sql = "SELECT * FROM dogs"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall() 
        dogs = [cls.new_from_db(row) for row in rows]  # Convert each row to a Dog instance
        return dogs
    @classmethod
    def find_by_name(cls, name):
      
        sql = "SELECT * FROM dogs WHERE name = ?"
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()  # Fetch the first row that matches the name

        if row:
            return cls.new_from_db(row)  # Create a Dog instance from the row
        else:
            return None 
        
    @classmethod

    def find_by_id(cls, dog_id):
 
        sql = "SELECT * FROM dogs WHERE id = ?"
        CURSOR.execute(sql, (dog_id,))
        row = CURSOR.fetchone()

        if row:
            return cls.new_from_db(row)  # Create and return a Dog instance
        else:
            return None
        
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = "SELECT * FROM dogs WHERE name = ? AND breed = ? LIMIT 1"
        row = CURSOR.execute(sql, (name, breed)).fetchone()
        
        if row:
            return cls.new_from_db(row)
        
        # If no dog is found, create a new dog and save it to the database
        new_dog = cls.create(name, breed)
        return new_dog
    
    def update(self):
        # SQL query to update the record in the database
        sql = '''
        UPDATE dogs 
        SET name = ?, breed = ?
        WHERE id = ?
        '''
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()