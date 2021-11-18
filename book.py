class Book:
	def __init__(self, data):
		self.isbn13 = data['industryIdentifiers'][0]['identifier']
		self.isbn10 = data['industryIdentifiers'][1]['identifier']
		self.title = data['title']
		self.authors = ",".join(data['authors'])
		self.publisher = data['publisher']
		self.published_date = data['publishedDate']
		self.description = data['description']
		self.page_count = data['pageCount']
		self.img_link_small = data['imageLinks']['smallThumbnail']
		self.img_link_large = data['imageLinks']['thumbnail']
		self.language = data['language']