import { createClient } from 'redis';
import { promisify } from 'util';
import { createQueue } from 'kue';
import express from 'express';

const client = createClient();
const queue = createQueue();
const app = express();
const PORT = 1245;
const INITIAL_SEATS = 50;
let reservationEnabled = false;

const reserveSeat = (number) => client.SET('available_seats', number);

const getCurrentAvailableSeats = async () => {
  const seats = await promisify(client.GET).bind(client)('available_seats');
  return seats;
};

app.get('/available_seats', (_, res) => {
  getCurrentAvailableSeats()
    .then((result) => res.json({ numberOfAvailableSeats: result }));
});

app.get('/reserve_seat', (_, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }
  try {
    const job = queue.create('reserve_seat');
    
    job
      .on('complete', () => {
        console.log(`Seat reservation job ${job.id} completed`);
      })
      .on('failed', (err) => {
        console.log(`Seat reservation job ${job.id} failed:`,
		    err.message || err.toString());
      });
    job.save();
    res.json({ status: 'Reservation in process' });
  } catch {
    res.json({ status: 'Reservation failed' });
  }
});

app.get('/process', (_, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', (_, done) => {
    getCurrentAvailableSeats()
      .then((availableSeats) => {
        reservationEnabled = availableSeats <= 1 ? false : reservationEnabled;
        if (availableSeats >= 1) {
          reserveSeat(availableSeats - 1);
          done();
        } else {
          done(new Error('Not enough seats available'));
        }
      });
  });
});

app.listen(PORT, () => {
  reserveSeat(INITIAL_SEATS);
  reservationEnabled = true;
  console.log(`API available on localhost port ${PORT}`);
});

export default app;
