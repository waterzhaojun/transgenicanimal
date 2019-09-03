def strain(animalid):
    s = animalid.split('-')[0:-1]
    s = ''.join(s)
    return(s)

def name_title(fullname):
    tmp = fullname.split('-')
    if len(tmp) >1:
        num_length = len(tmp[-1])
        title = fullname[0:int(len(fullname)-num_length-1)]
    else:
        title=fullname
    return(title)