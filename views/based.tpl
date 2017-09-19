<html>
    
    <meta charset="utf-8">
    <link rel="stylesheet" href="{{iid}}/static/views/{{css_file}}"
          type="text/css" />    
    <head><title>{{'Home page'}}</title></head>
    <body>

         <h3>Home</h3>

	 <hr>
         
         <form action="/comm_run" method="post">
            <input name="comm" type="text" />
            <input value="Enter command" type="submit" />
        </form>

    </body>
</html>
