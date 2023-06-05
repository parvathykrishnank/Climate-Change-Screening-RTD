from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random
import string
from datetime import date
from sqlalchemy import create_engine


app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('rtd-homepage.html')

@app.route('/index')
def index():

    engine = create_engine('postgresql://postgres:getdatabasemirra@128.199.226.170:5432/gpbprtd')
    df_records = pd.read_sql('threshold_db_new',engine)
    
    df_records = df_records.dropna(how='all')
    df_records = df_records[df_records['id'].astype(str)!='nan']
    df_records = df_records.fillna('')

    df_records['color_array'] = df_records[['t1','t2','t3','t4']].to_numpy().tolist()
    df_records['color_array'] = df_records['color_array'].apply(lambda color_ar:[x for x in color_ar if x != ''])   
    
    def get_color_list(color_array):
        if(len(color_array)==3):
            color_list = ['#ffe380','#ff8b00','#de0b16','white']

        if(len(color_array)==4):
            color_list = ['#ffe380','#ffc400','#ff8b00','#de0b16']

        if(len(color_array)==2):
            color_list = ['#ffe380','#de0b16','white','white']

        return(color_list)

    df_records['color_list'] = df_records['color_array'].apply(get_color_list)

    df_records['C1'] = df_records['color_list'].apply(lambda x:x[0])
    df_records['C2'] = df_records['color_list'].apply(lambda x:x[1])
    df_records['C3'] = df_records['color_list'].apply(lambda x:x[2])
    df_records['C4'] = df_records['color_list'].apply(lambda x:x[3])

    return render_template('index.html',row_data=list(df_records.values.tolist()))

@app.route('/references')
def references():
    df_records = pd.read_excel('references.xlsx').astype(str)
    df_records = df_records.dropna(how='all')
    df_records = df_records.fillna('')
    df_records = df_records.sort_values(by='Publication Year')
    return render_template('references.html',row_data=list(df_records.values), col_names=list(df_records.columns), 
        length_cols = len(list(df_records.columns))-1, length_records = len(list(df_records.columns)))

@app.route('/datastories')
def datastories():
    return render_template('data-stories.html')

@app.route('/record',methods=['POST'])
def record():
    if request.method == 'POST':
        climateParameter = request.form['climateParameter']
        riskTrigger = request.form['riskTrigger']
        templateChoice = request.form['templateChoice']
        levelDisruption = request.form['levelDisruption']

        def get_float_param(param):
            if(param!=''):
                param = float(param)
            else:
                param = None
            return param

        valueParameter = request.form['valueParameter']
        valueParameter = get_float_param(valueParameter)

        unitValue = request.form['unitValue']
        
        thres1 = request.form['thres1']
        thres1 = get_float_param(thres1)
        thres2 = request.form['thres2']
        thres2 = get_float_param(thres2)
        thres3 = request.form['thres3']
        thres3 = get_float_param(thres3)
        thres4 = request.form['thres4']
        thres4 = get_float_param(thres4)

        unitThreshold = request.form['unitThreshold']

        countryTags = request.form.getlist('countryTags')
        countryTags = ','.join(countryTags)

        appTags = request.form.getlist('appTags')
        appTags = ','.join(appTags)

        assetTags1 = request.form.getlist('assetTags1')
        assetTags1 = ','.join(assetTags1)

        assetTags2 = request.form.getlist('assetTags2')
        assetTags2 = ','.join(assetTags2)

        descriptionText = request.form['descriptionText']
        urlMore = request.form['urlMore']

        shortDescription = request.form['shortDescription']

        id_str1 = str(riskTrigger.split(' ')[0][0])+''+str(riskTrigger.split(' ')[1][0])
        id_str2 = str(templateChoice.split(' ')[0][0])+''+str(templateChoice.split(' ')[1][0])+''+str(templateChoice.split(' ')[2][0])
        
        idRandom = ''.join(random.choice(string.printable) for i in range(8))
        idRandom = id_str1+'-'+id_str2+'-'+idRandom

        todayDate = date.today()

        engine = create_engine('postgresql://postgres:getdatabasemirra@128.199.226.170:5432/gpbprtd')
        df_records = pd.read_sql('threshold_db_new',engine)

        df_new_record = pd.DataFrame([[idRandom,riskTrigger,templateChoice,
                    valueParameter,unitValue,
                    thres1,thres2,thres3,thres4,unitThreshold,
                    climateParameter,appTags,countryTags,descriptionText,urlMore,
                    shortDescription,levelDisruption,assetTags1,assetTags2,todayDate]])
        
        df_new_record.columns = df_records.columns
        df_new_record.to_sql('threshold_db_new', con=engine, if_exists='append', index=False)
        return redirect(url_for('index'))

@app.route('/record', methods=['GET'])
def recordroute():
    df_records = pd.read_excel('nace_code_list.xlsx')
    df_records_asset = pd.read_excel('asset_tags_list.xlsx')
    df_records_asset1 = pd.read_excel('asset_tags_list1.xlsx')

    return render_template('record.html',
        button_text='Update Risk Threshold Database', form_type='main_route',
        row_data=list(df_records.values.tolist()), 
        row_data_assets=list(df_records_asset.values.tolist()),
        row_data_assets1=list(df_records_asset1.values.tolist()))

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

@app.route('/release-notes')
def release_notes():
    return render_template('release-notes.html')

if __name__ == "__main__":
   app.run(debug=True,port=8080)




