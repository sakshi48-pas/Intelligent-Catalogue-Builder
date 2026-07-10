import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Intelligent Catalogue Builder")

st.title("🛒 Intelligent Catalogue Builder")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx", "xls"]
)

if uploaded_file:

    df = pd.read_excel(uploaded_file, header=1)

    # Remove empty columns
    df = df.loc[:, ~df.columns.isna()]

    # Convert numeric columns
    df["Total Sales Amount"] = pd.to_numeric(
        df["Total Sales Amount"],
        errors="coerce"
    )

    df["Profit and Loss"] = pd.to_numeric(
        df["Profit and Loss"],
        errors="coerce"
    )

    df["Total Quantity"] = pd.to_numeric(
        df["Total Quantity"],
        errors="coerce"
    )

    st.success("File Uploaded Successfully!")

    # Dataset Preview
    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    # Business Summary
    st.subheader("📊 Business Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Sales",
            f"₹ {df['Total Sales Amount'].sum():,.0f}"
        )

    with col2:
        st.metric(
            "Total Profit",
            f"₹ {df['Profit and Loss'].sum():,.0f}"
        )

    with col3:
        st.metric(
            "Total Quantity Sold",
            int(df["Total Quantity"].sum())
        )

    # Top Selling Products
    st.subheader("🔥 Top 10 Selling Products")

    top_sales = df.sort_values(
        by="Total Sales Amount",
        ascending=False
    )

    st.dataframe(
        top_sales[
            ["Product Name", "Total Sales Amount"]
        ].head(10)
    )

    # Top Profit Products
    st.subheader("💰 Top 10 Profitable Products")

    top_profit = df.sort_values(
        by="Profit and Loss",
        ascending=False
    )

    st.dataframe(
        top_profit[
            ["Product Name", "Profit and Loss"]
        ].head(10)
    )

    # Sales Chart
    st.subheader("📈 Top 10 Sales Chart")

    fig, ax = plt.subplots(figsize=(10, 5))

    top10 = top_sales.head(10)

    ax.bar(
        top10["Product Name"],
        top10["Total Sales Amount"]
    )

    plt.xticks(rotation=90)

    st.pyplot(fig)

    # Product Catalogue
    st.subheader("📋 Product Catalogue")

    catalogue = df[
        [
            "Product Name",
            "Category",
            "Total Sales Amount",
            "Profit and Loss"
        ]
    ]

    st.dataframe(catalogue)

    # Marketing Generator
    st.subheader("🤖 Marketing Content Generator")

    selected_product = st.selectbox(
        "Select Product",
        df["Product Name"]
    )

    if st.button("Generate Marketing Text"):

        text = f"""
        Buy {selected_product} today!

        High quality product at a great price.

        Limited stock available. Order now!
        """

        st.success(text)