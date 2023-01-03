import logging
import json
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate_score',methods=['POST'])
def calculate_score():
    '''
    For rendering results on HTML GUI
    '''
    print(request)

    request_json = {}
    request_value_list = [x for x in request.form.values()]
    request_json["name"] = request_value_list[0]
    request_json["age"] = float(request_value_list[1])
    request_json["height_cm"] = float(request_value_list[2])
    request_json["weight_kg"] = float(request_value_list[3])
    request_json["education"] = request_value_list[4]
    request_json["iit_nit"] = request_value_list[5]
    request_json["post_graduation"] = request_value_list[6]
    request_json["avg_degree_percentage"] = float(request_value_list[7])
    request_json["occupation"] = request_value_list[8]
    request_json["monthly_salary"] = float(request_value_list[9])
    request_json["work_from_home"] = request_value_list[10]
    request_json["willing_to_contribute_equally_to_household_expense"] = request_value_list[11]
    request_json["father_occupation"] = request_value_list[12]
    request_json["mother_occupation"] = request_value_list[13]
    request_json["relocate_to_yavatmal"] = request_value_list[14]
    request_json["willing_to_live_with_inlaws"] = request_value_list[15]

    #request_json = json.dumps(request_json)
    print(request_value_list)
    logging.info(request_json)

    name = request_json.get("name", "Random")
    age = request_json.get("age", 35)
    height_cm = request_json.get("height_cm", 150)
    weight_kg = request_json.get("weight_kg", 75)
    bmi = weight_kg/(height_cm/100)**2
    education = request_json.get("education", "msc")
    iit_nit = request_json.get("iit_nit", "No")
    post_graduation = request_json.get("post_graduation", "No")
    avg_degree_percentage = request_json.get("avg_degree_percentage", 0)
    occupation = request_json.get("occupation", "None")
    monthly_salary = request_json.get("monthly_salary", 0)
    work_from_home = request_json.get("work_from_home", "No")
    willing_to_contribute_equally_to_household_expense = request_json.get("willing_to_contribute_equally_to_household_expense", "No")
    father_occupation = request_json.get("father_occupation", "None")
    mother_occupation = request_json.get("mother_occupation", "None")
    relocate_to_yavatmal = request_json.get("relocate_to_yavatmal", "No")
    willing_to_live_with_inlaws = request_json.get("willing_to_live_with_inlaws", "No")


    age_difference = 32 - int(age)
    total_score = 0
    
    if age_difference>0 and age_difference < 5:
        total_score += 10

    if bmi > 18 and bmi<25:
        total_score += 5
    if height_cm > 160 and height_cm<180:
        total_score += 5
    if weight_kg > 55 and weight_kg <65:
        total_score += 5

    if education.lower() in ["engineering", "be", "b.e", "m.tech", "mtech", "me", "m.e"]:
        total_score += 5

    if iit_nit.lower() in ["yes", "iit", "nit"] :
        total_score += 20
    if post_graduation.lower() in ["yes"] :
        total_score += 5
        
    if avg_degree_percentage > 80:
        total_score += 10
        
    if occupation.lower() in ["it", "software", "job"] :
        total_score += 5

    if monthly_salary > 50000:
        total_score += 5

    if work_from_home.lower() == 'yes':
        total_score += 5

    if willing_to_contribute_equally_to_household_expense.lower() == 'yes':
        total_score += 10

    if relocate_to_yavatmal.lower() == 'yes':
        total_score += 15

    if willing_to_live_with_inlaws.lower() == 'yes':
        total_score += 20

    if father_occupation.lower() == "teacher":
        total_score += 5

    if mother_occupation.lower() == "teacher":
        total_score += 5


    # Perform some processing
    greeting = "Hello, " + name + "! " + "Your profile matching score is " + str(total_score)
    
    # Return the response to the user
    response = {}
    response["greeting"] = greeting
    logging.info(response)

    return render_template('index.html', prediction_text='Greetings {}! your profile matching score is {}'.format(name, total_score))


if __name__ == "__main__":
    app.run(debug=True)
