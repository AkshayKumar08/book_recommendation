class Book:
	def __init__(self, data, dataset):
		self.isbn_10 = data.get('isbn_10')
		self.isbn_13 = data.get('isbn_13')
		self.title = data.get('title')
		self.publishers = data.get('publishers')
		self.publish_date = data.get('publish_date')
		self.description = data.get('description').get('value')
		self.number_of_pages = data.get('number_of_pages')

		# self.covers_s = "https://covers.openlibrary.org/b/id/{covers}-S.jpg".format(covers=data.get('covers'))
		self.covers_m = "https://covers.openlibrary.org/b/id/{covers}-M.jpg".format(covers=data.get('covers')[0])
		# self.covers_l = "https://covers.openlibrary.org/b/id/{covers}-L.jpg".format(covers=data.get('covers'))

		self.authors = dataset.get('authors')
		self.average_rating = dataset.get('average_rating')
		self.language_code = dataset.get('language_code')

		