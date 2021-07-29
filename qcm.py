
#   /===============\
#  |     qcm.py      |
#   \===============/
#
# This module consist on the logic part of a multitier architecture [1]. 
# A multitier architecture or n-tier arch is architectural pattern in which 
# presentation, application processing (logic) and data management functions are 
# separated [x].
#
# This provides a model by which developers can create flexible and reusable app. 
# By segregating an application into tiers, developers acquire the option of modifying 
# or adding a specific layer, instead of reworking the entire applicationi [x]. 
#
# This is a supplementary layer added to our arch to avoid being stuck to how data 
# is presented/staured (which is in our case a csv file). The goal being, in addition
# to other choices, to enhance the scalability (evolutivity) of the solution. Other 
# measures may be the separation of concerns inplemented using n-tier architecture as
# discussed above.
# 
# AbdelbasetKABOU
#
# [x] https://en.wikipedia.org/wiki/Multitier_architecture


import database as db
import random

def add_question(question: str, subject: str, use: str, correct: str, \
                 responseA: str, responseB: str, responseC: str, responseD: str) -> bool:
    request = db.add_question(question, subject, use, correct, \
                              responseA, responseB, responseC, responseD)
    return request    

def get_qcm(use: str, subjects: list, nbr: int) -> list:
    mylist = db.get_questions(use, subjects)
    print (' get_qcm', use, subjects, nbr)
    return mylist[:nbr]

def get_qcm_random (use: str, subjects: list, nbr: int) -> list:
    print (' get_qcm_random ', use, subjects, nbr)
    mylist = db.get_questions(use, subjects)
    if len(mylist)>nbr:
        return random.sample(mylist, nbr)
    else :
        return mylist

def is_validated(number: int, use: str, subjects: list) -> bool:
    authorized_numbers = [5, 10, 20]
    authorized_uses = db.get_uses()
    authorized_subjects = db.get_subjects()
    if (number in authorized_numbers) and\
       (use in authorized_uses) and\
       (set(subjects).issubset(set(authorized_subjects))):
           return True
    else :
           return False
