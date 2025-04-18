class Product:

def _init_(self, product_id, name, price, description, category, brand, image_path, stock_quantity, sale_price=None, rating=0):

self.product_id = product_id self.name = name
self.price = price

self.sale_price = sale_price if sale_price else price self.description = description
self.category = category
 
self.brand = brand self.image_path = image_path
self.stock_quantity = stock_quantity self.reviews = []
self.rating = rating



def add_review(self, rating, comment): self.reviews.append({"Rating": rating, "Comment": comment}) self.update_rating()


def update_rating(self): if self.reviews:
self.rating = sum([r["Rating"] for r in self.reviews]) / len(self.reviews)



def update_stock(self, quantity): self.stock_quantity -= quantity


def to_dict(self): return {
"Product ID": self.product_id, "Name": self.name,
"Price": self.price,

"Sale Price": self.sale_price,
"Description": self.description, "Category": self.category,
 
"Brand": self.brand, "Stock": self.stock_quantity, "Rating": self.rating, "Image": self.image_path
}



class User:

def _init_(self, username, password, email, address): self.username = username
self.password = password self.email = email self.address = address self.orders = [] self.wishlist = [] self.profile_picture = None


def update_profile(self, password, email, address, profile_picture=None): self.password = password
self.email = email self.address = address if profile_picture:
self.profile_picture = profile_picture


def add_order(self, order): self.orders.append(order)
 


def add_to_wishlist(self, product): if product not in self.wishlist:
self.wishlist.append(product) return True
return False



def remove_from_wishlist(self, product): if product in self.wishlist:
self.wishlist.remove(product) return True
return False



class Order:

def _init_(self, user, products, status="Pending"): self.user = user
self.products = products self.status = status
self.order_id = random.randint(1000, 9999) self.order_date = datetime.now()
self.total_price = sum([product.sale_price for product in products])



def update_status(self, status): self.status = status
 
def order_details(self): return {
"Order ID": self.order_id, "User": self.user.username,
"Products": [product.name for product in self.products], "Total Price": self.total_price,
"Status": self.status,
"Date": self.order_date.strftime("%Y-%m-%d %H:%M:%S")

}



Initialize Data


# Create images directory if it doesn't exist if not os.path.exists("images"):
os.makedirs("images")



# Initialize sample data

if "users" not in st.session_state: st.session_state.users = {
"admin": User("admin", "admin123", "admin@example.com", "123 Admin St")

}



if "products" not in st.session_state: st.session_state.products = [
Product(1, "Wireless Headphones", 99.99, "Noise-cancelling wireless headphones",
 
"Electronics", "SoundMaster", "images/headphones.jpg", 50, 79.99), Product(2, "Smart Watch", 199.99, "Fitness tracking and notifications",
"Electronics", "TechGear", "images/smartwatch.jpg", 30, 149.99),

Product(3, "Backpack", 49.99, "Durable laptop backpack with USB charging port", "Accessories", "UrbanGear", "images/backpack.jpg", 100)
]



Session Management


if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "cart" not in st.session_state: st.session_state.cart = []
if "language" not in st.session_state: st.session_state.language = "en"


Authentication


def login():

st.title("Login to E-Commerce Platform") username = st.text_input("Username")
password = st.text_input("Password", type="password")
 
if st.button("Login"):

if username in st.session_state.users and st.session_state.users[username].password == password: st.session_state.logged_in = True
st.session_state.username = username st.success("Logged in successfully!") st.experimental_rerun()
else:

st.error("Invalid credentials")



def register(): st.title("Register")
username = st.text_input("New Username")

password = st.text_input("New Password", type="password") email = st.text_input("Email")
address = st.text_input("Address")



if st.button("Register"):

if username in st.session_state.users: st.error("Username already exists")
elif not username or not password or not email or not address: st.error("Please fill all fields")
else:

st.session_state.users[username] = User(username, password, email, address) st.success("Registration successful! You can now log in.")
 
Product Display


def filter_and_sort_products():

categories = list(set([p.category for p in st.session_state.products])) brands = list(set([p.brand for p in st.session_state.products]))


col1, col2 = st.sidebar.columns(2) with col1:
category_filter = st.selectbox("Filter by Category", ["All"] + categories) with col2:
brand_filter = st.selectbox("Filter by Brand", ["All"] + brands)



sort_option = st.sidebar.selectbox("Sort by",

["Default", "Price Low-High", "Price High-Low", "Rating", "Newest"])



filtered = st.session_state.products.copy()



if category_filter != "All":

filtered = [p for p in filtered if p.category == category_filter] if brand_filter != "All":
filtered = [p for p in filtered if p.brand == brand_filter]



if sort_option == "Price Low-High": filtered.sort(key=lambda x: x.sale_price)
elif sort_option == "Price High-Low":
 
filtered.sort(key=lambda x: x.sale_price, reverse=True) elif sort_option == "Rating":
filtered.sort(key=lambda x: x.rating, reverse=True) elif sort_option == "Newest":
filtered.sort(key=lambda x: x.product_id, reverse=True)



return filtered



def show_products(filtered_products): for product in filtered_products:
col1, col2, col3 = st.columns([1, 3, 1]) with col1:
try:
if os.path.exists(product.image_path): st.image(product.image_path, width=120)
else:

st.image("images/default.png", width=120) except:
st.image("images/default.png", width=120)



with col2: st.subheader(product.name)
st.write(f"*Price:* ${product.price:.2f}") if product.sale_price < product.price:
 
st.write(f"*Sale	Price:*	${product.sale_price:.2f}	(Save	${product.price	- product.sale_price:.2f})")

st.write(f"*Category:* {product.category}") st.write(f"*Brand:* {product.brand}")
st.write(f"*Rating:* {'★2' * int(round(product.rating))} ({product.rating:.1f}/5)") st.write(product.description)
st.write(f"*Stock:* {product.stock_quantity}")



with col3:

if st.button(f"Add to Cart", key=f"cart_{product.product_id}"): if product.stock_quantity > 0:
st.session_state.cart.append(product) product.update_stock(1)
st.success(f"Added {product.name} to cart!") else:
st.error("Out of stock")



user = st.session_state.users.get(st.session_state.username) if user:
if product in user.wishlist:

if st.button("❤ Remove Wishlist", key=f"remove_wish_{product.product_id}"): user.remove_from_wishlist(product)
st.experimental_rerun()

else:

if st.button("♡ Add Wishlist", key=f"add_wish_{product.product_id}"):
 
user.add_to_wishlist(product) st.experimental_rerun()


st.write("---")



Cart and Checkout


def view_cart():

st.title("Your Shopping Cart") if not st.session_state.cart:
st.write("Your cart is empty") return

total = 0

for i, item in enumerate(st.session_state.cart): col1, col2, col3 = st.columns([1, 3, 1]) with col1:
try:

if os.path.exists(item.image_path): st.image(item.image_path, width=80)
else:

st.image("images/default.png", width=80) except:
st.image("images/default.png", width=80)
 
with col2: st.write(f"{item.name}")
st.write(f"Price: ${item.sale_price:.2f}") st.write(f"Brand: {item.brand}")


with col3:

if st.button(f"Remove", key=f"remove_{i}"): st.session_state.cart.pop(i) item.stock_quantity += 1 st.experimental_rerun()


total += item.sale_price st.write("---")


st.write(f"### Total: ${total:.2f}")



if st.button("Proceed to Checkout"):

user = st.session_state.users[st.session_state.username] order = Order(user, st.session_state.cart.copy()) user.add_order(order)
st.session_state.cart.clear()

st.success(f"Order placed successfully! Your Order ID: {order.order_id}") st.balloons()
 
Profile Management


def update_profile(): st.title("Your Profile")
user = st.session_state.users[st.session_state.username]



with st.form("profile_form"):

new_password = st.text_input("Password", type="password", value=user.password) new_email = st.text_input("Email", value=user.email)
new_address = st.text_area("Address", value=user.address)

new_pic = st.file_uploader("Profile Picture", type=["png", "jpg", "jpeg"])



if st.form_submit_button("Update Profile"): user.update_profile(new_password, new_email, new_address, new_pic) st.success("Profile updated successfully!")


Order History


def view_order_history(): st.title("Your Order History")
user = st.session_state.users[st.session_state.username]



if not user.orders:

st.write("You haven't placed any orders yet") return
 


for order in user.orders:

with st.expander(f"Order #{order.order_id} - {order.status} - ${order.total_price:.2f}"): st.write(f"*Date:* {order.order_date.strftime('%Y-%m-%d %H:%M:%S')}") st.write(f"*Status:* {order.status}")
st.write("*Products:*")

for product in order.products:

st.write(f"- {product.name} (${product.sale_price:.2f})") st.write(f"*Total:* ${order.total_price:.2f}")


Wishlist


def view_wishlist(): st.title("Your Wishlist")
user = st.session_state.users[st.session_state.username]



if not user.wishlist:

st.write("Your wishlist is empty") return


for product in user.wishlist:

col1, col2, col3 = st.columns([1, 3, 1]) with col1:
try:

if os.path.exists(product.image_path):
 
st.image(product.image_path, width=80) else:
st.image("images/default.png", width=80) except:
st.image("images/default.png", width=80)



with col2: st.write(f"{product.name}")
st.write(f"Price: ${product.sale_price:.2f}") st.write(f"Brand: {product.brand}")


with col3:

if st.button("Remove", key=f"wish_remove_{product.product_id}"): user.remove_from_wishlist(product)
st.experimental_rerun()



if st.button("Add to Cart", key=f"wish_cart_{product.product_id}"): if product.stock_quantity > 0:
st.session_state.cart.append(product) product.update_stock(1)
st.success(f"Added {product.name} to cart!") else:
st.error("Out of stock")



st.write("---")
 



Admin Panel


def admin_panel(): st.title("Admin Dashboard")
if st.session_state.username != "admin":

st.error("You need to be an admin to access this page.") return


st.subheader("Manage Products")

action = st.radio("Select Action", ["Add Product", "Update Product", "Delete Product", "View All Products"])



if action == "Add Product": add_product_form()
elif action == "Update Product": update_product_form()
elif action == "Delete Product": delete_product_form()
elif action == "View All Products": view_all_products()

def add_product_form():

with st.form("add_product"):
 
name = st.text_input("Product Name")

price = st.number_input("Price", min_value=0.01, value=1.0)

sale_price = st.number_input("Sale Price (optional)", min_value=0.01, value=price)

category = st.selectbox("Category", ["Electronics", "Accessories", "Home Office", "Fashion"]) brand = st.text_input("Brand")
description = st.text_area("Description")

stock = st.number_input("Stock Quantity", min_value=0, value=1) image = st.file_uploader("Product Image", type=["png", "jpg", "jpeg"])


if st.form_submit_button("Add Product"):

if not name or not brand or not description: st.error("Please fill all required fields")
else:

product_id = max([p.product_id for p in st.session_state.products], default=0) + 1

image_path = f"images/{name.replace(' ', '_').lower()}.png" if image else "images/default.png"



if image:

with open(image_path, "wb") as f: f.write(image.getbuffer())


new_product = Product(

product_id, name, price, description, category, brand, image_path, stock, sale_price if sale_price != price else None
)

st.session_state.products.append(new_product)
 
st.success(f"Product '{name}' added successfully!")



def update_product_form(): product_id = st.selectbox(
"Select Product to Update",

options=[p.product_id for p in st.session_state.products],

format_func=lambda x: f"{x}: {next(p.name for p in st.session_state.products if p.product_id == x)}"

)



product = next(p for p in st.session_state.products if p.product_id == product_id)



with st.form("update_product"):

name = st.text_input("Product Name", value=product.name)

price = st.number_input("Price", min_value=0.01, value=product.price)

sale_price = st.number_input("Sale Price", min_value=0.01, value=product.sale_price) category = st.selectbox(
"Category",

["Electronics", "Accessories", "Home Office", "Fashion"],

index=["Electronics", "Accessories", "Home Office", "Fashion"].index(product.category)

)

brand = st.text_input("Brand", value=product.brand)

description = st.text_area("Description", value=product.description)

stock = st.number_input("Stock Quantity", min_value=0, value=product.stock_quantity) image = st.file_uploader("Update Product Image", type=["png", "jpg", "jpeg"])
 
if st.form_submit_button("Update Product"): product.name = name
product.price = price

product.sale_price = sale_price if sale_price != price else price product.category = category
product.brand = brand product.description = description product.stock_quantity = stock


if image:

image_path = f"images/{name.replace(' ', '_').lower()}.png" with open(image_path, "wb") as f:
f.write(image.getbuffer()) product.image_path = image_path


st.success(f"Product '{name}' updated successfully!")



def delete_product_form(): product_id = st.selectbox(
"Select Product to Delete",

options=[p.product_id for p in st.session_state.products],

format_func=lambda x: f"{x}: {next(p.name for p in st.session_state.products if p.product_id == x)}"

)



if st.button("Delete Product", key="delete_product"):
 
st.session_state.products = [p for p in st.session_state.products if p.product_id != product_id] st.success("Product deleted successfully!")


def view_all_products(): st.subheader("All Products")
df = pd.DataFrame([p.to_dict() for p in st.session_state.products]) st.dataframe(df)


Main App


def main_app(): st.sidebar.title("Navigation") nav = st.sidebar.radio(
"Menu",

["Home", "Cart", "Wishlist", "Order History", "Profile", "Admin", "Logout"], index=0
)



st.sidebar.write(f"Logged in as: *{st.session_state.username}*")



if nav == "Home":

st.title("Welcome to Our E-Commerce Store") filtered_products = filter_and_sort_products() show_products(filtered_products)
elif nav == "Cart":
 
view_cart()

elif nav == "Wishlist": view_wishlist()
elif nav == "Order History": view_order_history()
elif nav == "Profile": update_profile()
elif nav == "Admin": admin_panel()
elif nav == "Logout": st.session_state.logged_in = False st.session_state.username = "" st.session_state.cart = [] st.success("Logged out successfully!") st.experimental_rerun()


App Entry


def main():

st.set_page_config(page_title="E-Commerce App", page_icon="˙ „", layout="wide")



if not st.session_state.logged_in:

page = st.sidebar.radio("Select Page", ["Login", "Register"]) if page == "Login":
login()
 
elif page == "Register": register()
else:

main_app()

if _name_ == "_main_": main()
