from flask import Flask 
app =  Flask(__name__)
@app.route('/')
def todolist():
    return("your todolist is here ")


if __name__ == '__main__':
    app.run(debug=True)