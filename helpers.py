def getDbString():
    with open('dbConnectionString.txt', 'r') as myfile:
        data=myfile.read().replace('\n', '')
    return data

