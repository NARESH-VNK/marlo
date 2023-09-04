import psycopg2 as psycopg2
import streamlit as st
from sqlalchemy import create_engine
import pandas as pd




# Run the Streamlit app
if __name__ == "__main__":
    st.title("E-commerce Dashboard")


options = st.sidebar.selectbox('Menu',["Admin","User"])

conn = psycopg2.connect(
    host = 'localhost',
    user = "postgres",
    password ="naresh",
    port = 5432,
    database = "marlo"
)
nk = conn.cursor()

conn.autocommit = False

engine = create_engine('postgresql+psycopg2://postgres:naresh@localhost/marlo')



if options  == "User":
    st.title("New User !!!!")
    with st.expander("Registration"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        username = st.text_input("Enter your Username")
        password = st.text_input("Enter your Password", type="password")

        if st.button("Register"):
            nk.execute("insert into registration values (\'{a}\',\'{b}\',\'{c}\',\'{d}\')".format(a=first_name, b=last_name,
                                                                                                  c=username, d=password))
            conn.commit()
            st.success(f"User {first_name} {last_name} registered successfully!")



    # Set a title for the app
    st.title("Login")
    with st.form("Login Details "):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        query = ("select  * from registration")
        nk.execute(query)
        x = nk.fetchall()
        fetch = pd.DataFrame(x, columns=['Fn', 'Ln', 'Un', 'Ps'])


        submit = st.form_submit_button("Submit Login Details")

    if submit:

        if (fetch['Un'] == username).any():
            index = fetch[fetch['Un'] == username].index[0]

            if (fetch['Ps'][index] == password):
                st.write("login sucessfully")

                query = ("select  * from product")
                nk.execute(query)
                x1 = nk.fetchall()
                fetch1 = pd.DataFrame(x1, columns=['Name','Barcode','Brand','Description','Price','Available'])
                st.dataframe(fetch1)


            else:
                st.write("Incorrect Password")
        else:
            st.write("Username not found")


    st.title("Update Review and Ratings")


    agree = st.checkbox('Update')

    if agree:
        query1 = (f"SELECT column_name FROM information_schema.columns WHERE table_name = 'product'")
        nk.execute(query1)
        column_tuples = nk.fetchall()
        column_names = [column_tuple[0] for column_tuple in column_tuples]



        if 'ratings' and 'reviews' not in column_names:


            alter_table_query = f"""
                        ALTER TABLE product
                        ADD COLUMN RATINGS INT DEFAULT 0,
                        ADD COLUMN REVIEWS TEXT DEFAULT '';
                        """

            nk.execute(alter_table_query)
            conn.commit()


        else:
            st.write("Already Updated")



        st.title ("Enter your Ratings And Reviews")
        q2 = "select * from product"
        nk.execute(q2)
        x = nk.fetchall()
        # st.write(x)
        df = pd.DataFrame(x, columns=['Name', 'Barcode', 'Brand', 'Description', 'Price', 'Available','Ratings','Reviews'])
        df1 = df.copy()
        st.dataframe(df)


        product_name_input = st.text_input("Enter your  Product Name")
        review = st.text_input("Comment your Review")
        rating = st.number_input('Enter your rating')

        cleaned_product_list = [product.replace('\xa0', '').strip() for product in df1['Name'].values]
        if str(product_name_input) in cleaned_product_list:
            ind = cleaned_product_list.index(product_name_input)
            df1.loc[ind, 'Ratings'] = rating
            df1.loc[ind, 'Reviews'] = review


        sub = st.button("Click To Update in Database")


        if sub:
            st.write(df1)
            df1.to_sql('productupdate', engine, if_exists='append', index=False)

            st.write("Updated sucessfully in Database!!!")

            q2 = "select DISTINCT * from productupdate"
            nk.execute(q2)
            xa = nk.fetchall()
            fetch1 = pd.DataFrame(xa, columns=['Name', 'Barcode', 'Brand', 'Description', 'Price', 'Available', 'Ratings','Reviews'])
            st.dataframe(fetch1)





if options == "Admin":



    with st.form("Enter the Input Features"):
        admin_username = st.text_input("Username")
        admin_password = st.text_input("Password", type="password")

        if admin_username == "marlo":
            if admin_password == "marlo123":
                st.write("Admin Login sucessfully")

                uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

                if uploaded_file is not None:
                    df = pd.read_csv(uploaded_file)
                    st.dataframe(df)
                    df.to_sql('product', engine, if_exists='replace', index=False)

                    st.success("CSV file uploaded and processed successfully!")

            else:
                st.write("Incorrect Password")
        else:
            st.write("Admin username is incorrect found")


        submitted = st.form_submit_button("Submit")































