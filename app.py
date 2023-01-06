from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random
import string

app = Flask(__name__)

@app.route('/')
def index():
    df_records = pd.read_excel('database.xlsx')
    df_records = df_records.fillna('')
    return render_template('index.html',row_data=list(df_records.values.tolist()))

@app.route('/record',methods=['POST'])
def record():
    if request.method == 'POST':
        climateParameter = request.form['climateParameter']
        riskTrigger = request.form['riskTrigger']
        templateChoice = request.form['templateChoice']
        
        valueParameter = request.form['valueParameter']
        unitValue = request.form['unitValue']
        
        thres1 = request.form['thres1']
        thres2 = request.form['thres2']
        thres3 = request.form['thres3']
        thres4 = request.form['thres4']

        unitThreshold = request.form['unitThreshold']

        countryTags = request.form.getlist('countryTags')
        countryTags = ','.join(countryTags)

        appTags = request.form.getlist('appTags')
        appTags = ','.join(appTags)

        descriptionText = request.form['descriptionText']
        urlMore = request.form['urlMore']

        id_str1 = str(riskTrigger.split(' ')[0][0])+''+str(riskTrigger.split(' ')[1][0])
        id_str2 = str(templateChoice.split(' ')[0][0])+''+str(templateChoice.split(' ')[1][0])+''+str(templateChoice.split(' ')[2][0])
        idRandom = ''.join(random.choice(string.printable) for i in range(8))
        idRandom = id_str1+'-'+id_str2+'-'+idRandom

        df_records = pd.read_excel('database.xlsx')
        df_new_record = pd.DataFrame([[idRandom,riskTrigger,templateChoice,
                    valueParameter,unitValue,
                    thres1,thres2,thres3,thres4,unitThreshold,
                    climateParameter,appTags,countryTags,descriptionText,urlMore]])
        df_new_record.columns = df_records.columns
        
        df_combined_records = df_records.append(df_new_record)

        df_combined_records.to_excel('database.xlsx',index=False)
        return redirect(url_for('index'))

@app.route('/record', methods=['GET'])
def recordroute():
    return render_template('record.html',button_text='Update Risk Threshold Database', form_type='main_route')

@app.route('/editrecord', methods=['POST'])
def editrecord():
    selected_option = (request.form['optionTags'])

    recordID = request.form['recordID']
    df_records = pd.read_excel('database.xlsx')

    if selected_option=='deleteRecord':
        button_text = 'I am sure! Delete this record?'
        return render_template('record.html', button_text = button_text, form_type='delete')

    else:
        button_text = 'Are you sure you want to update this record?'
        return render_template('record.html', button_text = button_text, form_type='edit')


#if __name__ == "__main__":
#    app.run(debug=True)




