import os
from werkzeug.utils import secure_filename
from flask import flash,send_file,redirect,Flask, request, abort, jsonify, send_from_directory ,render_template
from src.app import app
from src.tesseract_ocr import ocr


api = Flask(__name__)

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('upload.html')



@app.route("/files",methods=["GET"])
def get_file(path):
    """Download a file."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], path, as_attachment=True)


@app.route('/', methods=['POST'])
def upload_and_process():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			name=filename.split(".")[0]
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			myocr=ocr()
			filepath="data/"+filename
			image=myocr.readimage(filepath)
			downloadfile=myocr.get_pdf_with_ocr(image,name)

			flash('File successfully uploaded')
			flash('download?downloadfile='+downloadfile)
			os.remove(filepath)
			return redirect('/')
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)

@app.route('/download',methods=['GET'])
def download_file():
	downloadfile=request.args.get("downloadfile")
	file=send_from_directory(app.config['DOWNLOAD_FOLDER'],downloadfile, as_attachment=True)
	os.remove("processeddata/"+downloadfile)
	return file

if __name__ == "__main__":
    app.run()

