#!/usr/bin/env python3
# Need to use projectq backend
# simulaqron set backend projectq

import random
import string
import time
# Useful to avoid having "with ..." everywhere.
from contextlib import ExitStack
# Quantum library
from cqc.pythonLib import CQCConnection, qubit
# Create new network
# https://softwarequtech.github.io/SimulaQron/html/ConfNodes.html
from simulaqron.network import Network

def id_generator(max_nb=65):
    return random.randint(0, max_nb)

def pre_measure(node, q, anc, mes):
    """mes is either I, X, Y, or Z"""
    # Create ancilla
    if mes == "I":
        return None
    elif mes == "X":
        q.H()
        q.cnot(anc)
        q.H()
    elif mes == "Y":
        q.K()
        q.cnot(anc)
        q.K()
        # q.rot_X(-64) # Rotation -pi/2
    elif mes == "Z":
        q.cnot(anc)
    else:
        raise NameError("The measurement {} does not exist.".format(mes))
    

def measure(node, q1, q2, measurements):
    """measurements is a string, with:
    - first element in ['+', '-']
    - second and third letter in ['I', 'X', 'Y', 'Z']"""
    # Create ancilla
    anc = qubit(node)
    ### ____
    pre_measure(node, q1, anc, measurements[1])
    pre_measure(node, q2, anc, measurements[2])
    if measurements[0] == "-":
        anc.X()
    return anc.measure()

global_array_measurement = [
    [('+XI'), ('+XX'), ('+IX')],
    [('-XZ'), ('+YY'), ('-ZX')],
    [('+IZ'), ('+ZZ'), ('+ZI')]
]

def get_all_measurements_row(n_row):
    return global_array_measurement[n_row]

def get_all_measurements_col(n_col):
    return [ row[n_col] for row in global_array_measurement ]

class MagicSquare:
    def __init__(self, global_stack, session_id=None, debug=False):
        """Session_id must be an integer"""
        self.global_stack = global_stack
        self.debug = debug
        if session_id:
            self.appID = int(session_id)
        else:
            self.appID = id_generator()
        ## Name of parties
        self.alice_name = "Alice"
        self.bob_name = "Bob"
        self.network_name = "default"
        # self.appID = 42
        ## Create the contexts to connect to CQC
        print("The appId is {}".format(self.appID))
        self.cqc_alice = self.global_stack.enter_context(
            CQCConnection(self.alice_name,
                          network_name=self.network_name,
                          appID = self.appID,
                          conn_retry_time=1)
        )
        self.cqc_bob = self.global_stack.enter_context(
            CQCConnection(self.bob_name,
                          network_name=self.network_name,
                          appID = self.appID,
                          conn_retry_time=1)
        )
        # Create two EPR pairs
        self.q1_a = self.cqc_alice.createEPR(self.bob_name,
                                             remote_appID=self.appID)
        self.q1_b = self.cqc_bob.recvEPR()
        self.q2_a = self.cqc_alice.createEPR(self.bob_name,
                                             remote_appID=self.appID)
        self.q2_b = self.cqc_bob.recvEPR()

    def close(self):
        self.cqc_alice.close()
        self.cqc_bob.close()

    def log(self, message):
        if self.debug:
            print(message)

    def print_info(self):
        print("The session id is {}".format(self.session_id))
        
    def alice_measurement(self, n_row):
        # m0 = self.q1_a.measure()
        all_measurements = get_all_measurements_row(n_row)
        res = [ measure(self.cqc_alice, self.q1_a, self.q2_a, m)
                for m in all_measurements ]
        return res

    def bob_measurement(self, n_col):
        all_measurements = get_all_measurements_col(n_col)
        res = [ measure(self.cqc_bob, self.q1_b, self.q2_b, m)
                for m in all_measurements ]
        return res


def parallel_epr():
    with ExitStack() as global_stack:
        n_row = int(input("Which row do you want? [0,1,2]"))
        n_col = int(input("Which column do you want? [0,1,2]"))
        n_row2 = int(input("Which row do you want? [0,1,2]"))
        n_col2 = int(input("Which column do you want? [0,1,2]"))
        magic_square = MagicSquare(global_stack, debug=True)
        magic_square.print_info()
        magic_square2 = MagicSquare(global_stack, debug=True)
        magic_square2.print_info()
        ma = magic_square.alice_measurement(n_row)
        mb = magic_square.bob_measurement(n_col)
        ma2 = magic_square.alice_measurement(n_row)
        mb2 = magic_square.bob_measurement(n_col)
        print("Alice: {}".format(ma))
        print("Bob: {}".format(mb))
        print("Alice 2: {}".format(ma2))
        print("Bob 2: {}".format(mb2))
        print("--- First run:")
        if ma[n_col] == mb[n_row]:
            print("They have the same result :D")
        else:
            print("Grr...! They have different result :-(")
        if sum(ma) % 2 == 0:
            print("The parity on row is good! :D")
        else:
            print("The parity on row is BAD! :-(")
        if sum(mb) % 2 == 1:
            print("The parity on column is good! :D")
        else:
            print("The parity on column is BAD! :-(")
        print("--- Second run:")
        if ma2[n_col2] == mb2[n_row2]:
            print("They have the same result :D")
        else:
            print("Grr...! They have different result :-(")
        if sum(ma2) % 2 == 0:
            print("The parity on row is good! :D")
        else:
            print("The parity on row is BAD! :-(")
        if sum(mb2) % 2 == 1:
            print("The parity on column is good! :D")
        else:
            print("The parity on column is BAD! :-(")
        ## Optional, as it will be closed when ExitStack is closed
        magic_square.close()
        magic_square2.close()
            
def one_exec():
    with ExitStack() as global_stack:
        magic_square = MagicSquare(global_stack, debug=True)
        magic_square.print_info()
        n_row = int(input("Which row do you want? [0,1,2]"))
        n_col = int(input("Which column do you want? [0,1,2]"))
        ma = magic_square.alice_measurement(n_row)
        mb = magic_square.bob_measurement(n_col)
        print("Alice: {}".format(ma))
        print("Bob: {}".format(mb))
        if ma[n_col] == mb[n_row]:
            print("They have the same result :D")
        else:
            print("Grr...! They have different result :-(")
        if sum(ma) % 2 == 0:
            print("The parity on row is good! :D")
        else:
            print("The parity on row is BAD! :-(")
        if sum(mb) % 2 == 1:
            print("The parity on column is good! :D")
        else:
            print("The parity on column is BAD! :-(")
        ## Optional, as it will be closed when ExitStack is closed:
        magic_square.close()

def main():
    # Usually works, but sometimes times out without apparent reason:
    print("=== Let's try a single exec")
    one_exec()
    # print("=== Let's try another single exec")
    # one_exec()
    # Fails:
    print("=== Let's try two parallel exec")
    parallel_epr()
            
if __name__ == '__main__':
    main()
