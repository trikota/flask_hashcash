# flask_hashcash
Force user to send Hashcash proof-of-work with each request.

All magic happens in cookies. 
Don't worry about including PoW by hand. Multiple tabs opened is not a problem.

It's very easy to use:
```python
@app.route('/')
@validate_work(difficulty = 5, wrong_solution_response = loading_solution_response)
def index():
    return render_template('index.html')

# in case user browse too fast show loading page
def loading_solution_response():
    return make_response(render_template('loading.html'))
```
And in frontend 
```html
<script src="static/js/sha1.js"></script>
<script src="static/js/flask_hashcash.js"></script>
<script>
  findHashcashSolution(); // find hashcash solution on page load
  $(document).ajaxSuccess(function(event, xhr, settings){
      findHashcashSolution(); // find hashcash solution after each ajax call
  });
</script>
```
`THIS IS IMPORTANT! You have to use server-side sessions `

Check out example project in this repo.

On default difficulty firefox finds Hashcash solution in ~0.3s. After solution has been found it sits in cookies waiting for user actions
