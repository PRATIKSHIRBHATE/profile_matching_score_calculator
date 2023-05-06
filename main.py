import logging
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from google.cloud import storage

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate_score',methods=['POST'])
def calculate_score():
    '''
    For rendering results on HTML GUI
    '''
    request_json = {}
    request_value_list = [x for x in request.form.values()]
    request_json["name"] = request_value_list[0]
    request_json["dob"] = request_value_list[1]
    request_json["height_cm"] = float(request_value_list[2])
    request_json["weight_kg"] = float(request_value_list[3])
    request_json["hobby"] = request_value_list[4]
    request_json["education"] = request_value_list[5]
    request_json["iit_nit"] = request_value_list[6]
    request_json["post_graduation"] = request_value_list[7]
    request_json["grad_year"] = int(request_value_list[8])
    request_json["postgrad_year"] = int(request_value_list[9])
    request_json["ssc_percentage"] = float(request_value_list[10])
    request_json["hsc_percentage"] = float(request_value_list[11])
    request_json["avg_degree_percentage"] = float(request_value_list[12])
    request_json["avg_post_grad_percentage"] = float(request_value_list[13])
    request_json["occupation"] = request_value_list[14]
    request_json["experience"] = float(request_value_list[15])
    request_json["monthly_salary"] = float(request_value_list[16])
    request_json["work_from_home"] = request_value_list[17]
    request_json["willing_to_contribute_equally_to_household_expense"] = request_value_list[18]
    request_json["father_occupation"] = request_value_list[19]
    request_json["mother_occupation"] = request_value_list[20]
    request_json["relocate_to_yavatmal"] = request_value_list[21]
    request_json["willing_to_live_with_inlaws"] = request_value_list[22]
    request_json["non_vegiterian"] = request_value_list[23]
    request_json["sleep_time"] = float(request_value_list[24])
    request_json["wake_uptime"] = float(request_value_list[25])
    request_json["exp1"] = request_value_list[26]
    request_json["exp2"] = request_value_list[27]
    request_json["exp3"] = request_value_list[28]
    request_json["exp4"] = request_value_list[29]
    request_json["exp5"] = request_value_list[30]

    #request_json = json.dumps(request_json)
    #logging.info(request_json)

    name = request_json.get("name", "Random")
    dob = request_json.get("dob", "yyyy-mm-dd")
    
    #Calculate Age Based on Date of Birth
    dob = datetime.strptime(dob, "%Y-%m-%d")
    birth_year = int(dob.year)
    current_date = datetime.now()
    current_year = int(current_date.year)
    age = (current_date - dob).days/365.25
    request_json["age"] = int(round(age))

    height_cm = request_json.get("height_cm", 150)
    weight_kg = request_json.get("weight_kg", 75)
    bmi = weight_kg/(height_cm/100)**2
    hobby = request_json.get("hobby", "None")
    education = request_json.get("education", "msc")
    iit_nit = request_json.get("iit_nit", "No")
    post_graduation = request_json.get("post_graduation", "No")
    ssc_percentage = request_json.get("ssc_percentage", 0)
    hsc_percentage = request_json.get("hsc_percentage", 0)
    avg_degree_percentage = request_json.get("avg_degree_percentage", 0)
    avg_post_grad_percentage = request_json.get("avg_post_grad_percentage", 0)

    grad_year = request_json.get("grad_year", 9999)
    postgrad_year = request_json.get("postgrad_year", 9999)

    occupation = request_json.get("occupation", "None")
    experience = request_json.get("experience", 0)
    monthly_salary = request_json.get("monthly_salary", 0)
    work_from_home = request_json.get("work_from_home", "No")
    willing_to_contribute_equally_to_household_expense = request_json.get("willing_to_contribute_equally_to_household_expense", "No")
    father_occupation = request_json.get("father_occupation", "None")
    mother_occupation = request_json.get("mother_occupation", "None")
    relocate_to_yavatmal = request_json.get("relocate_to_yavatmal", "No")
    willing_to_live_with_inlaws = request_json.get("willing_to_live_with_inlaws", "No")
    non_vegiterian = request_json.get("non_vegiterian", "No")
    sleep_time = request_json.get("sleep_time", 12)
    wake_uptime = request_json.get("wake_uptime", 9)

    """
    with open('data.json', 'w') as outfile:
        # Write the data to the file in JSON format
        json.dump(request_json, outfile)
    """

    age_difference = 32 - int(age)
    total_score = 0
    
    if age_difference>=0 and age_difference < 5:
        total_score += 10

    if bmi > 18 and bmi<25:
        total_score += 5
    if height_cm > 160 and height_cm<180:
        total_score += 5
    if weight_kg > 50 and weight_kg <70:
        total_score += 5

    if hobby.lower() in ["reading", "playing chess", "cooking", "chess", "badminton", "swimming", "painting"]:
        total_score +=10
    elif hobby.lower() in ["watching tv", "social media", "netflix"]:
        total_score -=10

    if education.lower() in ["engineering", "be", "b.e", "m.tech", "mtech", "me", "m.e"]:
        total_score += 5

    if iit_nit.lower() in ["yes", "iit", "nit"] :
        total_score += 20
    if post_graduation.lower() in ["yes"] :
        total_score += 5
        
    if ssc_percentage >= 80:
        total_score += 5
    if hsc_percentage >= 80:
        total_score += 5
    if avg_degree_percentage >= 80:
        total_score += 10
    if avg_post_grad_percentage >= 80:
        total_score += 5
        
    # Penalize if there is gap in eduction until graduation
    if grad_year - birth_year > 22:
        total_score -= 10

    if occupation.lower() in ["it", "software", "job", "engineer", "data scientist", "software engineer"] :
        total_score += 5

    ideal_work_experience = current_year - grad_year - 2 # 2 for postgradution
    if experience > ideal_work_experience:
        total_score += 5

    if monthly_salary > 50000:
        total_score += 5

    if work_from_home.lower() == 'yes':
        total_score += 15

    if willing_to_contribute_equally_to_household_expense.lower() == 'yes':
        total_score += 10

    if relocate_to_yavatmal.lower() == 'yes':
        total_score += 15

    if willing_to_live_with_inlaws.lower() == 'yes':
        total_score += 20

    if father_occupation.lower() in ["teacher", "professor", "retired teacher"]:
        total_score += 5

    if mother_occupation.lower() in ["teacher", "professor", "retired teacher"]:
        total_score += 5

    if non_vegiterian.lower() == "yes":
        total_score += 5

    if sleep_time > 11 and sleep_time < 6:
        total_score -= 10
    if wake_uptime > 7:
        total_score -= 10

    percentage_score = round(100*total_score/180)
    # Perform some processing
    greeting = "Hello, " + name + "! " + "Your profile matching score is " + str(percentage_score)
    
    # Return the response to the user
    response = {}
    response["greeting"] = greeting
    request_json["total_score"] = total_score
    request_json["percentage_score"] = percentage_score
    # logging.info(response)
    
    # Write the request-response to GCS
    # Create a client for interacting with Cloud Storage
    
    client = storage.Client()

    # Select the bucket where you want to store the file
    bucket = client.bucket('profile-matching-calculator-inputs')

    # Create a new Blob object
    filename = name + "_" + str(current_date.strftime("%Y-%m-%d-%H-%M"))
    blob = bucket.blob(f'input_jsons/{filename}.json')

    # Convert the dictionary to a JSON object
    json_object = json.dumps(request_json)

    # Write the JSON object to the Blob
    blob.upload_from_string(json_object)

    return render_template('index.html', prediction_text='Greetings {}! your profile matching score is {} %'.format(name, percentage_score))


if __name__ == "__main__":
    app.run(debug=True)
