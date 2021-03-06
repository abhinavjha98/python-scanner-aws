import os,io
# from google.cloud import vision
# from google.cloud.vision import types
import pandas as pd
from werkzeug.utils import secure_filename
import pyrebase
from firebase import firebase
from flask import *
import pandas as pd
app = Flask(__name__)
app.secret_key = "hello"
import httplib2
from PIL import Image

config = {
	"apiKey": "AIzaSyDcIab8JfwOMLUdeOIE4n8SpWqW3_S-GVM",
    "authDomain": "talentsetu-a4710.firebaseapp.com",
    "databaseURL": "https://talentsetu-a4710.firebaseio.com",
    "projectId": "talentsetu-a4710",
    "storageBucket": "talentsetu-a4710.appspot.com",
    "messagingSenderId": "476128197051",
    "appId": "1:476128197051:web:4e5f2a6d4520f07d34ec9e",
    "measurementId": "G-6CRFJBEQGV",
    "serviceAccount": "service.json"
}



http = httplib2.Http()
http.redirect_codes = http.redirect_codes - {308}
FBConn = firebase.FirebaseApplication('https://talentsetu-a4710.firebaseio.com/')

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ServiceAccount.json'
# client = vision.ImageAnnotatorClient()

# file_name = 'pan.jpeg'
# image_path = f'E:\PROJECT\\aadhar_OCR\{file_name}'

# with io.open(image_path, 'rb') as image_file:
# 		content = image_file.read()

# image = vision.types.Image(content=content)
# response = client.text_detection(image=image,  image_context={"language_hints": ["en"]})
# texts = response.text_annotations
# df = pd.DataFrame(columns=['locale', 'description'])

# for text in texts:
# 		df = df.append(
# 					dict(
# 				locale=text.locale,
# 				description=text.description
# 				),
#  				ignore_index=True
# 		)
# data_text=[]
# for i in df:
# 	data_text.append(df[i][0])

# print(df['description'][0])
# print(data_text)


@app.route('/',methods=["GET","POST"])
def pan():
	a=""
	name_of_person=""
	name=""
	pan_card=""
	datee=""
	father=""
	ad=""
	date=""
	datess=[]
	pan_c=""
	if request.method == "POST":
		if request.form['upload']=="Upload":
			upload = request.files['upload']
			filename = secure_filename(upload.filename)
			file_name = filename
			#image_path = f'E:\PROJECT\\aadhar_OCR\{file_name}'

			with io.open(image_path, 'rb') as image_file:
				content = image_file.read()

			image = vision.types.Image(content=content)
			response = client.text_detection(image=image,  image_context={"language_hints": ["en"]})
			texts = response.text_annotations
			df = pd.DataFrame(columns=['locale', 'description'])

			for text in texts:
				df = df.append(
					dict(
				locale=text.locale,
				description=text.description
				),
					ignore_index=True
				)
				
			a = df['description'][0]
			print(a)
			cc = a.split("\n")
			fs = cc[2]
			print(fs)
			if cc[2].startswith('w'):
				print("Hello1")
				b = a.split("Permanent Account Number\n")
			elif fs[:1].isupper()==True and fs[:1]!='P':
				b = a.split("Permanent Account Number\n")
			else:
				b = a.split("Permanent Account Number Card\n")
				ad = b[1].split("\n")
				pan_c = ad[0]
				print(cc)
			
			
			if cc[2].startswith('w'):
				print("Name"+cc[3])
				name_of_person=cc[3]
				print("FathersName"+cc[4])
				father=cc[4]
				print("Pancard"+cc[7])
				pan_c = cc[7]
			elif pan_c.isupper()==True:
				d = a.split("/ Name\n")
				e = d[1].split("\n")
				name_of_person=e[0]
				f = a.split("Father's Name\n")
				g = f[1].split("\n")
				father=g[0]
				
			else:
				print("Name"+cc[3])
				name_of_person=cc[2]
				print("FathersName"+cc[3])
				father=cc[3]
				print("Pancard"+cc[7])
				pan_c = cc[6]
			
			import re
			from datetime import datetime

			match = re.search(r'\d{2}/\d{2}/\d{4}',a)
			date = datetime.strptime(match.group(), '%d/%m/%Y').date()
			print(date)
			session["pan_name"] = name_of_person
			session["father_name"] = father
			session["pancard_number"] = pan_c
			session["date_pan"] = datee
			dataaa = {
			'count':int(0)
			}
			result = FBConn.post('/count_data/', dataaa)
		elif request.form['upload']=="next":
			return redirect(url_for('aadhar')) 
	return render_template('pan.html',a=a,name=name_of_person,father=father,pancard = pan_c,datee=date)

@app.route('/aadhar',methods=["GET","POST"])
def aadhar():
	a=""
	name_of_persons=""
	name=""
	pan_card=""
	datee=""
	dates=""
	gender=""
	ad=""
	date=""
	pan_c=""
	aadhar_number=""
	address=""
	if "pan_name" in session:
		name_of_person = session["pan_name"] 
		father = session["father_name"] 
		pan_c = session["pancard_number"]
		datee = session["date_pan"] 
	if request.method == "POST":
		if request.form['upload']=="Upload":
			upload = request.files['upload']
			filename = secure_filename(upload.filename)
			file_name = filename
			#image_path = f'E:\PROJECT\\aadhar_OCR\{file_name}'

			with io.open(image_path, 'rb') as image_file:
				content = image_file.read()

			image = vision.types.Image(content=content)
			response = client.text_detection(image=image,  image_context={"language_hints": ["en"]})
			texts = response.text_annotations
			df = pd.DataFrame(columns=['locale', 'description'])

			for text in texts:
				df = df.append(
					dict(
				locale=text.locale,
				description=text.description
				),
					ignore_index=True
				)
				
			a = df['description'][0]
			print(a)
			b = a.split("\n")
			print(b)
			name_of_persons = b[1]
			aadhar_number = b[4]
			print(aadhar_number)
			c = b[3].split(" / ")
			gender = c[1]
			import re
			from datetime import datetime

			match = re.search(r'\d{2}/\d{2}/\d{4}',a)
			dates = datetime.strptime(match.group(), '%d/%m/%Y').date()
			print(date)
			uploads = request.files['uploads']
			filenames = secure_filename(uploads.filename)
			file_names = filenames
			#image_path = f'E:\PROJECT\\aadhar_OCR\{file_names}'

			with io.open(image_path, 'rb') as image_file:
				content = image_file.read()

			image = vision.types.Image(content=content)
			response = client.text_detection(image=image,  image_context={"language_hints": ["en"]})
			texts = response.text_annotations
			dff = pd.DataFrame(columns=['locale', 'description'])

			for text in texts:
				dff = dff.append(
					dict(
				locale=text.locale,
				description=text.description
				),
					ignore_index=True
				)
				
			dataa = dff['description'][0]
			print(dataa)
			bc = dataa.split("\n")
			address = bc[2]+bc[3]+bc[4]
			print(address)
			session["aadhar_name"] = name_of_persons
			session["gender"] = gender
			session["adharcard"] = aadhar_number
			session["date_adhar"] = dates
			session["address"] = address
			session["pan_name"] = name_of_person
			session["father_name"] = father
			session["pancard_number"] = pan_c
			session["date_pan"] = datee
		elif request.form['upload']=="next":
			return redirect(url_for('info')) 
	return render_template('aadhar.html',name=name_of_persons,gender=gender,adharcard=aadhar_number,datee=dates,address=address)

@app.route('/info',methods=["GET","POST"])
def info():
	# name_of_persons = ""
	# gender=""
	# aadhar_number=""
	# dates_aadhar=""
	# address=""
	# name_of_person_pan=""
	# father_name=""
	# pan_c=""
	# datee_pan=""
	# if "pan_name" in session:

	# 	name_of_persons = session["aadhar_name"]
	# 	gender = session["gender"]
	# 	aadhar_number = session["adharcard"]
	# 	dates_aadhar = session["date_adhar"]
	# 	datess = dates_aadhar.split("00:00:00 GMT")
	# 	address = session["address"]
	# 	name_of_person_pan = session["pan_name"]
	# 	father_name = session["father_name"]
	# 	pan_c = session["pancard_number"]
	# 	datee_pan = session["date_pan"]
	aadhar_url_back=""
	proof_url=""
	cheque_url=""
	degree_url=""
	db = firebase.database()
	counttt = FBConn.get('/count_data/',None)
	for i,a in counttt.items():
		data_c = int(a['count'])
		da = data_c+1
	datta = {'count':int(da)}
	print(datta)
	print(i)
	db.child('/count_data/').child(i).update(datta)
	uploads = '/home/ubuntu/python-scanner-aws/static/'
	app.config['uploads'] = uploads
	if request.method == "POST":
		if request.form['upload']=="Upload":
			uploaddd = request.files['files']
			foo = Image.open(uploaddd)
			foo = foo.resize((300,300),Image.ANTIALIAS)
			print(foo)
			foo.save('/home/ubuntu/python-scanner-aws/static/'+str(da)+'Aadhar_Front.jpg',optimize=True,quality=95)
			# spl = os.path.basename('E:\PROJECT\\aadhar_OCR\\'+str(da)+'ima.jpg')
			# print(spl)
			# spll = spl.split(".")
			# data_name=str(da)+"Aadhar_Front"+"."+spll[1]
			# filena = secure_filename(data_name)
			# print(filena)

			# uploaddd.save(os.path.join(app.config['uploads'], filena))
			storage.child(str(da)+'Aadhar_Front.jpg').put('/home/ubuntu/python-scanner-aws/static/'+str(da)+'Aadhar_Front.jpg')
			filena = str(da)+'Aadhar_Front.jpg'
			# storage = firebase.storage()
			data_a = filena.split(".")
			files = storage.list_files()
			for file in files:
				word=storage.child(file.name).get_url(None)
				if (word.find(data_a[0]) != -1): 
					data_url = storage.child(file.name).get_url(None)
					aadhar_url_front = data_url

			uploa = request.files['fil']
			foos = Image.open(uploa)
			foos = foos.resize((300,300),Image.ANTIALIAS)
			print(foos)
			foos.save('/home/ubuntu/python-scanner-aws/static/'+str(da)+'Aadhar_Back.jpg',optimize=True,quality=95)
			# spl = os.path.basename('E:\PROJECT\\aadhar_OCR\\'+str(da)+'ima.jpg')
			# print(spl)
			# spll = spl.split(".")
			# data_name=str(da)+"Aadhar_Front"+"."+spll[1]
			# filena = secure_filename(data_name)
			# print(filena)

			# uploaddd.save(os.path.join(app.config['uploads'], filena))
			storage.child(str(da)+'Aadhar_Back.jpg').put('/home/ubuntu/python-scanner-aws/static/'+str(da)+'Aadhar_Back.jpg')
			filena = str(da)+'Aadhar_Back.jpg'
			# storage = firebase.storage()
			data_a = filena.split(".")
			files = storage.list_files()
			for file in files:
				word=storage.child(file.name).get_url(None)
				if (word.find(data_a[0]) != -1): 
					data_url = storage.child(file.name).get_url(None)
					aadhar_url_back = data_url

			uploads = request.files['filess']
			fooss = Image.open(uploads)
			fooss = fooss.resize((300,300),Image.ANTIALIAS)
			print(fooss)
			fooss.save('/home/ubuntu/python-scanner-aws/static/'+str(da)+'Proof.jpg',optimize=True,quality=95)
			# spl = os.path.basename('E:\PROJECT\\aadhar_OCR\\'+str(da)+'ima.jpg')
			# print(spl)
			# spll = spl.split(".")
			# data_name=str(da)+"Aadhar_Front"+"."+spll[1]
			# filena = secure_filename(data_name)
			# print(filena)

			# uploaddd.save(os.path.join(app.config['uploads'], filena))
			storage.child(str(da)+'Proof.jpg').put('/home/ubuntu/python-scanner-aws/static/'+str(da)+'Proof.jpg')
			filena = str(da)+'Proof.jpg'
			# storage = firebase.storage()
			data_a = filena.split(".")
			files = storage.list_files()
			for file in files:
				word=storage.child(file.name).get_url(None)
				if (word.find(data_a[0]) != -1): 
					data_url = storage.child(file.name).get_url(None)
					proof_url = data_url

			uploadss = request.files['uploadsss']
			foosss = Image.open(uploadss)
			foosss = foosss.resize((300,300),Image.ANTIALIAS)
			print(foosss)
			foosss.save('/home/ubuntu/python-scanner-aws/static/'+str(da)+'Cheque.jpg',optimize=True,quality=95)
			# spl = os.path.basename('E:\PROJECT\\aadhar_OCR\\'+str(da)+'ima.jpg')
			# print(spl)
			# spll = spl.split(".")
			# data_name=str(da)+"Aadhar_Front"+"."+spll[1]
			# filena = secure_filename(data_name)
			# print(filena)

			# uploaddd.save(os.path.join(app.config['uploads'], filena))
			storage.child(str(da)+'Cheque.jpg').put('/home/ubuntu/python-scanner-aws/static/'+str(da)+'Cheque.jpg')
			filena = str(da)+'Cheque.jpg'
			# storage = firebase.storage()
			data_a = filena.split(".")
			files = storage.list_files()
			for file in files:
				word=storage.child(file.name).get_url(None)
				if (word.find(data_a[0]) != -1): 
					data_url = storage.child(file.name).get_url(None)
					cheque_url = data_url

			upl = request.files['upl']
			foossss = Image.open(upl)
			foossss = foossss.resize((300,300),Image.ANTIALIAS)
			print(foossss)
			foossss.save('/home/ubuntu/python-scanner-aws/static/'+str(da)+'Degree.jpg',optimize=True,quality=95)
			# spl = os.path.basename('E:\PROJECT\\aadhar_OCR\\'+str(da)+'ima.jpg')
			# print(spl)
			# spll = spl.split(".")
			# data_name=str(da)+"Aadhar_Front"+"."+spll[1]
			# filena = secure_filename(data_name)
			# print(filena)

			# uploaddd.save(os.path.join(app.config['uploads'], filena))
			storage.child(str(da)+'Degree.jpg').put('/home/ubuntu/python-scanner-aws/static/'+str(da)+'Degree.jpg')
			filena = str(da)+'Degree.jpg'
			# storage = firebase.storage()
			data_a = filena.split(".")
			files = storage.list_files()
			for file in files:
				word=storage.child(file.name).get_url(None)
				if (word.find(data_a[0]) != -1): 
					data_url = storage.child(file.name).get_url(None)
					degree_url= data_url

			c_name = request.form['cname']
			s_name = request.form['sname']
			emp_no = request.form['emp']
			talent = request.form['talent']
			join_date = request.form['joining_date']
			full_name_adhar = request.form['full_name']
			dob_adhar = request.form['dob']
			gender = request.form.get('gender')
			martial_status = request.form.get('martial_status')
			marriage_date = request.form['marriage_date']
			passport_no = request.form['passport']
			passport_date = request.form['passport_date']
			pancard_number = request.form['PAN']
			
			aadhar_no = request.form['aadhar']
			
			mobile = request.form['mobile']
			email = request.form['email']
			contact_person = request.form['contact_person']
			contact_person_relation = request.form['contact_person_relation']
			contact_person_no = request.form['contact_person_no']
			father_name = request.form['father_name']
			father_date = request.form['father_date']
			mother_name = request.form['mother_name']
			mother_date = request.form['mother_date']
			address = request.form['address']
			city = request.form['city']
			state = request.form.get('state')
			zips = request.form['zip']
			permanent_address = request.form['permanent_address']
			pcity = request.form['pcity']
			pstate = request.form.get('pstate')
			pzip = request.form['pzip']
			bank_name = request.form['bank_name']
			branch = request.form['branch']
			acc = request.form['acc']
			IFSC = request.form['IFSC']
			OLD_PF = request.form['OLD_PF']
			OLD_ESIC = request.form['OLD_ESIC']
			edu = request.form.get('edu')
			dataa = {
			'Client Name':c_name,
			'Supervisor Name':s_name,
			'Employee No':emp_no,
			'talent':talent,
			'Date of Joinig':join_date,
			'Full name':full_name_adhar,
			'DOB':dob_adhar,
			'Gender':gender,
			'Martial Status':martial_status,
			'Date of marriage':marriage_date,
			'Passport No':passport_no,
			'Passport Expiry':passport_date,
			'PAN No':pancard_number,

			'aadhar_no':aadhar_no,
		
			'Mobile':mobile,
			'Email':email,
			'Contact Person':contact_person,
			'Contact person name':contact_person_no,
			'Contact person relation':contact_person_relation,
			'Father name':father_name,
			'Father DOB':father_date,
			'Mother name':mother_name,
			'Mother DOB':mother_date,
			'Address':address,
			'city':city,
			'state':state,
			'ZIP':zips,
			'Permanent Address':permanent_address,
			'Permanent city':pcity,
			'Permanent state':pstate,
			'Permanent Zip':pzip,
			'Bank Name':bank_name,
			'Bank Branch':branch,
			'Acc No':acc,
			'IFSC no':IFSC,
			'OLD_PF':OLD_PF,
			'OLD_ESIC':OLD_ESIC,
			'Education':edu,
			'adhar_img_front':aadhar_url_front,
			'adhar_img_back':aadhar_url_back,
			'proof_img':proof_url,
			'cheque_img':cheque_url,
			'degree_url':degree_url

			}
			FBConn.post('/data_talentsetu/',dataa)
	return render_template('info.html')
if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=80)
