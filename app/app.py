import pandas                   as pd
import numpy                    as np
import seaborn                  as sns
import matplotlib.pyplot        as plt
import plotly.express           as px
import streamlit                as st
import streamlit_extras
from streamlit_extras.metric_cards import style_metric_cards

# Load Data===========================================================================================

df_raw = pd.read_csv('../dataset/src/price_elasticity.csv')
df_raw = df_raw.drop(columns = ['Unnamed: 0'])
df_bp = pd.read_csv('../dataset/src/business_performance.csv')
df_e = pd.read_csv('../dataset/src/elasticity.csv')
df_e = df_e.drop(columns = ['Unnamed: 0'])
df_cp = pd.read_csv('../dataset/src/cross_price.csv')

# Page config ========================================================================================
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.title('Price Elasticity Analysis')
sns.set_theme(rc = {'figure.figsize':(15,10)})
style_metric_cards(border_left_color="#00688B")

tab1, tab2, tab3, tab4 = st.tabs(['About Project', 'Product Elasticity Analysis', 'Bussiness Performance', 'Cross Price Elasticity'])

with tab1:
    st.subheader('Business Problem')
    st.text('A company intends to change the prices of the products it sells, but is concerned that this alteration might impact the demand \nfor these products and consequently affect revenue. As a data analyst/scientist, you need to determine price elasticity using scientific \nmethodology based on the data from the prices of the products sold by the company.')
    st.dataframe(df_raw, use_container_width = True)

with tab2:
    label_selection = st.checkbox('Activate Label Cards')
    if label_selection:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric('Total of Stores', len(df_raw['brand'].unique()))
        col2.metric('Total of Brands', len(df_raw['merchant'].unique()))
        col3.metric('Average Billing', np.round(df_raw['disc_price'].mean(),2))
        col4.metric('Total of Billing', np.round(df_raw['disc_price'].sum(), 2))


    select_graph = st.selectbox('Select the Analysis:  ', ('Stores and Brands Overview', 'Volumetric Analysis', 'Temporal Analysis', 'Billing Analysis'))
    if select_graph == 'Stores and Brands Overview':
        col3, col4 = st.columns(2)
        with col3:
            aux = df_raw.groupby(['merchant', 'brand']).size().reset_index(name='count')
            aux = aux.groupby('merchant')['count'].sum().reset_index().sort_values(by='count', ascending=False)
            graph = px.bar(aux, x='merchant', y='count', color='merchant',text_auto = '0.2s', title = 'Number of brands per store')
            st.plotly_chart(graph, use_container_width=True)

        with col4:
            df_aux_perc = pd.DataFrame(df_raw['merchant'].value_counts(normalize=True) * 100).reset_index()
            df_aux_perc.columns = ['merchant', 'proportion']
            graph1 = px.bar(df_aux_perc, x='merchant', y='proportion', color='merchant', text='proportion', title = 'Volume of brands per store') 
            graph1.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
            st.plotly_chart(graph1, use_container_width=True)

        aux2 = df_raw.loc[:, ['date', 'category_name']].groupby('category_name').count().reset_index().sort_values(by='date', ascending=False).head(30)
        graph2 = px.bar(aux2, x = 'category_name', y = 'date', text_auto = '0.2s', title = 'Best Selling Products by Store')
        st.plotly_chart(graph2, use_container_width=True)

    elif select_graph  == 'Volumetric Analysis':
        
        option_product = st.checkbox('All products', value=True)
        option_merchant = st.checkbox('All Merchants', value=True)

        filtered_df = df_raw

        if not option_product:
            product = st.selectbox('Select the Product:  ', df_raw['category_name'].unique())
            filtered_df = filtered_df[filtered_df['category_name'] == product]

        if not option_merchant:
            merchant = st.selectbox('Select Merchant:  ', df_raw['merchant'].unique())
            filtered_df = filtered_df[filtered_df['merchant'] == merchant]

        cols1, cols2 = st.columns(2)

        with cols1:
            aux11 = filtered_df[['date', 'brand']].groupby('brand').count().reset_index().sort_values('date', ascending=False)
            plot = px.bar(aux11.head(10), x='brand', y='date', color='brand', text_auto='0.2s', title='Top more sales')
            st.plotly_chart(plot, use_container_width=True)
            with st.expander('Dataset Information'):
                st.dataframe(aux11)

        with cols2:
            df_aux_perc = pd.DataFrame(filtered_df['brand'].value_counts(normalize=True) * 100).reset_index()
            df_aux_perc.columns = ['brand', 'proportion']
            graph1 = px.bar(df_aux_perc.head(10).sort_values('proportion', ascending=False), x='brand', y='proportion', color='brand', text='proportion', title='Store Volumetry by category') 
            graph1.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
            st.plotly_chart(graph1, use_container_width=True)
            with st.expander('Dataset Information'):
                df_aux_perc_aux = df_aux_perc.copy()
                df_aux_perc_aux['proportion'] = df_aux_perc_aux['proportion'].apply(lambda x: f'{x:.2f}%')
                st.dataframe(df_aux_perc_aux)

    elif select_graph  == 'Temporal Analysis':

        option_product2 = st.checkbox('All products', value=True)
        option_merchant2 = st.checkbox('All Merchants', value=True)

        df = df_raw.copy()
        df['day_week'] = df['day_week'].replace({'Sunday': '1 - Sunday', 'Monday': '2 - Monday', 
                                                     'Tuesday': '3 - Tuesday', 'Wednesday': '4 - Wednesday', 
                                                     'Thursday': '5 - Thursday', 'Friday': '6 - Friday',
                                                     'Saturday': '7 - Saturday'})
        
        df['month'] = df['month'].replace({'January': '1 - January', 'February': '2 - February', 
                                                     'March': '3 - March', 'April': '4 - April', 
                                                     'May': '5 - May', 'June': '6 - June',
                                                     'July': '7 - July', 'August': '8 - August', 'September': '9 - September',
                                                     'October': '91 - October', 'November': '92 - November', 'December': '93 - December'})
        df_select_time = df.copy()

        columns3, columns4 = st.columns(2)
        cols3, cols4 = st.columns(2)

        if not option_product2:
            with columns3:
                product2 = st.selectbox('Select the Product:  ', df['category_name'].unique())
                df_select_time = df_select_time.loc[df_select_time['category_name'] == product2]

        if not option_merchant2:
            with columns4:
                merchant2 = st.selectbox('Select the Product:  ', df['merchant'].unique())
                df_select_time = df_select_time.loc[df_select_time['merchant'] == merchant2]

        with cols3:
            aux3 = df_select_time.groupby(['merchant', 'day_week']).count().reset_index().sort_values(by = 'day_week', ascending = True)
            plot3 = px.bar(aux3, x = 'day_week', y = 'date', text_auto='0.2s', color = 'merchant', title='Top more sales')
            st.plotly_chart(plot3, use_container_width=True)
            with st.expander('Dataset Information'):
                st.dataframe(aux3)



        with cols4:
            aux4 = df_select_time.groupby(['merchant', 'month']).count().reset_index().sort_values(by = 'month', ascending = True)
            plot4 = px.bar(aux4, x = 'month', y = 'date', color = 'merchant', text_auto='0.2s', title='Top more sales')
            st.plotly_chart(plot4, use_container_width=True)
            with st.expander('Dataset Information'):
                st.dataframe(aux4)


        aux5 = df_select_time.groupby(['merchant', 'week_number']).count().reset_index().sort_values(by = 'week_number', ascending = True)
        plot5 = px.bar(aux5, x = 'week_number', y = 'date', color = 'merchant', text_auto='0.2s', title='Top more sales')
        st.plotly_chart(plot5, use_container_width=True)
        with st.expander('Dataset Information'):
            st.dataframe(aux5)

    elif select_graph  == 'Billing Analysis':

        df = df_raw.copy()
        df['day_week'] = df['day_week'].replace({'Sunday': '1 - Sunday', 'Monday': '2 - Monday', 
                                                     'Tuesday': '3 - Tuesday', 'Wednesday': '4 - Wednesday', 
                                                     'Thursday': '5 - Thursday', 'Friday': '6 - Friday',
                                                     'Saturday': '7 - Saturday'})
        
        df['month'] = df['month'].replace({'January': '1 - January', 'February': '2 - February', 
                                                     'March': '3 - March', 'April': '4 - April', 
                                                     'May': '5 - May', 'June': '6 - June',
                                                     'July': '7 - July', 'August': '8 - August', 'September': '9 - September',
                                                     'October': '91 - October', 'November': '92 - November', 'December': '93 - December'})
               
        df_select_time2 = df.copy()

        option_product3 = st.checkbox('All products', value=True)
        option_merchant3 = st.checkbox('All Merchants', value=True)

        columns5, columns6 = st.columns(2)
        cols5, cols6 = st.columns(2)

        if not option_product3:
            with columns5:
                product3 = st.selectbox('Select the Product:  ', df['category_name'].unique())
                df_select_time2 = df_select_time2.loc[df_select_time2['category_name'] == product3]

        if not option_merchant3:
            with columns6:
                merchant3 = st.selectbox('Select the Product:  ', df['merchant'].unique())
                df_select_time2 = df_select_time2.loc[df_select_time2['merchant'] == merchant3]

        with cols5:
            aux5 = df_select_time2.groupby(['merchant', 'day_week'])['disc_price'].mean().reset_index().sort_values(by = 'day_week', ascending = True)
            plot5 = px.bar(aux5, x = 'day_week', y = 'disc_price', color = 'merchant', text_auto='0.2s', title='Top more sales')
            st.plotly_chart(plot5, use_container_width=True)
            with st.expander('Dataset Information'):
                st.dataframe(aux5)

        with cols6:           
            aux6 = df_select_time2.aux5 = df_select_time2.groupby(['merchant', 'month'])['disc_price'].mean().reset_index().sort_values(by = 'month', ascending = True)
            plot6 = px.bar(aux6, x = 'month', y = 'disc_price', color = 'merchant', text_auto='0.2s', title='Top more sales')
            st.plotly_chart(plot6, use_container_width=True)
            with st.expander('Dataset Information'):
                st.dataframe(aux6)
        
        
with tab3:

    df_e['ranking'] = df_e.loc[:, 'price_elasticity'].rank(ascending = True).astype(int)
    df_elasticity_product = df_e.reset_index(drop=True)

    fig, ax = plt.subplots()
    plt.figure(figsize = (10,10))
    ax.hlines(y = df_elasticity_product['ranking'], 
            xmin = 0, 
            xmax = df_elasticity_product['price_elasticity'], 
            alpha = 1, 
            linewidth = 8)

    for name, p in zip(df_elasticity_product['name'], df_elasticity_product['ranking']):
        ax.text(4, p, name)

    for x, y, s in zip(df_elasticity_product['price_elasticity'], df_elasticity_product['ranking'], df_elasticity_product['price_elasticity']):
        ax.text(x, y, round(s, 2), horizontalalignment='right' if x < 0 else 'left', 
                verticalalignment='center',
                fontdict={'color': 'red' if x < 0 else 'green', 'size': 12})

    plt.gca().set(ylabel = 'Ranking Number', xlabel = 'Price Elasticity')
    plt.title('Price Elasticity')
    plt.grid(linestyle = '--')
    st.pyplot(fig= fig)
    st.dataframe(df_elasticity_product.set_index('name'), use_container_width = True)


with tab4:
    st.dataframe(df_cp.set_index('name'), use_container_width = True)



