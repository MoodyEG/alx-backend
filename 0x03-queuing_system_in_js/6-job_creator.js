import kue from 'kue';

const queue = kue.createQueue();

const jobData = {
  phoneNumber: '888444',
  message: 'Stands for',
};

const job = queue.createJob('push_notification_code', jobData)
  .save((err) => {
    if (!err) {
      console.log(`Notification job created: ${job.id}`);
    }
  })
  .on('complete', () => {
    console.log('Notification job completed');
  })
  .on('failed', (err) => {
    console.log('Notification job failed');
  });
