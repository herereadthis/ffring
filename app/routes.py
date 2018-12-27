from app import app

# these are decorators
# whenever the browser requests either of these two routes, flask invokes the 
# next function
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"