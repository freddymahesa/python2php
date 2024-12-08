import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, env_path='.env'):
        # Load environment variables from .env file
        load_dotenv(env_path)
        
        # Read database connection details from environment variables
        self.host = os.getenv('DB_HOST', 'localhost')
        self.database = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.port = os.getenv('DB_PORT', '3306')
        
        # Connection and cursor attributes
        self.connection = None
        self.cursor = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("Successfully connected to the database")
                return True
        
        except Error as e:
            print(f"Error: {e}")
            return False
        
    def get_all_table_names(self):
        try:
            # Ensure we have an active connection
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            # Create a cursor with a different return type
            cursor = self.connection.cursor()
            
            # Query to get table names
            cursor.execute("SHOW TABLES")
            
            # Fetch all table names and flatten the list
            tables = [table[0] for table in cursor.fetchall()]
            
            # Close the temporary cursor
            cursor.close()
            
            return tables
        
        except Error as e:
            print(f"Error retrieving table names: {e}")
            return []
        
    def get_table_fields(self, table_name):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            # Query to get table column information
            query = f"DESCRIBE {table_name}"
            
            # Execute the query
            self.cursor.execute(query)
            
            # Fetch all column descriptions
            fields = self.cursor.fetchall()
            
            # Transform the results into a more readable format
            field_descriptions = []
            for field in fields:
                field_descriptions.append({
                    'name': field['Field'],
                    'type': field['Type'],
                    'null': field['Null'] == 'YES',
                    'key': field['Key'],
                    'default': field['Default'],
                    'extra': field['Extra']
                })
            
            return field_descriptions
        
        except Error as e:
            print(f"Error retrieving table fields: {e}")
            return None
        
    def get_primary_key(self, table_name):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            # Query to get table column information
            query = f"DESCRIBE {table_name}"
            
            # Execute the query
            self.cursor.execute(query)
            
            # Fetch all column descriptions
            fields = self.cursor.fetchall()
            
            # Find the primary key
            for field in fields:
                if field['Key'] == 'PRI':
                    return field['Field']
            
            # No primary key found
            return None
        
        except Error as e:
            print(f"Error retrieving primary key: {e}")
            return None
    
    def execute_query(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            return self.cursor.fetchall()
        
        except Error as e:
            print(f"Query execution error: {e}")
            return None
    
    def execute_insert(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            self.connection.commit()
            return self.cursor.lastrowid
        
        except Error as e:
            print(f"Insert error: {e}")
            self.connection.rollback()
            return None
    
    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
                
        except Error as e:
            print(f"Error closing connection: {e}")