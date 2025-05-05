from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
                                   

@app.route('/')
def home():
    return render_template('home.html')