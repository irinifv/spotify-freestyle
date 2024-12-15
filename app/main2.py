from app import create_app

# Create the Flask app using the factory function
app = create_app()

if __name__ == "__main__":
    # Run the app in debug mode
    app.run(debug=True)