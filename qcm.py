
import database as db
import random
#np.random.seed(0)
#df = pd.DataFrame(np.random.randn(5,3), columns=list('ABC'))

def add_question(question: str, subject: str, use: str, correct: str, \
                 responseA: str, responseB: str, responseC: str, responseD: str) -> bool:
    request = db.add_question(question, subject, use, correct, \
                              responseA, responseB, responseC, responseD)
    return request    

def get_qcm(use: str, subjects: list, nbr: int) -> list:
    '''
    '''
    mylist = db.get_questions(use, subjects)
    print (' get_qcm', use, subjects, nbr)
    return mylist[:nbr]

def get_qcm_random (use: str, subjects: list, nbr: int) -> list:
    '''
    '''
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
    #print (number in authorized_numbers, \
    #      use in authorized_uses,\
    #      set(subjects).issubset(set(authorized_subjects)))
    if (number in authorized_numbers) and\
       (use in authorized_uses) and\
       (set(subjects).issubset(set(authorized_subjects))):
    #   (subjects in authorized_subjects) :
           return True
    else :
           return False
