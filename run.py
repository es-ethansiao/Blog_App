# =====!!!!!!!!!!===== RUN BLOG APP FROM HERE =====!!!!!!!!!!=====

from main_app import app

# Allows main app to run the web server
if __name__=='__main__':
    app.run(debug=True)
