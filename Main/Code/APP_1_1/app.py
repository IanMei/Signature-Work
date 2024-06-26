from flask import Flask, render_template, request, send_from_directory
import os
import openai
import wget 

app = Flask(__name__, template_folder='templates')

# Define the function to generate an image
def generate_image(text):
    # Replace this with your image generation logic
    # The function should take text as input and return a URL for the generated image
    # For demonstration purposes, we'll return a placeholder image URL
    
    openai.api_key = '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'
    
    prompt = "Take a Chinese poem to analyze the objects in it and the emotions or feelings that the poem describe. Turn it into a text prompt less than 1000 letters for DALLE. The prompt must shorter than 1000 letters(including space). In the text prompt, descirbe objects in the picture with their color and their postion in the picture. Then, gave brief desicription about what background should looks like (color and scene). Also, don't forget this is a Chinese poem so the view and buildings and other things should looks like ancient Chinese style. There should not be any text and watermark in this generated image. Here is the Chinese poem:"

    text_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",   ## text-davinci-003
        messages=[{'role':'user','content':prompt+text}],
        temperature=0,
        max_tokens=256
    )
    
    prompt = text_response.choices[0].message['content']
    
    print(prompt)
    
    img_response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    
    image_url =img_response['data'][0]['url']
    
    print(image_url)
    
    return image_url

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_image_url = None
    download_url = None
    download_filename = None
    input_text = ""

    if request.method == 'POST':
        
        input_text = request.form.get('input-text')
        
        # Call the generate_image function to get the image URL
        generated_image_url = generate_image(input_text)

        # Create a download URL for the generated image
        download_url = f"/download/{input_text}.png"
        # download_url = generated_image_url
        download_filename = f"{input_text}.png"

    return render_template('index.html', generated_image_url=generated_image_url, input_text=input_text, download_url=download_url, download_filename=download_filename)

@app.route('/download/<filename>')
def download(filename):
    # Serve the generated image for download
    return send_from_directory('static/output_images', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
