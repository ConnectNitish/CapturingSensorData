from flask import Flask,render_template,jsonify
app= Flask(__name__)



networkInfo={
	"user1":["tyagi","10.0.9.266"],
	"user2":["nitish","31.0.1.10"],
	"user3":["jha","12.0.99.101"],
	"user4":["chitta","17.10.990.1"]
	}


wifi={
	"user1":["12","3","123"],
	"user2":["17","1","787"],
	"user3":["10","1","1819"],
	"user4":["20","2","876"]
}


# def get_data():
#     return jsonify({'data':networkInfo}) 





@app.route("/")
@app.route("/home")
def index():
	return render_template('layout.html', networkInfo=networkInfo,wifi=wifi)
 



if __name__ == '__main__':
	app.run(debug=True)