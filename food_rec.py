import streamlit as st
import pandas as pd
from groq import Groq

# Initialize the Groq client
client = Groq(
    api_key="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",
)

# Load your food dataset
df = pd.read_csv('C:\\Users\\aditya vashisht\\Downloads\\coding for practice\\Food rec for walmart project\\archive (1)\\1662574418893344.csv')

# Extract food items from the 'Describe' column
try:
    food_items = df['Describe'].str.split(',').explode().str.strip().unique().tolist()
except KeyError:
    st.error("The column 'Describe' does not exist. Please check your dataset.")
    st.stop()

# Function to generate dish recommendations
# Function to generate dish recommendations
def recommend_dishes(selected_items):
    # Prepare the prompt with selected items and dish names
    dish_list = df['Name'].tolist()  # Using the 'Name' column for dish titles
    prompt_content = (
        f"Based on the selected items: {selected_items}, recommend dishes from this list: {dish_list}. "
        "Keep the response short and precise. Provide only the top 2-3 dish recommendations and "
        "suggest a few additional ingredients needed for each dish."
    )

    # Create a chat completion request
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt_content,
            }
        ],
        model="llama3-70b-8192",  # Ensure this model is supported by your Groq account
    )

    # Return the response from the LLM
    return chat_completion.choices[0].message.content


# Streamlit UI
st.title("Dish Recommendation System")

# Create a multiselect box for the user to select food items
selected_items = st.multiselect("Select the food items you have:", food_items)

# When the user clicks the "Recommend Dishes" button
if st.button("Recommend Dishes"):
    if selected_items:
        recommendations = recommend_dishes(selected_items)
        st.write("Dish Recommendations:")
        st.write(recommendations)
    else:
        st.write("Please select at least one food item.")
