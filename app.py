from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'QCUey0U2EHJZGfbtY-qChGB2PJjO1wF2A1GJ1Z6dWhA'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html', title='Миссия Колонизация Марса')

@app.route('/index')
def index():
    return render_template('index.html', title='И на Марсе будут яблони цвести!')

@app.route('/promotion')
def promotion():
    promotion_list = [
        'Человечество вырастает из детства.',
        'Человечеству мала одна планета.',
        'Мы сделаем обитаемыми безжизненные пока планеты.',
        'И начнем с Марса!',
        'Присоединяйся!'
    ]
    return render_template('promotion.html', promotions=promotion_list)

@app.route('/image_mars')
def image_mars():
    return render_template('image_mars.html')

@app.route('/astronaut_selection', methods=['GET', 'POST'])
def astronaut_selection():
    if request.method == 'POST':
        flash('Данные успешно отправлены!', 'success')
        return redirect(url_for('astronaut_selection'))
    professions = [
        'инженер-исследователь', 'пилот', 'строитель', 'экзобиолог',
        'врач', 'инженер по терраформированию', 'климатолог',
        'специалист по радиационной защите', 'астрогеолог', 'гляциолог',
        'инженер жизнеобеспечения', 'метеоролог', 'оператор марсохода',
        'киберинженер', 'штурман', 'пилот дронов'
    ]
    return render_template('astronaut_selection.html', professions=professions)

@app.route('/results/<nickname>/<int:level>/<float:rating>')
def results(nickname, level, rating):
    return render_template('results.html', nickname=nickname, level=level, rating=rating)

@app.route('/photo/<nickname>', methods=['GET', 'POST'])
def photo(nickname):
    filename = None
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('Файл не выбран', 'error')
        else:
            file = request.files['photo']
            if file.filename == '':
                flash('Файл не выбран', 'error')
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{nickname}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                filename = unique_filename
            else:
                flash('Недопустимый тип файла', 'error')
    
    if filename and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        filepath = url_for('static', filename=f'uploads/{filename}')
    else:
        filepath = None
        
    return render_template('photo.html', nickname=nickname, filepath=filepath)

@app.route('/carousel')
def carousel():
    images = [
        url_for('static', filename='images/mars1.jpg'),
        url_for('static', filename='images/mars2.jpg'),
        url_for('static', filename='images/mars3.jpg'),
    ]
    return render_template('carousel.html', images=images)

if __name__ == '__main__':
    app.run(port=8080, debug=True)