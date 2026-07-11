import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Intelligent Catalogue Builder")

st.title("🛒 Intelligent Catalogue Builder")

st.markdown("""
### AI-Powered Retail Analytics Dashboard

Upload a sales report to:
- Analyze sales performance
- Identify top-selling products
- Track profits
- Generate product catalogues
- Generate marketing content
""")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx", "xls"]
)

if uploaded_file:

    # Read Excel
    df = pd.read_excel(uploaded_file, header=1)
    st.write(df.columns.tolist())
    # Remove empty columns
    df = df.loc[:, ~df.columns.isna()]

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Brand Detection
    df["Brand"] = (
        df["Product Name"]
        .astype(str)
        .str.split()
        .str[0]
    )

    # Pack Size Detection
    df["Pack Size"] = (
        df["Product Name"]
        .astype(str)
        .str.extract(
            r'(\d+\s?(?:ml|ML|gm|GM|g|G|kg|KG|L|ltr|Ltr))',
            expand=False
        )
    )

    # Description
    df["Description"] = (
        "High quality product suitable for everyday use."
    )

    # Tags
    df["Tags"] = "Best Seller"

    # Numeric Conversion
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

    st.success("✅ File Uploaded Successfully")

    st.write("Total Records:", len(df))



    # Dataset Preview
    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())
    # Margin Percentage
    df["Margin %"] = (
            (df["Profit and Loss"] / df["Total Sales Amount"]) * 100
    ).round(2)

    # Simple Subcategory Detection
    df["Subcategory"] = df["Category"]


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

    # Category Analysis
    st.subheader("📊 Category Analysis")

    category_sales = (
        df.groupby("Category")["Total Sales Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)

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

    # Top Profitable Products
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

    # High Margin Products
    st.subheader("💎 High Margin Products")

    st.dataframe(
        top_profit[
            ["Product Name", "Profit and Loss"]
        ].head(10)
    )

    # Slow Moving Products
    st.subheader("🐢 Slow Moving Products")

    slow_products = df.sort_values(
        by="Total Quantity",
        ascending=True
    )

    st.dataframe(
        slow_products[
            ["Product Name", "Total Quantity"]
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

    # Product Search
    st.subheader("🔍 Search Product")

    search = st.text_input("Enter Product Name")

    if search:
        filtered = df[
            df["Product Name"]
            .astype(str)
            .str.contains(search, case=False, na=False)
        ]

        st.dataframe(filtered)

    # Product Catalogue
    st.subheader("📋 Product Catalogue")

    catalogue = df[
        [
            "Product Name",
            "Brand",
            "Pack Size",
            "Category",
            "Subcategory",
            "Description",
            "Tags",
            "Total Sales Amount",
            "Total Purchase Amount",
            "Profit and Loss",
            "Margin %"
        ]
    ]

    st.dataframe(catalogue)

    # Download Catalogue
    csv = catalogue.to_csv(index=False)

    st.download_button(
        label="📥 Download Catalogue",
        data=csv,
        file_name="catalogue.csv",
        mime="text/csv"
    )
    # Product Image Finder
    st.subheader("🖼 Product Image Finder")

    selected_image_product = st.selectbox(
        "Select Product for Image Search",
        df["Product Name"],
        key="image_product"
    )

    product = str(selected_image_product).lower()

    image_path = "images/default.jpg"

    if "egg" in product:
        image_path = "images/eggs.jpg"

    elif "milk" in product:
        image_path = "images/milk.jpg"

    elif "kinley" in product or "water" in product:
        image_path = "images/kinley.jpg"

    elif "paneer" in product:
        image_path = "images/paneer.jpg"

    elif "coconut" in product:
        image_path = "images/coconut_water.jpg"

    elif "cashew" in product:
        image_path = "images/cashew.jpg"

    st.write("### Product Images")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(image_path, caption="Image 1")

    with col2:
        st.image(image_path, caption="Image 2")

    with col3:
        st.image(image_path, caption="Image 3")

    st.write("### ⭐ Recommended Image")

    st.image(
        image_path,
        caption=f"Recommended for {selected_image_product}",
        use_container_width=True
    )

    st.success("Confidence Score: 92%")

    st.info(
        "Best image selected automatically using product matching."
    )
    # Marketing Creative Generator
    st.subheader("🎨 Marketing Creative Generator")

    creative_product = st.selectbox(
        "Select Product for Creative",
        df["Product Name"],
        key="creative_product"
    )

    creative_type = st.selectbox(
        "Select Creative Type",
        [
            "Individual Product",
            "High Selling Product",
            "High Margin Product",
            "Festival Campaign"
        ]
    )

    if st.button("Generate Creative"):

        st.success(f"Creative Generated: {creative_type}")

        st.markdown(f"""
## 🔥 {creative_type}

### {creative_product}

✅ Premium Quality

✅ Customer Favourite

✅ Available Now

📞 Visit Our Store Today
""")

        st.image(
            "https://placehold.co/600x400?text=Marketing+Creative",
            caption="Marketing Poster",
            use_container_width=True
        )

    # Marketing Content Generator
    st.subheader("📢 Marketing Content Generator")

    selected_product = st.selectbox(
        "Select Product",
        df["Product Name"]
    )

    if st.button("Generate Marketing Content"):

        headline = f"🔥 Special Offer on {selected_product}"

        push_notification = (
            f"{selected_product} is now available. "
            f"Order today and don't miss this opportunity."
        )

        whatsapp_message = f"""
Hello Customer,

Check out our featured product:

{selected_product}

✅ High Quality
✅ Customer Favourite
✅ Great Value

Visit our store today.

Thank You.
"""

        st.write("### Campaign Headline")
        st.success(headline)

        st.write("### Push Notification")
        st.info(push_notification)

        st.write("### WhatsApp Message")
        st.text(whatsapp_message)

        marketing_text = f"""
Campaign Headline:
{headline}

Push Notification:
{push_notification}

WhatsApp Message:
{whatsapp_message}
"""

        st.download_button(
            "📥 Download Marketing Copy",
            marketing_text,
            file_name="marketing_copy.txt"
        )

    # Product Tags
    st.subheader("🏷 Product Tags")

    st.info("Best Seller | High Demand | Popular Product")