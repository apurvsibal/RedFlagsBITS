import waitress
import Back_Pain_App

waitress.serve(app.app, host='0.0.0.0', port=40000)