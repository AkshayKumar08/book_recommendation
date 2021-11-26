from flask import Flask, render_template, request
import sklearn, pandas, pickle
from book2 import Book

app = Flask(__name__)
data = pickle.load(open('data.pkl', 'rb'))
idlist = pickle.load(open('idlist.pkl', 'rb'))

def search_book(keyword):
	book_index = data[data['title'].astype(str).str.contains(keyword, case=False)].index
	if len(book_index) == 0:
		book_index = data[data['authors'].astype(str).str.contains(keyword, case=False)].index
	if len(book_index) == 0:
		book_index = data[data['publisher'].astype(str).str.contains(keyword, case=False)].index
	return book_index[0] if len(book_index) != 0 else -1


def book_recommendation_engine2(keyword):
	res, book_index = {}, search_book(keyword)
	if book_index < 0: return book_index
	res['book_details'] = Book(data.loc[book_index])
	res['recommendations'] = map(lambda id: Book(data.loc[id]), idlist[book_index])
	return res

@app.route('/')
def index(): return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
	book_name = str(request.form['book']).strip()
	book_list = book_recommendation_engine2(book_name)
	if type(book_list) == int: return render_template('error.html', msg='Book Not Found')
	return render_template('recommend2.html', result=book_list)

if __name__ == '__main__':
	app.run(debug=True) 
