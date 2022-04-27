import queue
import threading
import time

bacc_A, bacc_B = 10000, 10000
total = bacc_B + bacc_A
totalTransactionsAToB1 = 30
totalTransactionsAToB2 = 30
totalTransactionsBToA1 = 100
totalTransactionsBToA2 = 100
lock = threading.Lock()


def transfer5(q, thread_no):
    global bacc_A, bacc_B
    while True:
        task = q.get()
        # time.sleep(2)
        if (bacc_A - 5) >= 0:
            if (bacc_A + bacc_B) != total:
                print("error in total balance")
            lock.acquire()
            bacc_A -= 5
            bacc_B += 5
            lock.release()
            q.task_done()
            print(f'Thread #{thread_no} transfer 5€ from A to B successfully with transactionId 5#{task}')
        else:
            print("transaction 5#" + str(task) + " of 5€ from A to B canceled because of no money in this account")
            print(total)
            q.task_done()



def transfer10(q, thread_no):
    global bacc_A, bacc_B
    while True:
        task = q.get()

        if (bacc_B - 10) >= 0:
            if (bacc_A + bacc_B) != total:
                print("error in total balance")
            lock.acquire()
            bacc_B -= 10
            bacc_A += 10
            lock.release()
            q.task_done()
            print(f'Thread #{thread_no} transfer 10€ from B to A successfully with transactionId 10#{task}')
        else:
            print("transaction 10#" + str(task) + " of 10€ from B to A canceled because of no money in this account")
            q.task_done()



def transfer20(q, thread_no):
    global bacc_A, bacc_B
    while True:
        task = q.get()
        # time.sleep(2)
        if (bacc_A - 20) >= 0:
            if (bacc_A + bacc_B) != total:
                print("error in total balance")
            lock.acquire()
            bacc_A -= 20
            bacc_B += 20
            lock.release()
            q.task_done()
            print(f'Thread #{thread_no} transfer 20€ from A to B successfully with transactionId 20#{task}')
        else:
            print("transaction 20#" + str(task) + " of 20€ from A to B canceled because of no money in this account")
            print(total)
            q.task_done()


def transfer40(q, thread_no):
    global bacc_A, bacc_B
    while True:
        task = q.get()

        if (bacc_B - 40) >= 0:
            if (bacc_A + bacc_B) != total:
                print("error in total balance")
            lock.acquire()
            bacc_B -= 40
            bacc_A += 40
            lock.release()
            q.task_done()
            print(f'Thread #{thread_no} transfer 40€ from B to A successfully with transactionId 40#{task}')
        else:
            print("transaction 40#" + str(task) + " of 40€ from B to A canceled because of no money in this account")
            q.task_done()


def main():
    q5 = queue.LifoQueue()
    q10 = queue.LifoQueue()
    q20 = queue.LifoQueue()
    q40 = queue.LifoQueue()

    worker1 = threading.Thread(target=transfer5, args=(q5, 1,), daemon=True)
    worker1.start()
    worker2 = threading.Thread(target=transfer10, args=(q10, 2,), daemon=True)
    worker2.start()
    worker3 = threading.Thread(target=transfer20, args=(q20, 3,), daemon=True)
    worker3.start()
    worker4 = threading.Thread(target=transfer40, args=(q40, 4,), daemon=True)
    worker4.start()

    for j in range(totalTransactionsAToB1):
        q5.put(j)

    for j in range(totalTransactionsBToA1):
        q10.put(j)

    for j in range(totalTransactionsAToB2):
        q20.put(j)

    for j in range(totalTransactionsBToA2):
        q40.put(j)

    q5.join()
    q10.join()
    q20.join()
    q40.join()


main()