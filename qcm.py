
import database as db
import random
#np.random.seed(0)
#df = pd.DataFrame(np.random.randn(5,3), columns=list('ABC'))



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
    return random.sample(mylist, nbr)


