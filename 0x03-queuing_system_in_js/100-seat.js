import redis from 'redis';
import { promisify } from 'util';
import express from 'express';
import kue from 'kue';

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const app = express();
const queue = kue.createQueue();
let reservationEnabled = true;

client.set('available_seats', 50);

// Requirements:

// Make sure to use promisify with Redis
// Make sure to use the await/async keyword to get the value from Redis
// Make sure the format returned by the web application is always JSON and not text
// Make sure that only the allowed amount of seats can be reserved
// Make sure that the main route is displaying the right number of seats

const reserveSeat = (number) => {
  client.set('available_seats', number);
  if (number === 0) reservationEnabled = false;
}

const getCurrentAvailableSeats = async () => {
  const reply = await getAsync('available_seats');
  return Number(reply);
}

app.get('/available_seats', async (req, res) => {
  const currentSeats = String(await getCurrentAvailableSeats())
  res.json({"numberOfAvailableSeats":currentSeats});
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) return res.json({"status":"Reservation not available"});
  const currentSeats = await getCurrentAvailableSeats();
  if (currentSeats === 0) return res.json({"status":"Reservation not available"});
  const job = queue.createJob('reserve_seat', { currentSeats }).save((err) => {
    if (!err) {
      res.json({"status":"Reservation in process"});
    } else {
      res.json({"status":"Reservation failed"});
    }
  });
  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });
  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
  });
});

app.get('/process', async (req, res) => {
  res.json({"status":"Queue processing"});

  queue.process('reserve_seat', 1, async (job, done) => {
    const currentSeats = await getCurrentAvailableSeats();
    const newSeats = currentSeats - 1;
    if (newSeats < 0) {
      return done(new Error('Not enough seats available'));
    }
    reserveSeat(newSeats);
    if (newSeats === 0) {
      reservationEnabled = false;
    }
    done();
  });
})




app.listen(1245, () => {
  console.log('Server listening on port 1245');
});
