import streamlit as st
import pandas as pd
import numpy as np
import pickle
import re

st.set_page_config(layout="wide")

# Load the model, encoder, and scaler
with open('model_reg.pkl', 'rb') as f:
    model_reg = pickle.load(f)

with open('encoder_reg.pkl', 'rb') as f:
    encoder = pickle.load(f)

with open('scaler_reg.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('model_clf.pkl', 'rb') as f:
    model_clf = pickle.load(f)

with open('encoder_clf.pkl', 'rb') as f:
    encoder_clf = pickle.load(f)  

# Load sample data for dropdown options
sample_data = pd.read_excel('Copper_Set.xlsx')

# Streamlit app
st.title('Industrial Copper Modeling Application')



# st.write("""
# <div style='text-align:center'>
#     <h1 style='color:#009999;'>Industrial Copper Modeling Application</h1>
# </div>
# """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["PREDICT SELLING PRICE", "PREDICT STATUS"]) 
with tab1:    
        

# Input form
  with st.form('prediction_form'):
    col1,col2,col3=st.columns([5,2,5])
    with col1:
      st.write("Please enter the following details:")
      status = st.selectbox('Status', sample_data['status'].unique(),key=1)
      item_type = st.selectbox('Item type', sample_data['item type'].unique(),key=2)
      country = st.selectbox('Country', sample_data['country'].unique(),key=3)
      application = st.selectbox('Application', sample_data['application'].unique(),key=4)
      product_ref = st.selectbox('Product Reference', sample_data['product_ref'].unique(),key=5)
    with col3:
      quantity_tons = st.number_input('Quantity Tons', min_value=0.1, value=0.1)
      thickness = st.number_input('Thickness', min_value=0.18, value=0.18)
      width = st.number_input('Width', min_value=0.0, value=0.0)
      customer = st.number_input('Customer ID', min_value=0, value=0)
      delivery_duration=st.number_input("enter delivery duration.if no enter 0")
      #material_ref=st.text_input('material reference if have')
      submit_button = st.form_submit_button(label='Predict Selling Price')

      flag=0
      pattern="^(?:\d+|\d*\.\d+)$"
      for i in [quantity_tons,thickness,customer,width]:
         if re.match(pattern, str(i)):
            pass
         else:
            flag=1
            break

# Predict selling price
  if submit_button and flag==1:
          if len(i)==0:
             st.write("Please enter a valid number.No spaces are allowed")
          else:
             st.write("You have entered an invalid value:",i)

  if submit_button and flag == 0:
    input_data = pd.DataFrame({
                'customer': [int(customer)],
                'country': [float(country)],
                'status': [status],
                'item_type': [item_type],
                'application': [float(application)],
                'width': [float(width)],
                'product_ref': [int(product_ref)],
                'delivery_duration': [int(delivery_duration)],
                'thickness_log': [np.log(thickness)],
                'quantity_tons_log': [np.log(quantity_tons)]
            })
            

    input_encoded = encoder.transform(input_data)
    #input_data_encoded = pd.concat([input_data[['customer', 'country']],
                                    #input_encoded,
                                    #input_data[['application', 'width', 'product_ref',
                                     #            'delivery_duration', 'thickness_log', 'quantity_tons_log']]], axis=1)

    input_scaled = scaler.transform(input_encoded)
    predicted_log_price = model_reg.predict(input_scaled)
    predicted_price = np.exp(predicted_log_price)

    st.success(f'Predicted Selling Price: {predicted_price[0]:.2f}')



with tab2:
    
  with st.form('predict_status_form'):
    col1,col2,col3=st.columns([5,1,5])
    with col1:
      st.write("Please enter the following details:")
      item_type = st.selectbox('Item type', sample_data['item type'].unique(),key=22)
      country = st.selectbox('Country', sample_data['country'].unique(),key=23)
      application = st.selectbox('Application', sample_data['application'].unique(),key=24)
      product_ref = st.selectbox('Product Reference', sample_data['product_ref'].unique(),key=25)
      selling_price = st.number_input('selling price.Pleas enter value greater than zero')
    with col3:
      quantity_tons = st.number_input('Quantity Tons', min_value=0.1, value=0.1)
      thickness = st.number_input('Thickness', min_value=0.18, value=0.18)
      width = st.number_input('Width', min_value=0.0, value=0.0)
      customer = st.number_input('Customer ID', min_value=0, value=0)
      delivery_duration=st.number_input("enter delivery duration.if no enter 0")
      submit_button = st.form_submit_button(label='Predict Status')

      cflag=0
      pattern="^(?:\d+|\d*\.\d+)$"
      for k in [quantity_tons,thickness,customer,width]:
         if re.match(pattern,str(k)):
            pass
         else:
            cflag=1
            break

# Predict selling price
  if submit_button and cflag==1:
          if len(i)==0:
             st.write("Please enter a valid number.No spaces are allowed")
          else:
             st.write("You have entered an invalid value:",k)

  if submit_button and flag == 0:
           input_data1 = pd.DataFrame({
               'customer': [int(customer)],
                'country': [float(country)],
                'item_type': [item_type],
                'application': [float(application)],
                'width': [float(width)],
                'product_ref': [int(product_ref)],
                'delivery_duration': [int(delivery_duration)],
                'thickness_log': [np.log(thickness)],
                'quantity_tons_log': [np.log(quantity_tons)],
                'selling_price_log': [np.log(selling_price)]
            })
            # Replace this with the correct column name
        

           input_encoded1 = encoder_clf.transform(input_data1)
           
           #input_data_encoded1 = pd.concat([input_data1[uantity_tons_log','selling_price_log']]], axis=1)

    #input_scaled = scaler.transform(input_data_encoded)
           predicted_status = model_clf.predict(input_encoded1)
           if predicted_status==1:
              st.write('## :green[The status is WON]')
           else:
              st.write("## :red[The status is LOST]")
   


            

#st.write("App created by Your Name")
