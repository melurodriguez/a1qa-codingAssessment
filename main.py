import json
import os

class ProductModel:

    def __init__(self, name: str, category: str, price: float, stockQuantity: int):
        self.name= name
        self.category= category
        self.price= price
        self.stockQuantity= stockQuantity

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            raise ValueError(
                f"El precio debe ser estrictamente mayor a 0. Valor recibido: {value}"
            )
        self._price = float(value)

    @property
    def stock_quantity(self) -> int:
        return self.stockQuantity

    @stock_quantity.setter
    def stock_quantity(self, value: int):
        if value < 0:
            raise ValueError(
                f"El stock no puede ser menor a 0. Valor recibido: {value}"
            )
        self._stockQuantity = int(value)

    def to_dict(self) -> dict:
        """Convierte el producto a diccionario para facilitar la serialización JSON."""
        return {
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stockQuantity": self.stockQuantity,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Crea una instancia de Product a partir de un diccionario."""
        return cls(
            name=data["name"],
            category=data["category"],
            price=data["price"],
            stockQuantity=data["stockQuantity"],
        )

    def __str__(self) -> str:
        return f"{self.name} ({self.category}) - ${self.price:.2f} | Stock: {self.stockQuantity}"


class StoreInventory:

    def __init__(self):
        self.memory=[]

    def addProduct(self, product: ProductModel):
        self.memory.append(product)

    def deleteProduct(self, productName:str):
        prodName_lower= productName.strip().lower()
        for i, product in enumerate (self.memory):
            if product.name == prodName_lower:
                del self.memory[i]
                print (f"Product: {productName} has been safely deleted")
        print(f"Error: Product{productName} not found")

    def serachByCategory(self, category:str) -> list:
        category_lower=category.strip().lower()
        return [prod for prod in self.memory if category_lower == prod.category.lower()]


    def listInventory(self):
        if not self.memory:
            return "No products are available"
        return [prod for prod in self.memory]

    def searchByName(self, productName: str):
        prodName_lower= productName.strip().lower()
        for prod in self.memory:
            if prod.name.lower() == prodName_lower:
                return prod
        return None

    
def createOrder(inventory: StoreInventory, productName: str, quantity: int):
    existing_product= inventory.searchByName(productName)

    if existing_product is None:
        raise ValueError(f"Error: {productName} not found")
    if quantity <= 0:
        raise ValueError(f"Error: Invalid quantity amount {quantity}")
    
    if existing_product.stockQuantity < quantity:
        raise ValueError(f"Error: Not enough available stock for {productName}")

    existing_product.stockQuantity -= quantity

    subtotal= existing_product.price * quantity

    if (subtotal >= 500):
        discount=0.15
    elif (subtotal>=200):
        discount=0.1
    elif (subtotal>=100):
        discount=0.05
    else:
        discount=0

    order={
        "product": existing_product.name,
        "orderedQuantity": quantity,
        "unitPrice": existing_product.price,
        "appliedDiscount": f"{discount*100}%",
        "finalTotal": round(subtotal-(subtotal*discount), 2)
    }

    return order

def saveInventoryToFile(inventory: StoreInventory, path:str):
    data= [prod.to_dict() for prod in inventory.memory]

    with open (path, "w") as f:
        json.dump(data, f , indent=4)

def loadInventoryFromFile(path: str):
    inventory= StoreInventory()

    if not os.path.exists(path):
        return inventory
    
    with open (path, "r") as f:
        data= json.load(f)

    for item in data:
        inventory.addProduct(ProductModel.from_dict(item))
    return inventory


if __name__ == "__main__":
    print("=== 1. Creación e Inserción de Productos ===")
    inventory = StoreInventory()

    p1 = ProductModel("Laptop", "Electronics", 999.99, 5)
    p2 = ProductModel("Mouse", "Electronics", 25.00, 20)
    p3 = ProductModel("Desk Chair", "Furniture", 150.00, 10)

    inventory.addProduct(p1)
    inventory.addProduct(p2)
    inventory.addProduct(p3)

    inventory.listInventory()

    print("=== 2. Manejo de Casos Límite y Validaciones ===")
    try:
        print("Intentando crear producto con precio negativo (-10)...")
        p_invalid = ProductModel("Invalid Item", "Test", -10, 5)
    except ValueError as e:
        print(f"Excepción capturada correctamente: {e}")

    try:
        print("Intentando crear producto con stock negativo (-5)...")
        p_invalid_stock = ProductModel("Invalid Stock", "Test", 10.0, -5)
    except ValueError as e:
        print(f"Excepción capturada correctamente: {e}")

    print("\n=== 3. Procesamiento de Órdenes con Descuento ===")
    # Orden de 1 Laptop ($999.99 -> >= $500 aplica 15% de descuento)
    order1 = createOrder(inventory, "Laptop", 1)
    print("Resumen de Orden 1:", order1)

    # Orden de 8 sillas ($150 * 8 = $1200 -> >= $500 aplica 15% de descuento)
    order2 = createOrder(inventory, "Desk Chair", 2)
    print("Resumen de Orden 2 (1 Silla = $150 -> 5% desc):", order2)

    # Intentar ordenar más del stock disponible
    try:
        print("\nIntentando ordenar 10 Laptops cuando solo quedan 4...")
        createOrder(inventory, "Laptop", 10)
    except ValueError as e:
        print(f"Excepción capturada correctamente: {e}")

    inventory.listInventory()

    print("=== 4. Persistencia en Archivo ===")
    file_name = "inventory_data.json"
    print(f"Guardando inventario en '{file_name}'...")
    saveInventoryToFile(inventory, file_name)

    print("Cargando datos desde el archivo a un nuevo inventario...")
    restored_inventory = loadInventoryFromFile(file_name)
    restored_inventory.listInventory()

    # # Limpieza del archivo de prueba
    # if os.path.exists(file_name):
    #     os.remove(file_name)