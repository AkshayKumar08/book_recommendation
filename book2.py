class Book:
	def __init__(self, data):
		self.title = data['title']
		self.authors = data['authors']
		self.average_rating = data['average_rating']
		self.isbn = data['isbn']
		self.isbn13 = data['isbn13']
		self.language_code = data['language_code']
		self.rating_count = data['ratings_count']
		self.text_reviews_count = data['text_reviews_count']
		self.publication_date = data['publication_date']
		self.publisher = data['publisher']
		