from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
	def __init__( self , data ):
		self.id = data['id']
		self.title = data['title']
		self.num_of_pages = data['num_of_pages']
		self.created_at = data['created_at']
		self.updated_at = data['updated_at']
		
		self.authors = []

	@classmethod
	def get_all(cls):
		query = "SELECT * FROM books;"

		results = connectToMySQL('books_schema').query_db(query)
		books = []
		for book in results:
			books.append( cls(book) )
		return books

	@classmethod
	def save(cls, data ):
		query = "INSERT INTO books ( title, num_of_pages, created_at, updated_at ) VALUES ( %(title)s, %(pages)s , NOW() , NOW() );"
		return connectToMySQL('books_schema').query_db( query, data )

	@classmethod
	def get_book_by_id(cls, data):
		query = "SELECT * FROM books WHERE id = %(id)s;"
		result = connectToMySQL('books_schema').query_db( query, data )

		if len(result) < 1:
			return False
		return cls(result[0]) 


#=============================================================================================================#


	@classmethod
	def get_book_with_authors(cls, data):
		query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors ON authors.id = favorites.author_id WHERE book_id = %(id)s;"
		results = connectToMySQL('books_schema').query_db( query , data )

		if len(results) == 0:
			return 0	
			
		else:
			book = cls(results[0])
			for row_from_db in results:
				authors_data = {
					"id" : row_from_db["authors.id"],
					"name" : row_from_db["name"],
					"created_at" : row_from_db["authors.created_at"],
					"updated_at" : row_from_db["authors.updated_at"]		
				}
				book.authors.append(author.Author( authors_data) )
			return book
