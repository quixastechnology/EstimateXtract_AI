import streamlit as st
import requests

st.title("EstimateXtract AI")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    try:
        # Send file to Django API
        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')}
        response = requests.post('http://localhost:8000/api/upload/', files=files)
        
        if response.status_code == 200:
            cleaned_data = response.json()
            st.write("Extracted Key Values from PDF:")
            
            # Display Window Specifications
            st.subheader("Window Specifications:")
            if cleaned_data["windows"]:
                for window in cleaned_data["windows"]:
                    st.write(f"- Window Type: {window['window_type']}")
                    st.write(f"  Material: {window['material']}")
                    st.write(f"  Width (inches): {window['width_inches']}")
                    st.write(f"  Height (inches): {window['height_inches']}")
                    st.write(f"  Glass Type: {window['glass_type']}")
                    st.write(f"  Color: {window['color']}")
                    st.write(f"  Quantity: {window['quantity']}")
                    st.write(f"  Manufacturer: {window['manufacturer']}")
                    st.write("")  # New line for better readability
            else:
                st.write("No window specifications found.")

            # Display Door Specifications
            st.subheader("Door Specifications:")
            if cleaned_data["doors"]:
                for door in cleaned_data["doors"]:
                    st.write(f"- Door Type: {door['door_type']}")
                    st.write(f"  Material: {door['material']}")
                    st.write(f"  Width (inches): {door['width_inches']}")
                    st.write(f"  Height (inches): {door['height_inches']}")
                    st.write(f"  Glass Type: {door['glass_type']}")
                    st.write(f"  Color: {door['color']}")
                    st.write(f"  Quantity: {door['quantity']}")
                    st.write(f"  Manufacturer: {door['manufacturer']}")
                    st.write("")  # New line for better readability
            else:
                st.write("No door specifications found.")

        else:
            st.error(f"Error processing PDF: {response.json().get('error')}")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
