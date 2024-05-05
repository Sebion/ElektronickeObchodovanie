import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.sidebar.title('Interactive analysis of suppliers')
data = pd.read_csv('filtered_hlavna_sorted_doplnena_final.csv')
data = data.sort_values('AucZac')
# Group by 'Org' column and count rows
org_counts = data.groupby('Org').size()

# Sort in descending order and select top 10
top_orgs = org_counts.sort_values(ascending=False).head(10)

grouped_data = data.groupby('Vitaz')['VitaznaPonuka'].sum()

# Select the top 10 suppliers based on the sum of 'VitaznaPonuka'
top_suppliers = grouped_data.nlargest(10)

# Create a new subplot for the pie chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Create the first pie chart
ax1.pie(top_orgs, labels=top_orgs.index, autopct='%1.1f%%', textprops={'fontsize': 8})
ax1.set_title('Top 10 active organizations on the market')

# Create the second pie chart
ax2.pie(top_suppliers, labels=top_suppliers.index, autopct='%1.1f%%', textprops={'fontsize': 8})
ax2.set_title('Top 10 suppliers based on sum of VitaznaPonuka')


# Create a container for the pie chart
container1 = st.container()
with container1:
    st.pyplot(fig)

# Move the selectbox to the sidebar
column = st.sidebar.selectbox('Select a organization that you want to analyze : ', top_orgs.index)
st.sidebar.write(f'Displaying details about organization number: {column}')  # Print the selected column to the sidebar

# Filter the data for the selected organization
org_data = data[data['Org'] == column]

categories = org_data['Kateg'].unique()
category = st.sidebar.selectbox('Select a category for selected organization:', categories)
category_data = org_data[org_data['Kateg'] == category]

enable_subkategory_search = st.sidebar.checkbox('Enable search for Subkategory')

# Display the filtered data
container2 = st.container()
with container2:
    # Perform the search operation only if the checkbox is checked
    if enable_subkategory_search:
        # Get unique subcategories for the selected organization
        subkategories = category_data['Subkateg'].unique()

        # Add a selectbox for 'Subkategory'
        subkategory = st.sidebar.selectbox('Select a subkategory for selected organization:', subkategories)

        # Filter the data for the selected organization and subkategory
        filtered_data = category_data[category_data['Subkateg'] == subkategory]
        st.write("Data for the selected organization based on selected subcategory:")

        # Display the filtered data
        st.dataframe(filtered_data)
    else:
        # Display the data for the selected category without filtering by subcategory
        st.write("Data for the selected organization based on selected category:")

        st.dataframe(category_data)

container3 = st.container()
with container3:
    # Group the data by 'Vitaz' for the selected category and calculate the sum
    category_grouped_data = category_data.groupby('Vitaz').size()

    # Group the data by 'Vitaz' for the selected subcategory and calculate the sum
    if enable_subkategory_search:
        subcategory_data = category_data[category_data['Subkateg'] == subkategory]
        subcategory_grouped_data = subcategory_data.groupby('Vitaz').size()

    # Create a pie chart for the selected category and subcategory
    fig3, axs = plt.subplots(1, 2, figsize=(14, 7))  # 1 row, 2 columns

    # Create the first pie chart for the selected category
    axs[0].pie(category_grouped_data, labels=category_grouped_data.index, autopct='%1.1f%%')
    axs[0].set_title(f'Uspesnost dodavatelov pre kategoriu: {category}')

    # Create the second pie chart for the selected subcategory
    if enable_subkategory_search:
        axs[1].pie(subcategory_grouped_data, labels=subcategory_grouped_data.index, autopct='%1.1f%%')
        axs[1].set_title(f'Uspesnost dodavatelov pre subkategoriu: {subkategory}')

    # Display the pie charts in Streamlit
    st.pyplot(fig3)


# Create a container for the line plot
container4 = st.container()
with container4:
    if enable_subkategory_search:
        filtered_data = category_data[category_data['Subkateg'] == subkategory]
    else:
        filtered_data = category_data
        subkategory = "All subkategories"

    filtered_data = filtered_data.sort_values('AucZac')

    fig2, ax = plt.subplots(figsize=(10, 6))
    ax.plot(filtered_data['AucZac'], filtered_data['PocetAktivnychUcast'])
    ax.set_xlabel('Time')
    ax.set_ylabel('PocetAktivnychUcasti')
    ax.set_title(f'Pocet aktivnych ucasti na aukcii v priebehu casu pre kategoriu:{category} a subkategoriu:{subkategory}')
    ax.grid(True)

    # Display the plot in Streamlit
    st.pyplot(fig2)

