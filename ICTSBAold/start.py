from bracketer import app
print("ADMIN USERNAME :\'admin\'")
print("ADMIN PASSWORD :\'4vacM7WYkUwUy39\'")
if __name__ == '__main__':
    app.run(debug=True)
    app.config['SECRET_KEY'] = 'roxy'
