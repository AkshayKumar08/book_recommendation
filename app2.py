from flask import Flask, render_template, request
import sklearn, pandas, pickle
from book2 import Book

app = Flask(__name__)
data = pickle.load(open('data.pkl', 'rb'))
idlist = pickle.load(open('idlist.pkl', 'rb'))

def search_book(keyword):
	try:
		book_index = data[data['title'].astype(str).str.contains(keyword, case=False)].index
		if len(book_index) == 0:
			book_index = data[data['authors'].astype(str).str.contains(keyword, case=False)].index
		if len(book_index) == 0:
			book_index = data[data['publisher'].astype(str).str.contains(keyword, case=False)].index
		return book_index[0] if len(book_index) != 0 else 0
	except:
		return render_template('error.html', msg='Unexpected Error Occured')


def book_recommendation_engine2(keyword):
	try:
		res, book_index = {}, search_book(keyword)
		res['book_details'] = Book(data.loc[book_index])
		res['recommendations'] = map(lambda id: Book(data.loc[id]), idlist[book_index])
	except:
		return render_template('error.html', msg='Book Not Found')
	return res


@app.route('/')
def hello(): return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
	book_name = str(request.form['book']).strip()
	book_list_name = book_recommendation_engine2(book_name)
	return render_template('recommend2.html', result=book_list_name)

if __name__ == '__main__':
	app.run(debug=True) 
