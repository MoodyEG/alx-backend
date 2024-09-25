import createPushNotificationsJobs from './8-job.js';
import kue from 'kue';
import { expect } from 'chai';
import sinon from 'sinon'


describe('createPushNotificationsJobs', () => {
  const logSpy = sinon.spy(console, 'log');
  const queue = kue.createQueue({ name: 'push_notification_code_test' });
  before(() => {
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.clear();
    logSpy.resetHistory();
  });

  after(() => {
    queue.testMode.exit();
  });

  it('should create a job for each notification', (done) => {
    expect(queue.testMode.jobs.length).to.equal(0);
    const list = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account'
      }
    ];

    createPushNotificationsJobs(list, queue);

    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].data).to.equal(list[0]);
    expect(queue.testMode.jobs[1].data).to.equal(list[1]);
    expect(logSpy.callCount).to.equal(2);
    expect(logSpy.getCall(0).args[0]).to.equal('Notification job created: 1');
    expect(logSpy.getCall(1).args[0]).to.equal('Notification job created: 2');
    done();
  });

  it('should display an error if jobs is not an array', () => {
    const list = {
      phoneNumber: '4153518780',
      message: 'This is the code 1234 to verify your account'
    };

    expect(() => createPushNotificationsJobs(list, queue)).to.throw('Jobs is not an array');
  });
});
