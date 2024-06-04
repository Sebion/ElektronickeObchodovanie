import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
st.sidebar.title('Interactive analysis of suppliers')
ctyps = {'Vitaz': str}
data = pd.read_csv('new_hlavna.csv',dtype=ctyps)
data = data.sort_values('AucZac')
column_types = {'IDParticipant': str, 9:str}
bidy = pd.read_csv('new_bidy.csv',dtype=column_types)
# Group by 'Org' column and count rows
org_counts = data.groupby('Org').size()
top_orgs = org_counts.sort_values(ascending=False).head(10)

grouped_data = data.groupby('Vitaz')['VitaznaPonuka'].sum()
top_suppliers = grouped_data.nlargest(10)

column = st.sidebar.selectbox('Select a organization that you want to analyze : ', ['Select an organization...'] + list(top_orgs.index))

if column == 'Select an organization...':
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    ax1.pie(top_orgs, labels=top_orgs.index, autopct='%1.1f%%', textprops={'fontsize': 8})
    ax1.set_title('Top 10 active organizations on the market')

    ax2.pie(top_suppliers, labels=top_suppliers.index, autopct='%1.1f%%', textprops={'fontsize': 8})
    ax2.set_title('Top 10 suppliers based on sum of VitaznaPonuka')

    container1 = st.container()
    with container1:
        st.pyplot(fig)

    # container8 = st.container()
    # with container8:
    #     # Group the data by 'Vitaz'
    #     grouped_data = data.groupby('Vitaz')
    #     ru=grouped_data["Relativna Uspora"].mean()
    #     # Group by 'ParticipantID' and count rows
    #     participant_counts = bidy.groupby('IDParticipant').size()
    #
    #     # Count the number of unique 'UniqueID' for each 'ParticipantID'
    #     unique_id_counts = bidy.groupby('IDParticipant')['UniqueID'].nunique()
    #
    #     # Display the results
    #     # print("Count of rows grouped by ParticipantID:")
    #     # print(participant_counts)
    #     # print("\nNumber of unique IDs where each participant participated:")
    #     # print(unique_id_counts)
    #     # print(participant_counts/unique_id_counts)# Select the attributes you are interested in
    #
    #     attributes = ['Relativna Uspora']  # replace with your attributes
    #     data_selected = grouped_data[attributes]


if column != 'Select an organization...':

    # Move the selectbox to the sidebar
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
            # unique_ids = filtered_data['UniqueID'].unique()
            #
            # # Filter bidy based on these UniqueIDs
            # filtered_bidy = bidy[bidy['UniqueID'].isin(unique_ids)]
            #
            # # Get unique IDParticipant values from the filtered bidy
            # id_participant_options = filtered_bidy['IDParticipant'].unique()
            #
            # # Create a selectbox in the sidebar for IDParticipant
            # selected_id_participant = st.sidebar.selectbox('Select IDParticipant', id_participant_options)
            # Display the filtered data
            st.dataframe(filtered_data)
        else:
            # Display the data for the selected category without filtering by subcategory
            st.write("Data for the selected organization based on selected category:")
            # Get unique UniqueIDs from category_data
            # unique_ids = category_data['UniqueID'].unique()
            #
            # # Filter bidy based on these UniqueIDs
            # filtered_bidy = bidy[bidy['UniqueID'].isin(unique_ids)]
            #
            # # Get unique IDParticipant values from the filtered bidy
            # id_participant_options = filtered_bidy['IDParticipant'].unique()
            #
            # # Create a selectbox in the sidebar for IDParticipant
            # selected_id_participant = st.sidebar.selectbox('Select IDParticipant', id_participant_options)
            st.dataframe(category_data)
    container5 = st.container()
    with container5:
        # Group the data by 'Kateg' for the selected organization and calculate the sum of 'VitaznaPonuka'
        org_category_data = org_data.groupby('Kateg')['VitaznaPonuka'].sum()

        # Filter the data for the selected category
        category_data = org_data[org_data['Kateg'] == category]

        # Group the data by 'Subkateg' for the selected category and calculate the sum of 'VitaznaPonuka'
        org_subcategory_data = category_data.groupby('Subkateg')['VitaznaPonuka'].sum()

        # Create a subplot with 2 columns for the pie charts
        fig4, axs = plt.subplots(1, 2, figsize=(14, 7))

        # Create the first pie chart for 'Kateg'
        axs[0].pie(org_category_data, labels=org_category_data.index, autopct='%1.1f%%')
        axs[0].set_title(f'Rozlozenie nakladov podla jednotlivych kategorii a subkategorii pre organizaciu: {column}')

        # Create the second pie chart for 'Subkateg'
        axs[1].pie(org_subcategory_data, labels=org_subcategory_data.index, autopct='%1.1f%%')
        # axs[1].set_title(f'Rozlozenie nakladov pre subkategorie podla vybranej kategorie: {category}')

        # Display the pie charts in Streamlit
        st.pyplot(fig4)
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
        axs[0].set_title(f'Podiel dodavatelov pre kategoriu: {category}')

        # Create the second pie chart for the selected subcategory
        if enable_subkategory_search:
            axs[1].pie(subcategory_grouped_data, labels=subcategory_grouped_data.index, autopct='%1.1f%%')
            axs[1].set_title(f'Podiel dodavatelov pre subkategoriu: {subkategory}')

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


        # Group data by 'Vitaz' and calculate the mean of 'Relativna Uspora'
        average_relativna_uspora = filtered_data.groupby('Vitaz')['Relativna Uspora'].mean()


    unique_vitaz = filtered_data['Vitaz'].unique()
    # Convert 'unique_vitaz' to string
    # unique_vitaz = unique_vitaz.astype(str)
    # print(unique_vitaz[0].dtype)
    # Filter the 'bidy' DataFrame based on whether 'IDParticipant' is in 'unique_vitaz'
    filtered_bidy = bidy[bidy['IDParticipant'].isin(unique_vitaz)]

    # Count the number of rows for each 'IDParticipant' in the filtered 'bidy' DataFrame
    participant_counts = filtered_bidy.groupby('IDParticipant').size()
    # print(participant_counts)
    # Count the number of unique 'UniqueID' for each 'IDParticipant' in the filtered 'bidy' DataFrame
    unique_id_counts = filtered_bidy.groupby('IDParticipant')['UniqueID'].nunique()
    # Display the results
    ppb = participant_counts / unique_id_counts
    # Print unique values of unique_vitaz

    # Sort the series in descending order
    sorted_average_relativna_uspora = average_relativna_uspora.sort_values(ascending=False)

    # Count the number of UniqueIDs in bidy for each 'IDParticipant' in 'filtered_bidy'
    num_unique_ids_bidy = filtered_bidy.groupby('IDParticipant')['UniqueID'].nunique()

    # Count the number of UniqueIDs in data where 'Vitaz' is in 'filtered_bidy'
    num_unique_ids_data = data[data['Vitaz'].isin(filtered_bidy['IDParticipant'])].groupby('Vitaz')[
        'UniqueID'].nunique()

    # Calculate the success rate for each 'IDParticipant' in 'filtered_bidy'
    success_rate = num_unique_ids_data / num_unique_ids_bidy

    # Display the success rate
    # print(success_rate)
    combined_df = pd.concat(
        [sorted_average_relativna_uspora, ppb, participant_counts, unique_id_counts, success_rate, num_unique_ids_data,
         num_unique_ids_bidy], axis=1)

    # Rename the columns
    combined_df.columns = ['Priemerna relativna uspora', 'Priemerny pocet bidov na jednu aukciu', 'Celkovy pocet bidov',
                           'Pocet zucastnenych aukcii', 'Success rate', 'Vyhral', 'Zucastnil sa']

    # Create a new container at the bottom
    container6 = st.container()
    with container6:
        # Display the sorted series
        st.write("Average 'Relativna Uspora' grouped by 'Vitaz' ordered by the biggest 'Relativna Uspora':")

        # Concatenate the two series into a DataFrame along the columns axis


        # Display the DataFrame in Streamlit
        st.dataframe(combined_df)
        # with container6:
        #     st.write(f"Pocet ucasti {selected_id_participant}: {num_unique_ids_bidy}")
        #     st.write(f"Pocet vitazstiev {selected_id_participant}: {num_unique_ids_data}")
        #     st.write(f"Success rate for ParticipantID {selected_id_participant}: {success_rate}")


    container8 = st.container()
    with container8:
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
        import matplotlib.pyplot as plt
        import numpy as np

        # Select the attributes
        attributes = ['Priemerna relativna uspora', 'Priemerny pocet bidov na jednu aukciu', 'Success rate']
        selected_data = combined_df[attributes]

        # Standardize the data
        scaler = StandardScaler()
        standardized_data = scaler.fit_transform(selected_data)

        # Apply PCA
        pca = PCA(n_components=2)
        principal_components = pca.fit_transform(standardized_data)

        # Create a DataFrame with the first two principal components
        pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

        # Calculate the distance from each point to the origin
        distances = np.sqrt((pca_df['PC1'] ** 2) + (pca_df['PC2'] ** 2))

        # Define a threshold for what you consider an outlier
        threshold = np.percentile(distances, 95)  # 95th percentile, for example

        # Create a boolean mask for the outliers
        outliers_mask = distances > threshold

        # Plot the first two principal components
        plt.figure(figsize=(8, 6))
        plt.scatter(pca_df['PC1'], pca_df['PC2'], c=outliers_mask)

        # Add text next to each outlier dot using the index values from the DataFrame
        for i in range(len(pca_df)):
            plt.text(pca_df.iloc[i]['PC1'], pca_df.iloc[i]['PC2'], combined_df.index[i])

        plt.xlabel('First Principal Component (PC1)')
        plt.ylabel('Second Principal Component (PC2)')
        plt.title('PCA of combined_df with Outliers')
        st.pyplot(plt)
    if enable_subkategory_search:
        # Group data by 'Vitaz' and calculate the mean of 'Relativna Uspora'
        average_relativna_uspora_graf = filtered_data.groupby('AucZac')['Relativna Uspora'].mean()
    else :
        average_relativna_uspora_graf = category_data.groupby('AucZac')['Relativna Uspora'].mean()
    container7 = st.container()
    with container7:
        # Create a plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(average_relativna_uspora_graf)
        ax.set_xlabel('Time')
        ax.set_ylabel('Average Relativna Uspora')
        ax.set_title(f'Average Relativna Uspora over time for category: {category} and subcategory: {subkategory}')
        ax.grid(True)

        # Display the plot in Streamlit
        st.pyplot(fig)


