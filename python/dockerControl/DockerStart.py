import docker
from DockerContainerController import DockerContainer

containerName = ['sparkclient', 'sparknamenode', 'sparkdatanode', 'sparknodemanager', 'sparkresourcemanager']
containerVolume = {'e:/kiha/sharedDir/hadoop' : {'bind' : '/hadoop', 'mode': 'rw'} \
            ,'e:/kiha/shDir' : {'bind' : '/var/shDir', 'mode': 'rw'}}
containerIp = ['172.18.0.2', '172.18.0.3', '172.18.0.4', '172.18.0.5', '172.18.0.6']
execCommand = [['sudo', '-u', 'hdfs', 'hdfs', 'namenode', '-format'], \
    ['service', 'hadoop-hdfs-datanode', 'start'], \
    ['service', 'hadoop-hdfs-namenode', 'start'], \
    ['service', 'hadoop-yarn-nodemanager', 'start'], \
    ['service', 'hadoop-yarn-resourcemanager', 'start']]
imageName =  ['is8200/sparkclient:0.2', 'is8200/sparknamenode:0.2', 'is8200/sparkdatanode:0.2', 'is8200/sparknodemanager:0.2', 'is8200/sparkresourcemanager:0.2']


#노드 올림
container = DockerContainer()

container.open(imageName[0], containerName[0], containerVolume, containerIp[0])
container.open(imageName[1], containerName[1], {}, containerIp[1])
container.open(imageName[2], containerName[2], {}, containerIp[2])
#노드 포맷 및 구동
container.exec(containerName[1], execCommand[0])
container.exec(containerName[2], execCommand[1])
container.exec(containerName[1], execCommand[2])
#hdfs 작성
mkHdfs = [['sudo', '-u', 'hdfs', 'hdfs', 'dfs', '-mkdir', '-p', '/hadoop/tmp'], \
    ['sudo', '-u', 'hdfs', 'hdfs', 'dfs', '-chmod', '777', '/hadoop/tmp'], \
    ['sudo', '-u', 'hdfs', 'hdfs', 'dfs', '-mkdir', '-p', '/tmp'], \
    ['sudo', '-u', 'hdfs', 'hdfs', 'dfs', '-chmod', '777', '/tmp'], \
    ['sudo', '-u', 'hdfs', 'hdfs', 'dfs', '-mkdir', '-p', '/hadoop/yarn/app-logs'], \
    ['sudo', '-u', 'hdfs', 'hdfs', 'dfs', '-chmod', '777', '/hadoop/yarn/app-logs'], \
    ['sudo', '-u', 'hdfs', 'hdfs', 'dfs', '-mkdir', '-p', '/user/root'], \
    ['sudo', '-u', 'hdfs', 'hdfs', 'dfs', '-chown', 'root:hadoop', '/user/root']]

for idx, val in enumerate(mkHdfs):
    container.exec(containerName[0], val)
#매니저 올림
container.open(imageName[3], containerName[3], {}, containerIp[3])
container.open(imageName[4], containerName[4], {}, containerIp[4])
#매니저 구동
container.exec(containerName[3], execCommand[3])
container.exec(containerName[4], execCommand[4])

#노드 개수 창 띄우기
#resultLog = container.exec(containerName[0],  ['sudo', '-u', 'hdfs', 'hdfs', 'dfsadmin', '-report'])
#print(resultLog)
#sparkClient.close()
