def getDbString(platform="dev"):
    connectionStringFiles = {"dev" : 'dbConnectionString.txt', "prod" : 'prodConnectionString.txt'}
    fileName = connectionStringFiles[platform]
    with open(fileName, 'r') as myfile:
        data=myfile.read().replace('\n', '')
    return data

