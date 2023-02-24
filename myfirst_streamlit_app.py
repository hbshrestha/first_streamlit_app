#https://www.youtube.com/watch?v=Sb0A9i6d320&t=557s&ab_channel=CodingIsFun


import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

#if you want to emojis icon: # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title = "Himalaya's Sales Dashboard",
                  page_icon = ":bar_chart", #use icon of bar chart
                  layout = "wide"  #use entire screen
                  )

#read excel file
df = pd.read_excel("data/supermarkt_sales.xlsx",
                  sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,)

# Add 'hour' column to dataframe
df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    
#sidebar
st.sidebar.header("Please filter here:")

city = st.sidebar.multiselect("Select the city:",
                             options = df["City"].unique(),
                             default = df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)


#main page
st.title(":bar_chart: My Sales dashboard")

#insert new paragraph
st.markdown("##")

#kpi's
total_sales = int(df_selection["Total"].sum())

average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))

average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")

with middle_column:
    st.subheader("Average rating:")
    st.subheader(f"{average_rating} {star_rating}")

with right_column:
    st.subheader("Average sales per transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("---")

sales_by_product_line = df_selection.groupby(by = ["Product line"]).sum()[["Total"]].sort_values(by = ["Total"])

fig_product_sales = px.bar(
    sales_by_product_line,
    x = 'Total',
    y = sales_by_product_line.index,
    orientation = "h",
    title = "<b>Sales by Product Line </b>",
    color_discrete_sequence = ["#0083BB"] * len(sales_by_product_line),
    template = "plotly_white"
)

fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0, 0, 0, 0)",
    xaxis = (dict(showgrid = False))
)

# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width = True)

st.dataframe(df_selection)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(unsafe_allow_html=True)
