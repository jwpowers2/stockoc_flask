
import re,atexit,csv,time
from flask import Flask, render_template, request, redirect,flash,session 
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from collections import deque
from stock_api_call import ApiCall

app = Flask(__name__)    

TEST_STOCKS = [['GOOGL', 'Alphabet', '1100'],
              ['GE', 'General Electric', '14.5'],
              ['AMZN', 'Amazon', '1500'],
              ['TSLA', 'Tesla', '333'],
              ['TXT', 'Textron', '59'],
              ['F', 'Ford', '10'],
              ['BABA', 'Alibaba', '190'],
              ['F5', 'F5 networks', '50']]

d = deque()
input_file = csv.DictReader(open("nasdaq.csv"))
for row in input_file:
    row['price'] = None
    d.appendleft(row)

def rotate_queue():
    d.rotate(1) 
    d[0]['price'] = ApiCall().ticker_api_call(d[0]['Symbol'])

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=rotate_queue,
    trigger=IntervalTrigger(seconds=5),
    id='rotate queue',
    name='rotate last in stock queue to first',
    replace_existing=True)


atexit.register(lambda: scheduler.shutdown())



@app.route('/', methods=['GET'])          

def index():
   
  stock_list = [[d[0]['Symbol'],d[0]['Name'],d[0]['price']],[d[1]['Symbol'],d[1]['Name'],d[1]['price']],          
		[d[2]['Symbol'],d[2]['Name'],d[2]['price']],[d[3]['Symbol'],d[3]['Name'],d[3]['price']],          
		[d[4]['Symbol'],d[4]['Name'],d[4]['price']]]          

  return render_template('index.html',ticker_list=stock_list)
                         
@app.route('/stock', methods=['POST'])          

def stock():

  # I'll be working on making a query box for stocks and present graphs on screen

  if re.search("\W",request.form['stock']):
      flash("Not a valid stock symbol")
      return redirect("/")


  if len(request.form['stock']) < 1:
      flash("Stock symbol blank")
      return redirect("/")

  return redirect("/")

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)      

