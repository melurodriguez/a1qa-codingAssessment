# Store Inventory & Order Management System

A modular, Object-Oriented Programming (OOP) Python application designed to manage store inventory, validate product constraints, process customer orders with tiered volume discounts, and persist inventory state to disk using JSON serialization.

---

## Features

- **Encapsulated Product Model**:
  - Secure state management using properties and setters.
  - Strict validation rules: Price must be strictly greater than `0` (`price > 0`) and stock cannot be negative (`stockQuantity >= 0`).
  - Clear string representation for easy inspection.

- **Inventory Manager**:
  - Add and remove products by name (case-insensitive search).
  - Search products by category.
  - List current stock with structured formatting.

- **Order Processing & Business Rules**:
  - Automatic stock verification before completing an order.
  - Tiered subtotal volume discounts:
    - **$\ge \$500$**: 15% discount
    - **$\$200 - \$499.99$**: 10% discount
    - **$\$100 - \$199.99$**: 5% discount
    - **$<\$100$**: 0% discount
  - Detailed order summaries including original pricing, applied discounts, and final totals.

- **Data Persistence**:
  - Save current inventory state to JSON files (`saveInventoryToFile`).
  - Reconstruct active `StoreInventory` instances from JSON disk files (`loadInventoryFromFile`).

---

## Project Structure

```text
.
├── main.py              # Main application logic and demonstration workflow
├── README.md            # Project documentation
├── .gitignore          # Version control exclusion rules
└── inventory_data.json  # Generated dynamically during file persistence demo
```

---

## Requirements

- **Python 3.8+** (Uses standard library modules `json` and `os`; no external dependencies required).

---

## Getting Started

### 1. Clone the Repository
```bash
git clone <repository-url>
cd assessment
```

### 2. Set Up a Virtual Environment (Optional)
```bash
# On Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# On Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Run the Demonstration
Execute the entry script to verify object creation, error handling, order creation, and serialization workflow:

```bash
python main.py
```

---

## Code Example

```python
from main import ProductModel, StoreInventory, createOrder, saveInventoryToFile

# Create inventory and add items
inventory = StoreInventory()
laptop = ProductModel(name="Laptop", category="Electronics", price=999.99, stock_quantity=5)
inventory.addProduct(laptop)

# Process an order (15% discount applied for subtotal >= $500)
order_summary = createOrder(inventory, product_name="Laptop", quantity=1)
print(order_summary)

# Persist inventory to disk
saveInventoryToFile(inventory, "inventory.json")
```

---

## License

This project is open source and available under the [MIT License](LICENSE).