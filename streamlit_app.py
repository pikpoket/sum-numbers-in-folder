import pandas as pd
import os
import streamlit as st
import re

columns = ["File name", "Only numbers", "Split", "Index", "Reverse index"]
result_df = pd.DataFrame(columns=columns)


def sum_files(folder_path, i=0, j=0, split_separator="", split_index=0):
    global result_df
    sumFac = 0
    for file in os.listdir(folder_path):
        filename = os.fsdecode(file)
        if filename.endswith(".pdf"):
            only_numbers = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?!\d)', filename)
            index_method = os.path.join(filename)[i:]
            reverse_method = os.path.join(filename)[:-i]
            split = os.path.join(filename).split(split_separator)[split_index][:j]
            if type(only_numbers) == list:
                only_numbers = ','.join(only_numbers)
            line = [filename, only_numbers, split, index_method, reverse_method]
            result_df.loc[len(result_df)] = line
        else:
            continue
    return result_df


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    st.title('Easy sum calculator')
    st.header(
        'This script finds for each file the numbers in the name and sums them. Useful for invoices. Double check for errors.')

    # Help button to toggle help text

    st.write("""
            **How it works:**

            By default, the script will try to locate the numbers in the file that look like a price (with a coma).
            You may also specify parameters for more complex operations:

            - **Split by separator:** Specify the character separator used to split the filename.
            - **And take the portion number:** Which batch should be used from the splitted filename.
            - **then apply index** Should an index be applied for this batch ? You can use negative numbers to start from the end.
            - **Index only:** Alternative method, just take the X first letters. You can use negative numbers to start from the end.

            Do you own experiment !
        """)


    filepath_module = st.text_input("Enter the path to the files",
                                    value=r"\\almacg.com\frlyo1\Partage INN_CLIENTS_A\AGAMA GROUP\IP_BOX\2023\0 - Documents Clients\OVH 2023")
    col1, col2, col3 = st.columns(3)
    with col1:
        split_by = st.text_input("Split by separator", value=" ")
        i = st.number_input("Index only", value=0)
    with col2:
        k = st.number_input("And take the portion number ", value=0)
    with col3:
        j = st.number_input("then apply index", value=0)


    # Créer un conteneur pour le bouton et les données générées
    container = st.container()

    if container.button("Validate"):
        result_df = sum_files(filepath_module, i, j, split_by, k)
        container.dataframe(data=result_df)
    else:
        container.write("Click validate to gen data.")

    html_code = """
    <p style="text-align: right; color: grey; font-size: 11px;">
        Made by Sévan Pacharian
    </p>
    """
    # Render the HTML and CSS in Streamlit
    st.markdown(html_code, unsafe_allow_html=True)
