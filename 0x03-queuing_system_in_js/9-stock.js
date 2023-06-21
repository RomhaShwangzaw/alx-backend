import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const listProducts = [
  {
    itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4,
  },
  {
    itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10,
  },
  {
    itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2,
  },
  {
    itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5,
  },
];

const getItemById = (id) => {
  for (const product of listProducts) {
    if (product.itemId === id) {
      return product;
    }
  }
};

const app = express();
const PORT = 1245;
const client = createClient();

const reserveStockById = (itemId, stock) => client.SET(`item.${itemId}`, stock);

const getCurrentReservedStockById = async (itemId) => {
  const stock = await promisify(client.GET).bind(client)(`item.${itemId}`);
  return stock;
};

app.get('/list_products', (_, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId(\\d+)', (req, res) => {
  const itemId = Number.parseInt(req.params.itemId);
  const product = getItemById(itemId);

  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }
  getCurrentReservedStockById(itemId)
    .then((result) => Number.parseInt(result || 0))
    .then((reservedStock) => {
      product.currentQuantity = product.initialAvailableQuantity - reservedStock;
      res.json(product);
    });
});

app.get('/reserve_product/:itemId', (req, res) => {
  const itemId = Number.parseInt(req.params.itemId);
  const product = getItemById(itemId);

  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }
  getCurrentReservedStockById(itemId)
    .then((result) => Number.parseInt(result || 0))
    .then((reservedStock) => {
      if (reservedStock >= product.initialAvailableQuantity) {
        res.json({ status: 'Not enough stock available', itemId });
        return;
      }
      reserveStockById(itemId, reservedStock + 1);
      product.currentQuantity -= 1;
      res.json({ status: 'Reservation confirmed', itemId });
    });
});

const resetProductsStock = () => {
  return Promise.all(
    listProducts.map(
      (item) => client.SET(`item.${item.itemId}`, 0),
    ),
  );
};

app.listen(PORT, () => {
  resetProductsStock()
    .then(() => {
      console.log(`API available on localhost port ${PORT}`);
    });
});

export default app;
