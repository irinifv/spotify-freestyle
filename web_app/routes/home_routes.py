from flask import Blueprint, request, render_template, redirect, url_for

# Define the blueprint
home_routes = Blueprint("home_routes", __name__)

# Home route
@home_routes.route("/")
@home_routes.route("/home")
def index():
    """
    Handle the home page.
    """
    print("HOME route accessed.")
    return render_template("home.html")

# About route
@home_routes.route("/about")
def about():
    """
    Handle the about page.
    """
    print("ABOUT route accessed.")
    return render_template("about.html")

# Hello route with optional query parameter
@home_routes.route("/hello")
def hello_world():
    """
    Handle the hello page. Optionally takes a 'name' query parameter.
    Example: /hello?name=Harper
    """
    print("HELLO route accessed.")

    url_params = dict(request.args)
    print("URL PARAMS:", url_params)

    name = url_params.get("name", "World")
    message = f"Hello, {name}!"
    print("GREETING MESSAGE:", message)

    return render_template("hello.html", message=message)

# Search route
@home_routes.route("/search", methods=["GET", "POST"])
def search():
    """
    Handle search functionality.
    If POST: process search form input.
    If GET: render search page.
    """
    print("SEARCH route accessed.")

    if request.method == "POST":
        # Extract search query from form
        search_query = request.form.get("query")
        print("SEARCH QUERY:", search_query)

        if not search_query:
            # Redirect back to the search page if query is missing
            return redirect(url_for("home_routes.search"))

        # Perform some action with the search query (e.g., API call)
        # For now, just pass the query to the results template
        return render_template("search_results.html", query=search_query)

    # Render the search page
    return render_template("search.html")

# @home_routes.route("/search/results", methods=["GET", "POST"])
# def search():
#     """
#     Handle search functionality.
#     If POST: process search form input.
#     If GET: render search page.
#     """
#     print("SEARCH route accessed.")

#     return render_template("search_results.html")
