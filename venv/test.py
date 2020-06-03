
def abc():
    enable = True
    i=0
    if enable:
        enable = False
        i=i+1
        return True,i
    return False,i
print(abc())