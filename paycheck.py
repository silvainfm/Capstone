#paycheck.py
from flask import Flask, render_template, request, Response
import pdfkit

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    name = request.form['name']
    hours_worked = float(request.form['hours_worked'])
    hourly_rate = float(request.form['hourly_rate'])

    gross_pay = hours_worked * hourly_rate
    taxes = gross_pay * 0.2
    net_pay = gross_pay - taxes

    return render_template('result.html', name=name, gross_pay=gross_pay, taxes=taxes, net_pay=net_pay)

if __name__ == '__main__':
    app.run(debug=True)


# index.html
'''
<!DOCTYPE html>
<html>
<head>
    <title>Paycheck Calculator</title>
</head>
<body>
    <h1>Paycheck Calculator</h1>
    <form action="/calculate" method="post">
        <label for="name">Name:</label>
        <input type="text" name="name"><br>
        <label for="hours_worked">Hours worked:</label>
        <input type="number" name="hours_worked"><br>
        <label for="hourly_rate">Hourly rate:</label>
        <input type="number" name="hourly_rate"><br>
        <input type="submit" value="Calculate">
    </form>
</body>
</html> '''

# result.html
'''
<!DOCTYPE html>
<html>
<head>
    <title>Paycheck Calculator Results</title>
</head>
<body>
    <h1>Paycheck Calculator Results</h1>
    <p>Name: {{ name }}</p>
    <p>Gross pay: ${{ gross_pay }}</p>
    <p>Taxes: ${{ taxes }}</p>
    <p>Net pay: ${{ net_pay }}</p>
</body>
</html>'''

import pdfkit
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <h1>Paycheck Calculator</h1>
        <form action="/calculate" method="post">
            <label for="name">Name:</label>
            <input type="text" name="name"><br>
            <label for="hours_worked">Hours worked:</label>
            <input type="number" name="hours_worked"><br>
            <label for="hourly_rate">Hourly rate:</label>
            <input type="number" name="hourly_rate"><br>
            <input type="submit" value="Calculate">
        </form>
    '''

# for pdf output 
@app.route('/calculate', methods=['POST'])
def calculate():
    name = request.form['name']
    hours_worked = float(request.form['hours_worked'])
    hourly_rate = float(request.form['hourly_rate'])

    gross_pay = hours_worked * hourly_rate
    taxes = gross_pay * 0.2
    net_pay = gross_pay - taxes

    html = f'''
        <h1>Paycheck Summary for {name}</h1>
        <p>Gross pay: ${gross_pay:.2f}</p>
        <p>Taxes: ${taxes:.2f}</p>
        <p>Net pay: ${net_pay:.2f}</p>
    '''

    # Generate PDF using pdfkit
    pdf = pdfkit.from_string(html, False)

    # Create response with PDF content-type
    response = Response(pdf, content_type='application/pdf')
    response.headers['Content-Disposition'] = 'attachment; filename=paycheck.pdf'
    
    return response

if __name__ == '__main__':
    app.run(debug=True)

# pdf output css 
'''
<style>
    body {
        font-family: Arial, sans-serif;
        font-size: 14px;
    }
    .header {
        text-align: center;
        margin-bottom: 30px;
    }
    .header h1 {
        margin: 0;
        font-size: 24px;
    }
    .header p {
        margin: 0;
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #000;
        padding: 10px;
        text-align: left;
    }
    th {
        font-weight: bold;
    }
</style>
'''

# pdf output html

html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Paycheck Summary</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 14px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .header p {{
            margin: 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid #000;
            padding: 10px;
            text-align: left;
        }}
        th {{
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Paycheck Summary</h1>
        <p>{name}</p>
    </div>
    <table>
        <tr>
            <th>Description</th>
            <th>Amount</th>
        </tr>
        <tr>
            <td>Gross Pay</td>
            <td>${gross_pay:.2f}</td>
        </tr>
        <tr>
            <td>Taxes</td>
            <td>${taxes:.2f}</td>
        </tr>
        <tr>
            <td>Net Pay</td>
            <td>${net_pay:.2f}</td>
        </tr>
    </table>
</body>
</html>
'''


## new adjusted code
from flask import Flask, render_template, request, Response
import pdfkit

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# for pdf output
@app.route('/calculate', methods=['POST'])
def calculate():
    name = request.form['name']
    hours_worked = float(request.form['hours_worked'])
    hourly_rate = float(request.form['hourly_rate'])

    gross_pay = hours_worked * hourly_rate
    taxes = gross_pay * 0.2
    net_pay = gross_pay - taxes

    html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Paycheck Summary</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 14px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .header p {{
            margin: 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid #000;
            padding: 10px;
            text-align: left;
        }}
        th {{
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Paycheck Summary</h1>
        <p>{name}</p>
    </div>
    <table>
        <tr>
            <th>Description</th>
            <th>Amount</th>
        </tr>
        <tr>
            <td>Gross Pay</td>
            <td>${gross_pay:.2f}</td>
        </tr>
        <tr>
            <td>Taxes</td>
            <td>${taxes:.2f}</td>
        </tr>
        <tr>
            <td>Net Pay</td>
            <td>${net_pay:.2f}</td>
        </tr>
    </table>
</body>
</html>
'''

    # Generate PDF using pdfkit
    pdf = pdfkit.from_string(html, False)

    # Create response with PDF content-type
    response = Response(pdf, content_type='application/pdf')
    response.headers['Content-Disposition'] = 'attachment; filename=paycheck.pdf'

    return response

if __name__ == '__main__':
    app.run(debug=True)

