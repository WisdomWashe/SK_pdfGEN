# from flask import Flask, render_template, request, send_file
# import fitz
# import io

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/rechnung')
# def dashboard():
#     return render_template('rechnung.html')

# @app.route("/Leistungsvereinbarung")
# def Leistungsvereinbarung():
#     return render_template("Leistungsvereinbarung.html")


# # @app.route('/submit', methods=['POST'])
# # def submit():
# #     name = request.form.get('name')
# #     address = request.form.get('address')
# #     house_number = request.form.get('house_number')
# #     country = request.form.get('country')
# #     date = request.form.get('date')
# #     invoice_number = request.form.get('invoice_number')
# #     safari_number = request.form.get('safari_number')
# #     description = request.form.get('description')
# #     duration_date = request.form.get('duration_date')
# #     pickup = request.form.get('pickup')
# #     people = request.form.get('people')
# #     overnights = request.form.get('overnights')
# #     inclusive = request.form.get('inclusive')
# #     totalprice_deposit = request.form.get('totalprice_deposit')
    
# #     return render_template('login.html')


# @app.route('/submit', methods=['POST'])
# def submit():
#     template_used = request.form.get("template")
#     print("Submitted from:", template_used)
#     ...





# @app.route('/fill', methods=['POST'])
# def fill_pdf():
#     form_data = request.form.to_dict()  # Get all form values as a dict

#     # Load your PDF
#     doc = fitz.open(template_used)
#     page = doc[0]

#     # Fill fields based on form keys
#     for widget in page.widgets():
#         field_name = widget.field_name
#         if field_name in form_data:
#             widget.field_value = form_data[field_name]
#             widget.field_fontsize = 10
#             widget.update()

#     # Save to memory (or file)
#     output = io.BytesIO()
#     doc.save(output)
#     doc.close()
#     output.seek(0)

#     return send_file(output, as_attachment=True, download_name="filled_invoice.pdf")




# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, send_file, session
import fitz
import io

app = Flask(__name__)
app.secret_key = 'super-secret-key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rechnung')
def dashboard():
    return render_template('rechnung.html')

@app.route("/Leistungsvereinbarung")
def Leistungsvereinbarung():
    return render_template("Leistungsvereinbarung.html")

@app.route('/submit', methods=['POST'])
def submit():
    # Optionally store the template
    template_used = request.form.get("template")
    session['template_used'] = template_used
    print("Logged submission from:", template_used)
    return '', 204  # No Content

@app.route('/fill', methods=['POST'])
def fill_pdf():
    form_data = request.form.to_dict()
    template_used = form_data.get('template')

    if not template_used:
        return "Missing template", 400

    doc = fitz.open(template_used)
    page = doc[0]

    for widget in page.widgets():
        field_name = widget.field_name
        if field_name in form_data:
            widget.field_value = form_data[field_name]
            widget.field_fontsize = 10
            widget.update()

    output = io.BytesIO()
    doc.save(output)
    doc.close()
    output.seek(0)

    return send_file(output, as_attachment=True, download_name="filled_invoice.pdf")

if __name__ == '__main__':
    app.run(debug=True)
