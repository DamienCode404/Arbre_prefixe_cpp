import sys
import random
import textwrap

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

SEED = 41

minsize = 1

def int_parameter(s):
    try:
        return int(s)
    except ValueError:
        print(f"ERREUR: {s} n'est pas un entier",file=sys.stderr)
        exit(2)
        

def create_original_string(k):
    return ''.join(random.choices(['A','T','C','G'],k=k))

def prefix(s,k):
    return s[0:k]

def suffix(s,k):
    return s[-(k+1):]

def blast_string(s, k, minov, maxov, f):

    L = textwrap.wrap(s,len(s)//k)
    if len(L) != k:
        L[-2] += L[-1]
        del L[-1]
    print(k,file=f)
    strands=[f"{L[0]}{prefix(L[1],random.randint(minov,maxov))}"]
    for i in range(1,len(L)-1):
        if random.choice([True,False]):
            strands.append(f"{suffix(L[i-1],random.randint(minov,maxov))}{L[i]}{prefix(L[i+1],random.randint(minov,maxov))}")
        else:
            strands.append(f"{suffix(L[i-1],random.randint(minov,maxov))}{L[i]}")
    strands.append(f"{suffix(L[-2],random.randint(minov,maxov))}{L[-1]}")
    random.shuffle(strands)
    print(*strands,sep="\n",file=f)
    print(s,file=f)  
    
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("ERREUR: un message d'erreur ici", file=sys.stderr)
        exit(1)
    random.seed(SEED)
    filename = sys.argv[1]
    strsz = int_parameter(sys.argv[2])
    nsubs = int_parameter(sys.argv[3])
    if not (3 < nsubs < strsz//minsize):
        print(f"ERREUR: Le nombre de sous-chaînes doit être compris entre 3 et {strsz//minsize}.", file=sys.stderr)
        exit(3)

    sizesub = strsz // nsubs
    if len(sys.argv) < 5:
        minov = 1
        maxov = sizesub - 1
    else:
        minov = int_parameter(sys.argv[4])
        if len(sys.argv) < 6:
            maxov = sizesub - 1
        else:
            maxov = int_parameter(sys.argv[5])
            
    if sizesub <= minov or minov < 1 or sizesub <= maxov or maxov < minov:
        print(f"ERREUR: les overlaps doivent avoir une valeur dans [1,{sizesub-1}]",
              file=sys.stderr)
        exit(4)
        
    try:
        if filename == "-":
            blast_string(create_original_string(strsz), nsubs, minov, maxov, sys.stdout)
        else:
            with open(filename,"w") as f:
                blast_string(create_original_string(strsz), nsubs, minov, maxov, f)
    except PermissionError:
        print(f"ERREUR: Le fichier {filename} ne peut être ouvert en écriture",
              file=sys.stderr)
        exit(5)
    except Exception as e:
        print(f"ERREUR: {e}")
        exit(6)
            

    
