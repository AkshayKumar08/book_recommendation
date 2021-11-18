from flask import Flask, render_template, request, jsonify
import sklearn, pandas, pickle, requests
from book2 import Book

app = Flask(__name__)
data = pickle.load(open('data.pkl', 'rb'))
idlist = pickle.load(open('idlist.pkl', 'rb'))


def search_book(book_name):
	books_index = data[data['title'].astype(str).str.contains(book_name, case=False)].index
	if len(books_index) == 0:
		books_index = data[data['authors'].astype(str).str.contains(book_name, case=False)].index
	if len(books_index) == 0:
		books_index = data[data['publisher'].astype(str).str.contains(book_name, case=False)].index
	return books_index


def book_recommendation_engine(book_name):
	books_index = search_book(book_name)
	books_rec, items, res = [], [], {}
	try:
		if len(books_index) != 0:
			book_index = books_index[0]
			books_rec.append(data.loc[book_index]);
			for each_id in idlist[book_index]:
				books_rec.append(data.loc[each_id])

			for book in books_rec[:2]:
				url = "https://openlibrary.org/isbn/{isbn}.json".format(isbn=book.isbn13)
				# url = "".join(['https://www.googleapis.com/books/v1/volumes?q=', str(isbn13)])
				print(url)
				req = requests.get(url).json()
				items.append(Book(req, book))
			res['book_details'] = items[0]
			res['recommendations'] = items[1:]
			print(res['book_details'].covers_m)
	except Exception as e: 
		print(e)
		return render_template("error.html", msg="Book Not Found")
	return res


@app.route('/')
def hello(): return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
	try:
		book_name = str(request.form['book']).strip()
		recommendations = book_recommendation_engine(book_name)
		return render_template('recommend.html', result=recommendations)
	except: return render_template('error.html')

if __name__ == '__main__':
	app.run(debug=True) 
