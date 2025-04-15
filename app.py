import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Clean My Data Pro", layout="centered")

# Load logo (optional - add your own logo file to the same folder)
try:
    logo = Image.open("logo.png")
    st.image(logo, width=150)
except:
    pass

st.title("🧼 Clean My Data Pro")
st.write("A simple tool to fix messy spreadsheets. Powered by AI and built for busy people.")

def clean_data(df):
    df.dropna(how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    df.columns = [col.strip() for col in df.columns]
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.applymap(lambda x: x.capitalize() if isinstance(x, str) else x)
    df.drop_duplicates(inplace=True)
    return df

def convert_df(df, file_type):
    output = BytesIO()
    if file_type == "csv":
        df.to_csv(output, index=False)
        mime = "text/csv"
        filename = "cleaned_file.csv"
    else:
        df.to_excel(output, index=False, engine='openpyxl')
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = "cleaned_file.xlsx"
    output.seek(0)
    return output, mime, filename

uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file:
    file_type = "csv" if uploaded_file.name.endswith(".csv") else "excel"

    try:
        df = pd.read_csv(uploaded_file) if file_type == "csv" else pd.read_excel(uploaded_file)
        st.subheader("📄 Original File Preview")
        st.dataframe(df.head(10))

        cleaned_df = clean_data(df.copy())

        st.subheader("✅ Cleaned File Preview")
        st.dataframe(cleaned_df.head(10))

        file_output, mime_type, file_name = convert_df(cleaned_df, file_type)

        st.download_button(
            label=f"⬇️ Download Cleaned {file_type.upper()} File",
            data=file_output,
            file_name=file_name,
            mime=mime_type,
        )

    except Exception as e:
        st.error(f"Error processing file: {e}")

# --- Footer with 1-Cedi Campaign CTA
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center;'>
        ❤️ Built with love by <strong>You</strong> — Join the <strong>1-Cedi Campaign</strong> <br>
        💰 If this tool helped you, consider supporting with just 1 cedi! <br><br>
        <a href="https://your-donation-link.com" target="_blank">
            <button style='padding: 0.5em 1em; border: none; background-color: green; color: white; border-radius: 8px;'>Support Now</button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
