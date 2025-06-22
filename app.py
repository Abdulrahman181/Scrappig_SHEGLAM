import pandas as pd
import re
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud

# Load the data
df = pd.read_csv("sheglam_products.csv")

# Streamlit Title and Website Link
st.title("SHEGLAM Product Analysis Dashboard 💄")
st.markdown("[Visit Sheglam Website 🎀](https://www.sheglam.com/)")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Main Dashboard", "Visualizations", "Collections Analysis"])

# Clean Price column to numeric 💵
df['Price'] = df['Price'].replace('[\\$,]', '', regex=True).astype(float)

# Sidebar filters 🛠
with st.sidebar:
    st.header("Filter Options 🔍")
    categories = df['Category'].dropna().unique().tolist()
    selected_category = st.multiselect("Select Category", categories, default=categories)

# Apply filters ✅
filtered_df = df[df['Category'].isin(selected_category)]

# -------------------- TAB 1: MAIN DASHBOARD --------------------
with tab1:
    # Display filtered data 📋
    st.subheader("Filtered Products 🛒")
    st.write(f"Total Results: {filtered_df.shape[0]}")
    st.dataframe(filtered_df)

    # Overview Stats
    st.header("Descriptive Statistics 📊")
    st.subheader("Price and Stars Summary")
    st.dataframe(df[['Price', 'Stars']].describe().round(2))

    # Category and Subcategory
    st.header("Category and Subcategory Analysis 📂")
    st.subheader("Average Price and Stars by Category 🏷")
    st.dataframe(df.groupby('Category')[['Price', 'Stars']].mean().round(2))
    st.subheader("Average Price and Stars by Subcategory 🏷")
    st.dataframe(df.groupby('Subcategory')[['Price', 'Stars']].mean().round(2))

    # Best Sellers Analysis
    st.header("Best Sellers Overview")
    st.subheader("Best Seller Counts by Category 📊")
    best_seller_count = df[df['Best Seller'] == 1]['Category'].value_counts().reset_index()
    best_seller_count.columns = ['Category', 'Best Seller Count']
    st.dataframe(best_seller_count)

    st.subheader("Best Seller Counts by Subcategory 📊")
    best_seller_subcat_count = df[df['Best Seller'] == 1]['Subcategory'].value_counts()
    st.write(best_seller_subcat_count)

    # Top Rated Products
    st.header("Top Rated Products (4.5+ Stars)")
    top_rated = df[df['Stars'] >= 4.5].sort_values(by=['Stars', 'Price'], ascending=[False, True]).head(10)
    st.dataframe(top_rated[['Name', 'Stars', 'Category', 'Price']])

# -------------------- TAB 2: VISUALIZATIONS --------------------
with tab2:
    # Average Price and Stars by Category
    st.header("Average Price and Stars by Category 📊")
    subcat_stats = df.groupby('Category')[['Price','Stars']].mean().round(2).sort_values('Price', ascending=False)
    fig3, ax = plt.subplots(figsize=(10,8))
    sns.barplot(x=subcat_stats.index, y='Price', data=subcat_stats, color='#CCCCFF', ax=ax)  
    plt.xticks(rotation=90)
    ax.set_ylabel('Average Price ($)', color='black')
    ax.set_title('Average Price & Stars by Category', pad=20, color='black', fontweight='bold')
    ax.tick_params(axis='y', colors='black')
    ax2 = ax.twinx()
    sns.lineplot(x=subcat_stats.index, y='Stars', data=subcat_stats,
                 color='#B388EB', marker='o', ax=ax2, linewidth=2.5)  
    ax2.set_ylabel('Average Stars', color='black')
    ax2.tick_params(axis='y', colors='black')
    ax.annotate('Highest Price', xy=(0, subcat_stats.Price.iloc[0]),
                xytext=(5, 5), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='#FFC0CB', alpha=0.3),
                color='black')
    ax2.annotate('Lowest Stars', xy=(subcat_stats.Stars.idxmin(), subcat_stats.Stars.min()),
                 xytext=(-40, 15), textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', color='#B388EB'),
                 bbox=dict(boxstyle='round', fc='white'),
                 color='black')
    st.pyplot(fig3)
    
    # Average Price and Stars by Subcategory
    st.header("Average Price and Stars by Subcategory 📊")
    subcat_stats = df.groupby('Subcategory')[['Price', 'Stars']].mean().round(2).sort_values('Price', ascending=False)
    fig4, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=subcat_stats.index, y='Price', data=subcat_stats, color='#B388EB', ax=ax)  
    plt.xticks(rotation=90)
    ax.set_ylabel('Average Price ($)', color='black')
    ax.set_title('Average Price & Stars by Subcategory', pad=20, color='black', fontweight='bold')
    ax.tick_params(axis='y', colors='black')
    ax2 = ax.twinx()
    sns.lineplot(x=subcat_stats.index, y='Stars', data=subcat_stats,
                 color='#CCCCFF', marker='o', ax=ax2, linewidth=2.5)  
    ax2.set_ylabel('Average Stars', color='black')
    ax2.tick_params(axis='y', colors='black')
    ax.annotate('Highest Price', xy=(0, subcat_stats.Price.iloc[0]),
                xytext=(5, 5), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', fc='#ADD8E6', alpha=0.3),  
                color='black')
    ax2.annotate('Lowest Stars', xy=(subcat_stats.Stars.idxmin(), subcat_stats.Stars.min()),
                 xytext=(-40, 15), textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', color='#4682B4'),
                 bbox=dict(boxstyle='round', fc='white'),
                 color='black')
    st.pyplot(fig4)
    
    # Best Seller vs Non-Best Seller
    st.header("Best Seller vs Non-Best Seller 📉")
    avg_values = df.groupby('Best Seller')[['Price', 'Stars']].mean().round(2)
    avg_values.index = ['Non-Best Seller', 'Best Seller']
    st.dataframe(avg_values)

    fig = go.Figure(data=[
        go.Bar(x=avg_values.index, y=avg_values['Price'], name='Price', marker_color='#FF8C94',
              text=avg_values['Price'], textposition='auto', textfont=dict(color='black')),
        go.Bar(x=avg_values.index, y=avg_values['Stars'], name='Stars', marker_color='#DCA7F8',
              text=avg_values['Stars'], textposition='auto', textfont=dict(color='black'))
    ])
    fig.update_layout(
        title='Best Sellers vs Regular Products Comparison 📊',
        barmode='group',
        xaxis_title='Product Type 🛍',
        yaxis_title='Average Value 💵',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black')
    )
    st.plotly_chart(fig)
    
    # Sunburst Chart: Best Sellers by Category
    st.header("Best Sellers by Category (Interactive Sunburst Chart)")
    best_sellers_cat = df[df['Best Seller'] == 1]['Category'].value_counts().reset_index()
    best_sellers_cat.columns = ['Category', 'Count']
    color_map = {
        'Face': '#FFB6C1',
        'Lips': '#FF69B4',
        'Eyes': '#DB7093',
        'Hair Tools': '#FFA6C9',
        'Hair Care': '#FFC0CB',
        'Tools & Others': '#F4C2C2'}
    fig = px.sunburst(
        best_sellers_cat,
        path=['Category'],
        values='Count',
        color='Category',
        color_discrete_map=color_map,
        title='<b>Best Sellers by Category</b>'
    )
    fig.update_traces(
        marker=dict(line=dict(color='white', width=1)),
        hovertemplate='<b>%{label}</b><br>Best Sellers: %{value}<extra></extra>',
        textinfo='label+percent entry',
        textfont=dict(color='black')
    )
    fig.update_layout(
        paper_bgcolor='white',
        height=600,
        width=800,
        title_font=dict(size=18, color='black')
    )
    st.plotly_chart(fig)

    # Product Distribution by Category
    st.header("Product Distribution by Category 📊")
    plt.figure(figsize=(8,6))
    ax = sns.countplot(x='Category', data=df, order=df['Category'].value_counts().index, hue='Category',
                      palette=['#FFB6C1', '#FF69B4', '#FF1493', '#DB7093', '#FFC0CB', '#FF85C7'], legend=False)
    ax.set_facecolor('white')
    plt.gcf().set_facecolor('white')
    for spine in ax.spines.values():
        spine.set_linestyle(':')
        spine.set_color('#DB7093')
    heart = plt.Text(0.5, 0.5, '❤', fontsize=100, color='pink', alpha=0.1, ha='center', va='center', transform=ax.transAxes)
    ax.add_artist(heart)
    plt.xticks(rotation=45, ha='right', color='black')
    plt.yticks(color='black')
    plt.title('Product Distribution by Category', fontsize=12, pad=20, color='black', fontweight='bold')
    plt.xlabel('Category', color='black')
    plt.ylabel('Count', color='black')
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width()/2., p.get_height()), 
                    ha='center', va='center', xytext=(0, 5), 
                    textcoords='offset points', color='black', fontsize=9)
    plt.tight_layout()
    st.pyplot(plt)
    
    # Treemap: Product Distribution by Category and Subcategory
    st.header("Product Distribution by Category and Subcategory")
    fig = px.treemap(
        df,
        path=['Category', 'Subcategory'],
        title='Product Distribution by Category and Subcategory',
        color='Category',
        color_discrete_map=color_map
    )
    fig.update_layout(
        paper_bgcolor='white',
        height=600,
        width=800,
        font=dict(color='black')
    )
    fig.update_traces(
        textfont=dict(color='black')
    )
    st.plotly_chart(fig)

    # Price Distribution
    st.header("Price Distribution 💸")
    fig1, ax1 = plt.subplots()
    sns.histplot(df['Price'], bins=20, kde=True, ax=ax1, color='hotpink')
    ax1.set_title('Price Distribution 💵', color='black')
    ax1.set_xlabel('Price', color='black')
    ax1.set_ylabel('Count', color='black')
    ax1.tick_params(colors='black')
    st.pyplot(fig1)

    # Rating Distribution
    st.header("Rating Distribution")
    fig2, ax2 = plt.subplots()
    sns.histplot(df['Stars'], bins=10, kde=True, ax=ax2, color='hotpink')
    ax2.set_title('Rating Distribution ⭐', color='black')
    ax2.set_xlabel('Stars', color='black')
    ax2.set_ylabel('Count', color='black')
    ax2.tick_params(colors='black')
    st.pyplot(fig2)

    # Word Cloud
    st.header("Common Words in Product Names")
    text = ' '.join(df['Name'].dropna().tolist())
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='pink',
        contour_color='black'
    ).generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Common Words in Product Names', fontsize=16, color='black')
    plt.tight_layout()
    st.pyplot(plt)

    # Top 10 Rated Products
    st.header("Top 10 Rated Products")
    top_rated = df[df['Stars'] >= 4.5].sort_values(by=['Stars', 'Price'], ascending=[False, True]).head(10)
    plt.figure(figsize=(12, 8))
    girly_shades = [
        '#D36C6C',  # Dusty rose
        '#C97A9E',  # Blush mauve
        '#B36A5E',  # Terracotta pink
        '#A55D79',  # Rosewood
        '#955D85',  # Mauve
        '#B96B82',  # Soft berry
        '#A0527D',  # Plum pink
        '#C48291',  # Warm pink
        '#D08795',  # Faded red
        '#E6A6B0'   # Rose quartz
    ]
    bars = plt.barh(
        top_rated['Name'].str.wrap(30),
        top_rated['Stars'],
        color=girly_shades[:len(top_rated)],
        height=0.7)
    plt.title('Top 10 Highest Rated Products (4.5+ Stars)', pad=20, fontsize=14, fontweight='bold', color='black')
    plt.xlabel('Star Rating', color='black')
    plt.ylabel('Product Name', color='black')
    plt.xticks(color='black')
    plt.yticks(color='black')
    plt.xlim(4.4, 5.1)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.2)
    for bar, price, category in zip(bars, top_rated['Price'], top_rated['Category']):
        width = bar.get_width()
        plt.text(
            width - 0.05,
            bar.get_y() + bar.get_height()/2,
            f"{width:.1f} ★ | ${price} | {category}",
            va='center',
            ha='right',
            color='black',
            fontweight='bold')
    plt.tight_layout()
    st.pyplot(plt)

# -------------------- TAB 3: COLLECTIONS ANALYSIS --------------------
with tab3:
    # Bubble Chart: Average Price per Collection
    st.header("Average Price per Collection 💸")
    collection_patterns = [
        r'Adventure\s*Time',
        r'Harry\s*Potter\s*\|\s*SHEGLAM\s*2\.0',
        r'Harley\s*Quinn',
        r'Rick\s*and\s*Morty',
        r'Crimson\s*Butterfly',
        r'Hello\s*Kitty\s*\|\s*SHEGLAM',
        r'The\s*Powerpuff\s*Girls',
        r'Ember\s*Rose',
        r'Cosmic\s*Come\s*Up',
        r'Harry\s*Potter\s*\|\s*SHEGLAM\s*1\.0',
        r'Chroma\s*Zone\s*2\.0',
        r'Care\s*Bears',
        r'Corpse\s*Bride',
        r'Marilyn\s*Monroe',
        r'Frida\s*Kahlo',
        r'Willy\s*Wonka'
    ]

    combined_pattern = re.compile('|'.join(collection_patterns), re.IGNORECASE)
    df['collections'] = df['Name'].str.extract(f"({combined_pattern.pattern})", flags=re.IGNORECASE)
    collections_df = df.dropna(subset=['collections'])

    avg_price = (collections_df.groupby('collections')['Price']
                 .mean()
                 .round(2)
                 .sort_values(ascending=False)
                 .reset_index())

    fig = go.Figure()
    for _, row in avg_price.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['collections']],
            y=[row['Price']],
            mode='markers+text',
            marker=dict(size=row['Price'] * 3, color='pink', opacity=0.8),
            text=[f"${row['Price']}"],
            textposition='middle center',
            textfont=dict(color='black', size=12),
            showlegend=False
        ))

    fig.update_layout(
        title='Average Price by Collection',
        yaxis=dict(title='Average Price (USD)', title_font=dict(color='black')),
        xaxis=dict(title=None, tickfont=dict(color='black')),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black')
    )
    st.plotly_chart(fig)
    
    # Bar chart comparing total products and best sellers in each collection
    st.header("Products vs Best Sellers by Collection")
    summary = collections_df.groupby('collections')['Best Seller'].agg(
        Total='count',
        Best='sum'
    ).reset_index()
    
    fig = go.Figure(data=[
        go.Bar(
            x=summary['collections'],
            y=summary['Total'],
            name='Total Products',
            marker_color='#FFB6C1',
            text=summary['Total'],
            textposition='outside',
            textfont=dict(color='black')
        ),
        go.Bar(
            x=summary['collections'],
            y=summary['Best'],
            name='Best Sellers',
            marker_color='#9370DB',
            text=summary['Best'],
            textposition='outside',
            textfont=dict(color='black')
        )])
    
    fig.update_layout(
        title="Total vs Best Sellers by Collection",
        barmode='group',
        xaxis_title='Collection',
        yaxis_title='Count',
        xaxis=dict(tickfont=dict(color='black')),
        yaxis=dict(title_font=dict(color='black')),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black'),
        height=500,
        margin=dict(t=50, b=50)
    )
    st.plotly_chart(fig)