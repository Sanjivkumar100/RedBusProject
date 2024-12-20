import streamlit as st
import pandas as pd
import pymysql

st.title("Redbus Bus Booking")

st.subheader("About us")
st.markdown(
    """
    This application allows you to book buses and get information about bus services. The application is built using Streamlit and MySQL.
    In this application, you can select a bus service and filter the data based on various criteria like price, bus type, and more.
    """
)
st.image(r'C:\Users\sanji\Desktop\RedBusProject\Redbusimage\Ad1.png')

def create_connection():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="redbus"
        )
        
        return connection
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

connection = create_connection()

if connection:
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES;")
    data = cursor.fetchall()
    tablenames = [table[0] for table in data] 
    selectedtable = st.selectbox("Bus Service", tablenames)

    
    try:
        
        if selectedtable:
                query = f"SELECT * FROM `{selectedtable}`;"
                cursor.execute(query)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                with st.form(key='Filter Form'):
               
                    cursor.execute(f"SELECT DISTINCT `From` FROM {selectedtable};")
                    data = cursor.fetchall()
                    fromlist=[f[0] for f in data]
                    From=st.selectbox("From",fromlist)
                
                    cursor.execute(f"SELECT DISTINCT `To` FROM {selectedtable};")
                    data = cursor.fetchall()
                    To=tolist=[t[0] for t in data]
                    To=st.selectbox("To",tolist)
                
                    cursor.execute(f"SELECT DISTINCT `Bus_Type` FROM {selectedtable};")
                    data = cursor.fetchall()
                    bustypelist=[bt[0] for bt in data]
                    Bus_type=st.selectbox("Bus Type",bustypelist)
                    
                    minPrice,maxPrice=st.slider("Price Range",min_value=0,max_value=3000,value=(0,3000))
                    submit=st.form_submit_button("Filter")
                    if submit:
                        filter_query = f"""
                            SELECT * FROM `{selectedtable}`
                            WHERE `From` = '{From}' AND `To` = '{To}'
                            AND `Bus_Type` = '{Bus_type}' AND Price BETWEEN {minPrice} AND {maxPrice};
                            """
                        cursor.execute(filter_query)
                        filtered_data = cursor.fetchall()
                        filtered_df = pd.DataFrame(filtered_data, columns=columns)
                    
                        
                        if 'Link' in filtered_df.columns:
                            filtered_df['Link'] = filtered_df['Link'].apply(lambda x: f'<a href="{x}" target="_blank">View Details</a>')
                            
                            st.markdown( f"""
                    <div style="height: 300px; overflow-y: scroll; border: 1px solid #ddd;">
                        {filtered_df.to_html(escape=False, index=False)}
                    </div>
                    """,
                    unsafe_allow_html=True
                    )
                        else:
                            st.dataframe(filtered_df)      
                    
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
    finally:
        connection.close()
else:
    st.error("Database connection failed")
st.image(r'C:\Users\sanji\Desktop\RedBusProject\Redbusimage\Ad2.png',width=800)           
        