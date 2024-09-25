import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

const app = express();
const client = redis.createClient();

const getItemById = (id) => {
  return listProducts.find(product => product.id === id);
}

const reserveStockById = (itemId, stock) => {
  client.set(`item.${itemId}`, stock);
}

const getCurrentReservedStockById = async (itemId) => {
  const getAsync = promisify(client.get).bind(client);
  const reply = await getAsync(`item.${itemId}`);
  return reply;
}

app.get('/list_products', (req, res) => {
  const products = listProducts.map(product => ({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
  }));
  res.json(products);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = req.params.itemId;
  const product = getItemById(Number(itemId, 10));
  if (!product) {
    return res.json({ status: 'Product not found' });
  }

  const currentQuantity = await getCurrentReservedStockById(itemId);
  res.json({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
    currentQuantity: currentQuantity === null ? product.stock : Number(currentQuantity),
  });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = req.params.itemId;
  const product = getItemById(Number(itemId, 10));
  if (!product) {
    return res.json({ status: 'Product not found' });
  }

  let currentQuantity = await getCurrentReservedStockById(itemId);
  currentQuantity = currentQuantity === null ? product.stock : currentQuantity;

  if (currentQuantity <= 0) {
    return res.json({ 
      status: 'Not enough stock available',
      itemId: itemId
    });
  } else {
    const newQuantity = currentQuantity - 1;
    reserveStockById(itemId, newQuantity);
    return res.json({
      status: 'Reservation confirmed',
      itemId: itemId
    });
  }
})

app.listen(1245, () => {
  console.log('Server listening on port 1245');
});
