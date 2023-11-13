from flask import Flask, render_template, request
import csv
import random
import os

app = Flask(__name__)

# CSV file to store user data
CSV_FILE = 'users_data.csv'
# IMAGE_FOLDER = '../Generate_images/Images'
IMAGE_FOLDER = 'static/images'

@app.route('/')
def index():
    random_image_info = get_random_image()
    if random_image_info:
        random_image, random_image_name = random_image_info
    else:
        random_image = ''
        random_image_name = ''
    return render_template('index.html', random_image=random_image, random_image_name=random_image_name)

@app.route('/record_choice', methods=['POST'])
def record_choice():
    user_choice = request.form.get('choice')
    image_filename = request.form.get('image_filename')

    # Write user choice and image filename to the CSV file
    with open(CSV_FILE, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([user_choice, image_filename])

    return 'Choice recorded successfully'

@app.route('/get_random_image', methods=['GET'])
def get_random_image():
    random_image_info = choose_random_image()
    if random_image_info:
        random_image, random_image_name = random_image_info
        return random_image, 200  # Return the image URL with a 200 OK status
    else:
        return '', 404  # Return an empty response with a 404 status if no image is available

def choose_random_image():
    image_files = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]
    if image_files:
        random_image_filename = random.choice(image_files)
        random_image = os.path.join('static/images', random_image_filename)
        random_image_name = os.path.basename(random_image_filename)
        return random_image, random_image_name
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True,port=3333)

