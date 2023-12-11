# %% [markdown]
# ## Part 1: Explore the Data
# 
# Import the data and use Pandas to learn more about the dataset.

# %%
import pandas as pd

df = pd.read_csv('Resources/client_dataset.csv')

df.head()

# %%
# View the column names in the data
df.columns

# %%
# Use the describe function to gather some basic statistics
df.describe()



# %%
# Use this space to do any additional research
# and familiarize yourself with the data.



# %%
# What three item categories had the most entries?
df['category'].value_counts().head(3)


# %%
# For the category with the most entries,
# which subcategory had the most entries?
category_with_most_entries=df['category'].value_counts().idxmax()

filtered_df = df.loc[df['category'] == category_with_most_entries]
subcategory_counts = filtered_df['subcategory'].value_counts().head(1)
print(subcategory_counts)




# %%
# Which five clients had the most entries in the data?
df['client_id'].value_counts().head(5)



# %%
# Store the client ids of those top 5 clients in a list. #the index stores it as a variable separate from current file
top_5_list=list(df['client_id'].value_counts().head(5).index)
print(top_5_list)


# %%
# How many total units (the 'qty' column) did the
# client with the most entries order order?
df['client_id'].value_counts().head(1)
client_with_most_entries = df['client_id'].value_counts().head(1)
#trying to come up with formula so that 33615 is not hard coded in

total_units_df = df.loc[df['client_id'] == 33615, 'qty'].sum()
print(total_units_df)

# %% [markdown]
# ## Part 2: Transform the Data
# Do we know that this client spent the more money than client 66037? If not, how would we find out? Transform the data using the steps below to prepare it for analysis.

# %%
# Create a column that calculates the 
# subtotal for each line using the unit_price
# and the qty ## it is not apply, just math
df['line_subtotal'] = df['qty'] * df['unit_price']
df[['unit_price','qty','line_subtotal']].head()

# %%
# Create a column for shipping price.
# Assume a shipping price of $7 per pound 
# for orders over 50 pounds and
# $10 per pound for items 50 pounds or under.

#Calculate total_weight
total_weight = df['unit_weight'] * df['qty']
df['total_weight'] = total_weight

def shipping_rate_lb(weight):
    if weight > 50:  
        return weight * 7.00  
    return weight * 10.00   

df['shipping_price'] = df['total_weight'].apply(shipping_rate_lb)
df[['unit_price', 'unit_weight', 'qty', 'total_weight', 'shipping_price']].head(3)



# %%
# Create a column for the total price
# using the subtotal and the shipping price
# along with a sales tax of 9.25%
sales_tax_rate = 1.0925
df['line_price'] = (df['line_subtotal'] + df['shipping_price']) * sales_tax_rate
df['line_price'] = df['line_price'].round(2)
df[['line_subtotal', 'shipping_price','line_price']].head(3)


# %%
# Create a column for the cost
# of each line using unit cost, qty, and
# shipping price (assume the shipping cost
# is exactly what is charged to the client).

df['line_cost'] = df['unit_cost'] * df['qty'] + df['shipping_price']
df[['line_cost', 'unit_cost', 'qty','shipping_price',]].head(3)





# %%
# Create a column for the profit of
# each line using line cost and line price
df['line_profit'] = df['line_price'] - df['line_cost']
df[['line_profit', 'line_price', 'line_cost']].head(3)

# %%
df[['client_id','unit_price', 'unit_weight', 'qty', 'total_weight', 'shipping_price']].head(3)

# %% [markdown]
# ## Part 3: Confirm your work
# You have email receipts showing that the total prices for 3 orders. Confirm that your calculations match the receipts. Remember, each order has multiple lines.
# 
# Order ID 2742071 had a total price of \$152,811.89
# 
# Order ID 2173913 had a total price of \$162,388.71
# 
# Order ID 6128929 had a total price of \$923,441.25
# 

# %%
# Check your work using the totals above

def find_total_price(order_id):
    return df.loc[df['order_id']== order_id,'line_price'].sum()
order_ids = [2742071, 2173913, 6128929]

for order_id in order_ids:
    total_price_found = find_total_price(order_id)
    print(f"order {order_id} total: ${total_price_found:.2f}")



# %% [markdown]
# ## Part 4: Summarize and Analyze
# Use the new columns with confirmed values to find the following information.

# %%
# How much did each of the top 5 clients by quantity spend?

def find_total_price(client_id):
    return df.loc[df['client_id'] == client_id, 'line_price'].sum()
for client_id in top_5_list:
    total_spent = find_total_price(client_id)
    print(f"{client_id}: ${total_spent:.2f}")

# %%
# Create a summary DataFrame showing the totals for the
# for the top 5 clients with the following information:
# 1.) total units purchased, ttl_units_purch
# 2.) total shipping price, ttl_ship_price
# 3.) total revenue, and ttl_rev
# 4.) need to also include line cost
# 5.) total profit. ttl_profit
# --> Sort by total profit.

def ttl_units_purch(client_id): 
    return df.loc[df['client_id'] == client_id, 'qty'].sum()

def ttl_ship_price(client_id):
    return df.loc[df['client_id'] == client_id, 'shipping_price'].sum()

def ttl_rev(client_id):
    return df.loc[df['client_id'] == client_id, 'line_price'].sum()

def ttl_cost(client_id):
    return df.loc[df['client_id'] == client_id, 'line_cost'].sum()

def ttl_profit(client_id):
    return df.loc[df['client_id'] == client_id, 'line_profit'].sum()

summary_client_data = []
for client_id in top_5_list:
    ttl_units_purch_sum = ttl_units_purch(client_id)
    ttl_ship_price_sum = ttl_ship_price(client_id)
    ttl_rev_sum = ttl_rev(client_id)
    ttl_cost_sum = ttl_cost(client_id)
    ttl_profit_sum = ttl_profit(client_id)
    
    summary_dict = {
        'client_id': client_id,
        'qty':ttl_units_purch_sum,
        'shipping_price': ttl_ship_price_sum,
        'line_price': ttl_rev_sum,
        'line_cost': ttl_cost_sum,
        'line_profit': ttl_profit_sum,
    }
    summary_client_data.append(summary_dict)
summary_df = pd.DataFrame(summary_client_data)

summary_df = summary_df.sort_values(by="line_profit", ascending = False)
summary_df



# %%
# Format the data and rename the columns
# to names suitable for presentation.
# Currency should be in millions of dollars.
summary_client_data = []
for client_id in top_5_list:
    ttl_units_purch_sum = ttl_units_purch(client_id)
    ttl_ship_price_sum = ttl_ship_price(client_id)
    ttl_rev_sum = ttl_rev(client_id)
    ttl_cost_sum = ttl_cost(client_id)
    ttl_profit_sum = ttl_profit(client_id)    
    summary_dict = {
        'Client': client_id,
        'Units':ttl_units_purch_sum,
        'Shipping': ttl_ship_price_sum,
        'Total Revenue': ttl_rev_sum,
        'Total Cost': ttl_cost_sum,
        'Total Profit': ttl_profit_sum,
    }
    summary_client_data.append(summary_dict)

summary_df = pd.DataFrame(summary_client_data)

columns_to_reformat = ['Shipping', 'Total Revenue', 'Total Cost', 'Total Profit']
summary_df_reformat = summary_df.copy()


#Apply the formatting to the specific columns
summary_df_reformat[columns_to_reformat] = summary_df_reformat[columns_to_reformat].apply(lambda x: x.apply(lambda val: f'${val / 1_000_000:.2f}M'))\
# summary_df_display[columns_to_convert] = summary_df_display[columns_to_convert].apply

## Sort the updated data by "Total Profit" form highest to lowest
summary_df_reformat = summary_df_reformat.sort_values(by="Total Profit", ascending = False)
summary_df_reformat

# %%
#Write a brief 2-3 summary of your findings
"""
We explored and analyzed data from the csv file 'client_dataset'. We viewed the columns,
used the describe method to see basic stats on the data set.

We also identified the top 5 clients based on quantity of units and total profits. I found
the second to the last quesiton to be particularly challenging.  I don't know why, particularly.
I knew what I wanted to do in theory, but found it difficult to code.  I did have help from a couple of my 
classmates, with the help of Bing Chat, and chatgpt.

"""


