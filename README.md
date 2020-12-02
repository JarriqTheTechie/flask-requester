# Welcome to flask-requester!

**Flask requester** provides a clean way to retrieve data from a flask request. In most cases flask-requester completely replaces the need to use any of the following commands in your flask web application. 
eg:
 - **request.form**
 - **requests.args**
 - **requests.files**


# Getting Started!

 1. Clone repo into your application
 2. Import into your flask project ```from flask_requester import requester```

# Example Usage
simple-form.html
```
<form action="/" method="get">
	<input type="text" name="username" placeholder="Username">
	<input type="password" name="password" placeholder="Password">
	<div>
		<input type="checkbox" name="remember" checked>
		<label for="remember">Remember Me?</label>
	</div>
	<button type="submit">Submit</button>
</form>
```


In our flask route we can can use flask-requester like this:

```
@app.route('/', methods=['POST', 'GET'])  
def hello_world():  
    if request.method == 'GET':
	    # This will print all request data to the console.
	    print(requester.all())  
        return render_template('index.html')  
    else:  
        return redirect(url_for('hello_world'))
```




# Methods

 - Retrieving all input data
`requester.all()`

 - Retrieve specific input data
`requester.input('username')`

 - Retrieve truth or false value from checkboxes.
`requester.boolean('remember')`

 - Retrieve specific parts of input data
`requester.only(['username', 'password'])`

 - Ignore some parts of input data
`requester.ignore(['password', 'remember'])`

 - Return True if input data has key
`requester.has('username')`

 - Return True if input data has key and is filled 
`requester.filled('username')`

 - Return True if input data is missing key 
`requester.missing('username')`

**File Uploads**
 - Retrieving specific file input
`requester.file('file')`

 - Return True if input data has specific file
`requester.hasFile('file')`

 - Store file to a specific location
`requester.store('file', UPLOAD_DIR)`

