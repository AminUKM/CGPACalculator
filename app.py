from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# UKM Grade to Point Mapping
grade_to_point = {
    "A": 4.00, "A-": 3.67, "B+": 3.33, "B": 3.00, "B-": 2.67,
    "C+": 2.33, "C": 2.00, "C-": 1.67, "D+": 1.33, "D": 1.00, "E": 0.00
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    last_cgpa = float(data['lastCgpa'])
    subjects = data['subjects']

    total_points = 0
    total_credits = 0
    results = []

    for sub in subjects:
        name = sub['name']
        credit = float(sub['credit'])
        grade = sub['grade']
        point = grade_to_point.get(grade, 0.0)

        total_points += point * credit
        total_credits += credit
        results.append({
            'name': name,
            'credit': credit,
            'grade': grade,
            'point': round(point, 2)
        })

    semester_gpa = total_points / total_credits if total_credits else 0
    new_cgpa = (last_cgpa + semester_gpa) / 2

    return jsonify({
        'subjects': results,
        'semesterGpa': round(semester_gpa, 2),
        'lastCgpa': round(last_cgpa, 2),
        'newCgpa': round(new_cgpa, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
